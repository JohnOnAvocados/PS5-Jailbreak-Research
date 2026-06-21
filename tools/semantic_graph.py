import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = "sources/notes"
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def load_chunks():
    chunks = []
    files = []

    for root, _, filenames in os.walk(ROOT):
        for f in filenames:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as file:
                    chunks.append(file.read())
                    files.append(path)

    return files, chunks

def build_embeddings(texts):
    return MODEL.encode(texts)

def build_similarity_matrix(embeddings):
    return cosine_similarity(embeddings)

def find_links(files, sim_matrix, threshold=0.55):
    links = []

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            if sim_matrix[i][j] > threshold:
                links.append((files[i], files[j], sim_matrix[i][j]))

    return links

def write_links(links):
    for a, b, score in links:
        for file in [a, b]:
            with open(file, "a", encoding="utf-8") as f:
                f.write(f"\n\nRelated (semantic): [[{os.path.basename(a)}]] ↔ [[{os.path.basename(b)}]] (score={score:.2f})\n")

def main():
    files, chunks = load_chunks()

    print(f"Loaded {len(files)} documents")

    embeddings = build_embeddings(chunks)
    sim = build_similarity_matrix(embeddings)

    links = find_links(files, sim)

    write_links(links)

    print(f"Created {len(links)} semantic links")

if __name__ == "__main__":
    main()