# PS5 Kernel Architecture

## Overview

The PS5 kernel is a heavily modified FreeBSD 11.0 derivative (__FreeBSD_version 1100122) that serves as the core operating system layer running under hypervisor control. It manages all hardware resources including CPU, memory, GPU, storage, and I/O peripherals while enforcing Sony's security model through multiple interconnected protection mechanisms. The kernel implements three distinct sysvec (syscall vector) structures to handle different binary formats: PS4 SELF for backward compatibility with PlayStation 4 executables, FreeBSD ELF64 for standard FreeBSD binaries (normally unused on retail systems), and Native SELF for PS5 processes.

The kernel employs modern x86-64 hardware security features including NX (No-Execute) bit, SMAP (Supervisor Mode Access Prevention), SMEP (Supervisor Mode Execution Prevention), UMIP (User Mode Instruction Prevention), and AMD's nda/xotext (execute-only memory via EFER bit 16). These protections are layered with Sony-specific security mechanisms such as eXecute-Only Memory (XOM), signed secure modules, and a Trusted Execution Environment (TEE) running on the Platform Security Processor (PSP). The kernel's attack surface is exposed through syscalls, IOCTL devices, and the SceSbl authentication manager subsystem, all of which are critical paths for security research.

Communication with the hardware platform occurs through four co-processors managed by the kernel: MP0 (PSP — AMD Platform Security Processor), MP1 (SMU — Xtensa CPU for power/clock/thermal), MP3 (TEE — Trusted Execution Environment with PlayReady SL3000 DRM), and MP4 (ARM Cortex-A53 for I/O and memory management). The kernel enforces the security policy dictated by the hypervisor and secure loader boot chain, making it a critical but constrained component in the overall platform security architecture.

## Components

### Origin and Base

The PS5 kernel is derived from FreeBSD 11.0 with kernel version identifier 1100122. Sony has made extensive modifications including the addition of three sysvec structures for binary format dispatch, custom memory management with execute-only page table entries, proprietary file system drivers (PFS), and a comprehensive security monitoring subsystem. The kernel maintains compatibility layers for FreeBSD 4.x, 6.x, and 7.x syscalls (via sys_compat4, sys_compat6, sys_compat7 naming), alongside the PS4 compatibility layer (sys_compat) which maps PS4 syscalls to their native PS5 equivalents.

### System Call Interface

The PS5 syscall table (documented from kernel 2.20) is organized into ranges:

- **0x00-0x5F**: Standard BSD syscalls (exit, read, write, open, close, etc.)
- **0x60-0x8F**: Extended BSD and networking (socket, connect, bind, listen, ioctl at 0x36)
- **0x90-0xFF**: POSIX extensions (kqueue, signals, scheduling)
- **0x100-0x17F**: Modern BSD syscalls (aio, kld, mac, sched)
- **0x180+**: PS4/PS5 specific syscalls

Notable PS4-to-PS5 syscall mappings include:

| PS4 Syscall | Maps To | Description |
|---|---|---|
| sys_compat.ptrace (0x1a) | sys_ptrace | Process tracing |
| sys_ioctl (0x36) | sys_ioctl | Device I/O control |
| sys_mmap (0x47) | sys_compat.mmap | Memory mapping |
| sys_mtypeprotect (0x17b) | sys_mtypeprotect | Memory type protection |
| sys_sysarch (0xa5) | sys_sysarch | System architecture operations |
| sys_rfork (0xfb) | sys_rfork | Process fork |

Syscalls beyond 0x180 are PS5-specific additions with no PS4 compat layer equivalent. These represent unique PS5 attack surface. The naming convention uses prefixes: `sys_compat.*` for PS4 wrappers, `sys_compat4/6/7.*` for legacy FreeBSD compat, `sys_number*` for unnamed PS5-specific entries, and `sys_obsolete*` for deprecated calls.

### Memory Management

