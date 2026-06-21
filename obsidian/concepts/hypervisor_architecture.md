# Hypervisor Architecture

## Concept Summary

The PS5 employs a custom, proprietary type-1 hypervisor purpose-built by Sony to implement virtualization-based security. It is not derived from Xen, KVM, or Hyper-V — it is a unique implementation designed specifically for the PlayStation 5's security and isolation requirements. Its primary role is to enforce kernel integrity protection by running the operating system as a guest virtual machine under hardware-assisted virtualization, making it the highest-privilege software layer on the main x86-64 cores. Unlike server hypervisors that manage multiple independent VMs, the PS5 hypervisor hosts a single guest partition — the GameOS encompassing the entire kernel and all user-mode processes. The isolation boundary is between the hypervisor layer and the kernel rather than between multiple operating systems.

The hypervisor leverages AMD64 Secure Virtual Machine extensions extensively. Nested page tables provide second-layer address translation, allowing the hypervisor to control physical memory access independently of the kernel's own page tables. Guest Mode Execute Trap prevents code execution at incorrect privilege levels within the guest. Control register filtering intercepts writes to CR0, CR4, and EFER, preventing the kernel from disabling critical security features. The MSR Protection Map bitmap intercepts accesses to specific Model-Specific Registers, with each intercepted access causing a VM exit to the hypervisor for emulation or filtering.

On firmware versions 3.00 and later, a significant architectural refactoring occurred: the hypervisor became a separately loaded component, and an additional boot stage called the Hypervisor Loader (codename HyLonome) was introduced between the Secure Loader and the hypervisor. On earlier firmware (2.70 and below), the hypervisor was compiled directly into the kernel binary as a single monolithic image. This change decoupled the hypervisor loading logic from both the Secure Loader and the hypervisor itself, enabling independent firmware evolution and adding an additional integrity verification boundary.

The hypervisor interface is exposed through 17 defined hypercalls invoked via the `vmmcall` instruction, with additional hypercalls added in firmware 3.00 and later. These cover message interface functions, self-loading sequences, CPUID virtualization for PS4 backward compatibility, IOMMU management as the largest category with 7 hypercalls, timer violation error handling, VMClosure for secure guest isolation and termination, and multi-processor boot control. The IOMMU management hypercalls reflect a key architectural decision: the hypervisor has taken over IOMMU ownership from the kernel, meaning all device DMA operations must be mediated through the hypercall interface.

## Role in System

The hypervisor operates at the most privileged software level on the main x86-64 cores, sitting above the kernel and below the hardware. It virtualizes only a single guest environment — the GameOS — and focuses on protecting itself and controlling the kernel's behavior rather than mediating between competing operating systems. The hypervisor enforces memory isolation through nested page tables, manages device access to physical memory through the SMMU and IOMMU, and controls all transitions between the guest and hypervisor through VM entry and exit events.

The hypervisor does not perform traditional device emulation such as emulating network or storage controllers. Instead, it focuses on device isolation through IOMMU management. All DMA-capable peripherals — GPU, storage controllers, USB, networking, audio — are managed through the IOMMU, ensuring that no device can DMA into hypervisor-private memory or into kernel memory without explicit authorization. This architectural choice means that even kernel-level code execution cannot freely remap devices for DMA attacks without going through the hypercall interface.

## Connections

- [[hardware_architecture]]
- [[kernel_architecture]]
- [[security_model]]
- [[boot_chain]]
- [[system_architecture]]
- [[iommu_architecture]]
- [[gpu_dma_exploitation]]

## Security Relevance

- Highest-privilege software layer: compromise of the hypervisor undermines all software security guarantees on the system — it represents the primary barrier between a kernel exploit and full system compromise, and hypervisor bugs are consequently the most sought-after vulnerabilities
- Hypercall attack surface: 17 hypercalls represent the only intentional communication path from guest to hypervisor — the IOMMU management hypercalls are the most complex area with potential for race conditions in command queues, event log handling, and parameter validation bugs from malformed guest buffer descriptors
- NPT and xotext hardware collaboration: the execute-only memory feature using bit 58 in NPT page table entries is believed to be a custom extension co-developed with AMD specifically for the PS5, providing a hardware-level security boundary not present on any standard AMD64 platform
- Firmware version differences: the architectural split between pre-3.00 (hypervisor embedded in kernel) and post-3.00 (standalone hypervisor with HyLonome loader) means vulnerabilities in one boot model may not apply to the other — researchers must consider both models separately, particularly around AP boot management and VMClosure
- SMMU isolation boundaries: the System Memory Management Unit enforces DMA isolation at the hardware level, but PCIe Address Translation Services and PASID features introduce complexity where a compromised device could attempt to bypass IOMMU checks

## Graph Reference
research/hypervisor/hypervisor.md
