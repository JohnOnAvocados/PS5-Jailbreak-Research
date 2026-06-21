# PS5 Boot Chain

## Overview

The PS5 boot chain is a multi-stage secure boot process that begins at power-on and proceeds through hardware initialization, firmware loading, cryptographic verification, and ultimately kernel launch. Each stage is responsible for loading and verifying the next, forming a chain of trust rooted in immutable hardware. The entire boot sequence is orchestrated by the AMD Platform Security Processor (PSP), a dedicated ARM-based cryptoprocessor that executes the on-die Boot ROM and manages all early boot security operations. The PSP handles RSA verification, AES-CBC decryption, SHA-256 hashing, and secure key ring management throughout the boot process.

The boot chain consists of five primary stages: the on-die Boot ROM serving as the hardware root of trust, the Secure Loader (also called SCE SBL or IPL) running on the PSP, the EMC initialization phase, the Hypervisor Loader, and finally the kernel. Every stage is cryptographically signed and verified before execution proceeds. The boot chain embeds anti-rollback protection through a security revision system that monotonically increases with each firmware release, preventing booting any firmware older than the currently installed version. Stage transitions are protected by a combination of RSA-4096 signatures, AES-128-CBC encryption layers, SHA-256 integrity hashes, and revision-specific nonces.

The boot process is closely tied to the hardware architecture. The serial flash (Winbond W25Q16JVNIM) stores the Secure Loader and EMC firmware. The NAND flash stores the main system software. The PSP Boot ROM is immutable, etched into the AMD SoC die during manufacturing. This hardware anchoring ensures that even with physical access and sophisticated equipment, the root of trust cannot be altered. The PS5 boot chain represents a significant evolution from the PS4, adding stronger anti-rollback mechanisms, additional encryption layers, and a more complex key hierarchy.

## Stages

### Stage 0: Boot ROM (on-die ROM)

The Boot ROM is the immutable root of trust, embedded directly on the AMD SoC die during manufacturing. It is the very first code executed when the PS5 powers on, running on the AMD PSP (AMD Secure Technology). The PSP is comparable in security role to the SAMU on PS4, the CMeP on PS Vita, and the Kirk on PSP, but with significantly expanded capabilities.

The Boot ROM performs the following critical functions at power-on:

- Initializes the PSP processor core, caches, and basic peripherals
- Validates the integrity of the serial flash connection and reads the initial boot configuration
- Loads the Secure Loader from the serial flash into PSP internal memory
- Performs initial cryptographic verification of the Secure Loader header (RSA-4096 signature check)
- Sets up the secure key rings that will be used by subsequent stages
- Configures memory protection regions including Keystone XOM areas

Because the Boot ROM is implemented in mask ROM on the silicon die, it cannot be modified or patched after manufacturing. This makes it the ultimate root of trust for the entire system. Any vulnerability in the Boot ROM would be permanent and unpatcheable at the hardware level, requiring a SoC revision to fix. The Boot ROM also configures early system security policies including which regions of memory are accessible to each boot stage.

### Stage 1: Secure Loader (SCE SBL)

The Secure Loader (SCE Secure Boot Loader), also called the Initial Program Loader (IPL), is the first mutable firmware component in the boot chain. It is stored on the serial flash and loaded by the Boot ROM into PSP memory. The Secure Loader is the main loader of the Hypervisor, Hypervisor Loader, and Kernel, making it one of the most critical components in the entire boot chain.

The Secure Loader image begins at NAND Group 0 offset 0x800 on the serial flash. The header structure is meticulously organized:

| Offset | Size | Field | Details |
|--------|------|-------|---------|
| 0x00 | 4 | Magic | `E4 DB 7C 02` |
| 0x04 | 4 | Header Size | 0x400 (1024 bytes), little-endian |
| 0x08 | 4 | Entry Point | 0xB0, little-endian offset into body |
| 0x0C | 4 | Body Size | Varies by version, e.g. 0x631D0 (~406 KB) |
| 0x10 | 0x10 | Padding | Zero-filled |
| 0x20 | 0x20 | SHA-256 Digest | Hash of decrypted body from 0x400 to 0x635D0 |
| 0x40 | 0xB0 | Padding | ASCII "0123456789abcdef" repeated, then zeroes |
| 0xF0 | 1 | Flag | 0x80 |
| 0xF1 | 0x2B | Padding | Zero-filled |
| 0x11C | 4 | Security Revision | Anti-rollback value (see table below) |
| 0x120 | 0x20 | Revision Nonce | SHA-256 hash of IPL revision string |
| 0x140 | 0xC0 | Metadata | May contain keyrings and metadata digest |
| 0x200 | 0x200 | RSA-4096 Signature | Covers the entire header (offset 0x00-0x1FF) |
| 0x400 | varies | Encrypted Body | AES-CBC encrypted (two layers) |

