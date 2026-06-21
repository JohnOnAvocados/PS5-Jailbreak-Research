# Control Flow Integrity

## Source URL
https://clang.llvm.org/docs/ControlFlowIntegrity.html

## Domain
clang.llvm.org

## System Layer (choose one)
memory_protection

## Summary
Clang's CFI implementation provides a set of compiler-based schemes that abort the program upon detecting undefined behavior that could allow subversion of control flow. Schemes include virtual call checking (cfi-vcall), non-virtual member function call checking (cfi-nvcall), indirect function call checking (cfi-icall), bad cast checking (cfi-derived-cast, cfi-unrelated-cast), and member function pointer call checking (cfi-mfcall). Most schemes require link-time optimization (LTO) and static linking. Cross-DSO support exists experimentally.

## Key Concepts
- forward-edge CFI for virtual calls checks vptr dynamic type correctness
- bad cast checking prevents base-to-derived or void* casts to wrong dynamic type
- indirect function call checking (cfi-icall) validates function pointer type at call sites
- requires -flto for whole-program analysis and type identification
- LTO visibility must be hidden for classes to receive CFI checks
- cross-DSO mode extends CFI checks across shared library boundaries
- kcfi is an alternative scheme for low-level systems (kernels) that does not require LTO
- ignorelist via SanitizerSpecialCaseList relaxes checks for specific files, functions, or types

## Security Relevance
CFI enforces that control flow transfers follow the intended call graph, preventing attackers from hijacking indirect calls, virtual dispatches, or function pointers even after a memory corruption vulnerability is triggered. It is a critical mitigation for preserving control flow integrity in a trusted system.

## Relevance Tags
control flow integrity, cfi, clang, lto, virtual call protection, indirect call checking, compiler mitigation, forward-edge cfi
