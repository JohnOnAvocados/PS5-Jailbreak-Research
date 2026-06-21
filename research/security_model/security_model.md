# PS5 Security Model

## Overview

The PlayStation 5 employs a deeply layered security architecture spanning hardware, firmware, hypervisor, kernel, and usermode. Each layer cryptographically verifies and enforces trust in the layer above before surrendering control. The boot chain originates in immutable on-chip ROM embedded within the AMD Platform Security Processor (PSP), a dedicated cryptoprocessor isolated from the main x86 CPU cores. The PSP validates and loads the Secure Loader IPL (Initial Program Loader) from a Winbond 25Q16JVNIM serial flash chip, which in turn authenticates the hypervisor, the hypervisor loader, the kernel, and all subsequent system modules using RSA-4096 signatures, SHA-256 hashes, and AES-CBC decryption. Compromise of any given security layer requires defeating every layer beneath it, creating a root-of-trust hierarchy.

The security model is built on a multi-faceted authentication system that categorizes code by privilege level. Auth IDs (64-bit identifiers with privilege-encoding prefixes) and Program Authority IDs (PAIDs) determine what resources each process can access and what security policies apply. Code is distributed in the SELF (Signed Executable and Linkable Format) binary format, which embeds cryptographic signatures, key identifiers, and metadata that SceSbl (Secure Boot Loader) verifies before loading. The PS5 inherits architectural concepts from the PS4 -- including the passcode system, portability keys, Keystone trust anchor, and trophy keys -- but introduces significant hardening: eXecute-Only Memory (XOM) is backed by hypervisor-enforced nested page tables for kernel-level protection, revision nonces prevent firmware downgrade attacks, and secure modules compartmentalize trusted services into individually sandboxed components.

The AMD Zen 2 CPU provides hardware security features that the PS5 leverages extensively: the PSP for isolated trusted execution, nested page tables (NPT) for hypervisor isolation, TMR (Trusted Memory Regions) for encrypted memory compartments, and the AMD Secure Technology framework. Despite this formidable defense-in-depth, the platform has been compromised at every layer through software exploits targeting race conditions, use-after-free vulnerabilities, integer overflows, stack buffer mismanagement, and speculative execution side channels. The vulnerability landscape spans 12 distinct kernel exploit classes, multiple hypervisor bugs across early firmware versions, a family of PS2 emulator JIT exploitation techniques (mast1c0re), ongoing browser-engine attack surface (WebKit, V8, SpiderMonkey), and architectural AMD Zen 2 vulnerabilities that are fundamentally hardware issues.

## Components

### Secure Boot Chain

The secure boot chain begins at power-on with the AMD PSP executing its immutable on-chip boot ROM. This ROM initializes the PSP's cryptographic engine, loads an embedded public key, and authenticates the next-stage firmware from the SPI-connected serial flash. The Winbond 25Q16JVNIM (16 MB / 128 Mbit) flash is connected to the southbridge via a standard SPI bus with the following signal mapping: chip select (`/S50_SSB_SF_CS`), serial clock (`S50G_SSB_SF_SCLK`), data input (`S50_SSB_SF_SIO0`), data output (`S50_SSB_SF_SIO1`). The write protect and hold/reset pins are tied to the 3.3V power rail (`3.3V_SS_PG1`). Physical access to this flash is the prerequisite for any hardware-level attack on the boot chain.

The Secure Loader IPL is located at NAND Group 0 offset 0x800 and identified by the magic bytes `E4 DB 7C 02`. Its header structure (0x400 bytes) contains:

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0x00 | 4 | Magic | `E4 DB 7C 02` |
| 0x04 | 4 | Header Size | Little Endian, always 0x400 |
| 0x08 | 4 | Entry Point | Little Endian, e.g. 0xB0 |
| 0x0C | 4 | Body Size | Little Endian, e.g. 0x631D0 |
| 0x10 | 0x10 | Padding | Zeroes |
| 0x20 | 0x20 | SHA-256 Hash | Of decrypted body, verified from 0x400 to 0x400+body |
| 0x40 | 0xB0 | Padding | ASCII `0123456789abcdef` with zeroes |
| 0xF0 | 1 | Flag | 0x80 |
| 0xF1 | 0x2B | Padding | Zeroes |
| 0x11C | 4 | Security Revision | Monotonic firmware version gate |
| 0x120 | 0x20 | Revision Nonce | SHA-256 of IPL revision identifier |
| 0x140 | 0xC0 | Metadata | Possibly keyrings and metadata digest |
| 0x200 | 0x200 | RSA-4096 Signature | Over the entire header |
| 0x400 | ~0x631D0 | Body | Double AES-CBC encrypted IPL payload |

The RSA-4096 signature covers the header up to offset 0x400. The PSP verifies this signature using its embedded public key, ensuring the IPL has not been tampered with. After signature verification, the PSP uses the Revision Nonce and Security Revision to enforce downgrade protection: each firmware release increases the revision value embedded in the header, and the PSP refuses to boot any IPL with a revision lower than the last successfully booted value (stored in fuses or OTP memory).

Security revision values have evolved across firmware generations:

