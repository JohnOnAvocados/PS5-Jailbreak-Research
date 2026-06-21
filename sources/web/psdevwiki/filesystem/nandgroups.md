# Nandgroups

**Source:** https://www.psdevwiki.com/ps5/Nandgroups
**System Layer:** Filesystem
**Summary:** Description of the PS5 NAND flash group layout across the six SSD chips, containing IPL, CoreOS, WiFi firmware, and EFC firmware.
**Key Concepts:** NAND groups, FW_PSP_BL, FW_WIFI, FW_IDATA, FW_EFC_FW0, FW_EFC_FW1, IPL, CoreOS, Titania
**System Role:** NAND flash partitioning scheme that organizes boot firmware, WiFi firmware, and EFC controller firmware across physical SSD chips.

## Overview

Out of the 6 SSD chips in the PS5, 3 contain critical firmware data organized into NAND Groups.

## NAND Group Info

| Group Index | Size | Contains | Notes |
|---|---|---|---|
| 0 | 0x4000000 | FW_PSP_BL | Critical NAND Group |
| 1 | 0x3E00000 | FW_WIFI + FW_14 + FW_IDATA | Critical NAND Group |
| 2 | 0x237800 | FW_EFC_FW0 + FW_EFC_FW1 | Can be replaced with a chip of same FW_EFC version |

## Firmware Descriptions

### FW_PSP_BL
- Contains the IPL (Initial Program Loader) and CORE_OS
- Size: 0x4000000

### FW_WIFI
- WiFi firmware
- Size: 0x0200000

### FW_14
- Reserved (filled with zeroes)
- Size: 0x3A00000

### FW_IDATA
- Individual Data or IDSTORAGE
- Size: 0x0200000

### FW_EFC_FW0
- Titania EFC FW (IPL?)
- Size: 0x0181000

### FW_EFC_FW1
- Titania EFC FW (KBL?)
- Size: 0x00B6800
