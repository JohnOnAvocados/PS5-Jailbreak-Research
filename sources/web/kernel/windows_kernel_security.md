# Windows Kernel Security

## Source URL
https://www.microsoft.com/en-us/research/project/windows-kernel-security/

## Domain
microsoft.com

## System Layer (choose one)
kernel

## Summary
Microsoft Research project page on Windows kernel security covering kernel defense mechanisms, vulnerability research, exploit mitigation, and secure system design. Windows kernel implements HVCI (Hypervisor-Protected Code Integrity), Kernel DPAPI, Secure Kernel (VSM), and PatchGuard.

## Key Concepts
- Hypervisor-Protected Code Integrity (HVCI / Device Guard)
- Virtual Secure Mode (VSM) and secure kernel
- Kernel PatchGuard (protection against kernel patching)
- Windows Defender System Guard (boot integrity)
- Kernel Address Space Layout Randomization (KASLR)
- Control Flow Guard (CFG) for kernel
- Arbitrary Code Guard (ACG) kernel enforcement
- Windows Driver Frameworks (WDF) security

## Security Relevance
Windows kernel security is foundational to understanding Microsoft's trusted platform model. VSM and HVCI represent hardware-enforced kernel isolation mechanisms relevant to trusted execution environments and hypervisor-based security.

## Relevance Tags
windows, kernel, security, hvci, vsm, patchguard, kaslr, cfg, hypervisor, microsoft research