The kernel manages a virtual address space with hardware-enforced protections. The MMU is configured with nested paging (AMD's NPT / Intel's EPT equivalent) controlled by the hypervisor, providing two levels of address translation — guest physical to system physical. This design means the kernel cannot fully control its own page tables, as they are shadowed at the hypervisor level.

Key memory features:

- **NX bit**: Non-executable page enforcement on all data pages
- **SMAP/SMEP**: Prevents kernel from executing user-mode code or accessing user-mode data without explicit intent
- **UMIP**: Blocks user-mode execution of privileged instructions (SGDT, SIDT, SLDT, SMSW, STR)
- **nda/xotext (EFER bit 16)**: AMD-specific execute-only memory support

**XOM (eXecute-Only Memory)** is a critical protection that prevents read access to memory regions at the page table level. When a memory read is processed by the CPU and the XOM bit is set in the PTE, an exception is raised and handled by the hypervisor, which triggers a kernel panic on an uncompromised system. XOM operates at two levels:

- **Usermode XOM**: Enforced on PS5 game titles and system applications. Prevents dumping of usermode modules without a kernel exploit. With kernel read/write access, usermode XOM can be disabled by flipping the PTE bit and flushing TLBs.
- **Kernel XOM**: Protects kernel .text pages. Disabling requires hypervisor compromise or hardware attack due to nested paging shadowing. This creates a chicken-and-egg problem — hypervisor compromise is difficult without kernel reverse engineering, but kernel RE requires XOM bypass.

**Secure Modules** use service IDs in the 0x8002xxxx range, dispatched by the authentication manager. These modules handle cryptographic operations, key management, and verified boot services, and many operate with access to hardware-backed key storage and on-chip OTP fuses.

### Process Model

The PS5 kernel uses a process model derived from FreeBSD's struct proc, extended with PlayStation-specific fields for privilege level, sandbox profile, and credential management. Processes are launched through the sysvec dispatch mechanism which selects the appropriate binary format handler:

1. **PS4 SELF sysvec**: Handles PS4 backward-compatible executables with legacy syscall mappings
2. **FreeBSD ELF64 sysvec**: Standard FreeBSD binaries (largely unused on production systems)
3. **Native SELF sysvec**: All native PS5 processes

Process privileges are governed by capability-based sandboxing. The kernel enforces access controls through the PFS (PlayStation File System) namespace and restricts device access based on process origin. The /dev/ namespace provides controlled access to hardware and security services.

### Security Mechanisms

The kernel security architecture is multi-layered, combining hardware features with Sony-proprietary protections:

**Secure Module System (SceSbl):** The SceSbl (Sony Secure Boot Loader) subsystem provides kernel-level security services dispatched by service ID. The authentication manager (service ID 0x80021000) is the primary entry point for SELF verification, segment loading, and RnpsBundle decryption. Key functions include `sceSblAuthMgrAuthHeader`, `sceSblAuthMgrLoadBlock`, and `sceSblAuthMgrSmLoad`.