| Hex Value | Firmware Range |
|-----------|----------------|
| `00 00 00 01` | 0.85.007 through 1.XX |
| `00 00 00 07` | 1.00 through 6.02 |
| `00 00 00 FF` | 6.50 |
| `00 00 03 FF` | 7.00 through 7.61 |
| `00 00 0F FF` | 8.00 through 8.60 |
| `00 00 3F FF` | 9.00 through 9.60 |
| `00 00 FF FF` | 10.00 through 10.60 |
| `00 03 FF FF` | 11.00 and later |

The Revision Nonce is a SHA-256 hash uniquely identifying each IPL revision. Known nonces include:

| Revision | SHA-256 Hash |
|----------|-------------|
| 0xA0 | `E3 D9 8F 94 6E B3 2A 6D C8 A8 09 C2 6B 6F 4F 91 0E CA 63 59 00 48 4D 99 BA 12 39 E5 DF 74 5C 40` |
| 0xB0 | `55 18 14 A6 79 F1 4D 09 31 8B EC 56 DD EA 43 44 55 27 9A C4 7D 0C 5C 7E 14 91 D6 EF B2 1F 2B 48` |
| 0xC0 | `B3 59 79 B6 23 19 7C 34 6E E6 B1 62 8E 18 98 96 8C 66 DC DF 1C 96 5F 4C 77 07 30 07 78 4C 4E 6A` |
| 0xD0 | `1C B3 91 12 79 BA 5E 83 42 C9 C9 6B 2F C5 49 B3 DE BF D7 3D D6 B6 97 4E 07 84 DF 7B E8 BD 21 39` |
| 0xE0 | `FD 50 C2 9C C4 AE 88 21 1B CA 0B C5 09 1C 1D BF D6 A4 DC 07 DB F8 C0 B2 A6 17 FD 1D BE E0 3A 3B` |
| 0xF0 | `6F 20 B4 5B 4F CB 66 67 71 5F 4B 0E E4 90 7C C2 CB 41 47 0A 59 B2 26 E0 D4 F0 D0 1B 67 E8 80 50` |
| 0x100 | `50 C0 E3 99 33 83 2B 2B A6 89 FF AE 29 4A 44 92 03 8E 99 74 A8 BC A6 CC 0C 2E 9C 69 9D 37 2A 22` |

After the PSP authenticates and decrypts the IPL, the IPL body gains execution on the main CPU and proceeds to load the next-stage components: the Hypervisor, Hypervisor Loader, and Kernel. Each component is independently signed and verified. The IPL checks that the Security Revision in its own header is acceptable, and similarly verifies that the hypervisor and kernel revisions meet the required minimums. This chain of cryptographic verification ensures integrity from the first instruction to the fully booted OS.

### Cryptographic Keys

The PS5 employs an extensive key hierarchy covering boot authentication, content protection, DRM, peripheral pairing, and debug access. Many keys are shared with the PS4 for cross-generation compatibility, which creates a potential cross-platform attack surface.

**ROM Keys**: Multiple 256-byte keyseed sets designated Key 2 through Key 9 are embedded in hardware at manufacturing time. Key 2 is an RSA key used for UCMD (User Command) authentication in conjunction with Key 3. These keys are accessible only to the PSP and never exposed to the main CPU.

**PKG Metadata RSA-3072**: A fully recovered RSA-3072 private key used for signing PKG (package) metadata. The key includes all CRT parameters: modulus N, public exponent E, private exponent D, prime factors P and Q, and the CRT components DP, DQ, and QP. Possession of this key enables forging package metadata, which would allow installation of arbitrary content.

**SceShellCore Trophy Keys**: Identical to the PS4 trophy key set. Used to sign and verify trophy (achievement) data. The shared key means any PS4 trophy key leak directly compromises PS5 trophy integrity.

**Kernel NID Default Suffix**: The default suffix for kernel Name-to-ID (NID) resolution is identical to the PS4 value. NIDs are used to obfuscate symbol names in system modules; knowing the default suffix aids in reverse engineering kernel exports.

**Passcode Key**: A 512-byte symmetric key distributed through Prospero Publishing Tools. This key is used for authenticating developer/debug console access. APIs such as `_sceSblDevActSmGenPassCodeData` and `_sceSblDevActSmCheckPassCodeData` in SceSbl generate and verify passcode data against this key.

**Portability EncDec Master Keys**: 128-byte master key, blob, initialization vector (IV), and hash shared with PS4. Used for encrypting and decrypting content and save data across PS4 and PS5 platforms to enable cross-generation portability.

**Envelope File Keys**: RSA workaround_ctl public verification key and master key verification material. Envelope files (`sceSblEnvelopeOpen`, `sceSblEnvelopeOpen2`) wrap cryptographic operations in authenticated structures, providing a controlled API for key usage without exposing the key material directly.

**M.2 Dummy Keys**: The key `01 23 45 67 89 01 23 45 67 89 01 23 45 67 89 01` is used across firmware versions 1.00 through 12.20 for authenticating M.2 SSD expansion storage. This is a well-known test key, suggesting that M.2 authentication may be a placeholder or compatibility feature rather than a strong security boundary.

**RNPS Keys**: Remote Network Package Service uses AES-128-CBC MAC keys for integrity and RSA-2048/RSA-3072 key pairs for signing. RNPS enables network-based package delivery with cryptographic content verification.

**EMC IPL Cipher Key**: An AES-128-CBC key specific to PS5 EMC revision c0. Used by the PSP to decrypt the EMC firmware image during the boot process.

