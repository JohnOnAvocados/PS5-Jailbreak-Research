import os
import re
import json
from collections import defaultdict

VAULT_ROOT = "."
IGNORE_DIRS = {"node_modules", ".git", "venv", "__pycache__"}
OUTPUT_DIR = "obsidian/links"

def extract_terms(text):
    words = re.findall(r"[a-zA-Z]{5,}", text.lower())
    return words

def scan_markdown_files():
    files = []
    for root, dirs, filenames in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in filenames:
            if f.endswith(".md"):
                files.append(os.path.join(root, f))
    return files

def build_index(files):
    index = defaultdict(set)
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
        terms = extract_terms(text)
        for t in terms:
            index[t].add(file)
    return index

def generate_links(index):
    links = {}
    for term, files in index.items():
        if len(files) > 1:
            links[term] = list(files)
    return links

def get_links_for_file(filepath, links):
    file_links = {}
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().lower()
    for term, linked_files in links.items():
        if term in content:
            file_links[term] = [os.path.relpath(p, start=OUTPUT_DIR) for p in linked_files]
    return file_links

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = scan_markdown_files()
    index = build_index(files)
    links = generate_links(index)
    total_links = 0
    for file in files:
        file_links = get_links_for_file(file, links)
        if file_links:
            total_links += len(file_links)
            rel_name = os.path.relpath(file, start=VAULT_ROOT).replace("\\", "_").replace("/", "_") + ".json"
            out_path = os.path.join(OUTPUT_DIR, rel_name)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(file_links, f, indent=2)
    print(f"Wrote link maps for {len(files)} files ({total_links} total links) to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
