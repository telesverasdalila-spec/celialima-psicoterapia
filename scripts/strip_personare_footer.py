#!/usr/bin/env python3
"""
Remove o rodapé do Personare do fim de cada artigo em articles.json.

Padrão do rodapé (sempre no final do HTML):
  <p>Celia Lima</p>
  <p>Psicoterapeuta holística com abordagem junguiana ... saúde física e emocional.</p>
  <ul><li>Contato:celiacalima@gmail.com</li></ul>

Estratégia:
- Faz parse do HTML com BeautifulSoup.
- Encontra o <p> que contém exatamente "Celia Lima" (texto puro).
- A partir dele, remove todos os elementos seguintes (irmãos) — cobre <p> da bio e <ul> do contato.
- Também remove o próprio <p>Celia Lima</p>.
- Se não encontrar "Celia Lima" exato, tenta fallback por regex no HTML cru.
- Faz backup do articles.json antes de sobrescrever.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

ARTICLES_JSON = Path("/home/z/my-project/src/data/articles.json")
BACKUP = ARTICLES_JSON.with_suffix(
    f'.backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
)


def strip_footer_from_html(html: str) -> tuple[str, bool]:
    """Remove o rodapé do Personare. Retorna (novo_html, modificado)."""
    soup = BeautifulSoup(html, "html.parser")

    # Procura o <p> cujo texto é exatamente "Celia Lima"
    target_p = None
    for p in soup.find_all('p'):
        if p.get_text(strip=True) == 'Celia Lima':
            target_p = p
            break

    if target_p is None:
        # Fallback: procura <p> que começa com "Celia Lima" (às vezes vem com espaços)
        for p in soup.find_all('p'):
            t = p.get_text(strip=True)
            if t.startswith('Celia Lima') and len(t) < 30:
                target_p = p
                break

    if target_p is None:
        return html, False

    # Remove todos os irmãos seguintes do target_p
    removed = 1
    nxt = target_p.next_sibling
    while nxt is not None:
        to_remove = nxt
        nxt = nxt.next_sibling
        to_remove.extract()
        removed += 1

    # Remove o próprio <p>Celia Lima</p>
    target_p.extract()

    new_html = str(soup)
    return new_html, True


def main():
    if not ARTICLES_JSON.exists():
        print(f"[erro] {ARTICLES_JSON} não encontrado")
        return 1

    # Backup
    shutil.copy2(ARTICLES_JSON, BACKUP)
    print(f"[backup] {BACKUP}")

    articles = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    print(f"[info] {len(articles)} artigos carregados")

    total_modified = 0
    failed = []
    for art in articles:
        html = art.get('html', '')
        if not html:
            continue
        new_html, modified = strip_footer_from_html(html)
        if modified:
            art['html'] = new_html
            total_modified += 1
            # Atualiza wordCount se existir
            if 'wordCount' in art:
                # Recalcula contagem de palavras a partir do novo HTML
                soup = BeautifulSoup(new_html, "html.parser")
                text = soup.get_text(separator=' ', strip=True)
                art['wordCount'] = len(text.split())

    print(f"[ok] {total_modified} artigos tiveram o rodapé removido")

    if failed:
        print(f"[warn] {len(failed)} artigos não tiveram rodapé encontrado:")
        for f in failed[:5]:
            print(f"  - {f}")

    # Salva
    ARTICLES_JSON.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"[ok] articles.json salvo ({ARTICLES_JSON.stat().st_size / 1024:.1f} KB)")

    # Verificação: varre tudo pra ver se sobrou algum rodapé
    remaining = 0
    for art in articles:
        html = art.get('html', '')
        if 'Psicoterapeuta holística' in html or 'celiacalima@gmail.com' in html:
            remaining += 1
            print(f"  [still has footer] {art.get('slug')}")
    if remaining == 0:
        print(f"[verificado] Nenhum artigo restante com o rodapé do Personare.")
    else:
        print(f"[verificado] {remaining} artigos ainda contêm o rodapé.")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
