# PS5 Research Synthesis

## Overview

This synthesis consolidates findings across all PS5 security research
layers — hardware, firmware, hypervisor, kernel, userland, and the security
model that binds them together. The PlayStation 5 represents a significant
security architecture evolution from the PlayStation 4, adding hypervisor-
backed eXecute-Only Memory (XOM), a dedicated Hypervisor Loader (HyLonome)
on firmware versions 3.00 and later, dual-layer AES-CBC encryption with
revision nonces for anti-rollback, and an expanded secure module system
with 20+ authenticated service IDs (0x8002xxxx range).

The platform's security is rooted in the AMD PSP's immutable Boot ROM and
write-once OTP fuses, with cryptographic verification at every stage
transition: RSA-4096 for the Secure Loader header, dual-layer AES-CBC for
the IPL body, SHA-256 integrity checking, RSA-3072 for kernel SELF signing,
and HMAC-SHA1 for the Communication Processor key chain. The hypervisor,
a custom proprietary implementation built on AMD SVM extensions, provides
nested page tables, the custom xotext execute-only memory feature (bit 58
in NPT PTEs), Guest Mode Execute Trap (GMET), control register filtering,
and SMMU-based IOMMU control.

Despite this depth, the platform has been compromised at every layer through
software attacks. Userland has been breached through WebKit use-after-free
bugs (CVE-2022-22620), BD-J exploits (BD-JB family spanning FW <=12.70),
V8 exploits in YouTube and Netflix apps (Y2JB unpatched as of FW 13.40),
and the mast1c0re family targeting the PS2 emulator JIT. The kernel has
12+ documented vulnerability classes spanning ucred refcount leaks
(kqueueex), double fdrop (netcontrol), stack buffer errors (fsc2h_ctrl),
double free (aio_multi_delete), race conditions (umtx_shm CVE-2024-43102),
IPv6 option handling (CVE-2020-7457), GPU DMA bypass, exFAT overflow, and
SMAP bypass. The hypervisor has seen limited exploitation confined to early
firmware: TMR heap OOB (TheFloW, FW <=6.02), Byepervisor (FW <=2.70), and
Prosperous (fail0verflow/flatz 2026, FW <=4.51). No public hypervisor
exploits exist for FW >=7.00 as of mid-2026.

Cross-cutting themes include: the shared PS4 key material creating cross-
generation systemic risk, the PS2 emulator JIT as a design-level security
gap, the GPU DMA engine's ability to subvert software write protections,
and the architectural AMD Zen 2 vulnerabilities that represent permanent
hardware weaknesses. The kernel vulnerability discovery rate suggests
roughly one exploitable bug per major firmware release cycle. Y2JB remains
the longest-lived current vector, affecting FW 2.00-13.40 with no patch as
of FW 13.40. The hypervisor's resilience compared to the kernel suggests
that Sony's architectural investment has been effective.

## Layer Summaries

**Hardware**: The PS5 uses a custom AMD Zen 2 APU (Oberon for original PS5,
Viola for PS5 Pro) with 8 Zen 2 cores (16 threads, up to 3.5 GHz) and an
RDNA 2 GPU (up to 2.23 GHz, 10.28 TFLOPS). Memory is 16 GB GDDR6 (Micron
MT61K512M32KPA-14C:B, 256-bit bus, 448 GB/s, 4 channels E0/E1/D0/D1).
Storage includes a soldered 825 GB PCIe 4.0 SSD (SIE CXD90062GG Zao
controller) plus M.2 expansion (250 GB-8 TB). The southbridge CXD90061GG
(Salina, MediaTek MT3613CT based) provides Gigabit Ethernet, SATA, USB 2.0,
PCIe, I2C, SPI, UART, and PWM. Serial flash Winbond W25Q16JVNIM (2 MB, SPI)
stores the Secure Loader IPL and EMC firmware. The AMD PSP (Ariel) serves
as the root of trust. Four co-processors support the system: MP0 (PSP for
security), MP1 (SMU Xtensa for power/clock/thermal), MP3 (TEE for PlayReady
SL3000 DRM), MP4 (ARM Cortex-A53 for I/O). Three chassis generations exist:
FAT (CFI-10/11/12, 825 GB, 2020-2023), Slim (CFI-20/21, 848 GB/1 TB,
2023+), Pro (CFI-70/71, 2 TB, 2024+). Motherboard revisions span EDM-010
through EDM-BK21 for PS5 and VSM-010 for PS5 Pro. The AMD Zen 2
microarchitecture carries speculative execution vulnerabilities (EntrySign
CVE-2024-36347, ZenBleed CVE-2023-20593, Retbleed CVE-2022-29900, Inception
CVE-2023-20569) that are permanent hardware issues.

