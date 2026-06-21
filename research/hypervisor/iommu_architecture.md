# IOMMU Architecture: Hypervisor-Managed DMA Protection on PS5

## Overview

The PS5 represents an architectural departure from standard AMD platforms in how I/O Memory Management Unit (IOMMU) control is handled. On conventional AMD systems (both Windows and Linux), the operating system kernel configures the IOMMU directly through MMIO register access. On PS5, IOMMU management has been moved entirely into the hypervisor layer — the kernel must request all IOMMU operations through 7 dedicated hypercalls (0x06-0x0C). This architectural shift makes the IOMMU the largest and most complex hypercall category (7 of 17 total hypercalls), and it has profound implications for DMA-based exploitation.

The IOMMU (called SMMU — System Memory Management Unit — in PS5 documentation) provides hardware-enforced isolation for all DMA-capable devices: the GPU, storage controllers (NVMe SSD), USB controllers, networking (Wi-Fi/Bluetooth), and audio hardware. Every DMA transaction from any device must pass through the IOMMU's address translation and permission checking before reaching physical memory. The hypervisor exclusively manages the IOMMU device table, page tables, command queues, and event logs.

The IOMMU's role is particularly critical for the GPU DMA copy exploit (FW >=6.00) — a kernel .data write bypass technique that works despite IOMMU protection. Understanding why the IOMMU does NOT prevent this bypass is one of the most important open questions in PS5 security research.

## AMD-Vi IOMMU Background

The PS5's IOMMU is based on the AMD-Vi (AMD I/O Virtualization Technology) specification, which provides:

### Device Table
- One entry per PCI device (up to 65,536 entries for a single PCI segment)
- Each entry: 32 bytes, must be contiguous in memory (max 2 MB for full table)
- Each entry contains: translation control bits, domain ID, page table root pointer, attributes
- The hypervisor controls device table read/write through hypercall 0x0C

### Address Translation
- Translates Device Virtual Addresses (DVAs) to System Physical Addresses (SPAs)
- Supports I/O page tables with configurable page sizes (4 KB, 2 MB, 1 GB)
- Hardware walks I/O page tables for each DMA transaction
- IOTLB caches translations for performance

### Command and Event Queues
- **Command Buffer:** Ring buffer for sending commands to the IOMMU (MMIO-programmed base, head/tail pointers)
- **Commands include:** COMPLETION_WAIT, INVALIDATE_IOMMU_CACHE, INVALIDATE_IOTLB, INVALIDATE_INTR_CACHE
- **Event Log:** Ring buffer for IOMMU event reporting (DMA faults, permission violations, page faults)
- **Event types:** ILLEGAL_DEV_TABLE_ENTRY, PAGE_FAULT, INVALID_DEVICE_REQUEST

### Key Features
- **DMA Remapping:** Controls which physical memory regions a device can access
- **Interrupt Remapping:** Controls interrupt delivery from devices to CPUs
- **ATS (Address Translation Services):** Allows PCIe devices to cache translations (reduces IOMMU lookup overhead)
- **PASID (Process Address Space ID):** Allows devices to target specific process address spaces
- **Guest I/O Protection:** Stage-2 translation for I/O (nested IOMMU page tables)
- **Secure Nested Paging (SEV-SNP):** Hardware memory encryption for I/O (available on Zen 2, but PS5 usage unknown)

## PS5 IOMMU Architecture

### Hypervisor Ownership

Unlike standard AMD platforms where the OS kernel:

1. Discovers the IOMMU via PCI configuration space (class=0x08, subclass=0x06, progif=0x00)
2. Programs the IOMMU MMIO base address from ACPI IVRS table
3. Allocates and initializes the device table
4. Manages I/O page tables
5. Processes IOMMU event logs

On PS5, all of these functions are performed by the hypervisor. The kernel has no direct access to IOMMU MMIO registers. Any attempt by the kernel to access IOMMU configuration space would be intercepted by the hypervisor (if those MSRs or MMIO regions are included in the MSRPM or NPT protections).

### IOMMU Hypercall Interface

The hypervisor exposes 7 dedicated IOMMU hypercalls:

