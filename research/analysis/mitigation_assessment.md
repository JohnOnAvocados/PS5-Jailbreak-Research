# PS5 Mitigation Assessment

## Overview

The PS5 employs a deeply layered defense-in-depth security architecture
spanning hardware, firmware, hypervisor, kernel, and userland. Each layer
implements specific mitigations that either prevent attacks entirely or
raise the bar for exploitation. This assessment evaluates the effectiveness
of each layer's mitigations based on documented vulnerabilities, known
bypass techniques, and cross-generational comparison with the PS4. The
overall finding is that userland and kernel mitigations provide moderate
resistance (slowing but not preventing exploitation), while hypervisor
mitigations provide strong resistance (no public exploits for FW >=7.00
as of mid-2026). The Boot ROM is the only layer with absolute security
guarantees due to its immutable mask ROM implementation.

At the hardware level, the AMD Zen 2 SoC provides the Platform Security
Processor (PSP) as an isolated ARM-based cryptoprocessor, OTP fuses for
anti-rollback, nested page tables for hypervisor memory isolation, and
Keystone eXecute-Only Memory (XOM) for code protection. The boot chain
enforces RSA-4096 signing for the Secure Loader header, dual-layer AES-CBC
encryption for the IPL body, SHA-256 integrity checking, and RSA-3072
signing for kernel SELF binaries. The hypervisor implements nested page
tables (NPT), xotext execute-only memory (bit 58 in NPT PTEs), Guest Mode
Execute Trap (GMET), control register filtering, MSR interception, and
SMMU-based IOMMU control. The kernel enforces XOM at usermode and kernel
level, SMAP/SMEP/UMIP, KASLR, and signed secure modules. Userland
implements WebKit sandboxing, nullfs namespace isolation, capability-based
access control via Auth IDs and PAIDs, and disabled JIT in standard
contexts.

Despite this depth, every layer has been compromised through software
attacks. Use-after-free and double-free bugs dominate kernel exploitation
(12+ documented classes). Early hypervisor versions had TMR heap OOB
(FW <=6.02), vtable in data segment (FW <=2.70), debug flag retention
(FW <=2.70), and TMR protection edit paths (FW <=4.51). Userland exploits
via WebKit, BD-J, and V8 are the most common entry points. The mast1c0re
family exploits the PS2 emulator JIT, bypassing all standard userland
mitigations by design. Shared PS4 key material (trophy keys, portability
keys, kernel NID suffix) introduces cross-generation systemic risk.

## Hardware Mitigations

- **PSP (AMD Platform Security Processor)**: The PSP (codename Ariel) is
  an ARM-based cryptoprocessor integrated into the AMD Zen 2 SoC, isolated
  from main x86 CPU cores. It is the hardware root of trust for the entire
  PS5 platform. The PSP executes immutable Boot ROM from on-die mask ROM
  at power-on, initializes cryptographic engines, verifies the Secure
  Loader IPL signature using RSA-4096, decrypts the IPL using AES-CBC with
  keys from secure key rings, manages OTP fuse access, and monitors system
  behavior during boot. The PSP has its own memory and execution
  environment — even a fully compromised kernel on the x86 cores cannot
  read PSP key material or modify PSP firmware. The PSP is the evolution
  of PS4's SAMU, PS Vita's CMeP, and PSP's Kirk security processors,
  consolidating all security functions into a single SoC-integrated
  processor. Despite strong isolation, the PSP runs complex ARM firmware
  that may contain implementation bugs exploitable during the boot process.