**Firmware/Boot Chain**: Five primary stages from power-on to kernel launch.
Stage 0: Boot ROM (mask ROM, immutable, executed by PSP) validates serial
flash connection, loads Secure Loader from offset 0x800, performs RSA-4096
signature verification using ROM Key 2, sets up secure key rings. Stage 1:
Secure Loader (SCE SBL/IPL) at NAND Group 0 offset 0x800 with magic
E4 DB 7C 02. Header contains RSA-4096 signature at 0x200, Security Revision
at 0x11C (0x00000001-0x0003FFFF), Revision Nonce at 0x120 (SHA-256, nonces
0xA0-0x100 documented), metadata/keyrings at 0x140. Body undergoes dual-
layer AES-128-CBC decryption (global key + revision nonce key). Stage 2:
EMC firmware at serial flash offset 0x4000 in SLB2 segment format,
extractable with blsunpack. EMC versions span v0.7.6 (SDK 0.85.070
prototype) through v1.14.3 (FW 9.20 retail). Stage 2.5 (FW >=3.00):
Hypervisor Loader HyLonome adds an extra verification boundary. Stage 3:
Hypervisor initializes virtualization structures and IOMMU. Stage 4:
Kernel SELF encrypted with AES-128-CBC using EAP KBL keys, RSA-3072 signed.
The Communication Processor maintains the EMC/EAP/KBL key chain with
HMAC-SHA1. The CP Box (CPBH-100) provides TestKit debug authentication
via USB-C.

**Hypervisor**: Custom proprietary hypervisor (not Xen, KVM, or Hyper-V)
using AMD SVM extensions. Single-guest partition model — the entire GameOS
runs as one VM. Architecture split at FW 3.00: pre-3.00 hypervisor embedded
in kernel binary, post-3.00 standalone with HyLonome boot stage. SVM
features used include Nested Page Tables, Guest Mode Execute Trap, control
register filtering (CR0/CR4/EFER), MSRPM, and SMMU IOMMU. The xotext
feature (bit 58 in NPT PTEs) is a custom extension co-developed with AMD.
The hypercall interface has 17 calls (0x00-0x10 on FW >=3.00): message (2),
self-loading (2), CPUID (2), IOMMU (7), error (1), VMClosure (1,
FW >=3.00), MP boot (2, FW >=3.00). Known exploits: TMR heap OOB
(TheFloW, FW <=6.02), Byepervisor vtable/debug flag (FW <=2.70), Prosperous
TMR protection edit (fail0verflow/flatz 2026, FW <=4.51). No public
exploits for FW >=7.00.

**Kernel**: Heavily modified FreeBSD 11.0 derivative (1100122). Three
sysvec structures for PS4 SELF, FreeBSD ELF64, and Native SELF. Syscall
table: 500+ entries across 5 ranges (0x00-0x5F BSD, 0x60-0x8F networking,
0x90-0xFF POSIX, 0x100-0x17F modern BSD, 0x180+ PS4/PS5 specific). 100+
IOCTL device entries under /dev/. SceSbl dispatches 20+ secure modules
(0x8002xxxx) for authmgr, kms, pup, pfs, driveauth, pltauth, npdrm,
devact, otpaccess, manu, fttrm, srtc, and others. Memory protections: NX,
SMAP/SMEP, UMIP, KASLR, XOM (usermode and kernel). Kernel XOM is
hypervisor-backed via NPT. Known exploits: kqueueex (FW <=12.70), netcontrol
(FW <=12.00), fsc2h_ctrl (FW <=10.40), aio_multi_delete (FW <=10.01),
umtx_shm CVE-2024-43102 (FW <=7.61), IPV6_2292PKTOPTIONS (FW 3.00-4.51),
GPU DMA copy (FW >=6.00), exFAT overflow, SMAP bypass.