| Number | Name | Function | Parameters |
|--------|------|----------|------------|
| 0x06 | IOMMU_SET_GUEST_BUFFERS | Register memory buffers for device DMA | Guest physical address, size, direction (read/write) |
| 0x07 | IOMMU_ENABLE_DEVICE | Enable IOMMU translation for a specific device | Device ID (BDF), domain ID, flags |
| 0x08 | IOMMU_BIND_PASID | Bind a PASID to a device/process | Device ID, PASID, page table root, attributes |
| 0x09 | IOMMU_UNBIND_PASID | Unbind a PASID from a device/process | Device ID, PASID |
| 0x0A | IOMMU_CHECK_CMD_COMPLETION | Check IOMMU command queue completion status | Completion token, timeout |
| 0x0B | IOMMU_CHECK_EVLOG_REGS | Read IOMMU event log register state | Event log head/tail pointers, overflow status |
| 0x0C | IOMMU_READ_DEVICE_TABLE | Read an entry from the IOMMU device table | Device ID, output buffer |

### IOMMU Page Table Structure (Unknowns)

The exact IOMMU page table structure used by the PS5 hypervisor is not publicly documented. Key unknowns:

- **Page sizes supported:** 4 KB, 2 MB, 1 GB? (standard AMD-Vi supports all three)
- **Number of page table levels:** 2, 3, or 4 levels?
- **PTE format:** Does it include custom bits (similar to xotext bit 58 in NPT PTEs)?
- **Domain allocation:** How many IOMMU domains exist? Are devices grouped by domain?
- **Translation granularity:** Per-device, per-function, or per-bus?

### Device Table Structure

The IOMMU device table has one entry per PCI device (max 32 bytes each). Each entry contains:

- **Translation enable bit:** Whether IOMMU translation is active for this device
- **Domain ID:** Which IOMMU domain the device belongs to
- **Page table root pointer:** Pointer to the I/O page table root
- **ATS enable:** Whether Address Translation Services are enabled for this device
- **PASID support:** Whether PASID-based translation is supported
- **Cache coherency settings:** How DMA accesses interact with CPU caches

### GPU IOMMU Configuration

The GPU (AMD RDNA 2-based Liverpool GPU integrated in the Oberon/Viola APU) is the most complex IOMMU client:

- **Multiple DMA engines:** Graphics command processor, compute queues, DMA engine, display controller
- **Command buffer submission:** Via libSceGnmDriver → kernel hypercalls → IOMMU mapping
- **Shared memory access:** 16 GB GDDR6 is shared between CPU and GPU — the IOMMU must enforce separation
- **GPU page tables:** The GPU has its own page table hierarchy managed by the kernel, but the IOMMU provides a second layer of I/O address translation

The GPU DMA path involves:
1. Userland (game/app) submits GPU command buffers via `sceGnmSubmitCommandBuffers` or `sceGnmSubmitDone` from `libSceGnmDriver`
2. The kernel driver validates and forwards the submission
3. Buffer addresses are translated through IOMMU (hypercall 0x06 for guest buffer registration)
4. GPU executes the command buffer, performing DMA reads/writes
5. All GPU memory accesses go through IOMMU translation

### Non-GPU Device IOMMU Configuration

| Device Class | IOMMU Domain | DMA Type | Notes |
|-------------|-------------|----------|-------|
| GPU (Liverpool) | Domain 0 (likely) | High-bandwidth, streaming | 448 GB/s GDDR6 shared memory |
| NVMe SSD | Separate domain | Block I/O | 825 GB PCIe 4.0 x4 |
| USB 3.1 (x3) | Separate domain | Packet-based | 10 Gbps per port |
| USB-C | Separate domain | Packet-based | 10 Gbps, includes DP Alt Mode |
| Wi-Fi (AX) | Separate domain | Packet-based | AK8M19DFR1 module |
| Bluetooth 5.1 | Shared with Wi-Fi | Low-bandwidth | 2.5 mW |
| Audio DSP | Separate domain | Streaming | Tempest Engine audio processing |
| Southbridge | Separate domain | Control/status | CXD90061GG, manages SPI, UART, JTAG |

## The GPU DMA Bypass Problem

### What the Exploit Does

Since PS5 System Software 6.00, the kernel .data section is protected against writes by the hypervisor. Any attempt by the CPU to write to kernel .data triggers an NPT violation VM exit, causing a kernel panic. However, the GPU's DMA engine can write to kernel .data pages without triggering this protection.

This is NOT a vulnerability in the traditional sense — it is a designed-in bypass created by the architectural gap between:
1. **CPU write protection:** Enforced by NPT (stage-2 page tables) at 4 KB granularity with hypervisor supervision
2. **GPU DMA write protection:** Enforced by IOMMU I/O page tables at a coarser granularity, configured through hypercalls

