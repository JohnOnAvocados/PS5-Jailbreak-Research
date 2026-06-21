import json
from pathlib import Path

DATA = Path("intermediate/structured.json")
EDGES = Path("graph/edges.json")
OUT = Path("graph/graph.json")

def run():
    nodes = json.loads(DATA.read_text())
    edges = json.loads(EDGES.read_text())

    graph = {
        "nodes": nodes,
        "edges": edges
    }

    OUT.write_text(json.dumps(graph, indent=2))

if __name__ == "__main__":
    run()