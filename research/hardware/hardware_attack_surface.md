# PS5 Hardware Attack Surface

## Overview

The PlayStation 5's hardware attack surface spans multiple physical and logical domains that collectively define the lower bounds of the platform's security posture. While software-level exploitation (WebKit, kernel, hypervisor) has been the dominant vector for consumer jailbreaking, hardware attacks offer fundamentally different properties: they can bypass cryptographic protections at the root of trust, extract secret key material that no software bug could reveal, and achieve persistence that survives firmware reinstallation. The PS5's defense-in-depth architecture places the hardware root of trust at the AMD Platform Security Processor (PSP), but every layer above it — from the SPI serial flash to the GDDR6 shared memory to the PCIe bus topology — presents physical and side-channel attack surfaces that may be exploitable with sufficient access and equipment.

The hardware attack surface is especially relevant because the PS5 uses a semi-custom AMD Zen 2 APU (codenamed Oberon) which inherits all known microarchitectural vulnerabilities of the Zen 2 core: ZenBleed (CVE-2023-20593), Retbleed (CVE-2022-29900), Inception/SRSO (CVE-2023-20569), and EntrySign (CVE-2024-36347). These speculative execution vulnerabilities affect the PSP itself, which runs on the same Zen 2 die. Physical fault injection into the PSP's power supply — demonstrated in academic research as "One Glitch to Rule Them All" (Buhren et al., 2021) against AMD Secure Processor across Zen 1-3 — could bypass Secure Loader signature verification and execute arbitrary PSP firmware, compromising the entire security chain.

Beyond the SoC, the peripheral ecosystem (DualSense Bluetooth stack, PS VR2 USB-C connection, PS Portal Android fastboot, Blu-ray drive firmware, Wi-Fi module drivers) expands the physical attack surface to include USB-based firmware injection, Bluetooth keystroke injection, and media-based code execution paths. The fragmented firmware landscape across motherboard revisions (EDM-010 through EDM-BK21) means that hardware attack surface properties vary between console versions, with prototype and devkit units providing substantially more debug access than retail systems.

This document catalogs every known and theoretical hardware attack surface on the PS5, organized by physical access requirements, technical sophistication needed, and likelihood of practical exploitation. Each section distinguishes confirmed facts (from psdevwiki, academic research, and community reverse engineering) from speculative analysis.

## Physical Attack Surface

### SPI Serial Flash (W25Q16JVNIM)

The PS5 uses a Winbond W25Q16JVNIM serial flash memory (2 MB / 16 Mbit capacity) in a 150mil SOIC-8 package. This is the critical non-volatile storage for boot configuration and parameter data. It is connected via a standard SPI interface: /CS (chip select), /MISO (data output), /WP (write protect, active low), GND, VCC (3.3V), /HOLD (hold input, active low), SCLK (serial clock), and MOSI (data input). The SPI bus is driven by the CXD90061GG southbridge/EMC (Salina, based on MediaTek MT3613CT), which has dedicated SPI controller functionality alongside I2C, UART, GPIO, and PWM.

**Dumping Methods:** The SPI flash is readable via a Raspberry Pi GPIO interface using the standard `flashrom` tool. The 150mil SOIC-8 package is surface-mount but accessible on the motherboard for clip-on probing (e.g., Pomona SOIC-8 clip) or in-circuit reading. Chip-off dumping requires hot air rework capability but is feasible with moderate equipment.

**Serial Flash Layout:**
- Offset 0x800: Secure Loader IPL header with magic `E4 DB 7C 02`, RSA-4096 signature at offset 0x200, SHA-256 digest, Security Revision at 0x11C, Revision Nonce at 0x120
- Offset 0x4000: EMC firmware in SLB2 segment format
- Offset 0x1C7230: Model number string
- Offset 0x1C7250: Serial number / IDPS data (partial IDPS matching documented in serial database)

**Write Protection:** The /WP and /HOLD pins provide hardware-level protection. The W25Q16JVNIM supports status register write protection (SRP0, SRP1, TB, BP0-BP3) that locks sectors against software modification. On retail units, if WP# is tied to a protected state and status register locks are set, in-system modification is prevented. Chip-off dumping followed by modification and re-flashing bypasses this entirely.

**Potential Attacks:**
- Secure Loader modification (requires breaking RSA-4096 or extracting signing key)
- Boot configuration tampering (unprotected parameter regions)
- Anti-rollback bypass (defeated by OTP fuses + Revision Nonce cryptographic binding)
- Key extraction via side-channel during secure boot read operations
- EMC firmware replacement for persistence (if signature verification is bypassed)

The anti-rollback mechanism uses two complementary systems: the Security Revision field (offset 0x11C, 4 bytes) provides coarse monotonic version checking against OTP fuses (0x00000001 for FW 0.85-1.XX through 0x0003FFFF for FW 11.00+), while the Revision Nonce (offset 0x120, 32 bytes SHA-256) provides fine-grained per-revision cryptographic binding used in Layer 2 AES-CBC key derivation. Even with the global firmware key, an attacker cannot decrypt a firmware version without its specific nonce. Seven revision nonces are documented for revisions 0xA0 through 0x100.

**Error Indications:** Southbridge error codes 0x86000005 and 0x86000006 indicate "NOR Corrupt" — serial flash validation failures that halt secure boot.

### JTAG/SWD Debug Interfaces

**Motherboard Revisions:** Known PS5 motherboard revisions: EDM-010 (initial retail), EDM-020, EDM-030, EDM-040, EDM-041, EDM-044, EDM-AR10, EDM-AK30, EDM-BK21, and VSM-010 (PS5 Pro). Debug port accessibility likely varies across revisions.

On **retail units**, JTAG and full debug access is believed to be fused off at the SoC level. This mirrors the PS4 situation where JTAG was available on devkits but disabled on retail through e-fuse configuration. The PS4's JTAG was found accessible on early SDK units but locked on production hardware.

On **DevKit and TestKit hardware**, full JTAG-style debug is provided through the **CP Box** (model CPBH-100), a USB-C connected debug accessory. Two modes:
- Engineering Mode: USB-C to PS5 only
- Normal Mode: USB-C plus Ethernet DEV LAN to host
The CP Box is NOT hot-pluggable and must be connected before power-on. It can read PS5 information (serial number, operating mode) even while the PS5 is shut down. Without a CP Box, TestKits boot in Release Mode.