### Hypotheses for the Bypass

Several hypotheses explain why GPU DMA can bypass kernel .data write protection:

#### Hypothesis 1: IOMMU Page Table Granularity Gap
The IOMMU may support larger minimum page sizes (e.g., 2 MB or 1 GB) than NPT (4 KB). If kernel .data is mapped within a larger IOMMU page that also contains writable GPU buffers, the IOMMU cannot distinguish between legitimate GPU buffer writes and writes to kernel .data within the same page.

**Evidence:** AMD-Vi supports configurable page sizes. If the PS5 hypervisor configures the IOMMU with 2 MB pages for GPU domains, and kernel .data happens to share a 2 MB region with GPU-accessible memory, the IOMMU-level permission cannot separate the two.

**Counter-evidence:** Modern IOMMU implementations support multiple page sizes in a single page table (mixed page sizes). A competent hypervisor would use 4 KB pages for sensitive regions.

#### Hypothesis 2: GPU Command Buffer Address Validation Gap
The GPU driver (libSceGnmDriver) constructs PM4 command packets that may embed physical addresses directly. The IOMMU translates the GPU's DMA addresses, but if the GPU command processor can be tricked into issuing DMA to kernel physical addresses that are "accidentally" mapped in the GPU's IOMMU domain, the protection is bypassed.

**Evidence:** PM4 commands include WRITE_DATA, DMA_DATA, and other commands that take address parameters. If the attacker can craft a command buffer where a WRITE_DATA target address falls within kernel .data, the GPU will execute it.

#### Hypothesis 3: IOMMU Domain Overlap
The GPU may share an IOMMU domain with other devices that have broader memory access. If a single domain spans both GPU buffers and kernel memory, all devices in that domain inherit access to both.

#### Hypothesis 4: Missing IOMMU Mapping for Kernel .data
The kernel .data section may simply not be protected by IOMMU page tables at all. If the hypervisor only configures IOMMU mappings for explicitly registered guest buffers (via hypercall 0x06), and kernel .data is not registered as a guest buffer, the IOMMU may default to allowing access (identity mapping for unmapped addresses).

**Evidence:** AMD-Vi allows "pass-through" mode where devices have unrestricted memory access. If the hypervisor leaves the GPU in pass-through mode for performance reasons, no IOMMU protection exists for GPU DMA.

#### Hypothesis 5: GPU DMA Engine Bypasses IOMMU
The GPU's internal DMA engine may have a hardware path to memory that bypasses the IOMMU entirely. This could be a design feature for performance (GPU internal data movement) or a hardware bug.

**Evidence:** On many platforms, integrated GPUs share the same memory controller as the CPU and may have optimizations that bypass standard PCIe DMA paths.

#### Hypothesis 6: IOMMU TLBs Not Invalidated After Permission Change
If the hypervisor changes IOMMU page table permissions (e.g., write-protecting kernel .data), it must invalidate all IOTLB entries that cached the old permissions. If the invalidation is incomplete or racy, stale IOTLB entries may allow DMA writes that the current page tables would deny.

### Impact Assessment

| Hypothesis | Likelihood | Impact if True |
|------------|-----------|----------------|
| Page table granularity gap | Medium | Limit: affects devices with large IOMMU page sizes |
| Command buffer address validation | High | Exploitable: requires crafting specific PM4 commands |
| Domain overlap | Low | Design error: would be fixed if identified |
| Missing kernel .data IOMMU mapping | Medium | Config error: kernel .data lacks IOMMU protection |
| GPU DMA IOMMU bypass (hardware) | Low | Permanent: cannot be fixed in software |
| IOTLB invalidation race | Low | Timing-dependent: race condition |

**Most likely explanation:** A combination of Hypotheses 2 and 4. The GPU command buffer can embed target addresses that are not properly validated or restricted by the IOMMU configuration. The kernel .data section may lack explicit IOMMU page table entries, defaulting to permissive access for GPU DMA.

### Why This Matters

The GPU DMA bypass is currently the most powerful kernel exploitation primitive on PS5:
- It bypasses hypervisor-enforced kernel .data write protection
- It enables Debug Settings activation, security flag patching, and credential modification
- It works on ALL firmware >=6.00 (including 13.40)
- It requires no hypervisor exploit — it is an architectural gap

