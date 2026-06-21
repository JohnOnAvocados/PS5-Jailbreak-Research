import json
from pathlib import Path

DATA = json.loads(Path("intermediate/structured.json").read_text())

WIKI = Path("wiki")

def write_page(item):
    file = WIKI / f"{item['id']}.md"

    content = f"""
# {item['id']}

## System Layer
{item['layer']}

## Overview
{item['content'][:2000]}

## Source
{item['source']}
"""

    file.write_text(content)

def run():
    WIKI.mkdir(exist_ok=True)

    for item in DATA:
        write_page(item)

if __name__ == "__main__":
    run()