The Secure Loader body undergoes two-layer AES-CBC encryption. The first layer uses a global firmware key, while the second layer is keyed to the revision nonce. This dual-layer approach means that decryption requires both the global key material and the specific revision key for the firmware version being booted.

The Security Revision field at offset 0x11C is the primary anti-rollback mechanism. It has evolved across firmware generations:

| Security Revision | Firmware Versions |
|------------------|-------------------|
| 0x00000001 | 0.85.007 through 1.XX |
| 0x00000007 | 1.00 through 6.02 |
| 0x000000FF | 6.50 |
| 0x000003FF | 7.00 through 7.61 |
| 0x00000FFF | 8.00 through 8.60 |
| 0x00003FFF | 9.00 through 9.60 |
| 0x0000FFFF | 10.00 through 10.60 |
| 0x0003FFFF | 11.00 and later |

The revision nonce at offset 0x120 provides an additional layer of anti-rollback protection. It is computed as SHA-256 of the IPL revision string. Each firmware revision generates a unique nonce, and the nonce is used in the AES-CBC decryption of the body. This means that even with access to the global encryption keys, an attacker cannot decrypt or boot a firmware version without the corresponding revision nonce. Documented revision nonce values exist for revisions 0xA0 through 0x100.

After successful decryption and SHA-256 verification, the Secure Loader extracts the next-stage boot components from the body and prepares them for loading. The Secure Loader also manages the key rings stored in the metadata region, passing them to subsequent stages for their own verification needs.

### Stage 2: CP Box / EMC IPL

The Embedded Micro Controller (EMC) is a secondary processor within the PS5 that manages low-level hardware initialization, power sequencing, and system monitoring. The EMC uses a CXD90061GG hardware revision and runs its own firmware independent of the main PSP boot path.

The EMC firmware is stored on the serial flash at offset 0x4000 with a total length of 0x7E000 bytes (approximately 504 KB). It is structured as an SLB2 (Secure Loader Block 2) segment and can be extracted using the blsunpack tool. Within the SLB2 segment, the file identified as C0080001 contains the EMC version string.

EMC firmware has evolved substantially across PS5 firmware releases:

| EMC Version | PS5 Firmware | Platform |
|-------------|-------------|----------|
| 0.7.6 | SDK 0.85.070 | Prototype/DevKit |
| 1.0.4 | 1.01-1.14 | TestKit and Retail |
| 1.2.3 | 2.XX | TestKit |
| 1.4.2 | 3.00 | Retail |
| 1.6.0 | 4.00 | TestKit |
| 1.8.2 | 5.00 | Retail |
| 1.8.3 | 5.50 | Retail |
| 1.14.3 | 9.20 | Retail |

The EMC IPL is protected by AES-128-CBC encryption with keys specific to each EMC revision. For EMC revision c0, a documented 16-byte AES-128 cipher key is used for decryption. The EMC firmware manages power sequencing, thermal monitoring, and system reset handling, and coordinates with the main PSP during the boot process.

The CP Box (model CPBH-100) is a debug accessory for PS5 TestKits that connects via USB-C. It provides two operational modes:

- **Engineering Mode**: CP Box powered via USB-C to PS5 only. Provides basic debug access.
- **Normal Mode**: CP Box connected to USB-C portable HDD, Ethernet (DEV LAN) to host computer, and USB-C to PS5. Full debug functionality.

Without a CP Box connected, TestKits boot in Release Mode with full secure boot enforcement. With a CP Box, the TestKit can enter Assist Mode for debugging purposes. Assist Mode persists in memory even when the console is fully powered off. The CP Box is not hot-pluggable; it must be connected before power-on, or the PS5 will display an error. The CP Box can read PS5 information (serial number, boot mode) even when the PS5 is shut down.

