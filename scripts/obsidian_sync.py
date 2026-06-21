from __future__ import annotations

import json
from pathlib import Path

GRAPH = Path("graph/graph.json")
VAULT = Path("obsidian/vault")

def _frontmatter(title: str, tags: list[str]) -> str:
    return "---\n" + f"title: {title}\ntags: [{', '.join(tags)}]\n" + "---\n\n"

def render_home(graph: dict) -> str:
    layers = {}
    for n in graph.get("nodes", []):
        layers.setdefault(n.get("layer", "unknown"), []).append(n["id"])

    lines = ["# PS5 Research Vault", "", "## Layer Maps"]
    for layer, ids in sorted(layers.items()):
        lines.append(f"- [[maps/{layer}]] ({len(ids)} notes)")
    lines += ["", "## Top Hubs"]
    for item in graph.get("stats", {}).get("top_hubs", [])[:10]:
        lines.append(f"- [[nodes/{item['id']}]] · degree {item['degree']}")
    return "\n".join(lines) + "\n"

def render_layer(layer: str, nodes: list[dict]) -> str:
    lines = [f"# {layer.replace('_', ' ').title()}", "", "## Notes"]
    for n in sorted(nodes, key=lambda x: x["id"]):
        lines.append(f"- [[nodes/{n['id']}]]")
    return "\n".join(lines) + "\n"

def render_node(node: dict, graph: dict) -> str:
    related = []
    for e in graph.get("edges", []):
        if e["from"] == node["id"]:
            related.append(e["to"])
        elif e["to"] == node["id"]:
            related.append(e["from"])
    related = sorted(set(related))
    lines = [
        f"# {node['title']}",
        "",
        "## Source",
        node.get("source_path", ""),
        "",
        "## System Layer",
        node.get("layer", "unknown"),
        "",
        "## Summary",
        node.get("summary", ""),
        "",
        "## Concepts",
        ", ".join(node.get("concepts", [])),
        "",
        "## Related Notes",
    ]
    for rid in related[:20]:
        lines.append(f"- [[../nodes/{rid}]]")
    lines.append("")
    return "\n".join(lines)

def run():
    if not GRAPH.exists():
        raise FileNotFoundError("graph/graph.json not found. Run pipeline first.")
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))

    (VAULT / "maps").mkdir(parents=True, exist_ok=True)
    (VAULT / "nodes").mkdir(parents=True, exist_ok=True)
    (VAULT / "concepts").mkdir(parents=True, exist_ok=True)

    (VAULT / "00_Home.md").write_text(render_home(graph), encoding="utf-8")

    by_layer = {}
    for node in graph.get("nodes", []):
        by_layer.setdefault(node.get("layer", "unknown"), []).append(node)

    for layer, nodes in by_layer.items():
        (VAULT / "maps" / f"{layer}.md").write_text(render_layer(layer, nodes), encoding="utf-8")

    for node in graph.get("nodes", []):
        (VAULT / "nodes" / f"{node['id']}.md").write_text(render_node(node, graph), encoding="utf-8")

if __name__ == "__main__":
    run()
