#!/usr/bin/env python3
"""
Verifica se os 67 artigos classificados como 'artigo' (reflexiva) no articles.json
são exatamente os mesmos 67 que estão no livro PDF.

Estratégia: extrair todos os títulos do PDF do livro via pdftotext e comparar com
a lista de reflexivas do articles.json.
"""

import json
import subprocess
import unicodedata
import re
from pathlib import Path
from collections import Counter

ARTICLES_JSON = Path("/home/z/my-project/src/data/articles.json")
PDF_PATH = Path("/home/z/my-project/download/Celia-Lima-Caminhos-do-Autoconhecimento.pdf")
NORM_TO_TIPO = Path("/home/z/my-project/download/norm_to_tipo.json")

def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# 1. Lista de reflexivas do articles.json
articles = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
reflexivas_articles = [a for a in articles if a.get("contentType") == "artigo"]
praticas_articles = [a for a in articles if a.get("contentType") == "pratica"]
print(f"articles.json:")
print(f"  Reflexivas (contentType='artigo'): {len(reflexivas_articles)}")
print(f"  Práticas   (contentType='pratica'): {len(praticas_articles)}")

reflexivas_norms = {normalize(a["title"]): a["title"] for a in reflexivas_articles}
praticas_norms = {normalize(a["title"]): a["title"] for a in praticas_articles}

# 2. Extrai texto do PDF
print(f"\n[info] Extraindo texto do PDF: {PDF_PATH}")
result = subprocess.run(
    ["pdftotext", "-layout", str(PDF_PATH), "-"],
    capture_output=True, text=True, check=True
)
pdf_text = result.stdout
print(f"  Texto extraído: {len(pdf_text)} chars")

# 3. Lista de reflexivas do Excel
norm_to_tipo = json.loads(NORM_TO_TIPO.read_text(encoding="utf-8"))
reflexivas_excel = {k: v for k, v in norm_to_tipo.items() if v["tipo"] == "Reflexiva"}
praticas_excel = {k: v for k, v in norm_to_tipo.items() if v["tipo"] == "Prática"}
print(f"\nExcel sheet2 'Nova Categorias acrescentadas':")
print(f"  Reflexivas: {len(reflexivas_excel)}")
print(f"  Práticas:   {len(praticas_excel)}")

# 4. Compara reflexivas articles.json vs Excel
reflexivas_json_set = set(reflexivas_norms.keys())
reflexivas_excel_set = set(reflexivas_excel.keys())
print(f"\n=== Reflexivas: articles.json vs Excel ===")
print(f"  Em ambos: {len(reflexivas_json_set & reflexivas_excel_set)}")
print(f"  Só no articles.json: {len(reflexivas_json_set - reflexivas_excel_set)}")
print(f"  Só no Excel: {len(reflexivas_excel_set - reflexivas_json_set)}")
diff_json_only = reflexivas_json_set - reflexivas_excel_set
diff_excel_only = reflexivas_excel_set - reflexivas_json_set
if diff_json_only:
    print(f"  >>> Só no articles.json:")
    for n in diff_json_only:
        print(f"      - {reflexivas_norms[n]!r}")
if diff_excel_only:
    print(f"  >>> Só no Excel:")
    for n in diff_excel_only:
        print(f"      - {reflexivas_excel[n]['titulo_original']!r}")

# 5. Compara práticas articles.json vs Excel
praticas_json_set = set(praticas_norms.keys())
praticas_excel_set = set(praticas_excel.keys())
print(f"\n=== Práticas: articles.json vs Excel ===")
print(f"  Em ambos: {len(praticas_json_set & praticas_excel_set)}")
print(f"  Só no articles.json: {len(praticas_json_set - praticas_excel_set)}")
print(f"  Só no Excel: {len(praticas_excel_set - praticas_json_set)}")
diff_json_only = praticas_json_set - praticas_excel_set
diff_excel_only = praticas_excel_set - praticas_json_set
if diff_json_only:
    print(f"  >>> Só no articles.json:")
    for n in diff_json_only:
        print(f"      - {praticas_norms[n]!r}")
if diff_excel_only:
    print(f"  >>> Só no Excel:")
    for n in diff_excel_only:
        print(f"      - {praticas_excel[n]['titulo_original']!r}")

