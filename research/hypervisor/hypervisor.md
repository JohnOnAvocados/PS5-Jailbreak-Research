# PS5 Hypervisor Architecture

## Overview

The PS5 employs a custom hypervisor (HV) purpose-built by Sony to implement Virtualization-Based Security (VBS). This hypervisor is not derived from existing open-source projects such as Xen, KVM, or Hyper-V — it is a proprietary implementation designed specifically for the PlayStation 5's security and isolation requirements. Its primary role is to enforce kernel integrity protection by running the operating system as a guest virtual machine under hardware-assisted virtualization, making it the highest-privilege software layer on the main x86-64 cores.

The hypervisor sits above the kernel in the system privilege hierarchy. On firmware versions 2.70 and earlier, the hypervisor was compiled directly into the kernel binary as a single monolithic image. Starting with FW 3.00, Sony refactored this design: the hypervisor became a separately loaded component, and an additional boot stage called the Hypervisor Loader (codename "HyLonome") was introduced between the Secure Loader and the Hypervisor. This architectural change hardened the boot chain by adding an independently verified intermediate stage. The Secure Loader — running on the AMD Platform Security Processor (PSP) — is responsible for loading and verifying the hypervisor (and the hypervisor loader on FW >= 3.00), ensuring that only cryptographically signed hypervisor images can be executed.

The hypervisor virtualizes only a single guest environment — the GameOS (kernel and user space). Unlike server hypervisors that manage multiple independent VMs, the PS5 hypervisor uses a single-partition model where the entire operating system runs as one guest. The isolation boundary is therefore between the hypervisor layer and the kernel, not between multiple guest operating systems. This single-guest architecture simplifies the design while still providing strong security guarantees: even if the kernel is compromised, the hypervisor retains control over memory access, CPU control registers, and I/O memory management.

## Components

### Hypervisor Type and Provenance

- **Type:** Custom, proprietary hypervisor (not based on Xen, KVM, Hyper-V, or any known open-source hypervisor)
- **Origin:** Developed internally by Sony for the PS5
- **Underlying Technology:** AMD64 Secure Virtual Machine (SVM) extensions
- **SVM Features Used:**
  - Nested Page Tables (NPT) for second-level address translation (SLAT)
  - Guest Mode Execute Trap (GMET) to prevent code execution from incorrect privilege levels
  - Control Register (CR0, CR4) filtering and interception
  - Model-Specific Register (MSR) interception via MSR Protection Map (MSRPM)
  - EFER (Extended Feature Enable Register) bit masking
- **Distribution Model:**
  - FW <= 2.70: hypervisor code embedded in the kernel binary
  - FW >= 3.00: hypervisor loaded as a standalone component via the Hypervisor Loader
- **Codename Reference:** The hypervisor loader is named "HyLonome" (possibly "Hypervisor Loader — No ME"), suggesting an architectural decision to avoid or replace the AMD Management Engine (ME) for certain boot functions

### Partition Model

- **Number of Guest Partitions:** 1 (single guest: the GameOS)
- **Guest Composition:** The single guest partition encompasses the entire kernel and all user-mode processes
- **Partition Structure:**
  - No separation between kernel and user space at the hypervisor level — both run within the same VM
  - The kernel itself enforces user/kernel separation via traditional page tables, SMAP, SMEP, and UMIP
  - The hypervisor provides a second layer of defense through NPT and control register filtering
- **No Multi-Tenancy:** Unlike cloud hypervisors, the PS5 hypervisor is not designed to host multiple independent operating systems concurrently
- **Architectural Implication:** The hypervisor's attack surface is focused entirely on protecting itself and controlling the kernel's behavior, rather than mediating between competing guest OS instances

### Memory Isolation

The hypervisor enforces memory isolation through a combination of AMD SVM hardware features and custom extensions:

- **Nested Page Tables (NPT / SLAT):** The hypervisor maintains a second layer of page tables (stage-2 translation) that overlay the kernel's own page tables. This allows the hypervisor to control the physical memory that the guest can access, independently of the guest's own page table mappings. NPT enables the hypervisor to:
  - Restrict the guest to specific physical memory regions
  - Enforce access permissions (read, write, execute) at a granularity controlled by the hypervisor, not the kernel
  - Trap guest modifications to its own page tables without hypervisor intervention

