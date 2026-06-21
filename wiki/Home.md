# PS5 Jailbreak Research Wiki

## About This Wiki

A curated knowledge base for PS5 hardware, firmware, kernel, hypervisor, and security-model research. This wiki synthesizes public source data (psdevwiki, researcher publications, exploit documentation) with original deep research into a structured, cross-referenced graph.

The wiki is maintained alongside an Obsidian vault (`obsidian/`), a knowledge graph (`graph/`), and a pipeline (`tools/controller.py`) that keeps all forms of documentation synchronized.

## Quick Start

| If you want to... | Start here |
|---|---|
| Understand the full architecture | [System Overview](sections/system_overview.md), [Hardware](sections/hardware.md) |
| Learn the exploit path from userland to hypervisor | [Userland Entry](research/userland/) → [Kernel Exploitation](research/kernel/) → [Hypervisor](research/hypervisor/) |
| See which exploits work on which firmware | [Exploit Compatibility Matrix](Exploit_Compatibility_Matrix) |
| Understand boot security and cryptography | [Boot Chain](sections/boot_chain.md), [Secure Boot](sections/boot_chain.md) |
| Dive into southbridge firmware (EMC/EAP/CP Box) | [Southbridge Architecture](Southbridge_Architecture) |
| Read the full research roadmap | [Research Roadmap](research/analysis/research_roadmap.md) |

## Topic Hierarchy

```
Hardware ──┬─ SoC (Oberon/Viola Zen 2 + RDNA 2)
           ├─ Southbridge (EMC/EAP/CP Box)      → Southbridge_Architecture
           ├─ Memory System (GDDR6, NAND, flash)
           ├─ Attack Surface                     → sections/hardware_attack_surface.md
           └─ IOMMU Architecture                 → research/hypervisor/iommu_architecture.md

Firmware ──┬─ Boot Chain (5 stages)              → sections/boot_chain.md
           ├─ Secure Boot (RSA-4096, AES-CBC)
           ├─ PSP / Secure Processor
           ├─ EMC/EAP Firmware                   → Southbridge_Architecture
           └─ Anti-Rollback / Security Revisions

Hypervisor ─┬─ Architecture (NPT, xotext, SVM)   → sections/hypervisor.md
            ├─ Hypercall Interface (17 calls)
            ├─ IOMMU / SMMU                      → research/hypervisor/iommu_architecture.md
            ├─ TMR Management
            └─ Exploit History (<=FW 6.02)

Kernel ────┬─ FreeBSD 11.0 Derivative            → sections/kernel.md
           ├─ Syscall Catalog (500+ syscalls)    → research/kernel/syscall_catalog.md
           ├─ IOCTL Devices (100+ /dev/ entries)
           ├─ Secure Modules (20+ 0x8002xxxx)
           ├─ GPU DMA Exploitation               → research/kernel/gpu_dma_exploitation.md
           └─ Exploit Landscape                  → Kernel_Exploit_Landscape

Userland ──┬─ Y2JB (V8 TheHole, CVE-2021-38003) → research/userland/y2jb_sandbox_escape.md
           ├─ mast1c0re (PS2 Emulator JIT)       → research/userland/mast1c0re_jit_pipeline.md
           ├─ BD-JB (Blu-ray Java, <=FW 12.70)
           └─ WebKit / WebView Entry Points

Exploits ──┬─ CVE Timeline / History             → sections/cve_timeline.md
           ├─ Exploit Chains / Compatibility     → Exploit_Compatibility_Matrix
           ├─ Homebrew Enablers (etaHEN, kstuff)
           └─ Jailbreak History                  → research/exploit_history/jailbreak_comprehensive.md
```

## Pipeline Sections

Auto-generated node listings organized by system layer:

| Section | Nodes | Description |
|---------|-------|-------------|
| [Hardware](sections/hardware.md) | 51 | SoC, GPU, southbridge, memory, peripherals, attack surface |
| [Firmware](sections/firmware.md) | 42 | Boot chain, secure boot, EMC/EAP, PSP, keys, modules |
| [Boot Chain](sections/boot_chain.md) | 28 | Boot ROM → Secure Loader → Hypervisor → Kernel |
| [System Overview](sections/system_overview.md) | 14 | Orbis OS, FW versions, system software, update mechanism |
| [Security Model](sections/security_model.md) | 14 | Auth IDs, PAIDs, SELF signing, Keystone, key hierarchy |
| [Hypervisor](sections/hypervisor.md) | 6 | Hypervisor architecture, hypercalls, HyLonome |
| [Memory Protection](sections/memory_protection.md) | 4 | XOM, NX, SMAP/SMEP/UMIP, W^X enforcement |
| [CPU Architecture](sections/cpu_architecture.md) | 1 | Zen 2 core details |
| [Kernel](sections/kernel.md) | 1 | Kernel overview |

## Knowledge Graph

- **161 nodes**, **3,734 edges**, **1 connected component**
- 9 system layers mapped with explicit wiki-linked relationships
- Pipeline: `python tools/controller.py full_run` regenerates all auto content

## Key Research Files

| File | Topic |
|------|-------|
| `research/hardware/southbridge_analysis.md` | EMC/EAP firmware, CP Box, serial flash, NVS (704 lines) |
| `research/hardware/hardware_attack_surface.md` | SPI, JTAG, voltage glitching, ZenBleed, peripheral attack surface (469 lines) |
| `research/hypervisor/iommu_architecture.md` | 7 IOMMU hypercalls, AMD-Vi, GPU DMA bypass context (200 lines) |
| `research/kernel/gpu_dma_exploitation.md` | GPU DMA kernel .data write, PM4 commands, NPT vs IOMMU gap (180 lines) |
| `research/kernel/syscall_catalog.md` | 500+ syscalls, 3 sysvec structures, 100+ IOCTL devices (200 lines) |
| `research/userland/mast1c0re_jit_pipeline.md` | PS2 emulator JIT, two-process architecture, bridge exploit (230 lines) |
| `research/userland/y2jb_sandbox_escape.md` | V8 TheHole, YouTube app, CVE-2021-38003 exploitation (180 lines) |
| `research/exploit_history/jailbreak_comprehensive.md` | Full jailbreak history, 10+ exploit chains (581 lines) |
| `research/analysis/research_roadmap.md` | 15 research gaps, prioritized agenda, methodology (537 lines) |

## Pipeline Stats

Last run: 161 source files → 161 graph nodes → 3,734 edges → 9 wiki sections → 156 Obsidian vault nodes → wiki pages
