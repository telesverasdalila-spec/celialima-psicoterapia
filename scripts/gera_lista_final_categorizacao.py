#!/usr/bin/env python3
"""
Gera a lista final de classificação dos 98 artigos:
- 67 reflexivas (= as que estão no PDF do livro)
- 31 práticas (= as que não estão no livro)

Cria:
1. Um Excel "Lista-Final-Categorizacao.xlsx" com 3 abas:
   - "Reflexivas (no livro)" — 67 artigos
   - "Práticas" — 31 artigos
   - "Comparação com Excel enviado" — mostra a 1 divergência
2. Um JSON "classificacao_final.json" — para futura aplicação no site
"""

import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ARTICLES_JSON = Path("/home/z/my-project/src/data/articles.json")
NORM_TO_TIPO = Path("/home/z/my-project/download/norm_to_tipo.json")
OUT_DIR = Path("/home/z/my-project/download")

articles = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
norm_to_tipo = json.loads(NORM_TO_TIPO.read_text(encoding="utf-8"))

import unicodedata, re
def normalize(s):
    s = unicodedata.normalize("NFD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# Separa por contentType
reflexivas = [a for a in articles if a.get("contentType") == "artigo"]
praticas = [a for a in articles if a.get("contentType") == "pratica"]
print(f"Reflexivas: {len(reflexivas)}")
print(f"Práticas:   {len(praticas)}")

# Ordena reflexivas pelo contexto e título
reflexivas.sort(key=lambda a: (a.get("contextLabels", [""])[0], a.get("title", "")))
praticas.sort(key=lambda a: (a.get("contextLabels", [""])[0], a.get("title", "")))

# === Gera Excel ===
wb = Workbook()

# Estilos
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_fill_reflexiva = PatternFill("solid", fgColor="A05A3C")  # terracota
header_fill_pratica = PatternFill("solid", fgColor="7A8A5B")    # verde sálvia
header_fill_compara = PatternFill("solid", fgColor="3D3530")    # marrom escuro
header_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
body_align = Alignment(horizontal="left", vertical="top", wrap_text=True)
thin_border = Border(
    left=Side(style="thin", color="D8CFC0"),
    right=Side(style="thin", color="D8CFC0"),
    top=Side(style="thin", color="D8CFC0"),
    bottom=Side(style="thin", color="D8CFC0"),
)

# --- Aba 1: Reflexivas (no livro) ---
ws1 = wb.active
ws1.title = "Reflexivas (no livro)"
headers = ["#", "Título", "Contexto", "Tags/Palavras-chave", "Data publicação", "Slug"]
for col, h in enumerate(headers, 1):
    c = ws1.cell(row=1, column=col, value=h)
    c.font = header_font
    c.fill = header_fill_reflexiva
    c.alignment = header_align
    c.border = thin_border

for i, a in enumerate(reflexivas, 1):
    row = i + 1
    ws1.cell(row=row, column=1, value=i).border = thin_border
    ws1.cell(row=row, column=2, value=a.get("title", "")).border = thin_border
    ws1.cell(row=row, column=3, value=a.get("contextLabels", [""])[0] if a.get("contextLabels") else "").border = thin_border
    ws1.cell(row=row, column=4, value=", ".join(a.get("tags", []))).border = thin_border
    ws1.cell(row=row, column=5, value=a.get("datePublished", "")).border = thin_border
    ws1.cell(row=row, column=6, value=a.get("slug", "")).border = thin_border
    for col in range(1, 7):
        ws1.cell(row=row, column=col).alignment = body_align

# Larguras
widths = [4, 60, 38, 38, 16, 40]
for col, w in enumerate(widths, 1):
    ws1.column_dimensions[get_column_letter(col)].width = w
ws1.freeze_panes = "A2"

# --- Aba 2: Práticas ---
ws2 = wb.create_sheet("Práticas")
for col, h in enumerate(headers, 1):
    c = ws2.cell(row=1, column=col, value=h)
    c.font = header_font
    c.fill = header_fill_pratica
    c.alignment = header_align
    c.border = thin_border

for i, a in enumerate(praticas, 1):
    row = i + 1
    ws2.cell(row=row, column=1, value=i).border = thin_border
    ws2.cell(row=row, column=2, value=a.get("title", "")).border = thin_border
    ws2.cell(row=row, column=3, value=a.get("contextLabels", [""])[0] if a.get("contextLabels") else "").border = thin_border
    ws2.cell(row=row, column=4, value=", ".join(a.get("tags", []))).border = thin_border
    ws2.cell(row=row, column=5, value=a.get("datePublished", "")).border = thin_border
    ws2.cell(row=row, column=6, value=a.get("slug", "")).border = thin_border
    for col in range(1, 7):
        ws2.cell(row=row, column=col).alignment = body_align

for col, w in enumerate(widths, 1):
    ws2.column_dimensions[get_column_letter(col)].width = w
ws2.freeze_panes = "A2"

# --- Aba 3: Comparação com Excel enviado ---
ws3 = wb.create_sheet("Comparação com Excel")
headers3 = ["#", "Título", "Tipo no articles.json (site)", "Tipo no Excel (enviado)",
            "Está no PDF do livro?", "Divergência?"]
for col, h in enumerate(headers3, 1):
    c = ws3.cell(row=1, column=col, value=h)
    c.font = header_font
    c.fill = header_fill_compara
    c.alignment = header_align
    c.border = thin_border

all_articles = sorted(articles, key=lambda a: a.get("title", "").lower())
divergencias = 0
nao_no_excel = 0
for i, a in enumerate(all_articles, 1):
    row = i + 1
    title = a.get("title", "")
    tipo_json = a.get("contentType", "")
    tipo_json_label = "Reflexiva" if tipo_json == "artigo" else "Prática"
    # Busca no Excel
    norm = normalize(title)
    excel_match = norm_to_tipo.get(norm)
    if not excel_match:
        # Tenta parcial
        for k, v in norm_to_tipo.items():
            if norm and k and (norm in k or k in norm) and min(len(norm), len(k)) > 10:
                excel_match = v
                break
    if excel_match:
        tipo_excel = excel_match["tipo"]
    else:
        tipo_excel = "(não está no Excel)"
        nao_no_excel += 1
    no_pdf = "Sim" if tipo_json == "artigo" else "Não"
    # Divergência só conta se o artigo ESTÁ no Excel e tem tipo diferente
    if excel_match and tipo_json_label != tipo_excel:
        divergencia = "Sim"
        divergencias += 1
    elif not excel_match:
        divergencia = "Faltante no Excel"
    else:
        divergencia = ""
    ws3.cell(row=row, column=1, value=i).border = thin_border
    ws3.cell(row=row, column=2, value=title).border = thin_border
    ws3.cell(row=row, column=3, value=tipo_json_label).border = thin_border
    ws3.cell(row=row, column=4, value=tipo_excel).border = thin_border
    ws3.cell(row=row, column=5, value=no_pdf).border = thin_border
    ws3.cell(row=row, column=6, value=divergencia).border = thin_border
    for col in range(1, 7):
        ws3.cell(row=row, column=col).alignment = body_align
    if divergencia == "Sim":
        # Divergência real — vermelho claro
        for col in range(1, 7):
            ws3.cell(row=row, column=col).fill = PatternFill("solid", fgColor="FFE4E1")  # rosa claro
    elif divergencia == "Faltante no Excel":
        # Amarelo claro (atenção mas não divergência)
        for col in range(1, 7):
            ws3.cell(row=row, column=col).fill = PatternFill("solid", fgColor="FFF8DC")  # creme

print(f"\n[comparação] Divergências reais: {divergencias}")
print(f"[comparação] Faltantes no Excel: {nao_no_excel}")

widths3 = [4, 60, 22, 22, 18, 16]
for col, w in enumerate(widths3, 1):
    ws3.column_dimensions[get_column_letter(col)].width = w
ws3.freeze_panes = "A2"

# Salva Excel
out_xlsx = OUT_DIR / "Lista-Final-Categorizacao.xlsx"
wb.save(out_xlsx)
print(f"\n[ok] Excel salvo: {out_xlsx} ({out_xlsx.stat().st_size / 1024:.1f} KB)")

# === Gera JSON estruturado para aplicação no site ===
out_json = OUT_DIR / "classificacao_final.json"
final = {
    "gerado_em": "2026-10-19",
    "total_artigos": len(articles),
    "reflexivas_count": len(reflexivas),
    "praticas_count": len(praticas),
    "reflexivas": [
        {
            "slug": a.get("slug"),
            "title": a.get("title"),
            "context": a.get("contextLabels", [None])[0],
            "tags": a.get("tags", []),
            "datePublished": a.get("datePublished"),
            "summary": a.get("summary"),
            "wordCount": a.get("wordCount"),
            "readTime": a.get("readTime"),
        }
 for a in reflexivas
    ],
    "praticas": [
        {
            "slug": a.get("slug"),
            "title": a.get("title"),
            "context": a.get("contextLabels", [None])[0],
            "tags": a.get("tags", []),
            "datePublished": a.get("datePublished"),
            "summary": a.get("summary"),
            "wordCount": a.get("wordCount"),
            "readTime": a.get("readTime"),
        }
        for a in praticas
    ],
    "divergencias_com_excel": [
        {
            "title": a.get("title"),
            "no_articles_json": "Reflexiva" if a.get("contentType") == "artigo" else "Prática",
            "no_excel": (norm_to_tipo.get(normalize(a.get("title", "")), {}) or {}).get("tipo", "(não está no Excel)"),
            "no_pdf_do_livro": "Sim" if a.get("contentType") == "artigo" else "Não",
        }
        for a in articles
        if (
            # Inclui divergências reais
            normalize(a.get("title", "")) in norm_to_tipo
            and ("Reflexiva" if a.get("contentType") == "artigo" else "Prática")
                != norm_to_tipo.get(normalize(a.get("title", "")), {}).get("tipo", "")
        ) or (
            # Inclui também os que não estão no Excel
            normalize(a.get("title", "")) not in norm_to_tipo
        )
    ],
}
out_json.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[ok] JSON salvo: {out_json}")
print(f"     Divergências: {len(final['divergencias_com_excel'])}")
for d in final["divergencias_com_excel"]:
    print(f"       - {d['title']!r}: site={d['no_articles_json']} | excel={d['no_excel']} | livro={d['no_pdf_do_livro']}")
