# PS Portal

## Source
inbox\ps_portal.md

## System Layer
firmware

## Summary
# PS Portal
## Source URL
https://www.psdevwiki.com/ps5/PS_Portal
## System Layer
hardware
## Summary
PlayStation Portal remote player device runs a custom Android 13 operating system. Used for interacting with PS5 via Remote Play. ## Key Concepts
- **OS**: Custom Android 13
- **PS Portal Master Key**: 35 15 A8 8F 33 55 7D F1 33 FB F2 08 D6 3B 0A AF (Galois Counter Mode)
- **Update URLs**: JSON endpoint at dwc.dl.playstation.net for firmware info
- **PUP Structure**: Magic "DWCP", Type=1, Full Size field, Version field
- **Boot Modes**:
 - Fastboot: Android fastboot utility, screen stays black, activated by holding minus button while connecting USB
 - Recovery: Exposes 2 HID devices (PS Controller, PS Link Audio Device), screen stays black
- **Firmware updates**: Differential (.pup) and full packages, available for versions 1.0.0 through 6.0.1+
## System Role
Remote play device for streaming PS5 games.

## Concepts
android, device, portal, ps5, remote, system, black, custom, fastboot, field, firmware, full, key, play, playstation

## Related Notes
- [[../nodes/amd_platform_security_processor]]
- [[../nodes/aw_xm501]]
- [[../nodes/backup_and_restore]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/build_strings]]
- [[../nodes/codenames]]
- [[../nodes/cpu]]
- [[../nodes/cxd90063r1]]
- [[../nodes/demo_games]]
- [[../nodes/devices]]
- [[../nodes/disc_drive_media]]
- [[../nodes/dualsense]]
- [[../nodes/dualsense_dfu_modes]]
- [[../nodes/emc]]
- [[../nodes/error_codes]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_titles]]
- [[../nodes/game_update_information]]
