#!/usr/bin/env python3
"""
Scraper da Célia Lima no Personare.
Lê /tmp/articles.json (98 artigos coletados via headless browser) e:
  - Baixa o HTML de cada artigo (HTTP simples, são SSR)
  - Extrai do JSON-LD: datePublished, dateModified, wordCount, keywords, thumbnailUrl
  - Extrai o conteúdo do <main> (paragrafos, headings, listas)
  - Salva cada artigo como Markdown em /home/z/my-project/download/celia-lima-artigos/{slug}.md
  - Gera planilha Excel com todos os metadados

Cortesia: User-Agent próprio, delay de 0.6s entre requisições.
"""

import json
import re
import time
import html
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# --- Config ------------------------------------------------------------------
ARTICLES_JSON = Path("/tmp/articles.json")
OUT_DIR = Path("/home/z/my-project/download/celia-lima-artigos")
XLSX_OUT = Path("/home/z/my-project/download/celia-lima-artigos.xlsx")
HTML_CACHE = Path("/tmp/celia_html_cache")
HEADERS = {
    "User-Agent": "CeliaLimaArchiveBot/1.0 (+uso pessoal, preservação de obra própria)",
    "Accept-Language": "pt-BR,pt;q=0.9",
}
DELAY_S = 0.6
TIMEOUT_S = 30

OUT_DIR.mkdir(parents=True, exist_ok=True)
HTML_CACHE.mkdir(parents=True, exist_ok=True)

# Frases de CTA/promoção do Personare que NÃO fazem parte do artigo
CTA_PATTERNS = [
    r"^📱", r"^📲",
    r"^Entre para o grupo",
    r"^Conheça o (Clube )?Personare",
    r"^Faça seu (mapa|tarot|numerologia|horóscopo)",
    r"^Leia também",
    r"^Saiba mais sobre",
    r"^Acesse (o )?Personare",
    r"^Compartilhe",
    r"^Cadastre-se",
    r"^Assine",
    r"^Acesse agora",
    r"personare\.com\.br",
    r"^Clique aqui",
    r"^Saiba como",
    r"^Veja também",
]
CTA_REGEX = re.compile("|".join(CTA_PATTERNS), re.IGNORECASE)


# --- Helpers -----------------------------------------------------------------
def slugify(url: str) -> str:
    """https://www.personare.com.br/conteudo/carencia-afetiva-m273696 -> carencia-afetiva-m273696"""
    path = urlparse(url).path
    return path.rstrip("/").rsplit("/", 1)[-1]


def extract_jsonld(soup: BeautifulSoup) -> dict:
    """Procura todos os blocos JSON-LD e junta o que for relevante."""
    out = {}
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        # Pode vir como dict ou list
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            # Pode estar dentro de @graph
            if "@graph" in item and isinstance(item["@graph"], list):
                for sub in item["@graph"]:
                    if isinstance(sub, dict) and sub.get("@type") in ("Article", "NewsArticle", "BlogPosting"):
                        out.update({k: v for k, v in sub.items() if k in
                                    ("headline", "datePublished", "dateModified",
                                     "wordCount", "keywords", "thumbnailUrl",
                                     "author", "image", "description", "articleBody")})
            if item.get("@type") in ("Article", "NewsArticle", "BlogPosting"):
                out.update({k: v for k, v in item.items() if k in
                            ("headline", "datePublished", "dateModified",
                             "wordCount", "keywords", "thumbnailUrl",
                             "author", "image", "description", "articleBody")})
    return out


def get_meta(soup: BeautifulSoup, name: str, attr: str = "name") -> str:
    tag = soup.find("meta", attrs={attr: name})
    return tag.get("content", "").strip() if tag else ""


def is_cta(text: str) -> bool:
    """Verifica se um parágrafo é CTA/promoção do Personare (não é conteúdo)."""
    return bool(CTA_REGEX.search(text.strip()))


