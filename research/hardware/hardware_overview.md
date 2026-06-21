# PS5 Hardware Architecture

## Overview

The PlayStation 5 is Sony's 9th generation home console, released November 12, 2020 in NA/AU/NZ/JP/KR and November 19, 2020 globally. Two retail models exist at launch: the standard edition with an Ultra HD Blu-ray disc drive (CFI-10XX, 390x260x104mm, 4.5 kg) and the digital edition without disc drive (CFI-11XX, 390x260x92mm, 3.9 kg). The console is built around a custom semi-custom AMD APU codenamed Oberon (PS5) or Viola (PS5 Pro), combining a Zen 2 CPU complex with an RDNA 2 GPU on a single die. The APU (SIE CXD90060GG) is a large BGA package with hundreds of pins, featuring a GDDR6 memory interface across four channels (E0, E1, D0, D1) and SVI2 power management for 1.0V SOC power domains.

Three chassis generations exist: FAT (CFI-10/11/12, 825 GB, 2020-2023), Slim (CFI-20/21, 848 GB/1 TB, 2023+), and Pro (CFI-70/71, 2 TB, 2024+). The system is powered by an ADP-400DR internal PSU rated at 350W (standard) or 340W (digital), multi-voltage 110-240V, with measured peak draw of approximately 207W during gameplay (Spider-Man Miles Morales). Motherboard revisions span EDM-010 (initial retail) through EDM-020, 030, 040, 041, 044, AR10, AK30, BK21, with the PS5 Pro using VSM-010.

The hardware uses a unified memory architecture where 16 GB of GDDR6 is shared between CPU and GPU via a 256-bit bus at 448 GB/s. Storage is provided by a custom 825 GB PCIe 4.0 SSD (soldered to the motherboard, non-replaceable) using a proprietary controller based on the Marvell 88SS1098 (SIE CXD90062GG, codename Zao) driving 12 NAND channels. An M.2 2282 PCIe 4.0 x4 expansion slot supports NVMe SSDs from 250 GB to 8 TB (4 TB before system software 8.00), requiring a heatsink. USB extended storage (HDD) uses the same format as PS4.

## Components

### SoC (Oberon / Viola)

The main APU is the SIE CXD90060GG, a custom AMD APU integrating both CPU and GPU on a single die.

**CPU Complex (codename Oberon/Oberon Plus for CPU partition):**
- Architecture: x86-64 AMD Ryzen Zen 2
- 8 cores, 16 threads
- Variable frequency up to 3.5 GHz
- SVI2 power management (VDDCR_CORE at 1.0V_SOC_VCORE)

**GPU Complex (codename Azalia/Ariel for GPU partition):**
- Architecture: AMD RDNA 2 with Ray Tracing Acceleration
- Variable frequency up to 2.23 GHz
- 10.28 TFLOPS peak floating-point performance
- SVI2 power management (VDDCR_GFX at 1.0V_SOC_VGFX)
- 1.35V_G6_VMEMIO for GDDR6 memory interface

**SoC Codename Mapping:**
- Oberon: PS5 APU (CXD90060GG)
- Oberon Plus: Revised PS5 APU stepping
- Viola: PS5 Pro APU
- Prospero: PS5 system codename (Shakespeare theme)
- Ariel: GPU partition within the APU
- Azalia: GPU part (Lord of the Rings theme)

### Memory

- 16 GB GDDR6 total, eight 2 GB modules
- Manufacturer: Micron Technology
- Part number: MT61K512M32KPA-14C:B (FBGA code D9XKV)
- 256-bit memory bus (4 channels: E0, E1, D0, D1)
- 448 GB/s bandwidth
- Unified memory pool shared between CPU and GPU

### Storage

**Internal SSD:**
- Custom 825 GB PCIe 4.0 SSD, soldered to motherboard (non-replaceable)
- Proprietary custom SSD controller: SIE CXD90062GG (codename Zao, based on Marvell 88SS1098)
- 12 NAND flash channels (CH4 through CH11), 8-bit data bus each
- DDR4 memory chip for SSD controller
- 5.5 GB/s raw sequential read bandwidth
- 1.2V NAND I/O voltage (VDDQFIO)
- Additional DDR4 for controller caching (0x80871001/0x808B0098 error codes reference DDR4 issues)

