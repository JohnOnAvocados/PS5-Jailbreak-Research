# Secure Boot from Non-Volatile Memory for Programmable SoC Architectures

## Source URL
https://arxiv.org/abs/2004.09453

## Domain
arxiv.org

## System Layer (choose one)
boot_chain

## Summary
Academic paper (arXiv:2004.09453, April 2020) by Streit et al. proposing a secure boot methodology for FPGA-based Programmable System-on-Chip (PSoC) architectures. The approach uses the FPGA's reconfigurable logic to create a Trusted Memory-Interface Unit (TMIU) that verifies authenticity and integrity of boot configuration stored on encrypted SD cards or Flash memory. The boot process loads the TMIU hardware design first, which then authenticates and decrypts the NVM content before user application execution. Implemented and evaluated on a Xilinx Zynq PSoC.

## Key Concepts
- secure boot methodology for FPGA-based PSoC architectures
- Trusted Memory-Interface Unit (TMIU) as secure anchor point
- boot configuration stored on encrypted SD card or Flash (NVM)
- load-time verification: TMIU loaded first, then authenticates NVM content
- exploits FPGA reconfigurable logic for integrity/authenticity checks
- demonstrated on Xilinx Zynq PSoC platform
- evaluated for performance, power, and resource costs
- addresses threat of NVM manipulation at boot time

## Security Relevance
This paper proposes a secure boot implementation for reconfigurable SoC architectures, relevant to understanding how secure boot chains can be established on non-x86 programmable platforms (e.g., FPGA-based systems in diverse hardware ecosystems).

## Relevance Tags
secure boot, fpga, psoc, soc, non-volatile memory, trusted memory interface unit, xilinx zynq, embedded systems
