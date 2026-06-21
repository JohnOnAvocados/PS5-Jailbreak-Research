# Kernel Syscall Catalog: Complete Reference for PS5 Exploit Development

## Overview

The PS5 kernel is a heavily modified FreeBSD 11.0 derivative (__FreeBSD_version 1100122) with 500+ syscalls organized across five ranges: standard BSD (0x00-0x5F), extended BSD and networking (0x60-0x8F), POSIX extensions (0x90-0xFF), modern BSD (0x100-0x17F), and PS4/PS5 specific extensions (0x180+). The syscall dispatch uses three distinct sysvec structures: PS4 SELF (backward compatibility), FreeBSD ELF64 (standard, normally unused), and Native SELF (PS5 processes). Console naming conventions reveal the syscall provenance: `sys_compat.*` for PS4 wrappers, `sys_compat4/6/7.*` for FreeBSD legacy compat, `sys_number*` for unnamed PS5-specific entries, and `sys_obsolete*` for deprecated syscalls.

This catalog serves as the essential reference for kernel exploit development. Every confirmed kernel exploit on PS5 (kqueueex cr_ref, netcontrol double fdrop, aio_multi_delete double free, umtx_shm UaF, IPV6_2292PKTOPTIONS UaF, fsc2h_ctrl stack free) targets a syscall in one of these five ranges. The PS5-specific syscalls beyond 0x180 are the most promising targets for new exploit discovery — they lack FreeBSD compatibility constraints and are undocumented.

## Syscall Dispatch Architecture

### Three Sysvec Structures

| Sysvec | Purpose | ELF Type | Typical Usage |
|--------|---------|----------|---------------|
| PS4 SELF | PS4 backward compatibility | PS4 SELF | PS4 games on PS5 |
| FreeBSD ELF64 | Standard FreeBSD binary | FreeBSD ELF64 | Normally unused on PS5 |
| Native SELF | Native PS5 processes | PS5 SELF | All PS5 system software and games |

The PS4 SELF sysvec maps PS4 syscalls to PS5 native syscalls. For example, PS4's `sys_ptrace` (0x1a) maps to PS5's `sys_ptrace`. This compatibility layer is maintained for PS4 game backward compatibility and is a potential source of exploitation if the mapping introduces behavioral differences.

The FreeBSD ELF64 sysvec exists for standard FreeBSD binaries but is normally unused on retail PS5 — the kernel does not support loading standard FreeBSD ELF64 executables through normal means.

### Syscall Table Structure

The syscall table is an array of `struct sysent` entries, each containing:
- **sy_narg:** Number of arguments
- **sy_flags:** Syscall flags (SYF_CAPENABLED, SYF_NOLKM, etc.)
- **sy_call:** Function pointer to the syscall handler
- **sy_thrcnt:** Thread count statistics

The full table is populated at boot time and some entries may be NULL (unimplemented syscalls that return ENOSYS).

### Naming Conventions

| Prefix | Meaning | Example |
|--------|---------|---------|
| `sys_compat.*` | PS4 backward compatibility wrapper | `sys_compat.ptrace` |
| `sys_compat4.*` | FreeBSD 4.x compatibility | `sys_compat4.sigaction` |
| `sys_compat6.*` | FreeBSD 6.x compatibility | `sys_compat6.kevent` |
| `sys_compat7.*` | FreeBSD 7.x compatibility | `sys_compat7.mmap` |
| `sys_number*` | PS5-specific, unnamed | `sys_number01` through `sys_numberXX` |
| `sys_obsolete*` | Deprecated, returns ENOSYS or EOPNOTSUPP | `sys_obsolete.asynccancel` |

### Known Mappings

| Native | PS4 Compat | Syscall | Comments |
|--------|-----------|---------|----------|
| 0x1a | 0x1a | ptrace | Process tracing (PS4 compat wraps to native) |
| 0x36 | 0x36 | ioctl | Device I/O control |
| 0x47 | 0x47 | mmap | Memory mapping |
| 0xA5 | 0xA5 | sysarch | System architecture operations |
| 0xFB | 0xFB | rfork | Process fork |
| 0x17B | 0x17B | mtypeprotect | Memory type protection |
| 0x180+ | N/A | PS5-specific | No PS4 equivalents |

