import os
import re
import json

ROOT = "research"
OUTPUT = "intermediate/insights.json"

def extract_insights(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    insights = []
    keywords = [
        "is defined as",
        "means",
        "allows",
        "enables",
        "security",
        "vulnerability",
        "attack",
        "exploit",
        "mechanism",
        "designed to"
    ]
    for s in sentences:
        if any(k in s.lower() for k in keywords):
            insights.append(s.strip())
    return insights[:20]

def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    results = {}
    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as fh:
                    text = fh.read()
                insights = extract_insights(text)
                if insights:
                    results[path] = insights
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Extracted insights from {len(results)} files -> {OUTPUT}")

if __name__ == "__main__":
    main()
