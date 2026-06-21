# Arm Platform Security Architecture

## Source URL
https://developer.arm.com/architectures/security-architectures/platform-security-architecture

## Domain
developer.arm.com

## System Layer (choose one)
cpu_architecture

## Summary
The Arm Platform Security Architecture (PSA) is a holistic security framework and certification scheme for IoT and embedded devices. It comprises threat modeling, security-by-design guidelines, hardware architecture requirements, and a trusted firmware specification (PSA Firmware Framework). PSA Certified provides independent lab testing across levels 1–3, covering secure boot, trusted storage, cryptography, and attestation.

## Key Concepts
- PSA Certified: Level 1 (analysis), Level 2 (hardware), Level 3 (hardware + software)
- PSA Firmware Framework (PSA-FF) for Secure Processing Environment (SPE)
- PSA Security Model: 100+ threat model categories
- Ten security goals: identification, attestation, secure storage, crypto, etc.
- Root of Trust (RoT) hardware requirements
- Trusted Subsystem (M-class) and Application RoT (A-class)
- Partition Manager for Secure Partition scheduling
- PSA Crypto API and PSA Attestation API

## Security Relevance
PSA defines a vendor-neutral trusted system model for Arm Cortex-M and Cortex-A IoT/embedded devices. It directly specifies hardware-software trust boundaries, root of trust requirements, and secure boot/isolation primitives required for a verifiable trusted computing base.

## Relevance Tags
psa, platform security architecture, iot security, trusted firmware, secure boot, attestation, root of trust, arm cortex-m