- **Execute-Only Memory (xotext):** The PS5 hypervisor implements execute-only memory through a custom hardware extension developed in collaboration with AMD. Bit 58 in the NPT Page Table Entries (PTEs) marks pages as execute-only (xotext). This means:
  - Code pages marked xotext can be fetched for execution but cannot be read or written
  - This prevents information disclosure attacks where the kernel would read its own code pages to extract gadgets or data
  - The feature is controlled through EFER bit 16 (nda/xotext enable)
  - The hypervisor masks this EFER bit to ensure the guest cannot disable it

- **Guest Mode Execute Trap (GMET):** A hardware SVM feature that prevents code execution at the wrong privilege level within the guest. GMET ensures that:
  - User-mode code cannot execute kernel-mode pages and vice versa
  - Even if the kernel's own page tables are corrupted, the hardware traps invalid privilege-level execution at the hypervisor level

- **Control Register Filtering:** The hypervisor intercepts and filters writes to the guest's control registers:
  - **CR0 Filtered Bits:** PG (paging, bit 31), WP (write-protect, bit 16), NE (numeric error, bit 5), PE (protection enable, bit 0)
  - **CR4 Filtered Bits:** SMAP (bit 21), SMEP (bit 20), VME (virtual-8086 mode extensions, bit 0)
  - These filters prevent the kernel from disabling critical security features (e.g., the kernel cannot clear CR0.PG to disable paging, nor disable SMAP/SMEP)

- **EFER Masking:** The hypervisor masks writes to the Extended Feature Enable Register:
  - Bit 16: nda/xotext (execute-only memory)
  - Bit 12: SVME (SVM enable)
  - Bit 11: NXE (No-Execute enable)
  - The guest cannot disable NX protection or the xotext feature

- **MSR Protection Map (MSRPM):** The hypervisor uses an MSRPM bitmap to intercept accesses to specific Model-Specific Registers. Any MSR access by the guest that appears in the MSRPM causes a VM exit to the hypervisor, which can then emulate, filter, or deny the access

- **SMMU Integration:** The System Memory Management Unit (SMMU) provides I/O memory isolation. The hypervisor manages device access to physical memory through the IOMMU (I/O Memory Management Unit), ensuring that DMA-capable devices can only access memory regions explicitly assigned to them. This is analogous to stage-2 translation for devices

### Hypercall Interface