**M.2 Expansion Slot:**
- PCI-Express Gen4x4 NVMe SSD (Socket 3, Key M)
- Storage capacity: 250 GB - 8 TB (4 TB limit before FW 8.00)
- Form factors: 2230, 2242, 2260, 2280, 22110
- Width up to 25 mm with heatsink, thickness up to 11.25 mm
- Heatsink required: max 2.45 mm below, 8 mm above
- Requires system software 4.00 or later
- PCIe 3.0 drives may work with workaround; M.2 SATA not supported

**USB Extended Storage:**
- USB HDD support for PS4 games
- Format matches PS4 USB Extended Storage format
- USB drives also supported for media gallery screenshots/video export (exFAT/FAT32)

### Motherboard Revisions

**PS5 (Oberon) Motherboards:**
- EDM-010: Initial retail revision
- EDM-020, EDM-030, EDM-040, EDM-041, EDM-044: Later retail revisions with component changes
- EDM-AR10, EDM-AK30, EDM-BK21: Additional board variants

**PS5 Pro (Viola) Motherboards:**
- VSM-010: PS5 Pro motherboard model

**PS VR2 Motherboard:**
- EPT-01 (1-010-109-11): VR2 headset mainboard

**DualSense Motherboard:**
- BDM-010: Retail DualSense board
- BDM-010 R10: Engineering sample with MT3616ECT

### Southbridge / EMC

The SIE CXD90061GG (MediaTek MT3613CT based, codename Salina) serves as the southbridge/Embedded Micro Controller (EMC) with bundled SysCon firmware. It provides:

- **Peripheral Connectivity:** Gigabit Ethernet (4 pairs MDI0-MDI3), SATA (Port 0 and 1), USB 2.0 (Port 2)
- **PCIe:** Gen3 to Flash Controller, Gen1 to WiFi module
- **System Buses:** I2C (HDMI, SOC, general purpose), SPI (serial flash), UART (debug)
- **PWM:** FAN, LED, Buzzer control
- **System Management:** AUXADC (thermistor monitoring, power button, AC detect), RTC (32.768 kHz crystal)
- **Power Supplies:** 3.3V, 1.8V, 1.15V, 1.2V domains
- **Clock Generation:** 25 MHz main crystal, 27 MHz for HDMI (FLAVA), 100 MHz PCIe reference clocks
- **Key Signals:** PSW_* (power sequencing), /SOC_ALERT (thermal trip), /SOC_THERMTRIP, /HDMI_IRQ, FAN_PWM

EMC firmware hex codenames: C0000001 (emc_ipl)

### Power System

- Standard model: 350W internal PSU (ADP-400DR)
- Digital edition: 340W internal PSU
- Multi-voltage: 110-240V operation across all regions
- Typical gaming power draw: ~207W peak (Spider-Man Miles Morales)
- APU Voltage Regulation: Infineon XDPE14286A VRM controller
  - 8+2 phase PWM control for APU power
  - Manages VDDCR_GFX (GPU) and VDDCR_CORE (CPU) via SVI2
  - Input voltages: 1.8V_SOC_VDDA, 3.3V_VRM, 1.2V_VRM, 12V_MAIN
  - Temperature sensing (TSEN1/TSEN2), power good/fail outputs
  - Key signals: PSW_MSOC_PGC (enable), SOC_PWROK, /SOC_VRM_HOT, /SOC_GPU_PCC

### I/O and Connectivity

- **Wired Networking:** Gigabit Ethernet (via Salina southbridge GBE controller)
- **Wireless Module:** Sony AK8M19DFR1 (M19DFR1) module providing Wi-Fi IEEE 802.11ax and Bluetooth 5.1
- **Bluetooth:** 2.402-2.48 GHz, 2.5 mW (DualSense communication)
- **USB Ports:** 3x USB 3.1 (Type-A), 1x USB-C (front)
- **Video Output:** HDMI 2.1 (via Panasonic MN864739, codename FLAVA)
  - Input: 4-lane DisplayPort from SOC
  - Output: HDMI 2.0 with 4 TMDS channels (D0, D1, D2, CK)
  - Interfaces: Host I2C (HSDA/HSCL), DDC (SDA/SCL), CEC
  - Power: 1.8V, 0.9V analog, 3.3V domains
  - Clock: 27 MHz SYSCLK
  - Key pins: HPD (Hot Plug Detect), /HDMI_RESET, /HDMI_IRQ, DPHPD_IRQ
  - 4K 120Hz, VRR support