## Full Syscall Range Breakdown

### Range 0x00-0x5F: Standard BSD

The base FreeBSD syscall set. Most are stock FreeBSD 11.0 implementations with Sony modifications:

| Range | Category | Key Syscalls | Exploit Potential |
|-------|----------|-------------|-------------------|
| 0x00-0x0F | Process control | exit, fork, read, write, open, close, wait4, creat, link, unlink, execve, chdir, gethostid, sbrk | Low (well-audited) |
| 0x10-0x1F | File/process ops | chmod, chown, ptrace, getpid, setuid, getuid, recvfile, sendfile, access | Medium (ptrace) |
| 0x20-0x2F | File ops | getpid, getgid, getppid, getpgrp, setreuid, setregid, stat, lstat, fstat | Low |
| 0x30-0x3F | File/IO | statfs, fstatfs, fchmod, fchown, umask, ioctl, revoke, mmap | Medium (ioctl) |
| 0x40-0x4F | Memory/sync | munmap, mprotect, madvise, vhangup, mincore, pathconf, sbrk, sstk | Medium (mprotect) |
| 0x50-0x5F | Resource/misc | acct, shmget, shmctl, shmat, shmdt, sigpending, sigprocmask, sigreturn | Low |

**Notable PS5 modifications:**
- `sys_ptrace` (0x1a): Modified to restrict debugging capabilities based on process Auth ID and capability flags
- `sys_ioctl` (0x36): Custom IOCTL handler routing to 100+ PS5-specific devices
- `sys_mmap` (0x47): Modified for PS5's JIT shared memory model (`sys_jitshm_create`)

### Range 0x60-0x8F: Extended BSD and Networking

Networking syscalls are a rich source of PS5 kernel exploits:

| ID | Syscall | Exploit History |
|----|---------|-----------------|
| 0x61 | socket | Netcontrol (double fdrop UaF, FW <=12.00) |
| 0x62 | connect | Socket option exploitation |
| 0x63 | accept | File descriptor inheritance |
| 0x68 | setsockopt | IPV6_2292PKTOPTIONS (CVE-2020-7457, FW 3.00-4.51) |
| 0x69 | getsockopt | Information leak potential |
| 0x6A | fstat | Can be exploited via pipe-based kernel R/W primitives |
| 0x7X | send/recv family | Buffer management vulnerabilities |
| 0x8X | socket options | Additional socket option handlers |

**Key exploit classes in this range:**
- Use-after-free via socket option handlers (IPV6_2292PKTOPTIONS)
- Double file descriptor drop (netcontrol)
- Heap overflows through crafted option values
- Race conditions in socket state transitions

### Range 0x90-0xFF: POSIX Extensions

Includes kqueue, signals, scheduling:

| ID | Syscall | Exploit History |
|----|---------|-----------------|
| 0x9X | kqueue family | **kqueueex (P2JB):** cr_ref overflow via ~4.3B kqueueex calls (FW <=12.70) |
| 0xA0-0xAF | Signal handling | Signal delivery race conditions |
| 0xB0-0xBF | POSIX timers | Timer-related race conditions |
| 0xF0-0xFF | Process/thread | rfork (thread creation), jail |

**kqueueex (P2JB) — The current kernel exploit ceiling:**
The `sys_kqueueex` syscall holds a `crhold()` on the calling thread's `ucred` credential structure. If the optional `name` argument causes `copyinstr()` to fail (EFAULT), the error cleanup path calls `free()` + `fdclose()` + `fdrop()` but **never `crfree()`** — permanently leaking one `cr_ref` per call. After ~4.3 billion calls, the 32-bit counter wraps to zero, and a subsequent `setuid(0)` frees the real `ucred` while staged file descriptors still hold dangling `fp->f_cred` pointers. Sony's patch in FW 13.00 appears to have increased the cr_ref width or added overflow protection.

### Range 0x100-0x17F: Modern BSD

Async I/O, kernel loading, MAC, scheduling:

| ID | Category | Exploit History |
|----|----------|-----------------|
| 0x10X | aio (async I/O) | **aio_multi_delete (Lapse):** Double free via improper locking (FW <=10.01) |
| 0x11X | kld (kernel loader) | Module loading (restricted to signed modules) |
| 0x12X | mac (Mandatory Access Control) | Policy enforcement |
| 0x13X | sched (scheduler) | Thread scheduling manipulation |
| 0x14X-0x17X | umtx (user mutex) | **umtx_shm (CVE-2024-43102):** Use-after-free race condition (FW <=7.61) |
| 0x17B | mtypeprotect | Sony extension for memory type protection |