**Userland**: Three major exploit families. BD-J: BD-JB (FW <=4.51, 5 bugs),
BD-JB2 (FW <=7.61, path traversal), BD-JB-EX (FW <=12.70). Browser-engine
apps: YouTube Y2JB (FW 2.00-13.40, V8 CVE-2021-38003, unpatched), Netflix
(FW 4.03-12.40, V8/SpiderMonkey CVEs, patched FW 12.60). mast1c0re: PS2
emulator JIT exploitation via crafted save data in Lua/Ren'Py/YARPE
engines. WebKit: loadInSameDocument UaF CVE-2022-22620 (FW <=5.50),
CSSFontFaceSet (FW 3.00-4.51). Mitigations include WebKit sandboxing,
nullfs namespace isolation, Auth IDs/PAIDs capability model, disabled JIT
(standard contexts), and SELF binary signing.

**Security Model**: Multi-layered authentication framework. Auth IDs (64-bit
prefixes: 41=kernel, 48=system process, 49=system library) and PAIDs
determine privilege. Known Auth IDs: 4100000000000001 (Secure Kernel),
4100000000000002 (Kernel), 4800000000000024 (ScePlayReady),
4800000010000005 (bdj.elf). Code distributed as SELF binaries with
SceSbl signature verification. PSP manages secure key rings (Keys 2-9,
256-byte keyseeds), OTP access, and cryptographic operations. Key hierarchy
includes ROM keys (RSA-4096 for boot), Secure Loader keys (dual-layer
AES-CBC), EMC/EAP/KBL keys (AES-128-CBC, RSA-3072, HMAC-SHA1), content/
service keys (PKG metadata RSA-3072 fully leaked, trophy keys shared with
PS4, passcode 512-byte, portability EncDec master keys, M.2 dummy keys).
XOM at usermode (kernel-controlled, bypassable with kernel access) and
kernel (hypervisor-backed via NPT, requiring hypervisor compromise).
Keystone provides measured boot with PCRs for attestation. CP Box provides
hardware TestKit debug authentication.

## Cross-Cutting Findings

- **PS4-PS5 key sharing creates cross-generation risk**: Trophy keys are
  identical between generations. Portability EncDec master keys (128-byte
  key, blob, IV, hash), kernel NID suffix, and passcode are shared. The
  PKG metadata RSA-3072 key is fully leaked with CRT parameters. Any PS4
  key compromise directly impacts PS5. This is a permanent systemic
  vulnerability from cross-generation compatibility.

- **PS2 emulator JIT as design-level gap**: The mast1c0re family exploits
  the PS2 emulator JIT to emit arbitrary x86 code from crafted save data.
  The JIT must be enabled for emulation performance but processes
  untrusted data through a code-generation pipeline. This bypasses all
  standard userland mitigations — the JIT output is executable code by
  design. No software mitigation can fully close this without disabling
  the PS2 emulator.

- **GPU DMA as software protection bypass**: The GPU DMA engine provides a
  hardware memory access path outside the CPU's protection model. The GPU
  DMA copy exploit (FW >=6.00) reads and writes kernel .data pages through
  crafted GPU command buffers, bypassing CPU-level write protection. The
  hypervisor-managed IOMMU is the only effective mitigation.

- **Firmware version architecture split**: FW <=2.70 (hypervisor in kernel)
  versus FW >=3.00 (standalone hypervisor + HyLonome) creates two distinct
  research targets. Byepervisor only affects <=2.70. VMClosure and MP boot
  hypercalls (0x0E-0x10) only exist on >=3.00. Pre-3.00 exploits may not
  apply to modern firmware and vice versa.