# 6. Verifica quais títulos do PDF aparecem no texto
# (Nem todos os títulos podem ser extraídos perfeitamente do PDF, mas dá uma boa checagem)
print(f"\n=== Verificação cruzada com PDF do livro ===")
# Para cada reflexiva do articles.json, busca no texto do PDF
encontrados_no_pdf = 0
nao_encontrados_no_pdf = []
for norm, original_title in reflexivas_norms.items():
    # Tenta várias formas: título normalizado, primeiras palavras, etc
    # Como o pdftotext pode ter hifenização, espaços diferentes, etc.
    # Busca por primeiras 4 palavras
    palavras = norm.split()
    # Tenta com 4 palavras
    if len(palavras) >= 4:
        busca = " ".join(palavras[:4])
        busca_norm = normalize(busca)  # já está normalizado
        # Procura no texto do PDF (também normalizado)
        pdf_norm = normalize(pdf_text)
        if busca_norm in pdf_norm:
            encontrados_no_pdf += 1
        else:
            # Tenta com 3 palavras
            busca3 = " ".join(palavras[:3])
            if busca3 in pdf_norm:
                encontrados_no_pdf += 1
            else:
                nao_encontrados_no_pdf.append(original_title)
    else:
        # Título curto, busca direto
        pdf_norm = normalize(pdf_text)
        if norm in pdf_norm:
            encontrados_no_pdf += 1
        else:
            nao_encontrados_no_pdf.append(original_title)

print(f"  Reflexivas do articles.json encontradas no PDF: {encontrados_no_pdf}/{len(reflexivas_norms)}")
if nao_encontrados_no_pdf:
    print(f"  >>> Não encontradas no PDF ({len(nao_encontrados_no_pdf)}):")
    for t in nao_encontrados_no_pdf[:10]:
        print(f"      - {t!r}")

# 7. Verifica se alguma PRÁTICA está no PDF (não deveria estar)
print(f"\n=== Práticas NÃO deveriam estar no PDF do livro ===")
praticas_no_pdf = []
for norm, original_title in praticas_norms.items():
    palavras = norm.split()
    if len(palavras) >= 4:
        busca = " ".join(palavras[:4])
        pdf_norm = normalize(pdf_text)
        if busca in pdf_norm:
            praticas_no_pdf.append(original_title)
        else:
            # Tenta 3
            busca3 = " ".join(palavras[:3])
            if busca3 in pdf_norm:
                praticas_no_pdf.append(original_title)
    else:
        pdf_norm = normalize(pdf_text)
        if norm in pdf_norm:
            praticas_no_pdf.append(original_title)

if praticas_no_pdf:
    print(f"  ⚠️ {len(praticas_no_pdf)} práticas aparecem no PDF do livro:")
    for t in praticas_no_pdf[:10]:
        print(f"      - {t!r}")
else:
    print(f"  ✅ Nenhuma prática aparece no PDF do livro — coerente!")

# Salva relatório
relatorio = {
    "articles_json": {
        "reflexivas": len(reflexivas_articles),
        "praticas": len(praticas_articles),
        "reflexivas_titulos": [a["title"] for a in reflexivas_articles],
        "praticas_titulos": [a["title"] for a in praticas_articles],
    },
    "excel_sheet2": {
        "reflexivas": len(reflexivas_excel),
        "praticas": len(praticas_excel),
        "reflexivas_titulos": [v["titulo_original"] for v in reflexivas_excel.values()],
        "praticas_titulos": [v["titulo_original"] for v in praticas_excel.values()],
    },
    "diferencas_reflexivas": {
        "so_articles_json": [reflexivas_norms[n] for n in diff_json_only],
        "so_excel": [reflexivas_excel[n]["titulo_original"] for n in diff_excel_only],
    },
    "pdf_livro": {
        "reflexivas_encontradas_no_pdf": encontrados_no_pdf,
        "reflexivas_nao_encontradas": nao_encontrados_no_pdf,
        "praticas_no_pdf": praticas_no_pdf,
    },
}
out = Path("/home/z/my-project/download/cruzamento_livro_excel_articles.json")
out.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n[ok] Relatório salvo: {out}")
