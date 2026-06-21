# EMC

## Source
inbox\emc.md

## System Layer
firmware

## Summary
# EMC
## Source URL
https://www.psdevwiki.com/ps5/EMC
## System Layer
security
## Summary
The PS5 EMC (Embedded Micro Controller) uses hardware revision CXD90061GG with software versions ranging from 0.7.6 (prototype) to 1.14.3 (FW 9.20). EMC version can be extracted from serial flash at offset 0x4000 (0x7E000 bytes) using blsunpack. ## Key Concepts
- CXD90061GG hardware revision
- EMC v0.7.6: SDK 0.85.070 (prototype/DevKit)
- EMC v1.0.4: FW 1.01-1.14 (TestKit, Retail)
- EMC v1.2.3: FW 2.XX (TestKit)
- EMC v1.4.2: FW 3.00 (Retail)
- EMC v1.6.0: FW 4.00 (TestKit)
- EMC v1.8.2: FW 5.00 (Retail)
- EMC v1.8.3: FW 5.50 (Retail)
- EMC v1.14.3: FW 9.20 (Retail)
- Extracted from serial flash offset 0x4000, length 0x7E000
- SLB2 segment extraction via blsunpack
- C0080001 file contains EMC version
## System Role
Embedded controller firmware for power-on initialization

## Concepts
emc, retail, testkit, blsunpack, controller, cxd90061gg, embedded, extracted, flash, hardware, offset, prototype, ps5, revision, serial

## Related Notes
- [[../nodes/25q16jvnim]]
- [[../nodes/aw_xm501]]
- [[../nodes/backup_and_restore]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/build_strings]]
- [[../nodes/cxd90061gg]]
- [[../nodes/devices]]
- [[../nodes/dualsense]]
- [[../nodes/dualsense_dfu_modes]]
- [[../nodes/error_codes]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_titles]]
- [[../nodes/game_update_information]]
- [[../nodes/ioctl]]
- [[../nodes/jigkick_files]]
- [[../nodes/kernel_functions]]
- [[../nodes/languages]]
- [[../nodes/lapse_kernel_exploit]]
