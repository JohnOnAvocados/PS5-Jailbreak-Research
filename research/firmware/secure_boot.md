# PS5 Secure Boot

## Overview

The PS5 secure boot system implements a cryptographic chain of trust from the hardware root of trust through each boot stage up to the kernel. Every executable component in the boot chain must be cryptographically signed and verified before execution is allowed. The verification architecture uses a multi-layered key hierarchy spanning RSA-4096 for the Secure Loader header, RSA-3072 for kernel and package signing, and AES-128-CBC for firmware body encryption. Anti-rollback protection is enforced through a security revision system combined with revision-specific nonces that make each firmware release uniquely bound to its authorized decryption key.

The secure boot architecture extends beyond initial boot to include runtime secure modules that provide trusted services throughout system operation. These modules, identified by 0x8002xxxx service IDs, run within the PSP or a trusted execution environment and handle critical security operations including authentication (authmgr, pltauth, driveauth), key management (kms), DRM (npdrm), filesystem verification (pfs), and OTP access control (otpaccess, otpctrl). The entire verification infrastructure is managed by the AMD Platform Security Processor (PSP), which handles all cryptographic operations within its isolated secure environment. The PSP's role in secure boot makes it the central enforcement point for all security policies.

The secure boot design draws on lessons from the PS4 while introducing significant improvements. The PS4 used a simpler key hierarchy with fewer stages of verification. The PS5 adds dual-layer AES-CBC encryption for the Secure Loader, a more granular anti-rollback system with revision nonces, Keystone XOM protection for security-critical code, and a more extensive set of secure modules for runtime security. The key material hierarchy ensures that compromise of any single key does not break the entire chain: stage-specific keys, content keys, and platform keys are all independently managed within the PSP's secure key rings.

## Verification Algorithm Details

### RSA-4096 Signature Verification

The RSA-4096 signature covering the Secure Loader header (offset 0x200, 512 bytes) uses the standard RSASSA-PKCS1-v1_5 signature scheme with SHA-256 as the hash algorithm. The verification process:

1. Compute SHA-256 hash of the header bytes from offset 0x00 to 0x1FF (excluding the signature itself)
2. Decrypt the RSA-4096 signature using the public exponent (typically 65537) and the modulus stored in ROM Key 2
3. Compare the decrypted padding structure against the PKCS#1 v1.5 format
4. Extract the embedded hash and compare against the computed SHA-256
5. If the hashes match, the signature is valid

The RSA-4096 modulus size (4096 bits = 512 bytes) provides approximately 128 bits of security against known factoring attacks. The key is stored in the Boot ROM as part of the public key infrastructure and cannot be modified.

### AES-128-CBC Decryption

The Secure Loader body undergoes two sequential AES-128-CBC decryption operations:

**Layer 1 (Global Firmware Key)**:
- Key: Derived from ROM Key material (specific derivation not publicly documented)
- IV: Extracted from the Secure Loader metadata region (offset 0x140)
- Mode: CBC (Cipher Block Chaining)
- Padding: PKCS#7
- Purpose: Provides baseline encryption common across all firmware versions

**Layer 2 (Revision-Specific Key)**:
- Key: Derived from revision nonce (SHA-256 at offset 0x120) combined with additional PSP key material
- IV: Different from Layer 1, stored alongside Layer 1 IV in metadata
- Mode: CBC (Cipher Block Chaining)
- Padding: PKCS#7
- Purpose: Provides version-specific encryption that ties each firmware release to its authorized nonce

The dual-layer approach provides separation of concerns: Sony can share the global firmware key across their signing infrastructure without exposing revision-specific keys, and each firmware version's encryption is independently keyed to prevent cross-version decryption.

### SHA-256 Integrity Verification

After decryption, the body integrity is verified using SHA-256:

1. Compute SHA-256 hash of the decrypted body (offset 0x400 through the end, as specified by body size at offset 0x0C)
2. Compare against the expected hash stored at header offset 0x20
3. If hashes match, the body has been correctly decrypted and has not been corrupted

The SHA-256 verification serves a dual purpose: it confirms both that decryption was successful (correct keys) and that the decrypted content has integrity (no corruption or tampering).

## Key Hierarchy

### Root Keys (ROM Keys)

The PS5 stores multiple keyseed sets in the Boot ROM that form the immutable root of the key hierarchy. These ROM keysets are 256 bytes each and span Key 2 through Key 9. The actual key material is derived from these seeds through a proprietary derivation process within the PSP.

- **Key 2**: RSA key pair used for boot-time authentication and UCMD (User Command) verification. This is one of the most critical keys in the system, as it authenticates the Secure Loader and early boot components.
- **Key 3**: Additional RSA keys for UCMD authentication, providing a backup or alternative verification path.
- **Keys 4-9**: Additional keyseed sets for various boot and runtime security functions, including key material for secure module authentication.

