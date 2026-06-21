# PKG

**Source:** https://www.psdevwiki.com/ps5/PKG
**System Layer:** Filesystem
**Summary:** PS5 firmware PKG version table mapping PKG IDs to minimum firmware versions (MINVER), covering devkit, testkit, and retail releases.
**Key Concepts:** PKG ID, MINVER, PKG number offset, firmware version, devkit prototype, testkit, retail
**System Role:** Firmware package versioning system that tracks which minimum system software version corresponds to each PKG build.

## Overview

- Everything installed as OS to the PS5 is done via PKG
- Lower PKG Number = Lower Version
- PKG Number XXXX - Min Version XXXX
- PKG Number Offset: 0x1C73E0
- Min Ver Offset: 0x1C7468 (Endian Swapped)

## PKG Version Table

| PKG ID | MINVER | Notes |
|---|---|---|
| ???-???? | 0.78 | PS5 INTERNAL DEVKIT PROTOTYPE |
| PKG-0378 | 1.05 | PS5 DEVKIT |
| PKG-0384 | 1.05 | PS5 TESTKIT |
| PKG-0388 | 1.00 | PS5 RETAIL LAUNCH DAY |
| PKG-0430 | ???? | N/A |
| PKG-0711 | 2.00 | N/A |
| PKG-0911 | 3.00 | N/A |
| PKG-1307 | ???? | N/A |
| PKG-1407 | 5.00 | N/A |
| PKG-1438 | 5.02 | N/A |
| PKG-1506 | 5.10 | N/A |
| PKG-1590 | 5.50 | N/A |
| PKG-1591 | 5.50 | N/A |
| PKG-1766 | ???? | N/A |
| PKG-1906 | ???? | N/A |
| PKG-1976 | ???? | N/A |
| PKG-2066 | ???? | N/A |
| PKG-2094 | 6.50 | N/A |
| PKG-2266 | 7.00 | PS5 TRINITY DEVKIT PROTOTYPE |
| PKG-2347 | 7.00 | N/A |
