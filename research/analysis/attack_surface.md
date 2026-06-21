# PS5 Attack Surface Enumeration

## Overview

The PlayStation 5 presents a multi-layer attack surface spanning hardware,
firmware, hypervisor, kernel, userland, and peripherals. Each architectural
layer offers distinct entry points with varying exploitability and impact
to the overall system security. The platform's defense-in-depth design means
that compromising any single layer requires defeating every layer beneath it
in the privilege hierarchy. However, the vulnerability landscape documented
across all firmware versions reveals that userland entry points are the most
numerous and frequently exploited, kernel exploits follow at roughly one per
major firmware release cycle, and hypervisor exploits are the rarest with no
public examples for firmware versions 7.00 and above as of mid-2026.

The hardware attack surface includes the SPI serial flash bus (physical
dumping and reprogramming via Raspberry Pi GPIO), GDDR6 shared memory
(CPU/GPU isolation concerns due to the unified memory architecture), JTAG
and debug interfaces accessible through the southbridge, USB ports for media
injection and peripheral firmware communication, and wireless radios for
Wi-Fi 802.11ax and Bluetooth 5.1 communication. The firmware attack surface
centers on the Boot ROM (immutable mask ROM — any bug is permanent), the
Secure Loader IPL stored at serial flash offset 0x800 with dual-layer
AES-CBC encryption and RSA-4096 signing, the anti-rollback mechanism
combining Security Revision OTP fuses with Revision Nonce cryptographic
binding, and the PUP firmware update processing pipeline.