- **OTP fuses**: One-time programmable memory embedded in the SoC stores
  the minimum allowable security revision for anti-rollback. Each firmware
  update burns new OTP fuses to increase the revision floor. The fuses are
  write-once and cannot be reversed. Security revision values escalate
  monotonically: 0x00000001 (FW 0.85-1.XX), 0x00000007 (FW 1.00-6.02),
  0x000000FF (FW 6.50), 0x000003FF (FW 7.00-7.61), 0x00000FFF (FW 8.00-
  8.60), 0x00003FFF (FW 9.00-9.60), 0x0000FFFF (FW 10.00-10.60),
  0x0003FFFF (FW 11.00+). The Revision Nonce adds cryptographic binding —
  each firmware version's Layer 2 AES-CBC key derives from its unique
  SHA-256 nonce. The nonces span revisions 0xA0 through 0x100. Bypass
  requires physical OTP fuse manipulation or PSP compromise.

- **Keystone XOM**: Hardware execute-only memory for security-critical
  code. XOM pages can be executed but not read, written, or dumped through
  debug interfaces. Protects Boot ROM routines, PSP firmware, secure
  module code, key derivation functions, and OTP access control. Configured
  during early boot and persists throughout runtime. Believed to be a
  custom extension co-developed with AMD using bit 58 in NPT PTEs. Creates
  an effective barrier against code extraction — even kernel-level code
  execution cannot read protected security routines. One of very few x86
  deployments of execute-only memory, pioneered on ARM architectures.

- **SMMU/IOMMU**: The System Memory Management Unit provides hardware DMA
  isolation through the hypervisor-managed IOMMU. All DMA-capable devices
  (GPU, storage, USB, networking, audio) can only access memory regions
  explicitly mapped by the hypervisor. The IOMMU is configured exclusively
  through hypercalls (0x06-0x0C), preventing kernel-level attackers from
  freely remapping devices for DMA attacks.

## Boot Chain Mitigations

- **Dual-layer AES-CBC encryption**: The Secure Loader body undergoes two
  sequential AES-128-CBC decryption operations. Layer 1 uses a global
  firmware key derived from ROM key material. Layer 2 uses a revision-
  specific key derived from the SHA-256 Revision Nonce (offset 0x120)
  combined with additional PSP key material. Each layer uses PKCS#7
  padding and distinct IVs stored in the metadata region (offset 0x140).
  This separation of concerns means even a catastrophic leak of global
  firmware keys cannot decrypt images for firmware versions without the
  specific revision key. Also prevents booting firmware from one revision
  on a console updated to a different revision.

- **RSA-4096/3072 signing**: The Secure Loader header carries a 512-byte
  RSA-4096 signature at offset 0x200 using RSASSA-PKCS1-v1_5 with SHA-256.
  Verification computes SHA-256 of header bytes 0x00-0x1FF, decrypts the
  signature using ROM Key 2 public exponent (65537), and compares the
  PKCS#1 v1.5 padding structure hash. The 4096-bit modulus provides
  approximately 128 bits of security against factoring attacks. The kernel
  SELF uses RSA-3072 through the EAP key ladder. The PKG metadata RSA-3072
  key has been fully leaked (complete CRT parameters including P, Q, DP,
  DQ, QP) but affects content signing only, not boot security.

- **Anti-rollback (Security Revision + nonces)**: Two complementary
  systems. The Security Revision field (offset 0x11C, 4 bytes) provides
  coarse-grained version checking against OTP fuses. The Revision Nonce
  (offset 0x120, 32 bytes) provides fine-grained per-revision cryptographic
  binding. The PSP reads the IPL security revision and compares against
  the OTP fuse value at boot — if the revision is lower than the minimum,
  the boot process halts. The nonce ensures that even with all key
  material, firmware from one revision cannot be decrypted for another.

- **Secure module chain (EMC/EAP/KBL)**: The Communication Processor
  maintains a complete key chain spanning EMC, EAP, and KBL domains with
  HMAC-SHA1 integrity. Each domain has independent key material: EMC uses
  AES-128-CBC with revision-specific keys, EAP KBL uses separate AES-128-
  CBC keys for kernel boot loader decryption, and EAP kernel SELF uses
  RSA-3072 plus AES-128-CBC. The chain ensures all southbridge
  co-processors run authenticated firmware tied to the main boot chain.

