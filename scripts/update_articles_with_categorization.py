#!/usr/bin/env python3
"""
Atualiza articles.json com a categorização manual da Célia.

Lê:
  - /home/z/my-project/upload/RElação de ARtigos e Categorização.xlsx (manual)
  - /home/z/my-project/src/data/articles.json (atual)

Cruza por título (normalizado) e atualiza:
  - contentType: 'artigo' (Reflexiva) | 'pratica' (Prática)
  - contextos: novos 10 contextos
  - tags: tags sugeridas pela Célia (separadas por vírgula)
  - contextLabel

Escreve:
  - /home/z/my-project/src/data/articles.json (atualizado)
  - /home/z/my-project/download/categorizacao-cruzamento.xlsx (auditoria)
"""

import json
import re
import pickle
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# --- Paths -------------------------------------------------------------------
EXCEL_MANUAL = Path("/home/z/my-project/upload/Categorização dos Artigos.xlsx")
JSON_PATH = Path("/home/z/my-project/src/data/articles.json")
OUT_AUDIT = Path("/home/z/my-project/download/categorizacao-cruzamento.xlsx")

# --- 7 contextos consolidados (v2) -------------------------------------------
NEW_CONTEXTS = {
    "Dinâmica Familiar e Criação de Filhos": {
        "slug": "dinamica-familiar",
        "label": "Dinâmica Familiar e Criação de Filhos",
        "description": "Mães, pais, filhos, sogras, avós. A família como primeiro espelho e território de aprendizado.",
    },
    "Relacionamentos Amorosos e Sexualidade": {
        "slug": "relacionamentos-sexualidade",
        "label": "Relacionamentos Amorosos e Sexualidade",
        "description": "Amor, parceria, sexo, escolhas, separação. Tudo que envolve escolher e ser escolhido por outro.",
    },
    "Ansiedade, Estresse e Esgotamento": {
        "slug": "ansiedade-estresse",
        "label": "Ansiedade, Estresse e Esgotamento",
        "description": "Quando o corpo pede calma e a cabeça não consegue parar. Cansaço, exaustão, dificuldade de relaxar.",
    },
    "Autocrítica, Limites e Autoestima": {
        "slug": "autocritica-limites",
        "label": "Autocrítica, Limites e Autoestima",
        "description": "Aprender a dizer não, reconhecer o próprio valor, calar o juiz interior, cuidar de si sem culpa.",
    },
    "Sintomas Psicossomáticos e Saúde Emocional": {
        "slug": "sintomas-psicossomaticos-saude-emocional",
        "label": "Sintomas Psicossomáticos e Saúde Emocional",
        "description": "Emoção e corpo: como o que sentimos vira sintoma, doença como mensagem, terapias integrativas.",
    },
    "Produtividade, Carreira e Organização": {
        "slug": "produtividade-carreira",
        "label": "Produtividade, Carreira e Organização",
        "description": "Vocação, propósito, dinheiro como energia, trabalho como construção de sentido.",
    },
    "Espiritualidade e Autoconhecimento": {
        "slug": "espiritualidade-autoconhecimento",
        "label": "Espiritualidade e Autoconhecimento",
        "description": "Espiritualidade no cotidiano, meditação, exercícios de proteção, autoavaliação, paz interior.",
    },
}


def normalize_title(t: str) -> str:
    """Normaliza pra match: minúsculas, sem pontuação lateral, sem aspas, sem #."""
    t = t.lower().strip()
    t = re.sub(r'["\']', '', t)  # remove aspas em qualquer posição
    t = re.sub(r'^#+', '', t)  # hashtag no início
    t = re.sub(r'[:\?]+$', '', t)  # : ou ? no fim
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


# Mapeamento manual para artigos que ficaram de fora da planilha da Célia
MANUAL_FIXES = {
    "o que é masturbação: entenda da puberdade à maturidade": {
        "contexto": "Sintomas Psicossomáticos e Saúde Emocional",
        "tipo": "Reflexiva",
        "tags": "Sexualidade, Puberdade, Masturbação, Tabu Sexual",
    },
}


