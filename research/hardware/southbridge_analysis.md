# PS5 Southbridge Firmware Analysis

## Overview

The PS5 southbridge is a multi-function embedded controller that manages low-level hardware initialization, power sequencing, peripheral connectivity, system monitoring, and debug infrastructure. The primary southbridge chip is the SIE CXD90061GG (based on MediaTek MT3613CT, codename **Salina**), a custom MediaTek design that integrates an ARM-based Embedded Micro Controller (EMC), an Embedded Application Processor (EAP) running FreeBSD 9.0-RELEASE, a Communication Processor for inter-component messaging, and the CP Box (CPBH-100) debug interface all into a single coherent subsystem. Two codename generations exist: **Tahoe** (first revision, James Bond theme) and **Salina** (first revision, Islands theme), with **Sierra** as a second revision. The southbridge is internally referred to as SysCon, and its firmware carries hex codenames `40000001-40000003` (Syscon), `C0000001` (emc_ipl), and `40030001` (cp_fw).

The southbridge sits between the AMD SoC (Oberon APU with AMD Platform Security Processor/PSP) and the system peripherals, acting as both a traditional southbridge (providing PCIe, SATA, USB, Gigabit Ethernet) and as a security-enforcing management controller. It communicates with the PSP over dedicated buses and shares responsibility for boot sequencing — the EMC handles power-on initialization while the PSP handles cryptographic boot verification. The southbridge has its own independent firmware stored on external serial flash (Winbond W25Q16JVNIM, 2 MB) and a larger NVS flash (Winbond 25Q256JVEQ, 32 MB), making it a persistent firmware island that survives OS reinstalls and power cycles.

For security researchers, the southbridge represents a critical but comparatively under-documented attack surface. Unlike the main APU boot chain (which benefits from extensive AMD public documentation and PS4 lineage), the southbridge firmware is a custom MediaTek design with proprietary firmware formats, undocumented IOCTL interfaces, and hardware debug interfaces that can bypass the main x86 security model. The CP Box debug accessory creates a separate trust domain — on TestKits, it can enable Assist Mode with relaxed security enforcement. The manufacturing function interface, if reachable from userland, could bypass signed module requirements entirely through IOCTLs like load-module (0x40184D01) and set-manu-mode (0xC0184D03).

## Southbridge Architecture

### EMC (Error Management Controller)

The EMC is the primary embedded microcontroller within the southbridge, built on the **CXD90061GG** hardware revision. It is an ARM-based controller responsible for low-level hardware initialization, power sequencing, thermal management, error detection, and system monitoring throughout the PS5's operational lifecycle. The EMC runs its own independent firmware that is completely separate from the main APU boot path — it is loaded from serial flash by the PSP-based Secure Loader and executes concurrently with (but independently of) the main x86 boot chain.

**Firmware Storage and Format:**
- Stored on serial flash (W25Q16JVNIM) at offset **0x4000** from the beginning of the flash
- Total length: **0x7E000 bytes** (~504 KB)
- Packaged as an **SLB2 (Secure Loader Block 2)** segment
- Extractable using the **blsunpack** tool
- Within the SLB2 segment, the file identified as **C0080001** contains the EMC version string
- EMC firmware hex codename: **C0000001** (emc_ipl)
- Protected by **AES-128-CBC encryption** with keys specific to each EMC revision (revision c0 documented)

**EMC Firmware Version History:**

| Version | PS5 FW | Platforms | SDK |
|---------|--------|-----------|-----|
| v0.7.6 | SDK 0.85.070 | Prototype/DevKit | 0.85.070 |
| v1.0.4 | 1.01-1.14 | TestKit, Retail | — |
| v1.2.3 | 2.XX | TestKit | — |
| v1.4.2 | 3.00 | Retail | — |
| v1.6.0 | 4.00 | TestKit | — |
| v1.8.2 | 5.00 | Retail | — |
| v1.8.3 | 5.50 | Retail | — |
| v1.14.3 | 9.20 | Retail | — |

**Power Management Role:**
The EMC controls the complete power-on and power-off sequencing. It manages:
- **PSW_MSOC_PGC**: Main SoC power good signal — enables the APU VRM (Infineon XDPE14286A)
- **SOC_PWROK**: SoC power OK signal indicating stable APU voltage
- **/SOC_VRM_HOT**: VRM overtemperature warning signal
- **/SOC_GPU_PCC**: GPU power compliance control
- **PSW_*** signals: Full power sequencing state machine
- Monitoring of 5V_MAIN, 1.8V_SOC_VDDA, 3.3V_VRM, 1.2V_VRM, 12V_MAIN power rails
- Detection of unexpected power cuts (error 0x80000009)

**Thermal Management Role:**
The EMC provides comprehensive thermal monitoring and response:
- **AUXADC** inputs for thermistor monitoring (motherboard temperature sensors)
- **/SOC_ALERT** signal: Thermal trip warning from SoC
- **/SOC_THERMTRIP** signal: Critical thermal shutdown from SoC
- **FAN_PWM** output: Variable speed fan control based on temperature readings
- Error code 0x80000001 covers both overheat and init APU error conditions
- Error code 0x80C00140 indicates APU freeze from GDDR6 data line issues

**Error Management Role:**
The EMC detects, logs, and reports hardware errors through a structured error code system. Error codes are categorized by subsystem:
- **0xFFFFFFFF**: No errors
- **0x80000001-0x808FFFFF**: APU, power, and kernel panic errors
- **0xC0000000-0xC0FFFFFF**: APU response and VRM controller failures
- **0xE0000000-0xE0000006**: Southbridge self-diagnosis failures (cannot read errors)
- Error log stored at NVS offset **0x1200** with **0x400 bytes** capacity
- EMC checksum validation toggle at NVS offset **0x1010**: FF = disabled

**EMC IPL Boot Process (within Secure Boot chain):**
1. The Secure Loader (on PSP) locates EMC firmware at serial flash offset 0x4000
2. Decrypts EMC firmware using revision-specific AES-128-CBC key (documented key for revision c0)
3. Extracts the SLB2 segment via blsunpack; finds C0080001 version file
4. Verifies EMC version matches expected revision
5. Transfers control to EMC for power-on initialization
6. EMC initializes system power rails, clocks, thermal monitoring
7. EMC signals completion and control returns to Secure Loader
8. Secure Loader then proceeds to load Hypervisor Loader

**Security Role:**
- The EMC checksum validation can be **disabled** (NVS offset 0x1010 = FF), which suppresses EMC firmware integrity checking — a potential debug escape path
- EMC UART output can be **enabled** (NVS offset 0x1012 = FF), providing serial debug output from the EMC
- EMC firmware IPL is encrypted with AES-128-CBC but the key for revision c0 is documented, meaning EMC IPL can be decrypted by researchers