These ROM keys cannot be changed after manufacturing, as they are fused into the silicon. The keyseed derivation within the PSP ensures that the actual key material is never directly exposed outside the secure processor.

### Secure Loader Keys

The Secure Loader uses a multi-layered key protection scheme:

1. **RSA-4096 Signature Key**: The header at offset 0x200 contains a 512-byte RSA-4096 signature that covers the entire header structure (offsets 0x00 through 0x1FF). This signature is verified by the Boot ROM using the public key stored in ROM keys.

2. **AES-128-CBC Layer 1 (Global Firmware Key)**: The first decryption layer uses a global AES-128 key that is common across all firmware versions. This key is stored within the PSP's secure key rings and is derived from ROM key material.

3. **AES-128-CBC Layer 2 (Revision Key)**: The second decryption layer is keyed to the revision nonce (SHA-256 hash at header offset 0x120). Each firmware release has a unique revision nonce, and the AES key for this layer is derived from the nonce combined with additional PSP key material.

The dual-layer approach ensures that even if the global firmware key is compromised, an attacker cannot decrypt Secure Loader images for firmware versions they do not have the specific revision key for.

### EMC and EAP Keys

The EMC (Embedded Micro Controller) firmware uses its own encryption and key management system:

- **EMC IPL Cipher Key**: AES-128-CBC key for PS5 EMC revision c0. This key decrypts the EMC firmware stored on the serial flash at offset 0x4000.
- **EMC Key Derivation**: Each EMC firmware revision has unique key material, preventing cross-revision decryption.

The EAP (Execution and Protection) key ladder provides keys for kernel boot:

- **EAP KBL Keys**: AES-128-CBC keys for Kernel Boot Loader (KBL) decryption. These keys are specific to each firmware release and are managed by the Communication Processor.
- **EAP Kernel SELF Cipher Key**: AES-128-CBC key for decrypting the kernel SELF binary.
- **EAP Kernel SELF RSA-3072 Key Pair**: RSA-3072 key pair used to sign the kernel SELF. The public key is embedded in the Hypervisor Loader for verification.

The Communication Processor maintains the complete key chain spanning EMC, EAP, and KBL domains, with HMAC-SHA1 integrity protection across the entire chain. This ensures that the key material cannot be modified or corrupted during the boot process.

### Content and Service Keys

Beyond boot verification, the PS5 uses additional keys for content protection and service authentication:

- **PKG Metadata RSA-3072 Key**: Full RSA-3072 private key including CRT parameters (P, Q, DP, DQ, QP). This key is used for signing PKG metadata. The complete private key has been documented, which affects content verification security but does not impact the boot chain.
- **SceShellCore Trophy Keys**: Shared with PS4, these keys verify trophy data integrity.
- **Kernel NID default_suffix**: Also shared with PS4, used for kernel function naming and symbol obfuscation.
- **Passcode**: 512-byte key from Prospero Publishing Tools for development authentication.
- **Portability EncDec Master Keys**: 128-byte master key, blob, IV, and hash shared with PS4 for cross-platform portability services.
- **Envelope Files**: RSA workaround_ctl public verification key and master key verification material.
- **M.2 Dummy Keys**: `01234567890123456789012345678901` used consistently across FW 1.00 through 12.20 for M.2 SSD encryption.
- **RNPS**: AES-128-CBC MAC combined with RSA-2048/RSA-3072 for network-related security services.
- **Communication Processor Keys**: Complete EMC/EAP/KBL key chain with HMAC-SHA1 integrity.

## Verification Process

### Stage 0 to Stage 1: Boot ROM to Secure Loader

The verification process begins the moment power is applied. The Boot ROM, which has no external dependencies, performs the following sequence:

1. Read the serial flash contents starting at offset 0x800
2. Validate the Secure Loader magic (E4 DB 7C 02) at offset 0x00
3. Extract the RSA-4096 signature from offset 0x200
4. Compute SHA-256 hash of the header (offset 0x00 to 0x1FF)
5. Verify the RSA-4096 signature against the ROM Key 2 public key
6. If signature verification fails, halt the boot process with no fallback
7. If signature verifies, extract the body encryption parameters
8. Prepare PSP cryptographic engine for body decryption

This initial verification is critical because it validates the authenticity of the entire Secure Loader before any mutable code is executed.

### Stage 1 to Stage 2: Secure Loader to EMC

After the Secure Loader header passes verification, the body decryption and verification proceed:

