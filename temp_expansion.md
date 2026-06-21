
## Firmware Version History in Detail

### Version Numbering

PS5 firmware versions use a structured build string format: `YY.SS-MM.mm.nn.nn-UU.UU.UU.U.b`

- YY = last 2 digits of build year (20 for 2020, 26 for 2026)
- SS = semester (01=first half, 02=second half before 2024; per-year counters 03-07 since 2024)
- MM = major version, mm = minor version, nn.nn = extended minor
- UU.UU.UU.U = unknown version fields
- b = 0 or 1 (1 on CEX/retail, 0 on testkit/devkit)

Short display format is `MM.mm.nn` (e.g., 13.40).

### Retail Firmware Release History

| Version | Build | Date | Size | Key Changes |
|---------|-------|------|------|-------------|
| 1.00 | 20.01-01.00.00.37 | 2020-05-21 | - | Canada/US launch physical |
| 1.14 | 20.02-01.14.00.00 | 2020-10 | - | Minimum for launch games |
| 2.20 | 20.02-02.20.00.07 | 2020-11-06 | 868 MB | Official release day patch |
| 2.25 | 20.02-02.25.00 | 2020-11 | - | Improved system performance, fixed download queue |
| 2.26 | 20.02-02.26.00 | 2020-12 | - | Fixed disc game deletion bug, DualSense charging fix |
| 2.30 | 20.02-02.30.00 | 2021-02 | - | Data transfer fix, PS4 text input fix, Wi-Fi stability |
| 2.50 | 20.02-02.50.00 | 2021-04 | - | PS4 disc auto-install fix, Share Factory clip editing |
| 3.00 | 21.01-03.00.00 | 2021-04 | - | Ukrainian language, ext USB storage, hypervisor split |
| 3.20 | 21.01-03.20.00 | 2021-07 | - | DualSense firmware updater, screen reader fixes |
| 4.00 | 21.02-04.00.00.42 | 2021-09-03 | 913.7 MB | M.2 SSD expansion support |
| 5.00 | 22.01-05.00.00 | 2022-03 | - | Social features, HV TMR hardening |
| 6.00 | 23.01-06.00.00 | 2022-09 | - | WebKit update (patches CVE-2022-22620), GPU driver |
| 7.00 | 23.01-07.00.00.44 | 2023-02-28 | - | Discord voice chat, HV TMR hardening |
| 8.00 | 23.02-08.00.00 | 2023-09 | - | BD-J sandbox hardening |
| 9.00 | 24.02-09.00.00.45 | 2024-03-09 | - | Native PS2 emulator support |
| 10.00 | 24.06-10.00.00.46 | 2024-09-03 | - | VRR for 1440p, social enhancements |
| 11.00 | 25.02-11.00.00.43 | 2025-03-04 | - | Security improvements |
| 12.00 | 25.06-12.00.00.43 | 2025-09-09 | - | System update |
| 12.02 | - | 2025-09 | - | Patches netcontrol double fdrop |
| 12.60 | - | 2025-11 | - | Patches Netflix V8/SpiderMonkey CVEs |
| 13.00 | 26.02-13.00.00.40 | 2026-03-10 | - | Patches P2JB cr_ref overflow, BD-JB-EX |
| 13.40 | 26.04-13.40.00.02 | 2026-05-28 | - | Latest, minor bug fixes |

### TestKit and DevKit Versions

TestKit firmware: 0.95.00.44 through 2.30.00.05. DevKit firmware: 0.83.00.20 through 2.30.00.05. These often have relaxed security (debug modes, Assist Mode).

### PUP Infrastructure

Firmware updates distributed as PS5UPDATE.PUP files. The updatelist.xml at `http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6/list/<TLD>/updatelist.xml` lists available versions.

PUP download URL: `http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6/image/<YYYY_MMDD>/<TYPE>_<SHA256>/PS5UPDATE.PUP?dest=<TLD>`

The obfuscated string `tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6` is consistent across all URLs.

Three PUP types: `system` (full update), `recovery` (Safe Mode option 7), `system_ex` (extension).

