# PS5 Research Index

## Core Map
- [[MASTER_CONTEXT]]
- [[PROJECT_ROADMAP]]
- [[research_log]]
- [[open_questions]]
- [[assumptions]]
- [[terminology]]

## Research Areas
- [[research/hardware/hardware_overview|Hardware Architecture]]
- [[research/kernel/kernel|Kernel Layer]]
- [[research/hypervisor/hypervisor|Hypervisor Layer]]
- [[research/security_model/security_model|Security Model]]
- [[research/system_overview/system_overview|System Overview]]
- [[research/firmware/boot_chain|Firmware - Boot Chain]]
- [[research/firmware/secure_boot|Firmware - Secure Boot]]
- [[research/firmware/update_mechanism|Firmware - Update Mechanism]]
- [[research/analysis/attack_surface|Attack Surface]]
- [[research/analysis/mitigation_assessment|Mitigation Assessment]]
- [[research/analysis/synthesis|Research Synthesis]]
- [[research/exploit_history/webkit_kernel|WebKit & Kernel Exploits]]
- [[research/exploit_history/boot_hypervisor|Boot & Hypervisor Exploits]]
- [[research/exploit_history/cve_timeline|CVE Timeline]]

## External Inputs
- [[sources/notes/_index_|Source Notes]]

## Pipeline
- `pipeline.py` — entry point: Controller().full_run()
- `tools/controller.py` — orchestrator calling scripts.* modules
- `scripts/` — pipeline modules (ingest, normalize, extract, linker, graph_builder, obsidian_sync, wiki_sync, report_builder, query_engine, utils)
- `tools/` — additional analysis tools (graph_memory_compiler, contradiction_detector, vulnerability_scorer, etc.)
- `inbox/` → ingest → normalize → extract → linker → graph_builder → obsidian_sync / wiki_sync / report_builder

## Web Sources (by System Layer)
- [[sources/web/boot_chain/_index_|Boot Chain]]
- [[sources/web/cpu_architecture/_index_|CPU Architecture]]
- [[sources/web/firmware/_index_|Firmware]]
- [[sources/web/hypervisor/_index_|Hypervisor]]
- [[sources/web/kernel/_index_|Kernel]]
- [[sources/web/memory_protection/_index_|Memory Protection]]
- [[sources/web/threat_modeling/_index_|Threat Modeling]]
- [[sources/web/system_design/_index_|System Design]]
- [[sources/web/jailbreaking/_index_|Jailbreaking / Exploit Scene]]

## Obsidian Concept Layer
- [[obsidian/concepts/hardware_architecture|Concept: Hardware Architecture]]
- [[obsidian/concepts/kernel_architecture|Concept: Kernel Architecture]]
- [[obsidian/concepts/hypervisor_architecture|Concept: Hypervisor Architecture]]
- [[obsidian/concepts/security_model|Concept: Security Model]]
- [[obsidian/concepts/system_architecture|Concept: System Architecture]]
- [[obsidian/concepts/boot_chain|Concept: Boot Chain]]
- [[obsidian/concepts/secure_boot|Concept: Secure Boot]]
- [[obsidian/concepts/update_mechanism|Concept: Update Mechanism]]
- [[obsidian/maps/concept_map|Concept Map]]
- [[obsidian/maps/security_posture|Security Posture Map]]

## PSDevWiki Ingestion
- [[sources/web/psdevwiki/hardware/_index_|PSDevWiki - Hardware]]
- [[sources/web/psdevwiki/system_software/_index_|PSDevWiki - System Software]]
- [[sources/web/psdevwiki/filesystem/_index_|PSDevWiki - Filesystem]]
- [[sources/web/psdevwiki/security/_index_|PSDevWiki - Security]]
- [[sources/web/psdevwiki/kernel/_index_|PSDevWiki - Kernel]]
- [[sources/web/psdevwiki/hypervisor/_index_|PSDevWiki - Hypervisor]]
- [[sources/web/psdevwiki/debugging/_index_|PSDevWiki - Debugging]]
- [[sources/web/psdevwiki/devkits/_index_|PSDevWiki - DevKits]]
- [[sources/web/psdevwiki/storage/_index_|PSDevWiki - Storage]]
