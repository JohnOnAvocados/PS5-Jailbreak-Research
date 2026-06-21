import os
import subprocess
from datetime import datetime

PDF_DIR = "sources/papers"
OUTPUT_DIR = "sources/notes"
REPO_DIR = "."

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def list_pdfs():
    return [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

def create_placeholder_summary(pdf_name):
    base = pdf_name.replace(".pdf", "")
    return f"""# {base}

## Source Summary (Pending NotebookLM Processing)

### Key Concepts
- TBD (extract via NotebookLM)

### Security Relevance
- TBD

### Architecture Impact
- TBD

### Open Questions
- TBD

### Metadata
- Source: {pdf_name}
- Processed: {datetime.now().isoformat()}
"""

def write_summary(pdf_name):
    base = pdf_name.replace(".pdf", ".md")
    path = os.path.join(OUTPUT_DIR, base)

    content = create_placeholder_summary(pdf_name)

    with open(path, "w") as f:
        f.write(content)

def git_commit():
    run("git add .")
    run('git commit -m "auto-sync: update source pipeline notes"')
    run("git push")

def main():
    ensure_dirs()
    pdfs = list_pdfs()

    for pdf in pdfs:
        write_summary(pdf)

    git_commit()

if __name__ == "__main__":
    main()