**umtx_shm (UMTX2, CVE-2024-43102):**
Use-after-free in FreeBSD user-mutex shared memory subsystem. Two threads racing during `umtx_shm` operations trigger a memory free while one retains a dangling reference. FW <=7.61, patched FW 8.00. Discovered by shahrilnet, n0llptr, SpecterDev, ChendoChap.

**aio_multi_delete (Lapse):**
Double free in async I/O subsystem. Improper locking during concurrent `aio_multi_delete` operations causes the kernel to free the same AIO context twice, corrupting heap memory. FW <=10.01, patched FW 10.02. Broadest kernel exploit firmware range (1.00-10.01).

### Range 0x180+: PS4/PS5 Specific

The most important range for exploit discovery — these syscalls are Sony additions not present in stock FreeBSD:

| ID Range | Syscall | Description |
|----------|---------|-------------|
| 0x180-0x18F | `sys_number01-0F` | PS5-specific, unnamed |
| 0x190-0x19F | `sys_number10-1F` | PS5-specific, unnamed |
| 0x1A0-0x1AF | `sys_number20-2F` | PS5-specific, unnamed |
| 0x1B0-0x1BF | `sys_number30-3F` | PS5-specific, unnamed |
| 0x1C0-0x1CF | `sys_number40-4F` | PS5-specific, unnamed |
| 0x1D0-0x1F0+ | Extended, partially documented | Additional PS5-specific |

**Known PS5-specific syscalls:**
- `sys_jitshm_create` / `sys_jitshm_*`: JIT shared memory management (introduced for PS2 emulator and other JIT processes)
- `sys_fsc2h_ctrl`: File system cache-to-HDD control (vulnerable to kernel stack free, FW <=10.40, TheFloW HackerOne submission)
- `sys_mtypeprotect` (0x17B): Memory type protection (Sony extension)
- `sys_kqueueex`: Extended kqueue with credential reference (P2JB cr_ref overflow)
- Manufacturing and debug syscalls (restricted to specific Auth IDs)

**Potential exploit targets in this range:**
- Every undocumented syscall in 0x180-0x1FF is a candidate
- No backward compatibility constraints (unlike PS4 compat syscalls)
- Less auditing than stock FreeBSD code
- Sony-added syscalls may have weaker input validation

## IOCTL Device Interface

Beyond the syscall table, PS5 exposes over 100 kernel device entries under `/dev/` accessible through `sys_ioctl` (0x36). Each device has its own IOCTL command set:

| Device | Path | Function | Notable IOCTLs |
|--------|------|----------|----------------|
| PUP Update | /dev/pup_update0 | Firmware update processing | DecryptPupHeader (0xC0184402), DecryptPupSegment (0xC0184405), ReadNandGroup (0xC018440A), WriteNandGroup (0xC018440B) |
| TEE | /dev/tee* | Trusted Execution Environment | TEE_IOC_OPEN_SESSION (0xC010B402), TEE_IOC_INVOKE (0xC010B403), TEE_IOC_DLM_START_TA_DEBUG (0xC028B409) |
| Manufacturing | /dev/manuauth | Factory authorization | SetManuMode (0xC0184D03), LoadSecureModule (0x40184D01), UnloadSecureModule (0x40184D02) |
| Serial Flash | /dev/sflash0 | SPI flash access | Read/write operations to 2 MB Winbond 25Q16JVNIM |
| PFS | /dev/pfsctldev, /dev/pfsmgr | PlayStation File System | ICV table updates, namespace control |
| DRM | /dev/fttrm | Film/TV rights management | Read/write sector (0xC0185301-0xC0185304) |
| Drive Auth | /dev/driveauth | BD drive authentication | GetAacsDeviceKey (0xC0205364), GetCprmDeviceKey (0xC0205365) |
| Device Activation | /dev/devact | Console activation | devActInitStatus (0x40144401), devActGenRequest (0x4030440B) |
| Bluetooth/Wi-Fi | /dev/wlanbt | Wireless | DualSense pairing, network configuration |
| Backup/Restore | /dev/bar | Shellcore backup | System state backup and restore |
| TPM/Floyd | /dev/icc_floyd | Trusted Platform Module | Cryptographic operations, secure key storage |
| Root PARAM | /dev/rootparam | System configuration | PARAM.SFO/JSON verification |

