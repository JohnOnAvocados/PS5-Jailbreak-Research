# Security Model

## Concept Summary

The PlayStation 5 employs a deeply layered security architecture spanning hardware, firmware, hypervisor, kernel, and usermode. Each layer cryptographically verifies and enforces trust in the layer above before surrendering control. The boot chain originates in immutable on-chip ROM embedded within the AMD Platform Security Processor, a dedicated ARM-based cryptoprocessor isolated from the main x86 CPU cores. The PSP validates and loads the Secure Loader IPL from a Winbond serial flash chip, which in turn authenticates the hypervisor, the hypervisor loader, the kernel, and all subsequent system modules using RSA-4096 signatures, SHA-256 hashes, and AES-CBC decryption. Compromise of any given security layer requires defeating every layer beneath it, creating a root-of-trust hierarchy.

The security model is built on a multi-faceted authentication system that categorizes code by privilege level. Auth IDs, 64-bit identifiers with privilege-encoding prefixes, determine what resources each process can access and what security policies apply. Program Authority IDs at 64-bit values assigned at process creation define the security domain for mandatory access control enforcement. Code is distributed in the SELF binary format, which embeds cryptographic signatures, key identifiers, and metadata that the SceSbl authentication manager verifies before loading. The PS5 inherits architectural concepts from the PS4 — including the passcode system, portability keys, Keystone trust anchor, and trophy keys — but introduces significant hardening including hypervisor-backed XOM, revision nonces for downgrade protection, and individually sandboxed secure modules.

A comprehensive cryptographic key hierarchy covers boot authentication, content protection, DRM, peripheral pairing, and debug access. ROM keys are embedded in hardware at manufacturing time and accessible only to the PSP. Key rings managed by the PSP contain keys for various boot stages and services. Many keys are shared with the PS4 for cross-generation compatibility — the trophy key set, portability EncDec master keys, kernel NID suffix, and passcode system are all identical between generations, creating a potential cross-platform attack surface where PS4 ecosystem leaks directly impact PS5 security.

The AMD Zen 2 CPU provides hardware security features that the PS5 leverages extensively: the PSP for isolated trusted execution with its own memory and execution environment, nested page tables for hypervisor-backed memory isolation, Trusted Memory Regions for encrypted memory compartments, and the AMD Secure Technology framework. Despite this formidable defense-in-depth, the platform has been compromised at every layer through software exploits targeting race conditions, use-after-free vulnerabilities, integer overflows, stack buffer mismanagement, and speculative execution side channels across 12 distinct kernel exploit classes, multiple hypervisor bugs, and ongoing browser-engine attack surface.

## Role in System

The security model is woven into every layer of the PS5 architecture. At the hardware level, the PSP serves as the immutable root of trust, controlling OTP fuses, secure key rings, and initial boot verification with revision nonces that enforce downgrade protection at the hardware level. The hypervisor enforces memory isolation through nested page tables and controls the IOMMU for device DMA protection, providing the primary barrier between kernel-level compromise and full system control. The kernel implements process-level access control through Auth IDs and PAIDs, manages XOM page table entries for usermode and kernel code, and dispatches secure module operations through the SceSbl subsystem.

The interaction between layers is the critical architectural feature: the kernel cannot disable its own security protections because they are independently enforced by the hypervisor through stage-2 page tables. The hypervisor cannot be modified without cryptographic signatures verified by the PSP. Secure modules are compartmentalized by service ID, so compromise of one module does not automatically grant access to others. This creates a defense-in-depth architecture where no single vulnerability provides complete system compromise — an attacker must chain exploits across multiple layers to achieve full control.

## Connections

- [[hardware_architecture]]
- [[boot_chain]]
- [[secure_boot]]
- [[kernel_architecture]]
- [[hypervisor_architecture]]
- [[system_architecture]]
- [[y2jb_sandbox_escape]]
- [[mast1c0re_jit_pipeline]]
- [[syscall_catalog]]

## Security Relevance

- Layered root of trust: the PSP boot ROM through Secure Loader through hypervisor through kernel chain ensures each stage cryptographically verifies the next, with revision nonces providing hardware-enforced downgrade prevention that survives flash content manipulation
- XOM and nested paging synergy: kernel XOM enforced through hypervisor-backed nested page tables creates the strongest software protection on the platform — bypass requires either a hypervisor-level exploit or a hardware attack, making it the primary obstacle to full system compromise
- Cross-generation key sharing vulnerability: trophy keys, portability EncDec keys, kernel NID suffix, and passcode system are identical between PS4 and PS5, meaning any key leak from the PS4 ecosystem creates a direct vulnerability in PS5 security
- Vulnerability landscape spans every layer: kernel layer has been most targeted with 12 distinct exploit classes; hypervisor bugs remain confined to firmware 6.02 and earlier; browser-engine exploits (WebKit, V8, SpiderMonkey) and the PS2 emulator JIT mast1c0re family provide usermode entry points; AMD Zen 2 speculative execution vulnerabilities (ZenBleed, Inception, Retbleed, EntrySign) are fundamentally unpatcheable hardware issues
- Secure module compartmentalization: over 20 service IDs from 0x80021000 through 0x80021018 isolate cryptographic, authentication, and content protection services into individually sandboxed executables, limiting the blast radius of any single module compromise
- Manufacturing and debug control: the CP Box hardware accessory and passcode system restrict debug capabilities to authorized developers in physical possession of specific hardware, making TestKit exploitation dependent on hardware access

## Graph Reference
research/security_model/security_model.md
