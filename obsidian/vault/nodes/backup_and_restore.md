# Backup And Restore

## Source
inbox\backup_and_restore.md

## System Layer
firmware

## Summary
# Backup And Restore

## Source URL
https://www.psdevwiki.com/ps5/Backup_And_Restore

## System Layer
System Software

## Summary
The Backup And Restore (BAR) utility allows PS5 users to back up and restore user data (settings, saved data, screenshots, video clips, games, patches) to/from an external USB drive. ## Key Concepts
- Creates `archive.dat` files on USB drive containing backup of built-in storage data
- Not present on systems with FW 1.02 and older that never connected to PSN
- Present at least since FW 2.10 (2020-11-06)
- Uses PFS (PlayStation File System) encryption for backup data
- Related kernel functions: `sceSblBarCreateContext`, `sceSblBarUpdateAad`, `sceSblBarUpdateDecrypt`, `sceSblBarUpdateEncrypt`, `sceSblBarFinishDecrypt`, `sceSblBarFinishEncrypt`

## System Role
The BAR system uses SceSbl encryption functions to create secure encrypted backups. Understanding the archive.dat format and associated crypto operations is relevant for data recovery and forensic analysis.

## Concepts
data, system, backup, restore, archive, bar, dat, drive, encryption, functions, present, ps5, usb, uses, allows

## Related Notes
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/build_strings]]
- [[../nodes/devices]]
- [[../nodes/disc_drive_media]]
- [[../nodes/dualsense]]
- [[../nodes/dualsense_dfu_modes]]
- [[../nodes/emc]]
- [[../nodes/error_codes]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_titles]]
- [[../nodes/game_update_information]]
- [[../nodes/ioctl]]
- [[../nodes/jigkick_files]]
- [[../nodes/kernel_functions]]
- [[../nodes/languages]]
- [[../nodes/lapse_kernel_exploit]]
- [[../nodes/more_system_information]]
- [[../nodes/official_firmware]]
