# PS5 System Overview

## Overview

The PlayStation 5 is a ninth-generation video game console developed by Sony Interactive Entertainment, built around a custom system-on-chip combining an AMD Zen 2 CPU (8 cores, 16 threads at variable frequency up to 3.5 GHz) and an AMD RDNA 2 GPU (36 compute units at variable frequency up to 2.23 GHz, delivering 10.28 TFLOPS). The system contains 16 GB of GDDR6 memory (448 GB/s bandwidth) and a custom 825 GB NVMe SSD with a dedicated controller achieving 5.5 GB/s raw throughput (8-9 GB/s compressed). The Tempest 3D AudioTech engine provides hardware-accelerated spatial audio. Networking is handled by Wi-Fi 6 (802.11ax) and Bluetooth 5.1. Video output supports HDMI 2.1 with VRR, HFR up to 120 Hz, and HDR10. A 4K UHD Blu-ray drive is included in the standard model.

The software stack is deeply layered with defense-in-depth: a hardware root of trust anchors secure boot, a custom Type-1 hypervisor enforces game-to-game and game-to-system isolation, a FreeBSD-derived kernel mediates resource access, and the Orbis OS system software layer manages application runtime with sandboxed execution environments. Game processes cannot directly access system memory, other game partitions, or persistent storage without crossing privilege boundaries. This layered architecture means PS5 homebrew enablement requires chaining exploits across multiple privilege domains (usermode, kernel, hypervisor), unlike PS4 where kernel access alone was sufficient.

The system software (firmware) is distributed via PS5UPDATE.PUP files hosted on SIE content delivery networks. Version information is published through an `updatelist.xml` file. The version format follows `YY.SS-MM.mm.nn.nn-UU.UU.UU.U.b` where YY = last two digits of build year, SS = semester (01-02 before 2024, per-year counters 03-07 since 2024), MM = major, mm = minor, nn.nn = extended minor, UU.UU.UU.U = unknown fields, and b = 0/1 (1 for CEX/retail). Short display format is `MM.mm.nn`. PUP download URLs follow the pattern `http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/<OBFUSCATED_STRING>/image/<YYYY_MMDD>/<TYPE>_<SHA256>/PS5UPDATE.PUP?dest=<TLD>` with obfuscated string `tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6`. Three PUP types exist: `system` (full system update), `recovery` (recovery mode), and `system_ex` (system extension). Region EXTLD prefixes include fjp01 (JP), fus01 (US), feu01 (EU), pc, djp01, dus01, deu01.

As of June 2026, the latest retail firmware is version 13.40 (build 26.04-13.40.00.02, released 2026-05-28). The firmware history spans from the initial 1.00 (build 20.01-01.00.00.37, 2020-05-21) through 13 major versions. TestKit firmware versions range from 0.95.00.44 through 2.30.00.05. DevKit versions range from 0.83.00.20 through 2.30.00.05. PUP files are archived on the Internet Archive, Midnight Archive, Softpedia, Darthsternie, and DarkSoftware repositories. DevKit/testkit PUPs are also available on Yandex.

The security architecture shares conceptual lineage with PS4 but introduces significant hardening at every layer. The hypervisor is a distinct layer separating the kernel from direct hardware access. Game operating systems run in virtual machine partitions managed by the hypervisor. The system software itself runs as a privileged application set rather than a monolithic OS. PUP watermarking (old format with DevNet user ID, org name, company name, download date, IP address; new format with traceable serial number) enables forensic tracking of leaked firmware to the authorized developer who downloaded it.

## System Architecture Layers

### Hardware Layer

The PS5 hardware is anchored by a custom SoC (codenamed Oberon in initial retail units, Oberon Plus in later CFI-12xx revisions) integrating the CPU, GPU, I/O controller, and security coprocessors on a single die. The CPU implements 8 Zen 2 cores with simultaneous multithreading (16 threads), each core with 32 KB L1 instruction cache, 32 KB L1 data cache, 512 KB L2 cache, and a shared 4 MB L3 cache. The GPU contains 36 RDNA 2 compute units operating at variable frequency up to 2.23 GHz, delivering 10.28 TFLOPS peak performance with hardware-accelerated ray tracing. The GPU uses a tile-based rendering architecture.

Memory consists of 16 GB of GDDR6 across a 256-bit bus with 448 GB/s peak bandwidth. The memory subsystem is unified — CPU and GPU share the same pool. The storage subsystem is the most distinctive hardware feature: a custom 825 GB NVMe SSD with a dedicated 12-channel flash controller. Raw throughput is 5.5 GB/s (sequential reads) and compressed throughput reaches 8-9 GB/s using the Kraken compression engine via the I/O co-processor. The SSD connects via four PCIe 4.0 lanes. A dedicated I/O co-processor handles decompression (Kraken, zlib) and data management offload, reducing CPU overhead for streaming game assets.

The VBIOS is AMD ATOMBIOSBK with build strings like `AMDObrGeneri.2132099 .518911 . 06/15/20,23:33:14`. This firmware initializes the GPU hardware during boot. The HDMI 2.1 output supports Variable Refresh Rate (VRR), High Frame Rate (HFR) up to 120 Hz for 1080p and 1440p, 4K up to 120 Hz, and 8K output. The Tempest 3D AudioTech engine uses hundreds of audio sources with hardware-accelerated HRTF (Head-Related Transfer Function) processing for spatial audio. The 4K UHD Blu-ray drive reads discs at 2x CAV (36 MB/s for BD-ROM).

### Firmware Layer

The firmware layer is the lowest level of executable code, responsible for hardware initialization and establishing the root of trust. The Boot ROM is etched into the SoC's mask ROM — it is immutable and cannot be updated without a hardware revision. On power-on, the Boot ROM is the first code executed. It initializes minimal hardware (CPU caches, SRAM for stack) and validates the Secure Loader using hardware-rooted cryptographic keys stored in one-time programmable fuses.

The Secure Loader (second-stage bootloader) is loaded after Boot ROM verification. It initializes system DRAM, sets up the Trusted Execution Environment for secure operations, and validates subsequent boot stages. Secure Loader build strings contain sys-revision and sys-repository-path information, e.g., `Oberon-KDE 2021/04/06 05:22 releases/03.00 171343 pprbld-w54.build.rd.scei.sony.co.jp`. The Secure Loader also handles anti-rollback enforcement — it checks firmware version against stored version info and refuses to load firmware older than the currently installed version. The firmware version is stored in the registry at key `0x1100000` (SCE_REGMGR_ENT_KEY_REGISTRY_version) and the last installed version at `0x1080000` (SCE_REGMGR_ENT_KEY_REGISTRY_lastver).

### Hypervisor Layer

The hypervisor is a custom Type-1 hypervisor that partitions system hardware into isolated virtual machines. It sits directly above the firmware layer and beneath all operating system instances (system kernel and game kernels). The hypervisor enforces memory isolation between partitions through hardware IOMMU configuration, controls interrupt routing, and manages DMA remapping. Each partition receives a virtualized view of hardware resources.

