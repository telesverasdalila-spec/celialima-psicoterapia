#!/usr/bin/env python3
"""
Lê o Excel "REcuperação da Lista de Categorização.xlsx" enviado pelo usuário.
Extrai as duas abas e gera relatório comparativo:
  Sheet1: classificação antiga (Tipo vazio, Contexto preenchido)
  Sheet2 "Nova Categorias acrescentadas": classificação final (Tipo = Reflexiva/Prática)
"""

from openpyxl import load_workbook
from pathlib import Path
import json
import unicodedata
import re

EXCEL = Path("/home/z/my-project/upload/REcuperação da  Lista de Categorização.xlsx")
OUT_DIR = Path("/home/z/my-project/download")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Normaliza títulos para matching (sem acento, lowercase, sem espaços extras) ---
def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# --- Carrega Excel ---
wb = load_workbook(EXCEL, data_only=True)
print(f"Abas: {wb.sheetnames}")

# --- Sheet1 (classificação antiga) ---
sheet1 = wb[wb.sheetnames[0]]
print(f"\n=== {wb.sheetnames[0]} ===")
print(f"Linhas: {sheet1.max_row}, Colunas: {sheet1.max_column}")

# Header
headers_s1 = [c.value for c in sheet1[1]]
print(f"Headers: {headers_s1}")

sheet1_rows = []
for row in sheet1.iter_rows(min_row=2, values_only=True):
    if not row[0]:
        continue
    sheet1_rows.append({
        "titulo": row[0],
        "categoria_original": row[1],
        "keywords_original": row[2],
        "tipo_old": row[3],
        "contexto_old": row[4],
        "palavra_chave_sugerida_old": row[5],
    })
print(f"Total rows sheet1: {len(sheet1_rows)}")

# --- Sheet2 (Nova Categorias acrescentadas — classificação final) ---
sheet2_name = wb.sheetnames[1] if len(wb.sheetnames) > 1 else None
sheet2 = wb[sheet2_name] if sheet2_name else None
print(f"\n=== {sheet2_name} ===")
if sheet2:
    print(f"Linhas: {sheet2.max_row}, Colunas: {sheet2.max_column}")
    headers_s2 = [c.value for c in sheet2[1]]
    print(f"Headers: {headers_s2}")
    sheet2_rows = []
    for row in sheet2.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        sheet2_rows.append({
            "titulo": row[0],
            "contexto_final": row[1],
            "tipo_final": row[2],
            "tags_final": row[3],
        })
    print(f"Total rows sheet2: {len(sheet2_rows)}")

# --- Conta tipos ---
from collections import Counter
tipo_counts = Counter(r["tipo_final"] for r in sheet2_rows)
print(f"\nDistribuição por tipo (sheet2):")
for t, n in tipo_counts.most_common():
    print(f"  {t}: {n}")

contexto_counts = Counter(r["contexto_final"] for r in sheet2_rows)
print(f"\nDistribuição por contexto (sheet2):")
for c, n in contexto_counts.most_common():
    print(f"  {c}: {n}")

# --- Salva JSON intermediário ---
out = {
    "sheet1_old": sheet1_rows,
    "sheet2_final": sheet2_rows,
    "tipo_counts": dict(tipo_counts),
    "contexto_counts": dict(contexto_counts),
}
(OUT_DIR / "categorizacao_extraida.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"\n[ok] JSON salvo: {OUT_DIR / 'categorizacao_extraida.json'}")

# Lista de normalizados pra matching depois
print(f"\n[preview] Primeiros 5 títulos (sheet2):")
for r in sheet2_rows[:5]:
    print(f"  '{r['titulo']}' → '{normalize(r['titulo'])}' → tipo={r['tipo_final']}")

# Salva dicionário título_normalizado → tipo_final pra matching
norm_to_tipo = {}
for r in sheet2_rows:
    norm = normalize(r["titulo"])
    if norm:
        norm_to_tipo[norm] = {
            "titulo_original": r["titulo"],
            "contexto": r["contexto_final"],
            "tipo": r["tipo_final"],
            "tags": r["tags_final"],
        }
(OUT_DIR / "norm_to_tipo.json").write_text(
    json.dumps(norm_to_tipo, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"\n[ok] Dicionário normalizado salvo: {OUT_DIR / 'norm_to_tipo.json'}")
print(f"     {len(norm_to_tipo)} entradas únicas")
