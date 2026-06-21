import os
from datetime import datetime

QUEUE = "tools/notebooklm_queue"
OUTPUT = "sources/notes"

def create_queue_entry(pdf):
    name = pdf.replace(".pdf", "")

    content = f"""
# {name}

## NotebookLM Processing Queue

Status: Pending
Created: {datetime.now().isoformat()}

## Required Extraction
- Architecture concepts
- Security mechanisms
- Firmware relevance
- Attack surface insights
- Open questions
"""

    path = os.path.join(OUTPUT, name + ".md")

    with open(path, "w") as f:
        f.write(content)

def scan_pdfs():
    return [f for f in os.listdir(QUEUE) if f.endswith(".pdf")]

def main():
    for pdf in scan_pdfs():
        create_queue_entry(pdf)

if __name__ == "__main__":
    main()