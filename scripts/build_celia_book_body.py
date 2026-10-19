#!/usr/bin/env python3
"""
Gera o CORPO do livro "Caminhos do Autoconhecimento" — Célia Lima.
V3: Refatorado com base nos refinamentos da cliente.

Estrutura:
- Sumário (auto-gerado)
- Apresentação
- 7 capítulos (um por contexto terapêutico)
  - Página única de abertura do capítulo (título grande + prefácio)
  - Cada artigo começa em folha nova (PageBreak)
  - Só artigos reflexivos (67), excluindo práticas (31)
  - Sem data nem nome/descrição da Célia no fim
"""

import os
import re
import sys
import json
import hashlib
import platform
from pathlib import Path
from collections import defaultdict

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, PageBreak, Spacer, KeepTogether,
    CondPageBreak, HRFlowable
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
BODY_PDF = OUT_DIR / "celia-lima-corpo-v3.pdf"
ARTICLES_JSON = Path("/home/z/my-project/src/data/articles.json")

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
        print(f"[warn] install_font_fallback: {e}")

# --- Palette ----------------------------------------------------------------
PAGE_BG       = colors.HexColor('#faf6f1')
TEXT_PRIMARY  = colors.HexColor('#3d3530')
TEXT_MUTED    = colors.HexColor('#838179')
ACCENT        = colors.HexColor('#a05a3c')   # terracota
ACCENT_2      = colors.HexColor('#7a8a5b')   # verde sálvia
BORDER        = colors.HexColor('#e3dccd')

BODY_FONT = 'NotoSerifSC'
BOLD_FONT = 'NotoSerifSC-Bold'

# --- Estilos ----------------------------------------------------------------
styles = {}

styles['toc_title'] = ParagraphStyle(
    name='TocTitle', fontName=BOLD_FONT, fontSize=22, leading=28,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=0, spaceAfter=24,
)

styles['toc1'] = ParagraphStyle(
    name='TOC1', fontName=BOLD_FONT, fontSize=12, leading=18,
    leftIndent=0, rightIndent=0, textColor=TEXT_PRIMARY, spaceAfter=4,
)

styles['toc2'] = ParagraphStyle(
    name='TOC2', fontName=BODY_FONT, fontSize=10, leading=14,
    leftIndent=18, rightIndent=0, textColor=TEXT_MUTED, spaceAfter=2,
)

styles['chapter_title'] = ParagraphStyle(
    name='ChapterTitle', fontName=BOLD_FONT, fontSize=32, leading=40,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=0, spaceAfter=14,
)

styles['chapter_kicker'] = ParagraphStyle(
    name='ChapterKicker', fontName=BODY_FONT, fontSize=10, leading=14,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=0, spaceAfter=4,
)

styles['chapter_preface'] = ParagraphStyle(
    name='ChapterPreface', fontName='FreeSerif-Italic', fontSize=12, leading=18,
    textColor=TEXT_MUTED, alignment=TA_JUSTIFY, spaceBefore=8, spaceAfter=18,
    leftIndent=0, rightIndent=0, firstLineIndent=0,
)

styles['article_title'] = ParagraphStyle(
    name='ArticleTitle', fontName=BOLD_FONT, fontSize=18, leading=24,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=0, spaceAfter=8,
)

