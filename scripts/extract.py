from __future__ import annotations

import json
from pathlib import Path

from scripts.utils import INTERMEDIATE, classify_layer, first_sentences, top_concepts, extract_urls, extract_wikilinks

CLEAN = INTERMEDIATE / "clean.json"

def extract_record(item: dict) -> dict:
    text = item.get("content_norm", "")
    layer = classify_layer(text)
    concepts = top_concepts(text, limit=15)
    return {
        **item,
        "layer": layer,
        "summary": first_sentences(text, 3),
        "concepts": concepts,
        "urls": extract_urls(text),
        "wikilinks": extract_wikilinks(text),
        "tags": sorted(set([layer] + concepts[:8])),
    }

def run() -> list[dict]:
    if not CLEAN.exists():
        raise FileNotFoundError("Missing intermediate/clean.json. Run normalize first.")

    data = json.loads(CLEAN.read_text(encoding="utf-8"))
    structured = [extract_record(item) for item in data]
    (INTERMEDIATE / "structured.json").write_text(json.dumps(structured, indent=2, ensure_ascii=False), encoding="utf-8")
    return structured

if __name__ == "__main__":
    run()