The hypervisor is the most protected component of the PS5 security model. It is loaded by the Secure Loader after cryptographic verification. Its code runs at the highest privilege level (EL2 in ARM terms, but using AMD-V on the x86-64 based system). The hypervisor manages:
- **Memory partitioning**: Each VM receives isolated physical memory regions. DMA from devices is restricted to assigned memory regions via IOMMU
- **Interrupt management**: Interrupts are routed to the appropriate VM's virtual interrupt controller
- **Device pass-through**: Selected hardware devices are assigned to specific VMs with DMA remapping
- **VM lifecycle**: The hypervisor controls VM creation, destruction, and context switching

Hypervisor exploitation (via TMR vulnerabilities discovered by fail0verflow, flatz's hypervisor exploit, or Byepervisor by Specter) is the most valuable attack vector because hypervisor access disables security monitoring across all guest VMs. Full HEN capabilities require hypervisor access. The PS4 emulation layer runs as a hypervisor guest, which is why the hypervisor exploit was necessary for early PS4 compatibility analysis firmware.

### Kernel Layer

The kernel is derived from FreeBSD, continuing the lineage from PS3's Cell OS and PS4's Orbis kernel. It provides core OS services: process management with priority scheduling, virtual memory with demand paging, multiple file systems (UFS, PFS for PlayStation File System, exFAT), threading (pthreads), inter-process communication (pipes, sockets, shared memory), and device drivers. The kernel runs as a privileged hypervisor guest.

Key kernel subsystems:
- **SceSysModule**: Dynamic module loader managing 300+ system libraries with unique hex IDs. Libraries include libSceGnmDriver (GPU driver, 0x80000052), libSceVideoOut (0x80000022), libSceAudioOut (0x80000001), libSceNet (0x8000001C), libSceSaveData (0x8000000F), libSceWebKit2 (0x80000073), and libSceComposite (0x8000008A)
- **SceSbl**: Security block layer handling encryption, signature verification, BAR (Backup and Restore) cryptographic operations, and DRM enforcement
- **SceRegMgr**: Registry manager providing key-value persistent configuration storage
- **SceBgft**: Background file transfer for downloads and updates
- **SceAutoMounter**: Handles storage device mounting (internal SSD, M.2 SSD, USB external)
- **PFS**: PlayStation File System — the encrypted file system used for game data and backups

Kernel build strings are visible via sysctl `kern.version`, following the format `r153000/releases/01.00 May 21 2020 05:17:55`. The kernel also includes an equivalent PS4 SDK version string for compatibility purposes. Kernel module builds include repository path, revision number, and build date.

Kernel vulnerabilities have been identified in FreeBSD-derived syscalls: umtx (User Mutex) Use-after-Free, AIO (Asynchronous I/O) Double Free, IPV6_2292PKTOPTIONS Use-after-Free (CVE-2020-7457), and exFAT driver heap overflows. These provide kernel-level code execution but require pairing with hypervisor exploits for full system control.

### System Software Layer

The system software layer (Orbis OS) encompasses the user-mode runtime environment, system services, and the RNPS (Rich Native Platform Shell) application framework. RNPS comprises a large suite of applications identified by NPXS40xxx (SIE), NPXS24xxx (SCE), and NPXS27xxx Title IDs. These applications run as sandboxed user-mode processes with specific nullfs mounts and system library access.

RNPS applications are the visible face of the PS5 operating system:
- NPXS40000 (JSCD) — Contains libSceRnpsBundle.sprx; mounts /mnt/rnps to /mnt/sandbox/NPXS40000_000/mnt/rnps (nullfs)
- NPXS40002 (HOMEUI) — Home screen with game tiles, app icons, and dynamic content
- NPXS40003 (CONTROLCENTER) — Quick settings overlay accessible with PS button
- NPXS40007 (UAM_FS) — User Account Management file system
- NPXS40008 (SETTINGS) — System settings menu
- NPXS40009 (MILLENNIUMFALCON) — Game base/social feed
- NPXS40010 (WEBBROWSERDIALOG) — Modal web browser
- NPXS40011 (NOTIFICATION_OVERLAY) — Transient notification display
- NPXS40012 (NOTIFICATION_LIST) — Notification history
- NPXS40013 (PROFILE) — User profile screen
- NPXS40014 (ACTION_CARDS) — Game activity cards
- NPXS40015 (SEARCH) — System search
- NPXS40016 (MONTECARLO) — Game help/guides
- NPXS40017 (CONTENT_INFORMATION) — Content details
- NPXS40019 (SYSTEM_UPDATE) — System update UI
- NPXS40023 (CAPTURE_GALLERY) — Screenshot/video gallery
- NPXS40025 (TROPHY) — Trophy list viewer
- NPXS40033 (GAMEHUB) — Per-game hub page
- NPXS40047 (GAME_STORE) — PlayStation Store
- NPXS40063 (EXPLORE) — Discover/Explore tab
- NPXS40071 (LIBRARY) — Game library
- NPXS40080 (SHAREPLAY) — Share Play session UI
- NPXS40087 (SHELL_UI_2) — Shell UI 2 with nullfs mount
- NPXS40088 (LAUNCHER_2) — Secondary launcher
- NPXS40103 (NETCTLAP_DIALOG) — Network connection dialog
- NPXS40154 (REMOTEPLAY_HUB) — Remote Play interface

PS4-era legacy RNPS applications use NPXS24xxx IDs: NPXS24000 (FRIENDS), NPXS24001 (CHECKOUT), NPXS24002 (DEVELOPMENT), NPXS24003 (CICD_SAMPLE), NPXS24004 (BLANK), NPXS24005 (PARTY). The RNPS launcher is NPXS27027.

The system registry (REGMGR) stores all persistent configuration parameters. Key registry categories:
- 0x10xxxxx — Registry versioning, install, update, boot count (0x1070000), last version (0x1080000, 0x1100000), downgrade flags (0x1060000, 0x1110000), init flag (0x1400000)
- 0x20xxxxx — System settings: language, initialization, power management, network configuration, display, audio, IDU mode, arcade mode, HDCP, SELF verification error count, HDD write statistics, SMR HDD state
- 0x38xxxxx — Security/parental: game rating, BD/DVD region, browser, passcode, age limits
- 0x5xxxxxx — Date/time: timezone, UTC offset, RTC configuration, daylight saving
- 0x7xxxxxx — User: auto login, max users, face recognition
- 0x9xxxxxx — Accessibility: color inversion, large text, TTS, color correction (protanopia/deuteranopia/tritanopia), reduce motion
- 0xAxxxxxx — Video output: resolution, HDR metadata, 4K transfer rate, HDCP, VRR, HFR, color depth, supersampling
- 0xBxxxxxx — Audio output: 3D audio, virtual surround, codec, speaker configuration, sound format, calibration
- 0xCxxxxxx — Audio input: global mute, async source
- 0x128xxxxx — Bluetooth enable
- 0x14xxxxxx — Network: IP configuration (address, netmask, DNS, DHCP), WiFi (SSID, security, WPA keys, frequency band), HTTP proxy, SSL cert ignore, AOSS keys, AP mode, debug IP, packet capture
- 0x19xxxxxx — Network Platform: PSN environment, trophy debug, NPDRM debug, premium recheck, DRM debug clock, web API logging
- 0x1Exxxxxx — Camera hardware info
- 0x23xxxxxx — BD/DVD: menu language, audio mix, network connect, S3D on HMD
- 0x32xxxxxx — Game Live Streaming: broadcast URL, IRC, live quality
- 0x37xxxxxx — Share: recording settings, controller share, status
- 0x3Cxxxxxx — Browser: cookie, JavaScript, SSL verification, debug (JIT, network debug, iframe check)
- 0x41xxxxxx — Remote Play: enable, AP flag, 4K streaming, server version
- 0x44xxxxxx — Share Play: resolution, bitrate, framerate, quality graph, timeout settings
- 0x45xxxxxx — Party: voice priority, bandwidth, debug mode, P2P connections, WAV dump
- 0x46xxxxxx — Music: repeat, shuffle, audio balance
- 0x49xxxxxx — Video Player: 24p, closed caption settings (character color/opacity/size/font/edge/background, window color/opacity)
- 0x56xxxxxx — Voice Recognition: client ID, vendor
- 0x5Axxxxxx — System Core: shell watchdog
- 0x64xxxxxx — Companion App: debug launch mode, user bind
- 0x6Exxxxxx — Core Dump: dump mode/level, GPU dump, encrypted dump, uploader
- 0x70xxxxxx — Crash Reporting: auto sending, video clip attachment, QA auto send
- 0x73xxxxxx — System Logger: privacy configuration, debug mode, AWS, delivery URL
- 0x76xxxxxx — PS Cloud: GF version, GKO SDK version, streaming resolution
- 0x77xxxxxx — RNPS: update check, log level
- 0x78xxxxxx — Developer Environment: devkit name, boot param, GPIO0, region masquerade, CPU/GPU frequency, slow SSD mode, HDR scopes, pad disable LED sync, shell debug, compositor debug, VSH 4K rendering, theme preview, PS4 BC test mode, QA settings (fake space, fake finalized, disk copy, rebuild control, M2 select)
- 0xC0xxxxxx — Filesystem: UFS compat PKG, game PROC limits
- 0xDExxxxxx — Modules: M2 format at boot, M2 dirty flag, external HDD on CEX, HMD2 settings, voice agent

The system software layer handles localization with 30 supported languages (00-30). Language 30 (Ukrainian) was added in FW 3.00+. Each language has a still image (icon0_XX.png, 512x512px 24bit PNG noninterlaced) and update info XML (changeinfo_XX.xml, UTF-8, max 64KB). Speech recognition is supported for Japanese, English (US), French (France), Spanish (Spain), German, Italian, and Spanish (Latin America). Unreleased language slots 31-34 exist for Hebrew, Hindi, Malay, and Slovak.

System software modules are ELF binaries loaded by the kernel's SceSysModule service at boot time. The boot logo module (SceSysAvControl.elf) displays the 256x256 PS Logo image encoded as BPE (Bit Pack Encoding) with magic bytes `2A 80 80 07` during early initialization, before the RNPS shell takes over. The index.dat file generated by SceShellCore at boot contains the complete build manifest including UPD-version, release hex value, build type (cex/testkit/devkit), security-revision, sys-revision, sdk-internal-build-number, middleware-revision, vsh-revision, and Framework-Version.

System software processes utilize nullfs mounts for sandboxing. The /mnt/rnps directory is mounted on /dev/lv0/ and exposed to specific RNPS applications through nullfs bind mounts into their sandbox directories (e.g., NPXS40000 and NPXS40087 both mount /mnt/rnps into /mnt/sandbox/<TitleID>_000/mnt/rnps). NPXS40140 (Disc Player 2) mounts system_ex/rnps into its sandbox. This nullfs-based sandbox architecture prevents applications from accessing files outside their designated directories.

The modal browser (WebKit-based) provides embedded web rendering for system-integrated web content, social media authentication (Twitter, YouTube, Twitch), and the Users Guide. No standalone browser application exists — the browser is invoked modally by system applications. WebKit on PS5 has JIT compilation disabled (configured via HAVE_MAP_ALIGNED workaround in OptionsPlaystation.cmake), mitigating certain classes of JIT-based exploits. Despite this, the browser has been a source of CVEs including WebKit JSC bugs (get_by_id_with_this + ProxyObject JSScope leak patched in FW 10.00, CVE-2023-38600 integer underflow patched in FW 9.00). Chrome V8 CVEs (2025-6554, 2025-5419, 2024-0517) and Mozilla SpiderMonkey CVE-2018-5093 (WebAssembly Table integer underflow) are documented but untested on PS5. The browser registry keys at 0x3Cxxxxxx control cookie/JavaScript settings and include debug options (CA list load mode, SSL verification, DFG JIT enable, network debug config, iframe check, JS log).

### Application Layer

The application layer encompasses all user-facing software: games, system applications, and the system UI. Applications run in sandboxed environments with restricted file system access, mounted save data directories, and mediated GPU access through libSceGnmDriver.

Games use the PPSA Title ID prefix (e.g., PPSA01341 for Demon's Souls, PPSA01411 for Spider-Man: Miles Morales, PPSA01289 for Sackboy). Launch titles required minimum firmware 1.14. Game metadata includes genre, developer, publisher, release dates, size, VR support, and disc/digital availability. Game updates are tracked with the same PPSA prefix and revision numbers.

Application execution model:
- Games run in dedicated hypervisor partitions with their own kernel instances
- System applications (NPXS prefix) run in the system partition with broader but still restricted privileges
- Application sandboxes enforce file system access through mount points
- Save data is mounted at `/mnt/pfs/savedata_<User ID>_<Title ID>_<savedata name>` or `/mnt/sandbox/<Title ID>/savedataX` during gameplay
- PS4 save data on PS5 is stored at `/user/home/<User ID>/savedata/<Title ID>`
- Applications cannot directly access the encrypted SSD without kernel mediation

PS5 demo/trial games are listed on the PlayStation Store under category ID `95601a70-7564-4771-b305-0283fe3593e4` at URL format `https://store.playstation.com/<region>/category/95601a70-7564-4771-b305-0283fe3593e4`.

## Firmware History

The PS5 firmware has evolved through 13 major versions since launch. Key versions and their significance:

| Version | Build String | Date | Size | Key Changes |
|---------|-------------|------|------|-------------|
| 1.00 | 20.01-01.00.00.37 | 2020-05-21 | — | Canada/US launch physical release |
| 1.14 | 20.02-01.14.00.00 | 2020-10 | — | Minimum firmware for launch games |
| 2.20 | 20.02-02.20.00.07 | 2020-11-06 | 868 MB | Official release day patch |
| 2.25 | 20.02-02.25.00 | 2020-11 | — | Improved system performance, fixed download queue issue preventing game downloads |
| 2.26 | 20.02-02.26.00 | 2020-12 | — | Fixed disc game deletion bug after download, fixed DualSense charging via front USB-A in rest mode |
| 2.30 | 20.02-02.30.00 | 2021-02 | — | Fixed data transfer/cancel download, PS4 text input errors, Wi-Fi stability improvements |
| 2.50 | 20.02-02.50.00 | 2021-04 | — | Fixed PS4 disc auto-install after PS5 upgrade installation, added Share Factory Studio clip editing |
| 3.00 | 21.01-03.00.00 | 2021-04 | — | Major update; added Ukrainian language (language 30), external USB storage for PS4 games |
| 3.20 | 21.01-03.20.00 | 2021-07 | — | DualSense firmware updater, screen reader fixes, hidden game fix, USB storage copy stability |
| 4.00 | 21.02-04.00.00.42 | 2021-09-03 | 913.7 MB | Major update; M.2 SSD expansion slot support |
| 5.00 | 22.01-05.00.00 | 2022-03 | — | Major update; improved social features |
| 6.00 | 23.01-06.00.00 | 2022-09 | — | Major update |
| 7.00 | 23.01-07.00.00.44 | 2023-02-28 | — | Major update; Discord voice chat integration |
| 8.00 | 23.02-08.00.00 | 2023-09 | — | Major update |
| 9.00 | 24.02-09.00.00.45 | 2024-03-09 | — | Major update; native PS2 emulator support |
| 10.00 | 24.06-10.00.00.46 | 2024-09-03 | — | Major update; variable refresh rate for 1440p, social enhancements |
| 11.00 | 25.02-11.00.00.43 | 2025-03-04 | — | Major update; system performance and security improvements |
| 12.00 | 25.06-12.00.00.43 | 2025-09-09 | — | Major update |
| 13.00 | 26.02-13.00.00.40 | 2026-03-10 | — | Latest major; significant security hardening |
| 13.40 | 26.04-13.40.00.02 | 2026-05-28 | — | Latest version; minor bug fixes |

The firmware uses a semester-based build numbering system. Before 2024, SS (semester) was 01 (first half Jan-Jun) or 02 (second half Jul-Dec). Since 2024, SS uses per-year counters starting from 03, allowing multiple major releases per year.

Firmware update delivery uses the same CDN infrastructure as game updates. The `updatelist.xml` file at `http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6/list/<TLD>/updatelist.xml` lists available versions and their PUP download URLs. Installation requires a USB drive formatted FAT32 or exFAT with `PS5\UPDATE\PS5UPDATE.PUP`. Partial reinstallation (no data loss) uses the SYSTEM PUP via Safe Mode option 3 > option 1. Complete reinstallation (data loss) uses the RECOVERY PUP via Safe Mode option 7. Downgrading is not permitted — the system refuses to install a firmware version lower than the currently installed version.

## Boot Process

The PS5 boot process proceeds through multiple stages of increasing privilege and capability, each stage verifying the next:

1. **Power-on Reset**: The Boot ROM executes from the SoC's internal mask ROM. It initializes minimal hardware: CPU caches, stack pointer, SRAM. The Boot ROM reads one-time programmable fuses containing the root public key hash. It locates and validates the Secure Loader image from the boot flash using a hardware-accelerated cryptographic engine (SHA-256, RSA-2048 verification).

2. **Secure Loader**: The validated Secure Loader takes over. It initializes system DRAM (16 GB GDDR6), sets up memory controllers, and configures the Trusted Execution Environment for secure cryptographic operations. The Secure Loader validates the hypervisor loader image against its digital signature. Anti-rollback enforcement occurs here — the loader compares the firmware version to the stored last-version registry key and refuses downgrades.

3. **VBIOS Initialization**: The AMD ATOMBIOS (Video BIOS) is loaded and executed. It initializes GPU hardware, display planes, and HDMI/DisplayPort PHYs. The GPU is brought out of reset and configured for basic frame buffer output. The boot logo (256x256 PS Logo, BPE-encoded with magic bytes `2A 80 80 07`) is rendered by SceSysAvControl during this phase.

4. **Hypervisor Loader**: The hypervisor is brought up with its own memory partition. It establishes VM memory maps, configures the IOMMU for DMA remapping, sets up interrupt routing tables (to route hardware interrupts to appropriate VMs), and initializes the VM lifecycle manager. The hypervisor then creates the initial system VM.

5. **Kernel Load**: The system kernel loads into the system VM as a privileged hypervisor guest. It initializes device drivers, file systems (PFS root mount, UFS for system partitions), the networking stack, and system services including SceSysModule for dynamic library loading. Process table, virtual memory subsystem, and security monitors initialize.

6. **System Software Initialization**: The init process starts system daemons. SceSysAvControl hands off from boot logo to the RNPS shell. SceShellCore begins execution, reading index.dat from `/priv/etc/index.dat` for build configuration. RNPS applications initialize: Home UI (NPXS40002), Settings framework (NPXS40008), networking daemons (SceNetCtl, BGFT for background downloads). The system logger, crash reporter, and RNPS overlay services start.

7. **Ready State**: The console reaches the interactive home screen. Games and applications can be launched in isolated hypervisor partitions. DualSense pairing and user authentication are completed. Background services (update checker, telemetry) continue running.

The boot logo is rendered during the transition between VBIOS initialization and hypervisor loader execution. The SceSysAvControl module decodes the BPE-compressed 256x256 PS Logo image and outputs it to the display framebuffer. BPE (Bit Pack Encoding) uses the magic signature `2A 80 80 07` — this signature may change in future firmware versions. The logo remains on screen until SceShellCore completes initialization and the RNPS Home UI takes over.

The firmware update boot path differs from the normal boot path. When a PUP installation is triggered (via Safe Mode or system update), the Secure Loader processes the PUP file before handing off to the hypervisor. The PUP is cryptographically verified, extracted, and written to the system partitions. The recovery PUP path bypasses the normal system software entirely — the Secure Loader loads a minimal recovery environment for applying the update. This recovery environment is also the mechanism for Safe Mode option 7 (full reinstallation).

Safe Mode is a separate boot path triggered by holding the power button until two beeps (approximately 7 seconds). The DualSense must be connected via USB. Safe Mode provides seven numbered options:
1. **Restart PS5** — Ends Safe Mode and reboots normally
2. **Change Video Output** — Change Resolution (1080p/720p) or Change HDCP Mode (enable/disable)
3. **Update System Software** — Update from USB Drive (FAT32, PS5 > UPDATE > PS5UPDATE.PUP) or Update Using Internet
4. **Restore Default Settings** — Resets system to factory defaults without deleting user save data
5. **Rebuild Database** — Scans SSD and rebuilds content database; used to fix system freezes, frame rate drops, and content corruption
6. **Reset PS5** — Deletes all user data, restores factory state (equivalent to factory reset)
7. **Reset PS5 (Reinstall System Software)** — Full recovery using RECOVERY PUP via USB; wipes all data and reinstalls system software from scratch

## System Features

### Backwards Compatibility

The PS5 implements backward compatibility through multiple distinct mechanisms:

**PS4 Compatibility** — Available since FW 2.00+. PS4 games run via a PS4 emulation layer that translates PS4 syscalls, remaps GPU command buffers from PS4's Gnm to PS5's GnmDriver, and handles CPU mode switching. The PS4 emulator runs as a hypervisor guest, likely with its own kernel instance. PS4 emulator revisions are tracked via build strings in the firmware. The compatibility rating system: Incompatible (game does not boot), In-Game (boots but may not be playable, often rendering issues), Playable (minor issues like audio sync or frame drops), Perfect (no perceived issues), Enhanced (PS5-specific patches improving resolution/performance). God of War (2018) Enhanced runs at 4K/60fps with potentially stability issues. P.T. (Silent Hills playable teaser) is intentionally blocked by Konami at the firmware level. Most tested PS4 titles run at Perfect quality.

**PS2 Compatibility** — Two methods exist:
- Method 1 (PS4 SDK PS2 Emulator): Available since FW ~2.00. Uses the PS2emu from PS4 SDK packages running through the PS4 emulation layer. Games have CUSA (PS4) Title ID prefix and version numbering XX.YY (PS4 format). This is the emulator used by the mast1c0re exploit chain.
- Method 2 (Native PS5 PS2 Emulator): Available since May 2024 (around FW 9.00 timeframe). Compiled with PS5 SDK, not relying on PS4 emulation. Games have PPSA (PS5) Title ID prefix with PKG size differing from PS4 version. Version numbering follows format XX.000.0YY. Critically, the native emulator supports game savestates — a feature not available in the PS4-compat path, indicating tighter hypervisor/kernel integration.

**PS1 Compatibility** — Primarily delivered through Carbon Engine by Limited Run Games. PS1 games are released as PS5 native titles with PPSA Title IDs. Notable releases: Tomba! Special Edition (PPSA21381, 2024-08-01), Clock Tower: Rewind (PPSA21337, 2024-10-29), Gex Trilogy (PPSA28542, 2025-06-16), Fear Effect (PPSA27321, 2025-08-29). Announced titles include Tomba! 2, Fear Effect 2, Fighting Force Collection, and Vagrant Story.

**PSP Compatibility** — No PS5-specific PSP emulator exists. PSP emulation runs through the PS4 emulation layer, functionally identical to the PS4 implementation.

**PC Emulation** — Kyty is the only known PS5 emulator for PC (developed by InoriRus, GitHub: https://github.com/InoriRus/Kyty). The emulation state is early with limited game compatibility.

### Safe Mode

Safe Mode provides seven recovery options accessible by holding the power button until two beeps (console must be completely off, DualSense connected via USB):

1. Restart PS5 — Normal reboot exit from Safe Mode
2. Change Video Output — Set resolution to 1080p or 720p; enable/disable HDCP mode for HDMI troubleshooting
3. Update System Software — Install firmware via USB (FAT32, PS5/UPDATE/PS5UPDATE.PUP) or download from internet
4. Restore Default Settings — Factory reset preserving user save data
5. Rebuild Database — SSD scan and content database rebuild (fixes freezes, frame rate drops, game launch failures)
6. Reset PS5 — Full factory reset deleting all user data
7. Reset PS5 (Reinstall System Software) — Complete recovery requiring RECOVERY PUP file; wipes internal storage and reinstalls firmware

### Button Combos

Several hidden button combinations trigger diagnostic, debug, and developer functions:

- **Safe Mode**: Console off, hold power button until two beeps
- **More System Information**: Settings > System > System Software > Console Information, hold L1 + L3 + Triangle for 5 seconds, release, then press D-Pad Up + Options. Displays detailed build data from `/priv/etc/index.dat`
- **Staff Mode (IDU)**: Hold L1 + L2, then press Circle, Cross, Square, Triangle, D-Pad Right in sequence, release L1 + L2. Enters IDU staff configuration mode
- **PsnInGameCommerce**: In Debug Settings, press D-Pad Left + Square + R1 simultaneously. Opens in-game commerce testing tools
- **Toggle Extra Debug Menu**: On main menu, press Start + L3 simultaneously. Requires registry setting `SblRcMgrIsAllowDebugMenuForSettings` to be enabled
- **Crash The Shell**: With registry option enabled, various 4-button combos involving D-Pad Up + L1 + R1 + another button trigger shell crash dumps for debugging

### Networking

The PS5 online architecture uses PlayStation Network servers with structured CDN URLs. Game update infrastructure involves a three-file metadata system:

1. **Title Update XML**: Downloaded from URL in param.json. Contains URL to JSON metadata and URL to Delta Package PKG. Format: `https://sgst.prod.dl.playstation.net/sgst/prod/00/np/<NP Title ID>/<Hash>-version.xml`
2. **Title Update JSON**: Downloaded from URL in XML. Contains URL to Title Update Application PKG, URL to Title Update PlayGo Information PKG, URL to Title Update PlayGo Chunk CRC. Format: `https://sgst.prod.dl.playstation.net/sgst/prod/00/<NP Title ID>/app/info/<Revision>/f_<Hash>/<Content ID>.json`
3. **Delta Package**: Incremental update PKG. Format: `http://gst.prod.dl.playstation.net/gst/prod/00/<NP Title ID>/app/pkg/<Revision>/f_<Hash>/<Content ID>-DP.pkg`

RNPS (Rich Native Platform Shell) maintains dedicated hostnames on playstation.net servers:
- chimera-lambda.rnps.dl.playstation.net
- control-center.rnps.dl.playstation.net
- feature-discovery-device-dialog.rnps.dl.playstation.net
- gaming-lounge.rnps.dl.playstation.net
- home-lambda.rnps.dl.playstation.net
- home.rnps.dl.playstation.net
- igc-browse.rnps.dl.playstation.net
- invitation-dialog.rnps.dl.playstation.net
- millenniumfalcon.rnps.dl.playstation.net
- monte-carlo.rnps.dl.playstation.net
- notification-overlay.rnps.dl.playstation.net
- player-selection-dialog.rnps.dl.playstation.net
- ppr-crl.rnps.dl.playstation.net
- profile.rnps.dl.playstation.net
- ps5-multi-bundle-ota.rnps.dl.playstation.net
- uam-fs.rnps.dl.playstation.net

Other notable PlayStation Network hostnames: asm.np.community.playstation.net, ps5.np.playstation.net, static-resource.np.community.playstation.net, uef.np.dl.playstation.net.

Remote Play supports streaming PS5 games to external devices. Official clients: Android, iOS, macOS, PS4 (since FW 8.00), PS5, Windows. Open-source Chiaki client: Android, Linux, macOS, Nintendo Switch, PS5, PS Vita (ported via VitaKi). No official Linux or Nintendo Switch client exists. Remote Play supports up to 4K streaming resolution, controlled via registry keys at 0x41xxxxxx (enable, AP flag, 4K streaming, server version, log enable).

The PS5 also supports game update check and download through its online CDN infrastructure. Games check for updates by downloading a version.xml file from `https://sgst.prod.dl.playstation.net/sgst/prod/00/np/<NP Title ID>/<Hash>-version.xml`. This XML references a JSON file containing the actual update PKG URLs. Delta packages (incremental updates) use the suffix `-DP.pkg` while full updates use the standard `.pkg` extension. PlayGo information packages (with `_sc.pkg` suffix) contain metadata for streaming/chunked game loading. Chunk CRC files (`.crc`) provide integrity verification for PlayGo components.

RNPS (Rich Native Platform Shell) is the system service layer that manages all user-facing interactive experiences. It maintains its own set of daemon processes and applications with dedicated hostnames on playstation.net servers. RNPS applications handle everything from the home screen and control center to notification overlays, social features (friends, profiles, parties, messaging), media playback (music, video, disc player), store browsing, game hubs, trophies, capture gallery, and system settings. Each RNPS application has its own Title ID in the NPXS40xxx range. The RNPS registry key at 0x77xxxxxx controls update checking and logging.

Online connection management is handled by SceNetCtl (libSceNetCtl, 0x80000009) which manages network interface configuration, WiFi connection, and network status monitoring. The network registry keys at 0x14xxxxxx store IP configuration (address, netmask, DNS, DHCP hostname), WiFi credentials (SSID, WEP/WPA keys, frequency band), HTTP proxy settings, SSL certificate ignore flags, AP mode configuration, and numerous debug settings (packet capture, emulation type, routing configuration).

The PSN platform service layer (registry 0x19xxxxxx) manages NP environment selection, trophy management debugging, patch check and auto-download, DRM debug clocks, web API logging, and commerce testing facilities. These registry entries are primarily intended for development/test environments but can be leveraged by exploits to manipulate system behavior.

The error code framework categorizes all system errors:
- CE-1xxxxx-x: General/other errors — application crashes (CE-108255-1), storage issues, disc read errors, camera failures, data transfer problems, license errors, system update failures
- E2-xxxxxxxx: External 2 errors — network connection failures
- NP-1xxxxx-x: Network server errors — sign-in problems, entitlement errors, age restrictions, license confirmations
- NW-1xxxxx-x: Network library errors — PSN connection issues
- SU-xxxxx-x: Software update errors — update download/installation failures
- WS-xxxxx-x: Web API server errors — web service communication errors
- WV-xxxxx-x: Web view errors — embedded browser rendering failures

### Storage Management

The PS5 uses an encrypted SSD that prevents data extraction without running system software. Save data is stored at `/user/home/<User ID>/savedata_prospero/<Title ID>` for PS5 games and `/user/home/<User ID>/savedata/<Title ID>` for PS4 games on PS5. During gameplay, save data is mounted at `/mnt/pfs/savedata_<User ID>_<Title ID>_<savedata name>` or `/mnt/sandbox/<Title ID>/savedataX`. Save data directories are usually mounted read-only during gameplay.

Unlike PS3 and PS4, the PS5 does not allow exporting save data to USB — a deliberate security measure against save data manipulation exploits. Access control:
- Usermode exploit: access save data of the currently mounted PS5 game only
- Kernel exploit: access save data of any PS5 game (e.g., via FTP)
- The encrypted SSD prevents any offline data access

Third-party save tools: Playstation-5-Save-Mounter by n0llptr enables mounting and editing save data without running the game (requires exploit).

The Backup and Restore (BAR) utility creates encrypted `archive.dat` files on external USB drives using PFS (PlayStation File System) encryption. BAR functions: sceSblBarCreateContext, sceSblBarUpdateAad, sceSblBarUpdateDecrypt, sceSblBarUpdateEncrypt, sceSblBarFinishDecrypt, sceSblBarFinishEncrypt. BAR has been present since at least FW 2.10. It is not present on systems with FW 1.02 and older that never connected to PSN.

Storage expansion: The M.2 SSD slot (added via FW 4.00) supports compatible NVMe drives meeting Sony's performance requirements. External USB drives support PS4 game installation and media playback. The AutoMounter module (registry 0xDExxxxxx) manages M.2 formatting, external HDD detection, and mount operations with registry flags for skip mount, skip capability check, and dirty flags.

### Build Strings

Firmware builds embed rich provenance information detectable in kernel memory dumps, system logs, and index.dat:

- **CP Box EMC**: TestKit version 1.0.1.0
- **CP Box EAP KBL**: EAP SDK versions from 5.501.000 (2019-2021), featuring Sycorax build string versions 0.5.7.0 through 2.5.5.3
- **Secure Loader**: Build string format includes sys-revision and sys-repository-path fields. Example: `Oberon-KDE 2021/04/06 05:22 releases/03.00 171343 pprbld-w54.build.rd.scei.sony.co.jp`
- **VBIOS**: AMD ATOMBIOSBK string format. Example: `AMDObrGeneri.2132099 .518911 . 06/15/20,23:33:14`
- **Kernel**: Build strings from sysctl `kern.version`. Format: `r<SVN_revision>/releases/<release_branch> <build_date>`. Example: `r153000/releases/01.00 May 21 2020 05:17:55`. Also contains equivalent PS4 SDK version string
- **index.dat** (from SceShellCore): Output on boot (5-6 seconds) on TestKit/DevKit/QA/UART-enabled CEX consoles. Key entries: UPD-version, release (hex value), build type (cex/testkit/devkit), security-revision, sys-revision, sdk-internal-build-number, middleware-revision, vsh-revision, Framework-Version

### Error Codes

Standardized error reporting using prefix-based categorization:

- CE-1xxxxx-x: Application errors (crashes, corrupt data), storage errors (disk full, read failure), disc drive errors, camera errors, data transfer failures, license/entitlement errors, system software update errors
- E2-xxxxxxxx: Network connection failures (DHCP, DNS, NAT type, timeout)
- NP-1xxxxx-x: PSN server communication errors (sign-in failure, account suspended, age restriction, entitlement check, license confirmation)
- NW-1xxxxx-x: Network library low-level errors (socket errors, SSL/TLS handshake failures, PSN connection lost)
- SU-xxxxx-x: System update errors (download failure, verification failure, installation failure)
- WS-xxxxx-x: Web service API errors (JSON parse failure, HTTP error codes, service unavailable)
- WV-xxxxx-x: Embedded web view errors (page load failure, script error, certificate error)

### Developer Features

**STAR Debug Settings** — A comprehensive developer debug menu available on DevKit and TestKit consoles. On retail consoles, the menu can be displayed via exploit (confirmed working on FW 3.xx/4.xx) but most features will error out due to missing hardware capabilities or signing. Categories:

Game Settings: Package Downloader (download/install packages from local server), Package Installer (USB local install), SaveData tools, Add Content Manager (DLC entitlement), Slow SSD Mode (emulate slower SSD performance for testing), Instant App Suspending (test resume behavior), Notice Screen Skip Flag (skip middleware/legal screens)

System Settings: TRC Check Notifications (Technical Requirement Checklist compliance testing), Region Settings (test per-region language/timezone), Debug Network Clock (operate with sceRtcGetCurrentNetworkTick), Debug NPDRM Clock (license expiration testing), Boot History (boot count statistics), Display Title ID on Home Screen, Show System Application Version

Multi User: Switch User Group (up to 64 users for region/age testing), Display Account Information

PlayStation Network: NP Environment (set PSN environment — NP Production, NPQA, NP Dev), In-Game Commerce Debug (DLC purchase flow testing), Patch Check (game patch detection), Upgradable App Debug (SKU flag values: Trial, Full, Off)

Activation: Activate Using Internet (update DevKit/TestKit expiration), Show Expiration Date, System Passcode Management

Boot Parameters: Release Check Mode (three modes: Release/Retail, Assist Mode/stripped dev, Development Mode)

Graphics (DevKit only): PA Debug (GPU performance monitoring), System Load Control (set GPU load)

Network: Network Emulation (emulate packet loss/delay), mDNS (Multicast DNS control)

Sound and Screen: Set HDCP Encryption (enable/disable HDMI encryption), Audio Output Format (LPCM/Dolby/DTS/Headphone/TV Virtual Surround), Adjust HDR (HDR strength and effect editing)

System Update: Update Server URL (custom firmware update server URL)

Diagnostics: Export Error/Notification History to USB, Fake Device Settings (SIE-directed only), Core Dump (dump level, system dump level, GPU mini capture), Crash Reporting (enable/disable)

**IDU Mode (Individual Display Unit)** — Kiosk/demo mode for retail display consoles. Activated by hardware (IDU disc) or software, flashing a persistent flag to sflash/NOR that survives firmware reinstallation. The IDU Utility Normal application (3.87 MB, NPXS45182) manages demo bundles. IDU mode restricts application launching and PSN features. When no bundle is installed, a splash screen with "Content unavailable" is displayed. Setup options: Country, Language, Region, Disable Downloads (ON/OFF), Allow Game Downloads (automatic demo downloads), Allow Video Downloads (trailers), Disable Attract Mode Audio (ON/OFF), Virtual Controller (ON/OFF). Status screen displays: System Software Version, System Hardware ID (console's hardware ID, not normally visible), Client Version (IDU client version, like PS4's OMSK), Device Name, Installed Bundle version, Bundle Name.

Ten internal Title IDs for IDU functions: NPXS40069 (IDU Daemon, activates retail package recognition/installation), NPXS45085 (IDU Client, main GUI), NPXS45181 (IDU Utility Full), NPXS45182 (IDU Utility Normal), NPXS21005 (legacy PS4 IDU Daemon), NPXS29005 (legacy PS4 IDU OMSK Client), NPXS29800 (IDU Utility, possibly disc-only), NPXS29801 (IDU Utility Region), PPSL07787 (IDU Client for E1), PPSA01759 (IDU Client for Production).

**Game Hub Preview App** — DevKit/TestKit tool for previewing game hub page appearance. Input types: Concept ID, (NP) Title ID, or Product ID. Three lifecycle preview modes: Concept Announced (Coming Soon — no product available), Product Available (one or more products for sale), Product Sold (user has purchased the game). Retail use requires network connection.

**Store Preview** — DevKit/TestKit tool (NPXS40041) for previewing In-Game and Global catalogs of the regional PlayStation Store. On retail machines, requires internet connection.

**Publishing Tools** — Official Sony SDK tools for licensed developers:
- prospero-pub-param.exe: Param File Editor — creates/verifies .json param files for applications, patches, DLC
- prospero-pub-cmd.exe: Publishing Tools CLI — CUI versions of publishing features including Package Generator
- ProsperoGP5Editor.exe: GP5 Generator — scans game folder structure, generates .gp5 project files
- vagconv2w.exe / vagconv2.exe: VAG Converter 2 — converts 16-bit linear PCM to HE-VAG audio data
- at9tool.exe: ATRAC9 Encoder/Decoder
- sieaacformattool.exe: AAC Format Tool
- sieOpusFormatTool.exe: Opus Format Tool

**More System Information** — Hidden diagnostic menu accessible via button combo from Settings > System > System Software > Console Information (hold L1 + L3 + Triangle for 5 seconds, release, press D-Pad Up + Options). Displays detailed build data from `/priv/etc/index.dat`: system software version details including release (hex), build type (cex/testkit/devkit), revision numbers, security revision, sys revision, SDK internal build number, middleware revision, VSH revision, and Framework Version.

## Relationships

- [[hardware_overview]] — hardware is the foundation; the custom SoC (Oberon), GDDR6 memory subsystem, custom SSD controller, and I/O complex determine the capabilities and constraints of all higher layers
- [[kernel]] — kernel provides core OS services including process management, virtual memory, file systems (PFS, UFS, exFAT), device drivers, and the SceSysModule dynamic library loader
- [[hypervisor]] — hypervisor provides isolation between system and game partitions via Type-1 virtualization, IOMMU-enforced memory isolation, and VM lifecycle management
- [[security_model]] — security permeates all layers from hardware root of trust in Boot ROM through Secure Loader signing, hypervisor isolation, kernel access control, and application sandboxing
- [[firmware]] — firmware boot chain initializes the system from power-on through Boot ROM, Secure Loader, VBIOS, hypervisor loader, and kernel handoff

## Security Considerations

The PS5 architecture implements defense-in-depth with multiple independent security boundaries. The hardware root of trust in Boot ROM anchors cryptographic verification of all subsequent boot stages via RSA-2048 signatures and SHA-256 hashes. The hypervisor enforces strict VM isolation — a compromised game partition cannot access system memory or other game partitions. The kernel implements FreeBSD-derived access controls with encrypted PFS storage. The application layer enforces sandboxing through restricted file system mounts, mediated GPU access, and encrypted save data.

Despite these layers, several attack surfaces have proven viable:

**Usermode Entry Vectors**:
- WebKit JavaScriptCore bugs: get_by_id_with_this + ProxyObject JSScope leak (FW 6.00-9.60, patched 10.00), CVE-2023-38600 integer underflow in genericTypedArrayViewProtoFuncCopyWithin (FW 6.00-8.60, patched 9.00). JIT-disabled bugs (CVE-2024-27833 SBFX overflow, CVE-2023-41993 clobberize, DFG Abstract Interpreter type confusion) are not exploitable since PS5 disables JIT compilation in WebKit
- BD-J (Blu-ray Java): Native code execution through the Blu-ray Java environment, working on FW 1.00-7.61
- Lua game savedata: Hijacking Lua interpreter in games that use Lua for savedata scripting
- mast1c0re: JIT code execution via PS2 Classics emulator (Star Wars: Racer Revenge), FW 2.00-13.00. Uses the PS2 emulator's dynamic recompiler to generate native code, bypassing the JIT-disabled WebKit

**Kernel Exploits**:
- umtx Use-after-Free (multiple firmware ranges)
- AIO Double Free (combined with other exploits)
- IPV6_2292PKTOPTIONS UaF CVE-2020-7457 (FW 3.00-4.51)
- exFAT driver heap exploit (FW <=4.03, PoC only)
- GPU DMA copy bypass for kernel .data write protection on FW >=6.00

**Hypervisor Exploits**:
- TMR vulnerabilities discovered by fail0verflow
- flatz's hypervisor exploit (unreleased, FW <=2.70)
- Byepervisor by Specter (released, FW 1.00-2.70)

**Exploit Chains**:
- <=2.70: flatz's hypervisor + umtx UaF; Byepervisor + AIO/umtx
- 1.00-5.50: PSFree + AIO/umtx + WebKit loadInSameDocument
- 3.00-4.51: IPV6 UaF + WebKit or BD-JB
- 1.00-7.61: BD-JB chains with AIO/umtx + GPU DMA copy for >=6.00
- 1.00-10.01: Lua game savedata chains (mast1c0re)
- <=4.03: exFAT driver heap (PoC only)
- 2.00-13.00: Mast1c0re part 2 JIT execution

**Homebrew Enablers**: Prosperous HEN (FW 1.00-4.51, hypervisor + kernel), Byepervisor HEN (FW 1.00-2.70), HEN-V (FW 3.00-4.51, kernel-only), etaHEN (FW 2.00-10.01, kernel-only), kstuff (FW 3.00-12.00, kernel ELF loading), libhijacker (FW 3.00-4.51, library injection), BackPork (background auto-sideload), PS4 EBOOT DLC Patcher (PC tool).

**Forensic Traceability**: PUP watermarking provides content traceability for leaked firmware. Old-format watermarks embed DevNet user ID, organization name, company name, download date, and host IP address. New-format watermarks use a serial number that must be provided to the DevNet development team to identify the user and organization.

**Security Limitations and Gaps**:
- The encrypted SSD prevents offline data extraction but is decryptable with sufficient system access
- Save data cannot be exported to USB (unlike PS3/PS4), closing a known PS4 save-data manipulation attack vector
- Hypervisor exploits exist and have been demonstrated, enabling full HEN capabilities on vulnerable firmware versions
- The narrow firmware compatibility windows (Byepervisor HEN: 1.00-2.70, Prosperous HEN: 1.00-4.51) mean current firmware (13.40) has no publicly known full compromise path
- Kernel-only HEN (etaHEN) covers a wider range (2.00-10.01) but cannot disable hypervisor-level security monitoring
- Mast1c0re provides JIT execution on all firmware up to 13.00 but is limited to a single PS2 Classic game's emulator environment
- SIE publishes open-source component licenses at https://doc.dl.playstation.net/doc/ps5-oss/index.html, enabling version-specific vulnerability research against bundled open-source components
- The Unity PS5 LibIL2CPP is available at https://github.com/KuromeSan/ps5-lib-il2cpp (found in Unity PS5 Support for Editor 2021.2.0a6), providing insight into the PS5 IL2CPP runtime used by Unity games
- Third-party analysis tools (PS5-Pup-Decrypt, PS5-Pup-Unpacker by Zecoxao, PS5 Tools by SKFU) enable firmware extraction and analysis, though decryption keys are not publicly available for current firmware versions
- PS5Prxy (proxy for redirecting PS5 manual pages) provides a man-in-the-middle capability for analyzing system software update requests
- PS5 Firmware Checker enables automated version tracking and PUP download monitoring

The PS5's security model has evolved significantly through firmware updates. Each major firmware version has patched known exploit vectors while introducing new features that may expand the attack surface. FW 4.00 added M.2 SSD support (new storage attack surface), FW 7.00 added Discord voice chat (new network service integration), FW 9.00 added native PS2 emulator (new JIT compilation surface exploited by mast1c0re), and FW 10.00 patched the WebKit JSScope leak that had been exploitable since FW 6.00. This pattern of feature introduction and vulnerability patching is typical for console security lifecycles.

The most significant difference between PS5 and PS4 security is the hypervisor isolation layer. On PS4, kernel access (via the WebKit+kernel exploit chain) was sufficient for full system control. On PS5, kernel access alone cannot disable hypervisor-level security monitors — the hypervisor continues enforcing memory isolation even when the kernel is compromised. This architectural difference means PS5 homebrew requires either a hypervisor exploit or acceptance of kernel-only access with permanent security monitoring active.

## References

- https://www.psdevwiki.com/ps5/System_Software
- https://www.psdevwiki.com/ps5/Firmware_Changelog
- https://www.psdevwiki.com/ps5/Safe_Mode
- https://www.psdevwiki.com/ps5/System_Software_Installation
- https://www.psdevwiki.com/ps5/Backwards_compatibility
- https://www.psdevwiki.com/ps5/BootLogo
- https://www.psdevwiki.com/ps5/Build_Strings
- https://www.psdevwiki.com/ps5/Button_Combos
- https://www.psdevwiki.com/ps5/Error_Codes
- https://www.psdevwiki.com/ps5/Languages
- https://www.psdevwiki.com/ps5/Libraries
- https://www.psdevwiki.com/ps5/Registry
- https://www.psdevwiki.com/ps5/Remote_Play
- https://www.psdevwiki.com/ps5/Online_Connections
- https://www.psdevwiki.com/ps5/IDU_Mode
- https://www.psdevwiki.com/ps5/More_System_Information
- https://www.psdevwiki.com/ps5/Modal_Browser
- https://www.psdevwiki.com/ps5/Backup_And_Restore
- https://www.psdevwiki.com/ps5/Demo_Games
- https://www.psdevwiki.com/ps5/Games
- https://www.psdevwiki.com/ps5/Game_Titles
- https://www.psdevwiki.com/ps5/Game_Update_Information
- https://www.psdevwiki.com/ps5/Save_Data
- https://www.psdevwiki.com/ps5/PS1_Emulation
- https://www.psdevwiki.com/ps5/PS2_Emulation
- https://www.psdevwiki.com/ps5/PS4_Emulation
- https://www.psdevwiki.com/ps5/PSP_Emulation
- https://www.psdevwiki.com/ps5/PS5_Emulators_-_PC/MAC/Android
- https://www.psdevwiki.com/ps5/Watermarks
- https://www.psdevwiki.com/ps5/%E2%98%85_Debug_Settings
- https://www.psdevwiki.com/ps5/%E2%98%85_Game_Hub_Preview_App
- https://www.psdevwiki.com/ps5/%E2%98%85_Store_Preview
- https://www.psdevwiki.com/ps5/Publishing_Tools
- https://www.psdevwiki.com/ps5/Source_Code
- https://www.psdevwiki.com/ps5/Software
- https://www.psdevwiki.com/ps5/RNPS
- https://www.psdevwiki.com/ps5/Bugs
- https://www.psdevwiki.com/ps5/Exploit_Chains
- https://www.psdevwiki.com/ps5/Homebrew_Enabler