### Serial Flash

- Winbond W25Q16JVNIM serial flash memory
- 2 MB (16 Mbit) capacity
- 150mil SOIC package
- SPI interface signals: /CS, /MISO, /WP, GND, VCC, /HOLD, SCLK, MOSI
- Stores boot configuration and non-volatile parameters
- Dumpable via Raspberry Pi SPI interface using flashrom
- Critical attack surface for boot-level exploitation
- Serial number stored at sflash offset 0x1C7250
- Model number stored at sflash offset 0x1C7230

### Chassis and Serial Number Decoding

**FAT (CFI-10/11/12, 825 GB):**
- CFI-1008A (Russia, min FW 1.00), CFI-1015A (US, min FW 1.00), CFI-1016A (Europe, min FW 1.00), CFI-1002A (Australia, min FW 1.00)
- CFI-1100A (Japan), CFI-1116A (Europe)
- CFI-1215A (US), CFI-1216A (Europe), CFI-1208A (Russia)
- Factory firmware range: 1.00 (CFI-10) through 7.61 (CFI-12)

**Slim (CFI-20/21, 848 GB / 1 TB):**
- Factory firmware range: 7.00 (CFI-20) through 13.20 (CFI-21)

**Pro (CFI-70/71, 2 TB):**
- Factory firmware range: 9.05 (CFI-70) through 13.20 (CFI-71)

**Serial Format:** S01-[Region Letter][Model Digit][Year Digit][Month/Week Letter]xxxxxxxxxxxx
- Region codes: AJ/AK (USA), S01 (UK/EU), J (Japan)
- Region codes in IDPS: 82 (US/CA), 84 (US UCS), 87 (Europe EU8), 89 (Australia), 8A (Asia), 8C (Russia)
- Fan models vary by chassis: NMB, Delta, Nidec, Foxconn

### Media Playback

- Ultra HD Blu-ray drive (standard model only, drive model 502R)
- Blu-ray drive firmware versions: BD 1072 (FW 1.00), BD 1073 (FW 1.05), BD 1119 (FW 3.00), BD 1137 (FW 4.03), BD 1275 (FW 8.60)
- Blu-ray: region locked, Dolby Atmos, DTS:X support
- DVD: region locked, 5 region switches
- 4K Blu-ray: region locked, HDR10 and HLG only (no Dolby Vision, no HDR10+)
- No CD playback, no 3D Blu-ray support
- No external USB disc drive support
- USB media: exFAT/FAT32, requires Music/Video/Pictures folders
- Video codecs: H.264 MKV/MP4 up to 4K, VP9 WEBM up to 4K (no local HEVC)
- Audio: FLAC stereo, MP3, AAC stereo (no DRM files)
- Tempest 3D Audio Tech for spatial audio

### Peripherals

**DualSense Wireless Controller (codename: Bond):**
- Product code: CFI-ZCT1
- USB VID/PID: 054c:0ce6 (Sony Corp.)
- Revision IDs: 0x0CE6 (Bond), 0x0CE7 (Aston/early), 0x0D5A (Lotus/Media Remote)
- Bluetooth 2.402-2.48 GHz, 2.5 mW output
- USB Type-C wired interface
- 1,560 mAh battery
- Main MCU/DSP: SIE CXD9006GG (rebranded MediaTek MT3616XXX, ARM Cortex M4 & N9 DSP core) — codename Spider
- PMIC: Dialog DA9087
- Audio Codec: Realtek ALC5524 (codename Venom)
- Audio Amplifier: Realtek ALC1016 or Nuvoton NAU8225 3.0W Class-D
- Sub DSP: MediaTek MT3613CT (codename Onion)
- Trigger Assembly: Walther
- USB classes: Audio (speaker, microphone), HID
- USB classes: Audio (speaker, microphone), HID