### EAP (Error Application Processor)

The EAP is a separate application processor within the southbridge subsystem, running a full FreeBSD 9.0-RELEASE operating system on a Marvell PJ4C ARM core. The EAP handles higher-level debug and communication functions independent of the EMC's real-time control tasks.

**Hardware Specifications (from boot log):**
- **CPU**: Marvell PJ4C rev 2 (ARM), 500 MHz
- **DDR RAM**: 512 MB DDR3 at 800 MHz clock
- **Available memory**: ~473 MB (after firmware reservation)
- **EAP SDK Version**: 5.501.000
- **Sycorax Version**: 01.00.01.01
- **Subsystem ID**: 0x00040100 (Belize2 A0)
- **Boards ID**: 0x2001010101010501

**Peripherals and Devices (enumerated at boot):**
- UART serial console
- RTC (Real-Time Clock, 32.768 kHz crystal)
- SDHCI/SDIO host controller
- Belize GbE (Gigabit Ethernet via Salina southbridge)
- XHCI USB 3.0 controller
- I2C GPIO expanders (TCA9539)
- LED drivers (TLC59116)
- DECI5 debug interface

**Boot Sequence:**
- KBL (Kernel Boot Loader) boot → FreeBSD kernel loading → device enumeration → network configuration (DHCP) → CP firmware update check → service daemon startup
- Total boot time: ~**50 seconds** to "CP ready" state
- Services started: **emcd**, **uartd**, **disabler**, **DECI5s**, **DECI5**
- CP firmware update status checked at boot: status 0 = no update needed
- Ethernet MAC (from boot log example): 78:c8:81:d8:51:1b

**EAP Configuration via NVS:**
- EAP core startup flag at NVS offset **0x57**: 00 = enabled
- EAP UART flag at NVS offset **0x531F**: FF = disabled (UART output suppressed by default)
- DDR capacity byte at NVS offset **0x60**: 05 = 4 GiB, 07 = 16 GiB (indicates main PS5 memory size, not EAP local memory)
- Platform ID at NVS offset **0x00**: distinguishes CP Box (20 01 01 01 01 01 04 01) from Carlo CP prototype (10 01 02 01 02 01 02 02)
- MAC address at NVS offset **0x21**
- Serial number at NVS offset **0x4000**

**Key Ladder:**
- **EAP KBL**: AES-128-CBC keys for Kernel Boot Loader decryption
- **EAP Kernel SELF**: cipher key for AES-128-CBC decryption + RSA-3072 key pair for signature verification
- The Communication Processor maintains the complete key chain spanning EMC, EAP, and KBL domains, secured with HMAC-SHA1 integrity protection

### CP Box

The **CPBH-100** (CP Box) is a hardware debug accessory for PS5 TestKits that provides the primary development and debugging interface. It connects to the PS5 TestKit via USB-C and provides Ethernet connectivity, debug mode control, and Assist Mode capability.

**Hardware Description:**
- **Model**: CPBH-100
- **Connection**: USB-C to PS5 TestKit
- **Not hot-pluggable**: must be connected before PS5 power-on; PS5 checks for CP Box at boot and shows error if hot-plugged
- **CP Box can read PS5 info** (serial number, operating mode) even while PS5 is shut down — the CP Box has independent power

**Two Operational Modes:**
1. **Engineering Mode**: CP Box powered via USB-C to PS5 only. Basic debug connectivity.
2. **Normal Mode**: USB-C to portable HDD + Ethernet (DEV LAN) to host computer + USB-C to PS5. Full debug functionality including network access.

**Boot Mode Control:**
- **Without CP Box**: TestKits boot in **Release Mode** with full secure boot enforcement
- **With CP Box connected**: TestKit can switch to **Assist Mode** for debugging
- **Assist Mode persists** in memory even when the console is powered off
- PS5 power-on checks for CP Box presence; absence locks Release Mode

**Status LEDs (5 front-panel indicators):**
- **CP INIT**: Communication Processor initialization status
- **NETWORK INIT**: Network stack initialization
- **SPEED**: Ethernet link speed indicator
- **LINK/ACT**: Ethernet link and activity
- **STATUS**: General CP Box status

**Prototype CPB-K01 (earlier variant):**
- Uses **CXD90046GG** main chip
- Two separate CP systems: **recovery** + **normal operation**
- Dual-system architecture suggests debug infrastructure designed with redundancy for recovery scenarios

**VR Port:**
- USB-C port for PS VR2 activation
- Enabled after **cpupdate version 2700**

**UART Access:**
- The CP Box provides physical UART pins for accessing both **EMC** and **EAP** serial consoles
- This allows low-level debugging of both embedded controllers during development

### Communication Processor

The Communication Processor (CP) is the central routing and management component within the southbridge architecture. It handles inter-processor communication, manages the DECI5 debug protocol, and maintains the secure key chain spanning the entire southbridge firmware stack.

**Key Chain Management:**
The CP maintains the complete cryptographic key chain covering:
- **EMC keys**: AES-128-CBC IPL cipher keys for EMC firmware decryption
- **EAP KBL keys**: AES-128-CBC keys for Kernel Boot Loader decryption
- **EAP Kernel SELF keys**: AES-128-CBC cipher key + RSA-3072 key pair
- **HMAC-SHA1 integrity protection**: The entire key chain is protected by HMAC-SHA1, ensuring key material cannot be modified or corrupted during boot
- **UCMD authentication**: Key 2 (RSA) and Important Keys 3 used for UCMD (User Command) authentication

**DECI5 Protocol Routing:**
The CP acts as the central router for the DECI5 debug communication protocol:
- Manages shared memory nodes: DECI_SHM_NODE_MAGIC1_CP, MAGIC1_EAP, MAGIC1_MAIN, MAGIC1_MP3, MAGIC1_MP4, MAGIC1_SYCORAX
- Two channel types: **fix channels** (dedicated, point-to-point) and **ring channels** (buffered, multiple messages)
- Communication targets: EAP, MAIN (main x86 APU), MP3 (TEE), MP4, SYCORAX
- Supports mailbox interrupts and signal-based event handling (SIG0 through SIG3)
- Provides the low-level infrastructure for host-to-PS5 debug communication

**PSP Communication Protocol:**
The CP communicates with the AMD Platform Security Processor over dedicated internal buses. The protocol handles:
- Boot sequencing coordination (EMC readiness signaling)
- Key ring handoff from Secure Loader to EMC/EAP
- Runtime secure module dispatch coordination
- Error reporting and logging synchronization

## Hardware Debug Interfaces

### UART