1. Decrypt the Secure Loader body using Layer 1 AES-CBC (global firmware key)
2. Decrypt the result using Layer 2 AES-CBC (revision nonce-derived key)
3. Compute SHA-256 hash of the decrypted body (offset 0x400 through end)
4. Compare against the expected SHA-256 at header offset 0x20
5. Verify the security revision at offset 0x11C >= minimum stored in OTP fuses
6. If verification passes, execute the Secure Loader entry point
7. The Secure Loader reads the EMC firmware from serial flash offset 0x4000
8. Decrypt the EMC firmware using the EMC revision-specific AES-128-CBC key
9. Extract the SLB2 segment using blsunpack and locate the C0080001 version file
10. Verify EMC integrity and transfer control for power-on initialization

### Stage 2 to Stage 3: EMC to Hypervisor Loader

After EMC initialization completes, control returns to the Secure Loader:

1. The Secure Loader locates the Hypervisor Loader within its decrypted body
2. The Hypervisor Loader is verified using the same RSA-4096 chain
3. Security revision and revision nonce checks are re-validated
4. The Hypervisor Loader is loaded into protected memory
5. The key rings from the Secure Loader metadata region are passed to the Hypervisor Loader
6. Control is transferred to the Hypervisor Loader entry point

### Stage 3 to Stage 4: Hypervisor Loader to Kernel

The final verification stage before kernel execution:

1. The Hypervisor Loader reads the kernel SELF from NAND flash
2. The kernel SELF header is verified using EAP RSA-3072 public key
3. The kernel body is decrypted using EAP AES-128-CBC key from the KBL chain
4. The Communication Processor validates the entire EMC/EAP/KBL key chain integrity via HMAC-SHA1
5. The kernel is placed in a protected memory region configured by the hypervisor
6. A final SHA-256 integrity check is performed on the decrypted kernel
7. Hardware virtualization protections are activated
8. Control is transferred to the kernel entry point
9. The kernel takes over system management from the Hypervisor Loader

### Anti-Rollback Verification

The anti-rollback system is enforced at every stage transition where firmware version changes could occur. The mechanism works as follows:

1. OTP fuses on the SoC store the minimum allowed security revision
2. Each firmware update burns new OTP fuses to increase the minimum revision
3. At boot time, each boot stage checks its security revision against the OTP value
4. If the stage's revision is less than the OTP minimum, boot is halted
5. The revision nonce system provides a secondary anti-rollback check through encryption binding

The security revision values are hierarchical and cumulative. The hex values increase as the firmware version range expands:

- 0x00000001 covers the narrowest range (FW 0.85-1.XX)
- 0x00000007 covers FW 1.00-6.02
- Each subsequent value extends the accepted range
- 0x0003FFFF covers FW 11.00 and later (the broadest range)

The revision nonce collection provides a cryptographic fingerprint of each revision's decryption key. Documented nonces correspond to specific IPL revisions:

| Revision | Nonce (SHA-256) |
|----------|-----------------|
| 0xA0 | E3 D9 8F 94 ... |
| 0xB0 | 55 18 14 A6 ... |
| 0xC0 | B3 59 79 B6 ... |
| 0xD0 | 1C B3 91 12 ... |
| 0xE0 | FD 50 C2 9C ... |
| 0xF0 | 6F 20 B4 5B ... |
| 0x100 | 50 C0 E3 99 ... |

Each nonce uniquely identifies the firmware revision and serves as the root of the Layer 2 AES-CBC decryption key derivation. Without the correct nonce, the Secure Loader body cannot be decrypted even with all other key material.

## Secure Modules

PS5 secure modules provide trusted runtime services after the kernel is loaded. Each module is identified by a 0x8002xxxx ID and provides a specific security function. These modules run within the trusted execution environment (likely on the PSP or a dedicated secure processor) and are isolated from the main OS:

| ID | Name | Function |
|----|------|----------|
| 0x80021000 | authmgr | Authentication Manager — handles user and system authentication |
| 0x80021001 | kms | Key Management System — manages cryptographic key lifecycle |
| 0x80021002 | pup | PUP Firmware Update — verifies and processes system updates |
| 0x80021003 | pfs | PlayStation File System — encrypted filesystem operations |
| 0x80021004 | driveauth | Drive Authentication — validates Blu-ray/disc drive |
| 0x80021005 | pltauth | Platform Authentication — platform-level identity verification |
| 0x80021006 | npdrm | Network Product DRM — digital rights management for content |
| 0x80021007 | devact | Device Activation — console activation for services |
| 0x80021008 | qafutkn | QA/Utoken — quality assurance and user token management |
| 0x80021009 | sysveri | System Verification — validates system software integrity |
| 0x8002100A | otpaccess | OTP Access — one-time programmable memory access control |
| 0x8002100B | manu | Manufacturing — factory provisioning and test functions |
| 0x8002100C | fttrm | Film/TV Tracking Rights Management — media rights enforcement |
| 0x8002100D | srtc | Secure RTC — secure real-time clock management |
| 0x8002100E | rootparam | Root Parameter — system root configuration access |
| 0x8002100F | exthdd | External HDD — external storage authentication |
| 0x80021010 | cloudsd | Cloud SaveData — cloud save encryption and sync |
| 0x80021011 | bar | Backup and Restore — system backup operations |
| 0x80021012 | otprsvaccess | OTP Reserved Access — reserved OTP region control |
| 0x80021013 | diskid | Disk ID — disc identification and authentication |
| 0x80021014 | idata | Identity Data — console identity management |
| 0x80021015 | ddd | Unknown — undocumented module |
| 0x80021016 | otpctrl | OTP Control — OTP fuse programming and management |
| 0x80021017 | ncdt | Unknown — undocumented module |
| 0x80021018 | hidauth | HID Authentication — input device authentication |

