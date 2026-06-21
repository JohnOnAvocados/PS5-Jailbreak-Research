# PS5 Update Mechanism

## Overview

The PS5 firmware update system delivers system software updates through Sony's content delivery network as PUP (PlayStation Update Package) files. Updates are cryptographically signed and verified before installation, with anti-downgrade protection enforced by the boot chain's security revision system. The update mechanism supports three types of updates: full firmware replacement (recovery), partial system software updates (system), and extension packages (system_ex). Each update type undergoes cryptographic verification through the secure module infrastructure before any writes to persistent storage occur.

Updates are delivered over the internet through Sony's CDN infrastructure at `ps5.update.playstation.net`. The download URLs include an obfuscated path component (`tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6`) that serves as a CDN authentication token. The PUP file naming follows the pattern `PS5UPDATE.PUP` with a SHA-256 hash embedded in the URL path for pre-download integrity verification. For offline recovery, updates can be installed from USB media formatted FAT32 or exFAT with the file placed at `PS5/UPDATE/PS5UPDATE.PUP`. The Safe Mode interface provides the recovery environment for manual update installation.

The update system is designed with defense-in-depth principles. The PUP file itself is signed and verified by the `pup` secure module (0x80021002) before any contents are written. After installation, the updated firmware components are verified again during the next boot through the normal secure boot chain. The anti-rollback mechanism ensures that firmware can only move forward in version, with OTP fuses burning to permanently record the minimum security revision. This design means that even a successful compromise during the update process cannot result in a downgrade attack.

## Update Types

### System PUP

The `system` PUP type contains the full system software package for partial reinstallation or upgrade. This package preserves user data, installed applications, saved games, and all user settings. Key characteristics:

- **Size**: Varies by version, typically 800-1200 MB
- **Contents**: System software binaries, kernel, secure modules, libraries, system configuration
- **Installation methods**: Over-the-internet update, Safe Mode option 3 sub-option 1 (Update from USB Drive)
- **Data preservation**: All user data remains intact
- **Use cases**: Standard firmware upgrades, partial recovery of corrupted system software without data loss

The system PUP updates the main firmware partitions on the NAND flash but does not modify the boot-chain critical components (Secure Loader, EMC firmware) unless the update includes a boot chain revision. When boot components are updated, the security revision in OTP fuses is also increased.

### Recovery PUP

The `recovery` PUP type is a complete system software image used for full reinstallation. Installing a recovery PUP is a destructive operation that wipes all user data:

- **Size**: Larger than system PUP, typically 1-2 GB
- **Contents**: Complete system image including boot chain components, system software, pre-installed applications, factory configuration
- **Installation methods**: Safe Mode option 7 (Reset PS5 with Reinstall System Software)
- **Data preservation**: All user data, accounts, settings, and installed applications are deleted
- **Use cases**: Factory reset, recovery from severe system corruption, preparing console for resale

The recovery PUP includes the boot chain components (Secure Loader, EMC firmware, Hypervisor Loader, kernel) and writes them to all relevant partitions including the serial flash boot areas. After a recovery installation, the console boots from a clean state as if fresh from the factory, except with the restored firmware version's security revision.

### System Extension PUP

The `system_ex` PUP type provides supplementary system software updates that modify or extend specific system components without a full firmware replacement:

- **Size**: Relatively small, typically 100-300 MB
- **Contents**: Specific feature updates, security patches, component updates
- **Installation methods**: Over-the-internet update, may be bundled with system PUP updates
- **Data preservation**: All user data unaffected
- **Use cases**: Targeted security fixes, feature additions between major firmware releases

System extension PUPs allow Sony to deploy targeted updates without requiring a full firmware download, reducing bandwidth requirements and installation time.

## Update Process

### Delivery Infrastructure

The PS5 checks for available updates by fetching an XML manifest from Sony's update servers. The manifest URL uses a standardized pattern:

```
http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6/list/<TLD>/updatelist.xml
```

The components:
- `<EXTLD>`: Regional extension (e.g., `gs2`, `gsa`)
- `tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6`: CDN authentication string (consistent across all regions)
- `<TLD>`: Top-level domain code (e.g., `com`, `jp`)

The actual PUP file download URL:

```
http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6/image/<YYYY_MMDD>/<TYPE>_<SHA256>/PS5UPDATE.PUP?dest=<TLD>
```

