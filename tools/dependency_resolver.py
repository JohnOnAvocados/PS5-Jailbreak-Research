import os

ROOT = "research"

def scan():
    graph = {}

    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8") as file:
                    text = file.read()

                links = [line for line in text.split("\n") if "[[" in line]

                graph[path] = links

    return graph

def main():
    graph = scan()

    print("Dependency map:\n")

    for k, v in graph.items():
        if len(v) == 0:
            print("Isolated node:", k)

if __name__ == "__main__":
    main()