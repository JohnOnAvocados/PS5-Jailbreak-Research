from __future__ import annotations

import json
from pathlib import Path

GRAPH = Path("graph/graph.json")
WIKI = Path("wiki")

def page_home(graph: dict) -> str:
    lines = [
        "# PS5 Research Wiki",
        "",
        "## Overview",
        "A structured documentation surface for PS5 hardware, firmware, kernel, hypervisor, and security-model research.",
        "",
        "## Sections",
    ]
    for layer in sorted({n.get("layer", "unknown") for n in graph.get("nodes", [])}):
        lines.append(f"- [{layer.replace('_', ' ').title()}]({layer}.md)")
    lines += ["", "## Graph Stats", "```json", json.dumps(graph.get("stats", {}), indent=2), "```"]
    return "\n".join(lines) + "\n"

def page_layer(layer: str, nodes: list[dict]) -> str:
    lines = [
        f"# {layer.replace('_', ' ').title()}",
        "",
        "## Notes",
    ]
    for n in sorted(nodes, key=lambda x: x["id"]):
        lines.append(f"- {n['title']} (`{n['id']}`)")
    return "\n".join(lines) + "\n"

def run():
    if not GRAPH.exists():
        raise FileNotFoundError("graph/graph.json not found. Run pipeline first.")
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))

    WIKI.mkdir(parents=True, exist_ok=True)
    (WIKI / "sections").mkdir(exist_ok=True)

    (WIKI / "Home.md").write_text(page_home(graph), encoding="utf-8")

    by_layer = {}
    for node in graph.get("nodes", []):
        by_layer.setdefault(node.get("layer", "unknown"), []).append(node)

    for layer, nodes in by_layer.items():
        (WIKI / "sections" / f"{layer}.md").write_text(page_layer(layer, nodes), encoding="utf-8")

if __name__ == "__main__":
    run()
