from __future__ import annotations

import json
from pathlib import Path

from scripts.utils import (
    INBOX, INTERMEDIATE, normalize_whitespace, strip_html, sha256_text,
    read_text_file, title_from_text, slugify
)

def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except Exception:
        return f"[PDF ingest unavailable: install pypdf] {path.name}"
    try:
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)
    except Exception as exc:
        return f"[PDF read error] {path.name}: {exc}"

def read_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return read_pdf(path)
    if suffix in {".html", ".htm"}:
        return strip_html(read_text_file(path))
    return read_text_file(path)

def ingest_file(path: Path) -> dict:
    raw = read_file(path)
    return {
        "id": slugify(path.stem),
        "title": title_from_text(raw) if raw.strip() else path.stem,
        "source_path": str(path),
        "source_name": path.name,
        "extension": path.suffix.lower(),
        "content_raw": raw,
        "content_hash": sha256_text(raw),
    }

def run() -> list[dict]:
    records = []
    if not INBOX.exists():
        INBOX.mkdir(parents=True, exist_ok=True)

    for file in sorted(INBOX.rglob("*")):
        if file.is_file():
            records.append(ingest_file(file))

    INTERMEDIATE.mkdir(parents=True, exist_ok=True)
    (INTERMEDIATE / "raw.json").write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    return records

if __name__ == "__main__":
    run()
