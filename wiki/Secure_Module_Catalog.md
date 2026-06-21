# Secure Module Catalog

## Overview

Secure modules are trusted service modules dispatched by the **SceSbl** (Sony Secure Boot Loader) authentication manager. Each module has a service ID in the **0x8002xxxx** range and runs in an isolated execution context — compromise of one module does not affect others. Modules handle cryptographic operations, key management, firmware verification, DRM, and hardware authentication.

The authentication manager (authmgr, 0x80021000) is the primary entry point for SELF verification, segment loading, and secure dispatch.

## Module Table

| Service ID | Name | Key Functions | Security Role |
|-----------|------|---------------|---------------|
| 0x80021000 | **authmgr** | sceSblAuthMgrAuthHeader, sceSblAuthMgrLoadBlock, sceSblAuthMgrSmLoad | SELF verification, segment loading — primary dispatch |
| 0x80021001 | **kms** | sceSblKmsAllocKmbSlotForPprPkg, sceSblKmsSetKeyId, sceSblKmsClearKeyId | Key management — opaque handle-based key access, keys never exposed |
| 0x80021002 | **pup** | PUP update processing functions | Firmware update verification and installation |
| 0x80021003 | **pfs** | sceSblPfsmgrUpdateIcvTable | PFS filesystem integrity verification |
| 0x80021004 | **driveauth** | sceSblDriveauthGetAacsDeviceKey, sceSblDriveauthGetCprmDeviceKey | BD drive authentication, AACS/CPRM key retrieval |
| 0x80021005 | **pltauth** | sceSblPltAuth2GenC1, sceSblPltAuth2VeriR1C2GenR2 | Platform challenge-response authentication |
| 0x80021006 | **npdrm** | sceSblNpDrmCheckDebugClock, sceSblNpDrmGetCurrentDebugTick | NP DRM enforcement |
| 0x80021007 | **devact** | sceSblDevActGetId, sceSblDevActGetRemainingTime | Device activation state management |
| 0x80021008 | **qafutkn** | QA/UToken services | QA token and user token verification |
| 0x80021009 | **sysveri** | sceSblSysVeriInitialize | System verification |
| 0x8002100A | **otpaccess** | OTP fuse read services | One-Time Programmable fuse access |
| 0x8002100B | **manu** | sceSblManuAuthSetManuMode, sceSblManuAuthLoadSecureModule, sceSblManuAuthUnloadSecureModule | **Manufacturing mode** — highest-value target |
| 0x8002100C | **fttrm** | sceSblFttrmReadSector, sceSblFttrmWriteSector | Film/TV Tracking Rights Management (Blu-ray) |
| 0x8002100D | **srtc** | sceSblSrtcGetCurrentSecureTick | Secure Real-Time Clock |
| 0x8002100E | **rootparam** | sceSblRootParamVerifyPprRootParam | Root PARAM.SFO/JSON verification |
| 0x8002100F | **exthdd** | sceSblExternalHDDVerifyMetadata | External HDD metadata verification |
| 0x80021010 | **cloudsd** | sceSblPfsSaveDataUpdateAuthCode | Cloud SaveData authentication |
| 0x80021011 | **bar** | sceSblBarCreateContext, sceSblBarUpdateEncrypt, sceSblBarUpdateDecrypt | Backup and Restore |
| 0x80021012 | **otprsvaccess** | Reserved OTP access | Additional OTP fuse services |
| 0x80021013 | **diskid** | Disc ID services | Disc identification |
| 0x80021014 | **idata** | Installation data services | Game installation management |
| 0x80021015 | **ddd** | Digital Delivery Driver | Digital content delivery |
| 0x80021016 | **otpctrl** | OTP control | OTP fuse programming |
| 0x80021017 | **ncdt** | Non-volatile Config Data Table | Configuration data management |
| 0x80021018 | **hidauth** | HID authentication | Peripheral authentication |

## High-Value Targets

### Manufacturing Module (0x8002100B) — Highest Value
If reachable from userland:
- `sceSblManuAuthSetManuMode` — Enable manufacturing mode (persists across reboots)
- `sceSblManuAuthLoadSecureModule` — Load unsigned secure module (**bypasses all signature verification**)
- `sceSblManuAuthUnloadSecureModule` — Unload security modules (authmgr, pup, sysveri, npdrm)

### Key Management (0x80021001)
Opaque handle-based API — keys never leave the module in plaintext. All cryptographic operations go through KMS handles, preventing key extraction even with kernel access.

### Platform Authentication (0x80021005)
Challenge-response protocol between console and Sony servers. Used for device activation, DRM authorization, and online service authentication.

## Dispatch Mechanism

Modules are dispatched through the authmgr (0x80021000) which:
1. Receives service requests with target module ID and function ID
2. Validates caller authorization (credential check, capability flags)
3. Routes to the target module's handler
4. Returns results through shared memory interfaces

The exact dispatch mechanism — how function IDs map to handlers, calling conventions, argument validation — is not publicly documented.

## Cross-Module Communication

Modules can call each other through the authmgr dispatch. Known or suspected cross-module paths:
- authmgr → kms (request key for SELF verification)
- pup → kms (request key for PUP decryption)
- manu → authmgr (bypass authentication for unsigned modules)
- pltauth → otpaccess (read fuses for challenge generation)

## Research Gaps

- Complete function identifier catalog for each module
- Input validation coverage — do all functions validate parameters?
- Cross-module privilege boundaries — can one module exploit another?
- Shared memory interface between modules and kernel
- Manufacturing module reachability conditions on retail consoles
- Relationship between authmgr-secure modules and PSP TEE applications

## References

- `research/kernel/kernel.md` — kernel architecture with full module table
- `research/security_model/security_model.md` — Auth IDs, PAIDs, key hierarchy
- `research/hardware/southbridge_analysis.md` — key chain, CP Box
- [psdevwiki: Secure Modules](https://www.psdevwiki.com/ps5/Secure_Modules)
- [psdevwiki: SceSbl Functions](https://www.psdevwiki.com/ps5/SceSbl_Functions)