**Value if Accessible:** Full SoC register read/write, hardware breakpoints, memory dump without OS cooperation, instruction-level debugging of PSP/kernel/hypervisor, direct flash programming bypassing all software protections.

### UART

The CXD90061GG southbridge (Salina / MediaTek MT3613CT) provides UART debug signals accessible on the motherboard. The UART is part of the MediaTek peripheral set alongside SPI, I2C, GPIO, and PWM. Pin locations, voltage levels (likely 3.3V or 1.8V), and baud rate are not fully documented in public sources.

On **prototype units** (FW 0.85.070 and below), UART is confirmed active, emitting Secure Loader debug messages and kernel boot messages. On **retail units**, whether UART remains active is unclear — Sony may disable UART output via southbridge configuration, or leave it enabled but unpopulated. Historical PS4 precedent: UART was active on early retail units but disabled via firmware on later revisions.

If UART is active: boot sequence timing information aiding glitch attack development, kernel address space layout (defeating kASLR), filesystem/device enumeration details, panic/crash dumps.

### Motherboard Revisions

| Revision | Notes |
|----------|-------|
| EDM-010 | Initial retail revision (FW 1.00 factory) |
| EDM-020 | Component changes, possible power delivery revision |
| EDM-030 | Revised layout |
| EDM-040 | Further component changes |
| EDM-041 | Minor revision |
| EDM-044 | Latest documented non-variant Oberon board |
| EDM-AR10 | Additional variant |
| EDM-AK30 | Additional variant |
| EDM-BK21 | Additional variant |
| VSM-010 | PS5 Pro motherboard (Viola APU) |
| EPT-01 | PS VR2 headset motherboard (1-010-109-11) |
| BDM-010 | DualSense retail motherboard |
| BDM-010 R10 | DualSense eng. sample with MT3616ECT |

Changes affecting attack surface: removed/depopulated test points and debug headers on later revisions, VRM phase count and capacitor value changes that affect glitch timing, different serial flash chips or pin routing, southbridge firmware security updates, exploit compatibility varying by firmware ranges tied to production batches.

Factory firmware varies by chassis: CFI-10 (FW 1.00), CFI-11 (later), CFI-12 (up to FW 7.61). Slim CFI-20/21 (FW 7.00-13.20). Pro CFI-70/71 (FW 9.05-13.20).

### Prototype Units

PS5 prototype and dev hardware provides substantially different attack surface:

**DevKit Variants:**
- EVA3-3: DUTP-DSNxxxBK-Lx (earliest, ~FW 0.75)
- Prototype 0: DUTP-DSNxxxBK-Rx
- Prototype 1: DUTP-DSNxxxBK-Wx (e.g., DUTP-DSN18AAK-W5, min FW 0.85.070)
- Prototype 2: DSWxxxBK-xx

**TestKits:** EGR-TAxxxK-Gx, EGR-TAxxxK-Jx (Prototype 1 based)
**CP Boxes:** CPB-TAxxxK-Bx (FW ???), CPB-TAxxxK-Cx (min FW 0.9.0.5)

**Key Differences from Retail:**
- Unlocked debug features: CP Box JTAG access, DECI5 shared memory at MMIO 0x880000000-0x89FFFFFFF
- Active UART output with full boot debug messages
- Different Wi-Fi/BT chip: AW-XM501 (proto) vs Sony AK8M19DFR1 (retail)
- Different SysCon: Tirion on devkit proto vs integrated in Salina on retail
- No kASLR: prototype firmware (FW 0.85.070) reveals complete MMIO layout at base 0xFFFFF80000000000
- Different serial flash configuration potential

**MMIO Prototype Map** (FW 0.85.070 and below, no kASLR):

| Region | Address Range | Device | Codename |
|--------|--------------|--------|----------|
| nvme0 | 0xC4200000-0xC4203FFF, 0xC4000000-0xC40FFFFF | dev 0.0 pci1 | Titania |
| tpcie0 | 0xA0000000-0xBFFFFFFF, 0xC0000000-0xC3FFFFFF | dev 0.1 pci1 | Titania PCIe |
| spcie0 | 0x8500C000-0x8500CFFF, 0x85200000-0x853FFFFF, 0x85400000-0x8547FFFF | dev 0.5 pci1 | Salina PCIe |
| mtsc0 | 0x85000000-0x85000FFF | dev 0.2 pci1 | Salina GBE |
| ahci0 | 0x85004000-0x85007FFF | dev 0.3 pci1 | Salina SATA0 |
| ahci1 | 0x85008000-0x8500BFFF | dev 0.4 pci1 | Salina SATA1 |
| xhci0 | 0x85600000-0x857FFFFF | dev 0.6 pci1 | Salina USB |
| apcie0 | 0x81300000-0x813FFFFF, 0x81400000-0x81407FFF, 0x81600000-0x817FFFFF | dev 0.17 pci1 | Belize/Caliban PCIe |
| gc0 | 0xD0000000-0xDFFFFFFF, 0xE0000000-0xE01FFFFF, 0xE0600000-0xE067FFFF | dev 0.0 pci2 | Graphics Core |
| az0 | 0xE06C0000-0xE06C3FFF | dev 0.1 pci2 | GPU/Azalia Audio |
| sbl0 | 0xE0500000-0xE05FFFFF, 0xE06C6000-0xE06C7FFF | dev 0.2 pci2 | Ariel (PSP) |
| xhci1 | 0xE0200000-0xE02FFFFF | dev 0.4 pci2 | PPR USB |
| xhci2 | 0xE0300000-0xE03FFFFF | dev 0.5 pci2 | PPR USB |
| ajm0 | 0xE0680000-0xE06BFFFF | dev 0.6 pci2 | ACP (Audio Co-Processor) |
| mp40 | 0xE0400000-0xE04FFFFF, 0xE06C4000-0xE06C5FFF | dev 0.3 pci2 | MP4 |
| deci_shm_main0 | 0x880000000-0x89FFFFFFF | dev 0.19 pci1 | DECI5 (debug only) |
| bxe0 | 0x80000000-0x807FFFFF, 0x80800000-0x80FFFFFF, 0x81000000-0x8100FFFF | dev 0.10 pci1 | PCI BAR |