def extract_main_text(soup: BeautifulSoup) -> tuple[str, str, str]:
    """
    Extrai o conteúdo real do artigo (sem menu, breadcrumb, autor, CTAs).
    Estrutura típica do Personare:
      <div class="sc-4eef204f-0"> (container do artigo)
        ├── <div class="sc-f119ddf0-0">Amor › Relacionamento</div>  (breadcrumb - PULAR)
        ├── <h1>título</h1>
        ├── <h2 class="sc-4eef204f-2">subtítulo/resumo</h2>
        ├── <div class="sc-18f96a1d-0">Por Célia Lima</div>  (autor - PULAR)
        └── <div class="sc-4eef204f-4">
              └── <div class="sc-4eef204f-6">Atualizado em... + parágrafos reais</div>

    Retorna (markdown_text, plain_text, subtitle).
    """
    h1 = soup.find("h1")
    title_md = h1.get_text(strip=True) if h1 else ""
    subtitle = ""

    if not h1:
        # Fallback: usa o main inteiro
        container = soup.find("main") or soup
    else:
        container = h1.parent  # sc-4eef204f-0
        # Procura o subtítulo (h2 logo após o h1, com classe sc-4eef204f-2)
        sub_h2 = container.find("h2", class_=re.compile(r"sc-4eef204f-2"))
        if sub_h2:
            subtitle = sub_h2.get_text(strip=True)

    chunks_md = []
    chunks_plain = []

    # Título
    if title_md:
        chunks_md.append(f"# {title_md}\n")
        chunks_plain.append(title_md + "\n\n")
    # Subtítulo em itálico logo abaixo
    if subtitle:
        chunks_md.append(f"*{subtitle}*\n\n")
        chunks_plain.append(subtitle + "\n\n")

    # Itera sobre elementos de conteúdo dentro do container
    # Filtra: pula breadcrumb (sc-f119ddf0-0), autor (sc-18f96a1d-0), e a div "Atualizado em"
    for el in container.descendants:
        if not hasattr(el, "name") or el.name is None:
            continue
        # Pular tudo que estiver dentro do breadcrumb ou do card de autor
        if el.find_parent(class_=re.compile(r"sc-f119ddf0-0|sc-18f96a1d-0")):
            continue
        name = el.name
        if name in ("script", "style", "nav", "aside", "footer", "header"):
            continue

        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = el.get_text(strip=True)
            if not text or text == title_md or text == subtitle:
                continue
            level = int(name[1])
            chunks_md.append(f"\n{'#' * level} {text}\n")
            chunks_plain.append(text + "\n")
        elif name == "p":
            text = el.get_text(strip=True)
            if not text or is_cta(text):
                continue
            # Pula "Por Célia Lima" que ainda escapou
            if re.match(r"^Por\s*Celia\s*Lima", text, re.IGNORECASE):
                continue
            chunks_md.append(f"{text}\n\n")
            chunks_plain.append(text + "\n\n")
        elif name == "ul":
            items = el.find_all("li", recursive=False)
            if not items:
                continue
            for li in items:
                text = li.get_text(strip=True)
                if text and not is_cta(text):
                    chunks_md.append(f"- {text}\n")
                    chunks_plain.append(f"- {text}\n")
            chunks_md.append("\n")
            chunks_plain.append("\n")
        elif name == "ol":
            items = el.find_all("li", recursive=False)
            if not items:
                continue
            for i, li in enumerate(items, 1):
                text = li.get_text(strip=True)
                if text and not is_cta(text):
                    chunks_md.append(f"{i}. {text}\n")
                    chunks_plain.append(f"{i}. {text}\n")
            chunks_md.append("\n")
            chunks_plain.append("\n")
        elif name == "blockquote":
            text = el.get_text(strip=True)
            if text:
                chunks_md.append(f"> {text}\n\n")
                chunks_plain.append(text + "\n\n")

    md = "\n".join(chunks_md).strip()
    plain = "".join(chunks_plain).strip()
    return md, plain, subtitle


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ]+\b", text, flags=re.UNICODE))