- **Hypervisor Loader (HyLonome)**: Added in FW 3.00 as an independently
  verified boot stage. Pre-3.00: Boot ROM > Secure Loader > Hypervisor >
  Kernel. Post-3.00: Boot ROM > Secure Loader > Hypervisor Loader >
  Hypervisor > Kernel. Codename suggests "Hypervisor Loader — No ME,"
  indicating replacement of AMD Management Engine functions. Adds an extra
  integrity boundary before hypervisor execution. Decouples loading logic
  from both the Secure Loader and hypervisor for independent evolution.

## Hypervisor Mitigations

- **Nested page tables (NPT/SLAT)**: The hypervisor maintains stage-2
  page tables overlaying the kernel's stage-1 tables. Controls physical
  memory the guest can access independently of the guest's own mappings.
  The xotext bit (bit 58 in NPT PTEs) marks pages as execute-only — code
  can be fetched but not read or written. The feature is controlled through
  EFER bit 16 (nda/xotext), which the hypervisor masks to prevent the
  guest from disabling it. NPT enables the hypervisor to restrict the
  guest to specific physical memory and enforce access permissions at
  hypervisor-controlled granularity.

- **Restricted hypercall surface**: Only 17 hypercalls (0x00-0x10 on
  FW >=3.00) are exposed. Categories are tightly scoped: message interface
  (2), self-loading (2), CPUID virtualization (2), IOMMU management (7),
  error handling (1), VMClosure (1, FW >=3.00), MP boot (2, FW >=3.00).
  No hypercalls for memory allocation, thread creation, or other high-risk
  operations. Each handler must rigorously validate guest parameters —
  malformed descriptors trigger hypervisor-level protection.

- **IOMMU control**: Exclusive hypervisor control over IOMMU configuration.
  The kernel must request all IOMMU operations through hypercalls 0x06-0x0C.
  This architectural shift from earlier AMD platforms prevents even
  arbitrary kernel code execution from freely remapping devices for DMA
  attacks. All DMA-capable peripherals are managed through the IOMMU.

- **Control register filtering**: The hypervisor intercepts writes to CR0
  (PG, WP, NE, PE bits), CR4 (SMAP, SMEP, VME bits), and EFER (nda/xotext
  bit 16, SVME bit 12, NXE bit 11). The kernel cannot disable paging,
  write protection, SMAP/SMEP, NX protection, or the xotext feature.

- **GMET (Guest Mode Execute Trap)**: Hardware SVM feature preventing code
  execution at the wrong privilege level within the guest. User-mode code
  cannot execute kernel-mode pages and vice versa. Even with corrupted
  kernel page tables, the hardware traps invalid privilege execution at
  the hypervisor level. Provides a hardware-enforced privilege boundary
  independent of the kernel's software-based separation.

- **MSR Protection Map (MSRPM)**: The hypervisor uses an MSRPM bitmap to
  intercept specific MSR accesses. Any matching MSR read/write causes a
  VM exit for the hypervisor to emulate, filter, or deny the access.
  Prevents the guest from accessing MSRs that could leak hypervisor state
  or affect virtualization configuration.

- **VMClosure (FW >=3.00)**: Hypercall 0x0E provides a controlled path for
  securely shutting down or isolating the guest VM. Prevents a compromised
  kernel from remaining active. Introduced with the architecture split at
  FW 3.00 alongside the Hypervisor Loader.

## Kernel Mitigations

- **XOM enforcement (usermode)**: The kernel sets the XOM bit on every
  usermode code page during module loading. Memory reads targeting XOM-
  marked pages cause page fault exceptions that trigger kernel panic on
  uncompromised systems. Instruction fetches are not blocked. Prevents
  attackers with usermode code access from dumping binaries for gadget
  searching or reverse engineering. Can be bypassed with kernel access by
  clearing XOM bits in PTEs and flushing TLBs. Functions as a speed bump
  rather than a barrier at kernel privilege level.