**Codename Reference:**
- **Titania** = NVMe controller (Shakespeare theme)
- **Salina** = Southbridge/EMC (Islands theme)
- **Belize/Caliban** = PCIe bridge (Shakespeare theme)
- **Ariel** = PSP / GPU partition (Shakespeare theme)
- **GC** = Graphics Core (GPU)
- **ACP** = Audio Co-Processor

### Power Analysis

**PSU Specifications:**
- Standard model: 350W internal PSU (ADP-400DR)
- Digital edition: 340W
- Multi-voltage: 110-240V
- Peak measured draw: ~207W (Spider-Man Miles Morales)

**APU Power Delivery:**
- Infineon XDPE14286A VRM controller, 8+2 phase PWM
- Manages VDDCR_GFX (GPU, 1.0V_SOC_VGFX) and VDDCR_CORE (CPU, 1.0V_SOC_VCORE) via SVI2 (SVC/SVD/SVT)
- Input voltages: 1.8V_SOC_VDDA, 3.3V_VRM, 1.2V_VRM, 12V_MAIN
- Key signals: PSW_MSOC_PGC (enable), SOC_PWROK, /SOC_VRM_HOT, /SOC_GPU_PCC
- Temperature sensing via TSEN1/TSEN2

**Voltage Glitching Feasibility:**

"One Glitch to Rule Them All" (Buhren et al., 2021, arXiv:2108.04575) demonstrated that voltage glitching against the AMD Secure Processor (AMD-SP) supply bypasses firmware signature verification on Zen 1, Zen 2, and Zen 3. The attack enabled custom SEV firmware deployment, full SEV VM memory decryption, and endorsement key extraction (CEK/VCEK) for forging attestation reports. This is directly applicable to PS5 because:

- The PSP uses the same Zen 2 core microarchitecture as the attacked AMD-SP
- Timing requirements: glitch injection during Secure Loader signature verification (after boot ROM validates initial header, during RSA-4096 check)
- The XDPE14286A VRM's SVI2 interface and power good/fail signals (/SOC_VRM_HOT, SOC_PWROK) provide timing reference points
- No countermeasure exists on current hardware — requires microarchitectural fix to AMD-SP (per the paper)

**Fault Injection Targets:**
- VDDCR_CORE (CPU/PSP core, 1.0V_SOC_VCORE) — affects both x86 cores and PSP
- VDDCR_GFX (GPU, 1.0V_SOC_VGFX) — less likely to affect PSP
- VCC 3.3V — affects southbridge and serial flash
- GDDR6 VMEM (1.35V_G6_VMEMIO) — memory content corruption
- 1.8V_SOC_VDDA — analog/PLL supply, sensitive to glitches
- 12V_MAIN — main PSU rail, requires higher-power injection

**EM Fault Injection (EMFI):** Also theoretically applicable — localized eddy currents induce timing faults in specific chip regions without direct electrical contact. Requires precision positioning (CNC XYZ table, high-voltage probe) but leaves no physical evidence.

**Glitch Timing Reference Points:**
- Southbridge error 0x80C00140 (APU Freeze — GDDR6 Data Line Issue) indicates the southbridge monitors APU responsiveness — this is a fault detection mechanism that must be bypassed
- Error 0x80800009 (Unexpected Power Cut / Shutdown Failure) indicates power glitch detection
- VRM power fail errors (0x80050000, 0x80060000) indicate VRM fault detection thresholds

### Chip-Off Attacks

Physical removal of the W25Q16JVNIM serial flash enables:
1. **Depopulation:** SOIC-8 is relatively easy with hot air (300-350°C). BGA chips (APU, GDDR6) require proper BGA rework stations with preheating.
2. **Reading:** Any standard SPI programmer (bus pirate, CH341A, TL866, or Raspberry Pi GPIO with flashrom).
3. **Modification:** Binary patches applied, then re-flashed.
4. **Replacement:** Modified flash re-soldered or socket installed for iterative experimentation.

**Limitations:** Boot ROM (on-die mask ROM within PSP) is immutable. RSA-4096 signatures prevent modified IPL execution without Sony signing key. OTP fuses cannot be reset — anti-rollback persists. Layer 2 AES-CBC encryption prevents decryption without all key material.

**Reports:** psdevwiki community has documented successful SPI flash dumping via Raspberry Pi. PS4 chip-off re-flashing demonstrated; PS5-specific reports are limited but technically feasible with identical equipment.

**Permanent Boot Compromise:** If the PSP's fuse key ring or Secure Loader signing key is ever extracted (via side channel, insider leak, or cryptographic break), chip-off serial flash modification could achieve permanent, undetectable boot compromise — the system would boot a modified Secure Loader disabling all downstream security checks.

### Side-Channel Attacks

**EM Emissions:** The Zen 2 APU (Oberon) during cryptographic operations emits EM radiation correlated with data-dependent transitions. Targets:
- PSP AES-CBC decryption (Layer 1 global key, Layer 2 revision nonce-derived key)
- RSA-4096 signature verification
- SHA-256 digest computation
- HDCP key handling via MN864739 HDMI retimer

**Power Trace Analysis:** The XDPE14286A VRM's current draw is measurable via shunt resistor or magnetic field probe on VRM output inductors. DPA against PSP could extract:
- Global firmware AES keys
- Per-console OTP fuse keys
- HDCP 2.3 keys
- Secure module signing keys

**Timing Analysis:** Cryptographic comparisons (RSA signature verification, MAC checks, nonce comparisons) that short-circuit on first mismatched byte create timing side-channels. If PSP uses non-constant-time comparison, timing measurement from x86 side could leak information.

**Limitations:** PSP operates independently from x86 cores — direct timing observation requires synchronization. EM measurement requires physical proximity. Power trace analysis requires invasive probing (shunt resistor) or near-field probe placement. Effectiveness depends on SNR and measurement count (thousands to millions typically required).