The PS5 motherboard provides UART serial debug access through physical test points and via the CP Box service connectors. The UART interface enables low-level serial console access for debugging both the EMC and EAP processors.

**Available UART Connections:**
- **EMC UART**: Provides serial console output from the Error Management Controller
- **EAP UART**: Provides serial console output from the Embedded Application Processor (FreeBSD boot log)

**UART Configuration:**
- **EMC UART flag** at NVS offset **0x1012**: FF = enabled (default enabled)
- **EAP UART flag** at NVS offset **0x531F**: FF = disabled (default disabled)
- UART output from the EAP can be enabled by modifying the NVS configuration on the serial flash
- Specific baud rate and pinout details are documented on the Service Connectors page

**Known UART Data Captured:**
- Complete CP Box boot log (50 seconds to CP ready)
- FreeBSD kernel boot messages
- Device enumeration (USB, SDIO, I2C, GPIO)
- DHCP network configuration output
- CP firmware update status (status 0 = no update)
- Service daemon startup (emcd, uartd, disabler, DECI5s, DECI5)
- Error codes logged by EMC during boot

### DIPSW (DIP Switches)

The PS5 implements **256 dipswitches** (boot parameter flags) that control debug and development features. These are not physical switches but logical flag values initialized at boot from the CP Box MMIO region, gated by console type.

**Access Levels by Console Type:**
| Console Type | Access Level |
|-------------|-------------|
| Retail | None (0 switches accessible) |
| TestKit | Limited subset |
| DevKit | Most switches accessible |
| intdev DevKit | All 256 switches accessible |

**Documented Dipswitches:**

| Index | Name | Access | Purpose |
|-------|------|--------|---------|
| 0x00 | IsDevelopmentMode | — | Development mode flag (via libSceDipsw.sprx) |
| 0x02 | IsAssistMode | TestKit | Assist Mode enable |
| 0x18 | IsDisableRazor | — | Razor/GDK graphics optimization disable |
| 0x1E | GetDiableBinaryVersionCheckValue | — | Binary version check disable |
| 0x38 | isKeepProcess | — | Keep process on suspend/resume (via SceSysCore.elf) |
| 0x66 | Disable DSP | TestKit | Digital Signal Processor disable |
| 0x6D | IsCronos | — | Cronos mode (related to media/VR?) |
| 0x78 | GC Force Page Migration Window Enable | — | GPU page migration forcing |
| 0x9B | MP3 (TEE) Enable | — | Trusted Execution Environment enable |
| 0xB5 | Debug GC Enable | — | Debug GPU compute enable |
| 0xF1 | manu_mode related | — | Manufacturing mode control |

**Security Implications:**
- Dipswitch 0x02 (IsAssistMode) being TestKit-accessible means Assist Mode can be activated on TestKits, which may relax code signing enforcement
- Dipswitch 0x1E being able to disable binary version checks could allow mismatched firmware components to load
- Dipswitch 0xF1 being manufacturing mode-related is significant — if set, it could enable the manufacturing IOCTL interface (SceSblManuAuth)
- The MMIO region origin of dipswitches means they are loaded from CP Box firmware, not the main flash — hardware control point

### DECI5

DECI5 is the **Debug Communication Interface 5**, a proprietary protocol for host-to-PS5 debug communication. It uses shared memory nodes and supports multiple channel types for inter-processor communication.

**Architecture:**
- **Shared Memory Nodes**: Predefined shared memory regions identified by magic values:
  - `DECI_SHM_NODE_MAGIC1_CP` — Communication Processor
  - `MAGIC1_EAP` — Embedded Application Processor
  - `MAGIC1_MAIN` — Main x86 APU
  - `MAGIC1_MP3` — MP3 (TEE/Trusted Execution Environment)
  - `MAGIC1_MP4` — MP4 (additional co-processor)
  - `MAGIC1_SYCORAX` — Sycorax (CP Box KBL/Debug ROM)
- **Channel Types**:
  - **Fix channels**: Dedicated, point-to-point communication channels
  - **Ring channels**: Buffered channels supporting multiple messages with ring buffer semantics
- **Communication Targets**: EAP, MAIN, MP3, MP4, SYCORAX
- **Interrupt Mechanism**: Mailbox interrupts for asynchronous communication
- **Signal Handling**: SIG0 through SIG3 for event-based signaling

**Host Tools:**
- DECI5 is used by Sony's internal development tools for kernel debugging, memory inspection, and process control
- The CP manages data routing between all connected targets
- Shared memory node at MMIO: deci_shm_main0 at 0x880000000-0x89FFFFFFF (device 0.19 on pci1)

**Security Implications:**
- DECI5 provides direct access to kernel memory on DevKits/TestKits
- On retail hardware, DECI5 should be disabled or restricted, but the infrastructure remains in the firmware
- The protocol's shared memory mechanism is a potential attack surface if an attacker can inject messages into the DECI5 channel

### Manufacturing Functions

The PS5 exposes a set of manufacturing-related kernel functions through the **SceSbl** (Sce Secure Boot Loader) subsystem. These are accessed via **IOCTL calls** on dedicated kernel device entries.

**Manufacturing IOCTL Interface:**

| Function | IOCTL Code | Device | Purpose |
|----------|-----------|--------|---------|
| sceSblDriveSecureReset | — | — | Reset drive authentication for CS, debug, or QA modes |
| sceSblDriveAuthSetHostKeyVolatile | 0xC028530D | /dev/driveauth | Set volatile host key for drive authentication |
| sceSblDriveAuthGetPairingRequest | 0xC028530B | /dev/cd0 | Get drive pairing request data |
| sceSblDriveAuthSetPairingResData | 0xC028530C | /dev/driveauth | Set drive pairing response data |
| sceSblFttrmReadSector | 0xC0185301 | /dev/fttrm | Read FTTRM sector (film/TV tracking) |
| sceSblFttrmWriteSector | 0xC0185302 | /dev/fttrm | Write FTTRM sector |
| sceSblManuAuthLoadSecureModule | **0x40184D01** | /dev/manuauth | Load unsigned secure module (manu mode only) |
| sceSblManuAuthUnloadSecureModule | **0x40184D02** | /dev/manuauth | Unload secure module (manu mode only) |
| sceSblManuAuthGetManuMode | — | /dev/manuauth | Query if manufacturing mode is active |
| sceSblManuAuthSetManuMode | **0xC0184D03** | /dev/manuauth | Enable/disable manufacturing mode |
| sceSblSrtcSetFrequencyOffset | 0xC008530D | /dev/srtc | Set secure RTC frequency offset |

