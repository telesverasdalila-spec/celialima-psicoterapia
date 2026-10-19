#!/usr/bin/env python3
"""
Faz commit de todos os arquivos modificados hoje no GitHub da Célia
usando Git Data API (1 commit com todos os arquivos).
"""

import base64
import json
import sys
import requests
from pathlib import Path

# --- Config ------------------------------------------------------------------
TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""
REPO_OWNER = "telesverasdalila-spec"
REPO_NAME = "celialima-psicoterapia"
BRANCH = "main"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# --- Lista de arquivos para enviar -------------------------------------------
# Gerada automaticamente: varre src/, public/, scripts/ e adiciona tudo
# (exceto arquivos .local-backup, .cache, node_modules)
# Isso garante que qualquer arquivo novo/alterado suba junto.
import fnmatch

IGNORE_PATTERNS = [
    "*.local-backup",
    "*.bak",
    ".DS_Store",
    "node_modules/**",
    ".next/**",
    "*.log",
]

BASE_DIR = Path("/home/z/my-project")

def should_ignore(path: Path) -> bool:
    rel = str(path.relative_to(BASE_DIR))
    for pat in IGNORE_PATTERNS:
        if fnmatch.fnmatch(rel, pat):
            return True
    return False

def collect_files():
    files = []
    # Diretórios que devem subir para o GitHub
    scan_dirs = [BASE_DIR / "src", BASE_DIR / "public", BASE_DIR / "scripts"]
    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue
        for path in scan_dir.rglob("*"):
            if not path.is_file():
                continue
            if should_ignore(path):
                continue
            # Tamanho máximo do GitHub: 100 MB (vamos limitar a 25 MB pra segurança)
            if path.stat().st_size > 25 * 1024 * 1024:
                print(f"  [skip] Arquivo grande demais: {path}")
                continue
            rel = path.relative_to(BASE_DIR).as_posix()
            is_binary = path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico", ".pdf"}
            files.append((rel, rel, is_binary))
    return files

FILES_TO_PUSH = collect_files()

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

    print(f"[1] Autenticando no repositório {REPO_OWNER}/{REPO_NAME}...")
    # Confirma que o token funciona
    repo_info = requests.get(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}",
        headers=HEADERS,
    ).json()
    if "message" in repo_info and "Bad credentials" in repo_info["message"]:
        print(f"  ❌ Token inválido: {repo_info['message']}")
        sys.exit(1)
    print(f"  ✓ Acesso confirmado. Repo: {repo_info.get('full_name', '?')}")

    # Pega SHA do commit atual da branch main
    print(f"\n[2] Pegando commit atual da branch '{BRANCH}'...")
    ref = api_call("get", f"git/refs/heads/{BRANCH}")
    if not ref:
        sys.exit(1)
    current_commit_sha = ref["object"]["sha"]
    print(f"  ✓ Commit atual: {current_commit_sha[:8]}")

    # Pega a tree do commit atual
    print(f"\n[3] Pegando tree do commit atual...")
    commit_obj = api_call("get", f"git/commits/{current_commit_sha}")
    if not commit_obj:
        sys.exit(1)
    current_tree_sha = commit_obj["tree"]["sha"]
    print(f"  ✓ Tree atual: {current_tree_sha[:8]}")

    # Cria blobs pra cada arquivo
    print(f"\n[4] Criando blobs para {len(FILES_TO_PUSH)} arquivos...")
    tree_items = []
    for repo_path, local_path, is_binary in FILES_TO_PUSH:
        full_local = BASE_DIR / local_path
        if not full_local.exists():
            print(f"  ⚠ Arquivo não encontrado, pulando: {local_path}")
            continue

        if is_binary:
            content_bytes = full_local.read_bytes()
            content_b64 = base64.b64encode(content_bytes).decode("utf-8")
            encoding = "base64"
        else:
            content_text = full_local.read_text(encoding="utf-8")
            content_b64 = base64.b64encode(content_text.encode("utf-8")).decode("utf-8")
            encoding = "base64"

        # Cria blob
        blob = api_call("post", "git/blobs", {
            "content": content_b64,
            "encoding": encoding,
        })
        if not blob:
            sys.exit(1)
        tree_items.append({
            "path": repo_path,
            "mode": "100644",
            "type": "blob",
            "sha": blob["sha"],
        })
        print(f"  ✓ {repo_path} ({len(content_b64)} chars)")

    # Cria nova tree com os arquivos
    print(f"\n[5] Criando nova tree com {len(tree_items)} arquivos...")
    new_tree = api_call("post", "git/trees", {
        "base_tree": current_tree_sha,
        "tree": tree_items,
    })
    if not new_tree:
        sys.exit(1)
    new_tree_sha = new_tree["sha"]
    print(f"  ✓ Nova tree: {new_tree_sha[:8]}")

    # Cria novo commit
    print(f"\n[6] Criando commit...")
    commit_message = """Refinamentos da Célia: card Tom Zé + primeira pessoa + foto nova

Mudanças aplicadas:
- Card epígrafe com citação do Tom Zé na home (primeira posição, sem moldura)
- SVGs dos 7 contextos com cores mais saturadas (2 tons acima)
- Cards da home com altura igual + imagem alternando lado (espelhamento)
- Menu 'Saúde Mental' → 'Publicações' (header e footer)
- Página Publicações com texto da Célia (primeira pessoa, 30 anos de experiência)
- Página Atendimento com texto da Célia em primeira pessoa (sem psicodrama)
- Página Sobre em primeira pessoa (sem psicodrama, com 'Símbolos e sonhos')
- Foto nova na página Sobre (circular com fundo transparente)
- Keywords do site: removido 'psicodrama', adicionado 'junguiana' e 'psicosíntese'
"""
    new_commit = api_call("post", "git/commits", {
        "message": commit_message,
        "tree": new_tree_sha,
        "parents": [current_commit_sha],
    })
    if not new_commit:
        sys.exit(1)
    new_commit_sha = new_commit["sha"]
    print(f"  ✓ Novo commit: {new_commit_sha[:8]}")
    print(f"  ✓ URL: {new_commit.get('html_url', '?')}")

    # Atualiza a ref main
    print(f"\n[7] Atualizando branch '{BRANCH}'...")
    updated_ref = api_call("patch", f"git/refs/heads/{BRANCH}", {
        "sha": new_commit_sha,
    })
    if not updated_ref:
        sys.exit(1)
    print(f"  ✓ Branch atualizada para {new_commit_sha[:8]}")

    print(f"\n[8] ✅ Push completo!")
    print(f"   Commit: {new_commit_sha}")
    print(f"   {len(tree_items)} arquivos enviados")
    print(f"   Vercel vai detectar e deployar em 30-60 segundos")
    print(f"   URL do commit: {new_commit.get('html_url', '?')}")


if __name__ == "__main__":
    main()
