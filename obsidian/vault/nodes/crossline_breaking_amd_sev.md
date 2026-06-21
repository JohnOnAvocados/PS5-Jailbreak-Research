# CROSSLINE: Breaking "Security-by-Crash" based Memory Isolation in AMD SEV

## Source
inbox\crossline_breaking_amd_sev.md

## System Layer
hypervisor

## Summary
# CROSSLINE: Breaking "Security-by-Crash" based Memory Isolation in AMD SEV

## Source URL
https://arxiv.org/abs/2008.00146

## Domain
arxiv.org

## System Layer (choose one)
firmware

## Summary
This paper (Li, Zhang, Lin, 2020) presents CROSSLINE attacks against AMD Secure Encrypted Virtualization (SEV). The attack exploits SEV's improper use of Address Space Identifiers (ASIDs) for controlling VM access to encrypted memory pages, cache lines, and TLB entries. An attacker VM can change its ASID to impersonate a victim VM.

## Concepts
sev, memory, amd, crossline, isolation, asid, attack, computing, confidential, encrypted, arxiv, cache, decryption, demonstrated, exploitation

## Related Notes
- [[../nodes/amd_secure_encrypted_virtualization]]
- [[../nodes/amd_security]]
- [[../nodes/gbatemp_ps5_exploit_guide]]
- [[../nodes/google_cloud_confidential_computing]]
- [[../nodes/hypervisor]]
- [[../nodes/one_glitch_fault_injection_amd_sev]]
- [[../nodes/ps2_emulation]]
- [[../nodes/ps5_exploit_chains_overview]]