**Critical Discovery — the manu module (0x8002100B):**
The manufacturing module is a trusted service module loaded as part of the secure module infrastructure. If an attacker can reach the **set-manu-mode** IOCTL (0xC0184D03), they can enable manufacturing mode, which then allows:
- **load-module** (0x40184D01): Load unsigned secure modules, bypassing all signature verification
- **unload-module** (0x40184D02): Unload existing secure modules

The dipswitch **0xF1** (manu_mode related), if settable, could gate access to these IOCTLs. On retail hardware these should be restricted, but the interface surface exists in the kernel.

**QA-Related Manufacturing Functions:**
- sceSblDriveSecureReset supports three modes: **CS** (consumer/retail security), **debug** (development), **QA** (quality assurance)
- These mode transitions involve burning OTP fuses that are irreversible

### QA Flags

QA (Quality Assurance) flags are SELF-format authorization tokens that grant elevated privileges for development and testing on PS5 consoles.

**Token Format:**
- **Structure**: Header (0xC0 bytes) + Metadata (0x1E0 bytes) + Body (0x60 bytes)
- **Header Magic**: `54 14 F5 EE`
- **SELF Category**: 06 (QA Token SELF)
- **Body Encryption**: AES-CBC-CTS (Ciphertext Stealing variant of AES-CBC)
- **Body Signing**: HMAC-SHA256 + RSA 3096 (non-standard RSA key size)
- **Token Size**: 0x60 bytes total

**Body Fields:**
- **OpenPSID**: 0x10 bytes (16 bytes) — the console's Open PSID identifier
- **QA FLAGS**: 0x10 bytes (16 bytes) — flag values granting privileges
- **Padding**: Aligned to next boundary
- **SHA256HMAC**: Authentication tag

**Known Token:**
- **QAF Name**: `QAF_SYS_DEV_I` — System Developer I-level token
- **Validity Period**: 10 October 2019 to 4 October 2021 (725 days)
- This token was valid during the PS5 development period (pre-launch through first year of retail)

**Security Implications:**
- QA tokens are bound to a specific console's OpenPSID, preventing token sharing
- The AES-CBC-CTS encryption prevents token body tampering
- HMAC-SHA256 provides integrity verification
- RSA 3096 signing (non-standard, 387 bytes) provides authenticity
- If a QA token from an expired DevKit/TestKit can be recovered, it would grant elevated privileges on that specific console
- Token validity period means official Sony tokens from 2019-2021 have all expired, but the verification mechanism remains in firmware

### CP Box Service Connectors

The CP Box provides physical debug connectivity through a set of service connectors:

**Connector Types:**
- **USB-C**: Primary CP Box to PS5 TestKit connection
- **Ethernet (DEV LAN)**: Host computer connection in Normal Mode
- **USB-C (portable HDD)**: External storage for debug data in Normal Mode
- **USB-C (VR port)**: PS VR2 activation after cpupdate 2700
- **UART test pins**: Physical pins for EMC and EAP serial console access

**TestKit Features Available Through CP Box:**
- Assist Mode activation (relaxed security enforcement)
- DECI5 debug protocol over Ethernet
- Manufacturing mode (if dipswitch 0xF1 set and manu module accessible)
- Firmware update (cpupdate process)
- PS5 info reading (serial number, boot mode) while PS5 powered off
- VR function activation

**Physical Layout:**
- Pins for EMC UART (Tx/Rx)
- Pins for EAP UART (Tx/Rx)
- The physical pinout is documented on the PSDevWiki Service Connectors page

## Firmware Architecture

### CP Box Firmware

The CP Box runs a complete firmware stack independent of the main PS5 system software, with its own boot process, operating system, and update mechanism.

**Boot Process (from captured EAP boot log):**
1. **Power-on**: CP Box connected before PS5 power-on
2. **KBL Boot**: Sycorax (KBL ROM, version 01.00.01.01) loads and initializes hardware
3. **FreeBSD Kernel Load**: FreeBSD 9.0-RELEASE for ARM starts on Marvell PJ4C at 500 MHz
4. **Device Enumeration**: UART, RTC, SDHCI/SDIO, Belize GbE, XHCI USB 3.0
5. **DECI5 Initialization**: Debug communication interface starts
6. **I2C Setup**: GPIO expanders (TCA9539) and LED drivers (TLC59116) configured
7. **Network Configuration**: DHCP over DEV LAN Ethernet (MAC 78:c8:81:d8:51:1b)
8. **CP Firmware Update Check**: cpupdate verifies current firmware; status 0 = no update
9. **Service Startup**: emcd, uartd, disabler, DECI5s, DECI5 daemons start
10. **CP Ready**: ~50 seconds total boot time, Boards ID 0x2001010101010501

**File System Structure:**
- **C0080001**: Contains EMC version string
- **SLB2 format**: Secure Loader Block 2 segment packaging
- **40030001**: cp_fw firmware hex codename
- **Boot configuration**: Loaded from EAP NVS on the 32 MB Winbond 25Q256JVEQ serial flash

**Firmware Update (cpupdate):**
- CP Box firmware can be updated via the cpupdate mechanism
- Version 2700 enabled VR port functionality
- Firmware is distributed as part of system software updates
- Update files are likely signed and encrypted (format not publicly documented)
- Update status checked on every boot; returns 0 when no update pending

**Non-Volatile Storage (NVS):**
- Hardware: Winbond **25Q256JVEQ** (32 MB serial flash)
- NVS stored at flash offset **0x1C4000**
- Key offsets and fields:
  - **0x00**: Platform ID — CP Box = `20 01 01 01 01 01 04 01`, Carlo CP = `10 01 02 01 02 01 02 02`
  - **0x21**: MAC address
  - **0x57**: EAP core startup flag (00 = enabled)
  - **0x60**: DDR capacity (05 = 4 GiB, 07 = 16 GiB)
  - **0x1010**: EMC checksum validation flag (FF = disabled)
  - **0x1012**: EMC UART flag (FF = enabled)
  - **0x531F**: EAP UART flag (FF = disabled)
  - **0x1200**: Error log (0x400 bytes)
  - **0x4000**: Serial number

### EMC Firmware

The EMC firmware is responsible for power-on hardware initialization and runs on the CXD90061GG southbridge chip.

**Storage and Format:**
- Location: Serial flash (W25Q16JVNIM) offset **0x4000**
- Size: **0x7E000 bytes** (~504 KB)
- Format: **SLB2** (Secure Loader Block 2) segment
- Extraction: **blsunpack** tool
- Version file: **C0080001** within the SLB2 segment
- Codename: **C0000001** (emc_ipl)

