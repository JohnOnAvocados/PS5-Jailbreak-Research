# AMD Secure Encrypted Virtualization

## Source URL
https://www.amd.com/en/technologies/secure-encrypted-virtualization

## Domain
www.amd.com

## System Layer (choose one)
cpu_architecture

## Summary
AMD Secure Encrypted Virtualization (SEV) is a hardware memory encryption feature for AMD Epyc processors that encrypts virtual machine memory transparently. Each VM receives a unique AES-256 encryption key managed by the AMD Secure Processor. SEV-ES (Encrypted State) additionally encrypts CPU register state on VM exits. SEV-SNP (Secure Nested Paging) adds integrity protection against malicious hypervisor memory remapping. SEV is designed to protect tenant data from the hypervisor in cloud environments.

## Key Concepts
- AES-256 hardware encryption engine integrated into memory controller
- Per-VM unique encryption key, invisible to hypervisor
- SEV-ES: register state encryption on VM exit (prevents register injection)
- SEV-SNP: reverse-mapping table prevents replay and remapping attacks
- Attestation: signed chip endorsement keys (CEK, VCEK) prove firmware version
- AMD Secure Processor (PSP) manages key generation and firmware loading
- Transparent to guest OS — no software modification needed in basic SEV
- Nation state level classification (DoD IL4+ certified on Milan)

## Security Relevance
SEV is AMD's primary confidential computing technology for cloud trusted systems. Its security model relies entirely on the AMD Secure Processor (PSP) for key management and firmware integrity. Academic attacks (Buhren et al. — voltage glitching; Li et al. — CROSSLINE ASID attacks) have demonstrated SEV/SEV-ES/SEV-SNP weaknesses, including key extraction and memory decryption, undermining the trusted system guarantees for VM isolation in multi-tenant clouds.

## Relevance Tags
sev, sev-es, sev-snp, amd, confidential computing, memory encryption, attestation, trusted execution, virtual machine isolation
