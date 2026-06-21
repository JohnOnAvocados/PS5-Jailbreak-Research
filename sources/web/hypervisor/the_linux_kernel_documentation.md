# The Linux Kernel Documentation

## Source URL
https://docs.kernel.org/

## Domain
docs.kernel.org

## System Layer (choose one)
hypervisor

## Summary
docs.kernel.org is the main documentation portal for the Linux kernel. It hosts all official kernel documentation in reStructuredText format, including the Virtualization Support section covering KVM and Xen. Key virtualization-related documentation includes the KVM API reference, ARM pKVM documentation, x86 virtualization (SEV, TDX, nested VMX), s390 Protected VMs, and halt polling tuning. The site also documents kernel development processes, internal APIs, and architecture-specific guides.

## Key Concepts
- KVM API complete documentation
- ARM Protected KVM (pKVM) architecture
- AMD Secure Encrypted Virtualization (SEV)
- Intel Trust Domain Extensions (TDX)
- Nested virtualization (VMX) documentation
- s390 Ultravisor and Protected Virtualization
- KVM halt polling and locking
- Virtualization subsystem maintainer guides

## Security Relevance
docs.kernel.org provides the authoritative documentation for Linux kernel virtualization security features. The pKVM documentation describes how the kernel protects guest VMs from a compromised host OS. SEV and TDX documentation detail hardware-backed memory encryption for trusted guest execution. This is essential reference material for understanding the Linux KVM TCB.

## Relevance Tags
linux-kernel, documentation, kvm-api, pkvm, sev, tdx, nested-virtualization, kernel-development, virtualization-security
