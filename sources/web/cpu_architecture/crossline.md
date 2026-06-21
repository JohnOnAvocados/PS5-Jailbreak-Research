# CROSSLINE

## Source URL
https://arxiv.org/abs/2008.00146

## Domain
arxiv.org

## System Layer (choose one)
cpu_architecture

## Summary
A 2020 paper by Li, Zhang, and Lin presenting CROSSLINE, a class of attacks against AMD Secure Encrypted Virtualization (SEV and SEV-ES). The attack exploits improper use of Address Space Identifiers (ASIDs) for controlling VM access to encrypted memory pages. CROSSLINE V1 allows decrypting victim page tables by changing the attacker VM's ASID to match the victim's ASID. CROSSLINE V2 constructs encryption/decryption oracles by executing instructions of the victim VM, enabling full memory decryption without physical access.

## Key Concepts
- ASID (Address Space Identifier) — used for TLB and memory access control in SEV
- CROSSLINE V1: ASID spoofing to decrypt victim page tables
- CROSSLINE V2: instruction oracle through ASID manipulation
- No physical access required — exploitable by a malicious VM on the same host
- Attack relies on SEV's failure to bind ASID to memory encryption key
- Works against SEV and SEV-ES (pre-SNP)
- Encrypted memory isolation broken through logical/cache side channels

## Security Relevance
CROSSLINE demonstrates that the logical isolation primitives (ASID) in pre-SNP SEV are insufficient for trusted VM memory protection. Unlike physical attacks (voltage glitching), this attack is remotely exploitable by a co-resident VM in a cloud environment, fundamentally breaking SEV's tenant isolation guarantees under the trusted system model.

## Relevance Tags
amd sev, crossline, asid, memory isolation, confidential computing, virtual machine, side channel, cache attack
