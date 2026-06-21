# Address Space Layout Randomization

## Source URL
https://en.wikipedia.org/wiki/Address_space_layout_randomization

## Domain
en.wikipedia.org

## System Layer (choose one)
memory_protection

## Summary
ASLR is a computer security technique that randomly arranges the address space positions of key data areas of a process, including the executable base, stack, heap, and libraries, to prevent attackers from reliably redirecting code execution to exploited functions in memory. First implemented by the PaX project for Linux in 2001, ASLR became mainstream with OpenBSD 3.4 in 2003. When applied to the kernel it is called KASLR.

## Key Concepts
- randomized address space positions for stack, heap, libraries, and executable base
- entropy bits determine the probability of successful address guessing by an attacker
- position-independent executables (PIE) enable randomization of the main executable base address
- KASLR randomizes kernel code placement at boot time
- library load order randomization provides limited additional entropy
- brute force attacks against low-entropy ASLR can succeed in minutes on 32-bit systems
- side-channel attacks via branch target buffer or MMU page table walking can leak randomized addresses
- offset2lib technique exploits fixed offset between PIE executable and library regions

## Security Relevance
ASLR is a probabilistic memory protection mitigation that raises the bar for memory corruption exploitation. It complements NX bits and stack canaries by forcing attackers to leak or guess addresses before redirecting control flow. Part of the defense-in-depth strategy for trusted computing bases.

## Relevance Tags
aslr, kaslr, address randomization, memory protection, exploitation mitigation, control flow integrity, position-independent executable
