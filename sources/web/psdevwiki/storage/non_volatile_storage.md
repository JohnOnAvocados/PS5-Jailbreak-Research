# Non Volatile Storage
## Source URL
https://www.psdevwiki.com/ps5/Non_Volatile_Storage
## System Layer
Storage / NVS (Non-Volatile Storage)
## Summary
The NVS (Non-Volatile Storage) holds console-unique identifiers, tokens, flags, registry flags, and semi-permanent configuration data stored in the serial flash. It is organized into banks and blocks with areas including EMCAREA, DSAREA, PDAREA, OSAREA, G6AREA, and their backups.
## Key Concepts
- EMCAREA (Bank 0/Block 0): Platform ID, Ethernet MAC addresses, EMC error logs
- DSAREA (Bank 0/Block 1): Unknown area
- PDCSAREA (Bank 0/Block 2): Kiban ID, Product Serial (hw_info), Product Name (hw_model), Model Code, SocCuid (SoC Unique ID), Viop Data, WLAN MAC Address, BD Addresses, ImagePackageId, Manufacturing Process Flags
- OSAREA (Bank 0/Block 4): Coldboot flag, EAP UART, GPU packet, firmware versions, passcode status, QA flag token, ACF token, registry manager data, IDU mode, manufacturing mode
- BACKUPAREA (Bank 1/Block 0): Backup of OSAREA region
- BACKUPAREA2 (Bank 1/Block 1): Partial backup of EMCAREA
- ImagePackageId maps firmware images to specific hardware models (DFI-T1000AA, CFI-1015B, etc.)
- EAP Magic bytes (E5 E5 E5 01) mark valid areas
## System Role
Provides persistent storage for console identity, hardware configuration, network addresses, manufacturing flags, firmware version tracking, and QA-related tokens used during boot and system operation.
