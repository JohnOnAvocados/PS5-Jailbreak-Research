# PS5 Security Research Roadmap: Gaps, Priorities, and Strategic Directions

## Overview

The PS5 security research landscape as of mid-2026 presents a paradox: userland entry points are abundant and well-understood (Y2JB spans FW 2.00-13.40 unpatched, BD-JB-EX covers FW <=12.70, mast1c0re targets all firmware with PS2 emulation), kernel exploits follow a reliable cadence of roughly one per major firmware cycle (kqueueex through 12.70, netcontrol through 12.00, aio_multi_delete through 10.01), yet the hypervisor — the single most critical layer for full system compromise — has no public exploits for FW >=7.00. This creates a stratification where older firmware (<7.00) has complete compromise paths while modern firmware (13.40) is limited to userland access. The hypervisor wall at 6.02 is the defining challenge of current PS5 research.

This roadmap was compiled through synthesis of 15+ research documents covering hardware architecture, firmware boot chain, secure boot verification, hypervisor internals, kernel syscall/IOCTL surface, security model (Auth IDs, PAIDs, XOM, secure modules), attack surface enumeration, mitigation assessment, CVE history, exploit chain compatibility, and open questions. Source data draws from psdevwiki, academic publications (Buhren et al. voltage glitching, ZenBleed/Inception/Retbleed/EntrySign disclosures), community jailbreak releases (etaHEN, kstuff, Prosperous, Byepervisor), and private researcher communications. The document distinguishes confirmed facts from speculative analysis at every turn and prioritizes research directions by expected impact, difficulty, and dependency ordering.

The strategic picture reveals several cross-cutting themes: the southbridge firmware stack (EMC/EAP/CP Box) is the least-documented but most architecturally interesting attack surface, offering firmware-level persistence that survives OS reinstallation; the PSP firmware represents the highest-value but most difficult reverse engineering target; GPU DMA exploitation provides the most powerful kernel primitive but is poorly understood; and speculative execution vulnerabilities (ZenBleed on Zen 2) represent architectural weaknesses that may never be fully mitigated. The PS4-PS5 key sharing creates permanent cross-generation systemic risk. The mast1c0re family exploits a design-level gap in the PS2 emulator JIT that has no software fix short of disabling the emulator entirely.

## Research Gap Analysis

### Critical Gaps (Blocking Progress)

#### 1. PSP Firmware Internals

**Status:** No public disassembly, decompilation, or extraction methodology for PSP firmware exists. The PSP (AMD Platform Security Processor, codename Ariel) is an ARM-based cryptoprocessor integrated into the Zen 2 die, serving as the hardware root of trust. It executes immutable Boot ROM from mask ROM at power-on, validates the Secure Loader via RSA-4096 against ROM Key 2, manages secure key rings (Keys 2-9, 256-byte keyseeds), controls OTP fuse access, and provides the TEE for secure module execution.

**Confirmed Facts:**
- PSP uses AMD Secure Technology framework, integrated as a co-processor within the Oberon/Viola APU
- MMIO region: sbl0 at 0xE0500000-0xE05FFFFF and 0xE06C6000-0xE06C7FFF (device 0.2 on pci2)
- PSP boot ROM is immutable mask ROM — any vulnerability is permanent
- PSP handles RSA-4096/RSA-3072 signature verification, AES-128-CBC encryption/decryption, SHA-256 hashing, HMAC-SHA1 verification
- PSP controls access to OTP fuses used for security revision anti-rollback
- PSP communicates with southbridge CP over dedicated internal buses for boot coordination, key ring handoff, and secure module dispatch

**Unknowns:**
- ARM executable format used by PSP firmware (not publicly documented)
- Memory layout: code region, data region, stack, heap, MMIO mappings, secure key ring storage
- Secure boot region management implementation (how Keystone XOM regions are configured)
- Key ring implementation: storage format, key derivation algorithms, key slot allocation strategy
- OTP programming interface: how fuses are read, programmed, and write-protected
- TEE application loading mechanism: how secure modules (0x8002xxxx) are loaded into PSP execution context
- Whether PSP runs a proprietary RTOS, bare-metal code, or a modified ARM TrustZone implementation
- Complete syscall/hypercall interface between x86 cores and PSP
- Whether PSP firmware updates are possible through PUP or only through manufacturing
- Comparison with PS4 SAMU firmware: architectural similarities and differences

**Impact:** The PSP is the root of trust for the entire platform. Understanding its firmware is prerequisite for any boot-level attack. A PSP firmware vulnerability would bypass all higher-layer security (hypervisor, kernel, userland) and potentially expose all cryptographic keys. [[hardware_attack_surface]] [[mitigation_assessment]]

**Research Dependencies:**
- Requires NAND dumps from exploited units to extract PSP firmware
- Requires identification of ARM executable format before disassembly
- PSPReverse open-source project may provide tooling (state unknown)
- Serial flash dumping (W25Q16JVNIM via Raspberry Pi GPIO) provides IPL but not PSP firmware

---

#### 2. Southbridge Firmware (EMC/EAP/CP Box)

**Status:** The CXD90061GG southbridge (Salina, MediaTek MT3613CT based) contains multiple co-processors — EMC (Error Management Controller, ARM-based, 504 KB firmware at serial flash offset 0x4000), EAP (Embedded Application Processor, Marvell PJ4C ARM at 500 MHz, 512 MB DDR3, running FreeBSD 9.0-RELEASE), and the Communication Processor (managing the EMC/EAP/KBL key chain with HMAC-SHA1). The EMC firmware is extractable via blsunpack from PUP files (SLB2 segment format, C0080001 version string) and decryptable with the documented AES-128-CBC key for revision c0. The EAP boot log has been captured (~50 seconds to CP Ready, services: emcd, uartd, disabler, DECI5s, DECI5). The CP Box (CPBH-100) provides hardware debug authentication via USB-C on TestKits.

**Confirmed Facts:**
- EMC firmware versions: v0.7.6 (SDK 0.85.070 prototype) through v1.14.3 (FW 9.20 retail)
- Serial flash W25Q16JVNIM at offset 0x4000, 0x7E000 bytes, SLB2 format, extractable with blsunpack
- EMC IPL encrypted with AES-128-CBC, key for revision c0 documented
- EAP runs FreeBSD 9.0-RELEASE on Marvell PJ4C rev 2 (ARM), 500 MHz, 512 MB DDR3 at 800 MHz
- EAP SDK version 5.501.000, Sycorax version 01.00.01.01
- CP Box provides Assist Mode on TestKits, persists across power cycles
- 256 dipswitches loaded from CP Box MMIO region, gated by console type (Retail: 0, TestKit: limited, DevKit: most, intdev DevKit: all 256)
- NVS stored on Winbond 25Q256JVEQ (32 MB) serial flash, offset 0x1C4000
- Key NVS offsets: 0x00 platform ID, 0x21 MAC address, 0x57 EAP startup, 0x60 DDR capacity, 0x1010 EMC checksum validation, 0x1012 EMC UART, 0x531F EAP UART, 0x1200 error log, 0x4000 serial number