**DualSense Firmware Structure (stored at /system_ex/etc/):**
- Banana firmware (main MCU): 0x40 copyright, 0x10 build date, 0x10 build hour, 0x62 Product ID (0xCE6), 0x68 full size, 0x6C SDK version, 0x70 firmware version, 0x74 SwSeries, 0x78 ControllerVersion
- Venom firmware (audio): Type string "VenomB", build date, firmware version, body size
- Betty firmware: Type string "BettyBND", build date, body size
- Example: Nov 2020 (SwSeries 0x0004, ControllerVersion 0x0210, FW 2.50)

**DualSense DFU Modes:**
- DFU Primary Boot Loader (PBL): Flash SBL only
- DFU Secondary Boot Loader (SBL): Flash Main/Banana, Venom (Audio), Onion (DSP)
- Main Mode: Flash Venom (Audio), Onion (DSP), Bluetooth Patches

**DualSense HID Commands (key operations):**
- Get MCU Unique ID: ReportID=128, DeviceID=1, ActionID=9
- Read Device Info: ReportID=128, DeviceID=1, ActionID=12
- Erase Device Info: ReportID=128, DeviceID=1, ActionID=13 (DANGER)
- Reset: ReportID=128, DeviceID=1, ActionID=1
- Reboot Secure Boot Loader: ReportID=128, RebootCmd=1
- Get Firmware Info: ReportID=32
- Get/Set BT Address: ReportID=129/128, DeviceID=9
- Set DFU Mode: ReportID=160, EnablePBLMode=1, EnableSBLMode=2
- Flash: ReportID=240, DownloadCmd=0, WriteCmd=1
- NVS Lock/Unlock: ReportID=128, DeviceID=3
- Device IDs: 1=Main MCU, 2=Power, 3=NVS, 5=Touch Panel, 6=Venom FW, 9=BT, 14=BT Patch, 15=Venom, 16=Spider DSP, 17=VDD External

**Other Official Peripherals (2020 launch):**
- DualSense Charging Station (CFI-ZDS1): Docks two controllers via bottom charging pins
- HD Camera (CFI-ZEY1): Dual wide-angle lenses, 1080p capture, built-in stand, background removal
- Media Remote (CFI-ZMR1): Bluetooth, IR transmitter, quick access to Disney+/Netflix/YouTube/Spotify
- PULSE 3D Wireless Headset (CFI-ZWH1): Tempest 3D AudioTech, dual hidden mics, noise-cancelling, wireless adaptor, 3.5mm jack, 12h battery
- PS Camera Adaptor (CFI-ZAA1): AUX (IN), USB 3 Type-A (out), 5V 500mA, 87x17x25mm, ~38g

**PS Portal (Remote Player):**
- Custom Android 13 operating system
- PS Portal Master Key: 35 15 A8 8F 33 55 7D F1 33 FB F2 08 D6 3B 0A AF (GCM)
- Update endpoint: dwc.dl.playstation.net (JSON firmware info)
- PUP structure: Magic "DWCP", Type=1, Full Size, Version
- Boot modes: Fastboot (minus+USB), Recovery (2 HID devices: PS Controller, PS Link Audio)
- Firmware versions: 1.0.0 through 6.0.1+

**PS VR2 (codename: EPCOT):**
- Motherboard: EPT-01 (1-010-109-11)
- Side A: SIE CXD90067GG, K4U6E3 4AAMGCL (DRAM), THGBMNG5 D1LBAIT (4GB eMMC), WM1801B 26M7YHS, PCA9957 24-channel SPI serial bus
- Side B: SIE CXD90068GF, RTS5443H M7C88C5 (Realtek Type-C Controller)
- Power Button Board: KEY-01 (1-010-112-11)
- Firmware update format: Magic "CUP!" with 7 file entries at offset 0x10

### Prototype and Development Units

**DevKit Variants:**
- EVA3-3: DUTP-DSNxxxBK-Lx (earliest, ~FW 0.75)
- Prototype 0: DUTP-DSNxxxBK-Rx
- Prototype 1: DUTP-DSNxxxBK-Wx (e.g., DUTP-DSN18AAK-W5, min FW 0.85.070)
- Prototype 2: DSWxxxBK-xx