The hypervisor exposes a hypercall interface via the `vmmcall` instruction (the AMD SVM equivalent of Intel's `vmcall`). There are 17 defined hypercalls (0x00–0x10), with additional hypercalls added in FW >= 3.00:

| Number | Name | Description | FW |
|--------|------|-------------|-----|
| 0x00 | VMMCALL_HV_GET_MESSAGE_CONF | Query hypervisor message configuration | All |
| 0x01 | VMMCALL_HV_GET_MESSAGE_COUNT | Query the number of pending hypervisor messages | All |
| 0x02 | VMMCALL_HV_START_LOADING_SELF | Begin hypervisor self-loading sequence | All |
| 0x03 | VMMCALL_HV_FINISH_LOADING_SELF | Complete hypervisor self-loading sequence | All |
| 0x04 | VMMCALL_HV_SET_CPUID_PS4 | Set CPUID to PS4 compatibility mode | All |
| 0x05 | VMMCALL_HV_SET_CPUID_PPR | Set CPUID to production processor revision | All |
| 0x06 | VMMCALL_HV_IOMMU_SET_GUEST_BUFFERS | Configure IOMMU guest buffers | All |
| 0x07 | VMMCALL_HV_IOMMU_ENABLE_DEVICE | Enable IOMMU for a specific device | All |
| 0x08 | VMMCALL_HV_IOMMU_BIND_PASID | Bind a Process Address Space ID (PASID) | All |
| 0x09 | VMMCALL_HV_IOMMU_UNBIND_PASID | Unbind a Process Address Space ID | All |
| 0x0A | VMMCALL_HV_IOMMU_CHECK_CMD_COMPLETION | Check IOMMU command queue completion | All |
| 0x0B | VMMCALL_HV_IOMMU_CHECK_EVLOG_REGS | Check IOMMU event log registers | All |
| 0x0C | VMMCALL_HV_IOMMU_READ_DEVICE_TABLE | Read the IOMMU device table | All |
| 0x0D | VMMCALL_HV_GET_TMR_VIOLATION_ERROR | Get Timer violation error information | All |
| 0x0E | VMMCALL_HV_VMCLOSURE_INVOCATION | VMClosure invocation | >= 3.00 |
| 0x0F | VMMCALL_HV_STARTUP_MP | Start multi-processor (AP) boot | >= 3.00 |
| 0x10 | VMMCALL_HV_DISABLE_STARTUP_MP | Disable multi-processor startup | >= 3.00 |

**Hypercall Categories:**

- **Message Interface (0x00–0x01):** The kernel can query the hypervisor for message configuration and count, enabling asynchronous communication
- **Self-Loading (0x02–0x03):** Used during the boot process where the hypervisor manages its own initialization
- **CPUID Virtualization (0x04–0x05):** The hypervisor controls CPUID output, allowing PS4 backward compatibility via spoofed CPUID and the ability to set production processor revision identifiers
- **IOMMU Management (0x06–0x0C):** A significant portion of the hypercall interface — 7 of 17 calls — is dedicated to IOMMU operations, reflecting the architectural shift where IOMMU control moved from the kernel to the hypervisor
- **Error Handling (0x0D):** Timer violation error retrieval
- **VMClosure (0x0E):** The VMClosure mechanism (FW >= 3.00) allows the hypervisor to securely shut down or isolate the guest
- **MP Boot (0x0F–0x10):** Application Processor (AP) startup management was moved to the hypervisor in FW 3.00, further reducing kernel control over system initialization

### VM Entry/Exit

The hypervisor manages transitions between the guest (kernel/user mode) and the hypervisor itself via VM entry and VM exit events:

- **VM Entry:** The hypervisor enters the guest using AMD SVM's `vmrun` instruction. Before entry, the hypervisor configures:
  - The Virtual Machine Control Block (VMCB) with guest state (segment registers, control registers, MSRs)
  - Nested Page Tables for address translation
  - The MSRPM and I/O permission bitmap
  - Event injection settings for delivering interrupts and exceptions to the guest

- **VM Exit Conditions:** The hypervisor gains control when any of the following events occur:
  - **CPUID Instruction (VMEXIT_CPUID):** The hypervisor intercepts CPUID instructions to virtualize the processor identification. This is used for PS4 backward compatibility, where the hypervisor can report a PS4-compatible CPUID to PS4 applications running under the PS5 kernel
  - **RDPRU Instruction (VMEXIT_RDPRU):** The Read Processor Register User instruction is intercepted and injected with a General Protection Fault (#GP), preventing user-mode access to processor performance registers
  - **Control Register Writes:** Writes to CR0, CR4, and EFER cause VM exits when the modified bits are in the hypervisor's filter masks
  - **MSR Accesses:** MSR reads/writes that match the MSRPM cause VM exits for emulation or filtering
  - **NPT Violations:** Guest access to memory that violates the stage-2 page table permissions causes an NPT violation VM exit, allowing the hypervisor to enforce memory isolation
  - **IOMMU Operations:** Device-initiated DMA to disallowed memory regions trigger SMMU faults routed through the hypervisor
  - **HLT/INVD/INVLPG:** Certain privileged instructions can be configured to cause VM exits
  - **Hypercalls:** The `vmmcall` instruction causes a VM exit for hypercall servicing

- **VM Exit Handling Flow:**
  1. The CPU saves guest state into the VMCB and loads hypervisor state
  2. The hypervisor reads the VMEXIT code from the VMCB to determine the cause
  3. The hypervisor processes the event (emulation, filtering, forwarding to guest as injection)
  4. The hypervisor re-enters the guest via `vmrun`, possibly with modified state or injected events

- **Event Injection:** The hypervisor can inject interrupts, exceptions, and other events into the guest. For example, timer interrupts are injected as virtual interrupts, and the hypervisor can force the guest to handle exceptions such as #GP for intercepted RDPRU instructions

- **VMClosure (FW >= 3.00):** The VMClosure mechanism (invoked via hypercall 0x0E) provides a controlled path for terminating or isolating the guest VM, preventing a compromised kernel from remaining active

### Device Virtualization

The PS5 hypervisor does not perform traditional device emulation (e.g., emulating a network card or SATA controller for the guest). Instead, it focuses on device isolation through IOMMU management:

- **IOMMU Ownership:** The hypervisor has taken over IOMMU management from the kernel. On earlier AMD platforms, the operating system would configure the IOMMU directly. On the PS5, the kernel must request IOMMU operations through hypercalls (0x06–0x0C)

- **IOMMU Hypercall Functions:**
  - **Guest Buffer Registration (0x06):** The kernel informs the hypervisor of memory buffers that devices are allowed to DMA into/out of
  - **Device Enablement (0x07):** The kernel requests that a specific device be granted IOMMU access
  - **PASID Management (0x08, 0x09):** Process Address Space IDs allow devices to target specific process address spaces, enabling device-private memory access under hypervisor control
  - **Command Completion (0x0A):** The kernel polls the IOMMU command queue completion status
  - **Event Log (0x0B):** The kernel reads IOMMU event log registers for fault handling
  - **Device Table (0x0C):** The kernel reads the IOMMU device table to enumerate or validate device mappings

- **Devices Subject to IOMMU Control:** All DMA-capable peripherals are managed through the IOMMU, including the GPU, storage controllers, USB controllers, networking, and audio hardware. The hypervisor ensures that no device can DMA into hypervisor-private memory or into kernel memory without explicit authorization

- **Implication for Exploitation:** The movement of IOMMU control into the hypervisor means that even if an attacker achieves arbitrary kernel code execution, they cannot freely remap devices for DMA attacks without going through the hypercall interface. Any attempt to directly manipulate IOMMU hardware registers will be intercepted (if those MSRs or MMIO regions are protected by the hypervisor)

- **No Full Device Emulation:** The hypervisor does not emulate devices for the guest. Devices are passed through to the guest (with IOMMU protection) rather than being emulated. This is consistent with the single-guest model — there is no need for device sharing across multiple VMs

### Hypervisor Loader

Introduced in FW 3.00, the Hypervisor Loader (codename "HyLonome") is an additional verified boot stage that sits between the Secure Loader (IPL) and the Hypervisor:

- **Codename Analysis:** "HyLonome" is plausibly derived from "Hypervisor Loader — No ME," suggesting that Sony designed this component to replace or bypass the AMD Management Engine (ME) in the boot path for the hypervisor
- **Boot Chain Position:**
  - Pre-3.00: `Boot ROM → Secure Loader → Hypervisor → Kernel`
  - Post-3.00: `Boot ROM → Secure Loader → Hypervisor Loader → Hypervisor → Kernel`
- **Purpose:**
  - Provides an independently verified and measured boot stage
  - Decouples the hypervisor loading logic from both the Secure Loader and the hypervisor itself
  - Enables firmware update flexibility — the Secure Loader can remain stable while the hypervisor loader and hypervisor evolve independently
  - Adds additional integrity checking before the hypervisor begins execution
- **Security Hardening:** The introduction of a separate loader stage is a defense-in-depth measure. Even if the Secure Loader were compromised, the Hypervisor Loader provides an additional verification boundary before hypervisor code runs

## Relationships

- [[hardware_overview]] — The hypervisor virtualizes the AMD64 hardware platform, including CPU virtualization extensions (SVM), memory management units (SMMU/IOMMU), and system timing resources. It presents a controlled hardware interface to the kernel through filtered control registers, masked MSRs, and nested page tables
- [[kernel]] — The FreeBSD 11.0-based kernel runs as the primary (and only) guest of the hypervisor. The kernel's security features — NX, SMAP, SMEP, UMIP, and xotext — are enforced by the hypervisor at the stage-2 translation level, meaning the kernel cannot disable its own security protections. All kernel I/OMMU operations are mediated through hypercalls
- [[security_model]] — The hypervisor is the root of the PS5's security isolation model. It enforces the separation between privileged and unprivileged code by running the kernel as a guest. Hardware-backed features (NPT, GMET, xotext) provide isolation guarantees that cannot be bypassed by kernel-level exploits. The Secure Loader chain ensures only signed hypervisor images are loaded
- [[firmware]] — The hypervisor is loaded during the boot process by the Secure Loader (FW <= 2.70) or by the Hypervisor Loader (FW >= 3.00). The boot chain's cryptographic verification extends from Boot ROM through the Secure Loader to the hypervisor, ensuring firmware integrity at every stage

## Security Considerations

- **Highest-Privilege Software Layer:** The hypervisor operates at AMD SVM's most privileged level (VMX root equivalent, or hypervisor ring -1). It has full control over the CPU, memory, and devices. Compromise of the hypervisor would undermine all software security guarantees on the system. The hypervisor itself must be as small as possible to minimize its own attack surface

- **Hypercall Interface as Attack Surface:** The 17 (and growing) hypercalls represent the only intentional communication path from the guest to the hypervisor. Each hypercall is a potential vector:
  - **Parameter Validation:** Hypercall handlers must rigorously validate all parameters from the guest. A malformed IOMMU guest buffer descriptor or invalid PASID could trigger hypervisor memory corruption
  - **IOMMU Complexity:** With 7 of 17 hypercalls dedicated to IOMMU operations, this is the most complex and attack-rich area. Race conditions in IOMMU command queues, event log handling, and device table management are potential exploitation targets
  - **Self-Loading Hypercalls (0x02, 0x03):** These hypercalls manage hypervisor self-loading, an inherently sensitive operation. Firmware version differences in handling these calls could present exploitation opportunities
  - **VMClosure (0x0E):** The VMClosure mechanism (FW >= 3.00) introduces a state-transition path that must be carefully secured to prevent denial-of-service or privilege escalation

- **SMMU Isolation Boundaries:** The System Memory Management Unit enforces DMA isolation at the hardware level. Key security properties:
  - Devices can only access memory regions explicitly mapped by the hypervisor through the IOMMU
  - The hypervisor must ensure that IOMMU page tables cannot be tampered with by the guest
  - PCIe Address Translation Services (ATS) and PASID features introduce additional complexity: a compromised device could attempt to bypass IOMMU checks through ATS request manipulation
  - The event log mechanism (hypercall 0x0B) must report IOMMU faults accurately without leaking hypervisor memory layout information

- **VM Exit Handling Robustness:** Every VM exit is a transition from guest context to hypervisor context. The hypervisor must:
  - Preserve all guest state without leaking hypervisor data
  - Handle VM exits atomically with respect to concurrent events (interrupts, NMIs, SMIs)
  - Validate all state read from the VMCB before acting on it (a corrupted VMCB could trick the hypervisor)
  - Not introduce timing side-channels through asymmetric handling of VM exit causes

- **NPT and GMET as Security Boundaries:** The nested page tables and Guest Mode Execute Trap form the memory isolation foundation:
  - An NPT misconfiguration could expose hypervisor memory to the guest or allow a guest process to access kernel memory
  - The xotext bit (bit 58 in NPT PTEs) must be consistently applied to prevent read-implies-execute bypasses
  - GMET must correctly distinguish between guest user-mode and guest supervisor-mode to prevent privilege escalation within the VM

- **Downgrade Protection and Boot Chain Integrity:** The Secure Loader's revision nonce system ensures the hypervisor cannot be downgraded to an older, vulnerable version. Each firmware release updates the nonce, and the RSA4096 signature on the Secure Loader protects against tampering. The Hypervisor Loader (FW >= 3.00) adds an additional verification stage, raising the bar for boot-chain attacks

- **Firmware Version Differences as Attack Surface:** Architectural differences between FW <= 2.70 (hypervisor in kernel) and FW >= 3.00 (standalone hypervisor + HyLonome) mean that vulnerabilities in one version's boot model may not apply to the other. Researchers must consider both models separately, particularly around:
  - The mechanism by which the hypervisor sets up its own page tables and VMCB
  - The transition of AP boot from kernel control (pre-3.00) to hypervisor control (hypercalls 0x0F, 0x10 on >= 3.00)
  - The VMClosure feature only present on >= 3.00

- **xotext Hardware Collaboration:** The execute-only memory feature (bit 58 in NPT PTEs) is believed to be a custom extension co-developed with AMD specifically for the PS5. This represents a hardware-level security boundary not present in standard AMD64 platforms. Its implementation details — including how it interacts with instruction fetch, page walks, and speculative execution — are critical for understanding the PS5's unique security properties compared to standard x86-64 systems

## References

- https://www.psdevwiki.com/ps5/Hypervisor
- https://www.psdevwiki.com/ps5/Hypervisor_Loader
- https://www.psdevwiki.com/ps5/Kernel
- https://www.psdevwiki.com/ps5/Secure_Loader
- https://www.psdevwiki.com/ps5/Secure_Modules
