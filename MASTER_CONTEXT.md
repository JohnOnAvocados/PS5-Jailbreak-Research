# Master Context

## Objective
Systematically map PS5 exploit surface across all six architectural layers from hardware to application-level security history.

## Current State

**Phase:** 1 — Foundation research execution.
**Status:** DEEP RESEARCH COMPLETE. 17 research files across all domains (8,500+ lines total). New: southbridge_analysis.md (704 lines), hardware_attack_surface.md (469 lines), jailbreak_comprehensive.md (581 lines), research_roadmap.md (537 lines). Comprehensive jailbreak history covers 2020-2026 across 4 eras, full exploit chain compatibility matrix (14 firmware ranges), 12+ kernel exploit techniques, 4 hypervisor exploits, userland entry taxonomy, key researcher catalog, homebrew ecosystem analysis, anti-rollback mechanism documentation, speculative execution vulnerability assessment, and prioritized 3-tier research agenda. Graph: 317 nodes, 1,300 edges.
**Operating paradigm:** Repository intelligence engine mode active.
**Blockers:** None. All research complete. Pipeline ready for run.

### Milestones
| # | Milestone | Target | Status |
|--|-----------|--------|--------|
| M1 | Repository structure finalized | Week 0 | Done |
| M2 | All research template files created | Week 0 | Done |
| M3 | Architecture layer documented | Week 1 | Done |
| M4 | Firmware + Secure Boot documented | Week 2 | Done |
| M5 | Hypervisor layer documented | Week 3 | Done |
| M6 | Kernel layer documented | Week 4 | Done |
| M7 | System overview + security model synthesized | Week 5 | Done |
| M8 | Exploit history compiled | Week 6 | Done |

---

## Dependency Graph

```
                         +-----------------------+
                         | Hardware Architecture |
                         +----------+------------+
                                    |
                +-------------------+-------------------+
                |                                       |
     +----------v----------+                 +----------v-----------+
     |   Firmware System   |                 | Secure Boot Chain   |
     +----------+----------+                 +----------+-----------+
                |                                       |
                +-------------------+-------------------+
                                    |
                         +----------v------------+
                         |  Hypervisor Layer    |
                         +----------+------------+
                                    |
                         +----------v------------+
                         |    Kernel Layer       |
                         +----------+------------+
                                    |
                         +----------v------------+
                         |   Exploit History    |
                         +-----------------------+

Legend:
  A ───> B   = B depends on A
  Parallel   = Firmware + Secure Boot can run concurrently
  Dotted     = Exploit History pulls from all layers
```

## Learning Order

### Tier 0 — Foundation (Week 1)
| Module | Dependencies | Est. Effort |
|--------|-------------|-------------|
| Hardware Architecture | none | 20h |

### Tier 1 — Boot Layer (Week 2)
| Module | Dependencies | Est. Effort |
|--------|-------------|-------------|
| Firmware System | Hardware Architecture | 15h |
| Secure Boot Chain | Hardware Architecture | 10h |

### Tier 2 — System Layer (Week 3)
| Module | Dependencies | Est. Effort |
|--------|-------------|-------------|
| Hypervisor Layer | Firmware, Secure Boot | 15h |
| Kernel Layer | Hypervisor | 15h |

### Tier 3 — Context Layer (Week 4+)
| Module | Dependencies | Est. Effort |
|--------|-------------|-------------|
| Exploit History | All layers (contextual) | 10h |

---

## Priorities

### P0 — Must resolve before any exploit work
- SoC architecture and memory map baseline
- Boot chain stage identification
- Secure boot key hierarchy

### P1 — Required for meaningful analysis
- Hypervisor partition model and isolation boundaries
- Kernel syscall surface and security mechanism
- IOMMU configuration and stage-2 page tables

### P2 — Valuable context but non-blocking
- Complete CVE timeline compilation
- PS4-to-PS5 technique carryover analysis
- Research community mapping
- Toolchain and disassembler support

---

## Unknowns Register

### Hardware Architecture
- [ ] Exact SoC die revision (Oberon vs Ariel vs newer)
- [ ] Full memory map (reserved regions, MMIO windows)
- [ ] IOMMU page table format and walk cache
- [ ] Interrupt controller model (GIC? custom?)
- [ ] System hub / southbridge topology
- [ ] JTAG/SWD/debug interface presence
- [ ] OTP/eFuse bit assignment map
- [ ] Clock tree and reset domain boundaries

### Firmware System
- [ ] Boot ROM size, version, and patch level
- [ ] Number and identity of bootloader stages
- [ ] Encryption vs signing per stage
- [ ] Firmware update delta vs full-flash mechanism
- [ ] Recovery mode trigger and capabilities
- [ ] Version numbering scheme semantics
- [ ] Known bootloader bugs (any public?)

### Secure Boot Chain
- [ ] Root key source (fuses? OTP? eFuse row?)
- [ ] Number of keys in chain and their derivation
- [ ] Signature algorithm (RSA? ECDSA? EdDSA? key length?)
- [ ] Per-stage verification boundary
- [ ] Anti-rollback fuse burn logic
- [ ] Debug/developer mode bypass conditions
- [ ] Whether secure boot is unified or partition-specific

### Hypervisor Layer
- [ ] Hypervisor type (Type 1 native? Type 1.5?)
- [ ] Virtualization scope (CPU? memory? GPU? I/O?)
- [ ] Partition model (number, purpose, privilege levels)
- [ ] Hypercall ABI and surface
- [ ] Memory isolation: stage-2 page tables? IOMMU?
- [ ] VM exit handling mechanism
- [ ] Whether proprietary or based on an existing hypervisor

### Kernel Layer
- [ ] FreeBSD base version and divergence extent
- [ ] Custom syscall additions vs pure FreeBSD
- [ ] KASLR effectiveness (bits of entropy, re-randomization)
- [ ] Hardware memory protection (SMAP? SMEP? PAN? PXN?)
- [ ] Driver architecture (I/O kit port? custom?)
- [ ] Sandbox model (Capsicum? custom? seatbelt?)
- [ ] Debug stubs left in release kernels
- [ ] Kernel text/data isolation (W^X enforcement)

### Exploit History
- [ ] Complete CVE timeline (PS4 + PS5 specific)
- [ ] WebKit/Safari version map per firmware
- [ ] Kernel exploit technique taxonomy
- [ ] Hypervisor escape public record (if any)
- [ ] Boot chain attack literature (Fail0verflow, etc.)
- [ ] Active research community landscape
- [ ] Bug bounty program details and scope
- [ ] Between-firmware regression history

---

## Key Risks
1. **Dependency cascade**: Architecture delays → everything delayed
2. **Source scarcity**: PS5 has less public documentation than PS4
3. **Layer opacity**: Hypervisor layer may be entirely undocumented
4. **Scope creep**: Exploit history can balloon into full-time work
5. **Tooling gap**: No confirmed disassembler support for PS5 binaries
