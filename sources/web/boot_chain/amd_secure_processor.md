# AMD Secure Processor

## Source URL
https://www.amd.com/en/technologies/secure-processor

## Domain
amd.com

## System Layer (choose one)
boot_chain

## Summary
The AMD Secure Processor (formerly Platform Security Processor or PSP) is a dedicated ARM Cortex-A5-based security subsystem integrated into AMD CPUs and APUs. It operates independently of the main x86 cores and runs its own firmware. It handles secure boot verification, cryptographic operations, Trusted Platform Module (fTPM) 2.0 functionality, and memory encryption (SME/SEV). The AMD Secure Processor verifies the signature of the UEFI BIOS before the x86 cores are released from reset, forming the hardware root of trust in AMD platforms. AMD fTPM is a firmware-based TPM implementation running within the Secure Processor.

## Key Concepts
- dedicated ARM Cortex-A5 security co-processor in AMD CPUs/APUs
- operates independently from main x86 cores
- verifies UEFI BIOS signature before x86 cores boot
- implements AMD fTPM 2.0 firmware-based TPM
- handles Secure Memory Encryption (SME) and Secure Encrypted Virtualization (SEV)
- runs proprietary firmware (AGESA)
- forms the hardware root of trust for AMD platforms
- provides secure boot chain verification

## Security Relevance
The AMD Secure Processor is the hardware root of trust in AMD-based systems. It enforces secure boot by verifying firmware signatures before the main CPU is released. Compromise of this component would break the entire boot chain trust model.

## Relevance Tags
amd, secure processor, psp, hardware root of trust, secure boot, ftpm, platform security, firmware verification
