# AMD Security

## Source URL
https://www.amd.com/en/security

## Domain
amd.com

## System Layer (choose one)
firmware

## Summary
AMD's security portal provides information on platform security features including AMD Secure Processor (AMD-SP), Secure Encrypted Virtualization (SEV), Secure Memory Encryption (SME), and Platform Secure Boot. The AMD Secure Processor is a dedicated ARM Cortex-A5-based security processor that manages boot, encryption keys, and attestation. AMD SEV provides encrypted VM memory for confidential computing. The portal also publishes security advisory bulletins, vulnerability disclosures, and mitigation guidance for AMD products.

## Key Concepts
- AMD Secure Processor (AMD-SP) architecture
- Secure Encrypted Virtualization (SEV, SEV-ES, SEV-SNP)
- Secure Memory Encryption (SME)
- Platform Secure Boot implementation
- AMD firmware Trusted Platform Module (fTPM)
- AMD Platform Security Processor (PSP)
- Confidential computing with encrypted VM memory
- Security advisory and vulnerability disclosure program

## Security Relevance
AMD's firmware security architecture defines the root of trust for AMD-based systems. The AMD-SP/PSP operates as an independent security processor that initializes the system and manages encryption keys, making it the central trust anchor. SEV/SEV-SNP provides confidential computing guarantees. Vulnerabilities in AMD-SP firmware (e.g., CROSSLINE, voltage glitching attacks) directly compromise platform trust.

## Relevance Tags
amd, secure processor, psp, sev, sev-snp, platform security, secure boot, confidential computing