**PUP Integration:**
EMC firmware is distributed as part of PS5 system software updates (PUP files). The EMC IPL is one of the firmware components that gets updated when new system software is installed. The version history shows EMC updates across all major firmware releases:
- Early prototypes: EMC v0.7.6 (SDK 0.85.070)
- Retail launch: EMC v1.0.4 (FW 1.01-1.14)
- Latest documented: EMC v1.14.3 (FW 9.20)

**Disassembly Status:**
- The EMC IPL is partially disassembled using the documented AES-128-CBC key for revision c0
- The SLB2 format can be unpacked with blsunpack
- The C0080001 version file confirms the EMC version
- Full disassembly is ongoing — the firmware binary is ~504 KB of ARM code

**Key Observations:**
- EMC firmware is separate from the CP Box firmware — EMC runs on the CXD90061GG chip while CP Box runs on a separate processor
- EMC controls physical hardware (power, fans, thermals) while CP Box handles debug/communication
- The EMC IPL encryption key for revision c0 is documented, allowing decryption of at least one EMC firmware version
- EMC firmware updates modify the serial flash at offset 0x4000, which is controlled by the Secure Loader during boot
- The EMC does NOT have its own network stack — all network communication goes through the CP Box / EAP

### Serial Flash (W25Q16JVNIM)

The PS5 uses a **Winbond W25Q16JVNIM** serial flash memory as the primary boot firmware storage. This is one of the most security-critical components in the system, as it stores the Secure Loader and EMC firmware.

**Hardware Specifications:**
- **Model**: Winbond W25Q16JVXXX family (specific variant: W25Q16JVNIM)
- **Capacity**: 16 Mbit = **2 MB**
- **Package**: 150mil SOIC (Small Outline Integrated Circuit, 8 pins)
- **Interface**: Standard SPI bus

**Pin Configuration and Signal Names:**

| Pin | Name | Signal | Function |
|-----|------|--------|----------|
| 1 | /CS | S50_SSB_SF_CS | Chip Select |
| 2 | DO(IO1) | S50_SSB_SF_SIO1 | Data Output / IO1 |
| 3 | /WP(IO2) | **3.3V_SS_PG1** | Write Protect / IO2 (tied to power good) |
| 4 | GND | GND | Ground |
| 5 | DI(IO0) | S50_SSB_SF_SIO0 | Data Input / IO0 |
| 6 | CLK | S50G_SSB_SF_SCLK | Serial Clock |
| 7 | /HOLD or /RESET(IO3) | **3.3V_SS_PG1** | Hold/Reset / IO3 (tied to power good) |
| 8 | VCC | 3.3V_SS_PG1 | Power Supply |

**Critical Security Design — Write Protection:**
- Pin 3 (/WP — Write Protect) is tied to **3.3V_SS_PG1** (SoC Power Good signal)
- Pin 7 (/HOLD) is also tied to 3.3V_SS_PG1
- This means the serial flash write protection is gated by the SoC power good signal — the SoC must be in a valid power state for writes to be possible
- This hardware-level write protection prevents unauthorized SPI flash modifications without proper power sequencing

**Memory Layout:**

| Offset | Size | Content |
|--------|------|---------|
| 0x0000-0x07FF | 2 KB | Boot configuration parameters and unused space |
| **0x0800** | **0x400** | **Secure Loader IPL header** (magic: E4 DB 7C 02) |
| **0x0C00** | ~0x631D0 | **Secure Loader encrypted body** (dual-layer AES-CBC) |
| **0x4000** | **0x7E000** | **EMC firmware** (SLB2 segment, ~504 KB) |

**Dumping via Raspberry Pi:**
- The serial flash is readable via Raspberry Pi GPIO SPI interface
- Standard flashrom tool has W25Q16JVXXX support
- Physical access to motherboard SPI bus signals is required
- The SPI signals are motherboard-accessible and can be probed with logic analyzers

**Write Protection Analysis:**
- Pin 3 (/WP) tied to 3.3V_SS_PG1 means the flash is write-protected when SoC power is unstable
- When PS5 is powered down, /WP may float or be at GND, potentially allowing writes
- An attacker with physical access could:
  - Desolder the flash and read/write it in an external programmer (bypassing /WP entirely)
  - Use a Raspberry Pi to dump the flash contents (read-only without write access)
  - Use a clip-on SOIC programmer to read/modify contents while the system is off

**Configuration Modification Attack Vector:**
While modifying the Secure Loader would break RSA-4096 signatures (making it undetectable but also unbootable), modifying NVS data is a viable attack:
- NVS stored on the **32 MB** Winbond 25Q256JVEQ (separate flash, not this one)
- But the EMC firmware can be modified if the AES-128-CBC encryption key is known
- EMC firmware modifications would persist across power cycles and OS reinstalls

## Security-Relevant Components

### Key Chain

The PS5's southbridge key management is a hierarchical system where the Communication Processor maintains the complete key chain spanning EMC, EAP, and KBL domains. The entire chain is protected by **HMAC-SHA1** integrity verification.

**EMC Key Domain:**
- **EMC IPL Cipher Key**: AES-128-CBC key for EMC firmware decryption
- Documented key exists for EMC revision **c0**
- Each EMC firmware revision has unique key material, preventing cross-revision decryption
- EMC version-specific keys are derived from the key chain

**EAP Key Domain:**
- **KBL keys**: AES-128-CBC keys for Kernel Boot Loader decryption
- **Kernel SELF cipher key**: AES-128-CBC key for kernel binary decryption
- **Kernel SELF RSA-3072**: RSA-3072 key pair for kernel SELF signing
- The RSA-3072 public key is embedded in the Hypervisor Loader for verification

**Communication Processor Key Chain:**
- Maintains the complete set of EMC/EAP/KBL keys
- **HMAC-SHA1** integrity check across the entire chain
- Key chain is loaded from the Secure Loader metadata region (offset 0x140 in the IPL header)
- Passed through boot stages: Boot ROM → Secure Loader → Hypervisor Loader → Kernel
- **UCMD Authentication**: Key 2 (RSA) and Important Keys 3 provide authentication for User Commands

**ROM Key Seeds (stored in PSP Boot ROM):**
- Multiple 256-byte keyseed sets (Key 2 through Key 9)
- Key 2: RSA key pair for boot-time authentication and UCMD verification
- Key 3: Additional RSA keys for UCMD authentication (backup/alternative path)
- Keys 4-9: Additional keyseed sets for various boot and runtime security functions
- These seeds are fused into silicon and cannot be modified after manufacturing

**Key Relationship to PSP Key Ring:**
The Communication Processor key chain is related to but distinct from the PSP's internal key ring:
- The PSP manages RSA keys (ROM Keys 2-9) for signature verification
- The CP manages the EMC/EAP/KBL key chain for firmware decryption
- Both systems are required for a successful boot: PSP verifies signatures, CP provides decryption keys
- The HMAC-SHA1 on the CP key chain ensures the key material reaches the Hypervisor Loader intact