**EAP KBL Keys**: AES-128-CBC keys used by the Embedded Application Processor (EAP) to decrypt the kernel during the EAP boot path. The EAP is a southbridge co-processor that assists with system management.

**EAP Kernel SELF Keys**: An RSA-3072 key pair and a separate cipher key used to sign and encrypt EAP kernel SELF modules. This ensures only Sony-signed EAP kernel code can execute on the southbridge.

**Communication Processor Key Chain**: A complete key hierarchy covering EMC, EAP, and KBL (Kernel Boot Loader) stages, authenticated with HMAC-SHA1. This chain links the southbridge co-processors into the overall boot trust model.

**Key Rings**: Managed by the PSP, these contain cryptographic keys for various boot stages and services. The PSP provides controlled access to key rings through SceSbl's key management service (`sceSblKmsSetKeyId`, `sceSblKmsAllocSignedKeyHdl`, `sceSblKmsClearKeyId`). Keys are identified by opaque handles and never exposed in plaintext to untrusted code.

### Secure Modules (SCE SBL)

Secure modules are trusted service executables identified by unique `0x8002xxxx` IDs, loaded and managed by the SceSbl subsystem. Each module runs in an isolated execution context and provides a specific security-critical service through a controlled API surface. The modules are loaded as SELF binaries and authenticated through the standard SceSbl authentication pipeline.

The complete known module roster:

| ID | Name | Service |
|----|------|---------|
| `0x80021000` | authmgr | Authentication Manager: core SELF verification, segment decompression check, ELF segment extraction, SELF info retrieval, multi-block loading, block-level loading with callbacks. Both synchronous (`sceSblAuthMgr*`) and secure monitor (`_sceSblAuthMgrSm*`) variants exist. |
| `0x80021001` | kms | Key Management System: key ID allocation and deallocation (`sceSblKmsSetKeyId`, `sceSblKmsClearKeyId`), signed key handle allocation (`sceSblKmsAllocSignedKeyHdl`), key handle transcription to key IDs (`sceSblKmsTranscribeKeyHdl2KeyId`), KMB slot allocation (`sceSblKmsAllocKmbSlot`). |
| `0x80021002` | pup | PUP (PS5 Update Package) firmware update verification. Handles `sceSblPupExpirationGetStatus` for checking update expiration policies. |
| `0x80021003` | pfs | PlayStation File System: encrypted filesystem operations including `sceSblPfsClearKey`, `sceSblPfsSaveDataUpdateAuthCode`, `_sceSblPfsSaveDataUpdateAuthCodeIoctl`, and `sceSblPfsmgrUpdateIcvTable` for integrity-check value table management. |
| `0x80021004` | driveauth | Drive Authentication: optical disc pairing and authentication. Functions include `sceSblDriveauthGetId2`, `sceSblDriveauthGetAacsDeviceKey`, `sceSblDriveauthGetCprmDeviceKey`, `sceSblDriveauthGetGicData`, `_sceSblDriveauthSmDriveData`, `_sceSblDriveauthSmSetHostKey`, `_sceSblDriveauthSmGetPairingInfo`, `_sceSblDriveauthSmRemoveDiscKey`. Also handles PS4 disc authentication (`sceSblDriveAuthPs4Disc`, `sceSblDriveAuthRegisterPs4Disc`, `sceSblDriveAuthUnregisterDisc`). |
| `0x80021005` | pltauth | Platform Authentication: mutual challenge-response protocol. `sceSblPltAuth2GenC1` generates challenge C1, `sceSblPltAuth2VeriR1C2GenR2` verifies response R1 and generates C2/R2, `sceSblPltAuth2GetKdsMac` retrieves key-derived MAC, and `sceSblPltAuth2Initialize` sets up the authentication session. |
| `0x80021006` | npdrm | Network Product DRM: manages debug clock state (`sceSblNpDrmCheckDebugClock`), debug tick (`sceSblNpDrmGetCurrentDebugTick`, `sceSblNpDrmSetCurrentDebugTick`), and initialization status (`sceSblNpDrmGetInitStatus`). |
| `0x80021007` | devact | Device Activation: developer/debug console activation. Functions for generating activation headers (`_sceSblDevActSmGenActHeader`), activation requests (`_sceSblDevActSmGenActRequest`), passcode data (`_sceSblDevActSmGenPassCodeData`), checking passcode data (`_sceSblDevActSmCheckPassCodeData`), status management (`_sceSblDevActSmInitStatus`, `_sceSblDevActSmSetStatus`, `_sceSblDevActSmDeleteStatus`, `_sceSblDevActSmExit`), and reading device ID (`sceSblDevActGetId`, `_sceSblDevActSmGetId`). |
| `0x80021008` | qafutkn | QA/Utoken: QA feature token management including `sceSblRcMgrGetQafDescription`, `sceSblRcMgrGetQafExpirationTime`, `sceSblRcMgrGetQafGeneration`, and `sceSblRcMgrIsStoreMode` for region/store policy checks. |
| `0x80021009` | sysveri | System Verification: integrity checking of system files and installation state. |
| `0x8002100A` | otpaccess | OTP Access: read-only access to one-time programmable memory regions containing device-unique keys and serial numbers. |
| `0x8002100B` | manu | Manufacturing: controls manufacturing mode (`sceSblManuAuthSetManuMode`, `sceSblManuAuthGetManuMode`), manufacturing expiration (`sceSblManuAuthGetManuExpire`, `sceSblManuAuthSetManuExpire`), and secure module loading in manufacturing context (`sceSblManuAuthLoadSecureModule`, `sceSblManuAuthUnloadSecureModule`). |
| `0x8002100C` | fttrm | FTT RM (Film/TV Tracking Rights Management): DRM enforcement for video content, tracking usage rights and license compliance. |
| `0x8002100D` | srtc | Secure RTC: secure real-time clock services. Returns secure tick values via `sceSblSrtcGetCurrentSecureTick` and NP DRM tick values via `sceSblSrtcGetCurrentNpDrmTick`. |
| `0x8002100E` | rootparam | Root Parameter: system root configuration parameters, likely including console-unique identity data. |
| `0x8002100F` | exthdd | External HDD: authentication and encryption key management for external USB storage devices. |
| `0x80021010` | cloudsd | Cloud SaveData: encryption, authentication, and synchronization of cloud-stored save data. |
| `0x80021011` | bar | Backup and Restore: encryption and integrity verification for system backup archives. |
| `0x80021012` | otprsvaccess | OTP Reserved Access: additional OTP memory regions with restricted access patterns. |
| `0x80021013` | diskid | Disk ID: retrieval and management of unique disk identifiers for disc-based authentication. |
| `0x80021014` | idata | Identity Data: console identity information management. |
| `0x80021015` | ddd | Unknown function, likely debugging or diagnostics. |
| `0x80021016` | otpctrl | OTP Control: programming control for OTP memory, likely restricted to manufacturing flow. |
| `0x80021017` | ncdt | Unknown function. |
| `0x80021018` | hidauth | HID Authentication: authenticates Human Interface Devices (controllers, peripherals) through cryptographic pairing protocols. |

