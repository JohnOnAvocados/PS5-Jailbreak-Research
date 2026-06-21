import json
from collections import defaultdict

GRAPH_FILE = "graph_memory.json"

def load_graph():
    with open(GRAPH_FILE, "r") as f:
        return json.load(f)

def analyze(graph):
    degree = defaultdict(int)

    for edge in graph["edges"]:
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1

    sorted_nodes = sorted(degree.items(), key=lambda x: x[1], reverse=True)

    return {
        "hubs": sorted_nodes[:10],
        "isolated": [n for n in graph["nodes"] if degree[n] == 0],
        "edge_count": len(graph["edges"])
    }

def main():
    graph = load_graph()
    report = analyze(graph)

    print(report)

if __name__ == "__main__":
    main()