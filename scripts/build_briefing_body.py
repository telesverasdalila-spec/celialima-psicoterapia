#!/usr/bin/env python3
"""
Gera o CORPO do 'Briefing de Marca — Célia Lima' (PDF).
Documento editorial curto (5 páginas) com paleta acolhedora.
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
BODY_PDF = OUT_DIR / "briefing-celia-corpo.pdf"

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
    name='H1', fontName=BOLD_FONT, fontSize=24, leading=30,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=0, spaceAfter=14,
)

styles['h2'] = ParagraphStyle(
    name='H2', fontName=BOLD_FONT, fontSize=14, leading=18,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=18, spaceAfter=8,
)

styles['h3'] = ParagraphStyle(
    name='H3', fontName=BOLD_FONT, fontSize=12, leading=15,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4,
)

styles['body'] = ParagraphStyle(
    name='Body', fontName=BODY_FONT, fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_JUSTIFY,
    spaceBefore=0, spaceAfter=10, firstLineIndent=12,
)

styles['body_first'] = ParagraphStyle(
    name='BodyFirst', fontName=BODY_FONT, fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_JUSTIFY,
    spaceBefore=0, spaceAfter=10, firstLineIndent=0,
)

styles['quote'] = ParagraphStyle(
    name='Quote', fontName='FreeSerif-Italic', fontSize=12, leading=18,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=12, spaceAfter=14,
    leftIndent=20, rightIndent=20, firstLineIndent=0,
    borderColor=ACCENT, borderPadding=(8, 0, 8, 12),
)

styles['meta'] = ParagraphStyle(
    name='Meta', fontName='FreeSerif-Italic', fontSize=9, leading=12,
    textColor=TEXT_MUTED, alignment=TA_LEFT, spaceBefore=4, spaceAfter=12,
)

styles['card_title'] = ParagraphStyle(
    name='CardTitle', fontName=BOLD_FONT, fontSize=12, leading=15,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=0, spaceAfter=4,
)

styles['card_body'] = ParagraphStyle(
    name='CardBody', fontName=BODY_FONT, fontSize=10, leading=14,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0,
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
    canvas.drawString(0.85 * inch, page_h - 0.5 * inch, 'Briefing de Marca · Célia Lima')
    canvas.drawRightString(page_w - 0.85 * inch, page_h - 0.5 * inch, 'Outubro 2026')
    canvas.restoreState()


# --- Conteúdo ---------------------------------------------------------------
def section_intro():
    """Página 2 — Para começar (resumo executivo)."""
    flow = []
    flow.append(Paragraph('Para começar', styles['kicker']))
    flow.append(add_heading('O que é este documento', styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))
    flow.append(Paragraph(
        'Este é um <b>briefing de marca</b> — um documento curto que organiza, '
        'em poucas páginas, as decisões mais importantes sobre como a Célia vai se '
        'posicionar profissionalmente daqui para a frente. Não é um site, não é um '
        'contrato, não é uma exigência. É um mapa que ajuda a gente a não se perder.',
        styles['body_first']))
    flow.append(Paragraph(
        'Ele nasceu de uma conversa: depois de mais de quinze anos de prática '
        'clínica, com 98 textos publicados e uma trajetória sólida, faz sentido '
        'reorganizar a presença profissional da Célia em torno do que ela de fato '
        'faz — psicoterapia de orientação junguiana e psicosíntese — em vez de '
        'entrar na cesta genérica dos "terapeutas holísticos". A diferença não é '
        'estética. É posicional: define quem ela atrai, quanto cobra, como escreve, '
        'como é citada pelo Google e pelos novos buscadores com inteligência '
        'artificial.',
        styles['body']))
    flow.append(Paragraph(
        'Este documento está estruturado em cinco partes: <b>posicionamento</b> '
        '(por que a escolha da palavra certa importa), <b>método traduzido</b> '
        '(como explicar psicosíntese e junguiana pra um leigo em três minutos), '
        '<b>serviços possíveis</b> (o leque que ela pode abrir, no tempo dela), '
        '<b>próximos passos</b> (a mentoria em 5 fases) e um convite final. '
        'A intenção não é que a Célia concorde com tudo — é que ela leia com '
        'calma, marque o que faz sentido, risc o que não faz, e a gente reflete '
        'junto a partir daí.',
        styles['body']))
    flow.append(Spacer(1, 8))
    flow.append(Paragraph(
        '"Um documento vivo. Aceito rasuras."',
        styles['quote']))
    return flow


def section_posicionamento():
    """Página 3 — Posicionamento."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Posicionamento', styles['kicker']))
    flow.append(add_heading('Por que psicoterapeuta, não terapeuta holístico',
                            styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))
    flow.append(Paragraph(
        'O mercado de "terapeuta holístico" saturou. Virou uma cesta onde cabe '
        'tudo: reiki, óleo essencial, constelação, tarot terapêutico, regressão, '
        'aromaterapia, psicanálise mal aplicada. Quando a Célia se apresenta como '
        '"terapeuta holística", ela entra nessa cesta — e o algoritmo do Google '
        'a compara com cinquenta mil outros profissionais. Quando ela se apresenta '
        'como <b>psicoterapeuta de orientação junguiana e psicosíntese</b>, ela '
        'sai da cesta e entra num nicho muito menor, mais bem definido, e mais '
        'valioso para quem busca trabalho profundo.',
        styles['body_first']))
    flow.append(Paragraph(
        'A formação dela é real e dá pra usar com honestidade. Psicosíntese é '
        'uma escola europeia fundada por Roberto Assagioli, parente próxima da '
        'psicologia analítica de Jung. Trabalha com subpersonalidades, vontade, '
        'sentido e auto-realização. Não é "coisa de terapeuta esotérico" — é '
        'uma abordagem reconhecida, ensinada em institutos sérios no Brasil e '
        'no exterior. Esconder isso pra falar de "holístico" é desperdiçar o '
        'que ela tem de único.',
        styles['body']))
    flow.append(Paragraph(
        'Há também uma razão de cliente: quem busca "terapeuta holístico" '
        'geralmente quer coisa rápida, espiritual, alternativa. Quem busca '
        '"psicoterapia junguiana" ou "psicoterapia com psicosíntese" procura '
        'um trabalho profundo, de longo prazo, e está disposto a pagar por '
        'isso. Esse é o cliente que sustenta uma clínica estável.',
        styles['body']))
    flow.append(Paragraph(
        'Uma precisão importante: a Célia é <b>terapeuta</b>, não psicóloga '
        '(que é título protegido por lei). Ela pode usar a palavra '
        '"psicoterapia" — é o nome do processo terapêutico, não um título '
        'profissional. O que não pode é se apresentar como psicóloga sem ser. '
        'Desde que isso esteja claro, tudo bem.',
        styles['body']))
    flow.append(Paragraph(
        'A frase-método (rascunho para validação com ela):',
        styles['meta']))
    flow.append(Paragraph(
        '"Psicoterapia de orientação junguiana e psicosíntese, com escuta '
        'ativa e uso integrativo de florais, respiração e psicodrama, '
        'quando fazem sentido para cada pessoa."',
        styles['quote']))
    flow.append(Paragraph(
        'Esta frase é o alicerce de tudo que vem depois — site, copy, '
        'conversa com clientes, colunas editoriais. Se a Célia concordar '
        'com ela, a gente trabalha a partir daí. Se não, a gente refaz.',
        styles['body']))
    return flow