The SceSbl library exposes the full API surface for these modules. Beyond module-specific functions, it provides general security services: cryptographic operations (`sceSblServiceCrypt`, `sceSblServiceCryptAsync`, `sceSblServiceMailbox`), secure boot region management (`sceSblSecRegInitialize`, `sceSblSecRegResume`, `sceSblSecRegSuspend`), memory protection (`sceSblMp1Initialize`, `sceSblMp1DumpContext`, `sceSblMp1EnableErrorDetection`, `sceSblMp1DisableErrorDetection`), Trusted Memory Region mapping (`sceSblTmrMap`, `sceSblTmrUnmap`, `sceSblTmrEncAmmPt`, `sceSblTmrDecAmmPt`, `sceSblTmrExport`), Secure Video Path TEE management (`sceSblSvpMapPrdyTeeArea`, `sceSblSvpUnmapPrdyTeeArea`), random number generation (`sceSblRngGetRandomNumber`), display content protection (`sceSblDcnOpenScanInRegion`, `sceSblDcnOpenScanOutRegion`, `sceSblDcnCloseScanOutRegion`), and driver-level communication (`sceSblDriverSendMsg`, `sceSblDriverSendMsgPol`).

### eXecute-Only Memory (XOM)

XOM (eXecute-Only Memory) is a memory protection primitive that prevents read accesses to designated pages while permitting instruction execution. The PS5 is among the very few x86-based systems to implement this mechanism, which was pioneered on ARM architectures (ARM XOM / PXN). This provides strong protection against code dumping and static reverse engineering.

**Operation**: When the CPU processes a memory read targeting a XOM-marked page, the Page Table Entry (PTE) is checked. If the XOM bit is set, a page fault exception is raised. This exception is vectored to the hypervisor for handling. On an uncompromised hypervisor, the exception handler triggers a kernel panic, killing the offending process. Instruction fetches are not blocked -- the page remains executable, hence the name "eXecute-Only."

**Usermode XOM**: Enforced on all PS5 game titles and system applications. The kernel sets the XOM bit on every usermode code page during module loading. This prevents an attacker with usermode code execution from dumping game binaries to search for gadgets or reverse engineer proprietary algorithms. With kernel read/write access (obtained through a kernel exploit), usermode XOM can be bypassed by clearing the XOM bit on the target PTEs. The change takes effect after flushing the Translation Lookaside Buffers (TLBs) for the affected virtual address range. This makes usermode XOM a speed bump rather than a barrier once kernel-level access is achieved.

**Kernel XOM**: The PS5 kernel protects its own `.text` pages with XOM, creating a deeper obstacle. Because the kernel page tables are shadowed by the hypervisor through nested page tables (NPT) -- a hardware virtualization feature of AMD-V -- simply modifying the kernel's own page tables from within the kernel does not clear XOM. The nested page tables controlled by the hypervisor independently enforce XOM, and the kernel cannot modify them. This creates a chicken-and-egg problem: reverse engineering the hypervisor requires understanding how it processes XOM faults, but that requires reading kernel .text, which requires disabling kernel XOM, which requires hypervisor compromise. Kernel XOM therefore forces attackers to find hypervisor-level bugs, which are significantly rarer and harder to exploit than kernel bugs.

**Performance Considerations**: XOM interacts poorly with some CPU features. The PS5 likely excludes certain pages (e.g., `__patchable_function_entries`, hotpatch regions) from XOM to support system update patching. Additionally, the TLB flush requirement after XOM bit changes means any runtime code modification has a measurable performance cost.

### EMC (Error Management Controller)

The EMC (Embedded Micro Controller) is a co-processor using hardware revision CXD90061GG that handles low-level system initialization, power management, and error handling during boot. It operates independently of the main x86 CPU and has its own firmware image stored in the serial flash.

