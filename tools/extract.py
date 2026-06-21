import json
from pathlib import Path

DATA = Path("intermediate/clean.json")
OUT = Path("intermediate/structured.json")

SYSTEM_LAYERS = [
    "hardware",
    "firmware",
    "kernel",
    "hypervisor",
    "security_model",
    "boot_chain"
]

def classify(text):
    text = text.lower()

    for layer in SYSTEM_LAYERS:
        if layer in text:
            return layer

    return "unknown"

def run():
    data = json.loads(DATA.read_text())

    structured = []

    for item in data:
        structured.append({
            "id": item["id"],
            "layer": classify(item["content"]),
            "content": item["content"],
            "source": item["source"]
        })

    OUT.write_text(json.dumps(structured, indent=2))

if __name__ == "__main__":
    run()