The URL includes:
- `<YYYY_MMDD>`: Date stamp of the firmware release
- `<TYPE>`: PUP type (`system`, `recovery`, or `system_ex`)
- `<SHA256>`: SHA-256 hash of the PUP file, providing pre-download integrity verification

The updatelist.xml manifest contains metadata about available firmware versions including version numbers, file sizes, SHA-256 hashes, and release notes. The PS5 downloads this manifest periodically and in response to user-initiated update checks.

### Download and Verification

When a new firmware update is available, the download and verification proceeds as follows:

1. The PS5 fetches updatelist.xml and compares the available version against the installed version
2. If a newer version is available, the console downloads the PUP file from the CDN
3. During download, the SHA-256 hash is verified incrementally
4. After download completes, the full PUP file is verified by the `pup` secure module (0x80021002)
5. The `pup` module validates the PUP's cryptographic signature chain:
   - RSA-3072 signature on the PUP metadata header
   - Per-segment signature verification for each PUP content segment
   - SHA-256 integrity check for the complete PUP image
6. If verification passes, the update package is staged for installation
7. If verification fails, the download is discarded and an error is reported

The verification process ensures that only Sony-signed official firmware can be installed. The signature chain is rooted in the same RSA-4096 key hierarchy used by the boot chain, extending the chain of trust from hardware root through the update process.

### Installation

The installation phase proceeds after successful verification:

1. The system reboots into update mode (a special boot configuration that mounts the update partition)
2. The PUP contents are decrypted using the appropriate firmware keys
3. Each PUP segment is written to its target partition on the NAND flash
4. Boot chain components (if included in the update) are written to serial flash
5. The security revision in OTP fuses is updated to the new firmware's value
6. The kernel and system software partitions are overwritten with the new version
7. If updating from recovery PUP, user data partitions are formatted
8. On successful installation, the system reboots through the normal boot chain
9. The secure boot chain verifies all updated components before allowing normal boot
10. If boot chain verification fails, the system enters recovery mode

The installation process is designed to be atomic where possible. If the installation is interrupted (power loss, hardware failure), the system boots from the previous firmware version if the update partition was not yet modified, or enters recovery mode if critical boot components are corrupted.

## PUP File Internal Structure

While the exact internal layout of PS5 PUP files is not fully documented, analysis of firmware update patterns reveals a consistent structure:

### PUP Container Layer
- **Header**: Contains PUP type identifier (system/recovery/system_ex), firmware version, file size, and segment count
- **Signature Block**: RSA-3072 signature over the header, verified by the `pup` secure module
- **Manifest**: Lists all segments, their target partitions, sizes, and per-segment SHA-256 hashes
- **Segment Data**: Multiple compressed or encrypted data segments, each corresponding to a target NAND partition

### Target Partitions

PUP segments target specific NAND flash partitions:

- **boot chain area**: Serial flash at offset 0x800 (Secure Loader) and 0x4000 (EMC firmware)
- **kernel partition**: The kernel SELF binary
- **system partition**: Main system software including libraries and system daemons
- **secure module partition**: 0x8002xxxx secure module binaries
- **configuration partition**: System settings and calibration data
- **language/data partition**: Localization and asset data

### Compression and Encryption

PUP segments may use:
- **zlib compression**: For non-critical data segments to reduce download size
- **AES-128-CBC encryption**: For boot-critical segments, using the same key hierarchy as the boot chain
- **Per-segment signing**: Each critical segment may have its own RSA-3072 signature

The exact combination of encryption and compression depends on the segment type and target partition.

## Recovery

### Safe Mode

Safe Mode is a special boot mode accessed by holding the power button for approximately 7 seconds until two beeps are heard. The DualSense controller must be connected via USB cable (Bluetooth is not available in Safe Mode). Safe Mode provides a minimal operating environment running at a reduced system level, with only essential services initialized. This allows recovery operations even when the main system software is corrupted or unbootable.

Safe Mode is triggered by the boot chain when it detects corruption in critical system partitions, or manually by the user holding the power button at boot. The Safe Mode environment loads only:
- PSP and EMC firmware (standard boot chain stages 0-2)
- Minimal kernel with Safe Mode drivers
- USB mass storage support
- Display output at basic resolution
- DualSense controller input via USB

The Safe Mode interface presents seven options:

**Option 1 — Restart PS5**
Ends Safe Mode and reboots the console normally. All pending updates, if any, are cancelled.