## Speculative Execution Attacks

### ZenBleed (CVE-2023-20593)

**Technical Analysis:** ZenBleed is a side-channel vulnerability in AMD Zen 2 where the floating-point division unit's internal microarchitecture leaks SIMD/FP register file contents (XMM/YMM) across process boundaries. The attack exploits a timing side-channel in the integer division unit (`DIV`/`IDIV` uop) that shares circuitry with the FP division unit — by measuring division timing, an attacker infers other processes' FP register contents.

**PS5 Relevance:**
- Critical for PSP ↔ OS boundary attacks: the PSP runs on the same Zen 2 die
- If PSP crypto code uses SIMD (XMM/YMM) registers for cryptographic operations, ZenBleed could leak key material across the PSP ↔ OS boundary
- Technical requirements: precise timing (high-resolution cycle counter), FP division instruction loop, 4K page alignment
- **Unproven on PS5** as of mid-2026 — no public demonstration

**Attack Scenario:** Kernel-level code execution on x86 cores uses ZenBleed to observe PSP register file contents while PSP performs crypto (AES, RSA, key derivation). If PSP uses YMM registers for any crypto operation, key material could be reconstructed from leaked timing side-channel.

**Mitigation Status:** AMD released microcode patches. PS5 custom firmware may or may not incorporate them. Microarchitectural — cannot be fully mitigated in software without disabling SMT or FP division optimization.

### Retbleed (CVE-2022-29900, CVE-2022-29901)

**Technical Analysis:** Spectre-variant specific to AMD Zen 1-3 exploiting return instruction branch prediction. AMD's return predictors share hardware with indirect branch predictors, making Intel-style retpolines ineffective. The attack poisons return address prediction to redirect speculative execution to attacker-controlled gadgets.

**PS5 Relevance:**
- All PS5 units use Zen 2, natively affected
- If the PS5 hypervisor uses return instructions (almost certainly) rather than dedicated return-thunk sequences, hypercall handling could be attacked
- **Practical implications for hypervisor isolation:** Kernel execution could use Retbleed to speculatively access hypervisor memory, extracting secrets (encryption keys, VM memory) or finding ROP gadgets for hypervisor code execution
- Requirements: knowledge of hypervisor memory layout, identifiable return gadgets, BTB/RSB training from kernel context

**Mitigation:** AMD recommends "return thunk" sequences converting returns to indirect jumps. PS5 custom firmware may include equivalent hypervisor mitigations.

### EntrySign (CVE-2023-31315, CVE-2024-21955, CVE-2024-36347)

Listed in vulnerabilities.md as a PS5-relevant Zen 2 hardware vulnerability.

**Analysis:** EntrySign affects AMD Zen platform signed-secure-entry mechanisms. On EPYC, affects SEV/SEV-ES guest entry validation — crafted malicious entries bypassing signature verification allow arbitrary code execution at hypervisor/SEV firmware privilege.

**PS5 Relevance:**
- PS5 runs a custom proprietary hypervisor (built on AMD SVM, not SEV)
- Hypervisor uses validated entry points via hypercalls (0x00-0x10 on FW >=3.00), VMClosure for guest isolation, and SceSbl secure module dispatch
- If hypervisor entry validation has flaws analogous to EntrySign (incomplete state validation, race conditions, buffer overflows in parameter parsing), VM escape from game OS to hypervisor could be possible
- Prosperous exploit (fail0verflow/flatz 2026, FW <=4.51) demonstrated TMR protection state editing for arbitrary hypervisor read/write — related privilege escalation vector
- TMR heap OOB (TheFloW, FW <=6.02) demonstrated crafted TMR operations corrupting hypervisor heap

### Inception / SRSO (CVE-2023-20569)

Listed as a Zen 2 hardware vulnerability applicable to PS5. Inception (Speculative Return Stack Overflow) overflows the Return Stack Buffer (RSB) to poison speculative execution. If unmitigated in PS5 microcode or hypervisor, provides another path for breaking game OS ↔ secure OS isolation.

### Spectre-v2 / Branch Target Injection

**Applicability:** Game code runs at near-native speed in the game OS VM. Hypervisor enforces isolation via Nested Page Tables (NPT) and IOMMU, intercepting CPUID, MSR accesses, CR0/CR4/EFER writes, and hypercalls via VM exits.

**Key Questions:**
- Does the hypervisor flush the Branch Predictor Buffer (BPB) on VM exits? If not, branch target injection from guest could affect hypervisor speculative execution.
- Does the custom NPT (non-standard page table structure) provide any Spectre mitigation? Two-level translation adds overhead but does not inherently prevent speculation-based side channels.
- Is the xotext (text execute-out-of-place) region accessible speculatively?

**Mitigation Assessment:** Standard Spectre v2 mitigations (IBRS, STIBP, IBPB) require CPU support and OS/hypervisor enablement. If PS5 firmware enables these, Spectre-v2 attacks are mitigated. However, performance impact (particularly on game OS ↔ system OS context switches) may have led Sony to disable them on this gaming-focused platform.

### Speculative Execution Attack Surface Summary

| Vulnerability | CVE | PS5 Relevance | Proof on PS5 | Mitigation Status |
|--------------|-----|---------------|-------------|-------------------|
| ZenBleed | 2023-20593 | PSP ↔ OS key leakage via FP division timing | None | Unknown if microcode patched |
| Retbleed | 2022-29900/29901 | Hypervisor isolation break via return prediction | None | Unknown if return-thunks used |
| EntrySign | 2024-36347 | Hypervisor VM escape via entry validation | Related: Prosperous (<=4.51) | Patched via hypervisor updates |
| Inception/SRSO | 2023-20569 | RSB overflow for isolation break | None | Unknown |
| Sinkclose | Zen all | SMM bypass (system management mode) | Not confirmed on PS5 | Unknown |
| Spectre-v2 | Various | BPB poisoning across VM boundaries | None | Unknown |

## Peripheral Attack Surface

### USB

**Port Configuration:** 3x USB 3.1 Type-A (back), 1x USB-C (front). USB 2.0 available internally via Salina southbridge USB 2.0 port 2.

