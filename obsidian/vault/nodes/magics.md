# Magics

## Source
inbox\magics.md

## System Layer
boot_chain

## Summary
# Magics

## Source URL
https://www.psdevwiki.com/ps5/Magics

## System Layer
Security / Boot

## Summary
Lists known magic bytes/identifiers used in PS5 firmware binaries to identify different component types. ## Key Concepts

| Magic | Component |
|-------|-----------|
| 54 14 F5 EE | Certified File (SELF, PUP) |
| E4 DB 7C 02 | IPL / Secure Loader |
| AA F9 8F D4 | Southbridge EMC |
| 1D 33 47 77 | EAP Kernel / EAP KBL Firmware |
| 47 AB 6B EF | Floyd ICC Firmware |
| 55 AA 6B E9 | VBIOS |
| 5F 46 56 48 | BIOS |

## System Role
Magic numbers are used as file/header identifiers throughout the PS5 firmware to allow boot components to recognize and validate different binary formats before processing.

## Concepts
firmware, magic, ps5, boot, component, different, eap, file, identifiers, magics, system, allow, before, binaries, binary

## Related Notes
- [[../nodes/amd_platform_security_processor]]
- [[../nodes/amd_secure_processor]]
- [[../nodes/amd_security]]
- [[../nodes/arm_trusted_firmware]]
- [[../nodes/arxiv]]
- [[../nodes/arxiv_org_eprint_archive]]
- [[../nodes/auth_ids]]
- [[../nodes/backwards_compatibility]]
- [[../nodes/blackhat_archives]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/boot_logo]]
- [[../nodes/build_strings]]
- [[../nodes/codenames]]
- [[../nodes/cxd90063r1]]
- [[../nodes/dualsense_hid_commands]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_titles]]
- [[../nodes/game_update_information]]
- [[../nodes/games]]
- [[../nodes/homebrew_enabler]]
