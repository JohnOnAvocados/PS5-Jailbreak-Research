# Secure Boot from Non-Volatile Memory for Programmable SoC Architectures

## Source URL
https://arxiv.org/abs/2004.09453

## Domain
arxiv.org

## System Layer (choose one)
hypervisor

## Summary
This 2020 paper by Streit et al. presents a secure boot methodology for FPGA-based Programmable System-on-Chip (PSoC) architectures that boot from untrusted Non-Volatile Memory (NVM). The FPGA serves as a secure anchor point by performing integrity and authenticity verifications before any user application loads. A Trusted Memory-Interface Unit (TMIU) verifies the authenticity of deployed NVM and then decrypts and validates integrity of its content. The approach was implemented and evaluated on a Xilinx Zynq PSoC.

## Key Concepts
- Secure boot from untrusted NVM for PSoC
- FPGA as hardware root of trust
- Trusted Memory-Interface Unit (TMIU)
- Integrity and authenticity verification pre-boot
- Encrypted SD card / Flash as NVM storage
- Xilinx Zynq PSoC implementation
- Boot-time chain of trust establishment

## Security Relevance
Secure boot is the foundational step in establishing a chain of trust for any trusted system. This paper addresses the challenge of booting from potentially compromised external storage, which is directly relevant to hypervisor integrity: if the hypervisor binary loaded at boot is compromised, all subsequent isolation guarantees fail.

## Relevance Tags
secure-boot, fpga, psoc, hardware-root-of-trust, chain-of-trust, memory-integrity, boot-security, academic-paper
