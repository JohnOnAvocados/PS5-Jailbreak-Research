# Google Cloud Confidential Computing

## Source URL
https://cloud.google.com/confidential-computing

## Domain
cloud.google.com

## System Layer (choose one)
system_design

## Summary
Google Cloud's confidential computing portfolio providing encryption of data in use during processing. Includes Confidential VMs (using AMD SEV, Intel TDX), Confidential GKE Nodes, Confidential Space for multi-party collaboration, and Confidential Dataflow/Dataproc. Supports lift-and-shift migration with no code changes required.

## Key Concepts
- Confidential VMs with AMD SEV and Intel TDX for hardware-enforced memory encryption
- Confidential GKE Nodes for encrypted Kubernetes workload isolation
- Confidential Space for multi-party confidential collaboration and computation
- Confidential Dataflow and Dataproc for encrypted data pipeline processing
- Split-trust Encryption Tool for unified control of data at rest, in use, and in transit
- Shielded VM integration for rootkit and bootkit protection
- Attestation verification via Cloud Monitoring

## Security Relevance
Illustrates commercial deployment of hardware TEE technology (AMD SEV, Intel TDX) for protecting data in use. Confidential Space demonstrates trusted execution for multi-party computation, reducing trust in the cloud provider itself—a key pattern in zero-trust and confidential computing models.

## Relevance Tags
google cloud, confidential computing, confidential vm, amd sev, intel tdx, trusted execution environment, data in use, confidential space