**Testkits:** EGR-TAxxxK-Gx, EGR-TAxxxK-Jx (both Prototype 1 based)
**CP Boxes:** CPB-TAxxxK-Bx, CPB-TAxxxK-Cx (min FW 0.9.0.5)
**Controllers:** BDT-0250xxx (Bond), CFI-ZCT1x
**Cameras:** EDT-001
**Media Remotes:** LPT-D100x, CFI-ZMR1xx
**Prototype Wi-Fi/BT Chip:** AW-XM501

### MMIO Prototype Map

Base address: 0xFFFFF80000000000 (FW 0.85.070 and below, no kASLR)

| Region | Address Range | Device | Codename |
|--------|--------------|--------|----------|
| nvme0 | 0xC4200000-0xC4203FFF, 0xC4000000-0xC40FFFFF | device 0.0 on pci1 | Titania |
| tpcie0 | 0xA0000000-0xBFFFFFFF, 0xC0000000-0xC3FFFFFF | device 0.1 on pci1 | Titania PCIe |
| spcie0 | 0x8500C000-0x8500CFFF, 0x85200000-0x853FFFFF, 0x85400000-0x8547FFFF | device 0.5 on pci1 | Salina PCIe |
| mtsc0 | 0x85000000-0x85000FFF | device 0.2 on pci1 | Salina GBE |
| ahci0 | 0x85004000-0x85007FFF | device 0.3 on pci1 | Salina SATA0 |
| ahci1 | 0x85008000-0x8500BFFF | device 0.4 on pci1 | Salina SATA1 |
| xhci0 | 0x85600000-0x857FFFFF | device 0.6 on pci1 | Salina USB |
| apcie0 | 0x81300000-0x813FFFFF, 0x81400000-0x81407FFF, 0x81600000-0x817FFFFF | device 0.17 on pci1 | Belize/Caliban PCIe |
| gc0 | 0xD0000000-0xDFFFFFFF, 0xE0000000-0xE01FFFFF, 0xE0600000-0xE067FFFF | device 0.0 on pci2 | Graphics Core |
| az0 | 0xE06C0000-0xE06C3FFF | device 0.1 on pci2 | GPU/Azalia Audio |
| sbl0 | 0xE0500000-0xE05FFFFF, 0xE06C6000-0xE06C7FFF | device 0.2 on pci2 | Ariel (PSP) |
| xhci1 | 0xE0200000-0xE02FFFFF | device 0.4 on pci2 | PPR USB |
| xhci2 | 0xE0300000-0xE03FFFFF | device 0.5 on pci2 | PPR USB |
| ajm0 | 0xE0680000-0xE06BFFFF | device 0.6 on pci2 | ACP (Audio Co-Processor) |
| mp40 | 0xE0400000-0xE04FFFFF, 0xE06C4000-0xE06C5FFF | device 0.3 on pci2 | MP4 |
| deci_shm_main0 | 0x880000000-0x89FFFFFFF | device 0.19 on pci1 | DECI5 shared memory |
| bxe0 | 0x80000000-0x807FFFFF, 0x80800000-0x80FFFFFF, 0x81000000-0x8100FFFF | device 0.10 on pci1 | PCI BAR |

### Codename Reference

**James Bond Theme:**
- Bond: DualSense controller
- Aston: Early DualSense
- Lotus: Media Remote
- Walther: Trigger System (DualSense adaptive triggers)
- Venom: Audio Codec
- Tahoe: First southbridge revision
- Sierra: Second southbridge revision

**William Shakespeare Theme:**
- Prospero: PS5 system
- Caliban: CP Box EAP Kernel
- Sycorax: CP Box KBL
- Setebos: CP Box EMC FW
- Oberon/Oberon Plus: CPU part of APU
- Viola: PS5 Pro APU
- Titania: EFC/EAP / NVMe controller
- Ariel: GPU part of APU / PSP
- Tempest: 3D Audio Tech

**Islands Theme:**
- Salina: First southbridge revision / EMC

**Lord of the Rings Theme:**
- Antonio: Prototype DevKit board
- Tirion: SysCon on DevKit proto
- Onion: DSP firmware

**Others:**
- Sano: Prototype DevKit motherboard
- Carlo: CP board prototype
- Floyd: TPM chip
- Azalia: GPU part
- Gaikai: Remote Play
- Zao: NVMe/Flash controller
- FLAVA: HDMI chip (MN864739)
- EPCOT: PS VR2 headset
- Spider: Main MCU/DSP in DualSense

