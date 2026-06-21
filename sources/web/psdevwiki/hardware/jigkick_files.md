# Jigkick Files

## Source URL
https://www.psdevwiki.com/ps5/Jigkick_Files

## System Layer
Hardware / Manufacturing

## Summary
Jigkick PKG contains specialized firmware files used for Blu-ray drive recovery, manufacturing updates, and diagnostics.

## Key Concepts

### PKG File Contents

| Entry | Description |
|-------|-------------|
| BD_EM_BOOT_FW | Recovery Mediatek Blu-ray Firmware for Emergency Purposes (BD Drive FW brick recovery) |
| BD_MAIN_FW | Same as 30XR.bix (Blu-ray Drive Main Firmware) |
| BD_VEEPROM_DATA | Blu-ray EEPROM Data |
| GAME_OS_DIAG_2ND | Special Zip File (see GAME_OS_DIAG_2ND) |
| MANU_UPDATER | `manufacturing_updater.self` (renamed) |
| NET_LOAD_DIAG | Unknown, ~7 MiB size |

## System Role
Jigkick files are used during manufacturing and repair for reflashing Blu-ray drive firmware, diagnostics, and recovery. The BD_EM_BOOT_FW entry provides emergency brick recovery for the Mediatek BD controller.