| Service ID | Name | Key Functions |
|---|---|---|
| 0x80021000 | authmgr | SELF verification, segment loading |
| 0x80021001 | kms | Key slot allocation, `sceSblKmsAllocKmbSlotForPprPkg`, `sceSblKmsSetKeyId`, `sceSblKmsClearKeyId` |
| 0x80021002 | pup | PUP firmware update processing |
| 0x80021003 | pfs | PFS file system, `sceSblPfsmgrUpdateIcvTable` |
| 0x80021004 | driveauth | BD drive authentication, AACS/CPRM key retrieval |
| 0x80021005 | pltauth | Platform challenge/response, `sceSblPltAuth2GenC1`, `sceSblPltAuth2VeriR1C2GenR2` |
| 0x80021006 | npdrm | NP DRM, `sceSblNpDrmCheckDebugClock`, `sceSblNpDrmGetCurrentDebugTick` |
| 0x80021007 | devact | Device activation, `sceSblDevActGetId`, `sceSblDevActGetRemainingTime` |
| 0x80021008 | qafutkn | QA/Utoken services |
| 0x80021009 | sysveri | System verification, `sceSblSysVeriInitialize` |
| 0x8002100A | otpaccess | OTP (One-Time Programmable) fuse access |
| 0x8002100B | manu | Manufacturing mode, `sceSblManuAuthSetManuMode`, `sceSblManuAuthLoadSecureModule` |
| 0x8002100C | fttrm | NAND sector access, IDU flag read/write |
| 0x8002100D | srtc | Secure RTC, `sceSblSrtcGetCurrentSecureTick` |
| 0x8002100E | rootparam | Root parameter verification, `sceSblRootParamVerifyPprRootParam` |
| 0x8002100F | exthdd | External HDD metadata verification |
| 0x80021010 | cloudsd | Cloud SaveData, `sceSblPfsSaveDataUpdateAuthCode` |
| 0x80021011 | bar | Backup and Restore, `sceSblBarCreateContext`, `sceSblBarUpdateEncrypt`/`Decrypt` |
| 0x80021012-0x80021018 | otprsvaccess, diskid, idata, ddd, otpctrl, ncdt, hidauth | Additional security services |

**Secure Loader:** The IPL (Initial Program Loader) runs on the PSP and is the first code after boot ROM. It verifies and loads the hypervisor and kernel. The IPL header (at NAND Group 0 offset 0x800) contains a magic value (E4 DB 7C 02), RSA4096 signature at offset 0x200, SHA256 of the decrypted body at offset 0x20, and a security revision value that controls firmware downgrade protection. Security revisions escalate with firmware versions:

| Value | Firmware |
|---|---|
| 0x00000001 | 0.85.007-1.XX |
| 0x00000007 | 1.00-6.02 |
| 0x000000FF | 6.50 |
| 0x000003FF | 7.00-7.61 |
| 0x00000FFF | 8.00-8.60 |
| 0x00003FFF | 9.00-9.60 |
| 0x0000FFFF | 10.00-10.60 |
| 0x0003FFFF | 11.00+ |

**Kernel Patch Protection:** The kernel monitors its own code integrity and can detect modifications. This is supplemented by the hypervisor's ability to enforce memory protections through nested page tables, making kernel-level exploitation and persistence challenging.

### Driver Architecture

The PS5 kernel exposes hardware and security services through a /dev/ device model accessed via the `sys_ioctl` syscall (0x36). Over 100 kernel device entries are documented, providing interfaces to the system's co-processors and security subsystems:

| Device | Description |
|---|---|
| /dev/bar | Backup and Restore for shellcore |
| /dev/duid | Disc Unique Identifier |
| /dev/dldbg | Dynamic Library Debug |
| /dev/fttrm | Film/TV Tracking Rights Management (Blu-ray DRM) |
| /dev/icc_floyd | TPM (Trusted Platform Module) |
| /dev/manuauth | Manufacturer authorization |
| /dev/nsfsctl | Namespace Filesystem Control |
| /dev/pfsctldev | PlayStation FileSystem Control |
| /dev/pfsmgr | PFS Manager (trophies, savedata, keystone) |
| /dev/pup_update0 | Firmware update device |
| /dev/rootparam | Root PARAM.SFO/JSON verification |
| /dev/sflash0 | Serial Flash access (2MB) |
| /dev/wlanbt | Wireless LAN + Bluetooth |

The device tree is backed by four co-processors:
- **MP0 (PSP)**: AMD Platform Security Processor — secure boot, key management, cryptographic services
- **MP1 (SMU)**: Xtensa CPU — power management, clock gating, thermal monitoring
- **MP3 (TEE)**: Trusted Execution Environment on PSP — PlayReady SL3000 DRM, secure media paths
- **MP4 (A53)**: ARM Cortex-A53 — I/O co-processing, memory management offload