**Firmware Hex Codenames:**
- 40000001-40000003: Syscon
- 40030001: cp_fw
- C0000001: emc_ipl
- C0030002: wlanbt_fw
- C0040001-C0040002: floyd_fw (TPM)
- C0050001-C0050002: usbc_fw
- C3000005-C300000B: titania_fw

### Southbridge Error Codes

| Error Code | Description |
|-----------|-------------|
| 0xFFFFFFFF | No Errors |
| 0x80000001 | Overheat or Init APU Error |
| 0x80000009 | Unexpected Power Cut or Shutdown Failure |
| 0x80050000 | APU VRM (2 Phases) Power Fail |
| 0x80060000 | APU VRM (6 Phases) Power Fail |
| 0x80800000 | Kernel Panic Shutdown |
| 0x80800014 | TPM 2.0 chip or Power Failure |
| 0x80802081 | SSD Controller <-> APU Data Line Error |
| 0x80810001 | General Power Failure (Periphery, GDDR6, APU, Data Line Short) |
| 0x80830000 | GDDR6 Data Line Issue |
| 0x80871001 | DDR4 Error (Power Failure or Short Circuit) |
| 0x80891001 | SSD Controller or DDR4 Error |
| 0x808B0098 | DDR4 Error (Communication Issue) |
| 0x80C00136 | Wi-Fi or BT Problem or Power Failure |
| 0x80C00140 | APU Freeze (No Response) - GDDR6 Data Line Issue |
| 0x86000005/0x86000006 | NOR Corrupt |
| 0xC0020103-0xC0020303 | APU Not Responding |
| 0xC00C0002 | VRM Controller Failure |
| 0xC0810002-0xC0810303 | HDMI IC Problem or Power Failure |
| 0xE0000001-0xE0000006 | Southbridge Issue - Cannot Read Errors |

### Jigkick Files

The Jigkick PKG contains specialized firmware for manufacturing and repair:
- BD_EM_BOOT_FW: Recovery MediaTek Blu-ray firmware (brick recovery)
- BD_MAIN_FW: Blu-ray Drive Main Firmware (same as 30XR.bix)
- BD_VEEPROM_DATA: Blu-ray EEPROM Data
- GAME_OS_DIAG_2ND: Special zip file for diagnostics
- MANU_UPDATER: manufacturing_updater.self
- NET_LOAD_DIAG: Unknown, ~7 MiB

## Relationships

- [[system_overview]] — hardware provides the foundation for the entire system; all software layers depend on the hardware architecture described here
- [[kernel]] — the kernel manages all hardware resources including CPU scheduling, memory management, GPU command processing, and I/O device access via the MMIO map
- [[hypervisor]] — the hypervisor virtualizes hardware resources for isolation between the game OS and system OS; IOMMU configuration is critical
- [[security_model]] — hardware security primitives (PSP, secure boot, TPM/Floyd) enforce the chain of trust from power-on
- [[firmware]] — Syscon (40000001-40000003), EMC IPL (C0000001), Titania FW (C3000005-C300000B), and other firmware modules initialize and manage hardware components

## Security Considerations

- [[serial_flash]] — The Winbond W25Q16JVNIM SPI flash (2 MB) is a critical attack surface for boot-level exploitation via physical SPI dumping and reprogramming
- [[amd_platform_security_processor]] — The PSP (codename Ariel) handles the boot ROM, cryptographic operations, secure key rings, and Secure Module execution; similar security role to SAMU on PS4, CMeP on PS Vita, Kirk on PSP
- [[memory]] — GDDR6 is shared between CPU and GPU as a unified pool, affecting isolation boundaries and creating potential side-channel risks; southbridge error codes include GDDR6 data line errors (0x80830000)
- Motherboard revisions (EDM-010 through EDM-BK21, VSM-010 for Pro) may affect exploit compatibility due to component changes and firmware differences
- [[usb_drive]] — USB attack surface for media/save data injection; USB extended storage format matches PS4 format
- The SIE CXD90063R-1 chip remains undocumented — may be an additional security or management component
- TPM/Floyd chip (C0040001-C0040002 firmware) manages trusted platform functions; errors like 0x80800014 indicate TPM failures
- Controller HID interface exposes NVS lock/unlock, device info read/erase, BT address manipulation — these are attack surfaces through USB/BT
- PS VR2 firmware updates use "CUP!" format with 7 file entries; update package format analysis could reveal attack surfaces
- PS Portal runs custom Android 13 with fastboot and recovery modes accessible via USB — potential for low-level firmware manipulation
- Blu-ray drive firmware can be recovered via Jigkick's BD_EM_BOOT_FW; the BD drive uses a MediaTek controller with its own firmware attack surface