The kernel attack surface is the most extensively documented in public
research, with a 500+ entry syscall table organized into five ranges, an
IOCTL device interface covering over 100 kernel device entries under /dev/,
the SceSbl secure module dispatch subsystem with 20+ authenticated service
IDs, and filesystem parsers for PFS, exFAT, and UFS. Userland attack surface
includes the WebKit JavaScript engine, the BD-J Blu-ray Java environment,
game savedata parsing through the PS2 emulator JIT (mast1c0re and its
Lua/Ren'Py/YARPE variants), media format parsing, and network services in
the YouTube and Netflix apps which embed full V8 and SpiderMonkey engines.
Peripheral attack vectors include the DualSense controller HID command
interface, Bluetooth pairing protocols, USB DFU modes, and the PS Portal
Android fastboot and recovery modes.

## Hardware Attack Surface

- **Serial flash SPI bus**: The Winbond W25Q16JVNIM serial flash provides
  2 MB (16 Mbit) of storage on a standard SPI bus with accessible signal
  pins: /CS (chip select), /MISO (data output), /WP (write protect), GND,
  VCC (3.3V), /HOLD, SCLK (serial clock), and MOSI (data input). The
  device is packaged in a 150mil SOIC and is readable via a Raspberry Pi
  GPIO interface using the standard flashrom tool. The serial flash layout
  places the Secure Loader IPL header at offset 0x800 with magic E4 DB 7C
  02 and the EMC firmware at offset 0x4000 in SLB2 segment format. Physical
  access allows observation of boot data during the power-on sequence, but
  cryptographic signatures (RSA-4096 for the IPL header) prevent tampering
  without key material. The SPI bus signals are motherboard-accessible and
  can be probed with logic analyzers.

- **GDDR6 shared memory**: The PS5 uses 16 GB of GDDR6 memory (eight Micron
  MT61K512M32KPA-14C:B modules) across a 256-bit bus organized as four
  channels (E0, E1, D0, D1) providing 448 GB/s bandwidth. The unified
  memory pool is shared between CPU and GPU, meaning both processing
  elements access the same physical memory. This creates potential
  isolation concerns — the GPU DMA engine can read and write memory regions
  that the CPU considers privileged. The GPU DMA copy kernel exploit
  (FW >=6.00) demonstrated this by using crafted GPU command buffers to
  bypass kernel .data write protection. Southbridge error codes reference
  GDDR6 data line errors (0x80830000) and APU freeze conditions related to
  GDDR6 issues (0x80C00140).

- **JTAG and debug interfaces**: The CXD90061GG southbridge (Salina, based
  on MediaTek MT3613CT) provides UART debug signals accessible on the
  motherboard. Full JTAG-style debug access is available on DevKit and
  TestKit hardware through the CP Box (model CPBH-100), a USB-C connected
  debug accessory. The CP Box provides Engineering Mode (USB-C to PS5
  only) and Normal Mode (USB-C plus Ethernet DEV LAN to host). Without a
  CP Box, TestKits boot in Release Mode. The CP Box is not hot-pluggable
  and must be connected before power-on. It can read PS5 information
  (serial number, operating mode) even while the PS5 is shut down.

- **USB attack vectors**: 3x USB 3.1 Type-A ports and 1x USB-C front port.
  The USB attack surface includes media injection via exFAT/FAT32 (the
  exFAT overflow kernel exploit demonstrates filesystem parser
  vulnerability), savedata modification for games, DualSense controller
  firmware DFU modes (PBL, SBL, Main Mode) accessible through USB, and
  HID command injection targeting the controller main MCU. Dangerous HID
  commands include NVS lock/unlock and device info erase (ReportID=128,
  ActionID=13). USB extended storage format matches PS4 format.

- **Wireless (Wi-Fi/Bluetooth) attack surface**: The Sony AK8M19DFR1 module
  provides Wi-Fi 802.11ax and Bluetooth 5.1 (2.402-2.48 GHz, 2.5 mW). The
  DualSense controller communicates via Bluetooth with cryptographic
  pairing. Error code 0x80C00136 signals Wi-Fi or BT problems. The PS
  Portal remote player uses custom Android 13 with PS Link protocol over
  Wi-Fi, exposing fastboot (minus+USB at boot) and recovery modes (two
  HID devices: PS Controller and PS Link Audio). The PS VR2 headset uses
  CUP! format firmware updates with 7 file entries.

## Firmware Attack Surface

- **Boot ROM (immutable)**: On-die mask ROM within the AMD PSP (Ariel).
  Cannot be modified or patched after manufacturing — any vulnerability is
  permanent. Executes at power-on, initializes the PSP core, validates the
  Secure Loader via RSA-4096 signature check against ROM Key 2, and sets
  up secure key rings. The Boot ROM validates the magic value E4 DB 7C 02
  at serial flash offset 0x800 and halts if incorrect. Theoretical attack
  surface includes mask ROM implementation bugs, side-channel leakage
  during RSA-4096 verification, speculative execution (ZenBleed,
  Inception, Retbleed, EntrySign), and OTP fuse manipulation.

- **Secure Loader (serial flash)**: The IPL is the first mutable firmware
  component. Header structure (0x400 bytes at NAND Group 0 offset 0x800)
  contains magic (E4 DB 7C 02), header size (0x400), entry point (0xB0),
  body size (varies), SHA-256 digest, Security Revision at 0x11C, Revision
  Nonce at 0x120, metadata at 0x140, and RSA-4096 signature at 0x200. The
  body undergoes dual-layer AES-128-CBC encryption — Layer 1 with a global
  firmware key, Layer 2 with a revision nonce-derived key. Physical access
  allows dumping but not modification without breaking the signature. The
  dual-layer encryption prevents booting modified firmware without all key
  material.

- **Anti-rollback bypass**: Enforced through two complementary systems.
  The Security Revision field (offset 0x11C, 4 bytes) provides coarse-
  grained version checking against OTP fuses. Values escalate
  monotonically: 0x00000001 (FW 0.85-1.XX) through 0x0003FFFF (FW 11.00+).
  The Revision Nonce (offset 0x120, 32 bytes SHA-256) provides fine-grained
  per-revision cryptographic binding. Seven revision nonces are documented
  for revisions 0xA0 through 0x100. The nonce is used in Layer 2 AES-CBC
  key derivation — even with global firmware keys, an attacker cannot
  decrypt a firmware version without its specific nonce. Bypass would
  require OTP fuse manipulation or cryptanalysis.

- **Firmware update mechanism**: PUP update processing involves kernel
  IOCTLs: DecryptPupHeader (0xC0184402), DecryptPupSegment (0xC0184405),
  VerifyPupAdditionalSign (0xC0184403), VerifyPupWatermark (0xC0184404),
  DecryptPupSegmentBlock (0xC0284406), ReadNandGroup (0xC018440A),
  WriteNandGroup (0xC018440B), and UpdateSnvs (0x20004407). The secure
  module pup (0x80021002) handles update verification via
  sceSblPupExpirationGetStatus. Each decryption and verification step is a
  parsing attack surface. Manufacturing IOCTLs (set manu mode 0xC0184D03,
  load module 0x40184D01, unload module 0x40184D02) could bypass signed
  module requirements if reachable from userland.

## Hypervisor Attack Surface

The PS5 uses a custom proprietary hypervisor (not Xen, KVM, or Hyper-V)
built on AMD SVM extensions. On FW <=2.70 the hypervisor was embedded in
the kernel binary; on FW >=3.00 it is a standalone component with the
Hypervisor Loader (HyLonome) as an additional boot stage.

- **Hypercall interface**: 17 hypercalls (0x00-0x10 on FW >=3.00) exposed
  via the vmmcall instruction. Message interface (0x00 GET_MESSAGE_CONF,
  0x01 GET_MESSAGE_COUNT) for asynchronous communication. Self-loading
  (0x02 START_LOADING_SELF, 0x03 FINISH_LOADING_SELF) for boot-time
  initialization. CPUID virtualization (0x04 SET_CPUID_PS4, 0x05
  SET_CPUID_PPR) for compatibility mode. IOMMU management (0x06-0x0C)
  covers guest buffers, device enablement, PASID bind/unbind, command
  completion, event logs, and device table reads. Error handling (0x0D)
  for TMR violations. VMClosure (0x0E, FW >=3.00) for guest isolation. MP
  boot (0x0F STARTUP_MP, 0x10 DISABLE_STARTUP_MP, FW >=3.00). Each
  hypercall must validate all parameters — malformed IOMMU descriptors or
  invalid PASIDs could trigger hypervisor memory corruption.

- **VM exit handling**: VM exits occur on CPUID, RDPRU (intercepted with
  #GP injection), CR0/CR4/EFER writes, MSR accesses matching MSRPM, NPT
  violations, IOMMU operations, HLT/INVD/INVLPG, and hypercalls. The
  hypervisor saves guest state to VMCB, reads the VMEXIT code, processes
  the event (emulation, filtering, or forwarding), and re-enters via vmrun.
  Race conditions, interrupts, NMIs, and SMIs arriving during exit
  processing could corrupt hypervisor state.

- **IOMMU configuration**: 7 of 17 hypercalls are IOMMU-related, making
  this the largest and most complex hypercall category. The hypervisor
  exclusively manages the SMMU, controlling which memory regions DMA
  devices can access. Guest buffer registration must validate addresses
  and sizes. PASID bind/unbind manage device-private address spaces. ATS
  and PASID features introduce additional complexity — a compromised device
  could attempt to bypass IOMMU checks through ATS manipulation. Race
  conditions in IOMMU command queues could allow temporary access
  violations.

- **TMR management**: Trusted Memory Regions provide encrypted memory
  compartments. SceSbl interface exposes sceSblTmrMap, sceSblTmrUnmap,
  sceSblTmrEncAmmPt, sceSblTmrDecAmmPt, sceSblTmrExport. TMR heap OOB
  (TheFloW, FW <=6.02) demonstrated crafted TMR operations corrupting
  hypervisor heap. Prosperous (fail0verflow/flatz 2026, FW <=4.51) edited
  TMR protection state for arbitrary hypervisor read/write. Byepervisor
  (FW <=2.70) included vtable in data segment and debug flag retention.

## Kernel Attack Surface

- **Syscall table**: 500+ syscalls across five ranges: 0x00-0x5F standard
  BSD (exit, read, write, open, close), 0x60-0x8F extended BSD and
  networking (socket, connect, bind, listen, ioctl at 0x36), 0x90-0xFF
  POSIX extensions (kqueue, signals, scheduling), 0x100-0x17F modern BSD
  (aio, kld, mac, sched), 0x180+ PS4/PS5 specific. Three sysvec
  structures handle PS4 SELF, FreeBSD ELF64, and Native SELF. Known
  exploitable syscalls include kqueue (kqueueex ucred ref leak UaF
  FW <=12.70), socket (netcontrol double fdrop FW <=12.00), async I/O
  (aio_multi_delete double free FW <=10.01), IPC shared memory (umtx_shm
  UaF CVE-2024-43102 FW <=7.61), IPv6 options (CVE-2020-7457 FW 3.00-
  4.51). PS5-specific syscalls beyond 0x180 are undocumented and most
  likely for undiscovered exploits.

- **IOCTL device interface**: Over 100 kernel device entries under /dev/
  including /dev/bar, /dev/duid, /dev/dldbg, /dev/fttrm, /dev/icc_floyd,
  /dev/manuauth, /dev/nsfsctl, /dev/pfsctldev, /dev/pfsmgr,
  /dev/pup_update0, /dev/rootparam, /dev/sflash0, /dev/wlanbt. IOCTL
  codes encode direction, size, and command. Notable IOCTLs include
  TEE_IOC_DLM_START_TA_DEBUG (0xC028B409), TEE_IOC_DLM_FETCH_DEBUG_STRING
  (0xC110B40A), fftrm read/write sector (0xC0185301-0xC0185304), and
  driveauth AACS/CPRM key retrieval (0xC0205365-0xC0205364). The fsc2h_ctrl
  kernel stack free (FW <=10.40) demonstrates IOCTL-triggered memory
  corruption.

- **Driver attack surface**: GPU driver via libSceGnmDriver for command
  buffer submission. GPU DMA copy (FW >=6.00) bypasses kernel .data write
  protection through the GPU DMA engine. FTT RM driver (/dev/fttrm)
  manages film and TV DRM. PFS manager (/dev/pfsmgr) handles ICV table
  updates. Serial flash driver (/dev/sflash0) provides direct SPI access.
  TPM/Floyd driver (/dev/icc_floyd) communicates with the trusted platform
  module. Each driver IOCTL handler is a potential escalation vector.

- **SceSbl secure module dispatch**: Authentication manager (0x80021000)
  dispatches 20+ secure modules. Key functions include
  sceSblAuthMgrAuthHeader (SELF verification), sceSblAuthMgrLoadBlock
  (segment loading), sceSblAuthMgrSmLoad (secure monitor). KMS (0x80021001)
  handles key slots via sceSblKmsAllocKmbSlotForPprPkg and
  sceSblKmsSetKeyId. Manufacturing module (0x8002100B) provides
  sceSblManuAuthSetManuMode and sceSblManuAuthLoadSecureModule — if
  reachable these bypass signed module requirements.

- **File system parsing**: PFS with ICV integrity tables, exFAT for USB
  media (exploitable overflow), UFS base. PFS namespace sandboxing via
  /dev/nsfsctl and /dev/pfsctldev. External HDD verification via service
  ID 0x8002100F (sceSblExternalHDDVerifyMetadata).

## Userland Attack Surface

- **WebKit JavaScript engine**: System WebKit embedded in UI and app
  WebViews. Known exploits include loadInSameDocument UaF (CVE-2022-22620
  FW <=5.50) and CSSFontFaceSet (FW 3.00-4.51). The full web browser was
  removed after early firmware but WebKit remains in settings, store, and
  system dialogs.

- **BD-J (Blu-ray Java)**: BD-JB (FW <=4.51, 5 bugs by TheFloW), BD-JB2
  (FW <=7.61, path traversal patched FW 8.00), BD-JB-EX (FW <=12.70).
  Requires physical BD-R disc or jailbroken PS4 for authoring. The BD-J
  environment provides Java execution context with system API access.

- **Game savedata parsing (mast1c0re)**: Targets the PS2 emulator JIT
  compiler via crafted save data through Lua, Ren'Py, or YARPE game
  engines. Triggers JIT to emit native x86 code, providing usermode code
  execution without kernel bugs. The JIT is designed for emulation
  performance but creates a native code execution path from untrusted
  data — a fundamental design gap that cannot be fully mitigated without
  disabling the PS2 emulator.

- **Media format parsing**: Video (H.264 MKV/MP4 up to 4K, VP9 WEBM up to
  4K) and audio (FLAC, MP3, AAC) parsing triggered by USB media insertion.
  The exFAT overflow demonstrates filesystem parser exploitation path.
  Container format parsers provide additional codec-level attack surface.

- **Network services (YouTube/Netflix)**: YouTube Y2JB uses V8 CVE-2021-
  38003 JSON.stringify TheHole leak, unpatched as of FW 13.40 (FW 2.00-
  13.40). Netflix exploited V8/SpiderMonkey CVEs (FW 4.03-12.40, patched
  FW 12.60). These apps embed full JavaScript engines outside the WebKit
  sandbox, providing distinct userland entry paths.

## Entry Point Ranking

| Rank | Entry Point | Layer | Exploitability | Impact |
|------|-------------|-------|----------------|--------|
| 1 | YouTube V8 (Y2JB) | Userland | High | Low-Med |
| 2 | WebKit UaF | Userland | High | Low |
| 3 | BD-J exploits | Userland | Medium | Low-Med |
| 4 | mast1c0re (PS2 JIT) | Userland | Medium | Low |
| 5 | Kernel UaF/double-free | Kernel | Medium | High |
| 6 | Kernel IOCTL | Kernel | Medium | High |
| 7 | GPU DMA | Kernel | Medium | High |
| 8 | Hypercall interface | Hypervisor | Very Low | Critical |
| 9 | TMR management | Hypervisor | Low | Critical |
| 10 | Speculative execution | Hardware | Low | Critical |

Y2JB ranks highest due to broadest firmware coverage (FW 2.00-13.40,
unpatched). Kernel exploits provide the best risk-reward ratio with steady
discovery cadence. Hypervisor exploits are the rarest but most impactful.

## Relationships

- [[hardware_architecture]] — all attack surface depends on AMD Zen 2 SoC,
  southbridge, serial flash, and peripheral hardware
- [[kernel_architecture]] — syscall table, IOCTL devices, and SceSbl
  dispatch are the primary escalation targets from userland
- [[hypervisor_architecture]] — hypercall interface and NPT management are
  the highest-value but lowest-exposure attack surfaces
- [[boot_chain]] — firmware attack surface spans serial flash, Secure
  Loader IPL, EMC firmware, and anti-rollback mechanisms
- [[security_model]] — privilege hierarchy governs attack surface:
  PSP > hypervisor > kernel > userland

## Security Considerations

The attack surface evolves with each firmware update — new features
introduce new code paths while patches close old ones. Most effective
exploit chains combine userland access (WebKit, BD-J, or Y2JB) with a
kernel privilege escalation bug (kqueueex, netcontrol) and attempt
hypervisor escape. The GPU DMA exploit demonstrates that hardware
co-processors with independent memory access can subvert software write
protections. The PS2 emulator JIT creates a unique native code execution
path bypassing standard userland mitigations by design. Southbridge
firmware attack surfaces (EMC, EAP) are the least documented and may
provide alternative paths that bypass the main x86 security model.

## References

- sources/web/psdevwiki/security/vulnerabilities.md
- research/hardware/hardware_overview.md
- research/kernel/kernel.md
- research/hypervisor/hypervisor.md
- research/security_model/security_model.md
- research/firmware/boot_chain.md
- research/firmware/secure_boot.md
