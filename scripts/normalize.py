from __future__ import annotations

import json
from pathlib import Path

from scripts.utils import INTERMEDIATE, normalize_whitespace

RAW = INTERMEDIATE / "raw.json"

def normalize_record(item: dict) -> dict:
    content = normalize_whitespace(item.get("content_raw", ""))
    return {
        **item,
        "content_norm": content,
        "word_count": len(content.split()),
    }

def run() -> list[dict]:
    if not RAW.exists():
        raise FileNotFoundError("Missing intermediate/raw.json. Run ingest first.")

    data = json.loads(RAW.read_text(encoding="utf-8"))
    cleaned = [normalize_record(item) for item in data]
    (INTERMEDIATE / "clean.json").write_text(json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8")
    return cleaned

if __name__ == "__main__":
    run()