Region EXTLD prefixes: fjp01 (Japan), fus01 (US), feu01 (Europe), pc/djp01/dus01/deu01 (testkit/devkit).

PUP watermarking for forensic traceability:
- Old format: DevNet user ID, org name, company name, download date, IP address
- New format: Traceable serial number

PUP archives: Internet Archive, Midnight Archive, Softpedia, Darthsternie, DarkSoftware, Yandex (testkit/devkit).

### Firmware Patching Summary

| FW | Patches | Security Changes |
|----|---------|-----------------|
| 3.00 | Byepervisor (vtable + debug flag) | Standalone HV, HyLonome |
| 5.00 | Prosperous TMR edit, IPV6 UaF | HV TMR hardening |
| 6.00 | PSFree CVE-2022-22620 | WebKit update, GPU driver changes |
| 7.00 | TMR Heap OOB | HV TMR hardening |
| 8.00 | BD-JB2 path traversal, umtx_shm CVE-2024-43102, CloneDeserializer | BD-J sandbox hardening |
| 9.00 | CVE-2023-38600 | WebKit update |
| 10.00 | get_by_id_with_this JSScope leak | WebKit update |
| 10.02 | aio_multi_delete (Lapse) | Kernel locking fix |
| 10.50 | fsc2h_ctrl stack free | Kernel stack mgmt fix |
| 12.02 | netcontrol double fdrop | Kernel file descriptor fix |
| 12.60 | Netflix app CVEs | App update |
| 13.00 | P2JB cr_ref overflow, BD-JB-EX | Kernel refcount hardening |

## Boot Chain and Secure Loader Deep Dive

### Secure Loader IPL Header Structure

The IPL header at NAND Group 0 offset 0x800 on the serial flash is 0x400 bytes:

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0x00 | 4 | Magic | E4 DB 7C 02 |
| 0x04 | 4 | Header Size | Always 0x400 (1024 bytes), LE |
| 0x08 | 4 | Entry Point | 0xB0, LE offset into decrypted body |
| 0x0C | 4 | Body Size | Varies by version, e.g. 0x631D0 |
| 0x10 | 0x10 | Padding | Zero-filled |
| 0x20 | 0x20 | SHA-256 Digest | Hash of decrypted body (0x400 to end) |
| 0x40 | 0xB0 | Padding | ASCII 0123456789abcdef + zeroes |
| 0xF0 | 1 | Flag | 0x80 |
| 0xF1 | 0x2B | Padding | Zeroes |
| 0x11C | 4 | Security Revision | Anti-rollback value |
| 0x120 | 0x20 | Revision Nonce | SHA-256 of IPL revision |
| 0x140 | 0xC0 | Metadata | Keyrings and metadata digest |
| 0x200 | 0x200 | RSA-4096 Signature | Covers header 0x00-0x1FF |
| 0x400 | varies | Encrypted Body | Dual-layer AES-128-CBC |

### Security Revision Progression

| Value | Hex | Firmware Range |
|-------|-----|----------------|
| 0x00000001 | 01 00 00 00 | 0.85.007 through 1.XX |
| 0x00000007 | 07 00 00 00 | 1.00 through 6.02 |
| 0x000000FF | FF 00 00 00 | 6.50 |
| 0x000003FF | FF 03 00 00 | 7.00 through 7.61 |
| 0x00000FFF | FF 0F 00 00 | 8.00 through 8.60 |
| 0x00003FFF | FF 3F 00 00 | 9.00 through 9.60 |
| 0x0000FFFF | FF FF 00 00 | 10.00 through 10.60 |
| 0x0003FFFF | FF FF 03 00 | 11.00+ |

### Revision Nonces

Each IPL revision has a unique SHA-256 nonce at offset 0x120:

