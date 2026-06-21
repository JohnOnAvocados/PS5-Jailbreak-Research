# SceSbl Functions

## Source
inbox\scesbl_functions.md

## System Layer
boot_chain

## Summary
# SceSbl Functions

## Source URL
https://www.psdevwiki.com/ps5/SceSbl_Functions

## System Layer
Security

## Summary
Complete function list for the SceSbl (Secure Boot Loader) system library. These functions provide authentication, encryption, key management, and secure boot functionality. ## Key Concepts

### Auth Manager Functions
- `_sceSblAuthMgrCheckSelfHeader`, `_sceSblAuthMgrCheckSelfSegmentCompressed`, `_sceSblAuthMgrGetElfSegmentInformation`, `_sceSblAuthMgrGetSelfInfo`, `_sceSblAuthMgrGetSelfSegmentInformation`, `_sceSblAuthMgrLoadMultipleSelfBlocks`, `_sceSblAuthMgrLoadSelfBlock`, `_sceSblAuthMgrReadSegmentDataWithCallback`, `_sceSblAuthMgrSetHvConf`, `_sceSblAuthMgrSmFinalize`, `_sceSblAuthMgrSmIsLoadable2`, `_sceSblAuthMgrSmLoadMultipleSelfBlocks`, `_sceSblAuthMgrSmLoadSelfBlock`, `_sceSblAuthMgrSmUnload`, `_sceSblAuthMgrSmVerifyDecryptRnpsBundle`
- `sceSblAuthMgrAuthHeader`, `sceSblAuthMgrCheckSegmentCompressed`, `sceSblAuthMgrFinalize`, `sceSblAuthMgrIsLoadable`, `sceSblAuthMgrLoadBlock`, `sceSblAuthMgrLoadMultipleBlocks`, `sceSblAuthMgrSmLoad`, `sceSblAuthMgrVerifyDecryptRnpsBundle`

### Development/Activation Functions
- `_sceSblDevActGetRemainingTime`, `_sceSblDevActSmCheckPassCodeData`, `_sceSblDevActSmDeleteStatus`, `_sceSblDevActSmExit`, `_sceSblDevActSmGenActHeader`, `_sceSblDevActSmGenActRequest`, `_sceSblDevActSmGenPassCodeData`, `_sceSblDevActSmGetId`, `_sceSblDevActSmInitStatus`, `_sceSblDevActSmSetStatus`
- `sceSblDevActGetId`, `sceSblDevActGetRemainingTime`

### Drive Authentication Functions
- `_sceSblDriveauthSmDriveData`, `_sceSblDriveauthSmDriveGetId2`, `_sceSblDriveauthSmExit`, `_sceSblDriveauthSmGetDpData`, `_sceSblDriveauthSmGetPairingNonce`, `_sceSblDriveauthSmGetPairingRequest`, `_sceSblDriveauthSmGicGetData`, `_sceSblDriveauthSmRemoveDiscKey`, `_sceSblDriveauthSmSetHostKey`, `_sceSblDriveauthSmSetPairingInfo`
- `sceSblDriveAuthPs4Disc`, `sceSblDriveAuthPs4DiscGetId`, `sceSblDriveAuthPs4DiscReset`, `sceSblDriveAuthPs4DiscResume`, `sceSblDriveAuthPs4DiscSuspend`, `sceSblDriveAuthRegisterPprDisc`, `sceSblDriveAuthRegisterPs4Disc`, `sceSblDriveAuthUnregisterDisc`, `sceSblDriveauthGetAacsDeviceKey`, `sceSblDriveauthGetCprmDeviceKey`, `sceSblDriveauthGetGicData`, `sceSblDriveauthGetId2`

### Key Management Functions
- `sceSblKmsClearKeyId`, `sceSblKmsAllocSignedKeyHdl`, `sceSblKmsTranscribeKeyHdl2KeyId`, `sceSblKmsSetKeyId`, `sceSblKmsAllocKmbSlot`

### Manufacturing Authentication
- `_sceSblManuAuthSmGetManuExpire`, `_sceSblManuAuthSmGetManuMode`, `_sceSblManuAuthSmSetManuExpire`, `_sceSblManuAuthSmSetManuMode`
- `sceSblManuAuthLoadSecureModule`, `sceSblManuAuthSetManuMode`, `sceSblManuAuthSetManuModeInternal`, `sceSblManuAuthUnloadSecureModule`

