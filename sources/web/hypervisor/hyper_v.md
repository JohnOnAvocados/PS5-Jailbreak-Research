# Hyper-V

## Source URL
https://www.microsoft.com/en-us/research/project/hyper-v/

## Domain
microsoft.com

## System Layer (choose one)
hypervisor

## Summary
Hyper-V is Microsoft's Type-1 hypervisor for Windows Server and Windows, first introduced with Windows Server 2008. It uses a microkernel architecture where the hypervisor runs directly on hardware with minimal code, and management runs in a privileged parent partition. Hyper-V supports hardware-assisted virtualization via Intel VT-x and AMD-V, provides virtual machine isolation, dynamic memory, live migration, Shielded VMs with BitLocker encryption, and Device Guard virtualization-based security (VBS). Research at Microsoft has explored hypervisor security, formal verification of the hypervisor, and side-channel mitigations.

## Key Concepts
- Type-1 (bare-metal) microkernel hypervisor architecture
- Parent partition (management OS) vs. child partitions (guests)
- Virtualization-Based Security (VBS)
- Shielded VMs with encryption
- Live migration and dynamic memory
- Hyper-V Enlightenments for paravirtualized I/O
- Hyper-V Code Integrity (HVCI)
- Formal verification research on hypervisor correctness

## Security Relevance
Hyper-V is the foundation of Windows security features including Credential Guard, Device Guard, and Windows Defender Application Guard. These features use VBS to isolate sensitive processes in a separate virtualized environment, protecting them from a compromised kernel. This makes Hyper-V directly relevant to trusted execution and isolation models in commodity OS security.

## Relevance Tags
hyper-v, microsoft, type-1-hypervisor, vbs, virtualization-based-security, shielded-vms, hvci, live-migration, windows-security