**Unknowns:**
- Complete EMC firmware disassembly (partial, ~504 KB of ARM code, ongoing)
- Power-on initialization sequence details (beyond what error code analysis reveals)
- PSP communication protocol format and message types
- Error handling code paths and fault recovery mechanisms
- Firmware update mechanism within PUP files
- C0080001 file structure within SLB2 segments
- SLB2 segment format specification (beyond blsunpack capability)
- HMAC-SHA1 key chain structure managed by Communication Processor
- EMC revision-specific key derivation algorithm (only revision c0 documented)
- Key chain handoff protocol between PSP and CP during boot
- Whether the key chain can be dumped at runtime through EAP/CP Box access
- DECI5 protocol specification (message formats, channel IDs, signal behavior)
- cpupdate file format and signing mechanism
- CP Box authentication handshake with PS5
- DEV LAN network services exposed by EAP (beyond DHCP and DECI5)
- Whether UART is active on retail units (confirmed on prototypes FW <=0.85.070)
- Complete MMIO map and register set for Salina southbridge

**Impact:** Southbridge has complete system control — power sequencing, thermal management, error handling, peripheral I/O, debug authentication. Firmware-level persistence in EMC would survive OS reinstallation and factory reset. EAP running FreeBSD 9.0 has its own networking stack (DEV LAN), storage (512 MB DDR3, 32 MB NVS), and full OS capabilities — a potential independent attack platform. [[southbridge_analysis]] [[hardware_attack_surface]]

**Research Dependencies:**
- EMC firmware disassembly requires blsunpack + Ghidra with ARM processor module
- EAP boot log capture requires physical UART access on TestKit or prototype
- Key chain analysis requires runtime memory access on EAP (requires CP Box or physical UART)

---

#### 3. Hypervisor Codebase for FW >=7.00

**Status:** The PS5 uses a custom proprietary hypervisor (not Xen, KVM, or Hyper-V) built on AMD SVM extensions. FW <=2.70 had the hypervisor embedded in the kernel binary; FW >=3.00 uses a standalone hypervisor with the HyLonome (Hypervisor Loader) boot stage. The hypervisor provides Nested Page Tables (NPT/SLAT), xotext execute-only memory (bit 58 in NPT PTEs, custom AMD co-extension), Guest Mode Execute Trap (GMET), control register filtering (CR0/CR4/EFER), MSR Protection Map, and SMMU-based IOMMU control. 17 hypercalls (0x00-0x10 on FW >=3.00): message interface (2), self-loading (2), CPUID (2), IOMMU (7, 0x06-0x0C), error (1), VMClosure (1, >=3.00), MP boot (2, >=3.00).

**Confirmed Facts:**
- Known hypervisor exploits: TMR heap OOB (TheFloW, FW <=6.02), Byepervisor vtable/debug flag (FW <=2.70), Prosperous TMR protection edit (fail0verflow/flatz 2026, FW <=4.51)
- No public hypervisor exploits for FW >=7.00 as of mid-2026
- Hypervisor architecture split at FW 3.00 (pre-3.00: embedded in kernel; post-3.00: standalone + HyLonome)
- Single-guest partition model — entire GameOS runs as one VM
- xotext bit 58 in NPT PTEs, controlled through EFER bit 16 (nda/xotext), masked by hypervisor
- Filtered CR0 bits: PG (31), WP (16), NE (5), PE (0)
- Filtered CR4 bits: SMAP (21), SMEP (20), VME (0)
- Masked EFER bits: nda/xotext (16), SVME (12), NXE (11)
- TMR heap OOB and Prosperous both exploit the TMR subsystem
- VMClosure (hypercall 0x0E) and MP boot (0x0F-0x10) only exist on FW >=3.00

**Unknowns:**
- NPT layout strategies for FW 7.00+ — has the page table structure, PTE format, or walk algorithm changed since 6.00?
- xotext implementation details: how bit 58 interacts with instruction fetch, page walks, TLB behavior, and speculative execution
- Hypercall handler code paths for FW 7.00+ — complete disassembly and analysis of all 17 handlers
- VM exit handling for non-standard events: race conditions during concurrent NMI/SMI/interrupt delivery, TLB shootdown handling, APIC access emulation
- VMClosure mechanics: what state is saved, how the closure is initiated, whether cleanup can be interrupted
- Whether IOMMU handling changed in hypervisor code (7 of 17 hypercalls are IOMMU-related)
- Hypervisor binary format and loading mechanism (how it is packaged within the Secure Loader body)
- Whether any firmware-specific hypervisor patches or hardening were applied between 6.02 and 7.00
- The exact TMR implementation: memory region layout, encryption algorithm (AES-XTS? AES-CBC?), key management per region
- Whether the hypervisor flushes Branch Predictor Buffer on VM exits (Spectre v2 mitigation)
- Whether the hypervisor uses return thunks for Retbleed mitigation

**Impact:** The hypervisor wall at 6.02 is the single biggest blocker to full-chain jailbreak on modern firmware. No hypervisor escape means kernel exploits (when found) cannot disable kernel XOM, cannot read kernel .text, and cannot achieve stealthy persistence. [[hypervisor]] [[mitigation_assessment]]

**Research Dependencies:**
- Requires hypervisor binary extraction from PUP files for FW 7.00-13.40
- Requires disassembly toolchain (Ghidra with AMD64 SVM extensions)
- Prosperous and Byepervisor source code provide reference for hypervisor RE methodology
- Version diffing across FW 2.00, 3.00, 5.00, 7.00, 9.00, 11.00, 13.00 is the recommended approach

---

#### 4. GPU DMA Exploitation Internals

**Status:** The GPU DMA copy kernel exploit (FW >=6.00) is one of the most powerful kernel exploitation primitives — it reads and writes kernel .data pages through crafted GPU command buffers, bypassing CPU-level write protection. The exploit uses the GPU DMA engine accessed through libSceGnmDriver, the PS5 GPU driver. The IOMMU (managed exclusively by the hypervisor) is the only effective mitigation against this attack.

**Confirmed Facts:**
- GPU DMA copy bypasses kernel .data write protection on FW >=6.00
- The exploit submits crafted GPU command buffers through the GnmDriver interface
- The IOMMU should prevent DMA to kernel .data pages but the bypass exists
- The exploit was introduced with a GPU driver change at FW 6.00
- GPU has independent memory access through the unified GDDR6 memory pool (16 GB shared CPU/GPU)
- Hypervisor manages SMMU exclusively through hypercalls 0x06-0x0C
- 7 of 17 hypercalls are IOMMU-related, making this the most complex hypercall category

**Unknowns:**
- GPU command buffer structures: command format, buffer descriptors, submission model
- DMA engine programming model through libSceGnmDriver: how is DMA initiated, what are the target address constraints
- IOMMU configuration that SHOULD prevent DMA to kernel .data: what page tables are set up, what access permissions are enforced
- Why the GPU DMA copy exploit bypasses this protection: is it an IOMMU misconfiguration, a GPU hardware quirk, a race condition, or a missing permission check?
- Whether the IOMMU bypass is specific to GPU DMA or applies to other DMA-capable devices (storage, USB, networking, audio)
- Whether the bypass has been fixed or hardened in FW 13.40
- Whether GPU DMA can be used for reads-only, writes-only, or both
- Whether XOM-protected kernel .text can be read through GPU DMA (would bypass kernel XOM entirely)

