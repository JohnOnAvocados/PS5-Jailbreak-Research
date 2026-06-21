# Secure Loader

## Source URL
https://www.psdevwiki.com/ps5/Secure_Loader

## System Layer
Security / Boot ROM

## Summary
The PS5 Secure Loader is the Initial Program Loader (IPL) running on the AMD Platform Security Processor (PSP). It is the main loader of the Hypervisor, Hypervisor Loader, and Kernel.

## Key Concepts

### Header Structure (at NAND Group 0 offset 0x800)

| Offset | Offset from NAND Group 0 | Size | Description | Notes |
|--------|--------------------------|------|-------------|-------|
| 0x0 | 0x800 | 4 | Magic | E4 DB 7C 02 |
| 0x4 | 0x804 | 4 | Header Size | Little Endian (0x400) |
| 0x8 | 0x808 | 4 | Entry Point | Little Endian (0xB0) |
| 0xC | 0x80C | 4 | Body Size | Little Endian (e.g. 0x631D0) |
| 0x10 | 0x810 | 0x10 | Padding | Zeroes |
| 0x20 | 0x820 | 0x20 | SHA256 of decrypted body | Verified from 0x400 to 0x635D0 |
| 0x40 | 0x840 | 0xB0 | Padding | ASCII "0123456789abcdef" with zeroes |
| 0xF0 | 0x8F0 | 1 | Flag? | 0x80 |
| 0xF1 | 0x8F1 | 0x2B | Padding | all zeroes |
| 0x11C | 0x91C | 4 | Security Revision | See revision table |
| 0x120 | 0x920 | 0x20 | Revision Nonce | SHA256 of IPL revision; after this, IPL is AES-CBC encrypted (2 layers) |
| 0x140 | 0x940 | 0xC0 | MetaData? | May contain keyrings and metadata digest |
| 0x200 | 0xA00 | 0x200 | RSA4096 Header Signature? | |
| 0x400 | 0xC00 | ~0x631D0 | Body | | |

### Security Revision Values

| Value | Firmware Versions |
|-------|-------------------|
| 00 00 00 01 | 0.85.007-1.XX |
| 00 00 00 07 | 1.00-6.02 |
| 00 00 00 FF | 6.50 |
| 00 00 03 FF | 7.00-7.61 |
| 00 00 0F FF | 8.00-8.60 |
| 00 00 3F FF | 9.00-9.60 |
| 00 00 FF FF | 10.00-10.60 |
| 00 03 FF FF | 11.00+ |

### Revision Nonce Collection

| Revision | Hash |
|----------|------|
| 0xA0 | E3 D9 8F 94 6E B3 2A 6D C8 A8 09 C2 6B 6F 4F 91 0E CA 63 59 00 48 4D 99 BA 12 39 E5 DF 74 5C 40 |
| 0xB0 | 55 18 14 A6 79 F1 4D 09 31 8B EC 56 DD EA 43 44 55 27 9A C4 7D 0C 5C 7E 14 91 D6 EF B2 1F 2B 48 |
| 0xC0 | B3 59 79 B6 23 19 7C 34 6E E6 B1 62 8E 18 98 96 8C 66 DC DF 1C 96 5F 4C 77 07 30 07 78 4C 4E 6A |
| 0xD0 | 1C B3 91 12 79 BA 5E 83 42 C9 C9 6B 2F C5 49 B3 DE BF D7 3D D6 B6 97 4E 07 84 DF 7B E8 BD 21 39 |
| 0xE0 | FD 50 C2 9C C4 AE 88 21 1B CA 0B C5 09 1C 1D BF D6 A4 DC 07 DB F8 C0 B2 A6 17 FD 1D BE E0 3A 3B |
| 0xF0 | 6F 20 B4 5B 4F CB 66 67 71 5F 4B 0E E4 90 7C C2 CB 41 47 0A 59 B2 26 E0 D4 F0 D0 1B 67 E8 80 50 |
| 0x100 | 50 C0 E3 99 33 83 2B 2B A6 89 FF AE 29 4A 44 92 03 8E 99 74 A8 BC A6 CC 0C 2E 9C 69 9D 37 2A 22 |

## System Role
The Secure Loader is the first code executed after boot ROM on the PSP. It verifies and loads the next stage boot components. The RSA4096 signature protects the header integrity. The revision nonce system ensures that only authorized firmware versions can be booted, and is updated per firmware release to prevent downgrade attacks.
