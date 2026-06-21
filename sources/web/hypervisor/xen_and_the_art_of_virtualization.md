# Xen and the Art of Virtualization

## Source URL
https://www.cl.cam.ac.uk/research/srg/netos/papers/2003-xensosp.pdf

## Domain
cl.cam.ac.uk

## System Layer (choose one)
hypervisor

## Summary
This seminal 2003 SOSP paper by Barham et al. presents the design and implementation of the Xen hypervisor. Xen is a Type-1 (bare-metal) hypervisor that supports paravirtualization, requiring modified guest OSes for performance. It achieves near-native performance by exposing a virtual machine abstraction that is similar to the underlying hardware but avoids costly privileged instruction emulation. The paper describes the CPU scheduling, memory management, and I/O virtualization architecture of Xen, demonstrating performance within 1-8% of native for most workloads.

## Key Concepts
- Paravirtualization vs. full virtualization
- Hypervisor ABI for guest OS interaction
- Domain 0 (privileged control domain) architecture
- Round-robin CPU scheduler for VCPUs
- Page-table virtualization via hypervisor-managed PTEs
- Split device driver model (frontend/backend)
- Zero-copy I/O via grant tables
- Near-native performance benchmarks

## Security Relevance
This paper established the foundational architecture for modern Type-1 hypervisors, including the separation between privileged control domains (Dom0) and unprivileged guest domains (DomU). This separation model is directly relevant to trusted system design, where the hypervisor acts as the root of trust and enforces memory/device isolation.

## Relevance Tags
xen, type-1-hypervisor, paravirtualization, sosp, academic-paper, isolation, domain-separation, split-driver
