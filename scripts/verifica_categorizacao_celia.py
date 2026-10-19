#!/usr/bin/env python3
"""
Verifica a planilha "Publicações Personare- Com Categorização.xlsx" enviada pela Célia.

Para cada um dos 98 artigos, compara:
- Tipo (Reflexiva/Prática) que a Célia marcou
- vs. Tipo que está no articles.json (site)
- vs. Está no PDF do livro (Sim/Não)

Regra lógica:
- Reflexiva DEVERIA estar no livro (é o que define reflexiva)
- Prática DEVERIA NÃO estar no livro

Adiciona 3 colunas novas na planilha da Célia:
1. "Está no livro?" — Sim / Não
2. "Tipo no site" — Reflexiva / Prática (o que está no articles.json)
3. "Divergência (vs livro)" — OK / ⚠️ Divergência / ❓ Revisar

Salva a planilha de volta em /home/z/my-project/download/Publicações-Personare-Com-Categorização-COM-VERIFICAÇÃO.xlsx
"""

import json
import subprocess
import unicodedata
import re
import shutil
from pathlib import Path
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EXCEL_IN = Path("/home/z/my-project/upload/Publicações Personare- Com Categorização.xlsx")
EXCEL_OUT = Path("/home/z/my-project/download/Publicacoes-Personare-Com-Categorizacao-COM-VERIFICACAO.xlsx")
ARTICLES_JSON = Path("/home/z/my-project/src/data/articles.json")
PDF_PATH = Path("/home/z/my-project/download/Celia-Lima-Caminhos-do-Autoconhecimento.pdf")
OUT_DIR = Path("/home/z/my-project/download")

def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# --- 1. Carrega articles.json (fonte do site) ---
articles = json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))
print(f"[info] articles.json: {len(articles)} artigos")

# Map: slug → artigo
by_slug = {a.get("slug"): a for a in articles}
# Map: normalized_title → artigo
by_norm_title = {normalize(a.get("title", "")): a for a in articles}

# --- 2. Extrai texto do PDF do livro ---
print(f"[info] Extraindo texto do PDF...")
pdf_text = subprocess.run(
    ["pdftotext", "-layout", str(PDF_PATH), "-"],
    capture_output=True, text=True, check=True
).stdout
pdf_norm = normalize(pdf_text)
print(f"  Texto extraído: {len(pdf_text)} chars")

# Lista de títulos que estão no livro (usando os 67 reflexivas do articles.json)
# Como já verificamos antes: o PDF tem exatamente as 67 reflexivas do articles.json
reflexivas_articles = [a for a in articles if a.get("contentType") == "artigo"]
praticas_articles = [a for a in articles if a.get("contentType") == "pratica"]
print(f"[info] Reflexivas no articles.json (também no PDF): {len(reflexivas_articles)}")
print(f"[info] Práticas no articles.json (não no PDF): {len(praticas_articles)}")

# Set de slugs das reflexivas (= as que estão no livro)
slugs_no_livro = {a.get("slug") for a in reflexivas_articles}
# Set de títulos normalizados das reflexivas
norm_titles_no_livro = {normalize(a.get("title", "")) for a in reflexivas_articles}

# --- 3. Carrega a planilha da Célia ---
wb = load_workbook(EXCEL_IN, data_only=True)
ws = wb.active
print(f"\n[info] Planilha da Célia: '{ws.title}'")
print(f"  Linhas: {ws.max_row}, Colunas: {ws.max_column}")

# Headers atuais
headers_atuais = [c.value for c in ws[1]]
print(f"  Headers: {headers_atuais}")

# --- 4. Adiciona 3 novas colunas ---
# Encontra primeira coluna livre
col_inicio = ws.max_column + 1
col_esta_no_livro = col_inicio
col_tipo_site = col_inicio + 1
col_divergencia = col_inicio + 2

# Headers novos
ws.cell(row=1, column=col_esta_no_livro, value="Está no livro?")
ws.cell(row=1, column=col_tipo_site, value="Tipo no site (articles.json)")
ws.cell(row=1, column=col_divergencia, value="Divergência (vs livro)")

# Estilo headers novos (mesmo padrão dos existentes, mas em destaque)
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_fill = PatternFill("solid", fgColor="3D3530")  # marrom escuro
header_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
thin_border = Border(
    left=Side(style="thin", color="D8CFC0"),
    right=Side(style="thin", color="D8CFC0"),
    top=Side(style="thin", color="D8CFC0"),
    bottom=Side(style="thin", color="D8CFC0"),
)
for col in [col_esta_no_livro, col_tipo_site, col_divergencia]:
    c = ws.cell(row=1, column=col)
    c.font = header_font
    c.fill = header_fill
    c.alignment = header_align
    c.border = thin_border

