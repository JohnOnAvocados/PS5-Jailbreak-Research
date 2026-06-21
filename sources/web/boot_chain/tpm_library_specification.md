# TPM Library Specification

## Source URL
https://trustedcomputinggroup.org/resource/tpm-library-specification/

## Domain
trustedcomputinggroup.org

## System Layer (choose one)
boot_chain

## Summary
The TPM Library Specification, maintained by the Trusted Computing Group (TCG), defines the standard for Trusted Platform Module (TPM) implementations. The current version is TPM 2.0 Library Specification (revision of November 2019). It is divided into four parts: Part 1 (Architecture), Part 2 (Structures), Part 3 (Commands), and Part 4 (Supporting Routines). TPM 2.0 was also standardized as ISO/IEC 11889:2015. The specification covers cryptographic primitives, key hierarchies, platform configuration registers (PCRs), remote attestation, sealed storage, and authorization policies. Microsoft maintains the official TCG reference implementation under BSD license on GitHub.

## Key Concepts
- TPM 2.0 Library Specification in four parts (Architecture, Structures, Commands, Supporting Routines)
- ISO/IEC 11889:2015 standard
- Platform Configuration Registers (PCRs) for measurement storage
- three hierarchies: platform, storage, and endorsement
- multiple key algorithms per hierarchy
- policy-based authorization (HMAC, password, PCR, locality, physical presence, signed, etc.)
- NVRAM with counter, bitmap, extend, and PIN capabilities
- official TCG reference implementation by Microsoft (open source, BSD license)
- not backward compatible with TPM 1.2

## Security Relevance
TPM provides the hardware root of trust for the boot chain via PCR-based measured boot and remote attestation. It seals cryptographic keys to specific platform states, forming the bedrock of trusted boot and disk encryption security.

## Relevance Tags
tpm, trusted computing, trusted computing group, hardware root of trust, platform configuration register, measured boot, remote attestation