| Revision | SHA-256 Nonce |
|----------|--------------|
| 0xA0 | E3D98F94 6EB32A6D C8A809C2 6B6F4F91 0ECA6359 00484D99 BA1239E5 DF745C40 |
| 0xB0 | 551814A6 79F14D09 318BEC56 DDEA4344 55279AC4 7D0C5C7E 1491D6EF B21F2B48 |
| 0xC0 | B35979B6 23197C34 6EE6B162 8E189896 8C66DCDC 1C965F4C 77073007 784C4E6A |
| 0xD0 | 1CB39112 79BA5E83 42C9C96B 2FC549B3 DEBFD73D D6B6974E 0784DF7B E8BD2139 |
| 0xE0 | FD50C29C C4AE8821 1BCA0BC5 091C1DBF D6A4DC07 DBF8C0B2 A617FD1D BEE03A3B |
| 0xF0 | 6F20B45B 4FCB6667 715F4B0E E4907CC2 CB41470A 59B226E0 D4F0D01B 67E88050 |
| 0x100 | 50C0E399 33832B2B A689FFAE 294A4492 038E9974 A8BCA6CC 0C2E9C69 9D372A22 |

### Dual-Layer AES-128-CBC Decryption

The Secure Loader body undergoes two sequential decryptions:

**Layer 1 (Global Firmware Key):**
- Key derived from ROM Key material via proprietary PSP derivation
- IV from Secure Loader metadata region (offset 0x140)
- Baseline encryption common across all firmware versions
- PKCS#7 padding

**Layer 2 (Revision-Specific Key):**
- Key derived from Revision Nonce (offset 0x120 SHA-256) + additional PSP key material
- IV different from Layer 1
- Version-specific encryption tied to authorized nonce
- PKCS#7 padding

After decryption, SHA-256 of decrypted body (offset 0x400 through 0x400+body_size) is compared against expected hash at offset 0x20. Confirms correct decryption and integrity.

### Full Boot Chain Stage Transition

Stage 0 - Boot ROM (immutable mask ROM on AMD PSP):
1. PSU stabilizes; SoC power-on reset; PSP starts executing
2. Boot ROM from on-die mask ROM (address ~0xFFFF0000)
3. Initializes PSP caches; detects serial flash via SPI
4. Reads Secure Loader from serial flash offset 0x800 into SRAM
5. Validates magic E4 DB 7C 02; halts if mismatch
6. RSA-4096 signature verification using ROM Key 2
7. Reads Security Revision at 0x11C; compares against OTP fuse
8. Extracts encryption parameters
9. Layer 1 AES-CBC decryption (global firmware key)
10. Layer 2 AES-CBC decryption (revision nonce-derived key)
11. SHA-256 verification of decrypted body
12. Jumps to Secure Loader entry point (offset 0xB0 within body)

Stage 1 - Secure Loader (SCE SBL):
13. SBL sets up execution environment, memory protections
14. Extracts keyrings from metadata region (offset 0x140)
15. Locates EMC firmware at serial flash offset 0x4000
16. Decrypts EMC firmware with revision-specific AES-128-CBC key
17. Parses SLB2 segment using blsunpack; finds C0080001 version file
18. Transfers control to EMC for power-on initialization
19. EMC initializes power rails, clocks, thermal monitoring
20. Control returns to SBL
21. SBL locates Hypervisor Loader within its decrypted body
22. Re-verifies using RSA-4096 chain
23. Loads into protected memory; passes keyrings
24. Transfers control to HyLonome entry point

Stage 2 - Hypervisor Loader (HyLonome, FW >=3.00):
25. Sets up virtualization structures
26. Configures MMU for two-stage translation (NPT)
27. Initializes IOMMU for device isolation
28. Sets up interrupt virtualization
29. Establishes protected memory regions
30. Locates kernel SELF on NAND flash system partition
31. Reads EAP keys from keyring
32. Verifies RSA-3072 signature on kernel SELF header
33. Decrypts kernel body with EAP AES-128-CBC key
34. Validates EMC/EAP/KBL key chain via HMAC-SHA1
35. Performs final SHA-256 integrity check
36. Configures Keystone XOM regions
37. Transfers control to kernel entry point

Stage 3 - Kernel:
38. Initializes remaining hardware
39. Mounts PFS filesystem from NAND
40. Loads secure modules (0x8002xxxx IDs)
41. Mounts system firmware partitions
42. SceShellCore reads index.dat from /priv/etc/
43. RNPS applications initialize (Home UI, Settings, network daemons)
44. Console reaches interactive home screen

### EMC Firmware Versions