### Secure Boot Integration

The southbridge plays a critical role in the PS5 secure boot chain, participating at multiple stages from serial flash storage through EMC initialization to kernel loading.

**Stage 1 — Secure Loader:**
The Secure Loader (IPL) is stored on the serial flash at offset 0x800 and is the first mutable component verified. Its header structure:
- Magic: `E4 DB 7C 02` (4 bytes at offset 0x00)
- Header size: 0x400 bytes (little-endian at offset 0x04)
- Entry point: 0xB0 (little-endian at offset 0x08)
- Body size: varies (e.g., 0x631D0, at offset 0x0C)
- SHA-256 of decrypted body: at offset 0x20 (32 bytes)
- Security revision: at offset 0x11C (4 bytes, anti-rollback)
- Revision nonce: at offset 0x120 (32 bytes, SHA-256 of nonce seed)
- RSA-4096 signature: at offset 0x200 (512 bytes, covers header 0x00-0x1FF)
- Encrypted body: at offset 0x400 (dual-layer AES-128-CBC)

The Secure Loader is verified by the PSP Boot ROM using RSA-4096 against ROM Key 2. After verification, the body is decrypted (Layer 1: global firmware key, Layer 2: revision nonce-derived key), then SHA-256 verified.

**Stage 2 — EMC Initialization:**
After Secure Loader decryption, the EMC firmware is located at serial flash offset 0x4000:
- Decrypted using revision-specific AES-128-CBC key
- Extracted as SLB2 segment using blsunpack
- Version validated from C0080001 file
- EMC performs power-on initialization and signals completion
- Control returns to Secure Loader

**Stage 3 — Hypervisor Loader:**
- Located within the Secure Loader decrypted body
- Verified using the same RSA-4096 chain
- Security revision and revision nonce re-validated
- Key rings passed from Secure Loader metadata

**Stage 4 — Kernel:**
- Kernel SELF stored on NAND flash, not serial flash
- Verified using EAP RSA-3072 (Hypervisor Loader verifies)
- Decrypted using EAP AES-128-CBC key from KBL chain
- Communication Processor validates entire EMC/EAP/KBL key chain via HMAC-SHA1
- Final SHA-256 integrity check before execution

**Anti-Rollback Integration:**
The Security Revision system at header offset 0x11C is checked against OTP fuses:
- Value burned into OTP fuses monotonically increases with each firmware update
- Secure Loader boot is blocked if security revision < OTP minimum
- Security revision values: 0x00000001 (FW 0.85-1.XX) through 0x0003FFFF (FW 11.00+)
- Revision nonce (SHA-256 at offset 0x120) prevents cross-revision decryption even if security revision check is bypassed
- Seven documented revision nonces for revisions 0xA0 through 0x100

**Serial Flash Protection:**
- /WP pin tied to 3.3V_SS_PG1 (SoC Power Good) — write protection is hardware-gated
- /HOLD pin also tied to 3.3V_SS_PG1
- The Secure Loader RSA-4096 signature prevents undetected modification
- The dual-layer AES encryption prevents decryption without both global and revision-specific keys

### AMD PSP Interface

The AMD Platform Security Processor (PSP, codename **Ariel**) and the southbridge have a cooperative relationship in the PS5 architecture.

**PSP Role:**
- Executes the PS5 Boot ROM at power-on (immutable mask ROM)
- Handles all cryptographic operations: RSA-4096/RSA-3072 signature verification, AES-128-CBC encryption/decryption, SHA-256 hashing, HMAC-SHA1 verification
- Manages secure key rings (ROM Keys 2-9)
- Provides a trusted execution environment for secure modules (0x8002xxxx services)
- Monitors system behavior for suspicious activity during boot and runtime
- Controls access to OTP fuses for security revision programming
- MMIO region: sbl0 at 0xE0500000-0xE05FFFFF and 0xE06C6000-0xE06C7FFF (device 0.2 on pci2, codename Ariel)

**PSP Southbridge Communication Protocol:**
- **Boot coordination**: PSP reads Secure Loader from serial flash, decrypts EMC firmware, hands off to EMC for initialization
- **Key ring handoff**: PSP passes key rings (including CP key chain) through the Secure Loader metadata
- **Secure module dispatch**: PSP executes secure modules (authmgr, kms, pup, manu, etc.) that the southbridge may need to call for authentication
- **Error reporting**: Southbridge error codes are reported through the PSP's monitoring system

**Shared Responsibilities:**
| Function | PSP | Southbridge |
|----------|-----|-------------|
| Boot ROM execution | Primary (immutable) | — |
| Secure Loader verification | RSA-4096 verification | — |
| EMC firmware decryption | AES-128-CBC decryption | Execution |
| Power sequencing | — | Primary (EMC) |
| Thermal monitoring | — | Primary (EMC) |
| Key chain management | ROM Keys 2-9 | CP key chain (EMC/EAP/KBL) |
| Secure module execution | Module hosting | Module consumer |
| Debug interface | — | Primary (CP Box / EAP) |
| Kernel verification | RSA-3072 verification | Key chain validation |

**Trust Boundaries:**
The trust boundary between PSP and southbridge is established through:
1. **Cryptographic**: EMC firmware is encrypted with AES-128-CBC; PSP provides decryption
2. **Physical**: Southbridge is a separate chip (CXD90061GG / MT3613CT) from the APU (CXD90060GG)
3. **Operational**: PSP boots first, validates Secure Loader, then enables EMC — EMC cannot execute before PSP authorization
4. **Key isolation**: PSP ROM keys never leave the PSP; CP key chain is integrity-protected but decryption happens on PSP

## Known Vulnerabilities and Attack Surface

### SPI Flash Manipulation

The serial flash (W25Q16JVNIM) is one of the most accessible physical attack surfaces on the PS5 motherboard.

**Physical Access Vectors:**
- The flash is in a standard 150mil SOIC-8 package — clip-on programmers (SOIC-8 clip + Raspberry Pi) can dump contents without desoldering
- SPI bus signals are directly accessible on the motherboard
- Standard flashrom tool supports the W25Q16JVXXX series
- Dumping does not require system power (flash can be powered by programmer)

**Modification Risks:**
- **Secure Loader modification**: Would break RSA-4096 signature — boot would fail, detectable but system would be unbootable
- **EMC firmware modification**: AES-128-CBC encrypted; if key is known, modified EMC firmware could be written back
  - Modified EMC firmware could alter power sequencing, thermal thresholds, error reporting
  - Could disable fan control, leading to thermal damage
  - Could disable EMC checksum validation (NVS offset 0x1010 = FF already disables)