# --- Main --------------------------------------------------------------------
def main():
    data = json.load(open(ARTICLES_JSON))
    articles = data["data"]["result"]
    total = len(articles)
    print(f"[scrape] {total} artigos para baixar")

    results = []
    session = requests.Session()
    session.headers.update(HEADERS)

    for i, art in enumerate(articles, 1):
        url = art["href"]
        title = art["title"]
        category = art["category"]
        summary = art.get("description", "")
        slug = slugify(url)
        md_path = OUT_DIR / f"{slug}.md"
        cache_path = HTML_CACHE / f"{slug}.html"

        print(f"[{i:3}/{total}] {slug} ({category}) ... ", end="", flush=True)
        try:
            # Cache: se já baixamos o HTML antes, reutiliza
            if cache_path.exists():
                html_text = cache_path.read_text(encoding="utf-8")
            else:
                r = session.get(url, timeout=TIMEOUT_S)
                r.raise_for_status()
                html_text = r.text
                cache_path.write_text(html_text, encoding="utf-8")
                time.sleep(DELAY_S)

            soup = BeautifulSoup(html_text, "html.parser")

            jsonld = extract_jsonld(soup)
            date_pub = jsonld.get("datePublished") or get_meta(soup, "article:published_time", "property")
            date_mod = jsonld.get("dateModified") or ""
            keywords = jsonld.get("keywords") or get_meta(soup, "keywords")
            if isinstance(keywords, list):
                keywords = ", ".join(keywords)
            thumb = jsonld.get("thumbnailUrl") or jsonld.get("image", "")
            if isinstance(thumb, dict):
                thumb = thumb.get("url", "")
            wordcount_ld = jsonld.get("wordCount") or 0

            md_body, plain, subtitle = extract_main_text(soup)
            wc_real = count_words(plain)
            wc = wordcount_ld or wc_real

            # Salva Markdown
            frontmatter = [
                "---",
                f"title: {json.dumps(title, ensure_ascii=False)}",
                f"slug: {slug}",
                f"categoria: {json.dumps(category, ensure_ascii=False)}",
                f"data_publicacao: {date_pub or 's/d'}",
                f"data_modificacao: {date_mod or 's/d'}",
                f"link_original: {url}",
            ]
            if subtitle:
                frontmatter.append(f"subtitulo: {json.dumps(subtitle, ensure_ascii=False)}")
            if keywords:
                kw_list = [k.strip() for k in re.split(r"[,;]", keywords) if k.strip()]
                frontmatter.append(f"palavras_chave: {json.dumps(kw_list, ensure_ascii=False)}")
            if thumb:
                frontmatter.append(f"thumbnail: {thumb}")
            frontmatter.append(f"palavras: {wc}")
            frontmatter.append("---\n")
            md_text = "\n".join(frontmatter) + "\n" + md_body + "\n"
            md_path.write_text(md_text, encoding="utf-8")

            results.append({
                "n": i,
                "titulo": title,
                "categoria": category,
                "data_publicacao": date_pub or "s/d",
                "resumo": summary,
                "palavras_chave": keywords or "",
                "palavras": wc,
                "link": url,
                "arquivo_md": md_path.name,
            })
            print(f"OK ({wc} palavras, {len(md_body)} chars)")
        except Exception as e:
            print(f"ERRO: {e}")
            results.append({
                "n": i,
                "titulo": title,
                "categoria": category,
                "data_publicacao": "ERRO",
                "resumo": summary,
                "palavras_chave": "",
                "palavras": 0,
                "link": url,
                "arquivo_md": "",
                "erro": str(e),
            })

    # --- Gera planilha Excel --------------------------------------------------
    print(f"\n[xlsx] Gerando planilha em {XLSX_OUT}")
    wb = Workbook()
    ws = wb.active
    ws.title = "Artigos Célia Lima"

    headers = ["#", "Título", "Categoria", "Data publicação",
               "Resumo", "Palavras-chave", "Palavras", "Link original", "Arquivo MD"]
    ws.append(headers)

    # Estilo do cabeçalho
    header_fill = PatternFill("solid", fgColor="8B5A3C")
    header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    thin = Side(border_style="thin", color="D4C5B9")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="left", vertical="center")
        cell.border = border
    ws.row_dimensions[1].height = 28

    # Linhas de dados
    alt_fill = PatternFill("solid", fgColor="FAF6F1")
    for r in results:
        ws.append([r["n"], r["titulo"], r["categoria"], r["data_publicacao"],
                   r["resumo"], r["palavras_chave"], r["palavras"],
                   r["link"], r["arquivo_md"]])
        row_idx = ws.max_row
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if row_idx % 2 == 0:
                cell.fill = alt_fill

    # Larguras
    widths = {"A": 5, "B": 55, "C": 18, "D": 14, "E": 60, "F": 30, "G": 10, "H": 50, "I": 35}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    # Aba de resumo por categoria
    ws2 = wb.create_sheet("Resumo por categoria")
    ws2.append(["Categoria", "Qtd. artigos", "Palavras totais"])
    for col in range(1, 4):
        cell = ws2.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = Alignment(horizontal="left", vertical="center")
    ws2.row_dimensions[1].height = 28

    from collections import defaultdict
    cat_count = defaultdict(lambda: [0, 0])
    for r in results:
        cat_count[r["categoria"]][0] += 1
        cat_count[r["categoria"]][1] += r["palavras"] or 0
    for cat, (n, w) in sorted(cat_count.items(), key=lambda x: -x[1][0]):
        ws2.append([cat, n, w])
        row_idx = ws2.max_row
        for col in range(1, 4):
            cell = ws2.cell(row=row_idx, column=col)
            cell.border = border
            if row_idx % 2 == 0:
                cell.fill = alt_fill

    ws2.column_dimensions["A"].width = 25
    ws2.column_dimensions["B"].width = 14
    ws2.column_dimensions["C"].width = 18
    ws2.freeze_panes = "A2"

    wb.save(XLSX_OUT)

    ok = sum(1 for r in results if r.get("palavras", 0) > 0)
    print(f"\n[done] {ok}/{total} artigos baixados com sucesso")
    print(f"[done] Markdown em: {OUT_DIR}")
    print(f"[done] Planilha em: {XLSX_OUT}")


if __name__ == "__main__":
    main()
