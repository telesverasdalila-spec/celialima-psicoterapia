#!/usr/bin/env python3
"""
Cruza a classificação do Excel (sheet2 "Nova Categorias acrescentadas")
com o articles.json atual. Identifica:
- quais artigos mudaram de Tipo (de artigo/pratica → Reflexiva/Prática)
- quais mudaram de Contexto
- quais mudaram de Tags
- quais não foram encontrados (problema de matching de título)

No fim, atualiza o articles.json com a classificação correta.
"""

import json
import unicodedata
import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ARTICLES_JSON = Path("/home/z/my-project/src/data/articles.json")
NORM_TO_TIPO = Path("/home/z/my-project/download/norm_to_tipo.json")
OUT_DIR = Path("/home/z/my-project/download")

# Mapeia os contextos do Excel (label amigável) → slugs do site
# Ordem alfabética dos labels do Excel, baseada em src/lib/articles.ts
LABEL_TO_SLUG = {
    "Dinâmica Familiar e Criação de Filhos": "dinamica-familiar",
    "Relacionamentos Amorosos e Sexualidade": "relacionamentos-sexualidade",
    "Autocrítica, Limites e Autoestima": "autocritica-limites",
    "Ansiedade, Estresse e Esgotamento": "ansiedade-estresse",
    "Espiritualidade e Autoconhecimento": "espiritualidade-autoconhecimento",
    "Sintomas Psicossomáticos e Saúde Emocional": "sintomas-psicossomaticos-saude-emocional",
    "Produtividade, Carreira e Organização": "produtividade-carreira",
}

# Mapeia Tipo do Excel → contentType do articles.json
TIPO_TO_CONTENTTYPE = {
    "Reflexiva": "artigo",
    "Prática": "pratica",
}

def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFD", str(s))
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def load_articles():
    return json.loads(ARTICLES_JSON.read_text(encoding="utf-8"))

def load_norm_to_tipo():
    return json.loads(NORM_TO_TIPO.read_text(encoding="utf-8"))

def main():
    articles = load_articles()
    norm_to_tipo = load_norm_to_tipo()
    print(f"[info] articles.json: {len(articles)} artigos")
    print(f"[info] Excel sheet2: {len(norm_to_tipo)} entradas únicas")

    # Backup
    backup_path = ARTICLES_JSON.with_suffix(
        f'.backup-categorizacao-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
    )
    shutil.copy2(ARTICLES_JSON, backup_path)
    print(f"[backup] {backup_path}")

    # Para cada artigo no articles.json, encontra correspondente no Excel
    not_found = []
    matched = []
    changes_log = []

    for art in articles:
        title = art.get("title", "")
        norm = normalize(title)

        # Busca match exato
        match = norm_to_tipo.get(norm)

        # Se não encontrou, tenta busca parcial (primeiros 30 chars)
        if not match:
            for k, v in norm_to_tipo.items():
                if norm and k and (norm in k or k in norm) and min(len(norm), len(k)) > 10:
                    match = v
                    break

        if not match:
            not_found.append({"slug": art.get("slug"), "title": title, "norm": norm})
            continue

        matched.append({
            "slug": art.get("slug"),
            "title": title,
            "excel_title": match["titulo_original"],
            "old_contentType": art.get("contentType"),
            "new_contentType": TIPO_TO_CONTENTTYPE.get(match["tipo"]),
            "tipo_excel": match["tipo"],
            "old_contexts": art.get("contexts", []),
            "old_contextLabels": art.get("contextLabels", []),
            "new_context_label": match["contexto"],
            "new_context_slug": LABEL_TO_SLUG.get(match["contexto"]),
            "old_tags": art.get("tags", []),
            "new_tags_csv": match["tags"],
            "old_keywords": art.get("keywords", []),
        })

    print(f"\n[match] {len(matched)}/{len(articles)} artigos encontrados no Excel")
    print(f"[not found] {len(not_found)} não encontrados:")
    for nf in not_found[:10]:
        print(f"  - {nf['title']!r} (norm={nf['norm']!r})")
    if len(not_found) > 10:
        print(f"  ... e mais {len(not_found) - 10}")

    # Verifica diferenças
    changes = {
        "contentType_changed": 0,
        "context_changed": 0,
        "tags_changed": 0,
        "no_change": 0,
    }
    for m in matched:
        ct_changed = m["old_contentType"] != m["new_contentType"]
        # Context: compara old_contexts (lista) com [new_context_slug] (novo)
        # Obs: alguns artigos tinham 2 contextos no site antigo. Excel tem só 1.
        # Mantemos os 2 contextos se já existiam, mas adicionamos o novo do Excel
        # se for diferente.
        old_ctx_set = set(m["old_contexts"])
        new_ctx_set = {m["new_context_slug"]} if m["new_context_slug"] else set()
        ctx_changed = old_ctx_set != new_ctx_set

        # Tags: compara old_tags com new_tags (split por vírgula)
        new_tags_list = [t.strip() for t in (m["new_tags_csv"] or "").split(",") if t.strip()]
        tags_changed = set(m["old_tags"]) != set(new_tags_list)

        if ct_changed:
            changes["contentType_changed"] += 1
        if ctx_changed:
            changes["context_changed"] += 1
        if tags_changed:
            changes["tags_changed"] += 1
        if not (ct_changed or ctx_changed or tags_changed):
            changes["no_change"] += 1

        changes_log.append({
            **m,
            "ct_changed": ct_changed,
            "ctx_changed": ctx_changed,
            "tags_changed": tags_changed,
            "new_tags_list": new_tags_list,
        })

    print(f"\n[resumo das diferenças]")
    print(f"  contentType mudou: {changes['contentType_changed']}")
    print(f"  context mudou: {changes['context_changed']}")
    print(f"  tags mudaram: {changes['tags_changed']}")
    print(f"  nada mudou: {changes['no_change']}")

    # Lista artigos que mudaram de contentType
    print(f"\n[contentType mudou] (mostrando 15 primeiros):")
    for c in changes_log:
        if c["ct_changed"]:
            print(f"  - {c['title']!r}: {c['old_contentType']} → {c['new_contentType']} (Excel={c['tipo_excel']})")
    if changes["contentType_changed"] > 15:
        print(f"  ... e mais {changes['contentType_changed'] - 15}")

    # Salva relatório completo
    (OUT_DIR / "diff_categorizacao.json").write_text(
        json.dumps({
            "summary": {
                "total_articles": len(articles),
                "matched": len(matched),
                "not_found": len(not_found),
                "not_found_list": not_found,
                "changes": changes,
            },
            "details": changes_log,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\n[ok] Relatório: {OUT_DIR / 'diff_categorizacao.json'}")

if __name__ == "__main__":
    main()
