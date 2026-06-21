# Syscalls

## Source
inbox\syscalls.md

## System Layer
kernel

## Summary
# Syscalls

## Source URL
https://www.psdevwiki.com/ps5/Syscalls

## System Layer
Kernel

## Summary
PS5 kernel syscall table (from kernel 2.20) showing PS4 backward compatibility syscall mappings. The PS5 kernel maps PS4 syscalls to PS5 native syscalls. ## Key Concepts

### Syscall Categories (IDs 0x0-0x1FF)
- **0x00-0x5F**: Standard BSD syscalls (exit, read, write, open, close, etc.)
- **0x60-0x8F**: Extended BSD + networking (socket, connect, bind, listen, ioctl)
- **0x90-0xFF**: POSIX extensions (kqueue, signals, scheduling)
- **0x100-0x17F**: Modern BSD syscalls (aio, kld, mac, sched)
- **0x180+**: PS4/PS5 specific syscalls (truncated in source — see local dump)

### Notable PS4-PS5 Mappings
- `sys_compat.ptrace` (0x1a) -> `sys_ptrace` — process tracing
- `sys_ioctl` (0x36) -> `sys_ioctl` — device I/O control
- `sys_mmap` (0x47) -> `sys_compat.mmap` — memory mapping
- `sys_mtypeprotect` (0x17b) -> `sys_mtypeprotect` — memory type protection
- `sys_sysarch` (0xa5) -> `sys_sysarch` — system architecture
- `sys_rfork` (0xfb) -> `sys_rfork` — process fork
- Syscalls beyond 0x180 are PS5-specific additions not shared with PS4 compat layer

### Naming Convention
- `sys_compat.*` — PS4 compatibility wrappers
- `sys_compat4.*` — FreeBSD 4.x compatibility
- `sys_compat6.*` — FreeBSD 6.x compatibility
- `sys_compat7.*` — FreeBSD 7.x compatibility
- `sys_number*` — Unknown/unnamed syscalls (likely PS5-specific)
- `sys_obsolete*` — Deprecated syscalls

## System Role
Critical for understanding the PS5 kernel interface, PS4 backward compatibility layer, and identifying PS5-specific syscalls that may provide unique attack surface.

## Concepts
syscalls, compatibility, ps4, ps5, kernel, bsd, freebsd, layer, ps5-specific, sys_compat, syscall, system, backward, mappings, memory

## Related Notes
- [[../nodes/aw_xm501]]
- [[../nodes/backwards_compatibility]]
- [[../nodes/build_strings]]
- [[../nodes/cxd90063r1]]
- [[../nodes/demo_games]]
- [[../nodes/devices]]
- [[../nodes/disc_drive_media]]
- [[../nodes/homebrew_enabler]]
- [[../nodes/ioctl]]
- [[../nodes/iommu_architecture]]
- [[../nodes/kernel_overview]]
- [[../nodes/keys]]
- [[../nodes/keystone]]
- [[../nodes/mac_address]]
- [[../nodes/mast1c0re_jit_pipeline]]
- [[../nodes/memory]]
- [[../nodes/mt3613ct]]
- [[../nodes/p2jb_kernel_exploit]]
- [[../nodes/passcode]]
- [[../nodes/poops_kernel_exploit]]
