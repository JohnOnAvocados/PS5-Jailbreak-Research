# Serial Database
## Source URL
https://www.psdevwiki.com/ps5/Serial_Database
## System Layer
hardware
## Summary
Partial serial number to partial IDPS (IDPS) match database for PS5 retail, testkit, and prototype units. Maps serial prefixes to model numbers and minimum firmware versions.
## Key Concepts
- **Serial Location**: sflash0 at 0x1C7250
- **IDPS Location**: Kernel dump, +0x38 bytes after string "SSLP"
- **Model Number Location**: sflash0 at 0x1C7230
- **Prototypes**: DUTP-DSN18AAK-W5 (0.85.070 min), DAU-DGW18AEK-J9 (7.00 min)
- **Testkits**: DFI-T1000AA (1.05 min), DFI-T7000AA (9.20 min, PS5 Pro Testkit)
- **Retail Models**: CFI-1008A (Russia 1.00), CFI-1015A (US 1.00), CFI-1016A (Europe 1.00), CFI-1002A (Australia 1.00), CFI-1100A (Japan), CFI-1116A (Europe), CFI-1215A (US), CFI-1216A (Europe), CFI-1208A (Russia)
- **Region Codes in IDPS**: 82 (US/CA), 84 (US UCS), 87 (Europe EU8), 89 (Australia), 8A (Asia), 8C (Russia)
## System Role
Serial number to hardware identity mapping database for PS5 models.
