# Devices

## Source
inbox\devices.md

## System Layer
firmware

## Summary
# Devices
## Source URL
https://www.psdevwiki.com/ps5/Devices
## System Layer
kernel
## Summary
Comprehensive listing of PS5 kernel devices accessible through IOCTL. Covers Platform Security Processor (PSP/MP0), System Management Unit (SMU/MP1), Trusted Execution Environment (TEE/MP3), A53 co-processor (MP4), and detailed IOCTL command tables for each device subsystem. ## Key Concepts
- /dev/ devices accessible via IOCTL syscalls from kernel
- MP0 (PSP): AMD Platform Security Processor - security functions
- MP1 (SMU): Xtensa CPU for power/clock/thermal management
- MP2 (SFP): Sensor Fusion Processor (not present on PS5)
- MP3 (TEE): Trusted Execution Environment on PSP, PlayReady SL3000 DRM
- MP4 (A53): ARM Cortex-A53 co-processor for I/O and memory management
- Over 100 kernel device entries documented
- /dev/bar: Backup and Restore for shellcore
- /dev/duid: Disc Unique ID
- /dev/dldbg: Dynamic Library Debug
- /dev/fttrm: Film/TV Tracking Rights Management (Blu-ray DRM)
- /dev/icc_floyd: TPM (Trusted Platform Module)
- /dev/manuauth: Manufacturer authorization
- /dev/nsfsctl: Namespace Filesystem Control
- /dev/pfsctldev: PlayStation FileSystem Control
- /dev/pfsmgr: PFS Manager (trophies, savedata, keystone)
- /dev/pup_update0: Firmware update device
- /dev/rootparam: Root PARAM.SFO/JSON verification
- /dev/sflash0: Serial Flash access (2MB)
- /dev/wlanbt: Wireless LAN + Bluetooth
## System Role
Kernel device node reference for PS5 IOCTL interface

## Concepts
dev, kernel, device, devices, ioctl, management, ps5, platform, processor, psp, security, system, trusted, a53, accessible

## Related Notes
- [[../nodes/amd_platform_security_processor]]
- [[../nodes/amd_secure_processor]]
- [[../nodes/amd_security]]
- [[../nodes/arxiv]]
- [[../nodes/backup_and_restore]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/build_strings]]
- [[../nodes/dualsense]]
- [[../nodes/dualsense_dfu_modes]]
- [[../nodes/emc]]
- [[../nodes/error_codes]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_titles]]
- [[../nodes/game_update_information]]
- [[../nodes/ioctl]]
- [[../nodes/iommu_architecture]]
- [[../nodes/jigkick_files]]
- [[../nodes/kernel_functions]]