**Host Controllers:**
- Salina (CXD90061GG) USB host at MMIO 0x85600000-0x857FFFFF (xhci0, dev 0.6 pci1)
- PPR (Ariel/PSP) USB hosts at MMIO 0xE0200000-0xE02FFFFF (xhci1, dev 0.4 pci2) and 0xE0300000-0xE03FFFFF (xhci2, dev 0.5 pci2)

**DMA Attack Surface:** USB controllers are PCI devices with DMA capability. The hypervisor manages the SMMU exclusively via hypercalls 0x06-0x0C. A malicious USB device could present crafted descriptors triggering USB stack parsing vulnerabilities, perform DMA attacks if IOMMU configuration is incomplete, or exploit hub controller via descriptor manipulation (BadUSB-class).

**USB Extended Storage:** Same format as PS4. The exFAT overflow kernel exploit demonstrates filesystem parser vulnerability via USB media. External HDD verification via SceSbl service ID 0x8002100F (sceSblExternalHDDVerifyMetadata).

**mast1c0re / PS2 Emulator JIT Path:** Crafted save files on USB trigger PS2 emulator JIT to emit native x86 code, providing usermode execution without kernel bugs. Variants: Lua, Ren'Py, YARPE. This is a fundamental design gap — the JIT is designed for emulation performance but creates a native code execution path from untrusted data.

### M.2 SSD

**Interface:** PCIe 4.0 x4 NVMe (Socket 3, Key M), form factors 2230-22110, 250 GB - 8 TB (4 TB before FW 8.00). Requires system software 4.00+, heatsink required.

**DMA Attack Surface:** Direct PCIe 4.0 x4 connection to APU. NVMe SSD has full DMA capability. Hypervisor IOMMU management via hypercalls:
- 0x06: Alloc/register guest buffer
- 0x07: Free guest buffer
- 0x08: Enable device
- 0x09: Bind PASID
- 0x0A: Unbind PASID
- 0x0B: Read IOMMU command completion
- 0x0C: Read IOMMU event log

If an NVMe SSD's controller firmware is compromised, it could DMA into protected memory regions. ATS (Address Translation Services) and PASID features could enable device-driven mapping manipulation to bypass IOMMU restrictions.

**Encryption Key Status:** The internal SSD controller (SIE CXD90062GG / Zao, based on Marvell 88SS1098) uses static dummy encryption keys across FW 1.00-12.20. This means encryption applied to internal SSD data is effectively cosmetic — anyone with physical access to the NAND chips can read data using known or guessable keys. The keys may be per-firmware-version (not per-console), making extraction from a single unit sufficient for all units on that firmware. As of FW 12.20+, the key status may have changed. This fundamentally undermines data-at-rest security.

**Cold Boot Attack:** GDDR6 (8x Micron MT61K512M32KPA-14C:B, 2 GB each) retains data briefly after power loss (seconds at room temperature, longer when cooled). The internal SSD's DDR4 cache chip is also vulnerable. Could recover encryption keys, game DRM secrets, or user credentials.

### Bluetooth 5.1

**Wireless Module:** Sony AK8M19DFR1 (M19DFR1), providing Wi-Fi 802.11ax and Bluetooth 5.1 (2.402-2.48 GHz, 2.5 mW). Prototype units used AW-XM501.

**DualSense Bluetooth Stack Attack Surface:**
- DualSense (codename: Bond) uses Bluetooth HID with cryptographic pairing
- HID commands accessible over Bluetooth: Read/Write Device Info, Get/Set BT Address (ReportID=128/129, DeviceID=9), NVS Lock/Unlock (ReportID=128, DeviceID=3, ActionID=1/2/3), DFU mode switching (ReportID=160)
- **NVS Unlock (ActionID=2) and Erase Device Info (ActionID=13, DANGER)** are accessible if attacker establishes HID connection
- Get MCU Unique ID (ReportID=128, DeviceID=1, ActionID=9) leaks device identity
- Set DFU Mode (ReportID=160, EnablePBLMode=1, EnableSBLMode=2) switches controller to firmware update mode

**Keystroke Injection:**
- If attacker can pair a malicious BT device or compromise DualSense firmware, keystroke injection becomes feasible
- DualSense firmware: Banana (main MCU on ARM Cortex M4, from MediaTek MT3616XXX), Venom (audio codec, Realtek ALC5524), Betty (unknown). All stored at `/system_ex/etc/`
- DFU modes: PBL (flash SBL only), SBL (flash main + audio + DSP), Main Mode (audio, DSP, BT patches)
- HID Device IDs: 1=Main MCU, 2=Power, 3=NVS, 5=Touch Panel, 6=Venom FW, 9=BT, 14=BT Patch, 15=Venom, 16=Spider DSP, 17=VDD External

**Attack Scenarios:** Malicious BT peripheral impersonating DualSense, firmware modification via USB DFU to insert keystroke injection payload, BT pairing protocol exploitation (~10m range).

### Wi-Fi 6 (802.11ax)

**Module:** Sony AK8M19DFR1. Underlying silicon likely from Broadcom, MediaTek, or Qualcomm.

**Driver Attack Surface:**
- Kernel Wi-Fi/BT driver: /dev/wlanbt
- Wi-Fi firmware: wlanbt_fw (hex codename C0030002)
- Error code 0x80C00136: Wi-Fi or BT problems
- Known CVEs in Broadcom/MediaTek Wi-Fi chipsets potentially relevant
- Wi-Fi firmware parsing vulnerabilities could provide RCE on chipset microcontroller

**Remote Attack Surface:** Wi-Fi is the only truly remote (non-proximity) hardware attack vector. Exploiting the Wi-Fi stack could provide initial code execution on the chipset, then attempt PCIe DMA or host driver exploitation. High-value target for zero-click remote jailbreak.

### Disc Drive

**Drive Model:** 502R Ultra HD Blu-ray drive
**Firmware:** BD 1072 (FW 1.00), BD 1073 (FW 1.05), BD 1119 (FW 3.00), BD 1137 (FW 4.03), BD 1275 (FW 8.60)

