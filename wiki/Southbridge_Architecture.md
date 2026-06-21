# Southbridge Architecture

## Overview

The PS5 southbridge is a multi-function embedded controller managing low-level hardware initialization, power sequencing, peripheral connectivity, system monitoring, and debug infrastructure. The primary chip is the **SIE CXD90061GG** (MediaTek MT3613CT, codename **Salina**), integrating three co-processors: EMC (Error Management Controller, ARM), EAP (Embedded Application Processor, Marvell PJ4C ARM at 500 MHz), and a Communication Processor for inter-component messaging.

The southbridge runs its own independent firmware on external serial flash (Winbond **W25Q16JVNIM**, 2 MB) and NVS flash (Winbond **25Q256JVEQ**, 32 MB), making it a persistent firmware island that survives OS reinstalls and power cycles. It communicates with the AMD PSP over dedicated buses and shares responsibility for boot sequencing.

## Architecture

### EMC (Error Management Controller)

The EMC is the primary embedded controller within the southbridge — an ARM-based processor handling power-on initialization, power sequencing, thermal management, error detection, and system monitoring.

**Firmware:**
- Serial flash offset **0x4000**, length **0x7E000** bytes (~504 KB)
- SLB2 format, extractable via **blsunpack**, AES-128-CBC encrypted (rev c0 key documented)
- Version history: v0.7.6 (prototype) → v1.14.3 (FW 9.20+)

**Power Management:**
- Controls PSW_MSOC_PGC, SOC_PWROK, /SOC_VRM_HOT, /SOC_GPU_PCC signals
- Monitors 5V_MAIN, 1.8V_SOC_VDDA, 3.3V_VRM, 1.2V_VRM, 12V_MAIN power rails

**Thermal Management:**
- AUXADC thermistor inputs for motherboard temperature sensors
- Variable speed FAN_PWM fan control
- Thermal trip (/SOC_THERMTRIP) and warning (/SOC_ALERT) signals

**Error Codes:**
- 0xFFFFFFFF: No errors
- 0x80000001-0x808FFFFF: APU, power, kernel panic errors
- 0xC0000000-0xC0FFFFFF: APU response, VRM controller failures
- 0xE0000000-0xE0000006: Southbridge self-diagnosis failures
- Error log at NVS offset 0x1200 (0x400 bytes capacity)

**Security Flags (NVS):**
- Offset 0x1010: EMC checksum validation — FF = disabled
- Offset 0x1012: EMC UART — FF = enabled

### EAP (Embedded Application Processor)

The EAP runs a full **FreeBSD 9.0-RELEASE** operating system on a **Marvell PJ4C ARM** (rev 2) at 500 MHz, with 512 MB DDR3 (800 MHz). It handles higher-level debug and communication functions.

**Specifications:**
- SDK Version: 5.501.000, Sycorax Version: 01.00.01.01
- Subsystem ID: 0x00040100 (Belize2 A0), Boards ID: 0x2001010101010501
- Available memory: ~473 MB (after firmware reservation)

**Peripherals:** UART, RTC, SDHCI/SDIO, Belize GbE, XHCI USB 3.0, I2C GPIO (TCA9539), LED drivers (TLC59116), DECI5 debug interface

**Boot Sequence (~50 seconds to CP Ready):**
KBL boot → FreeBSD kernel → device enumeration → DHCP → CP firmware update check → emcd, uartd, disabler, DECI5s, DECI5 daemons

**Key Ladder:**
- EAP KBL: AES-128-CBC keys for Kernel Boot Loader decryption
- EAP Kernel SELF: AES-128-CBC cipher key + RSA-3072 key pair for kernel signing

### Communication Processor

Central routing and management component handling inter-processor communication, DECI5 protocol, and the secure key chain spanning EMC/EAP/KBL domains with **HMAC-SHA1** integrity protection.

**Key Chain:**
- EMC keys: AES-128-CBC IPL cipher keys
- EAP KBL keys: AES-128-CBC decryption keys
- EAP Kernel SELF keys: AES-128-CBC + RSA-3072
- UCMD authentication: Key 2 (RSA) + Important Keys 3

**DECI5 Protocol Routing:**
- Shared memory nodes: DECI_SHM_NODE_MAGIC1_CP, MAGIC1_EAP, MAGIC1_MAIN, MAGIC1_MP3, MAGIC1_MP4, MAGIC1_SYCORAX
- Fix channels (point-to-point) and ring channels (buffered)
- Targets: EAP, MAIN (x86 APU), MP3 (TEE), MP4, SYCORAX