**Option 2 — Change Video Output**
Provides two sub-options:
- Change Resolution: Sets output to 1080p or 720p for displays that do not support higher resolutions
- Change HDCP Mode: Enables or disables HDCP (High-bandwidth Digital Content Protection)

**Option 3 — Update System Software**
Provides two update methods:
- Update from USB Drive: Installs a system PUP from USB media at `PS5/UPDATE/PS5UPDATE.PUP`
- Update Using Internet: Downloads and installs the latest firmware from Sony's CDN

**Option 4 — Restore Default Settings**
Resets all system settings to factory defaults without deleting user data. This option does not affect saved games, user accounts, or installed applications. It resets display, audio, network, and accessibility settings to their default states.

**Option 5 — Rebuild Database**
Scans the internal SSD and rebuilds the content database. This can resolve issues such as:
- System freezes or crashes
- Frame rate drops
- Missing game tiles or library entries
- Corrupted content database errors

The rebuild process does not delete any user data but may take 30 minutes or longer depending on the amount of content installed.

**Option 6 — Reset PS5**
Deletes all user data and restores the console to its original out-of-box state. This option does not reinstall the system software; it only clears user data, accounts, settings, and installed applications. The current firmware version is retained.

**Option 7 — Reset PS5 (Reinstall System Software)**
Full destructive recovery that wipes all data and reinstalls system software from a recovery PUP on USB media. This option:
- Deletes all user data, accounts, settings, and installed applications
- Reinstalls the system software from the recovery PUP
- Writes boot chain components including Secure Loader and EMC firmware
- Formats all user data partitions
- Restores the console to a factory-fresh state with the recovery firmware version

### USB Installation Requirements

For Safe Mode USB installation, the following requirements must be met:

- USB drive format: FAT32 or exFAT
- Directory structure: `PS5/UPDATE/PS5UPDATE.PUP`
- PUP filename: Must be all uppercase `PS5UPDATE.PUP` (case-sensitive)
- USB capacity: No minimum requirement, but must fit the PUP file (typically 1-2 GB)
- Anti-downgrade: Cannot install a firmware version lower than the currently installed version
- PUP type matching: Option 3 sub-option 1 requires system PUP; option 7 requires recovery PUP

The USB installation path is the only official offline update mechanism. It is used for initial setup (if a console shipped with outdated firmware), recovery from corrupted system software, and updating consoles without internet connectivity.

## Version History

### Version Numbering Format

The PS5 uses two version numbering schemes:

**Long version format**: `YY.SS-MM.mm.nn.nn-UU.UU.UU.U.b`

| Field | Position | Description |
|-------|----------|-------------|
| YY | 1-2 | Last 2 digits of build year (e.g., 20, 24, 26) |
| SS | 4-5 | Semester or counter: 01=first half, 02=second half (pre-2024); 03-07 per-year counter since 2024 |
| MM | 7-8 | Major version (e.g., 01, 02, 11, 13) |
| mm | 10-11 | Minor version (e.g., 00, 40) |
| nn.nn | 13-17 | Extended minor version (e.g., 00.00) |
| UU.UU.UU.U | 19-30 | Unknown version fields |
| b | 32 | Branch: 0 for internal/test, 1 for retail/CEX |

Example: `26.04-13.40.00.02-00.00.00.0.1` = FW 13.40, year 2026, first branch (04), retail (1).

**Short version format**: `MM.mm.nn`

The short format is the user-facing version number. Example: `13.40`.

### Retail Firmware History

| Version | Build ID | Date | Notes |
|---------|----------|------|-------|
| 1.00 | 20.01-01.00.00.37 | 2020-05-21 | Canada/US launch physical |
| 2.20 | 20.02-02.20.00.07 | 2020-11-06 | Official release day patch (868 MB) |
| 4.00 | 21.02-04.00.00.42 | 2021-09-03 | Major update (913.7 MB) |
| 7.00 | 23.01-07.00.00.44 | 2023-02-28 | Major update |
| 9.00 | 24.02-09.00.00.45 | 2024-03-09 | Major update |
| 10.00 | 24.06-10.00.00.46 | 2024-09-03 | Major update |
| 11.00 | 25.02-11.00.00.43 | 2025-03-04 | Major update |
| 12.00 | 25.06-12.00.00.43 | 2025-09-09 | Major update |
| 13.00 | 26.02-13.00.00.40 | 2026-03-10 | Latest major release |
| 13.40 | 26.04-13.40.00.02 | 2026-05-28 | Latest version |