The EMC (CXD90061GG) firmware at serial flash offset 0x4000 (length 0x7E000, SLB2 segment):

| EMC Version | PS5 FW | Platform |
|-------------|--------|----------|
| v0.7.6 | SDK 0.85.070 | Prototype/DevKit |
| v1.0.4 | FW 1.01-1.14 | TestKit and Retail |
| v1.2.3 | FW 2.XX | TestKit |
| v1.4.2 | FW 3.00 | Retail |
| v1.6.0 | FW 4.00 | TestKit |
| v1.8.2 | FW 5.00 | Retail |
| v1.8.3 | FW 5.50 | Retail |
| v1.14.3 | FW 9.20 | Retail |

EMC IPL: AES-128-CBC encrypted with keys specific to EMC revision c0. Magic: AA F9 8F D4.

## Hypervisor Architecture Detail

### SVM Features Used

**Nested Page Tables (NPT/SLAT):** The hypervisor maintains stage-2 page tables overlaying the kernel's stage-1 tables. Controls physical memory access independently of the guest's own mappings. Enables restricting guest to specific physical memory regions, enforcing access permissions at hypervisor granularity, and trapping guest page table modifications.

**xotext (Execute-Only Memory):** Custom extension co-developed with AMD. Bit 58 in NPT PTEs marks pages as execute-only. Pages can be fetched but not read or written. Controlled via EFER bit 16 (nda/xotext), masked by hypervisor. One of very few x86 XOM deployments.

**GMET (Guest Mode Execute Trap):** Prevents code execution at wrong privilege level within guest. User-mode code cannot execute kernel pages and vice versa.

**CR Filtering:** Intercepts writes to CR0 (PG, WP, NE, PE), CR4 (SMAP, SMEP, VME), EFER (nda/xotext, SVME, NXE). Prevents kernel from disabling security features.

**MSRPM (MSR Protection Map):** Bitmap intercepting specific MSR accesses. Matching MSR read/write causes VM exit for emulation/filtering/denial.

**SMMU/IOMMU:** Hypervisor-managed DMA isolation. Devices can only access explicitly mapped memory regions through hypercalls 0x06-0x0C.

### Hypercall Interface

17 hypercalls (0x00-0x10 on FW >=3.00) via vmmcall:

| Num | Name | FW | Description |
|-----|------|-----|-------------|
| 0x00 | VMMCALL_HV_GET_MESSAGE_CONF | All | Query HV message configuration |
| 0x01 | VMMCALL_HV_GET_MESSAGE_COUNT | All | Query pending HV messages |
| 0x02 | VMMCALL_HV_START_LOADING_SELF | All | Begin HV self-loading |
| 0x03 | VMMCALL_HV_FINISH_LOADING_SELF | All | Complete HV self-loading |
| 0x04 | VMMCALL_HV_SET_CPUID_PS4 | All | CPUID to PS4 compatibility mode |
| 0x05 | VMMCALL_HV_SET_CPUID_PPR | All | CPUID to production processor revision |
| 0x06 | VMMCALL_HV_IOMMU_SET_GUEST_BUFFERS | All | Configure IOMMU guest buffers |
| 0x07 | VMMCALL_HV_IOMMU_ENABLE_DEVICE | All | Enable IOMMU for device |
| 0x08 | VMMCALL_HV_IOMMU_BIND_PASID | All | Bind Process Address Space ID |
| 0x09 | VMMCALL_HV_IOMMU_UNBIND_PASID | All | Unbind PASID |
| 0x0A | VMMCALL_HV_IOMMU_CHECK_CMD_COMPLETION | All | Check IOMMU command queue |
| 0x0B | VMMCALL_HV_IOMMU_CHECK_EVLOG_REGS | All | Check IOMMU event log |
| 0x0C | VMMCALL_HV_IOMMU_READ_DEVICE_TABLE | All | Read IOMMU device table |
| 0x0D | VMMCALL_HV_GET_TMR_VIOLATION_ERROR | All | Get TMR violation error info |
| 0x0E | VMMCALL_HV_VMCLOSURE_INVOCATION | >=3.00 | VMClosure invocation |
| 0x0F | VMMCALL_HV_STARTUP_MP | >=3.00 | Start MP (AP) boot |
| 0x10 | VMMCALL_HV_DISABLE_STARTUP_MP | >=3.00 | Disable MP startup |

