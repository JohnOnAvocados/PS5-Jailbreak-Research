# One Glitch to Rule Them All: Fault Injection Attacks Against AMD's Secure Encrypted Virtualization

## Source URL
https://arxiv.org/abs/2108.04575

## Domain
arxiv.org

## System Layer (choose one)
firmware

## Summary
This paper (Buhren et al., 2021) presents voltage glitching attacks against the AMD Secure Processor (AMD-SP) on Zen 1, Zen 2, and Zen 3 microarchitectures. The attack allows execution of custom payloads on the AMD-SP, deployment of custom SEV firmware to decrypt VM memory, and extraction of endorsement keys to fake attestation reports or pose as valid migration targets. The authors also reverse-engineered the Versioned Chip Endorsement Key (VCEK) mechanism, showing how to derive valid VCEKs for arbitrary firmware versions.

## Key Concepts
- Voltage glitching attack on AMD Secure Processor
- Custom SEV firmware deployment
- SEV VM memory decryption via firmware compromise
- Endorsement key extraction (CEK, VCEK)
- Attestation report forgery
- VM migration impersonation
- VCEK mechanism reverse engineering
- Zen 1/2/3 cross-microarchitecture exploitation

## Security Relevance
Demonstrates a physical fault injection attack against the AMD Secure Processor firmware, which serves as the root of trust for SEV confidential computing. Compromising the AMD-SP allows bypassing all SEV security guarantees including memory encryption, attestation, and key management. Proves that SEV on current CPUs cannot adequately protect data from insider attackers with physical access.

## Relevance Tags
amd, sev, fault injection, voltage glitching, secure processor, attestation, confidential computing, hardware attack
