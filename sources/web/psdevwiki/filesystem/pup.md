# PUP

**Source:** https://www.psdevwiki.com/ps5/PUP
**System Layer:** Filesystem
**Summary:** PlayStation Update Package (PUP) file format and firmware update installation phase sequence.
**Key Concepts:** SLB2 magic, PUP file table, Recovery PUP, Update PUP, update phases, bootloader images
**System Role:** Firmware update container format used for system software installation and recovery.

## Format

PUP (PlayStation Update) files contain firmware updates. They can be downloaded from Sony's firmware update page or via updatelist.xml.

Types:
- **Recovery PUP**: Contains the entire firmware, reinstalls everything
- **Update PUP**: Only updates changed components

### Data Structure

| Offset | Name | Value/Description |
|---|---|---|
| 0x00 | Magic | Always `53 4C 42 32` ("SLB2") |
| 0x30 | File table | Contains a list of all files in the PUP |

## Update Installation Phase Order

| Phase | ID | File | Description |
|---|---|---|---|
| 1 | 18 | usb_pdc_salina_c0.bls | System firmware phase 1 |
| 2 | 16 | emc_salina_c0.bls | System firmware phase 2 |
| 3 | 11 | titania.bls | System firmware phase 3 |
| 4 | 14 | eap_kbl.bin | System firmware phase 4 |
| 5 | 4 | mbr.bin | System firmware phase 5 |
| 6 | 259 | oberon_sec_ldr_c0.bin | System firmware phase 6 (secure loader) |
| 7 | 5 | kernel.bin | System firmware phase 7 (reboots here) |
| 8 | 513 | wlanbt.bin | WiFi/BT firmware (encrypted) |
| 9 | 515 | ssd0.system_b | System partition B (encrypted) |
| 10 | 516 | ssd0.system_ex_b | System EX partition B (encrypted) |
| 11 | 519 | ssd0.preinst | Preinst partition (mounts system) |
| 12 | 2000 | bluray.bin | Blu-ray drive firmware (encrypted) |
