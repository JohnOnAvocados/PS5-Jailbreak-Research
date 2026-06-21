# Master Boot Record

**Source:** https://www.psdevwiki.com/ps5/Master_Boot_Record
**System Layer:** Filesystem
**Summary:** PS5 Master Boot Record (MBR) structure for NAND group 0, describing the boot partition layout with secure loader and CoreOS regions.
**Key Concepts:** MBR, NAND group 0, sector size, revision, SecLDR, CoreOS, SonyInteractiveEntertainmentLLC magic
**System Role:** Boot partition header that defines the layout of the initial boot firmware stored in NAND flash.

## Overview

Main header of NAND group 0. Updated per firmware when necessary. Sector size = 0x200.

## Structure

| Offset | Size | Description | PS5 Value | Notes on Other Consoles |
|---|---|---|---|---|
| 0x0 | 0x20 | Magic | "SonyInteractiveEntertainmentLLC \0" | "Sony Computer Entertainment Inc." on Vita and PS4 |
| 0x20 | 0x4 | Revision | Always 5 | 3 on Vita, 4 on PS4 |
| 0x24 | 0x4 | Total Size of Container | 0x2000000 sectors = 64 MiB | Varies on Vita/PS4 |
| 0x28 | 0x8 | Unknown | D8 A0 AC 8E 4B 9D F9 1B | All zeroes on Vita and PS4 |
| 0x30 | 0x4 | Start of SecLDR | 0x4 × 0x200 = 0x800 | Same on Vita |
| 0x34 | 0x4 | Size of SecLDR | 0x359 × 0x200 = 0x6B200 | Same on Vita |
| 0x38 | 0x4 | Start of CoreOS | 0x3C4 × 0x200 = 0x78800 | Different on Vita |
| 0x3C | 0x4 | Padding | 0x00000000 | Different on Vita |
