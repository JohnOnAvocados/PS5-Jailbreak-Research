# Hypervisor Version Diffing Guide

## Overview

The PS5 hypervisor has undergone major architectural changes across firmware versions, with two critical inflection points: **FW 3.00** (standalone hypervisor + HyLonome introduced) and **FW 7.00** (TMR OOB patched, no public HV exploits since). Systematic cross-version comparison of hypervisor binaries is the most promising approach for discovering new hypervisor vulnerabilities on modern firmware (>=7.00).

## Architectural Versions

### Pre-3.00 (FW <=2.70)
- Hypervisor code **embedded in the kernel binary** as a single monolithic image
- 14 hypercalls (0x00-0x0D) — no VMClosure, no MP boot hypercalls
- Kernel controls AP (Application Processor) boot
- No HyLonome — Secure Loader loads hypervisor directly
- Known exploits: Byepervisor (vtable in data segment + debug flag), flatz (unreleased)

### 3.00-6.02 (FW 3.00-6.02)
- Standalone hypervisor + **HyLonome** (Hypervisor Loader) introduced
- Boot chain: `Boot ROM → Secure Loader → HyLonome → Hypervisor → Kernel`
- 17 hypercalls (0x00-0x10) — added VMClosure (0x0E), MP boot (0x0F-0x10)
- AP boot management moved from kernel to hypervisor
- Architecture split hardened the boot chain by adding an independently verified intermediate stage
- Known exploits: TMR Heap OOB (TheFloW, <=6.02)

### 7.00-13.40+ (FW >=7.00)
- TMR Heap OOB patched
- **No public hypervisor exploits** — the defining gap in PS5 research
- Hypervisor binary format and loading mechanism may have changed
- Unknown: NPT layout, xotext implementation, hypercall handler code, VM exit handling

## Exploit Catalog (Chronological)

| Exploit | FW | Discoverer | Technique | Patched |
|---------|-----|-----------|-----------|---------|
| Byepervisor (vtable) | <=2.70 | SpecterDev | Vtable pointer in readable HV data segment → vtable hijack | FW 3.00 |
| Byepervisor (debug flag) | <=2.70 | SpecterDev | Debug flag not cleared after rest mode → elevated privileges | FW 3.00 |
| flatz HV | <=2.70 | flatz | Unreleased — intended to chain with umtx UaF | FW 3.00 |
| Prosperous | <=4.51 | fail0verflow/flatz | TMR protection state editing for HV R/W | FW 5.00 |
| TMR Heap OOB | <=6.02 | TheFloW | Heap OOB in TMR manager via crafted TMR operations | FW 7.00 |
| **>=7.00** | **None** | **—** | **No public exploits** | **—** |

## Hypercall Evolution

| Number | Name | Pre-3.00 | 3.00-6.02 | 7.00+ |
|--------|------|----------|-----------|-------|
| 0x00-0x01 | Message interface | Present | Present | Present |
| 0x02-0x03 | Self-loading | Present | Present | Present |
| 0x04-0x05 | CPUID virtualization | Present | Present | Present |
| 0x06-0x0C | IOMMU management (7 calls) | Present | Present | Present |
| 0x0D | TMR error info | Present | Present | Present |
| 0x0E | VMClosure invocation | — | Added | Present |
| 0x0F-0x10 | MP boot control | — | Added | Present |

## Version Diffing Methodology

### Required Tools
- **Ghidra** with AMD64 SVM extensions for hypervisor binary analysis
- **Diaphora** or **Ghidra Diffing** for automated binary comparison
- Hypervisor binary extraction from PUP files for each target FW version

### Recommended FW Versions to Collect
| FW | Significance | Year |
|-----|--------------|------|
| 2.00 | Earliest jailbroken — baseline with embedded HV | 2020 |
| 3.00 | HyLonome introduced, standlone HV | 2021 |
| 5.00 | Prosperous patched | 2022 |
| 7.00 | TMR OOB patched — last HV exploit | 2023 |
| 9.00 | Native PS2 emulator introduced | 2024 |
| 11.00 | Security revision 0x0003FFFF | 2025 |
| 13.00 | P2JB + BD-JB-EX patched | 2026 |
| 13.40 | Latest as of June 2026 | 2026 |

### Analysis Target Areas

**1. Hypercall Handler Code (0x00-0x10)**
- Compare parameter validation logic for each hypercall across versions
- Look for: removed bounds checks, relaxed parameter constraints, changed data structures
- **Highest priority**: IOMMU hypercalls (0x06-0x0C) — 7 calls, most complex, most likely to contain version-specific bugs
- Pay special attention to IOMMU_SET_GUEST_BUFFERS (0x06) — buffer registration involves size calculation and permission assignment

**2. TMR Implementation**
- TMR (Trusted Memory Region) manager handles encrypted memory compartments
- Functions: sceSblTmrMap/Unmap, sceSblTmrEncAmmPt, sceSblTmrDecAmmPt, sceSblTmrExport
- Compare heap allocator implementation for TMR structures across versions
- Prosperous technique: manipulating TMR protection state (not heap corruption) — this approach might still work on newer FW

**3. NPT Page Table Management**
- Look for changes in NPT initialization, page table structure, PTE format
- xotext bit 58 handling — any changes to how execute-only pages are enforced
- Page walk and TLB behavior differences

**4. VM Exit Handling**
- Compare event injection code paths
- Race conditions in concurrent NMI/SMI/interrupt delivery
- VMCB state validation on VM exit — has it become stricter?

**5. VMClosure (0x0E)**
- Only on >=3.00 — state save/restore mechanism
- Cleanup path during termination — could be race condition
- Not present on early firmware, so less battle-tested

**6. IOMMU Event Log Handling**
- Compare event log reading (0x0B) and device table reading (0x0C)
- Memory layout disclosure via event log entries
- Firmware-specific differences in event severity classification

## Research Questions (Open)

- Q-CRIT-001: Has the hypervisor binary format changed between FW 6.02 and 7.00?
- Q-CRIT-002: How does the NPT page table structure differ between FW 2.70, 3.00, and 7.00+?
- Q-CRIT-003: Are there regression vulnerabilities — checks removed or weakened in newer FW?
- Q-IMP-001: Does Prosperous's TMR protection state manipulation technique work on FW 7.00+?
- Q-IMP-002: What hardening was applied to TMR heap allocator at FW 7.00?
- Q-IMP-003: Is the IOMMU hypercall handler implemented identically across all versions?
- Q-MIN-001: Are error codes or error messages different between versions (could indicate changed handling)?

## References

- `research/hypervisor/hypervisor.md` — 222-line HV architecture source
- `research/hypervisor/iommu_architecture.md` — IOMMU hypercalls, event log, AMD-Vi
- `research/exploit_history/boot_hypervisor.md` — HV exploit history
- `research/exploit_history/cve_timeline.md` — CVE chronology
- [psdevwiki: Hypervisor](https://www.psdevwiki.com/ps5/Hypervisor)
- [psdevwiki: Hypervisor Loader](https://www.psdevwiki.com/ps5/Hypervisor_Loader)
