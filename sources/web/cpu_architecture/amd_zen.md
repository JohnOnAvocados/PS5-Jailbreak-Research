# AMD Zen

## Source URL
https://en.wikipedia.org/wiki/AMD_Zen

## Domain
en.wikipedia.org

## System Layer (choose one)
cpu_architecture

## Summary
Zen is a family of x86-64 CPU microarchitectures from AMD, first launched in February 2017 with Ryzen 1000 series. Generations include Zen, Zen+, Zen 2, Zen 3, Zen 4, and Zen 5. Zen 2 introduced a chiplet-based multi-chip module (MCM) design with separate IO die and core chiplets on 7nm. Zen 3 unified the CCX into a single 8-core complex with 32MB L3. Zen 4 added DDR5/PCIe 5.0 on 5nm. Zen 5 uses 4nm/3nm. Zen 6 is planned for 2026-2027 on 3nm/2nm.

## Key Concepts
- Chiplet architecture with Infinity Fabric interconnect (Zen 2+)
- Core Complex (CCX): 4 cores sharing L3 cache (Zen 1/2); unified 8-core CCX (Zen 3+)
- Simultaneous multithreading (SMT) per core
- L1: 32KB data + 64KB instruction; L2: 512KB–1MB/core; L3: 8–32MB per CCX
- Fabrication nodes: 14nm (Zen) → 12nm (Zen+) → 7nm (Zen 2/3) → 5nm (Zen 4) → 4/3nm (Zen 5)
- Sinkclose vulnerability — System Management Mode (SMM) bypass affecting all Zen generations
- 3D V-Cache stacked L3 for gaming performance (Zen 3+/4)
- Zen 4c: high-density variant for cloud compute

## Security Relevance
Zen microarchitectures are used in the AMD Platform Security Processor and AMD Secure Encrypted Virtualization (SEV). The Sinkclose vulnerability (SMM bypass) demonstrated fundamental weaknesses in the trusted platform root of trust. The chiplet architecture introduces cross-die side channels that affect the trusted system model for confidential cloud computing on Epyc processors.

## Relevance Tags
amd, zen, x86-64, ryzen, epyc, chiplet, infinity fabric, sinkclose, smt, ccd, ccx