Understanding the bypass mechanism is critical for:
1. Determining if the bypass can be extended to kernel .text (would bypass XOM entirely)
2. Identifying similar bypasses in other DMA-capable devices (NVMe SSD, USB, networking)
3. Informing IOMMU hardening strategies for future firmware
4. Understanding whether the bypass has been fixed or hardened in FW 13.40+

## IOMMU Event Log Analysis

The IOMMU event log (accessible via hypercall 0x0B) records DMA faults. Event types include:

| Event Type | Meaning | Security Relevance |
|------------|---------|-------------------|
| ILLEGAL_DEV_TABLE_ENTRY | Device has invalid device table entry | Device enumeration attack detection |
| PAGE_FAULT | DMA to unmapped or protected page | Access violation detection — would fire on legitimate GPU DMA to kernel .data if IOMMU was correctly configured |
| INVALID_DEVICE_REQUEST | Malformed DMA transaction | Device malfunction or attack attempt |
| INVALID_ATS_REQUEST | ATS translation request from device | ATS spoofing attempt |
| IOTLB_INVALIDATE_ERROR | Error during IOTLB invalidation | Potentially exploitable race condition |

The event log is a critical data source for understanding the IOMMU bypass. If the GPU DMA copy exploit does NOT generate IOMMU page faults, the bypass is at the IOMMU configuration level (page table mapping issue). If it DOES generate faults but the GPU continues writing, the bypass is at the hardware level (GPU ignores IOMMU faults).

## Open Questions

### Architecture
- Q-CRIT-006: Does PS5 use AMD-Vi standard IOMMU or a custom SMMU implementation?
- Q-CRIT-007: IOMMU page table structure: page sizes, levels, PTE format
- Q-CRIT-008: Whether kernel .data has explicit IOMMU page table entries or relies on default/identity mapping
- Q-IMP-007: Number of IOMMU domains and device-to-domain assignment
- Q-IMP-008: Full register-level IOMMU configuration (MMIO base, capabilities, features enabled)

### GPU DMA Bypass
- Q-CRIT-009: Exact mechanism by which GPU DMA bypasses kernel .data write protection
- Q-CRIT-010: Whether the bypass can read kernel .text (bypassing XOM)
- Q-CRIT-011: Whether IOMMU event log records GPU DMA writes to kernel .data
- Q-IMP-009: Whether the bypass has been hardened or fixed in FW 13.40+
- Q-IMP-010: Whether other DMA devices (NVMe, USB, networking) have similar bypass capabilities

### Hypercall Interface
- Q-IMP-011: Complete parameter validation for each IOMMU hypercall
- Q-IMP-012: Race conditions in IOMMU command queue processing
- Q-IMP-013: Whether IOMMU hypercall handlers differ across firmware versions (regression targets)
- Q-MIN-002: Whether hypercall 0x0C (READ_DEVICE_TABLE) leaks hypervisor memory through device table entries

### ATS and PASID
- Q-IMP-014: Whether ATS is enabled for any PS5 PCIe devices
- Q-IMP-015: PASID usage: which devices use PASID-based translation
- Q-MIN-003: Whether ATS manipulation can bypass IOMMU checks

## References

### Specifications
- AMD I/O Virtualization Technology (IOMMU) Specification, Rev 3.10, Feb 2025 (48882-PUB)
- AMD64 Architecture Programmer's Manual, Volume 2: System Programming
- PCI Express Base Specification, ATS and PASID ECNs

### PSDevWiki
- https://www.psdevwiki.com/ps5/Hypervisor (IOMMU hypercall section)
- https://www.psdevwiki.com/ps5/Kernel (device list)
- https://www.psdevwiki.com/ps5/Vulnerabilities (GPU DMA copy section)
- https://www.psdevwiki.com/ps5/IOCTL (device IOCTL catalog)

### Related Research
- [[hypervisor]] — full hypervisor architecture, 17 hypercalls, NPT, xotext, GMET
- [[kernel]] — kernel syscall/IOCTL interface, device enumeration
- [[hardware_attack_surface]] — GDDR6 shared memory, GPU architecture, DMA attack surface
- [[attack_surface]] — entry point ranking, IOMMU as hypervisor attack surface
- [[mitigation_assessment]] — IOMMU/SMMU mitigation effectiveness rating

### OSDev
- https://wiki.osdev.org/AMD-Vi_IOMMU