def section_metodo():
    """Página 4 — O método traduzido."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('O método traduzido', styles['kicker']))
    flow.append(add_heading('Como explicar psicosíntese e junguiana pra um leigo',
                            styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))
    flow.append(Paragraph(
        'A Célia fala "psicosíntese" e "junguiana" e quase ninguém sabe o que '
        'é. O site precisa traduzir. Segue um rascunho de três cards curtos, '
        'em linguagem acessível, que podem ser usados na página "Sobre" e '
        'em conversas com clientes:',
        styles['body_first']))
    flow.append(Spacer(1, 6))

    # Tabela com 3 cards
    cards_data = [
        [Paragraph('<b>Subpersonalidades</b>', styles['card_title'])],
        [Paragraph(
            'A gente não é uma pessoa só. Tem a profissional, a mãe, a filha, '
            'a adolescente que ainda mora dentro de você, a crítica, a medrosa. '
            'A terapia trabalha como essas partes conversam entre si — e como '
            'às vezes elas se boicotam.',
            styles['card_body'])],
        [Paragraph('<b>Símbolos e sonhos</b>', styles['card_title'])],
        [Paragraph(
            'O inconsciente fala por imagens, não por palavras. Um sonho, um '
            'sintoma do corpo, uma frase que escapa — tudo isso é linguagem. '
            'A terapia aprende a ler essa linguagem.',
            styles['card_body'])],
        [Paragraph('<b>Sentido e totalidade</b>', styles['card_title'])],
        [Paragraph(
            'Não se trata só de parar de sofrer. Trata-se de virar a pessoa '
            'inteira que você veio ser. A junguiana chama isso de individuação; '
            'a psicosíntese chama de auto-realização. É o mesmo convite: ser '
            'mais você mesmo.',
            styles['card_body'])],
    ]
    # Em vez de tabela 1-col, faço 3 cards lado a lado
    cards_table_data = [
        [
            [
                Paragraph('<b>Subpersonalidades</b>', styles['card_title']),
                Spacer(1, 4),
                Paragraph(
                    'A gente não é uma pessoa só. Tem a profissional, a mãe, '
                    'a filha, a adolescente que ainda mora dentro de você, a '
                    'crítica, a medrosa. A terapia trabalha como essas partes '
                    'conversam entre si — e como às vezes elas se boicotam.',
                    styles['card_body']),
            ],
            [
                Paragraph('<b>Símbolos e sonhos</b>', styles['card_title']),
                Spacer(1, 4),
                Paragraph(
                    'O inconsciente fala por imagens, não por palavras. Um '
                    'sonho, um sintoma do corpo, uma frase que escapa — tudo '
                    'isso é linguagem. A terapia aprende a ler essa linguagem.',
                    styles['card_body']),
            ],
            [
                Paragraph('<b>Sentido e totalidade</b>', styles['card_title']),
                Spacer(1, 4),
                Paragraph(
                    'Não se trata só de parar de sofrer. Trata-se de virar a '
                    'pessoa inteira que você veio ser. A junguiana chama isso '
                    'de individuação; a psicosíntese chama de auto-realização. '
                    'É o mesmo convite: ser mais você mesmo.',
                    styles['card_body']),
            ],
        ]
    ]
    available_width = A4[0] - 2 * 0.85 * inch
    col_w = (available_width - 12) / 3
    cards_table = Table(cards_table_data, colWidths=[col_w, col_w, col_w],
                        hAlign='CENTER')
    cards_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('LINEBEFORE', (1, 0), (1, -1), 0.5, BORDER),
        ('LINEBEFORE', (2, 0), (2, -1), 0.5, BORDER),
    ]))
    flow.append(cards_table)
    flow.append(Spacer(1, 14))
    flow.append(Paragraph(
        'Esses três cards são a "porta de entrada" para o leitor entender o '
        'método sem precisar saber os nomes técnicos. E para quem quiser '
        'saber mais, um link "Saiba mais sobre a abordagem da Célia" pode '
        'levar a uma página mais profunda — opcional, no tempo dela.',
        styles['body']))
    return flow


def section_servicos():
    """Página 5 — Serviços possíveis (tabela)."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Serviços possíveis', styles['kicker']))
    flow.append(add_heading('O leque que a Célia pode abrir, no tempo dela',
                            styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))
    flow.append(Paragraph(
        'Mesmo que hoje ela só faça terapia individual, vale pensar o leque '
        'de serviços que ela <b> poderia</b> oferecer (e que o site pode '
        'mostrar, mesmo que ela só ative um por enquanto). A decisão é dela: '
        'qual desses faz sentido? Qual ela nunca faria? Qual é o primeiro?',
        styles['body_first']))

    # Tabela de serviços
    header = [
        Paragraph('<b>Serviço</b>', styles['table_header']),
        Paragraph('<b>O que é</b>', styles['table_header']),
        Paragraph('<b>Pra quem é</b>', styles['table_header']),
    ]
    rows = [
        ['Psicoterapia individual',
         'Sessões semanais de 50 min, em curso',
         'Quem quer trabalho profundo e contínuo'],
        ['Escuta inicial',
         'Conversa única, 90 min, sem compromisso',
         'Quem está em dúvida se faz terapia'],
        ['Mentoria pontual',
         'Sessão única sobre um tema (luto, separação, crise)',
         'Quem tem uma questão, não quer entrar em processo'],
        ['Grupo de estudos/terapia',
         'Grupo fechado de 6-8 pessoas, encontros mensais',
         'Quem quer trabalhar questões em comunidade'],
    ]
    table_data = [header]
    for r in rows:
        table_data.append([
            Paragraph(r[0], styles['table_cell_bold']),
            Paragraph(r[1], styles['table_cell']),
            Paragraph(r[2], styles['table_cell']),
        ])

    available_width = A4[0] - 2 * 0.85 * inch
    col_widths = [available_width * 0.25, available_width * 0.40, available_width * 0.35]
    t = Table(table_data, colWidths=col_widths, hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, CARD_BG]),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 14))
    flow.append(Paragraph(
        'Vale notar: não precisa por tudo isso no ar agora. A estrutura do '
        'site deixa espaço, e ela decide o que ativa primeiro. O mais '
        'comum é começar com "Psicoterapia individual" + "Escuta inicial" '
        '— esse par cobre quem está começando e quem quer só uma '
        'conversa de teste.',
        styles['body']))
    return flow


