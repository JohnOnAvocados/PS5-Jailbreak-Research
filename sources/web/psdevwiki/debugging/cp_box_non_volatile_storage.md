# CP Box Non Volatile Storage
## Source URL
https://www.psdevwiki.com/ps5/CP_Box_Non_Volatile_Storage
## System Layer
debugging
## Summary
CP Box NVS is stored on the main serial flash (Winbond 25Q256JVEQ) with multiple configuration partitions. Defines platform ID, MAC address, DDR capacity, EAP core startup flags, error logging, serial number, and toggle flags for EMC/UART checksums.
## Key Concepts
- Serial flash: Winbond 25Q256JVEQ (32 MB)
- NVS stored at flash offset 0x1C4000
- Platform ID at offset 0x00: CP Box = 20 01 01 01 01 01 04 01, Carlo CP = 10 01 02 01 02 01 02 02
- MAC address at offset 0x21
- DDR capacity byte at offset 0x60: 05 = 4 GiB, 07 = 16 GiB
- EAP core startup flag at offset 0x57: 00 = enabled
- EMC checksum validation flag at offset 0x1010: FF = disabled
- EMC UART flag at offset 0x1012: FF = enabled
- EAP UART flag at offset 0x531F: FF = disabled
- Error log at offset 0x1200 (0x400 bytes)
- Serial Number at offset 0x4000
## System Role
CP Box configuration storage map
