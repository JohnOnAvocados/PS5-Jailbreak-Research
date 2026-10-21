# SYSTEM SPECIFICATION — RESEARCH GRAPH ENGINE

## System Goal

Build a versioned knowledge base of PS5 hardware, firmware, software, and security architecture.

## Core Layers

- hardware
- boot_chain
- firmware
- kernel
- hypervisor
- cpu_architecture
- memory_protection
- threat_modeling
- security_model
- system_overview

## Repository Responsibilities

- `inbox/` contains raw inputs
- `intermediate/` stores pipeline outputs
- `graph/` stores nodes, edges, and summaries
- `wiki/` stores GitHub Wiki-ready pages — this is the published deliverable, pushed to the
  repo's actual GitHub Wiki (see `wiki/README_PUBLISHING.md`)
- `obsidian/` is legacy/internal; no longer a maintained output (decision made 2026-10-21 —
  the project moved from an Obsidian vault to the GitHub Wiki as the delivery format)
- `reports/` stores synthesized reports

## Pipeline Contract

1. ingest raw inputs
2. normalize content
3. extract structure
4. build semantic links
5. compile graph
6. sync wiki (`wiki/` — publish from here to the GitHub Wiki)

## Writing Rules

- preserve existing files
- prefer incremental updates
- use internal wikilinks for related pages
- keep summaries high level and factual
- classify content by system layer

## Query Rules

Queries should be answered from graph outputs where possible instead of re-reading raw files.