EMC firmware versions span the PS5's lifecycle:

| Version | Firmware Range | Target |
|---------|----------------|--------|
| v0.7.6 | SDK 0.85.070 | Prototype/DevKit |
| v1.0.4 | FW 1.01-1.14 | TestKit, Retail |
| v1.2.3 | FW 2.XX | TestKit |
| v1.4.2 | FW 3.00 | Retail |
| v1.6.0 | FW 4.00 | TestKit |
| v1.8.2 | FW 5.00 | Retail |
| v1.8.3 | FW 5.50 | Retail |
| v1.14.3 | FW 9.20 | Retail |

The EMC firmware is stored in the serial flash at offset 0x4000 with length 0x7E000 bytes. It uses the SLB2 segment format and can be extracted with the `blsunpack` tool. The C0080001 file within the extraction contains the EMC version string. The EMC IPL is encrypted with AES-128-CBC using a key specific to PS5 EMC revision c0, ensuring that only authorized EMC firmware can execute.

The EMC firmware magic (`AA F9 8F D4`) distinguishes it from other boot components in the serial flash layout. The EMC is part of a broader communication processor key chain that links the EMC, EAP (Embedded Application Processor), and KBL (Kernel Boot Loader) with HMAC-SHA1 authentication. This chain ensures that all southbridge co-processors are running authenticated firmware that is cryptographically tied to the main boot chain.

### Keystone

Keystone is a hardware/software trust anchor mechanism inherited from the PS4 architecture. It provides a measured boot capability where each stage of the boot process extends a set of Platform Configuration Registers (PCRs) with cryptographic hashes of the next-stage code before execution. The resulting measurements can be used for remote attestation and local policy decisions.

The primary API surface is `sceSblSsVerifyKeystone` in SceSbl, which verifies the keystone measurement against expected values. Keystone likely underpins content protection policies: a media player can verify that the system is in an approved boot configuration before decrypting premium content. While the PS5-specific Keystone implementation details remain undocumented, its presence in the SceSbl API confirms it plays an ongoing role in runtime security enforcement rather than being a legacy compatibility feature.

### CP Box

The CP Box (model CPBH-100) is a hardware test/debug accessory that connects to a PS5 TestKit via USB-C. It provides two operating modes: Engineering Mode (CP Box powered, USB-C connected to PS5 only) and Normal Mode (USB-C to a portable HDD plus Ethernet to a development network plus USB-C to PS5). The Ethernet port (labeled DEV LAN) connects to a host computer for remote debugging, log capture, and build deployment.

Status LEDs provide operational feedback: CP INIT, NETWORK INIT, SPEED, LINK/ACT, and STATUS. Without a CP Box connected, the TestKit boots in Release Mode with debug capabilities disabled. When a CP Box is connected at power-on, the TestKit can enter Assist Mode, which provides enhanced debugging support. This mode persists in memory across power cycles (until explicitly cleared).

The CP Box is not hot-pluggable -- the PS5 checks for its presence during the power-on sequence and displays an error if the CP Box is connected after boot. It can read PS5 information (serial number, operating mode) even while the PS5 is shut down, indicating it has independent power and communication capability through the USB-C connection. A prototype revision (CPB-K01) used a CXD90046GG main chip with dual CP systems for recovery and normal operation. After cpupdate version 2700, the VR port (USB-C) activates to support PS VR2 connectivity.

The CP Box represents the hardware root of debug authority: without physical possession of this device, a TestKit cannot access full debug capabilities, ensuring that development hardware in the field cannot be trivially converted to debug-enabled units.

### Authentication

The PS5 employs a multi-layered authentication framework that governs which code can execute at each privilege level and what resources each process can access.

**Auth IDs**: 64-bit identifiers that categorize code modules by privilege level. The prefix encoding is:

| Prefix | Privilege Level | Description |
|--------|-----------------|-------------|
| `41` | Kernel | Secure Kernel and Kernel modules |
| `48` | System Process | System applications and services |
| `49` | System Library | Shared system libraries (.sprx files) |

Known Auth IDs and their associated modules:

| Auth ID | Module Path |
|---------|-------------|
| `4100000000000001` | Secure Kernel |
| `4100000000000002` | Kernel |
| `4800000000000024` | /system/common/lib/ScePlayReady.self |
| `480000000000003b` | /system/common/lib/ScePlayReady2.self |
| `4800000000010001` | /system/sys/set_upper.self |
| `4800000000001006` | /system/vsh/app/NPXS40038/eboot.bin (shared by many VSH apps) |
| `4800000000010003` | ./sys/decid.elf |
| `4800000000000005` | ./sys/orbis_audiod.elf |
| `4800000000000007` | ./sys/SceSysCore.elf |
| `4800000000000010` | ./vsh/SceShellCore.elf |
| `4800000010000001` | /system_ex/app/NPXS40140/BdmvPlayerCore.elf |
| `4800000010000005` | /system_ex/app/NPXS40140/cdc/bin/bdj.elf |
| `4800000010000010` | /system/vsh/app/NPXS40109/webrtc_daemon.self |
| `4900000000000002` | Shared by hundreds of system libraries in /system/common/lib/, /system/priv/lib/, /system_ex/, etc. |
| `4900000000000007` | libSceGnmDriver.sprx, libSceGnmDriverCompat1.sprx, libSceGnmDriverForNeoMode.sprx |
| `4900000000000003` | /system_ex/app/NPXS40140/libAacs.sprx |
| `4900000000000006` | /system_ex/app/NPXS40140/libBdplus.sprx |

