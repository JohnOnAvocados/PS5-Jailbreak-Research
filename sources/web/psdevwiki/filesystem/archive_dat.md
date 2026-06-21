# Archive.dat

**Source:** https://www.psdevwiki.com/ps5/Archive.dat
**System Layer:** Filesystem
**Summary:** Binary container format (SIECAF) used for PS5 Backup and Restore (BAR) data, replacing the PS4 archive.dat structure.
**Key Concepts:** SIECAF, BAR backup, encryption, HMAC, segment table, segment signature, little-endian
**System Role:** Backup archive format for the PS5 Backup and Restore feature, storing encrypted and authenticated data segments.

## Overview

The archive.dat file stores PS3, PS4, and PS5 Backup And Restore (BAR) data. The PS5 version uses the SIECAF file structure, changed from its PS4 and PS3 predecessors. All data is little-endian.

Structure: Header, Repeating Section Meta Blocks, Repeating Section Hash Blocks.

## Header

| Offset | Size | Description |
|---|---|---|
| 0x0 | 0x8 | Magic `0x5349454341460000` ("SIECAF\0\0") |
| 0x8 | 0x8 | Version |
| 0x10 | 0x8 | Unknown (0x1) |
| 0x18 | 0x8 | Unknown (0x1) |
| 0x20 | 0x10 | Encryption IV (null bytes; removed in metadata blocks) |
| 0x30 | 0x4 | Unknown size |
| 0x34 | 0x4 | Unknown size |
| 0x38 | 0x4 | Unknown size |
| 0x3C | 0x4 | Padding |
| 0x40 | 0x8 | Number of Segments |
| 0x48 | 0x8 | File Offset |
| 0x50 | 0x8 | File Size |

## Section Meta Block

| Offset | Size | Description |
|---|---|---|
| 0x0 | 0x8 | Section ID |
| 0x8 | 0x8 | Section Start Offset |
| 0x10 | 0x8 | Aligned Section Length |
| 0x18 | 0x8 | Hash Key ID (0x0000000000000003) |
| 0x20 | 0x8 | Encryption Key ID (0x0000000000000001) |
| 0x28 | 0x10 | Encryption IV (null bytes) |
| 0x38 | 0x8 | Unaligned Section Length |

## Section Hash Block

| Offset | Size | Description |
|---|---|---|
| 0x0 | 0x8 | Section ID |
| 0x8 | 0x10 | Hash (128-bit) |
| 0x18 | 0x18 | Padding |

## Tools

- [ps5-bar-tool](https://github.com/c0w-ar/ps5-bar-tool)