# Estilos para os status
fill_ok = PatternFill("solid", fgColor="D8E8D0")         # verde claro
fill_divergencia = PatternFill("solid", fgColor="FFE4E1")  # rosa claro (atenção)
fill_faltante = PatternFill("solid", fgColor="FFF8DC")    # creme (info)
fill_campo_vazio = PatternFill("solid", fgColor="FFE4B5")  # amarelo (sem tipo)

body_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

# --- 5. Para cada linha (artigo), calcula o status ---
# Estrutura: assume que a planilha tem colunas: #, Título, Tipo, Contexto, Tags, Data, Slug
# Vou localizar as colunas por nome
col_idx = {h: i + 1 for i, h in enumerate(headers_atuais) if h}
print(f"  Mapa de colunas: {col_idx}")

# Encontra coluna do título e do tipo (podem ter nomes variados)
col_titulo = col_idx.get("Título") or col_idx.get("Titulo")
col_tipo_celia = col_idx.get("Tipo")
col_slug = col_idx.get("Slug")
col_contexto = col_idx.get("Contexto")

print(f"  Coluna Título: {col_titulo}")
print(f"  Coluna Tipo: {col_tipo_celia}")
print(f"  Coluna Slug: {col_slug}")
print(f"  Coluna Contexto: {col_contexto}")

# Estatísticas
stats = {
    "ok": 0,           # bate com o livro
    "divergencia": 0,   # não bate
    "sem_tipo": 0,      # campo tipo vazio
    "nao_no_site": 0,   # artigo não encontrado no articles.json
}

# Lista para relatório final
relatorio = []

# Itera linhas (pula header)
for row_idx in range(2, ws.max_row + 1):
    # Pega o ID da planilha (coluna '#') — é o que a Célia vê
    id_planilha = ws.cell(row=row_idx, column=col_idx.get("#", 1)).value
    titulo = ws.cell(row=row_idx, column=col_titulo).value
    tipo_celia = ws.cell(row=row_idx, column=col_tipo_celia).value
    slug = ws.cell(row=row_idx, column=col_slug).value if col_slug else None
    contexto = ws.cell(row=row_idx, column=col_contexto).value if col_contexto else None

    if not titulo:
        continue

    # Limpa tipo (pode ter espaços, maiúsculas diferentes)
    tipo_celia_clean = str(tipo_celia).strip() if tipo_celia else ""
    # Normaliza "Reflexiva"/"Prática" — aceita variações
    tipo_celia_norm = ""
    if tipo_celia_clean:
        if "reflex" in tipo_celia_clean.lower():
            tipo_celia_norm = "Reflexiva"
        elif "prát" in tipo_celia_clean.lower() or "prat" in tipo_celia_clean.lower():
            tipo_celia_norm = "Prática"

    # Encontra o artigo no articles.json (por slug, depois por título)
    artigo_site = None
    if slug:
        artigo_site = by_slug.get(slug)
    if not artigo_site:
        norm_titulo = normalize(titulo)
        artigo_site = by_norm_title.get(norm_titulo)

    # Determina: está no livro?
    # Se o artigo está no articles.json como "artigo" → está no livro
    # Se não está no articles.json → não temos certeza, marca ❓
    if artigo_site:
        esta_no_livro = "Sim" if artigo_site.get("contentType") == "artigo" else "Não"
        tipo_site = "Reflexiva" if artigo_site.get("contentType") == "artigo" else "Prática"
    else:
        # Não encontramos no articles.json — verifica pelo texto do PDF
        norm_titulo = normalize(titulo)
        # Tenta com primeiras 4 palavras
        palavras = norm_titulo.split()
        if len(palavras) >= 4:
            busca = " ".join(palavras[:4])
            if busca in pdf_norm:
                esta_no_livro = "Sim (encontrado no PDF)"
                tipo_site = "(não está no site)"
            else:
                esta_no_livro = "Não"
                tipo_site = "(não está no site)"
        else:
            esta_no_livro = "❓"
            tipo_site = "(não está no site)"
        stats["nao_no_site"] += 1

    # Determina divergência:
    # Regra: Reflexiva ↔ Sim (está no livro) | Prática ↔ Não (não está no livro)
    if not tipo_celia_norm:
        divergencia = "❓ Sem tipo informado"
        stats["sem_tipo"] += 1
    elif esta_no_livro.startswith("Sim"):
        # Está no livro → tem que ser Reflexiva
        if tipo_celia_norm == "Reflexiva":
            divergencia = "✅ OK"
            stats["ok"] += 1
        else:
            divergencia = "⚠️ Divergência: está no livro mas marcado como Prática"
            stats["divergencia"] += 1
    elif esta_no_livro.startswith("Não"):
        # Não está no livro → tem que ser Prática
        if tipo_celia_norm == "Prática":
            divergencia = "✅ OK"
            stats["ok"] += 1
        else:
            divergencia = "⚠️ Divergência: NÃO está no livro mas marcado como Reflexiva"
            stats["divergencia"] += 1
    else:
        divergencia = "❓ Não foi possível verificar"
        stats["sem_tipo"] += 1

    # Escreve nas 3 colunas novas
    ws.cell(row=row_idx, column=col_esta_no_livro, value=esta_no_livro)
    ws.cell(row=row_idx, column=col_tipo_site, value=tipo_site)
    ws.cell(row=row_idx, column=col_divergencia, value=divergencia)

    # Aplica estilo (cores)
    fill_to_use = fill_ok if "OK" in divergencia else (
        fill_divergencia if "Divergência" in divergencia else (
            fill_campo_vazio if "Sem tipo" in divergencia else fill_faltante
        )
    )
    for col in [col_esta_no_livro, col_tipo_site, col_divergencia]:
        c = ws.cell(row=row_idx, column=col)
        c.alignment = body_align
        c.border = thin_border
        c.fill = fill_to_use

    relatorio.append({
        "id_planilha": id_planilha,  # ← o que aparece na coluna # da planilha
        "linha_excel": row_idx,        # ← linha do Excel (interno)
        "titulo": titulo,
        "tipo_celia": tipo_celia_clean,
        "tipo_site": tipo_site,
        "esta_no_livro": esta_no_livro,
        "divergencia": divergencia,
        "slug": slug,
        "contexto": contexto,
    })

