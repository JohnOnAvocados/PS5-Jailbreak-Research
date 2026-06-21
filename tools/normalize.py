import json
from pathlib import Path

RAW = Path("intermediate/raw.json")
OUT = Path("intermediate/clean.json")

def normalize(text):
    return " ".join(text.split())

def run():
    data = json.loads(RAW.read_text())

    cleaned = []

    for item in data:
        cleaned.append({
            "id": item["id"],
            "source": item["source"],
            "content": normalize(item["content"])
        })

    OUT.write_text(json.dumps(cleaned, indent=2))

if __name__ == "__main__":
    run()