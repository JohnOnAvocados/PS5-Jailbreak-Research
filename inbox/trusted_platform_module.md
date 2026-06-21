# Trusted Platform Module

## Source URL
https://en.wikipedia.org/wiki/Trusted_Platform_Module

## Domain
en.wikipedia.org

## System Layer (choose one)
boot_chain

## Summary
A Trusted Platform Module (TPM) is a secure cryptoprocessor implementing ISO/IEC 11889 standard. TPM 1.2 was standardized in 2009; TPM 2.0 in 2015 (not backward compatible). TPM 2.0 is required for Windows 11. Common uses include verifying the boot process starts from trusted hardware/software and storing disk encryption keys. Provides hardware RNG, secure key generation, remote attestation, binding, sealed storage, and platform integrity via PCRs. Implementation types: discrete (dTPM), integrated (iTPM), firmware (fTPM), virtual (vTPM), and software TPM. Known security issues include cold boot attacks, TPM 2.0 SRTM design flaw (CVE-2018-6622), and ROCA vulnerability in Infineon TPMs (2017).

## Key Concepts
- secure cryptoprocessor standardized as ISO/IEC 11889
- TPM 1.2 (2009) vs TPM 2.0 (2015) - not backward compatible
- required for Windows 11
- provides: RNG, key generation, remote attestation, sealed storage
- Platform Configuration Registers (PCRs) for measured boot
- implementation types: dTPM, iTPM, fTPM, vTPM, software TPM
- discrete TPMs are most secure, FIPS 140-2 certified
- Intel fTPM, AMD fTPM, Qualcomm fTPM implementations exist
- known attacks: cold boot, CVE-2018-6622 (SRTM), ROCA vulnerability
- TPM 2.0 policy authorization supports AND/OR composition

## Security Relevance
TPM is the hardware root of trust used in measured boot chains. It anchors the trust model by securely storing measurements in PCRs that cannot be forged by software. Critical for Secure Boot, measured boot, disk encryption key protection, and remote attestation.

## Relevance Tags
tpm, trusted computing, secure cryptoprocessor, measured boot, platform integrity, hardware root of trust, bitlocker, windows 11