7 of 17 hypercalls are IOMMU-related (0x06-0x0C) — the most complex hypercall category.

### VM Exit Events

VM exits transition guest to hypervisor context:
- CPUID: intercepted for virtualization; PS4 compatibility CPUID spoofing
- RDPRU: intercepted with #GP injection; prevents user-mode access to processor performance registers
- CR0/CR4/EFER writes: intercepted when modified bits in filter masks
- MSR accesses: intercepted when matching MSRPM
- NPT violations: guest access violating stage-2 permissions
- IOMMU operations: SMMU faults from DMA devices
- HLT/INVD/INVLPG: configured to cause VM exits
- Hypercalls: vmmcall causes VM exit for servicing

### FW >=3.00 vs <=2.70 Architecture

| Aspect | FW <=2.70 | FW >=3.00 |
|--------|-----------|-----------|
| HV location | Embedded in kernel binary | Standalone component |
| Boot stages | SBL -> HV -> Kernel | SBL -> HyLonome -> HV -> Kernel |
| AP boot | Kernel-controlled | HV-controlled (0x0F, 0x10) |
| VMClosure | Not present | Available (0x0E) |
| Public HV exploits | Byepervisor, TMR, flatz | TMR (<=6.02 only) |
| Exploit difficulty | Lower | Significantly higher |

## Kernel Architecture Detail

### System Call Interface

The PS5 syscall table (documented from kernel 2.20) is organized into ranges:
- 0x00-0x5F: Standard BSD syscalls (exit, read, write, open, close)
- 0x60-0x8F: Extended BSD and networking (socket, connect, bind, listen, ioctl at 0x36)
- 0x90-0xFF: POSIX extensions (kqueue, signals, scheduling)
- 0x100-0x17F: Modern BSD syscalls (aio, kld, mac, sched)
- 0x180+: PS4/PS5 specific syscalls

Three sysvec structures handle binary dispatch:
1. PS4 SELF sysvec: PS4 backward-compatible executables
2. FreeBSD ELF64 sysvec: Standard FreeBSD binaries (unused on production)
3. Native SELF sysvec: All native PS5 processes

### SceSbl Secure Module Dispatch

20+ secure modules identified by 0x8002xxxx service IDs, loaded by the kernel during boot:

| ID | Name | Key Functions |
|----|------|--------------|
| 0x80021000 | authmgr | SELF verification (sceSblAuthMgrAuthHeader), segment loading (sceSblAuthMgrLoadBlock), SM load |
| 0x80021001 | kms | Key slot allocation (sceSblKmsAllocKmbSlotForPprPkg), key ID set/clear |
| 0x80021002 | pup | PUP firmware update verification (sceSblPupExpirationGetStatus) |
| 0x80021003 | pfs | PFS ICV table updates (sceSblPfsmgrUpdateIcvTable), save data auth codes |
| 0x80021004 | driveauth | BD drive authentication, AACS/CPRM key retrieval |
| 0x80021005 | pltauth | Platform challenge/response (sceSblPltAuth2GenC1, sceSblPltAuth2VeriR1C2GenR2) |
| 0x80021006 | npdrm | NP DRM, debug clock check |
| 0x80021007 | devact | Device activation (sceSblDevActGetId, passcode generation/verification) |
| 0x80021008 | qafutkn | QA feature token management |
| 0x80021009 | sysveri | System verification |
| 0x8002100A | otpaccess | OTP fuse read-only access |
| 0x8002100B | manu | Manufacturing mode (set/get manu mode, load/unload secure module) |
| 0x8002100C | fttrm | Film/TV tracking rights management |
| 0x8002100D | srtc | Secure RTC (sceSblSrtcGetCurrentSecureTick) |
| 0x8002100E | rootparam | Root parameter verification |
| 0x8002100F | exthdd | External HDD metadata verification |
| 0x80021010 | cloudsd | Cloud save data encryption/sync |
| 0x80021011 | bar | Backup and Restore encryption |
| 0x80021012 | otprsvaccess | Additional OTP regions |
| 0x80021013 | diskid | Disc unique identifier |
| 0x80021014 | idata | Identity data |
| 0x80021015 | ddd | Unknown |
| 0x80021016 | otpctrl | OTP fuse programming |
| 0x80021017 | ncdt | Unknown |
| 0x80021018 | hidauth | HID device authentication |

