# XOM (eXecute Only Memory)

## Source URL
https://www.psdevwiki.com/ps5/XOM

## System Layer
Security / Memory Protection

## Summary
eXecute Only Memory (XOM) is a mitigation against reverse engineering that prevents read accesses to certain memory regions via page tables. The PS5 is one of the only x86-based systems utilizing it (pioneered by ARM).

## Key Concepts

### Operation
- When a memory read is processed by the CPU, the Page Table Entry (PTE) is checked for the accessed address range
- If the XOM bit is set in the PTE, an exception is raised
- The exception is handled by the Hypervisor
- On an uncompromised hypervisor, this results in a kernel panic

### Usermode XOM
- Enforced on PS5 titles and system applications
- Prevents dumping usermode modules without a kernel exploit
- With kernel read/write access, usermode XOM can be disabled by flipping the bit on usermode PTEs
- Requires flushing the Translation Lookaside Buffers (TLBs) for changes to take effect

### Kernel XOM
- PS5 kernel uses XOM to protect its own .text pages
- Disabling kernel XOM likely requires compromising the hypervisor or a hardware attack
- Page tables are shadowed with nested paging (hypervisor-level)
- Presents a chicken-and-egg problem: hypervisor compromise is difficult without kernel RE, but kernel RE requires XOM bypass

## System Role
XOM provides strong protection against code dumping and static RE of both usermode and kernel modules. Kernel XOM is backed by hypervisor-enforced nested page tables, making it significantly harder to bypass than usermode XOM.
