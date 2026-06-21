# Stack Smashing Protection

## Source URL
https://www.gnu.org/software/libc/manual/html_node/Stack-Smashing-Protection.html

## Domain
www.gnu.org

## System Layer (choose one)
memory_protection

## Summary
Stack smashing protection (SSP) is a compiler-based mitigation that detects stack buffer overflows by placing a random canary value between local buffers and the saved return address. When a function returns, the canary is checked before the return address is used. If the canary has been overwritten, the program aborts. GNU libc integrates SSP through the `__stack_chk_fail` function, which is called when the canary check fails. The canary is initialized at process startup from a random source.

## Key Concepts
- stack canary (guard value) placed between local buffers and saved frame pointer/return address
- canary checked on function epilogue before return instruction executes
- canary value randomized per process at startup using secure random sources
- __stack_chk_fail function prints error message and aborts the program
- -fstack-protector enables SSP for functions with character arrays (buffers) of 8+ bytes
- -fstack-protector-strong extends coverage to functions with any local array or address-taken locals
- -fstack-protector-all enables protection for all functions regardless of buffer usage
- terminator canaries use NULL, CR, LF, and EOF bytes to prevent string-based overwrites

## Security Relevance
Stack canaries defend against stack buffer overflow attacks that attempt to overwrite the return address to hijack control flow. SSP is a foundational mitigation that, combined with NX and ASLR, forms the baseline of memory protection in modern operating systems and trusted execution environments.

## Relevance Tags
stack canary, ssp, buffer overflow protection, stack smashing, compiler mitigation, gcc, glibc, return address protection
