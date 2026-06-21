# Program Authority ID

## Source
inbox\program_authority_id.md

## System Layer
firmware

## Summary
# Program Authority ID

## Source URL
https://www.psdevwiki.com/ps5/Program_Authority_ID

## System Layer
Security

## Summary
Lists Program Authority IDs (PAIDs) assigned to PS5 system processes. Each PAID is a 64-bit hex value that identifies the authority level of a running program/process. ## Key Concepts

| PAID | Type | Notes |
|------|------|-------|
| 4801000000000000 | Kernel | |
| 4800000000000022 | mini-syscore.elf | |
| 480000000000001f | SceSysAvControl.elf | |
| 4800000000000007 | SceSysCore.elf | |
| 4800000000000005 | orbis_audiod.elf | |
| 4800000000000009 | AgcCompositor.elf | |
| 4800000000000010 | SceShellCore | |
| 480000000000000f | SceShellUI | |
| 4800000000000015 | SceAvCapture | |
| 4800000000000012 | SceGameLiveStreaming | |
| 4800000000000014 | ScePartyDaemon | |
| 4800000000001004 | SceMediaCoreServer | |
| 4800000000000019 | SceRemotePlay | |
| 4800000000000028 | ScePsNowClientDaemon | |
| 480000001000000e | SceSpZeroConf | |
| 4800000000000037 | SceSocialScreenMgr | |
| 480000000000003e | SceVoiceAndAgent | |
| 4800000000001003 | SceRedisServer | |
| 4800000000001002 | SceJSCd | |
| 480000000000100b | SceSystemLogger2 | |
| 480000000000100d | SceUpdatePupUtil | |
| 4800000000001015 | SceVrTrackerDaemon | |
| 480000000000001d | fs_cleaner.elf | |
| 4800000010000010 | webrtc_daemon.self | |
| 4800000000001005 | SceVideoCore2K | |
| 4800000010000009 | SceDiscPlayer | |
| 4800000010000001 | BdmvPlayerCore.elf | |
| 4800000010000005 | bdj.elf | |

## System Role
Program Authority IDs are used by the kernel and secure loader to validate and categorize running processes.

## Concepts
elf, authority, program, paid, processes, system, denotes, ids, kernel, process, ps5, running, security, access, agccompositor

## Related Notes
- [[../nodes/amd_platform_security_processor]]
- [[../nodes/auth_ids]]
- [[../nodes/aws_nitro_system]]
- [[../nodes/backup_and_restore]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/build_strings]]
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
- [[../nodes/kernel_overview]]
