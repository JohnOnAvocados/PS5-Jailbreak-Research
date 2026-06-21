from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict, deque
from pathlib import Path

GRAPH_FILE = Path("graph/graph.json")

class QueryError(Exception):
    pass

def load_graph() -> dict:
    if not GRAPH_FILE.exists():
        raise FileNotFoundError("graph/graph.json not found. Run pipeline first.")
    return json.loads(GRAPH_FILE.read_text(encoding="utf-8"))

def _nodes_index(graph):
    return {n["id"]: n for n in graph.get("nodes", [])}

def _neighbors(graph):
    adj = defaultdict(set)
    for e in graph.get("edges", []):
        adj[e["from"]].add(e["to"])
        adj[e["to"]].add(e["from"])
    return adj

def _parse_condition(expr: str):
    expr = expr.strip()
    m = re.match(r"(?P<field>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<op>=|!=|>=|<=|>|<|contains)\s*(?P<value>.+)", expr)
    if not m:
        raise QueryError(f"Could not parse condition: {expr}")
    field = m.group("field")
    op = m.group("op")
    value = m.group('value').strip().strip('"').strip("'")
    return field, op, value

def _match_value(actual, op, wanted):
    if actual is None:
        return False
    if isinstance(actual, list):
        actual = " ".join(map(str, actual))
    if op == "contains":
        return str(wanted).lower() in str(actual).lower()
    if op == "=":
        return str(actual).lower() == str(wanted).lower()
    if op == "!=":
        return str(actual).lower() != str(wanted).lower()
    try:
        a = float(actual)
        b = float(wanted)
    except Exception:
        a = str(actual).lower()
        b = str(wanted).lower()
    if op == ">":
        return a > b
    if op == "<":
        return a < b
    if op == ">=":
        return a >= b
    if op == "<=":
        return a <= b
    return False

def find_nodes(graph, where_clause: str = ""):
    nodes = graph.get("nodes", [])
    if not where_clause:
        return nodes

    clauses = [c.strip() for c in re.split(r"\bAND\b", where_clause, flags=re.I) if c.strip()]
    results = []
    for node in nodes:
        ok = True
        for clause in clauses:
            field, op, value = _parse_condition(clause)
            actual = node.get(field)
            if field in {"tags", "concepts", "urls", "wikilinks"} and op == "contains":
                actual = node.get(field, [])
            if not _match_value(actual, op, value):
                ok = False
                break
        if ok:
            results.append(node)
    return results

def find_edges(graph, where_clause: str = ""):
    edges = graph.get("edges", [])
    if not where_clause:
        return edges

    clauses = [c.strip() for c in re.split(r"\bAND\b", where_clause, flags=re.I) if c.strip()]
    results = []
    for edge in edges:
        ok = True
        for clause in clauses:
            field, op, value = _parse_condition(clause)
            actual = edge.get(field)
            if field == "type":
                actual = " ".join(edge.get("types", []))
            if field == "types" and op == "contains":
                actual = edge.get("types", [])
            if not _match_value(actual, op, value):
                ok = False
                break
        if ok:
            results.append(edge)
    return results

def traverse(graph, start: str, depth: int = 1):
    adj = _neighbors(graph)
    seen = {start}
    frontier = deque([(start, 0)])
    out = []
    while frontier:
        node, d = frontier.popleft()
        if d >= depth:
            continue
        for nxt in adj.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                out.append({"from": node, "to": nxt, "depth": d + 1})
                frontier.append((nxt, d + 1))
    return out

def path(graph, start: str, end: str):
    adj = _neighbors(graph)
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == end:
            break
        for nxt in adj.get(cur, []):
            if nxt not in prev:
                prev[nxt] = cur
                q.append(nxt)
    if end not in prev:
        return []
    route = []
    cur = end
    while cur is not None:
        route.append(cur)
        cur = prev[cur]
    return list(reversed(route))

def stats(graph):
    return graph.get("stats", {})

def execute(query: str):
    graph = load_graph()
    q = query.strip()

    if q.upper() == "STATS":
        return stats(graph)

    m = re.match(r"^FIND\s+(nodes|edges)(?:\s+WHERE\s+(.+))?$", q, flags=re.I)
    if m:
        kind = m.group(1).lower()
        where = m.group(2) or ""
        return find_nodes(graph, where) if kind == "nodes" else find_edges(graph, where)

    m = re.match(r"^TRAVERSE\s+from\s+(.+?)\s+depth\s+(\d+)$", q, flags=re.I)
    if m:
        return traverse(graph, m.group(1).strip(), int(m.group(2)))

    m = re.match(r"^PATH\s+from\s+(.+?)\s+to\s+(.+)$", q, flags=re.I)
    if m:
        return path(graph, m.group(1).strip(), m.group(2).strip())

    m = re.match(r"^NEIGHBORS\s+(.+)$", q, flags=re.I)
    if m:
        return traverse(graph, m.group(1).strip(), 1)

    raise QueryError(f"Unknown query: {query}")

def main():
    parser = argparse.ArgumentParser(description="Query the PS5 research graph")
    parser.add_argument("query", nargs="+", help="Query string, e.g. 'FIND nodes WHERE layer = firmware'")
    args = parser.parse_args()
    result = execute(" ".join(args.query))
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