A prototype CP Box variant (CPB-K01) uses the CXD90046GG main chip with two separate CP systems: one for recovery and one for normal operation. This dual-system architecture suggests the debug infrastructure was designed with redundancy for recovery scenarios. The CP Box also provides a VR port (USB-C) for PS VR2 activation, enabled after cpupdate version 2700.

CP Box status is indicated by five front-panel LEDs: CP INIT, NETWORK INIT, SPEED, LINK/ACT, and STATUS, providing visual feedback on the debug connection state.

### Stage 3: Hypervisor Loader

The Hypervisor Loader is loaded and verified by the Secure Loader after EMC initialization completes. It is responsible for initializing the PS5's hypervisor environment, which provides hardware-level virtualization and isolation between the kernel and user-mode processes. The Hypervisor Loader is a signed binary that undergoes the same cryptographic verification chain as the Secure Loader itself.

The Hypervisor Loader performs the following tasks:

- Configures the Memory Management Unit (MMU) for two-stage virtualization (guest physical to system physical address translation)
- Sets up interrupt virtualization including the IOMMU for device isolation
- Prepares the exception handling framework for hypervisor traps
- Establishes the memory protection boundaries between the hypervisor, kernel, and user space
- Loads the kernel SELF from NAND flash into memory
- Verifies the kernel signature using the EAP key ladder
- Transitions execution to the kernel entry point

The Hypervisor Loader's verification uses the RSA-4096 chain inherited from the Secure Loader, ensuring that the entire boot path from Boot ROM to hypervisor is covered by a single chain of signatures. The revision nonce system from the Secure Loader also constrains which Hypervisor Loader versions can be booted.

### Stage 4: Kernel Load

The kernel is the final stage loaded by the boot chain and represents the transition from firmware-level initialization to full operating system operation. The kernel is packaged as a SELF (Signed Executable and Linkable Format) binary, which is the PlayStation standard executable format used across PS4 and PS5.

The kernel SELF is encrypted with AES-128-CBC using keys derived from the EAP (Execution and Protection) key ladder. The EAP provides separate key material for the KBL (Kernel Boot Loader) and the kernel itself. The kernel SELF is also signed with an RSA-3072 key pair. The Communication Processor maintains the complete key chain spanning EMC, EAP, and KBL domains, secured with HMAC-SHA1 integrity protection.

The kernel loading process proceeds as follows:

1. The Hypervisor Loader reads the kernel SELF from the NAND flash system partition
2. The kernel header is verified against the EAP RSA-3072 public key
3. The kernel body is decrypted using the EAP AES-128-CBC key specific to the firmware revision
4. The Communication Processor validates the key chain integrity via HMAC-SHA1
5. The decrypted kernel is placed in protected memory regions
6. The Hypervisor Loader performs a final integrity check before releasing execution
7. Control is transferred to the kernel entry point

Once the kernel takes control, it initializes the remaining hardware subsystems, mounts the PlayStation File System (PFS) from NAND storage, loads secure modules (identified by 0x8002xxxx IDs) including authmgr, kms, pfs, and others, and begins loading the system software from the firmware partitions. The kernel also activates the full security monitor, enabling runtime protection mechanisms.

## Key Components

### Serial Flash (W25Q16JVNIM)

The PS5 uses a Winbond W25Q16JVNIM serial flash memory device for boot configuration and non-volatile parameter storage. This is a critical component as it stores the initial boot firmware that the ROM loads:

- **Model**: Winbond W25Q16JVNIM
- **Capacity**: 2 MB (16 Mbit)
- **Package**: 150mil SOIC (Small Outline Integrated Circuit)
- **Interface**: SPI bus with standard pinout
- **Pin Configuration**: /CS, /MISO, /WP, GND, VCC, /HOLD, SCLK, MOSI
- **Dumping**: Readable via Raspberry Pi GPIO using the flashrom tool

The serial flash memory layout includes:
- Offset 0x0000-0x07FF: Boot configuration parameters and unused space
- Offset 0x0800: Secure Loader header (E4 DB 7C 02 magic)
- Offset 0x0C00: Secure Loader encrypted body
- Offset 0x4000: EMC firmware (length 0x7E000 bytes)

The SPI bus interface makes the serial flash potentially observable with hardware probing tools, representing an attack surface for physical access scenarios.

### AMD PSP

The AMD Platform Security Processor (officially AMD Secure Technology) is the central security processor in the PS5 architecture. It is an ARM-based coprocessor integrated into the AMD SoC that serves as the primary trusted execution environment. The PSP:

- Executes the PS5 Boot ROM at power-on
- Handles all cryptographic operations: RSA-4096/RSA-3072 signature verification, AES-128-CBC encryption/decryption, SHA-256 hashing, HMAC-SHA1 integrity verification
- Manages secure key rings containing the key hierarchy
- Provides a trusted execution environment for secure modules (0x8002xxxx services)
- Monitors system behavior for suspicious activity during boot and runtime
- Controls access to one-time programmable (OTP) fuses used for device-unique keys

The PSP is the direct successor to the SAMU security processor in the PS4 and serves a similar role to the CMeP in PS Vita and the Kirk in PSP. The PSP's role has expanded significantly compared to previous generations, taking on more of the boot chain responsibilities that were previously handled by separate processors.

### Keystone

Keystone is a hardware memory protection mechanism integrated into the PS5 SoC that provides execute-only memory (XOM) capabilities. Code stored in Keystone-protected memory regions can be fetched and executed by the processor but cannot be read, written, or dumped through any debug interface. This protects sensitive code such as cryptographic routines, boot verification functions, and key management handlers from extraction even if an attacker gains arbitrary code execution.

Keystone is used throughout the boot chain:
- Boot ROM code resides in XOM regions
- Critical Secure Loader verification functions are XOM-protected
- Kernel security monitor routines execute from XOM memory
- Secure module cryptographic operations are isolated in XOM

Even the Hypervisor Loader and kernel cannot read XOM memory contents; they can only execute code within it. This provides a defense-in-depth mechanism that protects the most sensitive security code from both software and hardware attacks.

## Relationships

- [[hardware_overview]] — hardware provides boot ROM and serial flash
- [[hypervisor]] — boot chain loads the hypervisor
- [[kernel]] — kernel is final stage loaded
- [[security_model]] — every stage verified cryptographically
- [[system_overview]] — boot process initializes the entire system

## Detailed Stage Transition Flow

The boot chain follows a precise sequence of stage transitions, each with specific cryptographic checks:

### Power-On Sequence

1. **PSU stabilizes**: Power supply unit reaches stable voltages; reset signal is released
2. **SoC power-on reset**: AMD SoC begins internal initialization; PSP core starts executing
3. **Boot ROM execution**: PSP fetches Boot ROM from on-die mask ROM (address 0xFFFF0000 or similar)
4. **Cache initialization**: PSP initializes its instruction and data caches
5. **Serial flash detection**: PSP configures SPI controller and detects W25Q16JVNIM serial flash
6. **Boot device select**: PSP reads boot configuration to determine primary boot device (serial flash)
7. **Secure Loader header load**: PSP reads serial flash offset 0x800 into internal SRAM
8. **Magic validation**: PSP checks for E4 DB 7C 02 magic value; abort if mismatch
9. **RSA-4096 verification**: PSP hashes header and verifies RSA-4096 signature against ROM Key 2
10. **Security revision check**: PSP reads security revision at offset 0x11C; compares against OTP fuse value
11. **Body decryption setup**: PSP extracts encryption parameters and prepares AES engine
12. **Layer 1 decryption**: PSP decrypts body using global firmware AES-128-CBC key
13. **Layer 2 decryption**: PSP decrypts result using revision nonce-derived AES-128-CBC key
14. **SHA-256 verification**: PSP hashes decrypted body; compares against expected hash at offset 0x20
15. **Secure Loader execution**: PSP jumps to Secure Loader entry point (offset 0xB0 within body)

### Secure Loader Phase

16. **Secure Loader initialization**: SBL sets up its execution environment; configures memory protections
17. **Key ring extraction**: SBL reads metadata region at offset 0x140; extracts key rings for later stages
18. **EMC firmware location**: SBL locates EMC firmware at serial flash offset 0x4000
19. **EMC decryption**: SBL decrypts EMC firmware using revision-specific AES-128-CBC key
20. **SLB2 parsing**: SBL extracts SLB2 segment using blsunpack; finds C0080001 version file
21. **EMC version validation**: SBL verifies EMC version matches expected revision
22. **EMC execution handoff**: SBL transfers control to EMC for power-on initialization
23. **EMC initialization**: EMC initializes system power rails, clocks, thermal monitoring
24. **EMC completion handoff**: EMC signals completion; control returns to SBL
25. **Hypervisor Loader extraction**: SBL locates Hypervisor Loader within its decrypted body
26. **Hypervisor Loader verification**: SBL re-verifies using RSA-4096 chain
27. **Hypervisor Loader load**: SBL loads Hypervisor Loader into protected memory region
28. **Key ring handoff**: SBL passes key rings to Hypervisor Loader
29. **Hypervisor Loader execution**: SBL transfers control to Hypervisor Loader entry point

