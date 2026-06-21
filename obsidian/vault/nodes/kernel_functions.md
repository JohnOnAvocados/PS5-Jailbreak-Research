# Kernel Functions

## Source
inbox\kernel_functions.md

## System Layer
firmware

## Summary
# Kernel Functions

## Source URL
https://www.psdevwiki.com/ps5/Kernel_Functions

## System Layer
Kernel / Security

## Summary
SceSbl kernel function dispatch codes organized by service ID. These are kernel-level entry points accessed via the authentication manager subsystem. ## Key Concepts

### Service IDs and Functions

**80021000 - Authentication Manager**
- SELF header verification, segment loading, RnpsBundle decrypt
- Key functions: `sceSblAuthMgrAuthHeader`, `sceSblAuthMgrLoadBlock`, `sceSblAuthMgrSmLoad`

**80021001 - Key Management Service**
- Key slot allocation, key ID management
- `sceSblKmsAllocKmbSlotForPprPkg`, `sceSblKmsSetKeyId`, `sceSblKmsClearKeyId`

**80021003 - PlayStation File System Manager**
- `sceSblPfsmgrUpdateIcvTable` — ICV table update

**80021004 - Drive Authenticator**
- Disc authentication, BD drive pairing, AACS/CPRM key retrieval
- Functions for PS4 disc auth, PPR disc registration

**80021005 - Platform Authenticator**
- Platform authentication challenge/response
- `sceSblPltAuth2GenC1`, `sceSblPltAuth2VeriR1C2GenR2`

**80021006 - Network Platform DRM**
- NP DRM debug clock management
- `sceSblNpDrmCheckDebugClock`, `sceSblNpDrmGetCurrentDebugTick`

**80021007 - Device Activation**
- DevKit/TestKit activation, passcode management
- `sceSblDevActGetId`, `sceSblDevActGetRemainingTime`

**80021009 - System Verification**
- `sceSblSysVeriInitialize`

**8002100B - Manufacturing Authentication**
- Manufacturing mode management
- `sceSblManuAuthSetManuMode`, `sceSblManuAuthLoadSecureModule`

**8002100C - Fttrm**
- FTTRM (Flash Translation Table Region Manager) — NAND sector access
- IDU flag read/write, sector read/write

**8002100D - Secure RTC**
- Secure tick counters for NP DRM
- `sceSblSrtcGetCurrentSecureTick`

**8002100E - Root Parameter**
- Root parameter verification (PPR, PS4)
- `sceSblRootParamVerifyPprRootParam`

**8002100F - External Hard Drive Disc**
- External HDD metadata verification
- `sceSblExternalHDDVerifyMetadata`

**80021010 - PFS Save Data**
- Save data auth code management
- `sceSblPfsSaveDataUpdateAuthCode`

**80021011 - Backup And Restore**
- BAR encryption/decryption context management
- `sceSblBarCreateContext`, `sceSblBarUpdateEncrypt`/`Decrypt`

## System Role
These kernel function codes are the interface to SceSbl's security services.

## Concepts
management, kernel, key, authentication, disc, functions, manager, system, verification, drive, drm, platform, service, activation, auth

## Related Notes
- [[../nodes/auth_ids]]
- [[../nodes/backup_and_restore]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
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
- [[../nodes/languages]]
- [[../nodes/lapse_kernel_exploit]]
- [[../nodes/more_system_information]]
- [[../nodes/official_firmware]]