### Development Firmware

TestKit firmware versions range from 0.95.00.44 to 2.30.00.05. DevKit firmware versions range from 0.83.00.20 to 2.30.00.05. Development firmware often includes debug capabilities, additional logging, and relaxed security checks not present in retail firmware.

### Changelog Highlights

Early firmware changelog entries (from official Sony release notes):

- **02.25.00** (Nov 2020): Initial post-launch update; improved system performance, fixed download queue issue where queued downloads would not start automatically
- **02.26.00** (Dec 2020): Fixed disc game deletion bug where games would be incorrectly removed from the library; fixed DualSense charging via front USB-A port in rest mode
- **02.30.00** (Feb 2021): Fixed data transfer and download cancellation issues; resolved PS4 text input errors; improved Wi-Fi stability and connectivity
- **02.50.00** (Apr 2021): Fixed PS4 disc auto-install after PS5 upgrade; added Share Factory Studio clip editing capability; system performance improvements
- **03.00.00** (Sep 2021): Major update with full changelog available externally
- **03.20.00** (Nov 2021): DualSense controller firmware update; screen reader fixes; hidden game UI fix; USB storage copy stability improvements
- **04.00.00** (Sep 2022): Major update with external changelog
- **05.00.00** (Mar 2023): Major update with external changelog

Full changelogs for versions 3.00 and later are maintained externally on Sony's official support pages and community resources.

## Relationships

- [[boot_chain]] — updates may modify boot chain components including Secure Loader and EMC firmware
- [[secure_boot]] — updates verified by secure boot chain before installation
- [[system_overview]] — update mechanism is part of system software infrastructure

## Security Considerations

The update mechanism is protected by cryptographic verification at every stage of the process:

**Pre-download Integrity**: The SHA-256 hash embedded in the PUP download URL provides integrity verification before the download begins. The updatelist.xml manifest also includes SHA-256 hashes for comparison.

**PUP Signature Verification**: The `pup` secure module (0x80021002) validates the PUP's RSA-3072 signature before any installation begins. This ensures that only Sony-signed firmware can be installed.

**Anti-Downgrade Enforcement**: The security revision system prevents installation of firmware older than the currently installed version. This check is enforced at multiple levels:
- The PUP metadata includes the firmware security revision
- The installation process checks the revision against OTP fuses
- After installation, the boot chain re-verifies the revision
- OTP fuses are burned to permanently record the minimum revision

**Known Security Considerations**:

- **CDN Token**: The obfuscated string `tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6` appears to be a static CDN authentication token. Its consistency across all regions and updates suggests it is a shared secret rather than a per-request token. If this token is required for alternative update mechanisms, its static nature could be a design weakness.

- **M.2 Key Stability**: The M.2 dummy encryption keys `01234567890123456789012345678901` have remained unchanged across firmware versions 1.00 through 12.20. This suggests that M.2 storage encryption keys are not version-dependent and do not rotate with system updates.

- **USB Recovery Path**: The Safe Mode USB recovery path represents an alternative update mechanism with a different attack surface than over-the-internet updates. The USB path does not have the same CDN authentication checks, relying instead on physical access as a mitigating control. However, the same signature verification applies, so a forged PUP file would still fail the `pup` module verification.

- **TestKit/DevKit Firmware**: Development firmware builds have different version numbering and likely use different signing keys. The availability of TestKit and DevKit firmware on third-party mirrors (Yandex) raises the possibility of firmware comparison attacks where retail and development versions are compared to identify security differences.

- **OTP Fuse Irreversibility**: The anti-rollback mechanism relies on OTP fuses that can be burned but not unburned. Once a security revision is committed to OTP, the console can never boot a firmware with a lower revision. This is a one-way ratchet that must be carefully managed to avoid bricking consoles.

- **PUP Mirror Repositories**: The documented availability of PUP files on Internet Archive, Softpedia, Darthsternie, and other mirrors provides researchers with access to firmware for analysis but also creates a distribution channel for potentially modified firmware (though signature verification prevents installation of tampered files).

## References

- https://www.psdevwiki.com/ps5/System_Software
- https://www.psdevwiki.com/ps5/Firmware_Changelog
- https://www.psdevwiki.com/ps5/System_Software_Installation
- https://www.psdevwiki.com/ps5/Safe_Mode
- https://www.psdevwiki.com/ps5/Secure_Modules
- https://www.psdevwiki.com/ps5/Secure_Loader
