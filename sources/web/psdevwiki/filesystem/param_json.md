# Param.json

**Source:** https://www.psdevwiki.com/ps5/Param.json
**System Layer:** Filesystem
**Summary:** Complete specification of the PS5 application metadata file (param.json), which replaced param.sfo from previous PlayStation consoles.
**Key Concepts:** JSON metadata, application category, DRM type, title ID, age level, localized parameters, disc structure, PSML/PSSR, kernel memory settings, savedata sharing
**System Role:** Application metadata descriptor defining identity, capabilities, requirements, and configuration for all PS5 software titles.

## Overview

PS5 uses param.json instead of param.sfo from PSP/PS3/PS4/Vita. Three types exist: `param.json`, `origin-param.json`, and `target-param.json`.

## Fields

### addcont.serviceIdForSharing
List of shared content IDs for cross-title/PS4 save sharing. Format: `EP1004-PPSA01721_00` & `EP1004-CUSA00411_00`

### ageLevel
Dictionary of age ratings per region (73 regions including default). Region codes: AE, AR, AT, AU, BE, BG, BH, BO, BR, CA, CH, CL, CN, CO, CR, CY, CZ, DE, DK, EC, ES, FI, FR, GB, GR, GT, HK, HN, HR, HU, ID, IE, IL, IN, IS, IT, JP, KR, KW, LB, LU, MT, MX, MY, NI, NL, NO, NZ, OM, PA, PE, PL, PT, PY, QA, RO, RU, SA, SE, SG, SI, SK, SV, TH, TR, TW, UA, US, UY, ZA

### amm
Memory management settings:
- `multimapVaRangeInGib`: Integer (e.g. 512)
- `vaRangeInGib`: Integer (e.g. 512)

### applicationCategoryType
Integer identifying app type:

| Value | Category |
|---|---|
| 0 | Native Game |
| 65536 | Prospero Native Media App |
| 65792 | RNPS Media App |
| 66048 | Web Based Media App |
| 131328 | System Built-in App |
| 131584 | Big Daemon |
| 16777216 | ShellUI |
| 33554432 | Daemon |
| 50331648 | CommonDialog |
| 67108864 | ShellApp |

### applicationDrmType
String: `upgradable`, `standard`, `demo`, `free`

### asa
Anti-piracy/security attributes:
- `asa01`: String "2000000" (required if asa set)
- `asa08`: String "10"
- `asa09`: String "1" (required for massSize)
- `asa10`: String "1400"
- `sign`: List of 8 hex strings (64 chars each)

### attribute
Bitmask integer:

| Value | Description |
|---|---|
| 0 | No logout support, no HDR |
| 1 | Supports logout, no HDR |
| 536870912 | No logout, HDR support |
| 1073741824 | No logout, no suspend on PS button, no HDR, HDCP 2.2 |
| 1107296256 | No logout, no suspend, TTS, no HDR, HDCP 2.2 |
| 1644167168 | No logout, no suspend, TTS, HDR, HDCP 2.2 |

### attribute2
| Value | Description |
|---|---|
| 0 | No Content Search |
| 4 | Supports Content Search |

### attribute3
Controls video-out info, HFR, Share Library Capture, auto-scaling.

### backgroundBasematType
String: `Linear` or `EllipseNarrow`

### conceptId
Overarching ID shared across all regions for a title.

### contentBadgeType
| Value | Type |
|---|---|
| 0 | N/A |
| 1 | Game |
| 2 | Other |

### contentId, contentVersion
Content identifier and version string (e.g. "01.000.000").

### deeplinkUri
URI scheme for deep-linking into system settings and features. Supports URLs, pssettings:, psgm:, pstc:, psappinst:, psgamedatamgmt:, pspatchcheck:, psbase:, pscontentinfo:, ppscontentinfo:, pssmdlg: schemes.

### disc
Array describing disc contents:
- `contents[]`: {contentId, contentType ("PS5GD")}
- `files[]`: {digests, fileName}
- `localizedParameters`: {defaultLanguage, "<code>": {titleName}}
- `masterDataId`: e.g. "PPSA01234"
- `role`: "Play Disc"

### discNumber, discTotal
Integer disc numbers for multi-disc games.

### downloadDataSize
Integer download size.

### gameIntent.permittedIntents
List of intent types: `launchActivity`, `launchMultiplayerActivity`, `launchByCustomParameters`, `joinSession`

### kernel
Memory sizing:
- `cpuPageTableSize`: Integer
- `flexibleMemorySize`: Integer
- `gpuPageTableSize`: Integer

### localizedParameters
Dictionary per language code (31 supported languages): ar-AE, cs-CZ, da-DK, de-DE, el-GR, en-GB, en-US, es-419, es-ES, fi-FI, fr-CA, fr-FR, hu-HU, id-ID, it-IT, ja-JP, ko-KR, nl-NL, no-NO, pl-PL, pt-BR, pt-PT, ro-RO, ru-RU, sv-SE, th-TH, tr-TR, uk-UA, vi-VN, zh-Hans, zh-Hant. Each contains `titleName`.

### massSize
Integer (requires asa01 & asa09).

### masterVersion
String (e.g. "01.00").

### originContentVersion
String (e.g. "01.000.000").

### psml
PSSR (PlayStation Spectral Super Resolution) metadata:
- `mfsrVersion`: String. Known versions: 9.00, 9.40, 9.60, 10.20, 11.00, 11.60, 13.00, 13.00A

### pubtools
Contains `creationDate` (datetime), `loudnessSnd0` (float), `submission` (bool), `toolVersion` (string).

### requiredSystemSoftwareVersion
Hex string (e.g. "0x0114000000000000").

### savedata
Cross-title save data sharing:
- `titleIdForSharing`: String
- `titleIdForTransferring`: String array
- `titleIdForTransferringPs4`: String array

### sdkVersion
Hex string (e.g. "0x0100000000000000").

### titleId
String (e.g. "PPSA12345").

### usbDir
List: `MUSIC`, `VIDEO`, `PSNOW`

### userDefinedParam1-4
Integer user-defined parameters.

### versionFileUri
URL string for update version check.
