from __future__ import annotations

import json
from pathlib import Path

GRAPH = Path("graph/graph.json")
REPORTS = Path("reports")

def run():
    if not GRAPH.exists():
        raise FileNotFoundError("graph/graph.json not found. Run pipeline first.")
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))

    REPORTS.mkdir(parents=True, exist_ok=True)
    summary = graph.get("stats", {})
    content = [
        "# Final System Summary",
        "",
        "## Graph Summary",
        "```json",
        json.dumps(summary, indent=2),
        "```",
        "",
        "## Top Hubs",
    ]
    for item in summary.get("top_hubs", [])[:10]:
        content.append(f"- {item['id']} ({item['layer']}) degree={item['degree']}")
    (REPORTS / "final_system_summary.md").write_text("\n".join(content) + "\n", encoding="utf-8")

if __name__ == "__main__":
    run()
