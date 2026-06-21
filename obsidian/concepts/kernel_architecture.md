# Kernel Architecture

## Concept Summary

The PS5 kernel is a heavily modified FreeBSD 11.0 derivative that serves as the core operating system layer running under hypervisor control. It manages all hardware resources — CPU, memory, GPU, storage, and I/O peripherals — while enforcing Sony's security model through multiple interconnected protection mechanisms. The kernel implements three distinct syscall vector structures to handle different binary formats: PS4 SELF for backward compatibility with PlayStation 4 executables, FreeBSD ELF64 for standard FreeBSD binaries, and Native SELF for native PS5 processes. This multi-format dispatch system is unique to the PS5 and reflects Sony's approach to maintaining cross-generation compatibility while evolving the platform.

Memory management is enforced through hardware security features including NX, SMAP, SMEP, UMIP, and AMD's execute-only memory support via the nda/xotext EFER bit. These are layered with Sony-specific mechanisms such as eXecute-Only Memory (XOM), which operates at both usermode and kernel levels, signed secure modules dispatched through the SceSbl authentication manager, and a Trusted Execution Environment running on the Platform Security Processor. XOM at the kernel level is backed by hypervisor nested page tables, creating a two-layer memory protection architecture where the kernel cannot simply clear its own XOM bits.

The kernel communicates with four co-processors that provide specialized hardware services. The AMD Platform Security Processor handles secure boot, key management, and cryptographic operations. The System Management Unit manages power, clock gating, and thermal monitoring. The Trusted Execution Environment on the PSP runs PlayReady SL3000 DRM and secure media paths. An ARM Cortex-A53 handles I/O co-processing and memory management offload. These co-processors are accessed through a device model exposed via the IOCTL syscall interface, with over 100 documented kernel device entries.

A critical architectural aspect is the kernel's position under hypervisor control — it runs as a single guest within the hypervisor's virtual machine partition. This means the kernel does not have full control over its own memory management: nested page tables at the hypervisor level provide second-layer address translation that the kernel cannot modify. The kernel enforces the security policy dictated by the hypervisor and secure loader boot chain, making it a powerful but constrained component in the overall platform security architecture.

## Role in System

The kernel sits below the hypervisor in the privilege hierarchy, implementing the operating system services that user-mode processes depend on — process management, virtual memory, file systems, device I/O, and networking — while being subject to hypervisor-enforced constraints on memory access, control register values, and IOMMU configuration. The hypervisor intercepts and filters writes to CR0, CR4, and EFER, preventing the kernel from disabling critical security features such as paging, SMAP, SMEP, and NX enforcement.

The kernel serves as the primary interface between user-mode code and both hardware and security services. All system calls, device operations, and security module requests flow through the kernel. It enforces capability-based sandboxing through Auth IDs and Program Authority IDs, manages the PlayStation File System namespace for sandboxed file access, and dispatches secure module operations through the SceSbl authentication manager using over 20 service ID categories. The kernel also manages the PFS file system with integrity-checked data, encryption via the Key Management System, and the serial flash device used for boot configuration storage.

## Connections

- [[hardware_architecture]]
- [[hypervisor_architecture]]
- [[security_model]]
- [[boot_chain]]
- [[system_architecture]]

## Security Relevance

- Syscall attack surface: PS5-specific syscalls beyond 0x180 lack documentation and compatibility constraints, representing the most likely kernel exploitation vectors — over a dozen distinct vulnerability classes have been publicly demonstrated across firmware versions
- XOM enforcement: kernel-level XOM protects code pages from read access, with kernel XOM backed by hypervisor nested page tables creating a chicken-and-egg problem where reverse engineering the hypervisor requires reading kernel text, but reading kernel text requires hypervisor compromise
- IOCTL interface: over 100 kernel device entries expose hardware and security services through structured IOCTL codes — TEE debug commands, manufacturing mode module loading, and NAND sector access IOCTLs are particularly high-value security research targets
- Secure module system: the SceSbl subsystem dispatches over 20 security service categories through service IDs from 0x80021000 through 0x80021018, providing a wide API surface for cryptographic, authentication, key management, and content protection operations
- Kernel patch protection: the kernel monitors its own code integrity for modifications, supplemented by hypervisor-enforced memory protections through nested page tables, making kernel-level exploitation and persistence challenging
- PUP update processing: firmware update decryption and verification involves multiple parsing steps (header decryption, segment decryption, watermark verification, additional signature verification) that could contain vulnerabilities

## Graph Reference
research/kernel/kernel.md