### IOCTL Device Interface

100+ kernel device entries under /dev/:

Notable devices:
- /dev/pup_update0: firmware update processing (DecryptPupHeader, DecryptPupSegment, VerifyPupAdditionalSign, VerifyPupWatermark, ReadNandGroup, WriteNandGroup)
- /dev/pfsctldev, /dev/pfsmgr, /dev/nsfsctl: PFS filesystem control
- /dev/sflash0: Serial flash access (2 MB)
- /dev/bar: Backup and Restore
- /dev/duid: Disc Unique Identifier
- /dev/dldbg: Dynamic Library Debug
- /dev/fttrm: Film/TV rights management (Blu-ray DRM)
- /dev/icc_floyd: TPM (Trusted Platform Module)
- /dev/manuauth: Manufacturer authorization
- /dev/rootparam: Root PARAM.SFO/JSON verification
- /dev/wlanbt: Wireless LAN + Bluetooth

TEE IOCTLs (Trusted Execution Environment communication):
- TEE_IOC_VERSION, TEE_IOC_OPEN_SESSION, TEE_IOC_CLOSE_SESSION, TEE_IOC_INVOKE
- TEE_IOC_DLM_START_TA_DEBUG (0xC028B409), TEE_IOC_DLM_FETCH_DEBUG_STRING (0xC110B40A)
- TEE_IOC_DLM_STOP_TA_DEBUG, TEE_IOC_DLM_GET_DEBUG_TOKEN

Manufacturing IOCTLs:
- sceSblManuAuthSetManuMode (0xC0184D03)
- sceSblManuAuthUnloadSecureModule (0x40184D02)
- sceSblManuAuthLoadSecureModule (0x40184D01)

## Key Hierarchy

### ROM Keys
Multiple 256-byte keyseed sets (Keys 2-9) embedded at manufacturing time:
- Key 2: RSA key for boot authentication and UCMD verification
- Key 3: Additional RSA for UCMD backup
- Keys 4-9: Additional keyseeds for boot and runtime security

### PKG Metadata RSA-3072
Fully recovered RSA-3072 private key with complete CRT parameters (modulus N, public exponent E, private exponent D, primes P/Q, CRT components DP/DQ/QP). Used for package metadata signing. Does not affect boot security.

### Shared PS4 Keys (Cross-Generation Risk)
- SceShellCore trophy keys: identical to PS4
- Portability EncDec master keys (128-byte key, blob, IV, hash): shared with PS4
- Kernel NID default suffix: identical to PS4
- Passcode (512-byte symmetric key): shared with PS4 through Prospero tools

### M.2 Dummy Keys
Static key `01 23 45 67 89 01 23 45 67 89 01 23 45 67 89 01` used across FW 1.00-12.20. Well-known test key, suggesting placeholder rather than strong crypto.

### EMC/EAP/KBL Key Chain
- EMC IPL: AES-128-CBC key specific to revision c0
- EAP KBL: AES-128-CBC keys for kernel boot loader
- EAP kernel SELF: RSA-3072 + AES-128-CBC
- Communication Processor chain: HMAC-SHA1 integrity across all stages

## Auth IDs and PAIDs

Auth IDs (64-bit privilege-encoding prefixes):
- 41: Kernel modules (4100000000000001 = Secure Kernel, 4100000000000002 = Kernel)
- 48: System processes (4800000000000024 = ScePlayReady, 4800000010000005 = bdj.elf)
- 49: System libraries (4900000000000002 shared by hundreds of .sprx files)

PAIDs (Program Authority IDs): 64-bit values for process security domains.
- 4801000000000000: Kernel
- 4800000000000007: SceSysCore
- 4800000000000010: SceShellCore
- 480000000000000f: SceShellUI