**BD-J Attack Path:** Blu-ray Disc Java environment triggered by disc insertion.
- BD-JB (TheFloW, FW <=4.51, 5 bugs)
- BD-JB2 (FW <=7.61, path traversal, patched FW 8.00)
- BD-JB-EX (FW <=12.70)
Requires physical BD-R disc or jailbroken PS4 for authoring.

**Drive Firmware Attack Surface:**
- MediaTek-based BD drive controller with reflashable firmware via Jigkick PKG's BD_EM_BOOT_FW (emergency brick recovery)
- BD_VEEPROM_DATA contains drive EEPROM — could be modified to bypass region checks or authentication
- Drive firmware vulnerabilities could enable code execution on MediaTek controller for disc-based kernel attacks

**Jigkick File Contents (Manufacturing/Recovery PKG):**
- BD_EM_BOOT_FW: Recovery MediaTek Blu-ray firmware (brick recovery)
- BD_MAIN_FW: Main firmware (30XR.bix equivalent)
- BD_VEEPROM_DATA: EEPROM data
- GAME_OS_DIAG_2ND: Diagnostic zip
- MANU_UPDATER: manufacturing_updater.self
- NET_LOAD_DIAG: Unknown (~7 MiB)

### PS VR2

**Hardware:**
- Codename: EPCOT (E in EPT-01)
- Motherboard: EPT-01 (1-010-109-11)
- Side A: SIE CXD90067GG, K4U6E3 4AAMGCL (DRAM), THGBMNG5 D1LBAIT (4GB eMMC), WM1801B, PCA9957 (24-channel SPI serial bus)
- Side B: SIE CXD90068GF, RTS5443H (Realtek Type-C controller/hub)
- Power Button Board: KEY-01 (1-010-112-11)

**Firmware Update Format (Magic "CUP!"):**
- 0x0000/4: Magic "CUP!"
- 0x0004/4: Unknown (0x02011003)
- 0x0008/8: Unknown (0x0000000000000001)
- 0x0010+: 7 file entries (file type, offset, size)
- File types: 0x10000000, 0x2000000B-0x2000000E, 0x2FFFFFFE, 0x2FFFFFFF
- File data at offset 0x300

**Attack Surface:**
- USB-C for power/data — potential USB hub attack via RTS5443H
- CUP! format parsing — malformed packages triggering buffer overflows
- HDCP involvement in video transmission
- Tracking camera input parsing vulnerabilities
- PCA9957 24-channel SPI bus — SPI-based attacks on VR2 peripheral bus
- 4GB eMMC (THGBMNG5 D1LBAIT) — chip-off or SPI access for firmware modification

### PS Portal

**Hardware/Software:**
- Custom Android 13
- Master Key (GCM): `35 15 A8 8F 33 55 7D F1 33 FB F2 08 D6 3B 0A AF`
- Update endpoint: JSON REST API at `dwc.dl.playstation.net`
- PUP structure: Magic "DWCP", Type=1, Full Size, Version
- Firmware versions 1.0.0 through 6.0.1+

**Boot Modes (Local Attack Surface):**
- **Fastboot:** Android fastboot utility, screen black, activated by holding minus button + USB connect
- **Recovery:** Exposes 2 HID devices (PS Controller, PS Link Audio), screen black

**Attack Surface Comparison with PS5:**
- Less secure platform: Android 13 (Google security model, not Sony hardened kernel)
- Fastboot potentially unlockable via USB — allows flashing custom boot images
- Recovery mode HID interfaces exploitable via crafted USB descriptors
- Master key known — firmware updates potentially decryptable/modifiable
- DWCP PUP format parsing — similar to PS5 update mechanism but potentially less hardened
- Remote Play (PS Link) over Wi-Fi — man-in-the-middle or protocol exploitation

## Chipset-Level Vulnerabilities

### Southbridge Error Codes

The CXD90061GG southbridge (Salina / MediaTek MT3613CT) reports error codes revealing internal architecture:

| Code | Meaning | Security Relevance |
|------|---------|-------------------|
| 0xFFFFFFFF | No Errors | Normal |
| 0x80000001 | Overheat or Init APU Error | Thermal fault detection |
| 0x80000009 | Unexpected Power Cut / Shutdown Failure | Power glitch detection |
| 0x80050000 | APU VRM (2 Phases) Power Fail | VRM fault — glitch target feedback |
| 0x80060000 | APU VRM (6 Phases) Power Fail | VRM fault — glitch target feedback |
| 0x80800000 | Kernel Panic Shutdown | OS crash indication |
| 0x80800014 | TPM 2.0 (Floyd) or Power Failure | TPM communication attack |
| 0x80802081 | SSD Controller ↔ APU Data Line Error | SSD DMA/bus fault |
| 0x80810001 | General Power Failure | Broad power fault |
| 0x80830000 | GDDR6 Data Line Issue | Memory bus fault — fault injection feedback |
| 0x80871001 | DDR4 Error (Power/Short) | SSD cache RAM issue |
| 0x80891001 | SSD Controller or DDR4 Error | Storage subsystem fault |
| 0x808B0098 | DDR4 Communication Issue | SSD bus error |
| 0x80C00136 | Wi-Fi or BT Problem/Power Failure | Wireless subsystem fault |
| 0x80C00140 | APU Freeze (No Response) - GDDR6 Issue | System lockup — critical for glitch timing |
| 0x86000005/06 | NOR Corrupt | Serial flash validation failure — critical |
| 0xC0020103-0xC0020303 | APU Not Responding | SoC communication failure |
| 0xC00C0002 | VRM Controller Failure | XDPE14286A fault |
| 0xC0810002-0xC0810303 | HDMI IC Problem / Power Failure | MN864739 fault |
| 0xE0000001-0xE0000006 | Southbridge Issue — Cannot Read | Internal Salina failure |

**Security Relevance:** Error codes indicate hardware fault detection thresholds — useful for determining glitch margin before detection. Code 0x80C00140 (APU Freeze) indicates southbridge monitors APU responsiveness — a fault detection mechanism to bypass. NOR Corrupt (0x86000005/06) indicates serial flash integrity check failure — useful feedback when testing flash modifications. TPM error (0x80800014) reveals Floyd chip communication status.

### HDCP/HDMI

