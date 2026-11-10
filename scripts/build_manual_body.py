#!/usr/bin/env python3
"""
Gera o CORPO do Manual de Implementação — Projeto Célia Lima.
Documento técnico editorial de 14 páginas que documenta todo o caminho percorrido.
"""

import os
import sys
import hashlib
import platform
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, PageBreak, Spacer, KeepTogether,
    CondPageBreak, HRFlowable, Table, TableStyle
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

PDF_SKILL_DIR = "/home/z/my-project/skills/pdf"
sys.path.insert(0, os.path.join(PDF_SKILL_DIR, "scripts"))
try:
    from pdf import install_font_fallback
except Exception:
    install_font_fallback = None

# --- Paths -------------------------------------------------------------------
OUT_DIR = Path("/home/z/my-project/download")
OUT_DIR.mkdir(parents=True, exist_ok=True)
BODY_PDF = OUT_DIR / "manual-celia-corpo.pdf"

# --- Font Registration -------------------------------------------------------
_IS_MAC = platform.system() == 'Darwin'
FONT_DIR = os.path.expanduser('~/.openclaw/workspace/fonts') if _IS_MAC else '/usr/share/fonts'

pdfmetrics.registerFont(TTFont('NotoSerifSC', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSerifSC-Bold', f'{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))

registerFontFamily('NotoSerifSC', normal='NotoSerifSC', bold='NotoSerifSC-Bold')
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold',
                   italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')

if install_font_fallback:
    try:
        install_font_fallback()
    except Exception as e:
        print(f"[warn] install_font_fallback falhou: {e}")

# --- Palette (acolhedor terapêutico) -----------------------------------------
PAGE_BG       = colors.HexColor('#faf6f1')
TEXT_PRIMARY  = colors.HexColor('#3d3530')
TEXT_MUTED    = colors.HexColor('#838179')
ACCENT        = colors.HexColor('#a05a3c')   # terracota
ACCENT_2      = colors.HexColor('#7a8a5b')   # verde sálvia
BORDER        = colors.HexColor('#e3dccd')
CARD_BG       = colors.HexColor('#f4ede1')
HEADER_FILL   = colors.HexColor('#5a5239')

BODY_FONT = 'NotoSerifSC'
BOLD_FONT = 'NotoSerifSC-Bold'

# --- Estilos -----------------------------------------------------------------
styles = {}

styles['kicker'] = ParagraphStyle(
    name='Kicker', fontName=BODY_FONT, fontSize=9, leading=12,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=0, spaceAfter=4,
)

styles['h1'] = ParagraphStyle(
    name='H1', fontName=BOLD_FONT, fontSize=22, leading=28,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=0, spaceAfter=12,
)

styles['h2'] = ParagraphStyle(
    name='H2', fontName=BOLD_FONT, fontSize=14, leading=18,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=14, spaceAfter=6,
)

styles['h3'] = ParagraphStyle(
    name='H3', fontName=BOLD_FONT, fontSize=11.5, leading=15,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=8, spaceAfter=3,
)

styles['body'] = ParagraphStyle(
    name='Body', fontName=BODY_FONT, fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_JUSTIFY,
    spaceBefore=0, spaceAfter=8, firstLineIndent=12,
)

styles['body_first'] = ParagraphStyle(
    name='BodyFirst', fontName=BODY_FONT, fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_JUSTIFY,
    spaceBefore=0, spaceAfter=8, firstLineIndent=0,
)

styles['quote'] = ParagraphStyle(
    name='Quote', fontName='FreeSerif-Italic', fontSize=11, leading=16,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=10, spaceAfter=10,
    leftIndent=20, rightIndent=20, firstLineIndent=0,
)

styles['meta'] = ParagraphStyle(
    name='Meta', fontName='FreeSerif-Italic', fontSize=9, leading=12,
    textColor=TEXT_MUTED, alignment=TA_LEFT, spaceBefore=4, spaceAfter=10,
)

styles['table_header'] = ParagraphStyle(
    name='TableHeader', fontName=BOLD_FONT, fontSize=10, leading=13,
    textColor=colors.white, alignment=TA_LEFT,
)

styles['table_cell'] = ParagraphStyle(
    name='TableCell', fontName=BODY_FONT, fontSize=9.5, leading=13,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT,
)

styles['table_cell_bold'] = ParagraphStyle(
    name='TableCellBold', fontName=BOLD_FONT, fontSize=9.5, leading=13,
    textColor=ACCENT, alignment=TA_LEFT,
)

styles['stat_number'] = ParagraphStyle(
    name='StatNumber', fontName=BOLD_FONT, fontSize=28, leading=32,
    textColor=ACCENT, alignment=TA_CENTER, spaceBefore=0, spaceAfter=4,
)

styles['stat_label'] = ParagraphStyle(
    name='StatLabel', fontName=BODY_FONT, fontSize=9, leading=12,
    textColor=TEXT_MUTED, alignment=TA_CENTER, spaceBefore=0, spaceAfter=0,
)


# --- TocDocTemplate ----------------------------------------------------------
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))


def add_heading(text, style, level=0):
    key = 'h_' + hashlib.md5((text + str(level)).encode()).hexdigest()[:8]
    p = Paragraph(f'<a name="{key}"/>{text}', style)
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p