# --- 6. Ajusta larguras das novas colunas ---
ws.column_dimensions[get_column_letter(col_esta_no_livro)].width = 18
ws.column_dimensions[get_column_letter(col_tipo_site)].width = 22
ws.column_dimensions[get_column_letter(col_divergencia)].width = 50

# --- 7. Adiciona aba "Resumo" ---
ws_resumo = wb.create_sheet("Resumo da Verificação", 0)  # 0 = primeira posição

ws_resumo["A1"] = "Verificação da Planilha — Resumo"
ws_resumo["A1"].font = Font(name="Calibri", size=18, bold=True, color="3D3530")
ws_resumo["A1"].alignment = Alignment(horizontal="left", vertical="center")
ws_resumo.merge_cells("A1:B1")
ws_resumo.row_dimensions[1].height = 32

ws_resumo["A3"] = "Total de artigos verificados:"
ws_resumo["B3"] = len(relatorio)
ws_resumo["A4"] = "✅ OK (classificação bate com o livro):"
ws_resumo["B4"] = stats["ok"]
ws_resumo["A5"] = "⚠️ Divergências (precisa revisar):"
ws_resumo["B5"] = stats["divergencia"]
ws_resumo["A6"] = "❓ Sem tipo informado:"
ws_resumo["B6"] = stats["sem_tipo"]
ws_resumo["A7"] = "❓ Não encontrados no articles.json do site:"
ws_resumo["B7"] = stats["nao_no_site"]

# Estilo
for row in range(3, 8):
    for col in ["A", "B"]:
        c = ws_resumo[f"{col}{row}"]
        c.font = Font(name="Calibri", size=12,
                      bold=(col == "A"),
                      color="3D3530")
        c.alignment = Alignment(horizontal="left", vertical="center")
        c.border = thin_border

# Destaque nos números (só preenche se tiver valor diferente de zero)
if stats["ok"] > 0:
    ws_resumo["B4"].fill = fill_ok
if stats["divergencia"] > 0:
    ws_resumo["B5"].fill = fill_divergencia
elif stats["ok"] > 0:
    ws_resumo["B5"].fill = fill_ok
if stats["sem_tipo"] > 0:
    ws_resumo["B6"].fill = fill_campo_vazio
