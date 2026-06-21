# System Software (Official Firmware)

## Source
inbox\official_firmware.md

## System Layer
firmware

## Summary
# System Software (Official Firmware)

## Source URL
https://www.psdevwiki.com/ps5/System_Software

## System Layer
System Software

## Summary
Comprehensive reference for PS5 system software versions, PUP file structure, download URLs, and version history from 1.00 (2020) through 13.40 (June 2026). ## Key Concepts

### PUP Download URLs
- **updatelist.xml**: `http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6/list/<TLD>/updatelist.xml`
- **PS5UPDATE.PUP**: `http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6/image/<YYYY_MMDD>/<TYPE>_<SHA256>/PS5UPDATE.PUP?dest=<TLD>`
- Obfuscated string: `tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6`

### Version Format (Long)
`YY.SS-MM.mm.nn.nn-UU.UU.UU.U.b`
- YY = last 2 digits of build year
- SS = semester (01=first, 02=second before 2024; per-year counter 03-07 since 2024)
- MM = major version, mm = minor version, nn.nn = extended minor
- UU.UU.UU.U = unknown version format
- b = 0 or 1 (1 on CEX/retail)

### Version Format (Short)
`MM.mm.nn`

### Retail Firmware History (selected key versions)
- 1.00 (20.01-01.00.00.37, 2020-05-21) - Canada/US launch physical
- 2.20 (20.02-02.20.00.07, 2020-11-06) - Official release day patch (868MB)
- 4.00 (21.02-04.00.00.42, 2021-09-03) - Major update (913.7MB)
- 7.00 (23.01-07.00.00.44, 2023-02-28) - Major update
- 9.00 (24.02-09.00.00.45, 2024-03-09) - Major update 
- 10.00 (24.06-10.00.00.46, 2024-09-03) - Major update
- 11.00 (25.02-11.00.00.43, 2025-03-04) - Major update
- 12.00 (25.06-12.00.00.43, 2025-09-09) - Major update
- 13.00 (26.02-13.00.00.40, 2026-03-10) - Latest major
- 13.40 (26.04-13.40.00.02, 2026-05-28) - Latest version

### TestKit Versions
0.95.00.44 through 2.30.00.05

### DevKit Versions
0.83.00.20 through 2.30.00.05

### PUP Types
- `system` - Full system software
- `recovery` - Recovery mode package
- `system_ex` - System extension package

### PUP Mirror Repositories
- Internet Archive (Wayback Machine)
- Midnight Archive
- Softpedia
- Darthsternie
- DarkSoftware
- Yandex (testkit/devkit)

## System Role
Essential reference for obtaining PS5 firmware files for analysis, understanding version numbering schemes, and tracking firmware release history across all console variants (retail, testkit, devkit).

## Concepts
update, major, system, version, ps5, pup, firmware, official, software, versions, devkit, format, history, retail, testkit

## Related Notes
- [[../nodes/backup_and_restore]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/build_strings]]
- [[../nodes/codenames]]
- [[../nodes/devices]]
- [[../nodes/dualsense]]
- [[../nodes/dualsense_dfu_modes]]
- [[../nodes/emc]]
- [[../nodes/error_codes]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_titles]]
- [[../nodes/game_update_information]]
- [[../nodes/games]]
- [[../nodes/ioctl]]
- [[../nodes/jigkick_files]]
- [[../nodes/kernel_functions]]
- [[../nodes/languages]]
- [[../nodes/lapse_kernel_exploit]]