- **NVS modification**: Platform ID, MAC address, DDR capacity, UART flags, serial number could all be modified
  - Changing platform ID could affect console type detection
  - Enabling EAP UART (offset 0x531F) would expose FullBSD debug console
  - Disabling EMC checksum validation (offset 0x1010) suppresses firmware integrity errors

**Write Protection Bypass:**
- Pin 3 (/WP) tied to 3.3V_SS_PG1 — write protection is active when SoC has power
- Physical bypass options:
  1. Desolder flash and program externally (bypasses /WP entirely)
  2. Lift pin 3 and connect to GND to force write enable
  3. Use chip-off programmer for full flash access
  4. Hot-glitch the 3.3V_SS_PG1 line during flash write

**Configuration Modification Attack:** (most realistic)
Rather than modifying the Secure Loader (which breaks signatures), an attacker could:
1. Dump the serial flash (using Raspberry Pi, read-only via SPI)
2. Analyze the NVS and EMC firmware for weaknesses
3. If EMC encryption key is known, craft modified EMC firmware
4. Write modified firmware back using chip-off programming
5. The modified EMC firmware would persist across PS5 power cycles and OS reinstalls
6. EMC firmware modifications are NOT detected by main OS security checks (the OS does not verify EMC firmware after boot)

### CP Box Protocol Attacks

The CP Box debug interface, while limited to TestKits, reveals the debug infrastructure design and potential attack paths.

**USB-C Interface Attack Surface:**
- The CP Box communicates over USB-C, which is also a standard PS5 port
- Protocol enumeration, fuzzing USB-C communications could reveal undocumented commands
- The CP Box can read PS5 info (serial, mode) while PS5 is shut down — this requires independent power from the PS5
- Assist Mode persistence (survives power-off) means state is stored in non-volatile memory

**TestKit Authentication Bypass:**
- Without CP Box: TestKit boots in Release Mode (full security)
- With CP Box: TestKit can enter Assist Mode (relaxed security)
- The CP Box acts as a hardware authentication token — if the CP Box handshake could be emulated, a retail console might be tricked into Assist Mode
- CP Box presence check at boot could potentially be bypassed by modifying NVS or dipswitch values

**Assist Mode Escalation:**
- Assist Mode (dipswitch 0x02, TestKit-accessible) enables debug capabilities
- Combined with dipswitch 0x1E (binary version check disable), could allow loading unsigned firmware
- Assist Mode + manufacturing mode (dipswitch 0xF1) could enable the full manu IOCTL set

**Command Injection:**
- The CP Box DECI5 protocol supports mailbox interrupts and signal handling
- Malformed DECI5 messages could potentially trigger buffer overflows in the communication processor
- The EAP runs FreeBSD 9.0-RELEASE — an older FreeBSD version with known vulnerabilities
- Network service enumeration on the DEV LAN interface could reveal exploitable services

**cpupdate Attack Surface:**
- Firmware update process checks for new firmware on every boot
- Update distribution mechanism could be intercepted or replayed
- Version 2700 enabled VR functionality — suggesting updates gate new features
- Update file format is not publicly documented

### Manufacturing Mode

The manufacturing function interface is one of the highest-value attack targets on the PS5, as it can bypass all code signing requirements.

**IOCTL Surface (if reachable):**

| IOCTL | Code | Function | Impact |
|-------|------|----------|--------|
| sceSblManuAuthSetManuMode | **0xC0184D03** | Enable manufacturing mode | Gates all other manu functions |
| sceSblManuAuthLoadSecureModule | **0x40184D01** | Load unsigned secure module | **Bypasses all signature verification** |
| sceSblManuAuthUnloadSecureModule | **0x40184D02** | Unload secure module | Can disable security modules |
| sceSblManuAuthGetManuMode | — | Query manufacturing mode status | Reconnaissance |

**How to Reach Manufacturing Mode:**
Requirements for reaching the manu IOCTLs:
1. **Dipswitch 0xF1**: must indicate manu_mode enabled (set in firmware/MMIO config)
2. **Console Type**: DevKit/intdev DevKit have access; TestKit possibly; Retail unlikely
3. **SceSbl module dispatch**: manu module (0x8002100B) must be loaded

**If Reachable, Attack Impact:**
- **load-module (0x40184D01)**: Load any unsigned SELF as a trusted secure module
  - Could load a custom kernel that disables all security
  - Could load a custom hypervisor
  - Could load a persistent firmware backdoor (e.g., a module that re-enables on every boot)
- **unload-module (0x40184D02)**: Unload existing security modules
  - Could unload authmgr (0x80021000) — disable authentication
  - Could unload pup (0x80021002) — disable PUP update verification
  - Could unload sysveri (0x80021009) — disable system verification
  - Could unload npdrm (0x80021006) — disable DRM enforcement
- **set-manu-mode (0xC0184D03)**: Persist manufacturing mode across reboots

**Related Manufacturing IOCTLs (broader impact):**
- sceSblDriveSecureReset: Reset drive authentication — could bypass disc drive verification
- sceSblDriveAuthSetHostKeyVolatile (0xC028530D): Set drive authentication host key
- sceSblDriveAuthGetPairingRequest (0xC028530B): Extract drive pairing data
- sceSblDriveAuthSetPairingResData (0xC028530C): Set pairing response

### Southbridge Firmware Rootkit

The most significant security concern is the potential for an undetectable firmware-level implant in the southbridge firmware that persists across power cycles and OS reinstalls.

**Persistence Vectors:**
1. **EMC Firmware** (serial flash offset 0x4000, 504 KB):
   - Modified EMC firmware survives power cycles
   - Not checked by OS after boot — OS trusts the EMC
   - Could implement malicious power sequencing, thermal throttling, error suppression
   - Could add a backdoor that triggers on specific conditions (e.g., specific USB device insertion)

2. **EAP Firmware** (CP Box / EAP flash):
   - FreeBSD 9.0-RELEASE environment provides full OS capabilities
   - Network access (DEV LAN) for exfiltration
   - Independent storage (512 MB DDR3, 32 MB NVS flash)
   - Could implement network-based command and control

3. **NVS Configuration** (32 MB Winbond 25Q256JVEQ):
   - UART enables/disables
   - Checksum validation flags
   - Platform ID manipulation
   - Error log manipulation (suppress detection)

**Rootkit Capabilities:**
- **Persistence**: Survives full OS reinstall, hard drive replacement, factory reset
- **Stealth**: EMC firmware is never inspected by running OS
- **Hardware control**: Can modify fan curves, thermal thresholds, power sequencing
- **Error suppression**: Can prevent error codes from being logged (error 0xE0000001-0xE0000006 = southbridge cannot read errors)
- **Detection resistance**: Requires physical SPI access to detect — no software-based detection possible from main OS

