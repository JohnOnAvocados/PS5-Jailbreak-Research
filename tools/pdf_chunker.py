import os
import fitz  # PyMuPDF
from datetime import datetime

INPUT_DIR = "sources/papers"
OUTPUT_DIR = "sources/notes"

CHUNK_SIZE = 800  # characters

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text

def chunk_text(text, size=CHUNK_SIZE):
    return [text[i:i+size] for i in range(0, len(text), size)]

def save_chunks(pdf_name, chunks):
    base = pdf_name.replace(".pdf", "")

    folder = os.path.join(OUTPUT_DIR, base)
    os.makedirs(folder, exist_ok=True)

    for i, chunk in enumerate(chunks):
        path = os.path.join(folder, f"chunk_{i}.md")

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"""# {base} — Chunk {i}

## Metadata
Source: {pdf_name}
Created: {datetime.now().isoformat()}

## Content
{chunk}
""")

def process_pdf(pdf_file):
    path = os.path.join(INPUT_DIR, pdf_file)

    text = extract_text(path)
    chunks = chunk_text(text)

    save_chunks(pdf_file, chunks)

def main():
    pdfs = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    for pdf in pdfs:
        process_pdf(pdf)

    print(f"Processed {len(pdfs)} PDFs into semantic chunks")

if __name__ == "__main__":
    main()