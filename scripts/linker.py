from __future__ import annotations

import json
from pathlib import Path

from scripts.utils import INTERMEDIATE, jaccard

STRUCTURED = INTERMEDIATE / "structured.json"

def run() -> list[dict]:
    if not STRUCTURED.exists():
        raise FileNotFoundError("Missing intermediate/structured.json. Run extract first.")

    nodes = json.loads(STRUCTURED.read_text(encoding="utf-8"))
    edges = []

    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            if i >= j:
                continue

            edge_types = []
            weight = 0.0

            if a["layer"] == b["layer"]:
                edge_types.append("same_layer")
                weight += 0.35

            shared_concepts = set(a.get("concepts", [])) & set(b.get("concepts", []))
            if shared_concepts:
                edge_types.append("shared_concept")
                weight += min(0.5, 0.12 * len(shared_concepts))

            if set(a.get("wikilinks", [])) & {b["id"], b["title"], b["source_name"].rsplit(".", 1)[0]}:
                edge_types.append("explicit_link")
                weight += 0.4

            if set(a.get("urls", [])) & set(b.get("urls", [])):
                edge_types.append("shared_url")
                weight += 0.2

            if weight >= 0.35:
                edges.append({
                    "from": a["id"],
                    "to": b["id"],
                    "types": edge_types,
                    "weight": round(min(weight, 1.0), 3),
                })

    Path("graph").mkdir(parents=True, exist_ok=True)
    Path("graph/edges.json").write_text(json.dumps(edges, indent=2, ensure_ascii=False), encoding="utf-8")
    return edges

if __name__ == "__main__":
    run()
