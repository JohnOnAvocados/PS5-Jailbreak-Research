import os
import re

ROOT = "research/firmware"

def extract_versions(text):
    return re.findall(r"\b\d+\.\d+|\bfirmware\s+\d+", text.lower())

def scan():
    timeline = {}

    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8") as file:
                    text = file.read()

                versions = extract_versions(text)

                for v in versions:
                    timeline.setdefault(v, []).append(path)

    return timeline

def main():
    timeline = scan()

    print("Firmware timeline map:\n")

    for k, v in sorted(timeline.items()):
        print(k, "->", len(v), "entries")

if __name__ == "__main__":
    main()