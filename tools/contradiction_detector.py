import os
import re

ROOT = "."

def extract_statements(text):
    # naive sentence split
    return re.split(r'(?<=[.!?]) +', text)

def scan_files():
    files = []

    for root, _, filenames in os.walk(ROOT):
        for f in filenames:
            if f.endswith(".md"):
                files.append(os.path.join(root, f))

    return files

def find_contradictions(files):
    statements = {}

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for line in extract_statements(text):
            key = line.lower().strip()

            if len(key) < 20:
                continue

            if key in statements:
                statements[key].append(file)
            else:
                statements[key] = [file]

    conflicts = {k: v for k, v in statements.items() if len(v) > 1}

    return conflicts

def main():
    files = scan_files()
    conflicts = find_contradictions(files)

    print("Potential contradictions:")
    for k, v in list(conflicts.items())[:20]:
        print("-", k)
        print("  found in:", v)

if __name__ == "__main__":
    main()