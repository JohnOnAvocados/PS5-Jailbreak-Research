# System Architecture

## Concept Summary

The PS5 is a layered system built on defense-in-depth principles, combining custom hardware, a multi-stage firmware boot chain, a Type-1 hypervisor, a FreeBSD-derived kernel, and a sandboxed user-mode application runtime called Orbis OS. The hardware anchors a root of trust via an immutable Boot ROM in the AMD SoC, which cryptographically verifies each subsequent stage before execution proceeds. The hypervisor creates isolated virtual machine partitions for game operating systems, preventing compromised game code from accessing system memory or other game partitions.

The system software layer encompasses the RNPS (Rich Native Platform Shell) application framework, system services, and user-facing applications. RNPS applications (identified by NPXS40xxx Title IDs) handle everything from the home screen and settings to notifications, the PlayStation Store, and social features. These run in sandboxed environments with restricted file system access enforced through nullfs bind mounts. The WebKit-based modal browser provides embedded web rendering for system-integrated content but has JIT compilation disabled, forcing exploit developers toward alternative execution paths.

Firmware updates are distributed via PS5UPDATE.PUP files through a structured CDN, with version information published through an updatelist.xml system. The firmware has evolved through 13 major versions since launch, with each release typically introducing new features, security hardening, and updated anti-rollback mechanisms. PUP watermarking provides forensic traceability for leaked firmware, embedding identifying information about the authorized developer who downloaded it.

## Role in System

The system architecture defines the security boundaries and privilege domains that any exploit must traverse. Unlike PS4 where kernel access alone was sufficient for full control, the PS5's hypervisor isolation means homebrew enablement requires chaining exploits across multiple privilege layers: user-mode application, kernel system, and hypervisor. The hypervisor is the most valuable target because access at that level disables security monitoring across all guest VMs.

The system manages backwards compatibility through multiple mechanisms: a PS4 emulation layer running as a hypervisor guest, a PS2 emulator available via both the PS4 compatibility path and a native PS5 implementation (added around FW 9.00), and PS1 titles delivered through the Carbon Engine. Save data access is deliberately restricted — USB export is blocked to prevent manipulation attacks that were possible on PS3 and PS4.

## Connections

- [[hardware_architecture]]
- [[boot_chain]]
- [[kernel_architecture]]
- [[hypervisor_architecture]]
- [[security_model]]

## Security Relevance

- Hypervisor isolation means full compromise requires exploits across multiple privilege domains
- JIT-disabled WebKit forces exploit developers toward alternative execution paths (BD-J, mast1c0re, Lua)
- PUP watermarking provides forensic traceability for leaked firmware
- Encrypted SSD and blocked USB save data export prevent offline data extraction and manipulation

## Graph Reference

research/system_overview/system_overview.md