**Impact:** GPU DMA is the most powerful kernel exploit primitive documented but is poorly understood theoretically. Understanding the bypass mechanism could reveal similar vulnerabilities in other DMA paths or inform IOMMU hardening strategies. [[attack_surface]] [[kernel]]

**Research Dependencies:**
- Requires reverse engineering libSceGnmDriver GPU command buffer submission
- Requires IOMMU page table state capture during GPU operation
- Requires GPU firmware analysis (VBIOS and GPU microcode)

---

### High-Value Research Directions

#### 5. Secure Module Boundary Mapping

**Status:** 20+ secure modules with authenticated service IDs (0x8002xxxx range) are dispatched by the SceSbl authentication manager (0x80021000). Documented modules include authmgr, kms (key management), pup (PUP update verification), pfs (filesystem), driveauth (BD drive pair+s), pltauth (platform challenge-response), npdrm (DRM), devact (device activation), qafutkn (QA tokens), sysveri (system verification), otpaccess (OTP fuse read), manu (manufacturing mode), fttrm (film/TV rights management), srtc (secure RTC), rootparam, exthdd, cloudsd, bar (backup/restore), otprsvaccess, diskid, idata, ddd, otpctrl, ncdt, hidauth.

**Confirmed Facts:**
- Service IDs in 0x8002xxxx range, dispatched by authmgr (0x80021000)
- Manufacturing module (0x8002100B) provides sceSblManuAuthSetManuMode, sceSblManuAuthLoadSecureModule, sceSblManuAuthUnloadSecureModule
- KMS (0x80021001) provides opaque handle-based key access — keys never exposed in plaintext
- IOCTL interface exists for manufacturing: set-manu-mode 0xC0184D03, load-module 0x40184D01, unload-module 0x40184D02
- Modules run in isolated execution contexts — compromise of one does not affect others
- SceSbl provides general services beyond module dispatch: sceSblServiceCrypt, sceSblTmrMap/Unmap, sceSblSecRegInit/Resume/Suspend, sceSblRngGetRandomNumber

**Unknowns:**
- Function identifier catalog for each module — complete list of exported functions
- Calling conventions, argument validation, and error handling per function
- Input validation coverage — do all functions validate their parameters?
- Cross-module call paths — which modules call each other, with what privileges?
- Shared memory interfaces — which regions are shared between modules and the kernel?
- authmgr dispatch mechanism — how are function IDs mapped to handlers?
- Whether any modules have debug or manufacturing interfaces that could be exploited
- The relationship between authmgr-secure modules and PSP TEE applications
- Whether secure module code is XOM-protected in the kernel address space

**Impact:** Cross-module privilege escalation could bypass secure boot requirements. Manufacturing module (0x8002100B) is particularly interesting — if reachable from userland, it can load unsigned secure modules. [[security_model]] [[kernel]]

---

#### 6. mast1c0re / PS2 Emulator JIT Pipeline

**Status:** The mast1c0re exploit family targets the PS2 emulator's JIT compiler. By crafting PS2 save data through Lua, Ren'Py, or YARPE game engines, attackers trigger the JIT to emit native x86 code. This provides usermode code execution without exploiting kernel bugs. The JIT is a design-level gap — it must be enabled for emulation performance but processes untrusted data through a code-generation pipeline.

**Confirmed Facts:**
- mast1c0re variants: Lua, Ren'Py, YARPE (different game engines using PS2 emulation)
- Targets Star Wars: Racer Revenge and other PS2 Classics running through the PS2 emulator
- Two PS2 emulation methods exist: PS4 SDK emulator (Method 1, FW ~2.00+, CUSA titles) and Native PS5 emulator (Method 2, FW ~9.00+, PPSA titles with savestates)
- mast1c0re Part 2 extends to FW 13.00
- Y2JB + mast1c0re chains have been proposed for userland-to-kernel paths
- The JIT bypasses all standard userland mitigations — JIT output is executable code by design
- No software mitigation can fully close this without disabling PS2 emulation

**Unknowns:**
- Which savedata formats trigger JIT compilation paths — what are the exact data structures for Lua/Ren'Py/YARPE?
- JIT compilation pipeline: source parsing → intermediate representation → code generation → code emission → execution
- Data structures used: how are savedata files parsed, what triggers JIT compilation
- JIT output buffer protection: is the output region XOM-protected, W^X, or both readable and writable?
- Constraints on generated x86 code: what register conventions, calling conventions, or output format constraints exist?
- Whether the Native PS5 emulator (Method 2, FW >=9.00) has the same JIT vulnerability or hardened it
- Whether the JIT output can be redirected to arbitrary memory (full control over where code lands)
- Whether the PS2 emulator's JIT can be exploited from USB game saves or only from installed games

**Impact:** mast1c0re is the highest-FW userland exploit path (confirmed through FW 13.00). Understanding it fully could extend its range beyond 13.00 and identify new primitives (arbitrary JIT output location gives kernel-level power). [[cve_timeline]] [[attack_surface]]

---

#### 7. CPU Microarchitecture Side Channels

**Status:** The PS5's Zen 2 cores carry architectural speculative execution vulnerabilities that cannot be fully mitigated: ZenBleed (CVE-2023-20593, FP register file leakage across process boundaries via DIV timing), Retbleed (CVE-2022-29900, RET branch prediction hijack bypassing retpolines), Inception/SRSO (CVE-2023-20569, return stack overflow), EntrySign (CVE-2024-36347, secure entry signature verification bypass). No public demonstrations exist on PS5 as of mid-2026.

**Confirmed Facts:**
- All Zen 2 cores are natively affected — no µarch revisions fix these in hardware
- AMD released microcode patches; PS5 firmware may or may not incorporate them
- The hypervisor's reaction to speculative execution attacks is entirely unknown
- EntrySign affects AMD Zen secure-entry mechanisms; PS5 custom hypervisor may have analogous vulnerabilities

**Unknowns:**
- Whether PSP crypto uses SIMD (XMM/YMM) registers (ZenBleed target) — if so, key material could leak across PSP↔OS boundary
- Whether the PS5 hypervisor incorporates Spectre v2 mitigations (IBRS, STIBP, IBPB, BPB flushing on VM exit)
- Whether return thunks or equivalent are used in hypervisor code (Retbleed mitigation)
- Whether EFER bit 16 (nda/xotext) is accessible speculatively — could speculative execution read XOM code?
- Whether entry signing is used for VM transitions between GameOS guest and hypervisor
- Whether Sinkclose (Zen-based SMM bypass) is applicable to PS5

**Impact:** Speculative execution attacks could break hypervisor or PSP isolation without exploiting any software bugs. ZenBleed key extraction from PSP would be the single highest-impact security research result possible. [[hardware_attack_surface]]

---

### Medium-Value Research Targets

#### 8. PS Portal Boot Chain

**Status:** The PS Portal is a custom Android 13 device with PS Link protocol. It supports fastboot (minus+USB at boot) and recovery modes (2 HID devices: PS Controller, PS Link Audio). PUP structure uses magic "DWCP" with Type=1, Full Size, and Version fields. Update endpoint is dwc.dl.playstation.net (JSON firmware info). PS Portal Master Key (GCM): `35 15 A8 8F 33 55 7D F1 33 FB F2 08 D6 3B 0A AF`. Firmware versions span 1.0.0 through 6.0.1+.