### File System

The PS5 kernel implements multiple file system layers built on top of a UFS-like base:

- **PFS (PlayStation File System)**: Custom on-disk format used for game packages, save data, and system partitions. Supports ICV (Integrity Check Value) tables for data authentication. Managed through service ID 0x80021003 with the function `sceSblPfsmgrUpdateIcvTable`.
- **PFS Namespace (nsfsctl)**: Virtual file system layer providing sandboxed views of the file system per process. Controlled via /dev/nsfsctl and /dev/pfsctldev.
- **Encryption**: File system encryption is managed by the KMS (Key Management System, 0x80021001) which handles key slot allocation. Per-title and per-user encryption keys are derived from hardware-backed secrets.
- **External Storage**: External HDD support is verified through service ID 0x8002100F (`sceSblExternalHDDVerifyMetadata`).
- **serial flash**: 2MB serial flash (via /dev/sflash0) stores boot configuration, EMC firmware, and calibration data. EMC firmware can be extracted at offset 0x4000 (length 0x7E000) using blsunpack.

### IOCTL Interface

The IOCTL interface is a major kernel attack surface, providing user-to-kernel communication for device-specific operations. IOCTL codes follow a structured format encoding direction, size, and command identifier.

**PUP Update IOCTLs** (firmware update subsystem):

| IOCTL | Function |
|---|---|
| 0x20004407 | UpdateSnvs |
| 0x40047400 | updaterGetWlanDeviceId |
| 0xC001440F | GetXtsKeyNum |
| 0xC0104401 | VerifyBlsHeader |
| 0xC0104408 | genChallenge |
| 0xC010440E | UpdateFloydFw |
| 0xC010440C | IdentifyNandController |
| 0xC0104410 | verifyResponse |
| 0xC0184402 | DecryptPupHeader |
| 0xC0184403 | VerifyPupAdditionalSign |
| 0xC0184404 | VerifyPupWatermark |
| 0xC0184405 | DecryptPupSegment |
| 0xC018440A | ReadNandGroup |
| 0xC018440B | WriteNandGroup |
| 0xC0284406 | DecryptPupSegmentBlock |

**TEE IOCTLs** (Trusted Execution Environment communication):

| IOCTL | Function |
|---|---|
| 0x400CB400 | TEE_IOC_VERSION |
| 0x8008B40B | TEE_IOC_DLM_STOP_TA_DEBUG |
| 0xC004B405 | TEE_IOC_CLOSE_SESSION |
| 0xC004B40E | TEE_SHMEM_RELEASE |
| 0xC004B40F | TEE_SET_TIMEOUT |
| 0xC008B404 | TEE_IOC_CANCEL |
| 0xC010B402 | TEE_IOC_OPEN_SESSION |
| 0xC010B403 | TEE_IOC_INVOKE |
| 0xC010B408 | TEE_IOC_DLM_GET_DEBUG_TOKEN |
| 0xC020B40D | TEE_SHMEM_MAP_SETNAME |
| 0xC028B409 | TEE_IOC_DLM_START_TA_DEBUG |
| 0xC038B40C | TEE_IOC_INIT_ASD |
| 0xC110B40A | TEE_IOC_DLM_FETCH_DEBUG_STRING |

**Manufacturing Mode IOCTLs**:

| IOCTL | Function |
|---|---|
| 0xC0184D03 | sceSblManuAuthSetManuMode |
| 0x40184D02 | sceSblManuAuthUnloadSecureModule |
| 0x40184D01 | sceSblManuAuthLoadSecureModule |

**Other Notable IOCTLs**:

