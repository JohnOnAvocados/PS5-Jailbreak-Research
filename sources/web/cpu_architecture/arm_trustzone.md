# Arm TrustZone

## Source URL
https://developer.arm.com/ip-products/security-ip/trustzone

## Domain
developer.arm.com

## System Layer (choose one)
cpu_architecture

## Summary
Arm TrustZone is a hardware-enforced security technology integrated into Arm Cortex-A and Cortex-M processors. It partitions the CPU into two worlds: the Normal World (Rich OS) and the Secure World (trusted execution environment), using a bus-level signal (NS bit) to gate access to secure resources. TrustZone for Cortex-A provides full OS isolation for trusted applications; TrustZone for Armv8-M uses a unified Secure and Non-Secure address space with memory attribution units.

## Key Concepts
- Secure World / Normal World partitioning via NS (Non-Secure) bit
- Secure Monitor Call (SMC) as the gateway between worlds
- Bus-level isolation — AMBA bus signals propagate security state
- TrustZone Address Space Controller (TZASC) restricts DRAM regions
- TrustZone Memory Adapter (TZMA) for on-chip SRAM isolation
- Secure boot and trusted firmware chain
- TrustZone for Armv8-M adds Secure Attribution Units (SAU/IDAU)
- Trusted Execution Environment (TEE) on Secure World side

## Security Relevance
Arm TrustZone forms the foundational hardware isolation primitive for trusted execution in mobile, IoT, and embedded devices under a trusted system model. Compromise of TrustZone boundaries allows an attacker to read secure memory, extract cryptographic keys, and bypass secure boot.

## Relevance Tags
trustzone, arm, trusted execution environment, tee, hardware isolation, secure world, cortex-a, cortex-m