- **XOM enforcement (kernel)**: Kernel .text pages are XOM-protected with
  backing from hypervisor-level NPT. The kernel cannot disable its own XOM
  because the NPT layer is controlled by the hypervisor. This creates a
  chicken-and-egg problem for reverse engineering: understanding the
  hypervisor requires reading kernel .text, but that requires disabling
  kernel XOM, which requires hypervisor compromise. This is the single
  most effective kernel mitigation.

- **SMAP/SMEP/UMIP**: Supervisor Mode Access Prevention and Supervisor
  Mode Execution Prevention prevent the kernel from accessing user data or
  executing user code. Enforced at the CR4 level, filtered by the
  hypervisor. UMIP blocks user-mode execution of privileged instructions
  (SGDT, SIDT, SLDT, SMSW, STR). SMAP bypass techniques exist but require
  specific firmware-dependent gadget chains.

- **KASLR**: Kernel Address Space Layout Randomization randomizes the
  kernel base address at boot. Early firmware (FW 0.85.070) had no KASLR
  with fixed base 0xFFFFF80000000000. Modern firmware implements full
  KASLR. Effectiveness depends on entropy and the absence of information
  disclosure vulnerabilities that leak the kernel base.

- **SceSbl sandboxing**: 20+ secure modules (0x8002xxxx IDs) run in
  isolated execution contexts. authmgr handles SELF verification and
  segment loading. kms manages key lifecycle with opaque handle-based
  access — keys never exposed in plaintext. pfs handles filesystem ICV
  table updates. Manufacturing modules (manu, 0x8002100B) are restricted
  but can load/unload via IOCTLs if reachable. Even if one module is
  compromised, others remain protected due to sandboxed architecture.

- **Secure boot region management**: SceSbl functions sceSblSecRegInit,
  sceSblSecRegResume, sceSblSecRegSuspend manage protected memory regions
  for secure module execution. Key ring management uses opaque handles
  (sceSblKmsSetKeyId, sceSblKmsAllocSignedKeyHdl) to prevent key exposure.

- **PFS integrity**: PlayStation File System uses ICV tables for data
  authentication via service ID 0x80021003 (sceSblPfsmgrUpdateIcvTable).
  External HDD metadata verification via 0x8002100F.

## Userland Mitigations

- **WebKit sandbox**: System browser and WebViews run in a sandboxed WebKit
  environment restricting API access. The sandbox prevents direct
  filesystem access, process creation, and device access. Despite this,
  multiple bypasses exist (CVE-2022-22620, CSSFontFaceSet). The sandbox
  delays but does not prevent exploitation when combined with a kernel
  exploit.

- **nullfs namespace isolation**: Virtual filesystem layer providing
  sandboxed PFS namespace views per process via /dev/nsfsctl and
  /dev/pfsctldev. Each process sees only authorized filesystem paths. The
  BD-JB2 path traversal (FW <=7.61) demonstrated nullfs bypass through
  crafted path navigation within the BD-J sandbox.

- **Capability model (Auth IDs and PAIDs)**: Auth IDs (64-bit identifiers
  with prefixes: 41=kernel, 48=system process, 49=system library)
  categorize code modules. PAIDs determine process security domains and
  resource policies. Kernel has PAID 4801000000000000. System processes
  use prefix 4800. Limits what a userland exploit can do even with code
  execution — the exploit runs within its process capability profile.

- **JIT disabled in standard contexts**: Standard contexts have JIT
  disabled to prevent spraying attacks. However, the PS2 emulator JIT
  (mast1c0re) is enabled for emulation performance, creating a native
  code execution path through crafted save data. No software mitigation
  can fully close this gap without disabling PS2 backward compatibility.

- **SELF binary signing**: All executables use SELF format with
  cryptographic signatures verified by SceSbl. Auth ID enforcement prevents
  unprivileged code from loading kernel or system modules. Envelope files
  (sceSblEnvelopeOpen, sceSblEnvelopeOpen2) wrap cryptographic operations
  in authenticated structures.

