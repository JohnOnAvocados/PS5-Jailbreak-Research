# Master Context

## Objective
Understand PS5 architecture, firmware security, and historical exploit surface.

## Current Phase
Bootstrap — structure initialized, no research started.

## Dependency Graph

```
architecture --> firmware
     |              |
     +------+-------+
            v
        analysis
            |
            v
    exploit_history
```

## Research Areas

| Area | Path | Prerequisites | Status |
|------|------|---------------|--------|
| Architecture | research/architecture/ | none | not started |
| Firmware | research/firmware/ | architecture | not started |
| Analysis | research/analysis/ | architecture, firmware | not started |
| Exploit History | research/exploit_history/ | architecture (partial) | not started |

## Research Order
1. Architecture (zero deps)
2. Firmware + Exploit History (parallel, depend on architecture)
3. Analysis (depends on all above)

## Known Facts
- Repository uses lowercase directory convention
- Research areas: architecture, firmware, analysis, exploit_history
- Sources organized: books, notes, papers, presentations

## Open Questions
- TBD

## Key Risks
- Unknown attack surface complexity
- Dependency chain: architecture delays cascade downstream
