# KVM

## Source URL
https://www.kernel.org/doc/html/latest/virt/kvm/

## Domain
kernel.org

## System Layer (choose one)
hypervisor

## Summary
KVM (Kernel-based Virtual Machine) is a Linux kernel module that enables full virtualization by turning the kernel into a Type-2 hypervisor. It supports x86, ARM, s390, PowerPC, and LoongArch architectures. The documentation covers the KVM API, device interfaces, nested virtualization, memory management (shadow MMU), secure encrypted virtualization (SEV), Intel TDX, halt polling, locking overview, and vCPU request handling.

## Key Concepts
- KVM API for vCPU and VM management
- ARM VGIC interrupt controller virtualization
- Secure Encrypted Virtualization (SEV) for AMD
- Intel Trust Domain Extensions (TDX)
- Nested VMX support
- KVM halt polling system
- Shadow MMU for x86
- Paravirtualized time and hypercalls
- s390 Ultravisor and Protected VMs
- PPC KVM paravirtual interface and magic page

## Security Relevance
KVM serves as the core virtualization layer within Linux, enabling isolation between guest VMs and the host. Features like SEV and TDX provide hardware-backed memory encryption to protect guest data from the host, which is critical for trusted execution environments. The hypervisor is part of the trusted computing base (TCB) in virtualization security models.

## Relevance Tags
kvm, linux, kernel, virtualization, type-2-hypervisor, memory-isolation, sev, tdx
