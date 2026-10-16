#!/usr/bin/env python3
"""
Reclassifica os 98 artigos da Célia Lima em:
  - Tipo de conteúdo: 'artigo' (reflexivo) | 'pratica' (técnica)
  - Contextos: 1-2 dos 6 contextos terapêuticos
E gera:
  - JSON único (articles.json) atualizado
  - Planilha Excel (classificacao-artigos.xlsx) para revisão manual da Célia

Contextos (6):
  - ansiedade-stress
  - autoconhecimento-proposito
  - relacionamentos
  - luto-perdas
  - limites-autoestima
  - familia-relacoes-parentais

Heurística Caixa de Ferramentas (pratica):
  - Título tem técnica explícita: Respiração, Floral, Método, Áudios, Exercício, Prática
"""

import json
import re
import yaml
import html
from pathlib import Path
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

MD_DIR = Path("/home/z/my-project/download/celia-lima-artigos")
OUT_JSON = Path("/home/z/my-project/src/data/articles.json")
OUT_XLSX = Path("/home/z/my-project/download/classificacao-artigos-celia.xlsx")

# --- Mapeamento de contextos por palavra-chave -------------------------------
CONTEXT_KEYWORDS = {
    "ansiedade-stress": [
        "ansiedade", "ansioso", "stress", "estresse", "calma", "acalmar",
        "cansaco", "cansaço", "exaustao", "exaustão", "respiracao", "respiração",
        "paz", "encontrar paz", "aromaterapia", "florais", "oleos essenciais",
        "óleos essenciais", "incapacidade", "pessimismo", "medo da escassez",
        "encarar a realidade", "encarar a vida",
    ],
    "autoconhecimento-proposito": [
        "autoconhecimento", "auto-conhecimento", "proposito", "propósito",
        "vocacao", "vocação", "metamorfose", "juiz interior", "vitima",
        "vítima", "sobrevivente", "perfeicao", "perfeição", "timidez",
        "decepcao", "decepção", "pessoa chata", "fofoca", "odio", "ódio",
        "identidade", "mulher com m de maravilha", "sabor da sua vida",
        "psicodrama", "timidez", " Admirar sem desejar", "Admirar sem desejar",
    ],
    "relacionamentos": [
        "carencia", "carência", "relacionamento", "amor", "namoro", "namorada",
        "parceiro", "parceira", "separacao", "separação", "sexo", "sexual",
        "masturbacao", "masturbação", "fantasias sexuais", "exclusividade",
        "generosidade", "egoismo", "egosimo", "egoísmo", "mulheres maduras",
        "homens jovens", "beijei", "mesmo sexo", "prazer", "relacao aberta",
        "relação aberta", "amor no ambiente", "celular", "arma que dispara",
        "vida sexual", "tabus", "amor nao precisa", "amor não precisa",
        "equilibrando a razao", "equilibrando a razão",
    ],
    "luto-perdas": [
        "luto", "morte", "morte subita", "morte súbita", "perda", "perdas",
        "dor", "separacao", "separação", "faca as pazes", "faça as pazes",
        "ausencia paterna", "ausência paterna", "suicidio", "suicídio",
        "prevencao ao suicidio", "prevenção ao suicídio",
        "violencia domestica", "violência doméstica",
        "do virtual para o mundo", "impacto da pandemia",
    ],
    "limites-autoestima": [
        "limites", "limite", "dizer nao", "dizer não", "autoestima",
        "auto-estima", "impor limites", "teimosia", "teimosia",
        "generosidade", "egoismo", "egoísmo", "exigir exclusividade",
        "quer exclusividade", "competicao entre maes", "competição entre mães",
        "como deixar a culpa", "culpa", "papel de vitima", "papel de vítima",
    ],
    "familia-relacoes-parentais": [
        "familia", "família", "mae", "mãe", "filha", "filhas", "filho",
        "filhos", "sogra", "nora", "avo", "avó", "avos", "avós", "netos",
        "irmaos", "irmãos", "irma", "irmã", "lei da palmada", "pais idosos",
        "cuidar de pais", "recarregando as baterias em familia",
        "recarregando as baterias em família", "comunicacao em casa",
        "comunicação em casa", "educacao emocional", "educação emocional",
        "ensinando valores", "futebol politica", "futebol política",
        "natal", "festas de fim ano", "festa", "vovo", "vovó", "voce cuida",
        "você cuida", "familia em primeiro", "família em primeiro",
        "relacoes familiares", "relações familiares", "pandemia",
        "quarentena", "sogra voce e", "sogra você é", "que tipo de nora",
        "que tipo de sogra", "nao quero ter filhos", "não quero ter filhos",
    ],
}