**Confirmed Facts:**
- Custom Android 13 operating system (not Orbis OS)
- Fastboot mode accessible via physical button combination
- Recovery mode exposes HID devices (PS Controller, PS Link Audio)
- Master key is documented (GCM mode AES key)
- Update protocol: JSON REST API at dwc.dl.playstation.net
- PUP magic "DWCP", different from PS5 native "DWCP" format

**Unknowns:**
- Boot chain firmware format details beyond "DWCP" magic
- Android security model differences from main PS5: SELinux policy, verified boot, key attestation
- DRM key handling: how does the Portal authenticate with PS5 for Remote Play?
- Whether fastboot is locked (production) or unlockable
- Whether custom boot images can be flashed via fastboot
- The relationship between Portal keys and PS5 keys (shared? separate?)
- Whether Portal firmware updates are signed with the same infrastructure as PS5
- Attack surface through PS Link protocol over Wi-Fi (MITM, protocol bugs)

**Impact:** PS Portal is a separate device with possibly weaker security (Android 13 is a well-understood platform). A Portal compromise could leak keys or techniques applicable to main PS5, or provide a lateral attack path through the Remote Play connection. [[hardware_overview]] [[hardware_attack_surface]]

---

#### 9. Manufacturing Mode Reachability

**Status:** Manufacturing mode IOCTLs exist in the kernel but their reachability conditions are undocumented. IOCTL codes: set-manu-mode 0xC0184D03, load-module 0x40184D01, unload-module 0x40184D02. The manu module (0x8002100B) provides sceSblManuAuth functions. Dipswitch 0xF1 is manu_mode related and gated by console type. An internal variant also exists: sceSblManuAuthSetManuModeInternal (0xC0184D0A).

**Confirmed Facts:**
- Manufacturing IOCTLs exist on /dev/manuauth device
- If reachable: load-module bypasses all signature verification for secure modules
- If reachable: unload-module can disable security modules (authmgr, pup, sysveri, npdrm)
- set-manu-mode persists manufacturing mode across reboots
- Dipswitch 0xF1 is manu_mode related, accessible by console type
- Retail consoles access 0 dipswitches; TestKit limited; DevKit most; intdev DevKit all 256
- QA tokens (QAF_SYS_DEV_I) existed with validity 2019-2021, bound to console OpenPSID

**Unknowns:**
- Whether manu IOCTLs are reachable from userland on any console type
- The exact relationship between dipswitch 0xF1 and manu_mode activation
- Whether manu module is loaded by default or requires specific boot conditions
- Whether OTP fuse modifications can enable manufacturing mode post-retail
- Whether Assist Mode (dipswitch 0x02) enables any manu capability on TestKits
- The authentication requirements for calling set-manu-mode (checked by authmgr)
- Whether the 2019-2021 QA tokens can be recovered from exploited DevKits

**Impact:** If reachable, manufacturing mode bypasses the entire signed module architecture — the foundation of PS5 code execution policy. [[southbridge_analysis]] [[security_model]]

---

#### 10. IOMMU Architecture

**Status:** The hypervisor manages the SMMU (System Memory Management Unit) exclusively through hypercalls 0x06-0x0C. This is an architectural shift from standard AMD platforms where the OS configures the IOMMU directly. 7 of 17 hypercalls are IOMMU-related, making this the largest and most complex hypercall category.

**Confirmed Facts:**
- Hypercall interface: SET_GUEST_BUFFERS (0x06), ENABLE_DEVICE (0x07), BIND_PASID (0x08), UNBIND_PASID (0x09), CHECK_CMD_COMPLETION (0x0A), CHECK_EVLOG_REGS (0x0B), READ_DEVICE_TABLE (0x0C)
- All DMA-capable devices (GPU, storage, USB, networking, audio) are managed through IOMMU
- ATS and PASID features introduce device-driven address translation complexity
- IOMMU page tables are separate from the NPT (stage-2) page tables

**Unknowns:**
- IOMMU page table format: page sizes supported (4 KB, 2 MB, 1 GB?), number of levels, PTE format
- Walk cache depth and TLB behavior for IOMMU translations
- Invalidation granularity: per-device, per-PASID, global?
- Whether IOMMU is AMD-Vi style or a custom SMMU implementation
- Whether race conditions exist in IOMMU command queue processing
- Whether IOMMU event log reporting could leak hypervisor memory layout
- How GPU DMA bypass (kernel .data write) relates to IOMMU configuration
- Whether the IOMMU is configured identically across all firmware versions

**Impact:** IOMMU is critical for both hypervisor security analysis and GPU DMA exploitation understanding. [[hypervisor]] [[attack_surface]]

---

#### 11. Anti-Rollback Mechanism

**Status:** Anti-rollback is enforced through two complementary systems: Security Revision (4 bytes at offset 0x11C in Secure Loader header, monotonic OTP-burned fuse: 0x00000001 through 0x0003FFFF) and Revision Nonce (32 bytes SHA-256 at offset 0x120, used in Layer 2 AES-CBC key derivation). Seven nonces documented for revisions 0xA0 through 0x100.

**Confirmed Facts:**
- Security revision values: 0x00000001 (FW 0.85-1.XX), 0x00000007 (FW 1.00-6.02), 0x000000FF (FW 6.50), 0x000003FF (FW 7.00-7.61), 0x00000FFF (FW 8.00-8.60), 0x00003FFF (FW 9.00-9.60), 0x0000FFFF (FW 10.00-10.60), 0x0003FFFF (FW 11.00+)
- Revision nonces: 0xA0 (E3D98F94...), 0xB0 (551814A6...), 0xC0 (B35979B6...), 0xD0 (1CB39112...), 0xE0 (FD50C29C...), 0xF0 (6F20B45B...), 0x100 (50C0E399...)
- Nonce is used in Layer 2 AES-CBC key derivation — without it, firmware cannot be decrypted
- OTP fuses are write-once and cannot be reversed
- /WP pin on serial flash tied to 3.3V_SS_PG1 prevents unauthorized flash writes during operation

**Unknowns:**
- Exactly how fuse burning is triggered: is it during PUP installation, at first boot after update, or on-demand?
- What specific conditions cause a fuse burn: security version mismatch, downgrade attempt detection?
- Revision nonce structure: is it truly SHA-256 of the revision identifier? What is the exact input?
- Nonce rollover algorithm: how is the nonce derived per revision (pseudorandom, hash chain)?
- Whether anti-rollback can be bypassed via fw_unlock tool (if such a tool exists)
- Whether voltage glitching can bypass the fuse check (One Glitch to Rule Them All paper, Buhren et al., applies to Zen 1-3)
- Whether chip-off serial flash modification + OTP fuse bypass is feasible
- Whether there are documented revision nonces for revisions beyond 0x100 (FW 13.00+)

**Impact:** Anti-rollback bypass would enable firmware downgrade to exploitable versions. [[secure_boot]] [[boot_chain]]

---

#### 12. Kernel Syscall Catalog