def section_plano():
    """Página 6 — Próximos passos (mentoria em 5 fases)."""
    flow = []
    flow.append(PageBreak())
    flow.append(Paragraph('Próximos passos', styles['kicker']))
    flow.append(add_heading('A mentoria em cinco fases',
                            styles['h1'], level=0))
    flow.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                           spaceBefore=0, spaceAfter=14))
    flow.append(Paragraph(
        'O ritmo da Célia dita a velocidade. Nada aqui é urgente — mas é '
        'bom ter um mapa. Segue a proposta de cinco fases, cada uma com '
        'seu entregável, que a gente percorre no tempo que fizer sentido:',
        styles['body_first']))

    fases = [
        ('Fase 1 — Diagnóstico e posicionamento',
         'Sessão de 90 minutos com ela, no WhatsApp ou Google Meet. Você '
         'pergunta: "Conta pra mim, sem pressa, como você descreveria seu '
         'trabalho pra uma desconhecida". Anota, não corrige. Repete isso '
         'três vezes em três sessões. No fim, você terá três versões — '
         'aí propõe uma quarta, profissional, com a voz dela. '
         '<b>Entregável</b>: a frase-método (1 frase) + descrição da '
         'abordagem (3 cards) + perfil de cliente ideal (meia página).'),
        ('Fase 2 — Estrutura de serviços',
         'Você mostra pra ela os quatro modelos de serviço da página '
         'anterior e pergunta: "Qual te soa possível? Qual te dá calafrio?". '
         'Não é preciso que ela decida tudo agora. Só que decida o que '
         '<i>não</i> vai entrar. '
         '<b>Entregável</b>: lista de serviços que ela oferece, com '
         'preços (ou "a combinar", se ela preferir não publicar).'),
        ('Fase 3 — Copy do site',
         'Você mostra o site atual e pergunta: "Lê essa bio e me diz o '
         'que parece você, e o que parece a Célia de um site de terapeuta '
         'genérico". Aí ela reescreve, ou você reescreve a partir do que '
         'ela falou. '
         '<b>Entregável</b>: textos do site prontos (home, sobre, '
         'contato, descrições das áreas).'),
        ('Fase 4 — Colunas editoriais',
         'Voltamos à conversa das colunas (Saúde Mental / AutoTerapia) — '
         'agora com o posicionamento claro. Decidimos os nomes, a '
         'divisão dos 98 textos, e a cadência semanal. '
         '<b>Entregável</b>: calendário editorial das primeiras 8 '
         'semanas, com 20-30 textos selecionados e agendados.'),
        ('Fase 5 — CMS e publicação',
         'Aí sim entra o headless CMS (Sanity ou outro). Treinamento '
         'dela. Primeiras 4 semanas de cadência (com você acompanhando). '
         '<b>Entregável</b>: sistema rodando, Célia publicando sozinha, '
         'manual ilustrado de 3-4 páginas que ela pode consultar.'),
    ]
    for titulo, texto in fases:
        flow.append(Paragraph(titulo, styles['h3']))
        flow.append(Paragraph(texto, styles['body']))

    flow.append(Spacer(1, 6))
    flow.append(HRFlowable(width="100%", color=BORDER, thickness=0.5,
                           spaceBefore=8, spaceAfter=14))
    flow.append(Paragraph(
        '"A leitura abriu alguma pergunta? É assim que a gente começa."',
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
        title='Briefing de Marca — Célia Lima',
        author='Célia Lima',
        creator='Célia Lima',
        subject='Briefing de marca: psicoterapeuta de orientação junguiana e psicosíntese',
    )

    story = []
    # Sem sumário (documento curto, 5 páginas) — vão direto
    story.extend(section_intro())
    story.extend(section_posicionamento())
    story.extend(section_metodo())
    story.extend(section_servicos())
    story.extend(section_plano())

    doc.build(story, onFirstPage=draw_header_footer,
              onLaterPages=draw_header_footer)

    print(f"[ok] Corpo do briefing gerado: {BODY_PDF}")
    print(f"     Tamanho: {BODY_PDF.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
