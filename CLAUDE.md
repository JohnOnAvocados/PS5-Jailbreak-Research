# BOOTSTRAP INSTRUCTIONS

This repository is controlled by `controller.py` and the pipeline scripts.

## Operating rules

- read `SYSTEM_SPEC.md` first
- preserve existing structure
- do not rewrite working modules unless patching is required
- treat the repo as a research graph, not a chat transcript
- keep documentation synchronized across:
  - `graph/`
  - `wiki/` (the published deliverable — pushed to the repo's GitHub Wiki)
  - `reports/`
- `obsidian/` is legacy/internal only; the project no longer delivers an Obsidian vault
  (decision made 2026-10-21) — don't treat it as an output to keep current

## Runtime expectation

The normal entry point is:

```bash
python controller.py full_run
```

## Output expectation

Every pipeline run should refresh:
- raw ingestion outputs
- structured records
- links
- graph outputs
- wiki pages (`wiki/` — this is what gets pushed to the GitHub Wiki)
