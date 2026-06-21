# One Glitch to Rule Them All

## Source URL
https://arxiv.org/abs/2108.04575

## Domain
arxiv.org

## System Layer (choose one)
cpu_architecture

## Summary
A 2021 paper by Buhren, Jacob, Krachenfels, and Seifert demonstrating voltage glitching attacks against the AMD Secure Processor (AMD-SP) across Zen 1, Zen 2, and Zen 3 microarchitectures. The attack executes custom payloads on the AMD-SP, allowing full SEV VM memory decryption and extraction of endorsement keys (CEK, VCEK). The authors reverse-engineered the Versioned Chip Endorsement Key (VCEK) mechanism, showing how to forge attestation reports for arbitrary firmware versions — enabling VM migration impersonation without physical access to the target host.

## Key Concepts
- Voltage glitching on AMD-SP supply to bypass firmware signature verification
- Custom SEV firmware deployment on AMD-SP decrypts VM memory
- Endorsement key extraction (CEK/VCEK) enables fake attestation reports
- VCEK derivation reverse-engineered — forgeable for arbitrary firmware versions
- Affects all microarchitectures supporting SEV: Zen 1, Zen 2, Zen 3
- Insider attacker model: rogue cloud administrator with physical access
- No countermeasure on current hardware — requires microarchitectural fix to AMD-SP

## Security Relevance
This attack critically undermines AMD SEV's trusted system model for cloud confidential computing. Physical fault injection bypasses the SEV root of trust (AMD-SP), proving that current hardware cannot protect tenant data from malicious cloud insiders with physical access. The key extraction breaks attestation guarantees critical for establishing trust in remote platforms.

## Relevance Tags
amd sev, voltage glitching, fault injection, amd secure processor, attestation, confidential computing, vcek, hardware attack