## Exploit-Relevant Syscall Categories

### Reference Counting Bugs (Highest Success Rate)
3 of 6 documented kernel exploits involve reference counting errors:
- **kqueueex:** cr_ref overflow (FW <=12.70)
- **netcontrol:** fdrop double-drop (FW <=12.00)
- **aio_multi_delete:** Double free (FW <=10.01)

Reference counting bugs are the most reliable exploit class on PS5 due to:
- FreeBSD's extensive use of refcount-based resource management
- 32-bit refcount fields that are susceptible to overflow
- Multiple code paths that may skip refcount adjustments on error

### Socket Option Bugs
2 documented exploits:
- **IPV6_2292PKTOPTIONS:** setsockopt UaF (FW 3.00-4.51)
- **netcontrol:** Socket fd double-drop

Socket option handling is complex and frequently introduces vulnerabilities.

### Race Conditions
- **umtx_shm:** Race in shared memory operations (FW <=7.61)
- **aio_multi_delete:** Race in async I/O cancellation

## Future Exploit Targets

Based on the historical pattern, the following syscalls are the most likely future exploit targets:

| Priority | Syscall | Category | Reason |
|----------|---------|----------|--------|
| 1 | `sys_kqueueex` (already known) | Reference counting | Sony's FW 13.00 fix may have introduced new variants |
| 2 | Undocumented 0x180+ syscalls | Sony-specific | Least audited, no FreeBSD heritage constraints |
| 3 | `sys_ioctl` on TEE/devact devices | IOCTL interface | Complex parameter validation, manufacturing IOCTLs |
| 4 | `sys_setsockopt` (IPv6 extensions) | Socket options | Historic vulnerability pattern |
| 5 | `sys_jitshm_*` syscalls | Memory management | JIT shared memory introduces unusual memory semantics |
| 6 | `sys_fsc2h_ctrl` | File system | TheFloW's HackerOne disclosure may have additional depth |

## Open Questions

### Comprehensive Catalog
- Q-CRIT-012: Complete annotated list of all 500+ syscalls with handler function names and firmware version comparison
- Q-IMP-024: Which syscalls have Sony-added security checks (credential verification, capability gates)
- Q-IMP-025: Complete IOCTL catalog with descriptions for 100+ /dev/ entries

### Firmware Variation
- Q-IMP-026: Whether the syscall table differs across firmware versions (which syscalls added, removed, or modified)
- Q-IMP-027: Which syscalls were modified in the FW 13.00 security update (beyond the kqueueex cr_ref fix)
- Q-MIN-006: Whether PS5-specific syscalls are present on PS4 (architecture sharing analysis)

### PS4 Compatibility Layer
- Q-IMP-028: Behavioral differences between PS4 SELF compat syscalls and native PS5 implementations
- Q-IMP-029: Whether PS4 SELF compat has any reachable syscall that native PS5 does not
- Q-MIN-007: Whether PS4 compat syscalls have different security checks than native equivalents

## References

### PSDevWiki
- https://www.psdevwiki.com/ps5/Syscalls (syscall table, naming conventions)
- https://www.psdevwiki.com/ps5/Kernel (overview, FreeBSD 11.0 base)
- https://www.psdevwiki.com/ps5/Kernel_Functions (function reference)
- https://www.psdevwiki.com/ps5/IOCTL (IOCTL code catalog)
- https://www.psdevwiki.com/ps5/Devices (/dev/ device listing)

### Research Files
- [[kernel]] — full kernel architecture, XOM, SMAP/SMEP/UMIP
- [[cve_timeline]] — CVE reference, patching timeline
- [[jailbreak_comprehensive]] — exploit chain compatibility, kernel exploit catalog
- [[attack_surface]] — kernel attack surface enumeration
- [[mitigation_assessment]] — kernel mitigation effectiveness
- [[gpu_dma_exploitation]] — GPU DMA bypass (post-exploitation technique)
