# Arm Architecture Reference Manual

## Source URL
https://developer.arm.com/documentation/ddi0487/latest

## Domain
developer.arm.com

## System Layer (choose one)
cpu_architecture

## Summary
The Arm Architecture Reference Manual (DDI0487) documents the Armv8-A and Armv9-A architecture profiles. It defines the instruction set, exception model, memory management, virtualization support, and security extensions including TrustZone, S-EL2 (Secure EL2 for Cortex-A), and the Realm Management Extension (RME). The manual covers AArch64 and AArch32 execution states, page table formats, and system register descriptions.

## Key Concepts
- AArch64 and AArch32 execution states
- Exception levels: EL0–EL3 with EL3 as Secure Monitor
- Virtualization: EL2 hypervisor stage-2 translation
- Secure EL2 (S-EL2) for firmware isolation
- Realm Management Extension (RME) for confidential computing
- Two-stage address translation (IPA to PA)
- Memory Management Unit (MMU) with 4KB/16KB/64KB granules
- Generic Interrupt Controller (GIC) architecture
- Self-hosted and external debug

## Security Relevance
The architectural reference manual defines the hardware security model implemented by all Armv8-A/v9-A processors. Its exception level hierarchy, stage-2 translation, and TrustZone/RME extensions form the foundation for OS-enforced isolation, hypervisor security, and confidential compute enclaves in the Arm trusted system model.

## Relevance Tags
armv8-a, armv9-a, aarch64, exception levels, trustzone, virtualization, rme, memory management, system registers
