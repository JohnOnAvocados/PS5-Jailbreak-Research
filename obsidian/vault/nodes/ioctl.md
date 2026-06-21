# IOCTL

## Source
inbox\ioctl.md

## System Layer
firmware

## Summary
# IOCTL

## Source URL
https://www.psdevwiki.com/ps5/IOCTL

## System Layer
Kernel

## Summary
List of IOCTL codes for PS5 kernel device drivers, organized by subsystem. ## Key Concepts

### PUP Related IOCTLs
- `0x20004407` UpdateSnvs
- `0x40047400` updaterGetWlanDeviceId
- `0xC001440F` GetXtsKeyNum
- `0xC0104401` VerifyBlsHeader
- `0xC0104408` genChallenge
- `0xC010440E` UpdateFloydFw
- `0xC010440C` IdentifyNandController
- `0xC0104410` verifyResponse
- `0xC0184402` DecryptPupHeader
- `0xC0184403` VerifyPupAdditionalSign
- `0xC0184404` VerifyPupWatermark
- `0xC0184405` DecryptPupSegment
- `0xC018440A` ReadNandGroup
- `0xC018440B` WriteNandGroup
- `0xC0284406` DecryptPupSegmentBlock

### TEE Related IOCTLs
- `0x400CB400` TEE_IOC_VERSION
- `0x8008B40B` TEE_IOC_DLM_STOP_TA_DEBUG
- `0xC004B405` TEE_IOC_CLOSE_SESSION
- `0xC004B40E` TEE_SHMEM_RELEASE
- `0xC004B40F` TEE_SET_TIMEOUT
- `0xC008B404` TEE_IOC_CANCEL
- `0xC010B402` TEE_IOC_OPEN_SESSION
- `0xC010B403` TEE_IOC_INVOKE
- `0xC010B408` TEE_IOC_DLM_GET_DEBUG_TOKEN
- `0xC020B40D` TEE_SHMEM_MAP_SETNAME
- `0xC028B409` TEE_IOC_DLM_START_TA_DEBUG
- `0xC038B40C` TEE_IOC_INIT_ASD
- `0xC110B40A` TEE_IOC_DLM_FETCH_DEBUG_STRING

### Manufacturing Mode IOCTLs
- `0xC0184D0A` sceSblManuAuthSetManuModeInternal
- `0xC0184D03` sceSblManuAuthSetManuMode
- `0x40184D02` sceSblManuAuthUnloadSecureModule
- `0x40184D01` sceSblManuAuthLoadSecureModule

### Uncategorized IOCTLs
- `0xC028530A` _sceSblDriveauthSmGetPairingNonce
- `0xC028530B` _sceSblDriveauthSmGetPairingRequest
- `0xC028530C` _sceSblDriveauthSmSetPairingInfo
- `0xC028530D` _sceSblDriveauthSmSetHostKey
- `0xC028530E` _sceSblDriveauthSmRemoveDiscKey
- `0xC0205365` sceSblDriveauthGetCprmDeviceKey
- `0xC0205364` sceSblDriveauthGetAacsDeviceKey
- `0x80018F0A` icc_fan_change_servo_pattern
- `0xC0068F06` icc_fan_get_fan_manual_duty
- `0xC0105203` verifyDecryptRnpsBundle
- `0x40144401` devActInitStatus
- `0x40184402` sceSblDevActGetId
- `0x4030440B` devActGenRequest
- `0x8004B201` gc_reset
- `0xC0185301` fftrm read sector
- `0xC0185302` fftrm write sector
- `0xC0185303` fftrm read idu flag
- `0xC0185304` fftrm write idu flag

## System Role
IOCTLs provide the usermode-to-kernel interface for device-specific operations. PUP IOCTLs are critical for firmware update processing, TEE IOCTLs for trusted execution environment communication, and manufacturing IOCTLs for factory/debug operations.

## Concepts
ioctls, fftrm, ioctl, flag, idu, kernel, manufacturing, operations, ps5, pup, read, related, sector, system, tee

## Related Notes
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
- [[../nodes/idu_mode]]
- [[../nodes/iommu_architecture]]
- [[../nodes/jigkick_files]]
- [[../nodes/kernel_functions]]
- [[../nodes/kernel_overview]]
- [[../nodes/languages]]
- [[../nodes/lapse_kernel_exploit]]