**Program Authority IDs (PAIDs)**: 64-bit values assigned at process creation that determine the process's security domain and resource access policies. The kernel and secure loader use PAIDs to enforce mandatory access control. PAID `4801000000000000` denotes kernel-level authority; all system processes use PAIDs with prefix `4800`.

Notable PAID-to-process mappings:

| PAID | Process |
|------|---------|
| `4801000000000000` | Kernel |
| `4800000000000022` | mini-syscore.elf |
| `4800000000000007` | SceSysCore.elf |
| `4800000000000005` | orbis_audiod.elf |
| `4800000000000009` | AgcCompositor.elf |
| `4800000000000010` | SceShellCore |
| `480000000000000f` | SceShellUI |
| `4800000000000015` | SceAvCapture |
| `4800000000000012` | SceGameLiveStreaming |
| `4800000000000014` | ScePartyDaemon |
| `4800000000001004` | SceMediaCoreServer |
| `4800000000000019` | SceRemotePlay |
| `4800000000000028` | ScePsNowClientDaemon |
| `480000001000000e` | SceSpZeroConf |
| `4800000000000037` | SceSocialScreenMgr |
| `480000000000003e` | SceVoiceAndAgent |
| `4800000000001003` | SceRedisServer |
| `4800000000001002` | SceJSCd |
| `480000000000100b` | SceSystemLogger2 |
| `480000000000100d` | SceUpdatePupUtil |
| `4800000000001015` | SceVrTrackerDaemon |
| `480000000000001d` | fs_cleaner.elf |
| `4800000010000010` | webrtc_daemon.self |
| `4800000000001005` | SceVideoCore2K |
| `4800000010000009` | SceDiscPlayer |
| `4800000010000001` | BdmvPlayerCore.elf |
| `4800000010000005` | bdj.elf |
| `480000000000001f` | SceSysAvControl.elf |

**Magics**: 4-byte binary identifiers that allow boot components to recognize different binary formats before full parsing:

| Magic (Hex) | Component | Purpose |
|-------------|-----------|---------|
| `54 14 F5 EE` | Certified File (SELF, PUP) | All signed executables and update packages |
| `E4 DB 7C 02` | IPL / Secure Loader | Initial Program Loader header |
| `AA F9 8F D4` | Southbridge EMC | EMC firmware image |
| `1D 33 47 77` | EAP Kernel / EAP KBL Firmware | Embedded Application Processor firmware |
| `47 AB 6B EF` | Floyd ICC Firmware | ICC (Image Capture Controller) firmware |
| `55 AA 6B E9` | VBIOS | Video BIOS for GPU initialization |
| `5F 46 56 48` | BIOS | Main system BIOS |

**Passcode**: A security authentication system inherited from the PS4 for development and debug console authorization. The passcode is a 512-byte key provisioned through Prospero Publishing Tools. It is used to unlock debug features on TestKits and DevKits. The SceSbl API provides generation (`_sceSblDevActSmGenPassCodeData`), verification (`_sceSblDevActSmCheckPassCodeData`), and status management functions. Without a valid passcode, debug consoles operate in restricted mode, limiting developer access to system internals.

### AMD Platform Security Processor (PSP)

The AMD Platform Security Processor, officially branded as AMD Secure Technology, is a dedicated ARM-based cryptoprocessor integrated into the AMD Zen 2 SoC. It serves as the hardware root of trust for the entire PS5 platform. The PSP runs its own firmware, has exclusive access to secure key rings and OTP memory, and operates independently of the main x86 CPU cores.

**Functional Role**: The PSP is the first processor to execute at power-on. Its boot ROM is immutable (mask ROM), guaranteeing a trustworthy starting point. The PSP initializes cryptographic engines, verifies the Secure Loader IPL signature using RSA-4096, decrypts the IPL using AES-CBC with keys from its secure key rings, and then monitors system behavior for anomalies during boot. It likely executes secure modules directly within its isolated execution environment.

**Historical Context**: The PSP is the latest in a lineage of Sony console security processors: SAMU on PS4 (dedicated security co-processor), CMeP on PS Vita (context-aware memory protection), and Kirk on PSP (hardware crypto engine). Each generation has consolidated more security functionality into the dedicated processor.

**Security Guarantees**: Because the PSP has its own memory and execution environment, even a fully compromised kernel running on the x86 cores cannot read PSP key material or modify PSP firmware. The PSP controls access to OTP fuses (used for security revision tracking and device-unique keys) and can enforce security policies independently of the main CPU. External research resources include UEFI PlugFest documentation and the PSPReverse open-source project.

**Limitations**: The PSP is itself a piece of software running on a general-purpose ARM core, making it theoretically vulnerable to firmware exploits. Any vulnerability in PSP firmware that allows code execution or memory readout would bypass all higher-layer security, as the PSP is the root of trust for the entire boot chain. Such exploits are extremely rare and valuable.

### Vulnerabilities

The PS5 has been compromised at every security layer through diverse vulnerability classes. The following catalogs the known vulnerability landscape by layer:

**Usermode / Application-Layer Exploits**:

