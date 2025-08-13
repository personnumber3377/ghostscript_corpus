import os
import requests
from urllib.parse import quote
import random

# ==== CONFIG ====
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # set your token in env
SEARCH_QUERY = 'extension:ps size:<200000'  # tweak for size limits
OUTPUT_DIR = "ps_corpus"
MAX_PAGES = 10  # number of search pages to fetch (100 files per page)
# ===============

if not GITHUB_TOKEN:
    raise RuntimeError("Please set GITHUB_TOKEN environment variable with a GitHub personal access token")

os.makedirs(OUTPUT_DIR, exist_ok=True)
session = requests.Session()
session.headers.update({
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
})

def is_git_annex(content: bytes) -> bool:
    """Detect git-annex pointer files."""
    first_line = content.split(b"\n", 1)[0]
    return b".git/annex" in first_line or b"SHA256E-" in first_line

def download_file(item):
    raw_url = item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    print(f"[+] Downloading {raw_url}")
    r = session.get(raw_url)
    r.raise_for_status()
    data = r.content

    if is_git_annex(data):
        print("    [-] Skipped git-annex pointer file.")
        return

    filename = f"{item['repository']['full_name'].replace('/', '_')}__{item['name']}"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(data)
    print(f"    [✓] Saved {filepath} ({len(data)} bytes)")

for page in range(1, MAX_PAGES + 1):
    actual_page = random.randrange(1, MAX_PAGES)
    search_url = f"https://api.github.com/search/code?q={quote(SEARCH_QUERY)}&page={actual_page}&per_page=100"
    print(f"[PAGE {page}] {search_url}")
    r = session.get(search_url)
    r.raise_for_status()
    items = r.json().get("items", [])
    if not items:
        break

    for item in items:
        try:
            download_file(item)
        except Exception as e:
            print(f"    [!] Error: {e}")
