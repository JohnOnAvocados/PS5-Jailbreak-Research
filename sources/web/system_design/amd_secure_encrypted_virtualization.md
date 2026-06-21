# AMD Secure Encrypted Virtualization

## Source URL
https://www.amd.com/en/developer/sev

## Domain
amd.com

## System Layer (choose one)
system_design

## Summary
AMD SEV (Secure Encrypted Virtualization) is a hardware memory encryption technology for AMD EPYC processors. SEV encrypts VM memory with per-VM keys transparent to the hypervisor. Successive generations added SEV-ES (Encrypted State) for register protection and SEV-SNP (Secure Nested Paging) for integrity and anti-replay protection against malicious hypervisors.

## Key Concepts
- SEV encrypts guest VM memory with AES-128/256 hardware encryption using dedicated on-die memory controller
- SEV-ES encrypts CPU register state when context-switching between guest and hypervisor
- SEV-SNP adds memory integrity protection via reverse map table, preventing hypervisor replay and remapping attacks
- Attestation via AMD Secure Processor (ASP) firmware-signed reports
- VM migration with encrypted state transfer between SEV-capable hosts
- Transparent to guest OS — no application code changes required

## Security Relevance
Provides the foundational hardware trust mechanism for confidential computing on AMD platforms. SEV's threat model assumes the hypervisor is untrusted — a critical property for trusted system design where cloud providers must be excluded from the guest's trusted computing base. Used by Google Cloud, Azure, and other confidential VM offerings.

## Relevance Tags
amd sev, secure encrypted virtualization, memory encryption, trusted execution, hardware security, snp, hypervisor isolation, confidential computing