| IOCTL | Function |
|---|---|
| 0xC028530A | _sceSblDriveauthSmGetPairingNonce |
| 0xC028530B | _sceSblDriveauthSmGetPairingRequest |
| 0xC028530C | _sceSblDriveauthSmSetPairingInfo |
| 0xC028530D | _sceSblDriveauthSmSetHostKey |
| 0xC028530E | _sceSblDriveauthSmRemoveDiscKey |
| 0xC0205365 | sceSblDriveauthGetCprmDeviceKey |
| 0xC0205364 | sceSblDriveauthGetAacsDeviceKey |
| 0x80018F0A | icc_fan_change_servo_pattern |
| 0xC0068F06 | icc_fan_get_fan_manual_duty |
| 0xC0105203 | verifyDecryptRnpsBundle |
| 0xC0185301 | fftrm read sector |
| 0xC0185302 | fftrm write sector |
| 0xC0185303 | fftrm read idu flag |
| 0xC0185304 | fftrm write idu flag |
| 0x40144401 | devActInitStatus |
| 0x40184402 | sceSblDevActGetId |
| 0x4030440B | devActGenRequest |
| 0x8004B201 | gc_reset |

## Relationships

- [[hardware_overview]] — kernel manages hardware resources including the four co-processors (MP0-MP4), NAND storage, serial flash, and I/O peripherals through the IOCTL device interface
- [[hypervisor]] — kernel runs under hypervisor control with nested page tables; kernel XOM is enforced through hypervisor exception handling; the hypervisor is loaded by the Secure Loader before the kernel
- [[security_model]] — kernel enforces security policy through SceSbl secure module dispatch, capability-based sandboxing, PFS access controls, and XOM memory protections
- [[firmware]] — kernel is loaded by the Secure Loader (IPL) boot chain from NAND; PUP firmware updates are processed through kernel IOCTLs; the security revision system in the IPL header governs which kernel versions can boot

## Security Considerations

- [[xom]] — eXecute-Only Memory creates a read-prevention layer on both usermode and kernel .text pages; kernel XOM is hypervisor-backed via nested paging, creating a chicken-and-egg problem for reverse engineering
- [[secure_modules]] — signed kernel modules (0x8002xxxx service IDs) provide trusted cryptographic and security services; manufacturing modules can be loaded/unloaded via IOCTLs and represent potential escalation paths
- [[emc]] — Embedded Micro Controller (CXD90061GG) firmware manages power-on initialization and is stored in serial flash; EMC version correlates with system firmware version
- Syscall attack surface for privilege escalation: PS5-specific syscalls beyond 0x180 lack documentation and compatibility constraints, representing the most likely kernel exploitation vectors
- TEE IOCTL interface exposes trusted application management (open session, invoke, debug) through /dev/ devices — TEE_IOC_DLM_START_TA_DEBUG and TEE_IOC_DLM_FETCH_DEBUG_STRING are particularly interesting for security research
- Manufacturing mode IOCTLs (load/unload secure modules) are restricted but if reachable could bypass signed module requirements
- PUP update processing involves multiple decryption and verification steps that could contain parsing vulnerabilities (DecryptPupHeader, DecryptPupSegment, VerifyPupAdditionalSign, VerifyPupWatermark)
- Drive authentication IOCTLs handle AACS/CPRM key retrieval and BD drive pairing — cryptographic key extraction attempts could target these interfaces
- The fftrm (NAND sector read/write) IOCTLs provide low-level storage access that could be used for persistent modification
- Kernel functions dispatched via service IDs represent controlled but extensive kernel-level API surface with over 20 service categories

## References

- https://www.psdevwiki.com/ps5/Kernel
- https://www.psdevwiki.com/ps5/Kernel_Functions
- https://www.psdevwiki.com/ps5/Syscalls
- https://www.psdevwiki.com/ps5/IOCTL
- https://www.psdevwiki.com/ps5/Devices
- https://www.psdevwiki.com/ps5/Secure_Loader
- https://www.psdevwiki.com/ps5/Secure_Modules
- https://www.psdevwiki.com/ps5/XOM
- https://www.psdevwiki.com/ps5/EMC
