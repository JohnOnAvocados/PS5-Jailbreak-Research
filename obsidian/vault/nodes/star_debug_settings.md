# ★ Debug Settings

## Source
inbox\star_debug_settings.md

## System Layer
firmware

## Summary
# ★ Debug Settings

## Source URL
https://www.psdevwiki.com/ps5/%E2%98%85_Debug_Settings

## System Layer
System Software

## Summary
Comprehensive developer debug settings menu available on DevKit/TestKit consoles. Retail consoles require an exploit to access (on FW 3.xx/4.xx) but most features will error out. ## Key Concepts

### Game Settings
- **Package Downloader** — Package download/install emulation on local server
- **Package Installer** — Local package install via USB
- **SaveData** — Save data handling during development
- **Add Content Manager** — DLC entitlement management
- **Slow SSD Mode** — Emulate slow SSD for testing
- **Instant App Suspending** — Test resume from suspension
- **Notice Screen Skip Flag** — Skip middleware screens (NSSF)

### System Settings
- **TRC Check Notifications** — TRC (Technical Requirement Checklist) compliance checks
- **Region Settings** — Test system languages/time zones per region
- **Debug Network Clock** — Operate with `sceRtcGetCurrentNetworkTick()`
- **Debug NPDRM Clock** — License expiration testing
- **Boot History** — Boot count statistics
- **Display Title ID on Home Screen** — Show title IDs on icons
- **Show System Application Version** — Display version info

### Multi User
- **Switch User Group** — Switch up to 64 users for testing region/age settings
- **Display Account Information** — Show PSN account info on login screen

### PlayStation Network
- **NP Environment** — Set PSN environment variables
- **In-Game Commerce Debug** — DLC purchase flow testing
- **Patch Check** — Game patch detection
- **Upgradable App Debug** — SKU flag values (Trial, Full, Off)

### Activation
- **Activate Using Internet** — Update DevKit/TestKit expiration via PSN Dev Network
- **Show Expiration Date** — Display expiration
- **System Passcode Management** — Set boot passcode

### Boot Parameters
- **Release Check Mode** — Three modes: Release/Retail, Assist Mode (stripped dev), Development Mode

### Graphics (DevKit Only)
- **PA Debug** — GPU performance monitoring
- **System Load Control** — Set GPU load

### Network
- **Network Emulation** — Emulate packet loss/delay
- **mDNS** — Multicast DNS control

### Sound and Screen
- **Set HDCP Encryption** — Enable/disable HDMI encryption
- **Audio Output Format** — LPCM/Dolby/DTS/Headphone/TV Virtual Surround
- **Adjust HDR** — HDR strength and effect editing

### System Update
- **Update Server URL** — Custom firmware update server URL

### Other Notable Features
- **Export Error/Notification History to USB** — Error log export
- **Fake Device Settings** — Only when directed by SIE
- **Core Dump** — Dump level, system dump level, GPU mini capture
- **Crash Reporting** — System crash reporting enable/disable

## System Role
The Debug Settings menu provides extensive developer controls for testing all aspects of PS5 games and system behavior.

## Concepts
system, debug, settings, network, testing, update, boot, display, expiration, mode, package, screen, server, set, show

## Related Notes
- [[../nodes/backup_and_restore]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/button_combos]]
- [[../nodes/devices]]
- [[../nodes/dualsense]]
- [[../nodes/dualsense_dfu_modes]]
- [[../nodes/emc]]
- [[../nodes/error_codes]]
- [[../nodes/etahen_homebrew_enabler]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_titles]]
- [[../nodes/game_update_information]]
- [[../nodes/ioctl]]
- [[../nodes/jigkick_files]]
- [[../nodes/kernel_functions]]
- [[../nodes/languages]]
- [[../nodes/lapse_kernel_exploit]]
- [[../nodes/more_system_information]]
