# Memory Safety

## Source URL
https://en.wikipedia.org/wiki/Memory_safety

## Domain
en.wikipedia.org

## System Layer (choose one)
memory_protection

## Summary
Memory safety is the state of being protected from software bugs and security vulnerabilities involving memory access, such as buffer overflows, dangling pointers, and use-after-free. Microsoft and Google have reported that approximately 70% of all security vulnerabilities in their products stem from memory safety issues. Memory safety can be achieved through garbage collection, compile-time static analysis, runtime bounds checking, or type-safe languages like Rust that enforce ownership and borrowing rules.

## Key Concepts
- spatial memory errors: buffer overflow, buffer over-read, out-of-bounds access
- temporal memory errors: use-after-free, double free, wild pointers, invalid free, uninitialized variables
- spatiotemporal errors: struct tearing from non-atomic reads of multi-word data
- type-safe languages (Java, C#, Rust, Go) prevent memory errors through runtime checks or static analysis
- Rust enforces memory safety via ownership, borrowing, and lifetime rules without garbage collection
- AddressSanitizer (ASan) detects memory errors at runtime with ~2x slowdown
- Valgrind memcheck runs programs in a virtual machine detecting memory errors with ~40x slowdown
- fuzz testing combined with dynamic checkers effectively finds memory safety bugs

## Security Relevance
Memory safety is the most fundamental property of trusted system software. The majority of critical exploits (Heartbleed, sudo privilege escalation, Chromium RCE) originate from memory unsafety. Eliminating memory safety bugs through language choice, static analysis, or runtime monitoring is the highest-leverage security investment for any trusted computing base.

## Relevance Tags
memory safety, buffer overflow, use-after-free, dangling pointer, rust, addresssanitizer, spatial safety, temporal safety, type safety