styles['article_subtitle'] = ParagraphStyle(
    name='ArticleSubtitle', fontName='FreeSerif-Italic', fontSize=11, leading=15,
    textColor=TEXT_MUTED, alignment=TA_LEFT, spaceBefore=0, spaceAfter=10,
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

styles['h2'] = ParagraphStyle(
    name='H2', fontName=BOLD_FONT, fontSize=13, leading=17,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=12, spaceAfter=4,
)

styles['h3'] = ParagraphStyle(
    name='H3', fontName=BOLD_FONT, fontSize=11.5, leading=15,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4,
)

styles['list_item'] = ParagraphStyle(
    name='ListItem', fontName=BODY_FONT, fontSize=10.5, leading=15,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT,
    spaceBefore=0, spaceAfter=2, leftIndent=18, bulletIndent=4,
    firstLineIndent=0,
)

styles['presentation_title'] = ParagraphStyle(
    name='PresentationTitle', fontName=BOLD_FONT, fontSize=22, leading=28,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceBefore=0, spaceAfter=18,
)

styles['presentation_body'] = ParagraphStyle(
    name='PresentationBody', fontName=BODY_FONT, fontSize=11.5, leading=18,
    textColor=TEXT_PRIMARY, alignment=TA_JUSTIFY,
    spaceBefore=0, spaceAfter=10, firstLineIndent=14,
)

styles['presentation_body_first'] = ParagraphStyle(
    name='PresentationBodyFirst', fontName=BODY_FONT, fontSize=11.5, leading=18,
    textColor=TEXT_PRIMARY, alignment=TA_JUSTIFY,
    spaceBefore=0, spaceAfter=10, firstLineIndent=0,
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


# --- Markdown -> Flowables ---------------------------------------------------
def md_to_flowables(md_text: str):
    """Converte o corpo Markdown de um artigo em lista de Flowables ReportLab."""
    import re
    flowables = []
    lines = md_text.split('\n')
    i = 0
    is_first_para = True
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        # Pula o título h1 (já renderizado como article_title)
        if line.startswith('# ') and i < 3:
            i += 1
            continue
        # Subtítulo em itálico logo abaixo do h1
        if line.startswith('*') and line.endswith('*') and len(line.strip('*').strip()) > 0 and i < 5:
            subtitle = line.strip('*').strip()
            if subtitle:
                flowables.append(Paragraph(subtitle, styles['article_subtitle']))
            i += 1
            continue
        # h2
        if line.startswith('## '):
            text = line[3:].strip()
            flowables.append(Paragraph(text, styles['h2']))
            i += 1
            continue
        # h3
        if line.startswith('### '):
            text = line[4:].strip()
            flowables.append(Paragraph(text, styles['h3']))
            i += 1
            continue
        # h4+
        if line.startswith('#'):
            text = line.lstrip('#').strip()
            flowables.append(Paragraph(text, styles['h3']))
            i += 1
            continue
        # blockquote
        if line.startswith('> '):
            text = line[2:].strip()
            flowables.append(Paragraph(text, styles['article_subtitle']))
            i += 1
            continue
        # list item
        if line.startswith('- ') or re.match(r'^\d+\. ', line):
            is_ordered = bool(re.match(r'^\d+\. ', line))
            if is_ordered:
                text = re.sub(r'^\d+\. ', '', line).strip()
            else:
                text = line[2:].strip()
            text = text.replace('**', '').replace('*', '')
            bullet = '•' if not is_ordered else '·'
            flowables.append(Paragraph(f'{bullet}&nbsp;&nbsp;{text}', styles['list_item']))
            i += 1
            continue
        # parágrafo normal
        para_lines = [line]
        j = i + 1
        while j < len(lines):
            nl = lines[j].rstrip()
            if not nl.strip():
                break
            if nl.startswith(('#', '- ', '> ')) or re.match(r'^\d+\. ', nl):
                break
            para_lines.append(nl)
            j += 1
        para_text = ' '.join(para_lines).strip()
        para_text = para_text.replace('**', '').replace('*', '')
        # Escapa &, <, > (preservando tags super/sub)
        para_text = (para_text
                     .replace('&', '&amp;')
                     .replace('&lt;', '<')
                     .replace('&gt;', '>')
                     )
        if para_text:
            style_key = 'body_first' if is_first_para else 'body'
            flowables.append(Paragraph(para_text, styles[style_key]))
            is_first_para = False
        i = j
    return flowables


# --- Carrega artigos ---------------------------------------------------------
def load_articles():
    articles = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    # Só artigos reflexivos (exclui práticas da Caixa de Ferramentas)
    artigos = [a for a in articles if a.get("contentType") == "artigo"]
    return artigos


# --- 7 contextos (mesmos do site) --------------------------------------------
# Capítulo 4: "Burnout" no Word da Célia (em vez de "Esgotamento" no site)
CONTEXTS_ORDER = [
    ("dinamica-familiar", "Dinâmica Familiar e Criação de Filhos",
     "Mães, pais, filhos, sogras, avós. A família como primeiro espelho e território de aprendizado."),
    ("relacionamentos-sexualidade", "Relacionamentos Amorosos e Sexualidade",
     "Amor, parceria, sexo, escolhas, separação. Tudo que envolve escolher e ser escolhido por outro."),
    ("autocritica-limites", "Autocrítica, Limites e Autoestima",
     "Aprender a dizer não, reconhecer o próprio valor, calar o juiz interior, cuidar de si sem culpa."),
    ("ansiedade-estresse", "Ansiedade, Estresse e Burnout",
     "Quando o corpo pede calma e a cabeça não consegue parar. Cansaço, exaustão, dificuldade de relaxar."),
    ("sintomas-psicossomaticos-saude-emocional", "Sintomas Psicossomáticos e Saúde Emocional",
     "Emoção e corpo: como o que sentimos vira sintoma, doença como mensagem, terapias integrativas."),
    ("espiritualidade-autoconhecimento", "Espiritualidade e Autoconhecimento",
     "Espiritualidade no cotidiano, meditação, exercícios de proteção, autoavaliação, paz interior."),
    ("produtividade-carreira", "Produtividade, Carreira e Organização",
     "Vocação, propósito, dinheiro como energia, trabalho como construção de sentido."),
]


def build_story():
    artigos = load_articles()
    print(f"[info] {len(artigos)} artigos reflexivos (práticas excluídas)")

    # Agrupa por contexto
    by_ctx = defaultdict(list)
    for a in artigos:
        if a["contexts"]:
            by_ctx[a["contexts"][0]].append(a)
        else:
            by_ctx["outros"].append(a)

    # Ordena cada grupo por data (cronológico: do mais antigo ao mais recente)
    for ctx_slug in by_ctx:
        by_ctx[ctx_slug].sort(key=lambda a: a.get("datePublished", "1900-01-01"))

    story = []

    # --- Sumário ----------------------------------------------------------
    story.append(Paragraph('Sumário', styles['toc_title']))
    story.append(HRFlowable(width="100%", color=ACCENT, thickness=1.2,
                            spaceBefore=0, spaceAfter=18))
    toc = TableOfContents()
    toc.levelStyles = [styles['toc1'], styles['toc2']]
    story.append(toc)
    story.append(PageBreak())

    # --- Apresentação -----------------------------------------------------
    story.append(add_heading('Apresentação', styles['presentation_title'], level=0))
    story.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                            spaceBefore=0, spaceAfter=14))
    story.append(Paragraph(
        'Este livro reúne os textos que publiquei ao longo de mais de três '
        'décadas de prática como psicoterapeuta. São reflexões sobre amor, '
        'família, corpo, trabalho e espiritualidade — nascidas cada uma de '
        'uma situação concreta vivida no consultório, de uma dor, de uma '
        'pergunta, de um impasse.',
        styles['presentation_body_first']))
    story.append(Paragraph(
        'Organizei os textos em sete capítulos, agrupados por contexto '
        'terapêutico — aquilo que costuma trazer cada leitora e leitor até '
        'a leitura. Não é um manual de autoajuda. É um convite a pensar, '
        'sozinho ou com a sua própria terapia, sobre os temas que cruzam '
        'a vida de quase todo mundo.',
        styles['presentation_body']))
    story.append(Paragraph(
        'A leitura pode ser feita na ordem que fizer sentido para você. '
        'Dentro de cada capítulo, os textos seguem em ordem cronológica — '
        'do mais antigo ao mais recente — para que se possa acompanhar a '
        'maturação das ideias ao longo do tempo.',
        styles['presentation_body']))
    story.append(Paragraph(
        'Que cada texto encontre você na hora certa.',
        styles['presentation_body']))

    # --- 7 Capítulos (um por contexto) -----------------------------------
    for idx, (slug, label, description) in enumerate(CONTEXTS_ORDER):
        arts = by_ctx.get(slug, [])
        if not arts:
            continue

        # Página única de abertura do capítulo (PageBreak antes)
        # Sem KeepTogether — apenas a sequência natural de flowables.
        # A imagem é grande o suficiente pra preencher o espaço restante da página.
        story.append(PageBreak())
        story.append(Paragraph(f'Capítulo {idx + 1}', styles['chapter_kicker']))
        story.append(add_heading(label, styles['chapter_title'], level=0))
        story.append(HRFlowable(width="40%", color=ACCENT, thickness=1.2,
                                spaceBefore=0, spaceAfter=14))
        story.append(Paragraph(description, styles['chapter_preface']))
        story.append(Spacer(1, 50))  # Espaço entre texto e imagem

        # Imagem placeholder do capítulo (transparente, grande)
        from reportlab.platypus import Image
        png_path = f"/home/z/my-project/scripts/capitulos-png/{slug}.png"
        if os.path.exists(png_path):
            available_width = A4[0] - 2 * 0.85 * inch
            img_width = available_width * 0.75   # 75% da largura
            img_height = img_width * 0.65        # proporção ~4:2.6 (mais larga)
            img = Image(png_path, width=img_width, height=img_height)
            img.hAlign = 'CENTER'
            story.append(img)

        # Cada artigo em folha nova
        for art in arts:
            story.append(PageBreak())
            title = art.get("title", "").strip()
            body = art.get("html", "")

            # Extrai subtítulo (resumo) do JSON
            subtitle = art.get("summary", "").strip()

            # Título do artigo (em terracota, como no site)
            story.append(add_heading(title, styles['article_title'], level=1))

            # Subtítulo (resumo) em itálico logo abaixo
            if subtitle:
                story.append(Paragraph(subtitle, styles['article_subtitle']))

            # Linha divisória sutil
            story.append(HRFlowable(width="20%", color=BORDER, thickness=0.5,
                                    spaceBefore=0, spaceAfter=14))

            # Corpo do artigo — converte HTML pra texto simples
            # Como articles.json tem HTML, vamos usar BeautifulSoup pra extrair texto
            try:
                from bs4 import BeautifulSoup
                import re as re_mod
                # Funde <ol> consecutivos (bug do md_to_html: linhas em branco
                # fechavam <ol> e reabriam novo, resetando numeração pra 1)
                body = re_mod.sub(r'</ol>\s*<ol>', '', body)
                body = re_mod.sub(r'</ul>\s*<ul>', '', body)
                soup = BeautifulSoup(body, "html.parser")
                # Remove h2 (que vira título) — já temos o título
                for h2 in soup.find_all('h2'):
                    h2.decompose()
                # Para cada elemento, cria um Paragraph
                first_para = True
                for el in soup.children:
                    if isinstance(el, str):
                        continue
                    name = getattr(el, 'name', None)
                    if name == 'h3':
                        text = el.get_text(strip=True)
                        if text:
                            story.append(Paragraph(text, styles['h3']))
                            first_para = True
                    elif name == 'h4':
                        text = el.get_text(strip=True)
                        if text:
                            story.append(Paragraph(text, styles['h3']))
                            first_para = True
                    elif name == 'p':
                        classes = el.get('class', []) or []
                        text = el.get_text(strip=True)
                        if not text:
                            continue
                        if 'lead' in classes:
                            # Skip — subtítulo já foi mostrado acima a partir do campo summary
                            first_para = True
                            continue
                        else:
                            style_key = 'body_first' if first_para else 'body'
                            # Escapa HTML básico
                            text = (text.replace('&', '&amp;')
                                        .replace('<', '&lt;')
                                        .replace('>', '&gt;'))
                            story.append(Paragraph(text, styles[style_key]))
                            first_para = False
                    elif name == 'ul':
                        for li in el.find_all('li', recursive=False):
                            text = li.get_text(strip=True)
                            if text:
                                text = (text.replace('&', '&amp;')
                                           .replace('<', '&lt;')
                                           .replace('>', '&gt;'))
                                story.append(Paragraph(
                                    f'•&nbsp;&nbsp;{text}', styles['list_item']))
                        first_para = True
                    elif name == 'ol':
                        for i, li in enumerate(el.find_all('li', recursive=False), 1):
                            text = li.get_text(strip=True)
                            if text:
                                text = (text.replace('&', '&amp;')
                                           .replace('<', '&lt;')
                                           .replace('>', '&gt;'))
                                story.append(Paragraph(
                                    f'{i}.&nbsp;&nbsp;{text}', styles['list_item']))
                        first_para = True
                    elif name == 'blockquote':
                        text = el.get_text(strip=True)
                        if text:
                            story.append(Paragraph(
                                f'<i>{text}</i>', styles['article_subtitle']))
                            first_para = True
            except ImportError:
                # Fallback: usa o texto cru
                import re
                text_only = re.sub(r'<[^>]+>', ' ', body)
                text_only = re.sub(r'\s+', ' ', text_only).strip()
                story.append(Paragraph(text_only, styles['body_first']))

    return story


