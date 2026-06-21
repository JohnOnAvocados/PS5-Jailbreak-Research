# Contributing to This Research

## Repository Structure

```
PS5-Jailbreak-Research/
├── inbox/               # Source files for pipeline ingestion
├── sources/             # Raw source data (psdevwiki, jailbreaking)
├── research/            # Deep analysis documents by layer
│   ├── hardware/        # SoC, southbridge, attack surface
│   ├── firmware/        # Boot chain, secure boot, PSP
│   ├── hypervisor/      # Hypervisor arch, hypercalls, IOMMU
│   ├── kernel/          # Kernel arch, syscalls, IOCTLs, GPU DMA
│   ├── userland/        # WebKit, BD-J, V8, mast1c0re
│   ├── exploit_history/ # CVE timelines, jailbreak history
│   ├── analysis/        # Syntheses, roadmaps, attack surface
│   └── security_model/  # Auth IDs, PAIDs, keys, XOM
├── wiki/                # Hand-curated + auto-generated wiki pages
├── obsidian/            # Obsidian vault (concepts, maps, nodes)
├── graph/               # Knowledge graph outputs (JSON)
├── intermediate/        # Pipeline intermediate data (JSON)
├── reports/             # Pipeline reports
├── scripts/             # Pipeline modules (Python)
└── tools/               # Pipeline orchestrator
```

## Documentation Conventions

### File Naming
- Use `Title_Case_With_Underscores.md` for wiki pages and concept notes
- Use `snake_case.md` for research files in `research/`
- Hyphenated names become underscores in wikilinks

### Wikilinks
Use `[[wikilinks]]` to cross-reference:
- Between wiki pages in `wiki/`
- Between Obsidian concepts in `obsidian/concepts/`
- From research files to Obsidian concepts

### Distinguish Facts from Unknowns
In research documents, explicitly label:
- **Confirmed:** Verified facts with sources
- **Unknown:** Open questions needing investigation
- **Speculative:** Informed hypotheses needing validation

### Crediting Sources
- Include `## Source URL` in inbox files
- Reference psdevwiki URLs for hardware/firmware facts
- Credit researchers by name for exploit discoveries
- Link to original blog posts/GitHub repos when known

## Research Priorities

See `research/analysis/research_roadmap.md` for the full prioritized agenda.

### Current Highest Priority (Tier 1)
1. EMC/EAP firmware disassembly (Ghidra ARM + PUP extraction)
2. New kernel exploit for FW 13.00+ (FreeBSD kqueue/socket/IPC fuzzing)
3. Hypervisor binary extraction and version diffing (FW 2.00 vs 7.00+)

### Documentation Needed
- Missing wiki pages for: CVE timeline, PS Portal boot chain, attack surface map
- Updated firmware version history as new FW releases occur
- Expanded IOCTL reference as new entries are discovered

## Adding a New Research Finding

1. **Check for duplicates** — search `research/`, `wiki/`, `obsidian/concepts/` and `sources/`
2. **Choose the right location** — hardware finding → `research/hardware/`, kernel finding → `research/kernel/`, etc.
3. **Write the file** following conventions above
4. **Add to inbox** — copy to `inbox/` with proper frontmatter for pipeline ingestion
5. **Update cross-references** — add wikilinks in related docs, update Topics.md
6. **Run the pipeline** — `python tools/controller.py full_run`
7. **Commit** — `git add -A && git commit -m "descriptive message" && git push`

## Wiki Page Template

```markdown
# Topic Title

## Overview
2-3 paragraphs describing what this topic covers, why it matters, and its role
in the PS5 security landscape.

## Architecture
Key components, their relationships, and how they work.

### Subcomponent 1
Details.

### Subcomponent 2
Details.

## Security Considerations
Attack surface, known vulnerabilities, mitigation assessment.

## Open Questions
- What is unknown about this topic
- What needs further investigation

## References
- `research/path/to/source.md` — linked research file
- [External URL](https://example.com)
```

## Code of Conduct

- This is security research — all findings are documented for defensive purposes
- Do not include exploit code, key material, or proprietary Sony data
- Credit all sources and researchers
- Distinguish facts from speculation clearly
- Treat the repo as a research graph, not a chat transcript
