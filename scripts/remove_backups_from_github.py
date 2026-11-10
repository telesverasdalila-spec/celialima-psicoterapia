#!/usr/bin/env python3
"""
Remove arquivos de backup do GitHub (eles não precisam ficar no repo).
"""
import sys
import requests
from pathlib import Path

TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""
REPO_OWNER = "telesverasdalila-spec"
REPO_NAME = "celialima-psicoterapia"
BRANCH = "main"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Arquivos para REMOVER do GitHub (mantém no local, mas tira do repo)
FILES_TO_REMOVE = [
    "src/data/articles.backup-categorizacao-20261019-193119.json",
    "src/data/articles.backup-20261019-152554.json",
]

def api_call(method, endpoint, json_data=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/{endpoint}"
    r = requests.request(method, url, headers=HEADERS, json=json_data)
    if r.status_code >= 400:
        print(f"  ❌ ERRO {r.status_code} em {endpoint}: {r.text[:300]}")
        return None
    return r.json()

def main():
    if not TOKEN:
        print("Erro: passe o token como argumento")
        sys.exit(1)

    print(f"[1] Pegando commit atual da branch '{BRANCH}'...")
    ref = api_call("get", f"git/refs/heads/{BRANCH}")
    if not ref:
        sys.exit(1)
    parent_sha = ref["object"]["sha"]
    print(f"  ✓ Commit atual: {parent_sha}")

    print(f"\n[2] Pegando tree atual...")
    commit_obj = api_call("get", f"git/commits/{parent_sha}")
    tree_sha = commit_obj["tree"]["sha"]
    print(f"  ✓ Tree atual: {tree_sha}")

    print(f"\n[3] Listando todos os arquivos da tree...")
    # Recursive list
    tree_data = api_call("get", f"git/trees/{tree_sha}?recursive=1")
    all_files = {item["path"]: item["sha"] for item in tree_data["tree"] if item["type"] == "blob"}
    print(f"  ✓ {len(all_files)} arquivos na tree")

    # Novos blobs: precisamos criar um novo blob só pra arquivos que MANTEREMOS
    # que não estão na lista de remoção
    print(f"\n[4] Reconstruindo tree SEM os {len(FILES_TO_REMOVE)} arquivos de backup...")
    # Constrói tree_entries a partir dos arquivos existentes (menos os removidos)
    tree_entries = []
    for path, sha in all_files.items():
        if path in FILES_TO_REMOVE:
            print(f"  [skip] {path}")
            continue
        tree_entries.append({
            "path": path,
            "mode": "100644",
            "type": "blob",
            "sha": sha,
        })
    print(f"  ✓ {len(tree_entries)} arquivos mantidos")

    print(f"\n[5] Criando nova tree...")
    new_tree = api_call("post", "git/trees", json_data={"tree": tree_entries})
    if not new_tree:
        sys.exit(1)
    new_tree_sha = new_tree["sha"]
    print(f"  ✓ Nova tree: {new_tree_sha}")

    print(f"\n[6] Criando commit...")
    new_commit = api_call("post", "git/commits", json_data={
        "message": "remove backup files from repo (kept locally)",
        "tree": new_tree_sha,
        "parents": [parent_sha],
    })
    print(f"  ✓ Novo commit: {new_commit['sha'][:8]}")
    print(f"  URL: https://github.com/{REPO_OWNER}/{REPO_NAME}/commit/{new_commit['sha']}")

    print(f"\n[7] Atualizando branch '{BRANCH}'...")
    api_call("patch", f"git/refs/heads/{BRANCH}", json_data={"sha": new_commit["sha"]})
    print(f"  ✓ Branch atualizada")

    print(f"\n[8] ✅ Limpeza completa!")
    print(f"   Backups removidos do GitHub (mas ainda estão no seu computador local)")

if __name__ == "__main__":
    main()