## CP Box (CPBH-100)

Hardware debug accessory for TestKits, connecting via USB-C. Provides Assist Mode (relaxed security), DECI5 over Ethernet, manufacturing mode access, and UART debug pins for EMC and EAP serial consoles.

**Two Modes:**
1. Engineering Mode: USB-C only, basic debug connectivity
2. Normal Mode: USB-C + Ethernet (DEV LAN to host) + optional HDD

**Critical Behavior:**
- Must be connected before PS5 power-on; absence locks TestKit in Release Mode
- Assist Mode *persists in memory* across power-off cycles
- CP Box can read PS5 info (serial, mode) while PS5 is powered off (independent power)

## DIP Switches

256 logical boot parameter flags loaded from CP Box MMIO, gated by console type:

| Type | Access |
|------|--------|
| Retail | None (0 switches) |
| TestKit | Limited subset |
| DevKit | Most switches |
| intdev DevKit | All 256 switches |

**Key Flags:**
- 0x02: IsAssistMode (TestKit)
- 0x1E: DisableBinaryVersionCheck
- 0xF1: manu_mode related

## Manufacturing Functions

The highest-value attack target on the PS5 — if reachable, bypasses all code signing.

| IOCTL | Code | Impact |
|-------|------|--------|
| set-manu-mode | **0xC0184D03** | Gates all other manu functions |
| load-module | **0x40184D01** | Load unsigned secure module — bypasses all signature verification |
| unload-module | **0x40184D02** | Unload security modules (authmgr, pup, sysveri, npdrm) |

Requirements: dipswitch 0xF1 enabled, appropriate console type, manu module (0x8002100B) loaded.

## Serial Flash (W25Q16JVNIM)

2 MB Winbond SPI flash storing the Secure Loader and EMC firmware.

**Layout (2 MB):**

| Offset | Content |
|--------|---------|
| 0x0000-0x07FF | Boot config, unused |
| **0x0800** | **Secure Loader IPL** (0x400 header + encrypted body) |
| **0x4000** | **EMC firmware** (SLB2, ~504 KB) |

**Write Protection:** /WP pin tied to **3.3V_SS_PG1** (SoC Power Good). Flash is writable only when SoC has stable power. Physical bypass via desoldering, chip-off, or lifting pin 3 to GND.

**NVS Flash (Winbond 25Q256JVEQ, 32 MB):** Stores platform ID, MAC address, EAP config, UART enables, error logs, serial number at NVS offset 0x1C4000.

## Attack Surface

### SPI Flash Manipulation
- SOIC-8 clip + Raspberry Pi can dump serial flash contents
- Modified EMC firmware persists across OS reinstalls undetected
- EMC firmware rootkit cannot be detected by any software on the main PS5 OS

### Manufacturing Mode Escalation
- If reachable: load unsigned secure modules, disable DRM/auth/verification
- Drive auth reset could bypass disc drive verification

### Assist Mode + DIPSW Combination
- Assist Mode (0x02) + binary version check disable (0x1E) + manu_mode (0xF1) = full debug access

### EAP Network Services
- FreeBSD 9.0-RELEASE with known vulnerabilities
- DEV LAN DHCP, potential service exposure
- cpupdate file format undocumented

## Research Gaps

- Full EMC firmware disassembly (504 KB ARM code, ongoing)
- Complete CP Box/DECI5 protocol reverse engineering
- Manufacturing function reachability on retail consoles (unknown)
- EAP network service enumeration
- Key chain runtime dumping via EAP/CP Box access
- Voltage/clock glitching of southbridge SPI interface

## References

- `research/hardware/southbridge_analysis.md` — full 860-line source document
- [psdevwiki: CP Box](https://www.psdevwiki.com/ps5/CP_Box)
- [psdevwiki: EMC](https://www.psdevwiki.com/ps5/EMC)
- [psdevwiki: DIPSW](https://www.psdevwiki.com/ps5/Dipsw)
- [psdevwiki: Manufacturing Functions](https://www.psdevwiki.com/ps5/Manufacturing_Functions)
- [psdevwiki: Serial Flash](https://www.psdevwiki.com/ps5/Serial_Flash)
- [psdevwiki: Southbridge Error Codes](https://www.psdevwiki.com/ps5/Southbridge_Error_Codes)