## References

- [PSDevWiki PS5 Overview](https://www.psdevwiki.com/ps5/PlayStation_5_-_PS5)
- [PSDevWiki Hardware](https://www.psdevwiki.com/ps5/Hardware)
- [PSDevWiki CPU](https://www.psdevwiki.com/ps5/CPU)
- [PSDevWiki GPU](https://www.psdevwiki.com/ps5/GPU)
- [PSDevWiki Memory](https://www.psdevwiki.com/ps5/Memory)
- [PSDevWiki Storage](https://www.psdevwiki.com/ps5/Storage)
- [PSDevWiki Motherboards](https://www.psdevwiki.com/ps5/Motherboards)
- [PSDevWiki Codenames](https://www.psdevwiki.com/ps5/Codenames)
- [PSDevWiki Serial Number Guide](https://www.psdevwiki.com/ps5/Serial_Number_guide)
- [PSDevWiki Serial Flash](https://www.psdevwiki.com/ps5/Serial_Flash)
- [PSDevWiki Power](https://www.psdevwiki.com/ps5/Power)
- [PSDevWiki Wireless](https://www.psdevwiki.com/ps5/Wireless)
- [PSDevWiki M.2 SSD](https://www.psdevwiki.com/ps5/M.2_SSD)
- [PSDevWiki Media](https://www.psdevwiki.com/ps5/Media)
- [PSDevWiki Bond (DualSense)](https://www.psdevwiki.com/ps5/Bond)
- [PSDevWiki DualSense](https://www.psdevwiki.com/ps5/DualSense)
- [PSDevWiki DualSense DFU Modes](https://www.psdevwiki.com/ps5/DualSense_DFU_Modes)
- [PSDevWiki DualSense HID Commands](https://www.psdevwiki.com/ps5/DualSense_HID_Commands)
- [PSDevWiki Bluray Drive Firmware](https://www.psdevwiki.com/ps5/Bluray_Drive_Firmware)
- [PSDevWiki CXD90060GG (APU)](https://www.psdevwiki.com/ps5/CXD90060GG)
- [PSDevWiki CXD90061GG (EMC/Southbridge)](https://www.psdevwiki.com/ps5/CXD90061GG)
- [PSDevWiki CXD90062GG (SSD Controller)](https://www.psdevwiki.com/ps5/CXD90062GG)
- [PSDevWiki MN864739 (HDMI)](https://www.psdevwiki.com/ps5/MN864739)
- [PSDevWiki XDPE14286A (VRM)](https://www.psdevwiki.com/ps5/XDPE14286A)
- [PSDevWiki MMIO Prototype](https://www.psdevwiki.com/ps5/MMIO_Prototype)
- [PSDevWiki Prototype Units](https://www.psdevwiki.com/ps5/Prototype_Units)
- [PSDevWiki PS5 Peripherals](https://www.psdevwiki.com/ps5/PS5_Peripherals)
- [PSDevWiki Southbridge Error Codes](https://www.psdevwiki.com/ps5/Southbridge_Error_Codes)
- [PSDevWiki AMD Platform Security Processor](https://www.psdevwiki.com/ps5/AMD_Platform_Security_Processor)
- [PSDevWiki Serial Database](https://www.psdevwiki.com/ps5/Serial_Database)
- [PSDevWiki PS Portal](https://www.psdevwiki.com/ps5/PS_Portal)
- [PSDevWiki PSVR2](https://www.psdevwiki.com/ps5/PSVR2)
- [PSDevWiki PSVR2 Update Format](https://www.psdevwiki.com/ps5/PSVR2_Update_Format)
- [PSDevWiki Jigkick Files](https://www.psdevwiki.com/ps5/Jigkick_Files)
- [PSDevWiki HD Camera](https://www.psdevwiki.com/ps5/HD_Camera)
