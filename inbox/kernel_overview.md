# Kernel
## Source URL
https://www.psdevwiki.com/ps5/Kernel
## System Layer
kernel
## Summary
PS5 kernel is based on FreeBSD 11.0 (__FreeBSD_version 1100122). Supports NX bit, SMAP, SMEP, UMIP, and nda/xotext (EFER bit 16). Contains three sysvec structs: PS4 SELF (backward compatibility), FreeBSD ELF64 (standard, normally unused), and Native SELF (PS5 processes).
## Key Concepts
- FreeBSD 11.0 base (__FreeBSD_version: 1100122)
- NX (No-Execute) bit support
- SMAP (Supervisor Mode Access Prevention)
- SMEP (Supervisor Mode Execution Prevention)
- UMIP (User Mode Instruction Prevention)
- nda/xotext: execute-only memory (EFER bit 16)
- Three sysvec structs: PS4 SELF, FreeBSD ELF64, Native SELF
- PS4 backward compatibility via PS4 SELF sysvec
## System Role
Core operating system kernel