def main():
    # Carrega categorização manual
    from openpyxl import load_workbook
    wb = load_workbook(EXCEL_MANUAL)
    # Procura o sheet com mais colunas preenchidas
    ws = wb["Lista de Artigos Categorizados"]
    manual = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        titulo = str(row[0]).strip()
        contexto = str(row[1]).strip() if row[1] else ""
        tipo = str(row[2]).strip() if row[2] else ""
        tags = str(row[3]).strip() if row[3] else ""
        categoria_livro = str(row[4]).strip() if len(row) > 4 and row[4] else ""
        manual[normalize_title(titulo)] = {
            "titulo_original": titulo,
            "contexto": contexto,
            "tipo": tipo,
            "tags": tags,
            "categoria_livro": categoria_livro,
        }
    print(f"[1] Manual: {len(manual)} artigos catalogados")

    # Carrega JSON atual
    articles = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    print(f"[2] JSON atual: {len(articles)} artigos")

    # Atualiza cada artigo
    matched = 0
    unmatched = []
    for a in articles:
        key = normalize_title(a["title"])
        m = manual.get(key) or MANUAL_FIXES.get(key)
        if m:
            a["contentType"] = "pratica" if m["tipo"].lower().startswith("prát") else "artigo"
            # Contexto novo (slug + label)
            ctx = m["contexto"]
            if ctx in NEW_CONTEXTS:
                ctx_data = NEW_CONTEXTS[ctx]
                a["contexts"] = [ctx_data["slug"]]
                a["contextLabels"] = [ctx_data["label"]]
                a["contextDescription"] = ctx_data["description"]
            else:
                # Contexto não mapeado — mantém genérico
                a["contexts"] = ["outros"]
                a["contextLabels"] = [ctx or "Outros"]
                a["contextDescription"] = "Outros temas."
            # Tags (split por vírgula)
            tag_list = [t.strip() for t in re.split(r'[,;]', m["tags"]) if t.strip()]
            a["tags"] = tag_list
            # Mantém keywords antigas em campo separado (por compatibilidade)
            a["keywords"] = a.get("keywords", []) + tag_list
            # dedupe keywords
            seen = set()
            a["keywords"] = [x for x in a["keywords"] if not (x in seen or seen.add(x))]
            a["contextOriginal"] = m["contexto"]
            a["tipoOriginal"] = m["tipo"]
            matched += 1
        else:
            unmatched.append(a["title"])

    print(f"[3] Match: {matched}/{len(articles)} artigos atualizados")
    if unmatched:
        print(f"    ⚠ {len(unmatched)} artigos sem match:")
        for t in unmatched[:5]:
            print(f"      - {t}")

    # Salva JSON atualizado
    JSON_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[4] JSON atualizado: {JSON_PATH}")

    # Estatística final
    from collections import defaultdict
    by_ctx = defaultdict(int)
    by_type = defaultdict(int)
    for a in articles:
        for c in a["contexts"]:
            by_ctx[c] += 1
        by_type[a["contentType"]] += 1
    print("\nDistribuição por tipo:")
    for t, n in sorted(by_type.items()):
        print(f"  {t}: {n}")
    print("\nDistribuição por contexto (slug):")
    for c, n in sorted(by_ctx.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")

    # Gera planilha de auditoria
    wb_out = Workbook()
    ws_out = wb_out.active
    ws_out.title = "Cruzamento"
    ws_out.append(["Título no site", "Título na planilha", "Tipo (novo)", "Contexto (novo)", "Tags (novas)", "Match OK?"])
    header_fill = PatternFill("solid", fgColor="a05a3c")
    header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    thin = Side(border_style="thin", color="d9d4c5")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for col in range(1, 7):
        cell = ws_out.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="left", vertical="center")
    ws_out.row_dimensions[1].height = 28

    for a in articles:
        key = normalize_title(a["title"])
        m = manual.get(key, {})
        match_ok = "SIM" if m else "NÃO"
        ws_out.append([
            a["title"],
            m.get("titulo_original", ""),
            a["contentType"],
            a.get("contextOriginal", ""),
            ", ".join(a.get("tags", [])),
            match_ok,
        ])
        row_idx = ws_out.max_row
        for col in range(1, 7):
            cell = ws_out.cell(row=row_idx, column=col)
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if match_ok == "NÃO":
                cell.fill = PatternFill("solid", fgColor="fff4e6")
    ws_out.column_dimensions["A"].width = 55
    ws_out.column_dimensions["B"].width = 55
    ws_out.column_dimensions["C"].width = 14
    ws_out.column_dimensions["D"].width = 35
    ws_out.column_dimensions["E"].width = 45
    ws_out.column_dimensions["F"].width = 12
    ws_out.freeze_panes = "A2"
    ws_out.auto_filter.ref = ws_out.dimensions
    wb_out.save(OUT_AUDIT)
    print(f"\n[5] Auditoria: {OUT_AUDIT}")


if __name__ == "__main__":
    main()
