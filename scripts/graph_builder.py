from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from scripts.utils import INTERMEDIATE

STRUCTURED = INTERMEDIATE / "structured.json"
EDGES = Path("graph/edges.json")

def connected_components(nodes, edges):
    adj = defaultdict(set)
    for n in nodes:
        adj[n["id"]]  # ensure key
    for e in edges:
        adj[e["from"]].add(e["to"])
        adj[e["to"]].add(e["from"])

    seen = set()
    comps = []

    for n in adj:
        if n in seen:
            continue
        stack = [n]
        comp = []
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            comp.append(cur)
            stack.extend(adj[cur] - seen)
        comps.append(comp)
    return comps

def run() -> dict:
    if not STRUCTURED.exists():
        raise FileNotFoundError("Missing intermediate/structured.json. Run extract first.")
    if not EDGES.exists():
        raise FileNotFoundError("Missing graph/edges.json. Run linker first.")

    nodes = json.loads(STRUCTURED.read_text(encoding="utf-8"))
    edges = json.loads(EDGES.read_text(encoding="utf-8"))

    node_index = {n["id"]: n for n in nodes}
    degree = Counter()
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1

    for n in nodes:
        n["degree"] = degree[n["id"]]

    layers = Counter(n.get("layer", "unknown") for n in nodes)
    components = connected_components(nodes, edges)
    graph = {
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "layer_counts": dict(layers),
            "components": len(components),
            "largest_component": max((len(c) for c in components), default=0),
            "top_hubs": sorted(
                [{"id": n["id"], "degree": n["degree"], "layer": n["layer"]} for n in nodes],
                key=lambda x: (-x["degree"], x["id"])
            )[:15],
        }
    }

    Path("graph").mkdir(parents=True, exist_ok=True)
    Path("graph/graph.json").write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    Path("graph/nodes.json").write_text(json.dumps(nodes, indent=2, ensure_ascii=False), encoding="utf-8")
    Path("graph/summary.json").write_text(json.dumps(graph["stats"], indent=2, ensure_ascii=False), encoding="utf-8")
    return graph

if __name__ == "__main__":
    run()