**HDMI Chip:** Panasonic MN864739 (codename FLAVA), DP-to-HDMI conversion:
- Input: 4-lane DisplayPort from SoC
- Output: HDMI 2.0 with 4 TMDS channels (D0, D1, D2, CK)
- Interfaces: Host I2C (HSDA/HSCL), DDC (SDA/SCL), CEC
- Power: 1.8V, 0.9V analog, 3.3V
- Clock: 27 MHz SYSCLK input
- Key pins: HPD, /HDMI_RESET, /HDMI_IRQ, DPHPD_IRQ
- Test pad: CL3020

**HDCP 2.3 Attack Surface:**
- HDCP key storage in MN864739 — extraction via side-channel or I2C bus monitoring
- Host I2C interface (HSDA/HSCL) — bus-level attack vector for probing HDCP communication
- Error codes 0xC0810002-0xC0810303 (HDMI IC problems) — reveal HDCP authentication failures
- HDMI 2.1 VRR and 4K120 features involve additional HDCP bandwidth negotiation
- HDMI TMDS lines emit RF energy correlated with video content — possible side channel

### Audio DSP

The APU contains the ACP (Audio Co-Processor) at MMIO 0xE0680000-0xE06BFFFF (device 0.6 pci2, codename ajm0). GPU includes Azalia audio at 0xE06C0000-0xE06C3FFF (device 0.1 pci2). The Tempest 3D Audio engine runs on dedicated hardware.

**Firmware:** DSP firmware codename "Onion" (Lord of the Rings theme). In the DualSense, a separate MediaTek MT3616XXX (codename Spider) provides the main MCU/DSP with ARM Cortex M4 and N9 DSP core.

### TPM / Floyd

**Floyd Chip (TPM 2.0):** Codename for the TPM chip. Firmware hex codenames: C0040001-C0040002 (floyd_fw). Error code 0x80800014 indicates TPM 2.0 or power failure.

**Role:** Trusted platform functions, potentially including secure boot measurements, DRM key storage, and platform attestation. Communication likely via /dev/icc_floyd in the kernel. The TPM provides an additional hardware root of trust beyond the PSP.

## Security Chip Analysis

### AMD PSP Integration

**Role in PS5:**
- Executes PS5 boot ROM (immutable on-die mask ROM)
- Handles cryptographic operations: AES-CBC, RSA-4096, SHA-256
- Manages secure key rings from OTP fuses
- Loads and validates Secure Modules via SceSbl dispatch
- DRM enforcement through key management and content decryption
- HDCP key management (communicates with MN864739 via I2C through Salina)
- Power management communication with Salina southbridge
- First processor to run on power-up — controls release of x86 cores

**PSP Architecture (from AMD Platform Security Processor documentation):**
- ARM Cortex-A5 with TrustZone (standard PC implementation)
- On PS5: likely a custom implementation using a Zen 2-based core (codename Ariel within the APU) rather than ARM Cortex-A5 — listed as "Ariel" = GPU part of APU, "sbl0" at MMIO 0xE0500000-0xE05FFFFF, device 0.2 on pci2
- Runs proprietary firmware; AMD refused open-sourcing
- Full system DRAM access with MMIO capabilities — no memory isolation from x86 applications
- Provides RNG and TPM services

**Known Attack Surface:**
- PSP syscall interface via secure module dispatch (SceSbl, service IDs like 0x80021000 for authentication manager, 0x80021001 for KMS, 0x8002100B for manufacturing)
- TEE application loading via TEE_IOC_DLM_START_TA_DEBUG (0xC028B409) and TEE_IOC_DLM_FETCH_DEBUG_STRING (0xC110B40A) IOCTLs
- Shared memory with OS via the MMIO region (sbl0 at 0xE0500000-0xE05FFFFF and 0xE06C6000-0xE06C7FFF)
- Voltage glitching to bypass Secure Loader signature verification (academic paper, applicable to all Zen-based AMD-SP)
- Speculative execution vulnerabilities (ZenBleed, Retbleed, Inception) cross the PSP ↔ OS boundary
- Multiple CVEs from CTS Labs (2018) and Cfir Cohen (2017) reported against AMD PSP in general

**PSP vs PS4 SAMU:** SAMU on PS4 was a dedicated security coprocessor with limited attack surface exposure. On PS5, the PSP is integrated into the Zen 2 APU, inheriting the full microarchitectural attack surface of the Zen 2 core. This represents both a capability increase (more computational power for security operations) and an attack surface expansion (more side channels, speculative execution vulnerabilities, shared die resources).

### Keystone

Keystone is an SceSbl-managed verification mechanism referenced in the kernel device /dev/pfsmgr (PFS Manager for trophies, savedata, keystone). The primary API surface is `sceSblSsVerifyKeystone` in SceSbl, which verifies keystone measurements against expected values. Keystone likely underpins content protection policies — a media player can verify the system is in an approved boot configuration before decrypting premium content. While PS5-specific Keystone implementation details remain undocumented, its presence in the SceSbl API confirms it plays an ongoing role in runtime security enforcement rather than being a legacy compatibility feature.

### Secure Module Distribution

Kernel SceSbl dispatches 20+ secure modules:
- Authentication Manager (0x80021000): sceSblAuthMgrAuthHeader (SELF verification), sceSblAuthMgrLoadBlock, sceSblAuthMgrSmLoad
- Key Management Service (0x80021001): sceSblKmsAllocKmbSlotForPprPkg, sceSblKmsSetKeyId
- PUP update verification (0x80021002): sceSblPupExpirationGetStatus
- Manufacturing (0x8002100B): sceSblManuAuthSetManuMode, sceSblManuAuthLoadSecureModule — if reachable from userland, bypasses signed module requirements
- External HDD verification (0x8002100F): sceSblExternalHDDVerifyMetadata

### Secure Boot Chain

The immutable Boot ROM (mask ROM within PSP):
1. Validates Secure Loader IPL via magic `E4 DB 7C 02` at serial flash offset 0x800
2. Verifies RSA-4096 signature against ROM Key 2
3. Sets up secure key rings from OTP fuses
4. Decrypts IPL body using dual-layer AES-128-CBC (Layer 1: global firmware key, Layer 2: revision nonce-derived key)
5. If any step fails, the system halts