**Status:** The PS5 syscall table (from kernel 2.20) has 500+ entries across 5 ranges: 0x00-0x5F standard BSD, 0x60-0x8F extended BSD and networking, 0x90-0xFF POSIX extensions, 0x100-0x17F modern BSD, 0x180+ PS4/PS5 specific. Three sysvec structures dispatch PS4 SELF, FreeBSD ELF64, and Native SELF.

**Confirmed Facts:**
- FreeBSD 11.0 base (__FreeBSD_version 1100122)
- Three sysvec structures: PS4 SELF (backward compat), FreeBSD ELF64 (normally unused), Native SELF
- Console naming: `sys_compat.*` (PS4 wrappers), `sys_compat4/6/7.*` (FreeBSD legacy compat), `sys_number*` (unnamed, likely PS5-specific), `sys_obsolete*` (deprecated)
- Known exploitable syscalls: kqueue, socket (netcontrol), aio, umtx_shm, IPV6_2292PKTOPTIONS
- 100+ IOCTL device entries under /dev/
- NX, SMAP, SMEP, UMIP, xotext (EFER bit 16) enforced

**Unknowns:**
- Complete annotated list of all 500+ syscalls — identify what is trimmed, modified, or added vs stock FreeBSD 11.0
- PS5-specific syscalls beyond 0x180 — undocumented and most likely for undiscovered exploits
- Whether the syscall table is the same across all firmware versions (version diffing needed)
- Which syscalls have Sony-added security checks (credential verification, capability gates)
- The exact syscall number for each PS5-specific addition
- Whether any stock FreeBSD syscalls were removed or replaced
- Complete IOCTL catalog with descriptions for 100+ /dev/ entries

**Impact:** Essential reference for kernel exploit development. PS5-specific syscalls beyond 0x180 lack compatibility constraints and are the most likely kernel exploitation vectors. [[kernel]] [[cve_timeline]]

---

### Low-Value / Speculative

#### 13. SEV Interaction with Custom Hypervisor

**Status:** AMD Secure Encrypted Virtualization (SEV/SEV-ES) features are available on Zen 2 but whether the PS5 custom hypervisor uses them is unknown.

**Analysis:** SEV provides memory encryption per-VM with hardware-managed encryption keys. The PS5 predates broad SEV adoption (SEV-SNP was released 2022+). The custom hypervisor is single-guest (not multi-tenant), so SEV's primary use case — protecting VMs from a malicious hypervisor — is reversed here (hypervisor protects itself from the guest). SEV use is unlikely but confirmation would definitively close this question. [[hypervisor]] [[security_model]]

---

#### 14. HDCP/HDMI Key Extraction

**Status:** HDCP 2.3 key storage in the Panasonic MN864739 HDMI retimer (codename FLAVA). The chip converts 4-lane DisplayPort from SoC to HDMI 2.0 with 4 TMDS channels. Communication via Host I2C (HSDA/HSCL). Error codes 0xC0810002-0xC0810303 indicate HDMI IC problems.

**Analysis:** HDCP 2.3 master key compromise would not affect PS5 specifically but could enable HDMI signal interception for media piracy. Key extraction would require I2C bus monitoring, side-channel analysis, or MN864739 firmware reverse engineering. Low priority for PS5 security research specifically. [[hardware_overview]] [[hardware_attack_surface]]

---

#### 15. DualSense Bluetooth HID Attacks

**Status:** The DualSense controller (codename Bond, CXD9006GG main MCU) uses Bluetooth 5.1 with cryptographic pairing. HID commands include Get MCU Unique ID (ReportID=128, ActionID=9), Read/Erase Device Info (ActionID=12/13), NVS Lock/Unlock (DeviceID=3), Set DFU Mode (ReportID=160). Three DFU modes: PBL (flash SBL only), SBL (flash Main/Venom/Onion), Main Mode (Venom/Onion/BT patches).

**Analysis:** Erase Device Info (ActionID=13) is marked DANGER. NVS unlock (ActionID=2) grants access to non-volatile storage. DFU mode switching could allow malicious firmware injection. However, pairing is cryptographically bound and requires physical proximity (~10m Bluetooth range). Medium-value attack surface for persistence/escalation but low likelihood against a locked-down console. [[hardware_attack_surface]]

---

## Prioritized Research Agenda

### Tier 1: Immediate (0-6 months)

| Priority | Direction | Expected Impact | Difficulty | Key Dependencies |
|----------|-----------|----------------|------------|-----------------|
| 1 | Southbridge firmware disassembly: EMC/EAP from PUP using blsunpack + Ghidra ARM | Undetectable firmware rootkit, complete attack surface understanding of power/thermal/error management, EAP FreeBSD 9.0 network services | Medium | PUP extraction, blsunpack, Ghidra ARM module; AES-128-CBC key for EMC rev c0 documented |
| 2 | Y2JB sandbox escape: V8 CVE-2021-38003 TheHole leak to system services via crafted V8 heap layout | Extends userland entry from YouTube app to full system service access on latest firmware (13.40) | Medium | Understanding of YouTube app sandbox boundaries, V8 engine heap manipulation, WebView API surface |
| 3 | New kernel exploit search: FreeBSD kqueue/socket/IPC UaF and double-free fuzzing | Restores kernel capability on FW 12.70+ (currently no public kernel exploit) | Medium | Kernel disassembly from PUP, syscall catalog, FreeBSD vulnerability research methodology |
| 4 | GPU DMA IOMMU bypass analysis: libSceGnmDriver RE + IOMMU state capture | Documents the most powerful kernel exploit primitive; potentially reveals new DMA bypasses | High | GPU driver RE, IOMMU register state documentation, hypercall trace capture |

### Tier 2: Short-Term (6-12 months)

| Priority | Direction | Expected Impact | Difficulty | Key Dependencies |
|----------|-----------|----------------|------------|-----------------|
| 5 | Hypercall version diffing: compare hypervisor binaries across FW 2.00, 3.00, 5.00, 7.00, 9.00, 11.00, 13.00 | Identify regression vulnerabilities, changed validation logic, removed checks in 7.00+ hypervisor | High | Hypervisor binary extraction from all FW versions, Ghidra automated diffing, TMR handler understanding |
| 6 | Kernel syscall catalog: complete annotated list of 500+ syscalls identifying trimmed/modified/added | Essential reference for kernel exploit development — maps entire kernel attack surface | Low | Kernel binary extraction, FreeBSD 11.0 source reference for diffing |
| 7 | mast1c0re JIT pipeline: reverse engineer PS2 emulator JIT compilation for Lua/Ren'Py/YARPE | Extend highest-FW exploit path; potentially discover JIT output control for kernel-level primitives | High | PS2 emulator binary extraction, dynamic analysis of JIT compilation triggers |
| 8 | PSP firmware extraction and disassembly: NAND dump analysis, ARM executable format identification | Boot-level attack capability; first public PSP firmware analysis | Very High | NAND dumps from exploited console, unknown ARM executable format analysis |

### Tier 3: Long-Term (1-3 years)

