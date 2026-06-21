# Implementation Map

## Added layers

- `scripts/` — pipeline modules
- `graph/` — graph state
- `wiki/` — GitHub Wiki-ready pages
- `obsidian/` — vault sync
- `.github/workflows/` — automation

## Main control files

- `controller.py`
- `pipeline.py`
- `scripts/query_engine.py`

## Main data flow

`inbox/` → `intermediate/` → `graph/` → `wiki/` → `obsidian/`