CONTEXT_LABELS = {
    "ansiedade-stress": "Ansiedade & Stress",
    "autoconhecimento-proposito": "Autoconhecimento & Propósito",
    "relacionamentos": "Relacionamentos",
    "luto-perdas": "Luto & Perdas",
    "limites-autoestima": "Limites e Autoestima",
    "familia-relacoes-parentais": "Família e relações parentais",
}

CONTEXT_DESCRIPTIONS = {
    "ansiedade-stress":
        "Ansiedade, exaustão, dificuldade de relaxar. Quando o corpo pede calma e a cabeça não consegue parar.",
    "autoconhecimento-proposito":
        "Quem sou, o que quero, o que me move. Perguntas que voltam em diferentes momentos da vida.",
    "relacionamentos":
        "Amor, parceria, sexo, separação. Tudo que envolve escolher e ser escolhido por outro.",
    "luto-perdas":
        "Morte, separação, ausência. Quando a vida muda de forma irreversível e é preciso refazer o caminho.",
    "limites-autoestima":
        "Aprender a dizer não, reconhecer o próprio valor, cuidar de si sem culpa.",
    "familia-relacoes-parentais":
        "Mães, pais, filhos, sogras, avós. A família como espelho e território.",
}

# --- Heurística Caixa de Ferramentas ----------------------------------------
PRATICA_KEYWORDS = [
    "respiracao colorida", "respiração colorida",
    "florais", "oleos essenciais", "óleos essenciais",
    "metodo dos 5 segundos", "método dos 5 segundos",
    "8 audios", "8 áudios", "audio para voce", "áudio para você",
    "exercicios de protecao", "exercícios de proteção",
    "espiritualidade que esta no cotidiano", "espiritualidade que está no cotidiano",
    "terapias alternativas",
    "medicina tradicional e terapias",
    "respiracao", "respiração",
]

PRATICA_TITLE_REGEX = re.compile(
    r"(florais|óleos essenciais|oleos essenciais|respiração|respiracao|"
    r"método dos 5|método dos cinco|metodo dos 5|metodo dos cinco|"
    r"exercícios de prote|exercicios de prote|"
    r"áudios para você|audios para voce|8 áudios|8 audios|"
    r"terapias alternativas|medicina tradicional e terapias|"
    r"espiritualidade que está|espiritualidade que esta)",
    re.IGNORECASE,
)


def is_pratica(title: str, body: str) -> tuple[bool, str]:
    """Decide se é 'pratica' ou 'artigo' com base no título e corpo."""
    title_lower = title.lower()
    body_lower = body[:1500].lower()  # só começo do corpo

    # Se título claramente fala de técnica/prática
    if PRATICA_TITLE_REGEX.search(title):
        return True, "título"

    # Heurística adicional: tem técnica no corpo + título curto + tem passos numerados
    has_technique_in_body = any(
        kw in body_lower for kw in ["passo", "técnica", "tecnica", "exercício", "exercicio"]
    )
    has_list = bool(re.search(r"^(\d+\.|- )", body, re.MULTILINE))
    if has_technique_in_body and has_list:
        # Cautela: só marca se título também sugerir
        for kw in PRATICA_KEYWORDS:
            if kw in title_lower:
                return True, "título+corpo"

    return False, ""