| Priority | Direction | Expected Impact | Difficulty | Key Dependencies |
|----------|-----------|----------------|------------|-----------------|
| 9 | Hypervisor exploit for FW >=7.00: TMR management, hypercall parameter validation, VM exit edge cases | Full chain jailbreak on modern firmware — the defining challenge of PS5 research | Very High | Hypervisor version diffing, TMR implementation understanding, hypercall fuzzing framework |
| 10 | ZenBleed key extraction from PSP: timing side-channel across PSP↔OS boundary | Extract cryptographic keys from PSP via SIMD register leakage | Extreme | Kernel-level code execution on x86 cores, PSP SIMD usage confirmation, precise timing infrastructure |
| 11 | Boot ROM vulnerability research: mask ROM analysis via firmware behavior side channels | Permanent unpatched exploit — breaks entire chain of trust | Extreme | PSP firmware analysis, physical access, fault injection equipment |
| 12 | Boot chain reimplementation: open-source replacement for Secure Loader, hypervisor, kernel | Custom firmware loading capability — ultimate research goal | Extreme | Full boot chain understanding, all cryptographic keys, hardware modification capability |

## Methodology Recommendations

### Tooling Needed

**Firmware Extraction and Analysis:**
- blsunpack: SLB2 segment extraction from serial flash dumps and PUP files
- Ghidra with ARM processor module: EMC firmware disassembly (504 KB ARM code)
- Ghidra with AMD64 SVM extensions: hypervisor binary analysis (17 hypercalls, NPT/VMCB structures)
- PUP decryption tools: PS5-Pup-Decrypt, PS5-Pup-Unpacker (Zecoxao), PS5 Tools (SKFU) — decryption keys for current FW may not be public
- PS5 Firmware Checker: automated version tracking and PUP download monitoring
- PS5Prxy: MITM proxy for analyzing system software update requests

**Debugging and Runtime Analysis:**
- GDB for kernel debugging (via DECI5 on TestKits, via exploit on retail)
- Custom Frida scripts for runtime analysis of userland processes (V8 heap, WebKit, BD-J)
- Hypercall trace capture: intercept vmmcall instructions to catalog hypercall parameters
- IOMMU state capture: read device tables, page tables, event logs through hypercalls 0x0B-0x0C

**Hardware Probing and Fault Injection:**
- JTAGulator: debug interface scanning on unknown motherboard revisions
- ChipWhisperer (CW1173): voltage glitching for PSP fault injection
- Saleae logic analyzer (Pro 16): SPI bus capture, UART decoding, timing analysis
- Raspberry Pi GPIO + flashrom: W25Q16JVNIM serial flash dumping
- Pomona SOIC-8 clip: in-circuit serial flash programming without desoldering
- Hot air rework station: chip-off flash removal for external programming
- CNC XYZ table + high-voltage probe: EM fault injection (EMFI)

**Reverse Engineering Infrastructure:**
- PUP archive for every firmware version (FW 1.00 through 13.40) from Internet Archive, Midnight Archive, Darthsternie
- DevKit/TestKit PUP files from Yandex archives (for comparison with retail)
- Version diffing framework: automated binary comparison across FW versions using Ghidra Headless + Diaphora
- NAND dump from exploited unit: critical for PSP firmware and secure module analysis

### Collaboration Priorities

**Researchers to Follow and Their Current Work:**
- TheFloW (Andy Nguyen): BD-JB family, CVE-2020-7457, TMR heap OOB, netcontrol — the most prolific PS5 vulnerability researcher. Follow for TMR management insights applicable to >=7.00 hypervisor analysis.
- fail0verflow/flatz: Prosperous hypervisor exploit (FW <=4.51). Their TMR protection state editing technique is the best reference for understanding the TMR subsystem.
- Specter: Byepervisor hypervisor exploit (FW <=2.70). His approach to hypervisor binary analysis and vtable manipulation is foundational.
- Gezine: P2JB (kqueueex), Y2JB, YarP2JB. Primary researcher for the Y2JB chain — critical for understanding the unpatched V8 exploit path.
- idlesauce: UMTX2 jailbreak (PSFree + umtx_shm). Kernel exploit specialist for the umtx subsystem.
- ps5dev community: Lapse (aio_multi_delete), etaHEN development. Community coordination hub for exploit chain integration.

