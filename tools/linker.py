import json
from pathlib import Path
from difflib import SequenceMatcher

DATA = Path("intermediate/structured.json")
OUT = Path("graph/edges.json")

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def run():
    data = json.loads(DATA.read_text())
    edges = []

    for i in range(len(data)):
        for j in range(i + 1, len(data)):

            score = similarity(
                data[i]["content"][:400],
                data[j]["content"][:400]
            )

            if score > 0.3:
                edges.append({
                    "from": data[i]["id"],
                    "to": data[j]["id"],
                    "weight": score
                })

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(edges, indent=2))

if __name__ == "__main__":
    run()