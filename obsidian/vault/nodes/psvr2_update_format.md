# PSVR2 Update Format

## Source
inbox\psvr2_update_format.md

## System Layer
firmware

## Summary
# PSVR2 Update Format
## Source URL
https://www.psdevwiki.com/ps5/PSVR2_Update_Format
## System Layer
hardware
## Summary
PSVR2 firmware update file format with magic "CUP!" and a structured file entry table. ## Key Concepts
- **Header** (offset/size):
 - 0x0000/4: Magic "CUP!"
 - 0x0004/4: Unknown (0x02011003)
 - 0x0008/8: Unknown (0x0000000000000001)
- **File Entry Structure** (at offset 0x10, 7 entries):
 - 0x0000/4: File Type (0x10000000, 0x2000000B, 0x2000000C, 0x2000000D, 0x2000000E, 0x2FFFFFFE, 0x2FFFFFFF)
 - 0x0004/4: Offset of File Relative to Header (0x300)
 - 0x0008/4: Size of File
 - 0x000C/4: Padding/Zeroes
- After entries: 0x90 bytes padding, 0x30 bytes unknown blob, 0xC0 bytes padding, 0x40 bytes unknown blob, 0xC0 bytes final padding, then file data
## System Role
PSVR2 firmware update package binary format specification.

## Concepts
file, bytes, padding, unknown, format, offset, psvr2, update, blob, cup, entries, entry, firmware, header, magic

## Related Notes
- [[../nodes/backup_and_restore]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/devices]]
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
- [[../nodes/magics]]
- [[../nodes/more_system_information]]
- [[../nodes/official_firmware]]
