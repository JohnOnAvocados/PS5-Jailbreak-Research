# ARM Trusted Firmware-A

## Source URL
https://github.com/ARM-software/arm-trusted-firmware

## Domain
github.com

## System Layer (choose one)
firmware

## Summary
Trusted Firmware-A (TF-A) is a reference implementation of secure world software for Arm A-Profile architectures (Armv8-A and Armv7-A). It includes an Exception Level 3 (EL3) Secure Monitor and provides a starting point for productization of secure world boot and runtime firmware in AArch32 or AArch64 execution states. TF-A implements Arm interface standards including PSCI, TBBR-CLIENT, SMC Calling Convention, SCMI, and SDEI. The repository has over 19,500 commits, 2,200 stars, and is written primarily in C (91%) with Assembly, Makefile, and Python components.

## Key Concepts
- EL3 Secure Monitor implementation
- Power State Coordination Interface (PSCI)
- Trusted Board Boot Requirements (TBBR-CLIENT)
- SMC Calling Convention standard
- System Control and Management Interface (SCMI)
- Software Delegated Exception Interface (SDEI)
- Portable secure world firmware across Arm platforms
- AArch32 and AArch64 execution state support

## Security Relevance
Implements the highest privilege level (EL3) firmware for Arm processors, which serves as the root of trust for the entire platform. The secure monitor handles transitions between normal and secure worlds, and the trusted boot requirements ensure integrity of the boot chain from the first stage.

## Relevance Tags
arm, trusted firmware, el3, secure monitor, psci, tbbr, secure boot, aarch64