## Mitigation Gaps

- **PS4 key sharing**: Trophy keys, portability EncDec master keys (128-
  byte master key, blob, IV, hash), kernel NID default suffix, and passcode
  system are shared with PS4. Any PS4 key compromise in these domains
  directly impacts PS5. This is a permanent systemic risk from cross-
  generation compatibility requirements.

- **M.2 dummy keys**: Static key 01 23 45 67 89 01 23 45 67 89 01 23 45
  67 89 01 used across FW 1.00-12.20 for M.2 SSD authentication. Suggests
  placeholder implementation rather than strong cryptographic boundary.
  Known test key allows decryption of M.2 storage contents.

- **PS2 emulator JIT (mast1c0re)**: The JIT must be enabled for PS2
  emulation performance, creating a native code execution path from
  untrusted save data. No software mitigation can fully close this gap
  without disabling the PS2 emulator or introducing comprehensive JIT
  output verification — both of which break backward compatibility.

- **GPU DMA bypass**: GPU DMA engine reads and writes kernel .data pages
  even when CPU write-protected (FW >=6.00). Hardware-level bypass of
  software protection. Mitigation requires hypervisor IOMMU reconfiguration
  to restrict GPU DMA targets.

- **Speculative execution (Zen 2)**: EntrySign (CVE-2024-36347), ZenBleed
  (CVE-2023-20593), Retbleed (CVE-2022-29900), Inception/SRSO (CVE-2023-
  20569). Architectural hardware vulnerabilities that cannot be fully
  mitigated in microcode. ZenBleed can leak SIMD/FP register contents
  across privilege boundaries, potentially exposing cryptographic key
  material during PSP operations.

- **Hypervisor debug flag retention (FW <=2.70)**: Byepervisor bug where
  debug flag persisted through rest mode, allowing debug escalation on
  resume. Fixed in later firmware but demonstrates state management risk.

- **CP Box assist mode persistence**: On TestKits, Assist Mode persists
  across power cycles until explicitly cleared. Creates persistent debug
  surface on development hardware.

- **Limited zeroization**: Debug flag retention suggests incomplete
  zeroization. Cryptographic key material and sensitive state may persist
  longer than necessary, creating disclosure vectors.

## Relationships

- [[security_model]] — every mitigation derives from the platform's
  security architecture: PSP root of trust, SceSbl dispatch, XOM,
  capability-based access control, cryptographic chain of trust
- [[boot_chain]] — boot chain mitigations provide the integrity foundation;
  all later-layer mitigations assume the boot chain is uncompromised
- [[hardware_architecture]] — hardware mitigations (PSP, OTP, NPT, xotext)
  are the most fundamental; all software mitigations depend on correct
  hardware implementation

## Security Considerations

The layered strategy is effective: no single exploit provides complete
system compromise. Even with a fully exploited kernel, kernel XOM cannot
be disabled without a separate hypervisor bug. The hypervisor is the most
resilient layer with no public exploits for FW >=7.00. Userland mitigations
are the weakest link — WebKit, BD-J, and V8 exploits are regularly found.
The mast1c0re family is a design-level gap that cannot be fully mitigated
without disabling the PS2 emulator. The shared PS4 key material is a
systemic risk persisting across the platform lifecycle. The Zen 2
speculative execution vulnerabilities are architectural — they cannot be
patched and represent permanent hardware weakness. The GPU DMA bypass
shows that hardware co-processors with independent memory access can
subvert software protections. The hypervisor's relative resilience
suggests Sony's architectural investment has been effective, but the
evolving complexity of the hypercall interface introduces new surface that
may yield future vulnerabilities.

## References

- sources/web/psdevwiki/security/vulnerabilities.md
- research/hardware/hardware_overview.md
- research/kernel/kernel.md
- research/hypervisor/hypervisor.md
- research/security_model/security_model.md
- research/firmware/boot_chain.md
- research/firmware/secure_boot.md
