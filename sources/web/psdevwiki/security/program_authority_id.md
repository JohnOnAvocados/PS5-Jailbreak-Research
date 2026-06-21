# Program Authority ID

## Source URL
https://www.psdevwiki.com/ps5/Program_Authority_ID

## System Layer
Security

## Summary
Lists Program Authority IDs (PAIDs) assigned to PS5 system processes. Each PAID is a 64-bit hex value that identifies the authority level of a running program/process.

## Key Concepts

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
Program Authority IDs are used by the kernel and secure loader to validate and categorize running processes. The PAID determines what security policies apply to a process and what resources it can access. The prefix `4801` denotes kernel-level authority while `4800` denotes system-level processes.
