# Kernel Self-Protection

## Source URL
https://www.kernel.org/doc/html/latest/security/self-protection.html

## Domain
kernel.org

## System Layer (choose one)
kernel

## Summary
Documentation on the Linux kernel's self-protection mechanisms including attack surface reduction, memory integrity, probabilistic defenses, and information exposure prevention. Covers CONFIG_STRICT_KERNEL_RWX, stack canaries, KASLR, seccomp, and module signing.

## Key Concepts
- Strict kernel memory permissions (CONFIG_STRICT_KERNEL_RWX, CONFIG_STRICT_MODULE_RWX)
- Kernel Address Space Layout Randomization (KASLR)
- Stack buffer overflow protections (CONFIG_STACKPROTECTOR)
- seccomp syscall filtering
- Kernel module signing (CONFIG_MODULE_SIG_FORCE)
- SMEP/SMAP/PXN/PAN hardware memory segregation
- Memory poisoning and initialization
- Function pointer read-only protection (__ro_after_init)
- Stack depth overflow protection (thread_info isolation)

## Security Relevance
Directly defines Linux kernel self-defense mechanisms against exploitation. Critical for understanding kernel-level attack surface reduction in a trusted system model where the kernel is the primary trusted computing base.

## Relevance Tags
linux, kernel, self-protection, memory protection, kaslr, stack canary, seccomp, module signing, attack surface reduction