def detect_contexts(title: str, summary: str, body: str, original_category: str) -> list[str]:
    """Atribui 1-2 contextos baseado em palavras-chave. Garante pelo menos 1."""
    text = (title + " " + summary + " " + body[:3000]).lower()

    scores = defaultdict(int)
    for ctx, keywords in CONTEXT_KEYWORDS.items():
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in text:
                scores[ctx] += 1
                # Título pesa mais
                if kw_lower in title.lower():
                    scores[ctx] += 2

    # Se nada encontrado, usa a categoria original como fallback
    if not scores:
        fallback = {
            "Autoconhecimento": "autoconhecimento-proposito",
            "Amor": "relacionamentos",
            "Família": "familia-relacoes-parentais",
            "Saúde": "ansiedade-stress",
            "Carreira": "autoconhecimento-proposito",
            "Futuro": "ansiedade-stress",
            "Espiritualidade": "autoconhecimento-proposito",
            "Casa": "autoconhecimento-proposito",
            "Dinheiro": "autoconhecimento-proposito",
            "Alimentação saudável": "ansiedade-stress",
            "Sem categoria": "autoconhecimento-proposito",
        }
        ctx = fallback.get(original_category, "autoconhecimento-proposito")
        return [ctx]

    # Pega top 1-2 contextos (com score >= 2 para o segundo)
    sorted_ctxs = sorted(scores.items(), key=lambda x: -x[1])
    result = [sorted_ctxs[0][0]]
    if len(sorted_ctxs) > 1 and sorted_ctxs[1][1] >= 2:
        result.append(sorted_ctxs[1][0])
    return result


# --- Markdown → HTML --------------------------------------------------------
def md_to_html(md_text: str) -> str:
    """Converte Markdown simples em HTML."""
    lines = md_text.split('\n')
    html_lines = []
    in_ul = False
    in_ol = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_ul:
                html_lines.append("</ul>"); in_ul = False
            if in_ol:
                html_lines.append("</ol>"); in_ol = False
            continue
        if stripped.startswith('👉'):
            continue
        if re.match(r'^Leia (também|aqui|mais):', stripped):
            continue
        if stripped.startswith('# '):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if in_ol: html_lines.append("</ol>"); in_ol = False
            html_lines.append(f"<h2>{html.escape(stripped[2:])}</h2>")
        elif stripped.startswith('## '):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if in_ol: html_lines.append("</ol>"); in_ol = False
            html_lines.append(f"<h3>{html.escape(stripped[3:])}</h3>")
        elif stripped.startswith('### '):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if in_ol: html_lines.append("</ol>"); in_ol = False
            html_lines.append(f"<h4>{html.escape(stripped[4:])}</h4>")
        elif stripped.startswith('*') and stripped.endswith('*') and len(stripped) > 2:
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if in_ol: html_lines.append("</ol>"); in_ol = False
            html_lines.append(f"<p class=\"lead\"><em>{html.escape(stripped.strip('*'))}</em></p>")
        elif re.match(r'^- ', stripped):
            if in_ol: html_lines.append("</ol>"); in_ol = False
            if not in_ul:
                html_lines.append("<ul>"); in_ul = True
            html_lines.append(f"<li>{html.escape(stripped[2:])}</li>")
        elif re.match(r'^\d+\. ', stripped):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if not in_ol:
                html_lines.append("<ol>"); in_ol = True
            html_lines.append(f"<li>{html.escape(re.sub(r'^\d+\. ', '', stripped))}</li>")
        else:
            if in_ul: html_lines.append("</ul>"); in_ul = False
            if in_ol: html_lines.append("</ol>"); in_ol = False
            html_lines.append(f"<p>{html.escape(stripped)}</p>")
    if in_ul: html_lines.append("</ul>")
    if in_ol: html_lines.append("</ol>")
    return "\n".join(html_lines)