### Platform Authentication (PltAuth)
- `sceSblPltAuth2GenC1`, `sceSblPltAuth2GetKdsMac`, `sceSblPltAuth2Initialize`, `sceSblPltAuth2Result`, `sceSblPltAuth2VeriR1C2GenR2`, `sceSblPltAuthSmExitWait`

### Cryptographic Service
- `sceSblServiceCrypt`, `sceSblServiceCryptAsync`, `sceSblServiceMailbox`, `sceSblServiceSpawn`, `sceSblServiceSysMailSend`, `sceSblServiceWaitForExit`, `sceSblSmServiceEventHandler`

### Secure Region (SecReg)
- `sceSblSecRegInitialize`, `sceSblSecRegResume`, `sceSblSecRegSuspend`

### NP DRM / Tick
- `sceSblNpDrmCheckDebugClock`, `sceSblNpDrmGetCurrentDebugTick`, `sceSblNpDrmGetInitStatus`, `sceSblNpDrmSetCurrentDebugTick`
- `sceSblSrtcGetCurrentNpDrmTick`, `sceSblSrtcGetCurrentSecureTick`

### PFS/Storage
- `_sceSblPfsSaveDataUpdateAuthCodeIoctl`, `sceSblPfsClearKey`, `sceSblPfsSaveDataUpdateAuthCode`, `sceSblPfsmgrUpdateIcvTable`

### Other Notable Functions
- `sceSblSsVerifyKeystone` - Keystone verification
- `sceSblEnvelopeOpen`, `sceSblEnvelopeOpen2` - Envelope crypto operations
- `sceSblRngGetRandomNumber` - Random number generation
- `sceSblRcMgrIsStoreMode`, `sceSblRcMgrGetQafDescription`, `sceSblRcMgrGetQafExpirationTime`, `sceSblRcMgrGetQafGeneration` - Region/Restriction checks
- `sceSblPupExpirationGetStatus` - PUP expiration
- `sceSblSelfGetPaidFromPlainHeaderSize` - SELF parsing
- `sceSblTmrEncAmmPt`, `sceSblTmrDecAmmPt`, `sceSblTmrExport`, `sceSblTmrMap`, `sceSblTmrUnmap` - TMR (Trusted Memory Region) operations
- `sceSblSvpMapPrdyTeeArea`, `sceSblSvpUnmapPrdyTeeArea` - Secure Video Path TEE area
- `sceSblMp1Initialize`, `sceSblMp1DumpContext`, `sceSblMp1EnableErrorDetection`, `sceSblMp1DisableErrorDetection` - Memory Protection
- `sceSblDriverSendMsg`, `sceSblDriverSendMsgPol` - SBL driver communication
- `sceSblDcnOpenScanInRegion`, `sceSblDcnOpenScanOutRegion`, `sceSblDcnCloseScanOutRegion` - Display connection

## System Role
SceSbl forms the core of PS5's security subsystem, handling module authentication (SELF verification), key management, drive authentication (disc verification), NP DRM tick management, manufacturing authentication, platform authentication, secure boot, PFS encryption, and trustzone operations.

## Concepts
authentication, functions, secure, key, management, boot, operations, region, scesbl, system, verification, drive, drm, encryption, manufacturing

## Related Notes
- [[../nodes/amd_platform_security_processor]]
- [[../nodes/amd_security]]
- [[../nodes/arm_trusted_firmware]]
- [[../nodes/arxiv]]
- [[../nodes/arxiv_org_eprint_archive]]
- [[../nodes/auth_ids]]
- [[../nodes/backup_and_restore]]
- [[../nodes/backwards_compatibility]]
- [[../nodes/blackhat_archives]]
- [[../nodes/boot_logo]]
- [[../nodes/build_strings]]
- [[../nodes/disc_drive_media]]
- [[../nodes/dualsense_hid_commands]]
- [[../nodes/homebrew_enabler]]
- [[../nodes/hypervisor_loader]]
- [[../nodes/ieee_xplore_digital_library]]
- [[../nodes/ioctl]]
- [[../nodes/kernel_functions]]
- [[../nodes/keystone]]
- [[../nodes/magics]]
