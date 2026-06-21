import json
import re

GRAPH_FILE = "graph_memory.json"

# ----------------------------
# LOAD GRAPH
# ----------------------------
def load_graph():
    with open(GRAPH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------
# PARSE QUERY
# ----------------------------
def parse(query):
    query = query.strip()

    if query.startswith("FIND nodes"):
        return ("find_nodes", query)
    if query.startswith("FIND edges"):
        return ("find_edges", query)
    if query.startswith("TRAVERSE"):
        return ("traverse", query)
    if query.startswith("CLUSTER"):
        return ("cluster", query)

    return ("unknown", query)

# ----------------------------
# NODE FILTERING
# ----------------------------
def find_nodes(graph, query):
    results = []

    conditions = re.findall(r"WHERE (.*)", query)
    condition = conditions[0] if conditions else ""

    for node, data in graph["nodes"].items():
        text = node.lower() + " " + " ".join(data.get("concepts", [])).lower()

        if "contains =" in condition:
            keyword = condition.split("contains =")[1].strip()
            if keyword.lower() in text:
                results.append(node)

        elif "tag =" in condition:
            tag = condition.split("tag =")[1].strip()
            if tag.lower() in text:
                results.append(node)

        elif "vulnerability_score" in condition:
            # optional field (if added later)
            if data.get("score", 0) > 7:
                results.append(node)

        else:
            results.append(node)

    return results

# ----------------------------
# EDGE FILTERING
# ----------------------------
def find_edges(graph, query):
    results = []

    if "type =" in query:
        etype = query.split("type =")[1].split()[0]

        for edge in graph["edges"]:
            if edge.get("type") == etype:
                results.append(edge)

    elif "weight >" in query:
        val = float(query.split("weight >")[1].strip())

        for edge in graph["edges"]:
            if edge.get("weight", 0) > val:
                results.append(edge)

    else:
        results = graph["edges"]

    return results

# ----------------------------
# TRAVERSAL ENGINE
# ----------------------------
def traverse(graph, query):
    match = re.search(r"from (.*?) -> DEPTH (\d+)", query)

    if not match:
        return []

    start = match.group(1).strip()
    depth = int(match.group(2))

    visited = set()
    frontier = [start]
    result = []

    for _ in range(depth):
        next_frontier = []

        for node in frontier:
            if node in visited:
                continue

            visited.add(node)

            for edge in graph["edges"]:
                if node in edge["source"]:
                    next_frontier.append(edge["target"])

        result.extend(next_frontier)
        frontier = next_frontier

    return list(set(result))

# ----------------------------
# MAIN EXECUTOR
# ----------------------------
def run_query(query):
    graph = load_graph()

    qtype, raw = parse(query)

    if qtype == "find_nodes":
        return find_nodes(graph, raw)

    if qtype == "find_edges":
        return find_edges(graph, raw)

    if qtype == "traverse":
        return traverse(graph, raw)

    return {"error": "unknown query type"}

# ----------------------------
# CLI ENTRY
# ----------------------------
def main():
    print("Graph Query Engine Ready")
    print("Enter query:")

    while True:
        q = input("> ")

        if q in ["exit", "quit"]:
            break

        result = run_query(q)

        print("\nRESULT:\n")
        print(result)
        print("\n---\n")

if __name__ == "__main__":
    main()