- **Southbridge as underexplored attack surface**: EMC/EAP/EFC co-processors
  and the Communication Processor key chain are the least documented
  security layer. EMC firmware spans v0.7.6 through v1.14.3. The EMC
  manages power-on initialization, thermal monitoring, and system reset
  handling. Southbridge compromise would bypass the main x86 security
  model with potential cross-power-cycle persistence.

- **Userland entry point abundance**: Y2JB (unpatched FW 13.40), BD-JB-EX
  (FW <=12.70), Netflix (FW 4.03-12.40), mast1c0re (all FW with PS2
  emulation), WebKit (early FW). Multiple independent paths mean userland
  access is reliably achievable on most firmware versions.

- **Kernel exploit cadence**: kqueueex (<=12.70), netcontrol (<=12.00),
  fsc2h_ctrl (<=10.40), aio_multi_delete (<=10.01), umtx_shm (<=7.61),
  IPV6 (3.00-4.51). Roughly one exploitable kernel bug per major firmware
  cycle. Dominant class: use-after-free in FreeBSD-derived code.

## High-Value Targets

- **Boot ROM vulnerability**: Permanent, unpatcheable. Breaks the entire
  chain of trust from the root. Highest value, lowest probability.

- **PSP firmware exploit**: ARM firmware with cryptographic, key management,
  and OTP access surfaces. Grant access to all keys and OTP fuses, bypassing
  all higher-layer security. Extremely rare but highest impact.

- **Hypervisor bug on FW >=7.00**: No public hypervisor escapes for modern
  firmware. Would provide full system compromise. Best research areas: TMR
  management, hypercall parameter validation, VM exit edge cases, race
  conditions in concurrent event processing.

- **Southbridge firmware vulnerability**: EMC/EAP firmware under-explored.
  Controls power, thermal, error handling, and peripherals. Could persist
  across power cycles and OS reinstalls for firmware-level rootkit.

- **Kernel exploit for current firmware**: Steady supply of UaF and double-
  free bugs in FreeBSD-derived code (kqueue, socket, IPC).

- **Speculative execution key extraction**: ZenBleed can leak SIMD/FP
  register contents. If PSP crypto uses SIMD registers, key material
  could leak. Unproven for PS5 but critical theoretical attack.

## Research Gaps

- **PSP firmware internals**: No public disassembly, decompilation, or
  extraction methodology for PSP firmware. ARM code, memory layout, secure
  boot region management, and key ring implementation are undocumented.

- **Southbridge firmware analysis**: EMC/EAP/EFC firmware internals,
  Communication Processor key chain, C0080001 file structure, SLB2 segment
  format, and IPC protocol with PSP are not publicly documented.

- **Hypervisor codebase for FW >=7.00**: NPT layout strategies, xotext
  implementation, hypercall handler code paths, VM exit handling for
  non-standard events, VMClosure mechanics not documented for recent
  firmware revisions.

- **GPU DMA exploitation details**: GPU command buffer structures, DMA
  engine programming model through GnmDriver, IOMMU configuration that
  should prevent the attack, and exact bypass mechanism are not public.

- **mast1c0re technical details**: PS2 emulator JIT pipeline, Lua/Ren'Py/
  YARPE data structures triggering JIT code emission, JIT output buffer
  protection, constraints on generated x86 code not publicly documented.

- **Secure module intercommunication**: Module-to-module protocol, shared
  memory interfaces, privilege boundaries, and authmgr dispatch mechanism
  not publicly analyzed. Cross-module call paths could reveal escalation.

- **CP Box protocol**: USB-C communication protocol with TestKit, Assist
  Mode activation mechanism, debugging capabilities, command set, and
  firmware update mechanism not documented at protocol level.

- **SEV interaction with custom hypervisor**: Whether AMD SEV/SEV-ES
  features are used alongside the custom hypervisor has not been
  investigated. If present, SEV could provide additional protections.