### Hypervisor to Kernel Phase

30. **Hypervisor initialization**: Sets up virtualization structures; configures MMU for two-stage translation
31. **IOMMU configuration**: Initializes IOMMU for device isolation
32. **Interrupt virtualization**: Sets up interrupt controller for virtualized interrupt delivery
33. **Memory partitioning**: Establishes protected memory regions for kernel and secure modules
34. **Kernel SELF location**: Finds kernel SELF on NAND flash system partition
35. **EAP key retrieval**: Reads EAP keys from the key ring passed by SBL
36. **Kernel SELF verification**: Validates RSA-3072 signature on kernel SELF header
37. **Kernel decryption**: Decrypts kernel body using EAP AES-128-CBC key
38. **Communication Processor validation**: Verifies EMC/EAP/KBL key chain integrity via HMAC-SHA1
39. **Final SHA-256 check**: Computes and verifies hash of decrypted kernel
40. **XOM configuration**: Configures Keystone XOM regions for kernel security routines
41. **Stage transition**: Hypervisor Loader transfers control to kernel entry point
42. **Kernel initialization**: Kernel takes control; initializes remaining hardware; mounts PFS filesystem
43. **Secure module loading**: Kernel loads secure modules (0x8002xxxx) into protected memory
44. **System software launch**: Kernel mounts system firmware partitions and begins user-space initialization

## Security Considerations

The PS5 boot chain implements defense-in-depth security at every stage transition. The root of trust is the immutable Boot ROM, which cannot be altered post-manufacturing. Each subsequent stage is cryptographically verified before execution proceeds.

The anti-rollback mechanism is enforced through two complementary systems. The Security Revision field (4 bytes at offset 0x11C in the Secure Loader header) provides coarse-grained version checking. The revision nonce (32 bytes at offset 0x120) provides fine-grained per-revision binding. Together, they ensure that a firmware image from one revision cannot be booted on a console that has been updated to a higher revision.

The dual-layer AES-CBC encryption of the Secure Loader body provides separation of concerns. Layer 1 uses global firmware keys that can be shared across Sony's signing infrastructure. Layer 2 uses revision-specific keys derived from the nonce. This means that even a full leak of Sony's firmware signing infrastructure would not allow booting arbitrary firmware versions on arbitrary consoles.

Known attack surfaces include:

- **Physical serial flash access**: The W25Q16JVNIM is accessible via SPI bus, which can be probed with logic analyzers or modified with a Raspberry Pi. However, modifying the Secure Loader would break the RSA-4096 signature verification.
- **PSP firmware vulnerabilities**: The PSP runs complex firmware that may contain implementation bugs exploitable during the boot process.
- **EMC firmware path**: The EMC firmware stored on serial flash is protected by AES-128-CBC but may have a narrower attack surface for analysis.
- **CP Box debug interface**: On TestKits, the CP Box provides alternative boot modes with relaxed security. This is limited to development hardware but the interface design reveals Sony's internal debug architecture.
- **Side-channel attacks**: The cryptographic operations during boot may be observable through power analysis or electromagnetic emissions.

The Keystone XOM protection mitigates many post-boot extraction attacks by making critical security code unreadable even from kernel context. Any successful attack on the main boot chain would require either a cryptographic breakthrough against RSA-4096 or RSA-3072, a hardware vulnerability in the Boot ROM (which cannot be patched), or a critical implementation bug in one of the signed boot components.

## References

- https://www.psdevwiki.com/ps5/Secure_Loader
- https://www.psdevwiki.com/ps5/EMC
- https://www.psdevwiki.com/ps5/CP_Box
- https://www.psdevwiki.com/ps5/Serial_Flash
- https://www.psdevwiki.com/ps5/AMD_Platform_Security_Processor
- https://www.psdevwiki.com/ps5/Keys
- https://www.psdevwiki.com/ps5/Secure_Modules