# --- Main -------------------------------------------------------------------
def main():
    articles = []
    for md in sorted(MD_DIR.glob('*.md')):
        text = md.read_text(encoding='utf-8')
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.DOTALL)
        if not m:
            continue
        fm = yaml.safe_load(m.group(1))
        body = m.group(2).strip()
        body_clean = re.sub(r'^# .*\n', '', body, count=1)
        body_clean = re.sub(r'^\*[^\n]+\*\n+', '', body_clean, count=1)

        cat_raw = fm.get('categoria', '')
        if isinstance(cat_raw, str):
            cat_raw = cat_raw.strip().strip('"').strip("'")
        if not cat_raw:
            cat_raw = 'Sem categoria'

        date = fm.get('data_publicacao', '')
        if hasattr(date, 'isoformat'):
            date = date.isoformat()
        date_str = (date or '')[:10]
        try:
            y, mo, d = date_str.split('-')
            date_display = f"{d}/{mo}/{y}"
        except Exception:
            date_display = ''

        title = (fm.get('title', '') or md.stem).strip().strip('"').strip("'")

        summary = ''
        if isinstance(fm.get('subtitulo'), str):
            summary = fm['subtitulo'].strip().strip('"').strip("'")
        if not summary:
            for line in body.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('*') and not line.startswith('-'):
                    summary = line[:200] + ('...' if len(line) > 200 else '')
                    break

        keywords = fm.get('palavras_chave', [])
        if isinstance(keywords, list):
            keywords = [str(k).strip() for k in keywords if k]
        elif isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        else:
            keywords = []

        html_body = md_to_html(body_clean)
        word_count = len(re.findall(r'\b[\wÀ-ÿ]+\b', body_clean, flags=re.UNICODE))
        read_time = max(2, round(word_count / 200))

        # Classificação nova
        is_prat, prat_reason = is_pratica(title, body_clean)
        content_type = "pratica" if is_prat else "artigo"
        contexts = detect_contexts(title, summary, body_clean, cat_raw)

        articles.append({
            "slug": md.stem,
            "title": title,
            "summary": summary,
            "categoryOriginal": cat_raw,
            "contentType": content_type,
            "contexts": contexts,
            "contextLabels": [CONTEXT_LABELS[c] for c in contexts],
            "datePublished": date_str,
            "dateDisplay": date_display,
            "keywords": keywords,
            "wordCount": word_count,
            "readTime": read_time,
            "thumbnail": fm.get('thumbnail', ''),
            "html": html_body,
        })

    articles.sort(key=lambda a: a["datePublished"] or '1900-01-01', reverse=True)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[json] {len(articles)} artigos salvos em {OUT_JSON}")
    print(f"       Tamanho: {OUT_JSON.stat().st_size / 1024:.1f} KB")

    # --- Estatística por tipo ---
    print("\nDistribuição por tipo de conteúdo:")
    by_type = defaultdict(int)
    for a in articles:
        by_type[a["contentType"]] += 1
    for t, n in by_type.items():
        print(f"  {t}: {n}")

    print("\nDistribuição por contexto:")
    by_ctx = defaultdict(int)
    for a in articles:
        for c in a["contexts"]:
            by_ctx[c] += 1
    for c, n in sorted(by_ctx.items(), key=lambda x: -x[1]):
        print(f"  {CONTEXT_LABELS.get(c, c)}: {n}")

    # --- Gera planilha Excel para revisão manual da Célia ---
    print(f"\n[xlsx] Gerando planilha de revisão: {OUT_XLSX}")
    wb = Workbook()
    ws = wb.active
    ws.title = "Classificação Artigos"

    headers = ["#", "Título", "Categoria original (Personare)", "Tipo sugerido",
              "Contexto 1", "Contexto 2", "Palavras-chave", "Data", "Palavras",
              "Link original", "Aceita classificação? (S/N)", "Novo tipo (se mudar)",
              "Novo contexto 1 (se mudar)", "Novo contexto 2 (se mudar)", "Observações"]
    ws.append(headers)

    # Estilo cabeçalho
    header_fill = PatternFill("solid", fgColor="a05a3c")
    header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    thin = Side(border_style="thin", color="d9d4c5")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="left", vertical="center")
        cell.border = border
    ws.row_dimensions[1].height = 32

    # Linhas
    alt_fill = PatternFill("solid", fgColor="faf6f1")
    for i, a in enumerate(articles, 1):
        ws.append([
            i,
            a["title"],
            a["categoryOriginal"],
            a["contentType"],
            CONTEXT_LABELS.get(a["contexts"][0], a["contexts"][0]) if a["contexts"] else "",
            CONTEXT_LABELS.get(a["contexts"][1], a["contexts"][1]) if len(a["contexts"]) > 1 else "",
            ", ".join(a["keywords"]),
            a["dateDisplay"],
            a["wordCount"],
            f"https://www.personare.com.br/conteudo/{a['slug']}",
            "",  # Aceita?
            "",  # Novo tipo
            "",  # Novo contexto 1
            "",  # Novo contexto 2
            "",  # Observações
        ])
        row_idx = ws.max_row
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if row_idx % 2 == 0:
                cell.fill = alt_fill

    # Larguras
    widths = {"A": 5, "B": 55, "C": 22, "D": 14, "E": 25, "F": 25, "G": 30,
              "H": 12, "I": 10, "J": 50, "K": 14, "L": 14, "M": 25, "N": 25,
              "O": 35}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    # Aba 2: Resumo
    ws2 = wb.create_sheet("Resumo")
    ws2.append(["Métrica", "Valor"])
    for col in range(1, 3):
        cell = ws2.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
    ws2.row_dimensions[1].height = 28
    ws2.append(["Total de artigos", len(articles)])
    ws2.append(["Saúde Mental (artigos)", by_type.get("artigo", 0)])
    ws2.append(["Caixa de Ferramentas (práticas)", by_type.get("pratica", 0)])
    ws2.append([""])
    ws2.append(["Distribuição por contexto", "Qtd. artigos"])
    for c, n in sorted(by_ctx.items(), key=lambda x: -x[1]):
        ws2.append([CONTEXT_LABELS.get(c, c), n])
    for col in range(1, 3):
        ws2.column_dimensions[get_column_letter(col)].width = 45
    ws2.freeze_panes = "A2"

    # Aba 3: Instruções
    ws3 = wb.create_sheet("Como revisar")
    ws3.column_dimensions["A"].width = 100
    ws3.append(["Como usar esta planilha — para a Célia"])
    ws3["A1"].font = Font(bold=True, size=14, color="a05a3c")
    ws3.append([""])
    ws3.append(["1. Esta planilha contém a classificação automática de todos os seus 98 textos."])
    ws3.append(["2. Para cada texto, o sistema sugeriu:"])
    ws3.append(["   • Um tipo (artigo reflexivo ou prática da Caixa de Ferramentas)"])
    ws3.append(["   • 1-2 contextos terapêuticos (Ansiedade, Relacionamentos, Luto, etc.)"])
    ws3.append([""])
    ws3.append(["3. PARA CADA LINHA, por favor:"])
    ws3.append(["   • Coluna K: marque 'S' se concorda com a classificação, 'N' se não"])
    ws3.append(["   • Se 'N', nas colunas L, M, N preencha o que você acha correto"])
    ws3.append(["   • Coluna O: observações livres (texto solto, sem padrão)"])
    ws3.append([""])
    ws3.append(["4. Não precisa fazer tudo de uma vez. Vá por contexto, ou por data, ou"])
    ws3.append(["   como achar mais confortável. Pode levar semanas — sem pressa."])
    ws3.append([""])
    ws3.append(["5. Quando terminar (ou quando quiser que eu aplique as mudanças),"])
    ws3.append(["   me devolva o arquivo. Eu atualizo o site com suas decisões."])
    for r in range(2, 20):
        for c in range(1, 2):
            ws3.cell(row=r, column=c).alignment = Alignment(vertical="top", wrap_text=True)

    wb.save(OUT_XLSX)
    print(f"[ok] Planilha: {OUT_XLSX}")
    print(f"     Tamanho: {OUT_XLSX.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