**Communities to Monitor:**
- PS5DevWiki (https://www.psdevwiki.com/ps5/) — the central documentation repository; contribute findings back
- PS5 jailbreak subreddit and Discord communities — exploit chain testing and compatibility reports
- Sony HackerOne program — vulnerability disclosure patterns indicate Sony's patching priorities
- Academic security conferences (HardWear.io, Hexacon, CCC, WOOT) — new exploit techniques and disclosures

**Coordination Strategy:**
- Avoid duplicating work: check published research on psdevwiki and GitHub before starting new analysis
- Publish partial findings incrementally (disassembly progress, IOCTL discoveries, version diffs) rather than waiting for complete results
- Use the open questions register (open_questions.md) and assumptions register (assumptions.md) to track what is known vs unknown
- Cross-reference PS4 research: many architectural concepts (SceSbl, SELF format, XOM) are evolutionary rather than revolutionary

### Documentation Standards

All research findings should be captured in this repository following these conventions:

**File Organization:**
- `research/hardware/` — hardware architecture, southbridge, attack surface
- `research/firmware/` — boot chain, secure boot, PSP, EMC/EAP
- `research/hypervisor/` — hypervisor architecture, hypercall interface, TMR, IOMMU
- `research/kernel/` — kernel architecture, syscalls, IOCTL, secure modules
- `research/security_model/` — Auth IDs, PAIDs, XOM, key hierarchy, CP Box
- `research/userland/` — WebKit, BD-J, V8, mast1c0re, JIT analysis
- `research/analysis/` — synthesis, attack surface, mitigation assessment, roadmap
- `research/exploit_history/` — CVE timeline, exploit chains
- `sources/web/psdevwiki/` — raw source data categorized by system layer

**Documentation Standards:**
- Use [[wikilinks]] to connect research documents (e.g., [[southbridge_analysis]] to reference detailed southbridge findings)
- Distinguish confirmed facts from speculation explicitly: "Confirmed:" vs "Unknown:" vs "Speculative:"
- Track open questions as `Q-{CRIT|IMP|MIN}-{NNN}` in open_questions.md
- Track assumptions as `ASM-NNN` in assumptions.md with confidence rating and status
- Include source URLs and psdevwiki references for all factual claims
- Use consistent naming for firmware versions (FW X.YY format)
- Document kernel analysis with the syscall number, not just the name

## Relationship to Existing Work

This roadmap builds on every existing research file in this repository:

### Hardware Layer
- [[hardware_overview]] — SoC architecture (Oberon/Viola), memory subsystem (GDDR6 448 GB/s), storage (825 GB PCIe 4.0 SSD), motherboard revisions, serial flash W25Q16JVNIM, southbridge CXD90061GG, power system (XDPE14286A VRM), peripheral connectivity
- [[hardware_attack_surface]] — SPI serial flash dumping and modification, JTAG/SWD debug interface accessibility, UART, voltage glitching references (Buhren et al., One Glitch to Rule Them All), speculative execution vulnerabilities (ZenBleed, Retbleed, EntrySign, Inception), peripheral attack surface (USB, M.2 SSD DMA, Bluetooth, Wi-Fi, disc drive, PS VR2, PS Portal)

### Firmware Layer
- [[boot_chain]] — five primary stages from Boot ROM to kernel launch, Secure Loader IPL header structure (magic E4 DB 7C 02, RSA-4096 at offset 0x200, Security Revision at 0x11C, Revision Nonce at 0x120, dual-layer AES-CBC), EMC firmware at serial flash offset 0x4000, CP Box debug authentication
- [[secure_boot]] — RSA-4096 verification algorithm (RSASSA-PKCS1-v1_5 with SHA-256), AES-128-CBC dual-layer decryption, SHA-256 integrity verification, key hierarchy (ROM Keys 2-9, Secure Loader keys, EMC/EAP/KBL key chain, communication processor keys), anti-rollback enforcement

### Hypervisor Layer
- [[hypervisor]] — custom proprietary hypervisor (not Xen/KVM/Hyper-V), AMD SVM features (NPT, GMET, CR/MSR filtering, xotext bit 58), 17 hypercalls 0x00-0x10, single-guest partition model, architecture split at FW 3.00 (embedded vs standalone + HyLonome), TMR management, VMClosure

### Kernel Layer
- [[kernel]] — FreeBSD 11.0 derivative (1100122), three sysvec structures (PS4 SELF, FreeBSD ELF64, Native SELF), 500+ syscalls across 5 ranges, 100+ IOCTL devices, 20+ secure modules (0x8002xxxx), XOM (usermode and kernel), SMAP/SMEP/UMIP, KASLR

### Security Model
- [[security_model]] — Auth IDs (41=kernel, 48=system process, 49=system library), PAIDs, SELF binary signing, key hierarchy (ROM keys, PKG RSA-3072 fully leaked, trophy keys shared with PS4, portability keys, M.2 dummy keys), Keystone trust anchor, CP Box authentication, secure modules catalog

### System Architecture
- [[system_overview]] — Orbis OS overview, firmware version history (FW 1.00 through 13.40), system software layer (RNPS applications NPXS40xxx), boot process chain, Safe Mode, firmware update mechanism, backward compatibility (PS4, PS2 emulator methods), system registry

### Analysis Documents
- [[synthesis]] — cross-cutting findings (PS4-PS5 key sharing, PS2 emulator JIT design gap, GPU DMA bypass, firmware architecture split at FW 3.00, southbridge as underexplored surface, kernel exploit cadence), high-value targets (Boot ROM, PSP firmware, hypervisor 7.00+, southbridge)
- [[attack_surface]] — entry point ranking (Y2JB #1, WebKit #2, BD-J #3, mast1c0re #4, kernel UaF #5-7, hypercall interface #8), hardware/firmware/hypervisor/kernel/userland attack surface enumeration
- [[mitigation_assessment]] — hardware mitigations (PSP, OTP fuses, Keystone XOM, SMMU/IOMMU), boot chain mitigations (dual-layer AES-CBC, RSA-4096/3072, anti-rollback, HyLonome), hypervisor mitigations (NPT, xotext, GMET, CR filtering, MSRPM, VMClosure), kernel mitigations (XOM, SMAP/SMEP/UMIP, KASLR, SceSbl sandboxing), userland mitigations (WebKit sandbox, nullfs, capability model, SELF signing)

### Exploit History
- [[cve_timeline]] — WebKit CVEs (CVE-2022-22620, CVE-2023-38600, CVE-2023-28205, CVE-2021-38003), kernel CVEs (CVE-2020-7457, CVE-2024-43102), non-CVE kernel exploits (kqueueex, netcontrol, fsc2h_ctrl, aio_multi_delete, exFAT overflow, GPU DMA copy, SMAP bypass), hypervisor exploits (Byepervisor, TMR Heap OOB, Prosperous, APIC pointers), Zen 2 µarch CVEs (ZenBleed CVE-2023-20593, Retbleed CVE-2022-29900, Inception CVE-2023-20569, EntrySign CVE-2024-36347), BD-JB bug chain chronology

### Source Data
- sources/web/psdevwiki/security/vulnerabilities.md — comprehensive vulnerability catalog
- sources/web/psdevwiki/system_software/exploit_chains.md — FW-to-exploit compatibility matrix
- sources/web/psdevwiki/debugging/manufacturing_functions.md — manufacturing IOCTL catalog
- sources/web/psdevwiki/debugging/dipsw.md — 256 dipswitch boot parameters
- sources/web/psdevwiki/kernel/kernel_overview.md — FreeBSD 11.0 base, three sysvec structures
- sources/web/psdevwiki/kernel/syscalls.md — syscall table ranges 0x00-0x1FF, naming conventions
- sources/web/psdevwiki/kernel/ioctl.md — PUP, TEE, manufacturing IOCTL codes
- sources/web/psdevwiki/hypervisor/hypervisor.md — 17 hypercalls, SVM features, xotext bit 58
- sources/web/psdevwiki/hypervisor/hypervisor_loader.md — HyLonome codename, FW 3.00 introduction

### Tracking Documents
- [[open_questions]] — 5 critical questions, 12 important questions, 10 minor questions tracking specific unknowns
- [[assumptions]] — 9 tracked assumptions (ASM-001 through ASM-009) with confidence ratings and validation status

## Conclusions

The PS5 security research field is at an inflection point. Userland access is reliably achievable on virtually all firmware versions through multiple independent paths (Y2JB unpatched on 13.40, BD-JB-EX through 12.70, mast1c0re through 13.00). Kernel exploits have followed a predictable cadence of roughly one per major firmware release cycle, with the current gap at FW 13.00+ likely temporary. The hypervisor, however, has proven substantially more resilient — no public exploits exist for FW >=7.00 as of mid-2026, creating a four-year gap since the last public hypervisor vulnerability.

The most likely breakthrough scenarios, in descending order of probability:

1. **A new kernel exploit (FW 13.00+)** restores partial capability through known FreeBSD vulnerability classes (UaF, double-free in kqueue, socket, or IPC subsystems). This is the most predictable outcome given the historical cadence.

2. **Hypervisor version regression** — a vulnerability removed in one FW version that reappears in a later version, discovered through systematic cross-version diffing of hypercall handlers. The IOMMU hypercalls (0x06-0x0C) are the most promising target given their complexity.

3. **Southbridge firmware vulnerability** enables an alternative attack path that bypasses the main x86 security model. The EMC firmware's debug flags (checksum validation disable at NVS 0x1010, UART enable at 0x1012) and the manufacturing mode IOCTL interface are the most promising targets.

4. **PSP firmware exploit** — the highest-impact but lowest-probability breakthrough. Would require extracting PSP firmware from NAND dumps, identifying the ARM executable format, and finding a vulnerability in the PSP's cryptographic or key management code.

5. **Speculative execution key extraction** — ZenBleed applied across the PSP↔OS boundary could leak cryptographic keys. This is purely theoretical and hinges on whether PSP crypto uses SIMD registers.

The strategic recommendation is to invest heavily in southbridge firmware analysis (Tier 1, highest practical impact) and hypercall version diffing (Tier 2, highest potential impact for modern FW). These two directions offer the best risk-reward ratio given current tooling and knowledge. The kernel exploit gap is likely temporary and will be filled by ongoing community research. The mast1c0re JIT pipeline is the highest-priority userland research direction due to its broad FW coverage and potential for new primitives.

The hypervisor wall remains the defining challenge. Every firmware version >=7.00 without a public hypervisor exploit represents a hardening validation that Sony's architectural investment has been effective. Whether this reflects genuine security or merely insufficient research attention is the open question that this roadmap is designed to answer.

## References

### Research Documents (this repository)
- research/analysis/synthesis.md
- research/analysis/attack_surface.md
- research/analysis/mitigation_assessment.md
- research/exploit_history/cve_timeline.md
- research/kernel/kernel.md
- research/hypervisor/hypervisor.md
- research/security_model/security_model.md
- research/firmware/boot_chain.md
- research/firmware/secure_boot.md
- research/system_overview/system_overview.md
- research/hardware/hardware_overview.md
- research/hardware/hardware_attack_surface.md
- research/hardware/southbridge_analysis.md
- open_questions.md
- assumptions.md

### psdevwiki Sources
- https://www.psdevwiki.com/ps5/Vulnerabilities
- https://www.psdevwiki.com/ps5/Bugs
- https://www.psdevwiki.com/ps5/Exploit_Chains
- https://www.psdevwiki.com/ps5/Homebrew_Enabler
- https://www.psdevwiki.com/ps5/System_Software
- https://www.psdevwiki.com/ps5/Kernel
- https://www.psdevwiki.com/ps5/Kernel_Functions
- https://www.psdevwiki.com/ps5/Syscalls
- https://www.psdevwiki.com/ps5/IOCTL
- https://www.psdevwiki.com/ps5/Devices
- https://www.psdevwiki.com/ps5/Secure_Modules
- https://www.psdevwiki.com/ps5/SceSbl_Functions
- https://www.psdevwiki.com/ps5/Hypervisor
- https://www.psdevwiki.com/ps5/Hypervisor_Loader
- https://www.psdevwiki.com/ps5/Secure_Loader
- https://www.psdevwiki.com/ps5/Keys
- https://www.psdevwiki.com/ps5/EMC
- https://www.psdevwiki.com/ps5/XOM
- https://www.psdevwiki.com/ps5/Keystone
- https://www.psdevwiki.com/ps5/Auth_IDs
- https://www.psdevwiki.com/ps5/Program_Authority_ID
- https://www.psdevwiki.com/ps5/Magics
- https://www.psdevwiki.com/ps5/Passcode
- https://www.psdevwiki.com/ps5/Serial_Flash
- https://www.psdevwiki.com/ps5/25Q16JVNIM
- https://www.psdevwiki.com/ps5/AMD_Platform_Security_Processor
- https://www.psdevwiki.com/ps5/CP_Box
- https://www.psdevwiki.com/ps5/CP_Box_Boot_Process
- https://www.psdevwiki.com/ps5/CP_Box_Non_Volatile_Storage
- https://www.psdevwiki.com/ps5/CP_Box_Service_Connectors
- https://www.psdevwiki.com/ps5/Debugging
- https://www.psdevwiki.com/ps5/DECI5
- https://www.psdevwiki.com/ps5/Dipsw
- https://www.psdevwiki.com/ps5/Manufacturing_Functions
- https://www.psdevwiki.com/ps5/QA_Flags
- https://www.psdevwiki.com/ps5/UART
- https://www.psdevwiki.com/ps5/Southbridge_Error_Codes
- https://www.psdevwiki.com/ps5/CXD90060GG
- https://www.psdevwiki.com/ps5/CXD90061GG
- https://www.psdevwiki.com/ps5/CXD90062GG
- https://www.psdevwiki.com/ps5/MN864739
- https://www.psdevwiki.com/ps5/XDPE14286A
- https://www.psdevwiki.com/ps5/Bond
- https://www.psdevwiki.com/ps5/DualSense
- https://www.psdevwiki.com/ps5/DualSense_DFU_Modes
- https://www.psdevwiki.com/ps5/DualSense_HID_Commands
- https://www.psdevwiki.com/ps5/PS_Portal
- https://www.psdevwiki.com/ps5/PSVR2
- https://www.psdevwiki.com/ps5/PSVR2_Update_Format
- https://www.psdevwiki.com/ps5/Jigkick_Files
- https://www.psdevwiki.com/ps5/Prototype_Units
- https://www.psdevwiki.com/ps5/MMIO_Prototype
- https://www.psdevwiki.com/ps5/Codenames
- https://www.psdevwiki.com/ps5/Motherboards
- https://www.psdevwiki.com/ps5/Backwards_compatibility
- https://www.psdevwiki.com/ps5/PS2_Emulation
- https://www.psdevwiki.com/ps5/Save_Data
- https://www.psdevwiki.com/ps5/Registry
- https://www.psdevwiki.com/ps5/Button_Combos
- https://www.psdevwiki.com/ps5/Build_Strings
- https://www.psdevwiki.com/ps5/Error_Codes
- https://www.psdevwiki.com/ps5/%E2%98%85_Debug_Settings

### CVE References
- CVE-2020-7457 — IPV6_2292PKTOPTIONS UaF (FW 3.00-4.51)
- CVE-2021-38003 — V8 JSON.stringify TheHole leak (Y2JB, FW 2.00-13.40, unpatched)
- CVE-2022-22620 — WebKit loadInSameDocument UaF (PSFree, FW <=5.50)
- CVE-2022-29900/CVE-2022-29901 — Retbleed (Zen 2)
- CVE-2023-20569 — Inception/SRSO (Zen 2)
- CVE-2023-20593 — ZenBleed (Zen 2)
- CVE-2023-28205 — WebKit CloneDeserializer UaF
- CVE-2023-38600 — WebKit integer underflow (FW 6.00-8.60)
- CVE-2023-41993 — JSC DFG clobberize (JIT disabled, not exploitable)
- CVE-2024-0517 — Chrome V8 integer overflow (untested on PS5)
- CVE-2024-27833 — JSC SBFX overflow (JIT disabled, not exploitable)
- CVE-2024-36347 — EntrySign (Zen 2 secure boot bypass)
- CVE-2024-43102 — umtx_shm UaF (FW <=7.61)

### Academic and Research References
- Buhren et al., "One Glitch to Rule Them All: Fault Attacks on AMD Secure Processor" (arXiv:2108.04575, 2021)
- AMD-SP / PSPReverse open-source project
- fail0verflow PS4/PS5 research publications
- TheFloW (Andy Nguyen) — BD-JB, TMR heap OOB, netcontrol, HardWear.io/Hexacon presentations
- Specter — Byepervisor hypervisor exploit
- flatz — Prosperous hypervisor exploit

### Community Tools and Repositories
- https://github.com/TheOfficialFloW/bd-jb
- https://github.com/ps5dev/Lapse
- https://github.com/Gezine/Luac0re
- https://github.com/idlesauce/umtx2
- https://docs.google.com/spreadsheets/d/1dgu0p7U2yB_mhcUELz-Wkc7Yhs-avoWLY1Gcm0n5XJw/edit (PS5 Jailbreak Compatibility Sheet)
- https://github.com/KuromeSan/ps5-lib-il2cpp
- https://github.com/InoriRus/Kyty (PS5 emulator)