The Blu-ray Java attack surface has been the most prolific usermode entry point. BD-JB (FW <=4.51) comprised 5 distinct bugs discovered by TheFloW targeting the BD-J Java environment. BD-JB2 (FW <=7.61) exploited a path traversal vulnerability in the Blu-ray Java implementation, patched in FW 8.00. BD-JB-EX (FW <=12.70) extended the technique to later firmware versions.

Browser-engine exploits have been used for initial userland access. The WebKit `loadInSameDocument` use-after-free (CVE-2022-22620) affected FW <=5.50. A CSSFontFaceSet bug affected FW 3.00-4.51. The YouTube application (Y2JB) leverages V8 CVE-2021-38003, a `JSON.stringify` TheHole value leak that provides V8 engine access on FW 2.00-13.40 -- notably remaining unpatched as of FW 13.40. The Netflix application has been exploited across FW 4.03-12.40 using multiple V8 and SpiderMonkey CVEs, patched in FW 12.60.

The mast1c0re exploit family targets the PS2 emulator's JIT (Just-In-Time) compiler. By crafting specific PS2 save data (via Lua, Ren'Py, or YARPE game engines), attackers trigger the PS2 emulator JIT to emit and execute native x86 code. This provides usermode code execution without exploiting kernel bugs.

**Kernel Exploits**:

The kernel has been the most targeted layer, with a steady cadence of discoveries:

- **kqueueex (P2JB)**: A use-after-free in the kqueue subsystem caused by an `ucred` (user credential) refcount leak. When a kqueue event fires after the associated credential structure has been freed, it yields a kernel read/write primitive. Affected FW <=12.70, patched in FW 13.00.

- **netcontrol**: A double `fdrop` (file descriptor drop) on a socket file descriptor. Calling `fdrop` twice on the same socket causes a use-after-free in the file descriptor table. Affected FW <=12.00.

- **fsc2h_ctrl**: A kernel stack buffer management error where a stack-allocated structure is incorrectly freed during an ioctl operation. Affected FW <=10.40.

- **aio_multi_delete**: A double free vulnerability in the asynchronous I/O subsystem caused by improper locking during concurrent `aio_multi_delete` operations. Affected FW <=10.01.

- **umtx_shm (UMTX2, CVE-2024-43102)**: A use-after-free race condition in the user-space mutex shared memory subsystem. Two threads racing during umtx_shm operations can trigger a free while another thread retains a reference. Affected FW <=7.61.

- **IPV6_2292PKTOPTIONS (CVE-2020-7457)**: A use-after-free in the IPv6 socket option handler. An old FreeBSD vulnerability ported to the PS5 kernel. Affected FW 3.00-4.51.

- **GPU DMA Copy**: The GPU's DMA engine can read and write kernel `.data` pages even when the CPU has write-protected them. By submitting crafted GPU command buffers, attackers bypass the kernel's `.data` write protection. Affected FW >=6.00 (introduced with a GPU driver change).

- **exFAT Overflow**: A buffer overflow in the exFAT filesystem driver triggered by a maliciously crafted exFAT volume image.

- **SMAP Bypass**: Techniques to bypass Supervisor Mode Access Prevention, allowing kernel code to read/write usermode pointers without the usual SMAP fault.

**Hypervisor Exploits**:

Hypervisor bugs are the most valuable due to the hypervisor's position above the kernel in the privilege hierarchy:

- **TMR Heap Out-of-Bounds**: TheFloW discovered a heap out-of-bounds vulnerability in the Trusted Memory Region manager within the hypervisor. By crafting TMR operations that overflow adjacent heap allocations, an attacker could corrupt hypervisor-internal data structures. Affected FW <=6.02.

- **Byepervisor**: Two bugs in early firmware (<=2.70): a vtable pointer left in the readable data segment of the hypervisor (allowing vtable hijacking), and a debug flag that was not cleared when the system exited rest mode (allowing debug-mode escalation on resume).

- **Prosperous hypervisor exploit** (fail0verflow/flatz, 2026): A hypervisor compromise targeting FW <=4.51. The technique involved editing TMR protection state to gain arbitrary read/write in hypervisor memory space.

- **APIC Pointers**: Manipulation of Advanced Programmable Interrupt Controller data structures to hijack hypervisor execution flow.

**Hardware and Speculative Execution Vulnerabilities**:

The AMD Zen 2 microarchitecture is vulnerable to several speculative execution attacks that can leak sensitive data across privilege boundaries:

- **EntrySign (CVE-2024-36347)**: A vulnerability in the AMD Zen 2 signature verification mechanism that can bypass secure boot guarantees, potentially allowing unauthorized firmware to execute.

- **ZenBleed (CVE-2023-20593)**: A speculative execution side channel that leaks the contents of floating-point registers across process boundaries. Since the PSP and cryptographic operations use SIMD/floating-point registers, this could potentially leak key material.

- **Retbleed (CVE-2022-29900)**: A RET (return) instruction-based branch prediction hijack that allows cross-privilege speculative execution, bypassing existing Retpoline mitigations.

- **Inception / SRSO (CVE-2023-20569)**: Speculative Return Stack Overflow, allowing an attacker to poison the CPU's return stack predictor and speculatively execute arbitrary code sequences.

**Southbridge and Firmware Exploits**:

