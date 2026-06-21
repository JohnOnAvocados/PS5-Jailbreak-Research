# Intel Architecture and Technology

## Source URL
https://www.intel.com/content/www/us/en/architecture-and-technology.html

## Domain
www.intel.com

## System Layer (choose one)
cpu_architecture

## Summary
Intel develops x86 and x86-64 CPU architectures including Core (P-core/E-core hybrid), Xeon (server/cloud), and Atom (low-power). Key architectural technologies include Hyper-Threading (SMT), Turbo Boost (dynamic frequency scaling), Intel 7/4/3/20A process nodes, and hybrid architecture with Performance-cores (P-cores) and Efficient-cores (E-cores) starting with Alder Lake (12th Gen). Security features include Intel SGX (enclave memory encryption), TDX (trusted domain extensions), and Intel ME (Management Engine).

## Key Concepts
- Hybrid architecture: P-core (Golden Cove/Raptor Cove/Lion Cove) + E-core (Gracemont/Crestmont/Skymont)
- Hyper-Threading: 2 threads per physical core
- Intel 7 (10nm Enhanced), Intel 4 (7nm), Intel 3, Intel 20A (2nm Angstrom-era)
- Intel SGX: application-level enclave memory encryption (deprecated on client)
- Intel TDX: VM-level trusted domain extensions for confidential computing
- Intel Management Engine (ME): separate microcontroller for platform management
- Total Memory Encryption (TME) for full memory bus encryption
- AVX-512/AMX: advanced vector and matrix extensions for AI

## Security Relevance
Intel's architectural security features define the trusted system model for the majority of x86 cloud and client computing. The ME/CSME is a proprietary coprocessor forming the hardware root of trust — analogous to AMD PSP. SGX and TDX provide confidential computing enclaves. Intel has had significant architectural vulnerabilities (Spectre, Meltdown, L1TF, MDS, Downfall) affecting the trusted system isolation model.

## Relevance Tags
intel, x86, x86-64, core, xeon, hyper-threading, hybrid architecture, sgx, tdx, management engine, aes-ni
