# XNU Kernel Source

## Source URL
https://opensource.apple.com/source/xnu/

## Domain
opensource.apple.com

## System Layer (choose one)
kernel

## Summary
Apple's open-source XNU (X is Not Unix) kernel source code repository. XNU is a hybrid kernel combining the Mach microkernel (IPC, VM) with a FreeBSD-derived BSD layer (process model, networking, POSIX) and an IOKit C++ driver framework.

## Key Concepts
- Hybrid kernel architecture (Mach + BSD + IOKit)
- Mach message-based IPC
- BSD system call layer
- IOKit C++ object-oriented driver framework
- Kernel extensions (kext) loadable modules
- arm64 architecture support (Apple Silicon)
- Kernel ASLR and code signing enforcement
- KASAN (Kernel Address Sanitizer)

## Security Relevance
XNU is the kernel of iOS/iPadOS/tvOS/watchOS/macOS. Understanding XNU internals is critical for iOS security research, jailbreak development, and analyzing Apple's trusted execution environment.

## Relevance Tags
xnu, apple, kernel, mach, ios, macos, ipc, iokit, kext, arm64, open source