- **Manufacturing mode reachability**: Conditions for manufacturing IOCTLs
  (set manu mode 0xC0184D03, load module 0x40184D01, unload module
  0x40184D02) are not documented. If reachable, could bypass signed module
  requirements.

- **PS Portal attack surface**: Custom Android 13 with fastboot and recovery
  modes. Boot chain firmware format (magic "DWCP"), update protocol (JSON
  at dwc.dl.playstation.net), and Android security model differences from
  main PS5 are not documented.

## Recommended Next Steps

1. **Analyze southbridge firmware internals**: Extract EMC firmware from
   PUP files using blsunpack. Disassemble to understand power-on init,
   PSP communication protocol, system management functions, and attack
   surface. Map Communication Processor key chain and HMAC-SHA1 paths.

2. **Catalog hypercall handlers cross-version**: Compare hypercall
   implementations across FW 2.00, 3.00, 5.00, 7.00, 9.00, 11.00, 13.00.
   Identify changed validation logic, removed checks, and newly added
   code paths. Focus on IOMMU hypercalls (0x06-0x0C).

3. **Reverse engineer PSP firmware**: Obtain PSP firmware from NAND dumps.
   Identify ARM executable format. Disassemble to understand key ring
   management, secure module loading, OTP programming, and boot ROM
   interaction. Compare with documented PS4 SAMU firmware.

4. **Test Y2JB exploit chain**: Reproduce V8 CVE-2021-38003 TheHole leak
   across FW 10.00-13.40. Analyze V8 heap layout, WebView sandbox
   boundaries, sandbox escape to system services. Document API surface
   available from the YouTube V8 context.

5. **Document GPU DMA engine**: Reverse engineer GPU command buffer
   submission from libSceGnmDriver through kernel to GPU. Identify the
   IOMMU configuration that should prevent DMA to kernel .data. Understand
   why the GPU DMA copy exploit bypasses this protection.

6. **Map secure module boundaries**: For each of 20+ secure modules,
   catalog function identifiers, calling conventions, input validation,
   and cross-module call paths. Analyze authmgr dispatch for function-
   table injection or confusion attacks. Identify shared memory interfaces.

7. **Investigate PS2 emulator JIT pipeline**: Disassemble PS2 emulator.
   Identify JIT compilation paths triggered by different savedata formats.
   Determine if JIT output region is XOM-protected or writable. Map full
   save-data-to-JIT-code pipeline and identify constraints on generated
   x86 code.

8. **Benchmark XOM bypass techniques**: Test PTE clearing, NPT manipulation,
   speculative execution gadgets on available firmware. Verify kernel XOM
   cannot be disabled via kernel-level page table modifications. Document
   TLB flush patterns needed for usermode XOM bypass.

## Relationships

- [[hardware_architecture]] — all findings constrained by AMD Zen 2 SoC
  (Oberon/Viola), southbridge (Salina), serial flash (W25Q16JVNIM), and
  peripheral hardware
- [[kernel_architecture]] — kernel syscall table, IOCTL devices, SceSbl
  dispatch are the primary escalation path from userland; kernel XOM
  backed by hypervisor NPT is the critical kernel protection
- [[hypervisor_architecture]] — hypervisor provides highest software-layer
  isolation through NPT, xotext, GMET, CR filtering, IOMMU; hypervisor
  exploits are the ultimate goal for full system compromise
- [[security_model]] — multi-layer authentication (Auth IDs, PAIDs, SELF
  signatures, secure modules) governs all code execution; privilege
  hierarchy is PSP > hypervisor > kernel > userland
- [[system_architecture]] — complete system integrates all layers through
  boot chain, hypervisor mediation, kernel management, and userland
  application execution

## References

- sources/web/psdevwiki/security/vulnerabilities.md
- research/hardware/hardware_overview.md
- research/kernel/kernel.md
- research/hypervisor/hypervisor.md
- research/security_model/security_model.md
- research/firmware/boot_chain.md
- research/firmware/secure_boot.md