The southbridge co-processors (EMC, EAP, EFC) run their own firmware and communicate with the main system through shared memory and interrupt channels. Vulnerabilities in the communication protocol or firmware parsing can provide an alternative attack path that bypasses the main x86 security model. These attacks are less documented publicly but represent a growing area of research interest.

**Vulnerability Trends**: Across all layers, the dominant vulnerability class is use-after-free (kqueueex, umtx_shm, IPV6_2292PKTOPTIONS, netcontrol) followed by double free (aio_multi_delete, netcontrol) and logic bugs (BD-JB path traversal, GPU DMA bypass, hypervisor debug flag retention). Speculative execution vulnerabilities are architectural and will persist across Zen generations. The kernel vulnerability discovery rate suggests roughly one exploitable kernel bug per major firmware release cycle, with the hypervisor appearing substantially more resilient (no known public hypervisor exploit for FW >=7.00 as of mid-2026).

## Relationships

- [[hardware_overview]] -- every security primitive depends on the underlying AMD Zen 2 SoC hardware: PSP as root of trust, nested page tables for hypervisor-backed XOM, TMR for encrypted memory compartments, and the southbridge SPI flash layout for boot chain storage
- [[kernel]] -- the kernel enforces Auth ID and PAID-based access control, manages XOM page table entries for usermode processes, and implements the system call interface through which all SceSbl security services are accessed; kernel exploits (kqueueex, netcontrol, umtx_shm) provide the primary escalation path from userland
- [[hypervisor]] -- the hypervisor provides the highest software-layer isolation through nested page tables that back kernel XOM enforcement, manages TMR for encrypted memory regions, virtualizes APIC for interrupt control, and mediates all transitions between privilege levels; hypervisor compromise (TMR OOB, Byepervisor, Prosperous) grants full system control with no software restrictions
- [[firmware]] -- the secure boot chain spans the PSP boot ROM, Secure Loader IPL in serial flash, EMC/EAP/EFC southbridge firmware layers, and the hypervisor/kernel loading sequence; each firmware component has its own revision tracking and signature verification that must pass before execution proceeds

## Security Considerations

**Strengths**: The PS5 security architecture represents the state of the art in consumer device protection. The multi-layer approach ensures no single vulnerability provides complete compromise -- even a fully exploited kernel cannot disable kernel XOM without a separate hypervisor bug. The PSP isolates all key material from the main CPU, rendering memory-dump attacks ineffective against boot keys. The revision nonce system provides hardware-enforced downgrade prevention that cannot be bypassed by rewriting flash contents. The secure module architecture compartmentalizes trust: even if one module (e.g., npdrm) is compromised, other modules (e.g., kms, otpaccess) remain protected. The breadth of authentication identifiers (Auth IDs, PAIDs, magics) provides defense in depth, requiring attackers to forge or bypass multiple independent checks.

**Weaknesses**: The architectural decision to share keys and mechanisms with the PS4 introduces cross-generation attack surface. The trophy keys, portability EncDec keys, kernel NID suffix, and passcode system are all identical between generations, meaning leaks from the PS4 ecosystem directly impact PS5 security. The reliance on AMD for the PSP/CPU introduces systemic risk from speculative execution vulnerabilities (ZenBleed, Inception, Retbleed, EntrySign) that are fundamentally hardware issues and cannot be fully mitigated in software. The use of progressively obsoleted browser engines (WebKit on older FW, Chromium-derived V8 in YouTube/Netflix) creates a large and continuously evolving attack surface that Sony must patch reactively.

**Exploit Landscape Trends**: The kernel has been the most targeted layer with 12 distinct vulnerability classes exploited since launch. The median time between firmware release and public kernel exploit availability has decreased with each generation. Hypervisor exploits remain confined to FW <=6.02, suggesting the hypervisor is the most resilient layer and the primary barrier to full system compromise. The mast1c0re family represents a novel attack surface unique to the PS5 -- the PS2 emulator JIT introduces a code-execution path that bypasses standard content security policies. Browser-engine exploits (Y2JB, Netflix) provide the most accessible userland entry points and remain viable across broad firmware ranges.

**Future Research Directions**: Southbridge firmware analysis (EMC, EAP) represents an underexplored attack surface. PSP firmware reverse engineering could yield critical vulnerabilities that bypass all higher-layer security. The interaction between the AMD Secure Encrypted Virtualization (SEV) features and the PS5's custom hypervisor has not been publicly analyzed. The increasing complexity of secure modules and their inter-communication channels may introduce new attack surfaces in the module-to-module boundary.

## References

- https://www.psdevwiki.com/ps5/Keys
- https://www.psdevwiki.com/ps5/Secure_Loader
- https://www.psdevwiki.com/ps5/Secure_Modules
- https://www.psdevwiki.com/ps5/EMC
- https://www.psdevwiki.com/ps5/XOM
- https://www.psdevwiki.com/ps5/Keystone
- https://www.psdevwiki.com/ps5/CP_Box
- https://www.psdevwiki.com/ps5/Auth_IDs
- https://www.psdevwiki.com/ps5/Program_Authority_ID
- https://www.psdevwiki.com/ps5/Magics
- https://www.psdevwiki.com/ps5/Passcode
- https://www.psdevwiki.com/ps5/SceSbl_Functions
- https://www.psdevwiki.com/ps5/25Q16JVNIM
- https://www.psdevwiki.com/ps5/Vulnerabilities
- https://www.psdevwiki.com/ps5/AMD_Platform_Security_Processor