# --- Header / Footer ---------------------------------------------------------
def draw_header_footer(canvas, doc):
    canvas.saveState()
    page_w, page_h = A4
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.4)
    # Linha no topo (separador do header)
    canvas.line(0.85 * inch, page_h - 0.55 * inch, page_w - 0.85 * inch, page_h - 0.55 * inch)
    # Linha no rodapé (separador do footer)
    canvas.line(0.85 * inch, 0.55 * inch, page_w - 0.85 * inch, 0.55 * inch)

    # HEADER (topo): título do livro à esquerda + NÚMERO DA PÁGINA à direita
    page_num = canvas.getPageNumber()
    canvas.setFont(BODY_FONT, 8.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(0.85 * inch, page_h - 0.5 * inch,
                      'Caminhos do Autoconhecimento')
    # Número da página no canto direito do header (em vez de "Célia Lima")
    if page_num >= 2:
        canvas.setFont('FreeSerif', 9)
        canvas.setFillColor(TEXT_MUTED)
        canvas.drawRightString(page_w - 0.85 * inch, page_h - 0.5 * inch,
                                str(page_num - 1))

    # FOOTER (rodapé): "Célia Lima | Terapeuta | celialima.terapeuta@gmail.com"
    # (em vez do número da página centralizado)
    canvas.setFont(BODY_FONT, 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawCentredString(page_w / 2, 0.36 * inch,
                             'Célia Lima  |  Terapeuta  |  celialima.terapeuta@gmail.com')
    canvas.restoreState()


# --- Main -------------------------------------------------------------------
def main():
    story = build_story()

    doc = TocDocTemplate(
        str(BODY_PDF),
        pagesize=A4,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.95 * inch,
        bottomMargin=0.85 * inch,
        title='Caminhos do Autoconhecimento — Textos de uma trajetória terapêutica',
        author='Célia Lima',
        creator='Célia Lima',
        subject='Coletânea de 67 artigos reflexivos da psicoterapeuta Célia Lima, organizados por 7 contextos terapêuticos.',
    )

    doc.multiBuild(story, onFirstPage=draw_header_footer,
                   onLaterPages=draw_header_footer)

    print(f"[ok] Corpo do livro gerado: {BODY_PDF}")
    print(f"     Tamanho: {BODY_PDF.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
