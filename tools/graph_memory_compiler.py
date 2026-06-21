import os
import re
import json
import sys
from collections import defaultdict

ROOT = "."

GRAPH_OUTPUT = "graph_memory.json"

def extract_links(text):
    return re.findall(r"\[\[(.*?)\]\]", text)

def extract_concepts(text):
    # simple fallback concept extractor
    words = re.findall(r"[a-zA-Z]{6,}", text.lower())
    return list(set(words))

def scan_files():
    nodes = {}

    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()

                nodes[path] = {
                    "links": extract_links(content),
                    "concepts": extract_concepts(content),
                    "size": len(content)
                }

    return nodes

def build_graph(nodes):
    graph = {
        "nodes": {},
        "edges": []
    }

    for path, data in nodes.items():
        graph["nodes"][path] = data

        for link in data["links"]:
            for target in nodes.keys():
                if link.lower() in target.lower():
                    graph["edges"].append({
                        "source": path,
                        "target": target,
                        "type": "explicit_link"
                    })

    return graph

def add_semantic_edges(graph):
    # lightweight heuristic similarity (upgradeable later)
    nodes = list(graph["nodes"].keys())

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a = graph["nodes"][nodes[i]]["concepts"]
            b = graph["nodes"][nodes[j]]["concepts"]

            overlap = len(set(a) & set(b))

            if overlap >= 3:
                graph["edges"].append({
                    "source": nodes[i],
                    "target": nodes[j],
                    "type": "semantic_overlap",
                    "weight": overlap
                })

    return graph

def main():
    nodes = scan_files()
    graph = build_graph(nodes)

    enable_semantic = "--semantic" in sys.argv
    if enable_semantic:
        graph = add_semantic_edges(graph)
        print("  (semantic overlap edges included — may be noisy)")

    with open(GRAPH_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)

    print(f"Graph compiled: {len(nodes)} nodes, {len(graph['edges'])} edges")

if __name__ == "__main__":
    main()