**Rootkit Limitations:**
- Requires physical access for initial installation (SPI flash programming)
- Cannot modify main APU boot chain (Secure Loader signatures prevent this)
- Cannot bypass kernel-level security from EMC alone (needs coordinate with main OS exploit)
- EMC code space limited to ~504 KB

**Rootkit Detection Challenge:**
- Cannot be detected by any software running on the main PS5 OS
- EMC firmware dump and comparison against known-good hash is the only reliable detection method
- Requires desoldering or clip-on programming of serial flash
- Even then, a sophisticated rootkit could present clean firmware when the flash is read (SPI bus man-in-the-middle)

## Research Gaps

The following areas require further investigation:

**EMC Firmware Disassembly:**
- Full disassembly of EMC IPL firmware (C0000001 / SLB2 format) has not been completed
- The complete IOCTL interface for EMC control is undocumented
- EMC firmware update mechanism within PUP files is not fully reverse-engineered
- SLB2 format specifications beyond blsunpack capability need documentation

**CP Box Protocol Documentation:**
- The DECI5 protocol specification is incomplete — message formats, channel IDs, and signal behavior need reverse engineering
- cpupdate file format and signing mechanism are unknown
- CP Box authentication handshake with PS5 is not documented
- The DEV LAN network services exposed by EAP are not fully enumerated

**Manufacturing Function Reachability:**
- It is unknown whether the manu IOCTLs (0xC0184D03, 0x40184D01, 0x40184D02) are reachable from userland on any console type
- The relationship between dipswitch 0xF1 and manu_mode activation needs verification
- The manu module (0x8002100B) dispatch mechanism and authentication requirements are undocumented
- Whether OTP fuse modifications can enable manufacturing mode post-retail is unknown

**UART and Debug Interface Documentation:**
- Complete pinout for EMC and EAP UART on all motherboard revisions is needed
- EAP UART boot log capture at full verbosity has not been documented
- UART baud rate and protocol configuration details need verification
- Whether UART access is available on retail units (with resistor/pin modifications) is unclear

**Key Chain Analysis:**
- The HMAC-SHA1 key chain structure used by the Communication Processor needs full reverse-engineering
- EMC revision-specific key derivation algorithm is unknown (only revision c0 key documented)
- Key chain handoff protocol between PSP and CP during boot is undocumented
- Whether the key chain can be dumped at runtime through EAP/CP Box access is unknown

**Serial Flash Full Layout:**
- The complete memory layout of the 2 MB W25Q16JVNIM has not been fully documented
- Areas between Secure Loader body end (0x400 + body_size) and EMC firmware start (0x4000) are unknown
- The 32 MB Winbond 25Q256JVEQ full layout beyond NVS offsets needs mapping
- Write protection behavior under various power states needs empirical testing

**Physical Attack Vectors:**
- Voltage/clock glitching of the southbridge SPI interface has not been attempted publicly
- EMC firmware rollback to an older (potentially vulnerable) version has not been tested
- Whether downgrading serial flash contents triggers error handling that could be exploited is unknown
- Side-channel analysis of EMC cryptographic operations (if any) has not been performed

**Secure Module Interface with Southbridge:**
- Which secure modules (0x8002xxxx) communicate with the southbridge is unknown
- The interface between SceSbl and EMC for hardware security operations needs documentation
- Whether secure module loading requires southbridge involvement is unclear
- The OTP fuse programming path (otpctrl, 0x80021016) and its relationship to southbridge error codes needs analysis

## Relationships

- [[hardware_overview]] — southbridge (CXD90061GG / MT3613CT, codename Salina) is a key hardware component providing peripheral connectivity, power management, and debug interfaces
- [[boot_chain]] — southbridge participates in boot stages 1-2, storing the Secure Loader and EMC firmware on serial flash, executing EMC initialization before hypervisor load
- [[secure_boot]] — southbridge provides the cryptographic key chain (EMC/EAP/KBL) with HMAC-SHA1 integrity protection, integrated with PSP-verified boot
- [[security_model]] — CP Box authentication, dipswitch access control, manufacturing functions, and QA flags define the privilege hierarchy for debug access
- [[attack_surface]] — southbridge debugging interfaces (UART, DIPSW, DECI5, CP Box), serial flash SPI bus, manufacturing functions, and firmware persistence provide critical attack surfaces

## References

- https://www.psdevwiki.com/ps5/CP_Box — CP Box hardware debug accessory specifications
- https://www.psdevwiki.com/ps5/CP_Box_Boot_Process — Complete EAP boot log with FreeBSD 9.0
- https://www.psdevwiki.com/ps5/CP_Box_Non_Volatile_Storage — NVS layout on 32 MB serial flash
- https://www.psdevwiki.com/ps5/CP_Box_Service_Connectors — UART pin access points
- https://www.psdevwiki.com/ps5/Debugging — GDB debug server setup for payload development
- https://www.psdevwiki.com/ps5/DECI5 — Debug Communication Interface protocol details
- https://www.psdevwiki.com/ps5/Dipsw — 256 dipswitch boot parameters and access levels
- https://www.psdevwiki.com/ps5/Manufacturing_Functions — Manufacturing IOCTL codes and interfaces
- https://www.psdevwiki.com/ps5/QA_Flags — QA token SELF format and cryptography
- https://www.psdevwiki.com/ps5/UART — UART serial debug interface overview
- https://www.psdevwiki.com/ps5/EMC — EMC firmware versions and serial flash extraction
- https://www.psdevwiki.com/ps5/25Q16JVNIM — Winbond serial flash pinout and specifications
- https://www.psdevwiki.com/ps5/Serial_Flash — Serial flash dumping via Raspberry Pi
- https://www.psdevwiki.com/ps5/Southbridge_Error_Codes — Complete error code reference
- https://www.psdevwiki.com/ps5/AMD_Platform_Security_Processor — PSP security processor overview
- https://www.psdevwiki.com/ps5/XDPE14286A — Infineon APU VRM controller
- https://www.psdevwiki.com/ps5/MN864739 — Panasonic HDMI retiming chip (FLAVA)
- https://www.psdevwiki.com/ps5/MT3613CT — MediaTek southbridge chip identification
- https://www.psdevwiki.com/ps5/Secure_Loader — Secure Loader IPL header structure and security revisions
- https://www.psdevwiki.com/ps5/Secure_Modules — Secure module IDs (0x8002xxxx)
- https://www.psdevwiki.com/ps5/Keys — Cryptographic key material including EMC, EAP, and CP keys
