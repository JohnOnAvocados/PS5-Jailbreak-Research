# PS2 Emulation

## Source
inbox\ps2_emulation.md

## System Layer
hypervisor

## Summary
# PS2 Emulation

## Source URL
https://www.psdevwiki.com/ps5/PS2_Emulation

## System Layer
System Software

## Summary
PS2 emulation on PS5 is done via two methods: a PS5-native PS2 emulator (since May 2024) or the PS4 PS2 emulator running through PS4 backward compatibility. ## Key Concepts

### Method 1: PS4 SDK PS2 Emulator (via PS4 Emulation)
- Uses PS2emu from PS4 PKG, running through PS4 emulation layer on PS5
- Available since FW ~2.00
- Games have CUSA (PS4) Title ID prefix
- Version numbering: XX.YY (PS4 format)

### Method 2: PS5 SDK PS2 Emulator (Native)
- Direct PS5 PS2 emulator, not relying on PS4 emulation
- Available since May 2024
- Games have PPSA (PS5) Title ID prefix
- PKG size differs from PS4 version
- Version numbering: XX.000.0YY
- **Supports game savestates** (unlike the PS4 emulator path)

## System Role
Important architectural distinction: PS5 has a native PS2 emulator compiled with PS5 SDK (since mid-2024) separate from the PS4-compat PS2 emulator path. The native emulator supports savestates, indicating tighter hypervisor/kernel integration.

## Concepts
ps4, emulator, ps2, ps5, emulation, since, native, sdk, system, version, available, games, layer, method, numbering

## Related Notes
- [[../nodes/amd_secure_encrypted_virtualization]]
- [[../nodes/aw_xm501]]
- [[../nodes/backwards_compatibility]]
- [[../nodes/build_strings]]
- [[../nodes/crossline_breaking_amd_sev]]
- [[../nodes/cxd90063r1]]
- [[../nodes/demo_games]]
- [[../nodes/disc_drive_media]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_update_information]]
- [[../nodes/games]]
- [[../nodes/gbatemp_ps5_exploit_guide]]
- [[../nodes/hypervisor]]
- [[../nodes/kernel_overview]]
- [[../nodes/keystone]]
- [[../nodes/mac_address]]
- [[../nodes/mast1c0re_jit_pipeline]]
- [[../nodes/mt3613ct]]
- [[../nodes/official_firmware]]
- [[../nodes/passcode]]
