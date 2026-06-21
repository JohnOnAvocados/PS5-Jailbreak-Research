import os
from collections import defaultdict

ROOT = "sources/notes"

def scan():
    clusters = defaultdict(list)

    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8") as file:
                    text = file.read().lower()

                if "hypervisor" in text:
                    clusters["hypervisor"].append(path)
                if "kernel" in text:
                    clusters["kernel"].append(path)
                if "firmware" in text:
                    clusters["firmware"].append(path)
                if "boot" in text:
                    clusters["boot_chain"].append(path)
                if "exploit" in text:
                    clusters["exploits"].append(path)

    return clusters

def main():
    clusters = scan()

    print("Knowledge Clusters:\n")

    for k, v in clusters.items():
        print(k.upper())
        for item in v:
            print(" -", item)
        print()

if __name__ == "__main__":
    main()