if stats["nao_no_site"] > 0:
    ws_resumo["B7"].fill = fill_faltante

ws_resumo.column_dimensions["A"].width = 50
ws_resumo.column_dimensions["B"].width = 12

# Lista divergências em detalhe
linha_inicial = 10
ws_resumo[f"A{linha_inicial}"] = "Lista de divergências (se houver):"
ws_resumo[f"A{linha_inicial}"].font = Font(name="Calibri", size=14, bold=True, color="3D3530")
ws_resumo.merge_cells(f"A{linha_inicial}:E{linha_inicial}")

if stats["divergencia"] > 0 or stats["sem_tipo"] > 0:
    # Headers da lista
    linha_inicial += 2
    headers_lista = ["ID #", "Título", "Tipo informado", "Tipo no site", "Está no livro?", "Divergência"]
    for col, h in enumerate(headers_lista, 1):
        c = ws_resumo.cell(row=linha_inicial, column=col, value=h)
        c.font = header_font
        c.fill = header_fill
        c.alignment = header_align
        c.border = thin_border

    # Lista de divergências
    for r in relatorio:
        if "Divergência" in r["divergencia"] or "Sem tipo" in r["divergencia"] or "Não foi possível" in r["divergencia"]:
            linha_inicial += 1
            ws_resumo.cell(row=linha_inicial, column=1, value=r["id_planilha"])  # ← agora usa ID da planilha
            ws_resumo.cell(row=linha_inicial, column=2, value=r["titulo"])
            ws_resumo.cell(row=linha_inicial, column=3, value=r["tipo_celia"])
            ws_resumo.cell(row=linha_inicial, column=4, value=r["tipo_site"])
            ws_resumo.cell(row=linha_inicial, column=5, value=r["esta_no_livro"])
            ws_resumo.cell(row=linha_inicial, column=6, value=r["divergencia"])
            for col in range(1, 7):
                c = ws_resumo.cell(row=linha_inicial, column=col)
                c.alignment = body_align
                c.border = thin_border
                c.fill = fill_divergencia if "Divergência" in r["divergencia"] else fill_campo_vazio
    # Larguras
    widths = [8, 55, 18, 18, 18, 50]
    for col, w in enumerate(widths, 1):
        ws_resumo.column_dimensions[get_column_letter(col)].width = w
else:
    linha_inicial += 2
    ws_resumo.cell(row=linha_inicial, column=1, value="✅ Nenhuma divergência encontrada. Toda a classificação está correta!")
    ws_resumo.cell(row=linha_inicial, column=1).font = Font(name="Calibri", size=14, bold=True, color="5B7A3C")

# Salva
wb.save(EXCEL_OUT)
print(f"\n[ok] Planilha verificada salva em: {EXCEL_OUT}")
print(f"     Tamanho: {EXCEL_OUT.stat().st_size / 1024:.1f} KB")

# Salva relatório JSON
relatorio_out = OUT_DIR / "verificacao_categorizacao_celia.json"
relatorio_out.write_text(json.dumps({
    "estatisticas": stats,
    "total_verificado": len(relatorio),
    "detalhes": relatorio,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[ok] Relatório JSON: {relatorio_out}")

# --- Resumo no console ---
print(f"\n{'=' * 60}")
print(f"RESUMO DA VERIFICAÇÃO")
print(f"{'=' * 60}")
print(f"Total verificado: {len(relatorio)} artigos")
print(f"✅ OK:                  {stats['ok']}")
print(f"⚠️ Divergências:         {stats['divergencia']}")
print(f"❓ Sem tipo:             {stats['sem_tipo']}")
print(f"❓ Não encontrados site: {stats['nao_no_site']}")
print()

if stats["divergencia"] > 0:
    print(f"\n>>> Divergências (precisam revisão):")
    for r in relatorio:
        if "Divergência" in r["divergencia"]:
            print(f"  ID {r['id_planilha']}: {r['titulo']!r}")
            print(f"    Marcado como: {r['tipo_celia']}")
            print(f"    Tipo no site: {r['tipo_site']}")
            print(f"    Está no livro? {r['esta_no_livro']}")
            print(f"    Slug: {r['slug']}")
            print(f"    → {r['divergencia']}")
            print()

if stats["sem_tipo"] > 0:
    print(f"\n>>> Sem tipo informado:")
    for r in relatorio:
        if "Sem tipo" in r["divergencia"]:
            print(f"  ID {r['id_planilha']}: {r['titulo']!r}")