These modules are loaded after kernel initialization and provide the trusted computing base for all runtime security operations. The pup module (0x80021002) is particularly relevant to firmware security as it handles the verification of PS5UPDATE.PUP files during system updates.

## XOM Integration

Keystone execute-only memory (XOM) is a hardware security feature integrated into the PS5's memory controller that enforces strict memory access controls. Memory pages marked as XOM can be fetched and executed by the processor but cannot be read or written by any software, including the kernel and hypervisor.

XOM is used to protect:

- **Boot ROM routines**: The most fundamental cryptographic verification code
- **PSP firmware**: Key management and cryptographic engine code running on the PSP
- **Secure Module code**: Runtime trusted service routines that handle sensitive operations
- **Key derivation functions**: The algorithms that derive AES and RSA keys from ROM seeds
- **OTP access control**: Functions that read and program one-time programmable fuses

The XOM protection is configured during the early boot stages and persists throughout system operation. Even if an attacker achieves arbitrary code execution at the kernel level, they cannot extract or modify the code running in XOM regions. This provides a critical defense against runtime attacks targeting the secure boot infrastructure.

## Relationships

- [[boot_chain]] — secure boot is the verification mechanism for the boot chain
- [[security_model]] — root of trust model
- [[hardware_overview]] — hardware roots of trust

## Security Considerations

The PS5 secure boot architecture represents a significant advancement over the PS4 in several key areas:

**Key Hierarchy Depth**: The PS5 uses a deeper key hierarchy with more independent key domains. RSA-4096 protects the Secure Loader, RSA-3072 protects the kernel, and AES-128-CBC protects the encrypted bodies. Stage-specific keys (EMC, EAP, KBL) are independently managed, so compromise of one domain does not cascade to others.

**Anti-Rollback Strength**: The combination of security revision (OTP-enforced minimum version) and revision nonce (cryptographic binding of encryption to specific firmware) provides dual-layer anti-rollback protection. The PS4 primarily relied on simpler version checks that were more vulnerable to bypass.

**Encryption Layering**: The two-layer AES-CBC encryption of the Secure Loader creates a separation of concerns between global firmware encryption (Layer 1) and revision-specific encryption (Layer 2). This design ensures that even a catastrophic key leak of global keys cannot decrypt future or past firmware revisions.

**Documented Weaknesses**:

- **PKG Metadata RSA-3072 Leak**: The full RSA-3072 private key for PKG metadata signing has been documented with complete CRT parameters (P, Q, DP, DQ, QP). This compromises content signing but does not affect boot security.
- **M.2 Dummy Keys**: The M.2 encryption keys are static (`01234567890123456789012345678901`) across all firmware versions from 1.00 through 12.20. This suggests M.2 storage encryption is not firmware-revision-dependent.
- **PS4 Key Sharing**: Several portability keys are shared between PS4 and PS5, including portability EncDec master keys and SceShellCore trophy keys. Any compromise of PS4 key material in these shared domains would affect PS5.
- **CP Box Debug Path**: TestKits with CP Box connected can boot with relaxed security (Assist Mode). The CP Box debug infrastructure reveals design insights about Sony's internal testing methodology.

**Theoretical Attack Vectors**:

- **Boot ROM vulnerability**: An exploitable bug in the mask ROM would be unpatcheable. This is the single highest-value target.
- **RSA-4096 cryptanalysis**: A breakthrough in factoring large RSA keys would break the root of trust, but this is infeasible with current technology.
- **Serial flash modification**: Physical access to the SPI bus could allow observation or modification of boot data, but cryptographic signatures prevent tampering.
- **Side-channel attacks**: Power analysis or EM emission analysis during cryptographic operations could leak key material over time.
- **OTP fuse manipulation**: If OTP fuse programming can be reversed or bypassed, the anti-rollback mechanism would be defeated.

## References

- https://www.psdevwiki.com/ps5/Keys
- https://www.psdevwiki.com/ps5/Secure_Loader
- https://www.psdevwiki.com/ps5/Secure_Modules
- https://www.psdevwiki.com/ps5/EMC
- https://www.psdevwiki.com/ps5/AMD_Platform_Security_Processor
- https://www.psdevwiki.com/ps5/CP_Box