# --- Header / Footer ---------------------------------------------------------
def draw_header_footer(canvas, doc):
    canvas.saveState()
    page_w, page_h = A4
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.4)
    canvas.line(0.85 * inch, 0.55 * inch, page_w - 0.85 * inch, 0.55 * inch)

    canvas.setFont(BODY_FONT, 9)
    canvas.setFillColor(TEXT_MUTED)
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(page_w / 2, 0.36 * inch, str(page_num))

    canvas.setFont(BODY_FONT, 8.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(0.85 * inch, page_h - 0.5 * inch, 'Manual de Implementação · Projeto Célia Lima')
    canvas.drawRightString(page_w - 0.85 * inch, page_h - 0.5 * inch, 'Dalila Teles Veras')
    canvas.restoreState()


# --- Helpers ----------------------------------------------------------------
def make_table(data, col_widths, header_row=True):
    available_width = A4[0] - 2 * 0.85 * inch
    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0, 1 if header_row else 0), (-1, -1), [colors.white, CARD_BG]),
    ]
    if header_row:
        style_cmds.append(('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL))
    t.setStyle(TableStyle(style_cmds))
    return t


def stat_card(number, label, width):
    """Card com número grande + label embaixo, tipo 'estatística em destaque'."""
    data = [
        [Paragraph(number, styles['stat_number'])],
        [Paragraph(label, styles['stat_label'])],
    ]
    t = Table(data, colWidths=[width])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    return t


# ============================================================================
# SEÇÕES DO MANUAL
# ============================================================================

def section_visao_geral():
    """Página 2 — Visão geral."""
    flow = []
    flow.append(Paragraph('Visão geral', styles['kicker']))
    flow.append(add_heading('O que foi construído', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(Paragraph(
        'Este manual documenta, em 7 fases, todo o processo de construção do '
        'site institucional + blog terapêutico da psicoterapeuta Célia Lima — '
        'desde a extração dos 98 artigos publicados na plataforma Personare '
        'até o deploy final na Vercel. O documento serve como referência '
        'técnica, material de portfólio e base para propostas comerciais '
        'futuras. Cada fase traz: contexto, decisões tomadas, ferramentas '
        'utilizadas, entregáveis concretos e lições aprendidas.',
        styles['body_first']))

    # Estatísticas em destaque (4 cards)
    available_width = A4[0] - 2 * 0.85 * inch
    gap = 8
    card_w = (available_width - 3 * gap) / 4
    stats = [
        ("98", "artigos extraídos do Personare"),
        ("250", "páginas no livro PDF gerado"),
        ("16", "rotas no site Next.js"),
        ("7", "contextos terapêuticos curados"),
    ]
    stats_row = [[stat_card(n, l, card_w) for n, l in stats]]
    stats_table = Table(stats_row, colWidths=[card_w] * 4, hAlign='CENTER')
    stats_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), gap / 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), gap / 2),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    flow.append(Spacer(1, 6))
    flow.append(stats_table)
    flow.append(Spacer(1, 10))

    flow.append(Paragraph(
        'O projeto partiu de uma pergunta simples: "como tirar o conteúdo '
        'da Célia de uma plataforma terceira e dar a ela posse completa da '
        'própria obra?". A resposta evoluiu em camadas: primeiro preservar '
        '(extração + livro PDF), depois posicionar (briefing de marca), '
        'finalmente publicar (site no ar). Cada camada entregou um artefato '
        'concreto que compõe o produto final.',
        styles['body']))

    flow.append(Paragraph(
        'Toda a construção foi feita no ambiente Z.ai, com deploy final '
        'para GitHub (versionamento) + Vercel (hospedagem). O código-fonte '
        'está disponível no repositório <b>celialima-psicoterapia</b> e o '
        'site no ar em <b>celialima-psicoterapia-cw1u.vercel.app</b>.',
        styles['body']))

    flow.append(Spacer(1, 6))
    flow.append(Paragraph(
        '"Documento vivo — acompanha o ritmo da cliente e da desenvolvedora."',
        styles['quote']))
    return flow


def section_linha_do_tempo():
    """Página 3 — Linha do tempo das 7 fases."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Linha do tempo', styles['kicker']))
    flow.append(add_heading('As sete fases do projeto', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(Paragraph(
        'O projeto aconteceu em 7 fases consecutivas. Algumas eram pré-requisito '
        'para outras (não dá fazer o site sem antes ter o conteúdo organizado); '
        'outras poderiam ser refeitas a qualquer momento (refinamentos de '
        'design). A tabela abaixo mostra a sequência, a duração aproximada e o '
        'entregável principal de cada fase.',
        styles['body_first']))
    flow.append(Spacer(1, 8))

    header = [
        Paragraph('<b>#</b>', styles['table_header']),
        Paragraph('<b>Fase</b>', styles['table_header']),
        Paragraph('<b>O que aconteceu</b>', styles['table_header']),
        Paragraph('<b>Entregável</b>', styles['table_header']),
    ]
    rows = [
        ['1', 'Descoberta e Extração',
         'Investigação técnica do Personare + scraping dos 98 artigos',
         'Planilha Excel + 98 Markdowns'],
        ['2', 'Organização do Conteúdo',
         'Categorização manual em 7 contextos + tags SEO + auditoria',
         'Planilha revisão + JSON único'],
        ['3', 'Livro PDF',
         'Design editorial, 250 págs, 6 capítulos por categoria',
         'Caminhos do Autoconhecimento.pdf'],
        ['4', 'Briefing de Marca',
         'Posicionamento profissional (psicoterapeuta não holístico)',
         'Briefing-de-Marca-Celia-Lima.pdf'],
        ['5', 'Desenvolvimento Next.js',
         '16 rotas, funil TOFU/MOFU/BOFU, articulação cruzada',
         'Site Next.js 16 + TypeScript'],
        ['6', 'Refinamentos',
         'Hero com overlay, contextos com 2 colunas, tags visíveis',
         'Site v2 + v3 + v4'],
        ['7', 'Deploy',
         'GitHub (.gitignore) + Vercel + variáveis de ambiente',
         'Site no ar em produção'],
    ]

    table_data = [header]
    for r in rows:
        table_data.append([
            Paragraph(f"<b>{r[0]}</b>", styles['table_cell_bold']),
            Paragraph(r[1], styles['table_cell_bold']),
            Paragraph(r[2], styles['table_cell']),
            Paragraph(r[3], styles['table_cell']),
        ])

    available_width = A4[0] - 2 * 0.85 * inch
    col_widths = [
        available_width * 0.06,
        available_width * 0.24,
        available_width * 0.42,
        available_width * 0.28,
    ]
    flow.append(make_table(table_data, col_widths))
    flow.append(Spacer(1, 10))
    flow.append(Paragraph(
        'Cada fase foi documentada com log de trabalho (worklog.md) e '
        'snapshots de backup ao final. Em caso de regressão — como '
        'aconteceu na Fase 5, quando o ambiente reiniciou e perdeu parte '
        'das alterações — foi possível restaurar a partir do backup ZIP '
        'mais recente.',
        styles['body']))
    return flow


def section_fase1():
    """Página 4 — Fase 1: Descoberta e Extração."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Fase 1', styles['kicker']))
    flow.append(add_heading('Descoberta e Extração', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(add_heading('Contexto', styles['h3'], level=1))
    flow.append(Paragraph(
        'A Célia tinha 98 artigos publicados na plataforma Personare. '
        'Após um desentendimento com a equipe, ela queria sair de lá e '
        'precisava de uma cópia completa do próprio conteúdo — título, '
        'data, categoria, palavras-chave e texto integral. O desafio '
        'inicial era: existe um jeito de extrair isso tudo sem copiar e '
        'colar manualmente 98 páginas?',
        styles['body_first']))

    flow.append(add_heading('Investigação técnica', styles['h3'], level=1))
    flow.append(Paragraph(
        'Antes de escrever qualquer código, foi necessário investigar a '
        'página de autora do Personare. Conclusões da análise:',
        styles['body']))
    flow.append(Paragraph(
        '• As páginas de artigo são renderizadas no servidor (SSR) — '
        'disponíveis no HTML retornado por HTTP simples, sem precisar '
        'de browser headless.<br/>'
        '• Os artigos não estão atrás de paywall ou login — qualquer '
        'pessoa pode acessar.<br/>'
        '• Cada artigo tem JSON-LD embutido (metadados estruturados) com '
        'título, data de publicação original, keywords e thumbnail.<br/>'
        '• O robots.txt não proíbe scraping das rotas <i>/autor/</i> e '
        '<i>/conteudo/</i> — eticamente liberado.',
        styles['body']))

    flow.append(add_heading('Decisões técnicas', styles['h3'], level=1))
    flow.append(Paragraph(
        'Optou-se por Python + BeautifulSoup + requests (HTTP simples). '
        'Playwright só foi usado para coletar a lista inicial de 98 URLs, '
        'porque a página de autora usa JavaScript para paginar. Depois, '
        'cada artigo foi baixado via HTTP direto, com User-Agent próprio '
        '("CeliaLimaArchiveBot") e delay de 0.6s entre requisições por '
        'cortesia.',
        styles['body']))

    flow.append(add_heading('Entregável', styles['h3'], level=1))
    flow.append(Paragraph(
        '98 arquivos Markdown (um por artigo, ~864 KB total) com frontmatter '
        'YAML completo (título, slug, categoria, data de publicação, '
        'palavras-chave, thumbnail, contagem de palavras) + uma planilha '
        'Excel de auditoria com 2 abas: "Artigos Célia Lima" (98 linhas) e '
        '"Resumo por categoria" (10 categorias com totais).',
        styles['body']))

    flow.append(add_heading('Lição aprendida', styles['h3'], level=1))
    flow.append(Paragraph(
        'Antes de codar, investigar a estrutura do site alvo economiza '
        'horas de trabalho. A descoberta de que os artigos eram SSR '
        'eliminou a necessidade de browser headless em 99% do processo — '
        'de ~5 minutos por artigo para ~0.6 segundos por artigo.',
        styles['body']))
    return flow


def section_fase2():
    """Página 5 — Fase 2: Organização do Conteúdo."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Fase 2', styles['kicker']))
    flow.append(add_heading('Organização do Conteúdo', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(add_heading('Contexto', styles['h3'], level=1))
    flow.append(Paragraph(
        'Os 98 artigos tinham 11 categorias originais do Personare '
        '(Autoconhecimento, Amor, Família, Saúde, Carreira, etc.). Para '
        'o site novo, precisávamos de uma estrutura que servisse ao '
        'funil de vendas (TOFU/MOFU/BOFU) e ao SEO/GEO — o que significa '
        'agrupar por <b>dor/pergunta do leitor</b>, não por "área da vida".',
        styles['body_first']))

    flow.append(add_heading('Primeira classificação (automática)', styles['h3'], level=1))
    flow.append(Paragraph(
        'Script Python com heurística por palavras-chave no título + corpo. '
        'Resultado: 10 contextos automáticos com distribuição razoável. '
        'Problemático: algumas palavras-chave geravam falsos positivos, e '
        'a Célia não tinha controle sobre a classificação.',
        styles['body']))

    flow.append(add_heading('Segunda classificação (manual pela Célia)', styles['h3'], level=1))
    flow.append(Paragraph(
        'Célia preencheu uma planilha Excel com classificação manual: '
        'cada um dos 98 artigos recebeu (a) um contexto terapêutico, '
        '(b) tipo — Reflexiva ou Prática, (c) 1-4 tags SEO. Após duas '
        'iterações (a primeira tinha registros redundantes por filtro '
        'escondido), consolidamos em 7 contextos finais.',
        styles['body']))

    flow.append(add_heading('Os 7 contextos finais', styles['h3'], level=1))

    header = [
        Paragraph('<b>Contexto</b>', styles['table_header']),
        Paragraph('<b>Qtd. artigos</b>', styles['table_header']),
        Paragraph('<b>Descrição curta</b>', styles['table_header']),
    ]
    rows = [
        ['Dinâmica Familiar e Criação de Filhos', '21',
         'Mães, pais, filhos, sogras, avós. A família como primeiro espelho.'],
        ['Relacionamentos Amorosos e Sexualidade', '21',
         'Amor, parceria, sexo, escolhas, separação.'],
        ['Autocrítica, Limites e Autoestima', '14',
         'Dizer não, reconhecer valor próprio, calar o juiz interior.'],
        ['Sintomas Psicossomáticos e Saúde Emocional', '12',
         'Emoção que vira sintoma, doença como mensagem.'],
        ['Ansiedade, Estresse e Esgotamento', '12',
         'Quando o corpo pede calma e a cabeça não consegue parar.'],
        ['Espiritualidade e Autoconhecimento', '11',
         'Espiritualidade no cotidiano, meditação, paz interior.'],
        ['Produtividade, Carreira e Organização', '7',
         'Vocação, propósito, trabalho como construção de sentido.'],
    ]
    table_data = [header]
    for r in rows:
        table_data.append([
            Paragraph(r[0], styles['table_cell_bold']),
            Paragraph(r[1], styles['table_cell']),
            Paragraph(r[2], styles['table_cell']),
        ])
    available_width = A4[0] - 2 * 0.85 * inch
    col_widths = [available_width * 0.32, available_width * 0.15, available_width * 0.53]
    flow.append(make_table(table_data, col_widths))
    flow.append(Spacer(1, 8))

    flow.append(add_heading('Entregável', styles['h3'], level=1))
    flow.append(Paragraph(
        'JSON único (712 KB) com 98 artigos classificados + planilha de '
        'auditoria (categorizacao-cruzamento.xlsx) com 98/98 match SIM. '
        'Esse JSON alimenta o site Next.js direto, sem banco de dados em '
        'runtime.',
        styles['body']))

    flow.append(add_heading('Lição aprendida', styles['h3'], level=1))
    flow.append(Paragraph(
        'Classificação automática é bom pra começar, mas a curadoria '
        'humana da própria autora gera um resultado qualitativamente '
        'superior. As tags curadas pela Célia ("Luto da Separação", '
        '"Carência Afetiva", "Codependência") são exatamente o formato '
        'que LLMs (ChatGPT, Perplexity) usam pra citar sites — vantagem '
        'GEO que só mão humana entrega.',
        styles['body']))
    return flow


def section_fase3():
    """Página 6 — Fase 3: Livro PDF."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Fase 3', styles['kicker']))
    flow.append(add_heading('Livro PDF', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(add_heading('Contexto', styles['h3'], level=1))
    flow.append(Paragraph(
        'Antes de existir site, fazia sentido criar um artefato que desse '
        'à Célia a posse imediata de toda a obra, num formato que ela '
        'pudesse imprimir, enviar por WhatsApp, ou simplesmente guardar. '
        'Um livro PDF resolve isso: é portátil, é permanente, é "dela".',
        styles['body_first']))

    flow.append(add_heading('Decisões de design', styles['h3'], level=1))
    flow.append(Paragraph(
        'Paleta acolhedora terapêutica (areia #faf6f1, terracota #a05a3c, '
        'verde sálvia #7a8a5b, marrom-escuro quente #3d3530). Tipografia '
        'Cormorant Garamond (títulos) + Noto Serif SC (corpo) + FreeSerif '
        '(itálicos e números). Estrutura editorial: capa em HTML/Playwright '
        '+ corpo em ReportLab com sumário automático (TocDocTemplate + '
        'multiBuild), numeração de páginas, cabeçalho/rodapé discretos, '
        'sem quebras de página entre capítulos (regra de fluxo contínuo).',
        styles['body']))

    flow.append(add_heading('Estrutura final', styles['h3'], level=1))
    flow.append(Paragraph(
        '250 páginas em 6 capítulos por categoria, cada um com prefácio '
        'curto + artigos em ordem cronológica (do mais antigo ao mais '
        'recente, pra acompanhar a maturação das ideias). Apresentação '
        'inicial + nota final explicando a origem da coletânea. Após '
        'refinamento solicitado pela cliente, os títulos dos artigos '
        'foram coloridos em terracota + linha divisória sutil no fim de '
        'cada artigo, pra facilitar a navegação visual.',
        styles['body']))

    flow.append(add_heading('Entregável', styles['h3'], level=1))
    flow.append(Paragraph(
        'Caminhos-do-Autoconhecimento.pdf (252 páginas, 942 KB). '
        'Disponível tanto na pasta <i>download</i> do projeto quanto '
        'integrado ao site (página /livro com botão de download '
        'gratuito). Também foi gerado um briefing de marca em PDF '
        '(6 páginas, 191 KB) — ver Fase 4.',
        styles['body']))

    flow.append(add_heading('Lição aprendida', styles['h3'], level=1))
    flow.append(Paragraph(
        'Capa em HTML + corpo em ReportLab é o melhor dos dois mundos: '
        'design visual sofisticado na capa (Playwright renderiza CSS, '
        'Google Fonts, gradientes) + conteúdo estruturado tipograficamente '
        'no corpo (ReportLab lida bem com TOC, paginação, KeepTogether). '
        'Mesclar via pypdf no fim. Evita a tentação de fazer tudo num '
        'só — cada ferramenta no que é melhor.',
        styles['body']))
    return flow


def section_fase4():
    """Página 7 — Fase 4: Briefing de Marca."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Fase 4', styles['kicker']))
    flow.append(add_heading('Briefing de Marca', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(add_heading('Contexto', styles['h3'], level=1))
    flow.append(Paragraph(
        'Conversando com a cliente (a desenvolvedora), surgiu a preocupação: '
        '"como posicionar a Célia longe da cesta genérica dos terapeutas '
        'holísticos?". A Célia tem 30 anos de experiência, formação em '
        'psicosíntese e análise junguiana — mas se apresentava como '
        '"terapeuta holística", o que dilui seu valor comercial.',
        styles['body_first']))

    flow.append(add_heading('Decisão estratégica', styles['h3'], level=1))
    flow.append(Paragraph(
        'Reposicionar como <b>psicoterapeuta de orientação junguiana e '
        'psicosíntese</b>. Razões: (1) mercado saturado de holísticos, '
        '(2) formação dela é real e dá pra usar com honestidade, (3) o '
        'cliente que ela quer atrai não procura "holístico", procura '
        'trabalho profundo, (4) SEO/GEO: nicho vence generalista.',
        styles['body']))

    flow.append(add_heading('Conteúdo do briefing', styles['h3'], level=1))
    flow.append(Paragraph(
        'Documento de 6 páginas cobrindo: (1) resumo executivo, (2) '
        'argumento de posicionamento, (3) método traduzido em 3 cards '
        'pra leigo (Subpersonalidades, Símbolos e Sonhos, Sentido e '
        'Totalidade), (4) 4 serviços modelados (psicoterapia individual, '
        'escuta inicial, mentoria pontual, grupo), (5) mentoria em 5 '
        'fases (diagnóstico → serviços → copy → colunas editoriais → '
        'CMS), (6) convite pra Célia riscar o que não fizer sentido.',
        styles['body']))

    flow.append(add_heading('Entregável', styles['h3'], level=1))
    flow.append(Paragraph(
        'Briefing-de-Marca-Celia-Lima.pdf (6 páginas, 191 KB), mesma '
        'paleta visual do site e do livro, pra criar identidade visual '
        'unificada entre todos os artefatos do projeto. Mandado pra '
        'Célia no WhatsApp pra ler com calma e marcar o que concorda.',
        styles['body']))

    flow.append(add_heading('Lição aprendida', styles['h3'], level=1))
    flow.append(Paragraph(
        'Briefing de marca é o documento que vende o "porquê" do projeto. '
        'Antes de codar site, definir identidade. Um briefing de 6 '
        'páginas é mais eficiente que 10 reuniões — dá pra Célia ler, '
        'marcar, devolver, e a desenvolvedora trabalha a partir disso. '
        'Identidade visual unificada (paleta + tipografia) entre briefing, '
        'livro e site é diferencial profissional que custa pouco e vale '
        'muito.',
        styles['body']))
    return flow


def section_fase5():
    """Página 8 — Fase 5: Desenvolvimento Next.js."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Fase 5', styles['kicker']))
    flow.append(add_heading('Desenvolvimento Next.js', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(add_heading('Contexto', styles['h3'], level=1))
    flow.append(Paragraph(
        'Com conteúdo extraído (Fase 1-2) e posicionamento definido '
        '(Fase 4), faltava construir o site que pudesse tudo isso. Stack '
        'escolhida: Next.js 16 (App Router, Turbopack) + TypeScript 5 '
        '+ Tailwind CSS 4 com shadcn/ui. Sem banco de dados em runtime — '
        'JSON estático alimenta o site (decisão consciente: '
        'a Célia não vai editar sozinha no primeiro ano).',
        styles['body_first']))

    flow.append(add_heading('Arquitetura de rotas', styles['h3'], level=1))

    header = [
        Paragraph('<b>Rota</b>', styles['table_header']),
        Paragraph('<b>Tipo</b>', styles['table_header']),
        Paragraph('<b>Conteúdo</b>', styles['table_header']),
    ]
    rows = [
        ['/', 'Estática', 'Home com hero + 7 cards de contexto + artigo da semana'],
        ['/sobre', 'Estática', 'Bio da Célia + 3 cards de método'],
        ['/atendimento', 'Estática', 'Abordagem + 4 serviços + 3 cards de método'],
        ['/saude-mental', 'Client', 'Lista de 67 artigos com busca + filtro'],
        ['/saude-mental/[slug]', 'Dinâmica (SSG)', '98 páginas de artigos individuais'],
        ['/caixa-de-ferramentas', 'Client', 'Lista de 31 práticas com busca + filtro'],
        ['/caixa-de-ferramentas/[slug]', 'Dinâmica (SSG)', '31 páginas de práticas individuais'],
        ['/contextos/[slug]', 'Dinâmica (SSG)', '7 páginas, uma por contexto'],
        ['/livro', 'Estática', 'Vitrine do PDF + download'],
        ['/contato', 'Client', 'Formulário que monta link WhatsApp'],
        ['/termos, /privacidade, /direitos-autorais', 'Estática', '3 páginas legais'],
    ]
    table_data = [header]
    for r in rows:
        table_data.append([
            Paragraph(r[0], styles['table_cell_bold']),
            Paragraph(r[1], styles['table_cell']),
            Paragraph(r[2], styles['table_cell']),
        ])
    available_width = A4[0] - 2 * 0.85 * inch
    col_widths = [available_width * 0.32, available_width * 0.18, available_width * 0.50]
    flow.append(make_table(table_data, col_widths))
    flow.append(Spacer(1, 8))

    flow.append(add_heading('Funil de vendas integrado', styles['h3'], level=1))
    flow.append(Paragraph(
        'TOFU (conscientização): busca no Google cai num artigo → página '
        'do artigo tem tag + keywords + sumário + OpenGraph otimizado. '
        'MOFU (consideração): fim do artigo sugere "Práticas relacionadas '
        'a este texto" → Caixa de Ferramentas. Prática tem "Textos para '
        'acompanhar esta prática" → volta pra Saúde Mental. BOFU (decisão): '
        'CTA em todas as páginas → /contato → formulário que monta link '
        'WhatsApp.',
        styles['body']))

    flow.append(add_heading('Articulação cruzada', styles['h3'], level=1))
    flow.append(Paragraph(
        'Cada artigo mostra até 3 práticas do mesmo contexto (não '
        'mais "1 prática coerente" — lista, dá mais opções pro leitor). '
        'Recíproco: cada prática mostra até 3 artigos do mesmo contexto. '
        'Implementado via helpers <i>getPraticasRelacionadas</i> e '
        '<i>getArtigosRelacionados</i> em lib/articles.ts.',
        styles['body']))

    flow.append(add_heading('Entregável', styles['h3'], level=1))
    flow.append(Paragraph(
        'Site Next.js 16 completo, 16 rotas, ~3000 linhas de TypeScript, '
        'lint passando sem erros, todas as rotas retornando 200. Backup '
        'ZIP disponível para portfólio.',
        styles['body']))
    return flow


def section_fase6():
    """Página 9 — Fase 6: Refinamentos."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Fase 6', styles['kicker']))
    flow.append(add_heading('Refinamentos', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(add_heading('Contexto', styles['h3'], level=1))
    flow.append(Paragraph(
        'Após o site inicial funcionar, começou um ciclo de refinamentos '
        'baseados em (a) feedback da cliente sobre o que ressoava com a '
        'estratégia comercial e (b) decisões de design tomadas pela '
        'desenvolvedora estudando templates de referência (Stillpoint, '
        'tipo Webflow). Cada refinamento gerava uma versão nova do site.',
        styles['body_first']))

    flow.append(add_heading('Refinamento 1: Hero com overlay', styles['h3'], level=1))
    flow.append(Paragraph(
        'Troca do hero original (foto da Célia à direita + título à esquerda) '
        'por hero com imagem de fundo (montanhas abstratas em SVG, tons '
        'quentes) + overlay (background/55 + gradient) + título centralizado. '
        'Botão "Ler textos" virou "Conheça meu trabalho" → /atendimento. '
        'Cards de contexto ganharam imagem SVG à esquerda, sem numeração.',
        styles['body']))

    flow.append(add_heading('Refinamento 2: Páginas de contexto com 2 colunas', styles['h3'], level=1))
    flow.append(Paragraph(
        'Cada um dos 7 contextos ganhou hero próprio (mesma imagem SVG do '
        'card + overlay + título + descrição introdutória). Abaixo, duas '
        'colunas: esquerda com artigos reflexivos (Saúde Mental) + direita '
        'com práticas relacionadas (Caixa de Ferramentas). Visual editorial '
        'tipo "jornal de psicologia".',
        styles['body']))

    flow.append(add_heading('Refinamento 3: Tags visíveis abaixo do título', styles['h3'], level=1))
    flow.append(Paragraph(
        'As tags SEO curadas pela Célia ("Carência Afetiva", "Luto da '
        'Separação", "Relacionamentos Abusivos") passaram a aparecer '
        'abaixo do título em cada artigo, prática e card de listagem. '
        'Cores diferenciadas: artigos em terracota, práticas em verde '
        'sálvia. CTA pós-artigo também foi renomeado de "prática coerente" '
        'para "Práticas relacionadas a este texto" (lista de até 3).',
        styles['body']))

    flow.append(add_heading('Refinamento 4: Paleta consolidada em 7 contextos', styles['h3'], level=1))
    flow.append(Paragraph(
        'Primeira categorização tinha 10 contextos — dois eram variantes '
        'de "Espiritualidade" e dois eram variantes de "Saúde". Célia '
        'refez a planilha consolidando em 7, mais enxuta. Atualizamos JSON, '
        'lib/articles.ts, SVGs (criamos 4 novos + reaproveitamos 3) e '
        'limpamos os antigos.',
        styles['body']))

    flow.append(add_heading('Lição aprendida', styles['h3'], level=1))
    flow.append(Paragraph(
        'Refinamentos iterativos são normais e esperados. Cliente que '
        'participa do processo de design entrega produto melhor que '
        'cliente que "deixa tudo nas mãos do dev". A diferença: cada '
        'iteração foi <b>pequena e reversível</b> — se a Célia não '
        'gostasse de uma mudança, voltávamos em 5 min. Esse é o padrão '
        'profissional: incrementos pequenos, validação frequente, sem '
        'medo de refazer.',
        styles['body']))
    return flow


def section_fase7():
    """Página 10 — Fase 7: Deploy."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Fase 7', styles['kicker']))
    flow.append(add_heading('Deploy', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(add_heading('Contexto', styles['h3'], level=1))
    flow.append(Paragraph(
        'Com o site pronto, faltava colocá-lo no ar. Estratégia: '
        'GitHub (versionamento + colaboração futura) + Vercel '
        '(hospedagem gratuita + deploy automático a cada push). '
        'Decisão importante: usar conta GitHub + Vercel da própria '
        'desenvolvedora (Dalila), num repositório separado, pra deixar '
        'site no ar imediato. Depois, quando a Célia tiver GitHub próprio, '
        'transfere o repo e ela fica dona do código.',
        styles['body_first']))

    flow.append(add_heading('Passos executados', styles['h3'], level=1))
    flow.append(Paragraph(
        '<b>1.</b> Criação de arquivo <i>.gitignore</i> na raiz do projeto '
        'pra evitar subir node_modules, .next, .env e caches.<br/>'
        '<b>2.</b> <i>git init</i> + <i>git add .</i> + <i>git commit</i> '
        'com mensagem descritiva ("Versão inicial: site da Célia Lima '
        'com 98 artigos, 7 contextos, design acolhedor").<br/>'
        '<b>3.</b> Criação do repositório no GitHub (público) e '
        '<i>git remote add origin</i> + <i>git push -u origin main</i>.<br/>'
        '<b>4.</b> Login na Vercel com conta GitHub + criação do projeto '
        'importando o repositório.<br/>'
        '<b>5.</b> Configuração de variável de ambiente DATABASE_URL '
        '(file:./db/custom.db) — necessária pro Prisma funcionar durante '
        'o build, mesmo sendo SQLite local.<br/>'
        '<b>6.</b> Commit vazio + push pra forçar o primeiro deploy '
        '(<i>git commit --allow-empty -m "Trigger primeiro deploy"</i>).<br/>'
        '<b>7.</b> Deploy pronto em 46s. Site no ar em <b>celialima-'
        'psicoterapia-cw1u.vercel.app</b>.',
        styles['body']))

    flow.append(add_heading('Decisões de segurança', styles['h3'], level=1))
    flow.append(Paragraph(
        'Arquivo .env (com DATABASE_URL) não subiu pro Git — fica só no '
        'computador local. Na Vercel, a variável foi adicionada pela '
        'interface, criptografada. Repositório é público mas não contém '
        'segredos. Backup ZIP de segurança mantido em /download/ no '
        'ambiente de desenvolvimento.',
        styles['body']))

    flow.append(add_heading('Entregável', styles['h3'], level=1))
    flow.append(Paragraph(
        'Site no ar em produção, URL pública funcional, deploy automático '
        'a cada git push. Repositório no GitHub com histórico limpo de '
        'commits. URL: <b>https://celialima-psicoterapia-cw1u.vercel.app</b>.',
        styles['body']))

    flow.append(add_heading('Lição aprendida', styles['h3'], level=1))
    flow.append(Paragraph(
        'Deploy não é o último passo do projeto — é o primeiro passo do '
        'ciclo de vida do site. A partir do momento que está no ar, '
        'toda alteração no código vira novo deploy automático. Isso muda '
        'a relação com o cliente: ele vê o site evoluindo em tempo real, '
        'sem precisar "pedir atualização".',
        styles['body']))
    return flow


def section_stack_tecnico():
    """Página 11 — Stack técnico."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Stack técnico', styles['kicker']))
    flow.append(add_heading('Tecnologias utilizadas', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(Paragraph(
        'Cada tecnologia foi escolhida com critério: fazer uma coisa bem, '
        'sem reinventar a roda. A tabela abaixo mapeia o que foi usado e '
        'em qual fase.',
        styles['body_first']))
    flow.append(Spacer(1, 8))

    header = [
        Paragraph('<b>Tecnologia</b>', styles['table_header']),
        Paragraph('<b>Fase</b>', styles['table_header']),
        Paragraph('<b>Para que serviu</b>', styles['table_header']),
    ]
    rows = [
        ['Python 3.12', '1, 2, 3, 4', 'Scraping, scripts de categorização, geração de PDF (ReportLab)'],
        ['BeautifulSoup 4', '1', 'Parser de HTML dos artigos extraídos do Personare'],
        ['requests', '1', 'Cliente HTTP para baixar 98 artigos'],
        ['openpyxl', '1, 2', 'Geração e leitura de planilhas Excel de auditoria'],
        ['ReportLab', '3, 4', 'Geração do livro PDF e do briefing de marca (corpo)'],
        ['Playwright', '3, 4', 'Renderização de capas HTML para PDF'],
        ['pypdf', '3, 4', 'Mescla capa (Playwright) + corpo (ReportLab)'],
        ['Next.js 16 (App Router, Turbopack)', '5, 6, 7', 'Framework React full-stack para o site'],
        ['TypeScript 5', '5, 6, 7', 'Linguagem tipada para o site'],
        ['Tailwind CSS 4 + shadcn/ui', '5, 6, 7', 'Estilização + componentes de UI'],
        ['Vercel', '7', 'Hospedagem gratuita + deploy automático'],
        ['GitHub', '7', 'Versionamento do código-fonte'],
        ['Git', '7', 'Sistema de versionamento distribuído'],
    ]
    table_data = [header]
    for r in rows:
        table_data.append([
            Paragraph(r[0], styles['table_cell_bold']),
            Paragraph(r[1], styles['table_cell']),
            Paragraph(r[2], styles['table_cell']),
        ])
    available_width = A4[0] - 2 * 0.85 * inch
    col_widths = [available_width * 0.32, available_width * 0.15, available_width * 0.53]
    flow.append(make_table(table_data, col_widths))
    return flow


def section_entregaveis():
    """Página 12 — Entregáveis por fase."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Entregáveis', styles['kicker']))
    flow.append(add_heading('O que foi entregue em cada fase', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(Paragraph(
        'Lista de artefatos concretos produzidos ao longo do projeto. '
        'Cada um é "demonstrável" — dá pra abrir, testar, validar.',
        styles['body_first']))
    flow.append(Spacer(1, 8))

    header = [
        Paragraph('<b>Fase</b>', styles['table_header']),
        Paragraph('<b>Artefato</b>', styles['table_header']),
        Paragraph('<b>Formato/Tamanho</b>', styles['table_header']),
    ]
    rows = [
        ['1', 'celia-lima-artigos.xlsx', 'Excel · 24 KB · 2 abas'],
        ['1', 'celia-lima-artigos/ (pasta de 98 .md)', 'Markdown · 864 KB'],
        ['2', 'articles.json', 'JSON · 712 KB · 98 artigos classificados'],
        ['2', 'classificacao-artigos-celia.xlsx', 'Excel · 19 KB · 3 abas'],
        ['2', 'categorizacao-cruzamento.xlsx', 'Excel · auditoria 98/98'],
        ['3', 'Caminhos-do-Autoconhecimento.pdf', 'PDF · 942 KB · 252 págs'],
        ['4', 'Briefing-de-Marca-Celia-Lima.pdf', 'PDF · 191 KB · 6 págs'],
        ['5-6', 'Site Next.js completo', '16 rotas · ~3000 linhas TS'],
        ['7', 'Repositório GitHub celialima-psicoterapia', '136 arquivos commitados'],
        ['7', 'Deploy na Vercel (URL pública)', 'celialima-psicoterapia-cw1u.vercel.app'],
        ['7', 'site-celia-lima-backup-v4.zip', 'ZIP · 2.2 MB · snapshot final'],
    ]
    table_data = [header]
    for r in rows:
        table_data.append([
            Paragraph(r[0], styles['table_cell_bold']),
            Paragraph(r[1], styles['table_cell_bold']),
            Paragraph(r[2], styles['table_cell']),
        ])
    available_width = A4[0] - 2 * 0.85 * inch
    col_widths = [available_width * 0.08, available_width * 0.52, available_width * 0.40]
    flow.append(make_table(table_data, col_widths))
    return flow


def section_valor_comercial():
    """Página 13 — Valor de mercado."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Valor comercial', styles['kicker']))
    flow.append(add_heading('Quanto vale cada fase no mercado', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(Paragraph(
        'Tabela pra usar como base de proposta comercial. Valores '
        'referenciam o mercado brasileiro de freelancers iniciantes/'
        'intermediários em 2026. Para cliente amiga, pode-se aplicar '
        'desconto de 30-50% — mas nãoZero. Cobrar é um ato de respeito '
        'pelo tempo, skill e cliente.',
        styles['body_first']))
    flow.append(Spacer(1, 8))

    header = [
        Paragraph('<b>Entrega</b>', styles['table_header']),
        Paragraph('<b>Valor mercado</b>', styles['table_header']),
        Paragraph('<b>Valor amizade</b>', styles['table_header']),
    ]
    rows = [
        ['Extração + organização do conteúdo (Fase 1-2)', 'R$ 500 - R$ 800', 'R$ 250 - R$ 400'],
        ['Livro PDF (Fase 3)', 'R$ 400 - R$ 800', 'R$ 200 - R$ 400'],
        ['Briefing de marca (Fase 4)', 'R$ 600 - R$ 1.200', 'R$ 300 - R$ 600'],
        ['Site Next.js 16 rotas (Fase 5-6)', 'R$ 2.000 - R$ 4.000', 'R$ 1.000 - R$ 2.000'],
        ['Deploy na Vercel (Fase 7)', 'R$ 200 - R$ 400', 'R$ 100 - R$ 200'],
        ['Total projeto completo', 'R$ 3.700 - R$ 7.200', 'R$ 1.850 - R$ 3.600'],
        ['Manutenção mensal (opcional)', 'R$ 150 - R$ 300/mês', 'R$ 75 - R$ 150/mês'],
    ]
    table_data = [header]
    for r in rows:
        is_total = 'Total' in r[0]
        cell_style = styles['table_cell_bold'] if is_total else styles['table_cell']
        table_data.append([
            Paragraph(r[0], cell_style),
            Paragraph(r[1], cell_style),
            Paragraph(r[2], cell_style),
        ])
    available_width = A4[0] - 2 * 0.85 * inch
    col_widths = [available_width * 0.45, available_width * 0.27, available_width * 0.28]
    flow.append(make_table(table_data, col_widths))

    flow.append(Spacer(1, 10))
    flow.append(Paragraph(
        '<b>Importante:</b> o valor do projeto não é o tempo gasto pela '
        'desenvolvedora — é o valor gerado para a cliente. Um site que '
        'traz 5 novos pacientes por ano pagou 50x o investimento inicial.',
        styles['body']))

    flow.append(Paragraph(
        '<b>Modelos de cobrança:</b> (a) Tudo incluído — preço único + '
        'manutenção mensal; (b) Por etapa — cada fase com preço separado, '
        'cliente aprova antes de seguir; (c) Híbrido — desconto no setup '
        'em troca de contrato de manutenção anual.',
        styles['body']))
    return flow


def section_proximos_passos():
    """Página 14 — Próximos passos."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Próximos passos', styles['kicker']))
    flow.append(add_heading('O que ainda falta fazer', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(Paragraph(
        'O projeto está em "estado de pronto pra apresentar". As próximas '
        'etapas são complementares e podem ser negociadas separadamente '
        'com a cliente.',
        styles['body_first']))

    flow.append(add_heading('Curto prazo (próximas 2 semanas)', styles['h3'], level=1))
    flow.append(Paragraph(
        '• <b>Refinamentos finais</b> — cliente navega no site no ar e '
        'identifica ajustes (cores, copy, espaçamentos). Pequenos, '
        'reversíveis.<br/>'
        '• <b>Apresentação formal</b> — conversa de 30 min com Célia, '
        'apresentação do briefing, alinhamento do posicionamento, '
        'proposta de valor.<br/>'
        '• <b>Definição de pagamento</b> — combinar valor, forma (Pix, '
        'parcelado) e cronograma.<br/>'
        '• <b>Tirar screenshots profissionais</b> do site rodando — pra '
        'portfólio da desenvolvedora.',
        styles['body']))

    flow.append(add_heading('Médio prazo (próximos 2 meses)', styles['h3'], level=1))
    flow.append(Paragraph(
        '• <b>Transferência para GitHub/Vercel da Célia</b> — ela cria '
        'contas próprias, desenvolvedora transfere o repositório e '
        'conecta na Vercel dela. Célia fica dona do código.<br/>'
        '• <b>Domínio próprio</b> — comprar <i>celialima.com.br</i> '
        '(~R$ 40/ano) e conectar na Vercel. URL fica mais profissional.<br/>'
        '• <b>Sanity CMS</b> — implementar headless CMS pra Célia '
        'conseguir editar textos sozinha (sem precisar da desenvolvedora '
        'pra cada ajuste). Célia aprende fluxo de edição em 1h.<br/>'
        '• <b>Treinamento da Célia</b> — 1h de sessão pra ela aprender '
        'a usar Sanity Studio, criar novo artigo, agendar publicação.',
        styles['body']))

    flow.append(add_heading('Longo prazo (próximos 6 meses)', styles['h3'], level=1))
    flow.append(Paragraph(
        '• <b>Cadência editorial semanal</b> — dos 98 artigos, publicar '
        '20-30 inicialmente e ir alimentando 1-2 por semana. Melhora '
        'SEO/GEO sem content dump.<br/>'
        '• <b>Newsletter opcional</b> — captura de email no site + '
        'integração com Substack ou Beehiiv.<br/>'
        '• <b>Analytics</b> — configurar Plausible ou Google Analytics '
        'pra entender quais contextos atraem mais visitantes.<br/>'
        '• <b>Contrato de manutenção mensal</b> — formalizar pagamento '
        'recorrente pra suporte contínuo.',
        styles['body']))
    return flow


def section_licoes():
    """Página 15 — Lições aprendidas."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Retrospectiva', styles['kicker']))
    flow.append(add_heading('Lições aprendidas', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))

    flow.append(Paragraph(
        'Cada projeto ensina algo. Essas são as lições que ficam pra '
        'aplicar nos próximos.',
        styles['body_first']))

    flow.append(add_heading('Sobre o processo', styles['h3'], level=1))
    flow.append(Paragraph(
        '<b>1. Investigar antes de codar.</b> A investigação técnica da '
        'página de autora do Personare (que descobriu que os artigos '
        'eram SSR) economizou horas de trabalho com Playwright '
        'desnecessário.<br/>'
        '<b>2. Documentar cada fase.</b> O worklog.md salvou o projeto '
        'quando o ambiente reiniciou e perdeu parte das alterações — '
        'tinha passo-a-passo documentado pra refazer.<br/>'
        '<b>3. Backup frequente.</b> Snapshot ZIP a cada milestone. '
        'Custou 30 segundos por snapshot, salvou horas de retrabalho.',
        styles['body']))

    flow.append(add_heading('Sobre a relação com cliente', styles['h3'], level=1))
    flow.append(Paragraph(
        '<b>4. Briefing de marca antes de codar site.</b> Definir '
        'posicionamento primeiro evita refatorações depois. Um PDF de '
        '6 páginas que a cliente lê com calma vale mais que 5 reuniões.<br/>'
        '<b>5. Iterações pequenas e frequentes.</b> Mostrar progresso '
        'ao longo do projeto (em vez de surpreender no fim) gera '
        'confiança e ajustes mais baratos.<br/>'
        '<b>6. Cliente participa da curadoria.</b> A categorização manual '
        'pela Célia foi mais rica que qualquer heurística automática — '
        'ela conhece os próprios textos melhor que ninguém.',
        styles['body']))

    flow.append(add_heading('Sobre negócio', styles['h3'], level=1))
    flow.append(Paragraph(
        '<b>7. Cobrar é respeitar.</b> Cliente que paga valoriza o que '
        'recebeu. Cliente que ganha de graça esquece que existe.<br/>'
        '<b>8. Identidade visual unificada.</b> Briefing + livro + site '
        'com mesma paleta e tipografia cria marca — diferencia freelancer '
        'iniciante de freelancer profissional.<br/>'
        '<b>9. Documentar o processo é construir portfólio.</b> Este '
        'manual aqui <i>é</i> portfólio. Mostra o que foi feito, como '
        'foi feito, e por que tem valor.<br/>'
        '<b>10. Neurodivergência é superpoder.</b> Pensar em rede (e '
        'não linearmente) permite ver conexões que outros não veem — '
        'tipo unir "neurodivergente + site de psicoterapeuta + SEO + '
        'funil de vendas + portfólio" numa estratégia única.',
        styles['body']))

    flow.append(Spacer(1, 8))
    flow.append(HRFlowable(width="100%", color=BORDER, thickness=0.5,
                           spaceBefore=8, spaceAfter=14))
    flow.append(Paragraph(
        '"Cliente satisfeita é aquela que pagou o preço justo por um '
        'trabalho bem feito."',
        styles['quote']))
    return flow


# --- Main -------------------------------------------------------------------
def main():
    doc = TocDocTemplate(
        str(BODY_PDF),
        pagesize=A4,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.95 * inch,
        bottomMargin=0.85 * inch,
        title='Manual de Implementação — Projeto Célia Lima',
        author='Dalila Teles Veras',
        creator='Dalila Teles Veras',
        subject='Manual técnico: site institucional + blog terapêutico + livro PDF para Célia Lima',
    )

    story = []
    story.extend(section_visao_geral())
    story.extend(section_linha_do_tempo())
    story.extend(section_fase1())
    story.extend(section_fase2())
    story.extend(section_fase3())
    story.extend(section_fase4())
    story.extend(section_fase5())
    story.extend(section_fase6())
    story.extend(section_fase7())
    story.extend(section_stack_tecnico())
    story.extend(section_entregaveis())
    story.extend(section_valor_comercial())
    story.extend(section_proximos_passos())
    story.extend(section_licoes())

    doc.build(story, onFirstPage=draw_header_footer,
              onLaterPages=draw_header_footer)

    print(f"[ok] Corpo do manual gerado: {BODY_PDF}")
    print(f"     Tamanho: {BODY_PDF.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
