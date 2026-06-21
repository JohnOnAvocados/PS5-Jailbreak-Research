# Kernel Syscall Catalog

## Concept Summary

The PS5 kernel is a heavily modified FreeBSD 11.0 derivative with 500+ syscalls organized across five ranges: standard BSD (0x00-0x5F), extended BSD/networking (0x60-0x8F), POSIX extensions (0x90-0xFF), modern BSD (0x100-0x17F), and PS4/PS5 specific (0x180+). Three sysvec structures dispatch PS4 SELF (backward compat), FreeBSD ELF64, and Native SELF binaries.

Naming conventions reveal provenance: sys_compat.* (PS4 wrappers), sys_compat4/6/7.* (FreeBSD legacy), sys_number* (unnamed PS5-specific), sys_obsolete* (deprecated). Over 100 IOCTL devices under /dev/ are accessible through sys_ioctl (0x36), covering PUP update processing, TEE communications, manufacturing authorization, serial flash access, DRM, drive authentication, and the TPM.

Every confirmed PS5 kernel exploit targets a syscall in these ranges: kqueueex cr_ref (kqueue, 0x9X), netcontrol double fdrop (socket, 0x61), aio_multi_delete double free (aio, 0x10X), umtx_shm UaF (umtx, 0x14X-0x17X), IPV6_2292PKTOPTIONS UaF (setsockopt, 0x68), and fsc2h_ctrl stack free (PS5-specific, 0x180+). The PS5-specific syscalls beyond 0x180 are the most promising targets for new exploit discovery.

## Role in System

The syscall table is the kernel's primary interface to userland — every process interaction with the OS passes through it. It is also the primary kernel attack surface, with 12+ documented exploit classes across the five ranges. The undocumented PS5-specific syscalls (0x180+) lack FreeBSD heritage and compatibility constraints, making them the least audited and most likely source of future exploits.

## Connections

- [[kernel_architecture]]
- [[security_model]]
- [[jailbreak_comprehensive]]
- [[cve_timeline]]

## Graph Reference
research/kernel/syscall_catalog.md