After Secure Loader is validated and decrypted, it loads:
- EMC firmware (at serial flash offset 0x4000 in SLB2 format)
- Kernel
- Hypervisor (on FW >=3.00, loaded by HyLonome / Hypervisor Loader)
- Secure Modules

### TMR (Trusted Memory Regions)

TMRs provide encrypted memory compartments managed by SceSbl:
- sceSblTmrMap, sceSblTmrUnmap
- sceSblTmrEncAmmPt, sceSblTmrDecAmmPt
- sceSblTmrExport

TMR heap OOB (TheFloW, FW <=6.02) demonstrated crafted TMR operations corrupting hypervisor heap. Prosperous (fail0verflow/flatz 2026, FW <=4.51) edited TMR protection state for arbitrary hypervisor read/write.

## M.2 SSD Encryption Analysis

**Internal SSD Controller:** SIE CXD90062GG (codename Zao, based on Marvell 88SS1098), 12 NAND channels (CH4-CH11), 8-bit data bus each, 1.2V NAND I/O (VDDQFIO), PCIe Gen4 interface for M.2 expansion.

**Encryption Key Status:** Static dummy encryption keys are used across FW 1.00-12.20. This discovery fundamentally undermines data-at-rest security on the PS5:
- The encryption applied to internal SSD data is effectively cosmetic
- Anyone with physical access to the NAND chips can read data using known or guessable keys
- Keys may be per-firmware-version (not per-console), making extraction from any single unit sufficient for all units on that firmware
- As of FW 12.20+, the key status may have changed — this requires verification
- The DDR4 cache chip on the SSD controller (referenced by error codes 0x80871001, 0x80891001, 0x808B0098) may also contain plaintext keys or data

**Impact:** Game backups, DRM state, user data, and credentials stored on internal SSD are recoverable without defeating any Sony cryptographic protection if static keys are confirmed. This makes chip-off NAND reading a viable data recovery and game backup extraction method.

## Relationships

- [[hardware_overview]] — main hardware research describing all components
- [[southbridge_analysis]] — southbridge firmware and Salina CXD90061GG details
- [[attack_surface]] — general attack surface enumeration across all layers
- [[mitigation_assessment]] — which hardware mitigations have been bypassed publicly
- [[security_model]] — hardware roots of trust: PSP, Boot ROM, OTP fuses, Floyd TPM
- [[boot_chain]] — hardware initialization sequence from power-on to kernel load
- [[webkit_kernel]] — software exploits that bypass hardware protections to achieve code execution

## References

### psdevwiki Hardware
- https://www.psdevwiki.com/ps5/Serial_Flash
- https://www.psdevwiki.com/ps5/AMD_Platform_Security_Processor
- https://www.psdevwiki.com/ps5/Serial_Database
- https://www.psdevwiki.com/ps5/Jigkick_Files
- https://www.psdevwiki.com/ps5/MMIO_Prototype
- https://www.psdevwiki.com/ps5/Prototype_Units
- https://www.psdevwiki.com/ps5/Codenames
- https://www.psdevwiki.com/ps5/Motherboards
- https://www.psdevwiki.com/ps5/CPU
- https://www.psdevwiki.com/ps5/GPU
- https://www.psdevwiki.com/ps5/Memory
- https://www.psdevwiki.com/ps5/Storage
- https://www.psdevwiki.com/ps5/Power
- https://www.psdevwiki.com/ps5/Wireless
- https://www.psdevwiki.com/ps5/USB_Drive
- https://www.psdevwiki.com/ps5/USB_Extended_Storage
- https://www.psdevwiki.com/ps5/M.2_SSD
- https://www.psdevwiki.com/ps5/Disc_Drive/Media
- https://www.psdevwiki.com/ps5/MAC_Address
- https://www.psdevwiki.com/ps5/Southbridge_Error_Codes
- https://www.psdevwiki.com/ps5/Bluray_Drive_Firmware
- https://www.psdevwiki.com/ps5/CXD90060GG
- https://www.psdevwiki.com/ps5/CXD90061GG
- https://www.psdevwiki.com/ps5/CXD90062GG
- https://www.psdevwiki.com/ps5/CXD90063R-1
- https://www.psdevwiki.com/ps5/MN864739
- https://www.psdevwiki.com/ps5/XDPE14286A
- https://www.psdevwiki.com/ps5/MT3613CT
- https://www.psdevwiki.com/ps5/Bond
- https://www.psdevwiki.com/ps5/DualSense
- https://www.psdevwiki.com/ps5/DualSense_DFU_Modes
- https://www.psdevwiki.com/ps5/DualSense_HID_Commands
- https://www.psdevwiki.com/ps5/PS5_Peripherals
- https://www.psdevwiki.com/ps5/PlayStation_VR2
- https://www.psdevwiki.com/ps5/PSVR2
- https://www.psdevwiki.com/ps5/PSVR2_Update_Format
- https://www.psdevwiki.com/ps5/HD_Camera
- https://www.psdevwiki.com/ps5/PS_Portal
- https://www.psdevwiki.com/ps5/Vulnerabilities

### CPU Architecture
- https://en.wikipedia.org/wiki/AMD_Zen
- https://en.wikipedia.org/wiki/AMD_Platform_Security_Processor
- https://arxiv.org/abs/2108.04575 (One Glitch to Rule Them All)

### Jailbreak / Community
- https://docs.google.com/spreadsheets/d/1dgu0p7U2yB_mhcUELz-Wkc7Yhs-avoWLY1Gcm0n5XJw/edit (PS5 Jailbreak Compatibility Sheet)
- PSPReverse GitHub project

### CVEs Referenced
- CVE-2023-20593 (ZenBleed)
- CVE-2022-29900, CVE-2022-29901 (Retbleed)
- CVE-2023-31315, CVE-2024-21955, CVE-2024-36347 (EntrySign)
- CVE-2023-20569 (Inception/SRSO)
- CVE-2022-22620 (WebKit)
- CVE-2021-38003 (V8 TheHole)
- CVE-2024-43102 (umtx_shm)
- CVE-2020-7457 (IPv6)
