# CROSSLINE: Breaking "Security-by-Crash" based Memory Isolation in AMD SEV

## Source URL
https://arxiv.org/abs/2008.00146

## Domain
arxiv.org

## System Layer (choose one)
firmware

## Summary
This paper (Li, Zhang, Lin, 2020) presents CROSSLINE attacks against AMD Secure Encrypted Virtualization (SEV). The attack exploits SEV's improper use of Address Space Identifiers (ASIDs) for controlling VM access to encrypted memory pages, cache lines, and TLB entries. An attacker VM can change its ASID to impersonate a victim VM. CROSSLINE V1 decrypts victim page tables; CROSSLINE V2 constructs encryption/decryption oracles. Successfully demonstrated on SEV and SEV-ES processors.

## Key Concepts
- AMD SEV memory isolation vulnerability
- ASID reuse and impersonation attack
- Encrypted memory page decryption
- Cache line and TLB side-channel exploitation
- Security-by-crash design failure
- Cross-VM confidential computing breach
- SEV and SEV-ES demonstrated exploitation

## Security Relevance
Directly demonstrates a critical failure in AMD SEV's firmware-enforced memory isolation, which is designed to protect confidential computing workloads from untrusted hypervisors. The attack breaks the trust boundary between virtual machines that SEV firmware is supposed to enforce, compromising the confidentiality guarantees of the platform.

## Relevance Tags
amd, sev, memory isolation, side channel, confidential computing, virtualization security, asid
