from pathlib import Path
import json

INBOX = Path("inbox")
OUT = Path("intermediate/raw.json")

def ingest_file(file):
    return {
        "id": file.stem,
        "type": file.suffix,
        "content": file.read_text(errors="ignore"),
        "source": str(file)
    }

def run():
    data = []

    for f in INBOX.rglob("*"):
        if f.is_file():
            data.append(ingest_file(f))

    OUT.parent.mkdir(parents=True, exist_ok=True)

    OUT.write_text(json.dumps(data, indent=2))

if __name__ == "__main__":
    run()