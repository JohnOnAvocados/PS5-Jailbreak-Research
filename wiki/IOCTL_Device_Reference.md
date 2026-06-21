# IOCTL Device Reference

## Overview

The PS5 kernel exposes hardware and security services through a `/dev/` device model, accessed via the `sys_ioctl` syscall (0x36). Over **100 kernel device entries** are documented, providing interfaces to system co-processors and security subsystems.

IOCTL codes follow a structured format encoding direction, size, and command identifier.

## Device Tree

| Device | Purpose |
|--------|---------|
| `/dev/bar` | Backup and Restore for shellcore |
| `/dev/duid` | Disc Unique Identifier |
| `/dev/dldbg` | Dynamic Library Debug |
| `/dev/fttrm` | Film/TV Tracking Rights Management (Blu-ray DRM) |
| `/dev/icc_floyd` | TPM (Trusted Platform Module) |
| `/dev/manuauth` | Manufacturer authorization |
| `/dev/nsfsctl` | Namespace Filesystem Control |
| `/dev/pfsctldev` | PlayStation FileSystem Control |
| `/dev/pfsmgr` | PFS Manager (trophies, savedata, keystone) |
| `/dev/pup_update0` | Firmware update device |
| `/dev/rootparam` | Root PARAM.SFO/JSON verification |
| `/dev/sflash0` | Serial Flash access (2 MB) |
| `/dev/wlanbt` | Wireless LAN + Bluetooth |

## PUP Update IOCTLs

Firmware update processing subsystem. These handle decryption, verification, and installation of system software updates.

| IOCTL | Function |
|-------|----------|
| 0x20004407 | UpdateSnvs |
| 0x40047400 | updaterGetWlanDeviceId |
| 0xC001440F | GetXtsKeyNum |
| 0xC0104401 | VerifyBlsHeader |
| 0xC0104408 | genChallenge |
| 0xC010440E | UpdateFloydFw |
| 0xC010440C | IdentifyNandController |
| 0xC0104410 | verifyResponse |
| 0xC0184402 | DecryptPupHeader |
| 0xC0184403 | VerifyPupAdditionalSign |
| 0xC0184404 | VerifyPupWatermark |
| 0xC0184405 | DecryptPupSegment |
| 0xC018440A | ReadNandGroup |
| 0xC018440B | WriteNandGroup |
| 0xC0284406 | DecryptPupSegmentBlock |

## TEE IOCTLs

Trusted Execution Environment communication. Provides interface to the secure world on the PSP.

| IOCTL | Function |
|-------|----------|
| 0x400CB400 | TEE_IOC_VERSION |
| 0x8008B40B | TEE_IOC_DLM_STOP_TA_DEBUG |
| 0xC004B405 | TEE_IOC_CLOSE_SESSION |
| 0xC004B40E | TEE_SHMEM_RELEASE |
| 0xC004B40F | TEE_SET_TIMEOUT |
| 0xC008B404 | TEE_IOC_CANCEL |
| 0xC010B402 | TEE_IOC_OPEN_SESSION |
| 0xC010B403 | TEE_IOC_INVOKE |
| 0xC010B408 | TEE_IOC_DLM_GET_DEBUG_TOKEN |
| 0xC020B40D | TEE_SHMEM_MAP_SETNAME |
| 0xC028B409 | TEE_IOC_DLM_START_TA_DEBUG |
| 0xC038B40C | TEE_IOC_INIT_ASD |
| 0xC110B40A | TEE_IOC_DLM_FETCH_DEBUG_STRING |

## Manufacturing IOCTLs

The highest-value IOCTL surface — if reachable, bypasses all code signing.

| IOCTL | Function | Impact |
|-------|----------|--------|
| 0xC0184D0A | sceSblManuAuthSetManuModeInternal | Internal variant of set-manu-mode |
| **0xC0184D03** | **sceSblManuAuthSetManuMode** | Enable manufacturing mode |
| **0x40184D02** | **sceSblManuAuthUnloadSecureModule** | Unload secure modules |
| **0x40184D01** | **sceSblManuAuthLoadSecureModule** | Load unsigned secure module |

## Drive Authentication IOCTLs

Blu-ray drive pairing, AACS/CPRM key retrieval.

| IOCTL | Function |
|-------|----------|
| 0xC028530A | _sceSblDriveauthSmGetPairingNonce |
| 0xC028530B | _sceSblDriveauthSmGetPairingRequest |
| 0xC028530C | _sceSblDriveauthSmSetPairingInfo |
| 0xC028530D | _sceSblDriveauthSmSetHostKey |
| 0xC028530E | _sceSblDriveauthSmRemoveDiscKey |
| 0xC0205365 | sceSblDriveauthGetCprmDeviceKey |
| 0xC0205364 | sceSblDriveauthGetAacsDeviceKey |

## Other Notable IOCTLs

| IOCTL | Function |
|-------|----------|
| 0x80018F0A | icc_fan_change_servo_pattern |
| 0xC0068F06 | icc_fan_get_fan_manual_duty |
| 0xC0105203 | verifyDecryptRnpsBundle |
| 0x40144401 | devActInitStatus |
| 0x40184402 | sceSblDevActGetId |
| 0x4030440B | devActGenRequest |
| 0x8004B201 | gc_reset |
| 0xC0185301 | fftrm read sector |
| 0xC0185302 | fftrm write sector |
| 0xC0185303 | fftrm read idu flag |
| 0xC0185304 | fftrm write idu flag |

## Co-Processors Backing the Device Tree

| Co-Processor | Type | Role |
|-------------|------|------|
| MP0 (PSP) | AMD Platform Security Processor | Secure boot, key management, cryptographic services |
| MP1 (SMU) | Xtensa CPU | Power management, clock gating, thermal monitoring |
| MP3 (TEE) | ARM (PSP-based) | PlayReady SL3000 DRM, secure media paths |
| MP4 (A53) | ARM Cortex-A53 | I/O co-processing, memory management offload |

## Attack Surface Notes

- **PUP IOCTLs** involve multiple decryption/verification steps — potential parsing vulnerabilities in `DecryptPupHeader`, `DecryptPupSegment`, `VerifyPupAdditionalSign`, `VerifyPupWatermark`
- **TEE IOCTLs** expose trusted application management — `TEE_IOC_DLM_START_TA_DEBUG` and `TEE_IOC_DLM_FETCH_DEBUG_STRING` are particularly interesting
- **Manufacturing IOCTLs** are restricted but if reachable from userland would bypass signed module requirements
- **Drive authentication IOCTLs** handle AACS/CPRM key retrieval — potential cryptographic key extraction targets
- **fftrm IOCTLs** provide low-level NAND sector access — could be used for persistent storage modification

## References

- `sources/web/psdevwiki/kernel/ioctl.md` — IOCTL source data
- `research/kernel/kernel.md` — kernel architecture, device tree
- `research/kernel/syscall_catalog.md` — syscall dispatch, naming conventions
- `research/hardware/southbridge_analysis.md` — manufacturing IOCTL details
- [psdevwiki: IOCTL](https://www.psdevwiki.com/ps5/IOCTL)
- [psdevwiki: Devices](https://www.psdevwiki.com/ps5/Devices)
