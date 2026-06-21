# Bond
## Source URL
https://www.psdevwiki.com/ps5/Bond
## System Layer
hardware
## Summary
Codename of the DualSense controller. Firmware is stored under /system_ex/etc/. Contains Banana (main), Venom (audio), and Betty firmware components.
## Key Concepts
- **Bond**: Codename for DualSense
- **Firmware Location**: /system_ex/etc/ on PS5
- **Banana Firmware Structure** (offset/size/description):
  - 0x00/0x40: Copyright String
  - 0x40/0x10: Build Date String
  - 0x50/0x10: Build Hour String
  - 0x62/0x2: Product ID (e.g., 0xCE6)
  - 0x68/0x4: Full Size
  - 0x6C/0x4: SDK Version
  - 0x70/0x4: Firmware Version
  - 0x74/0x4: SwSeries
  - 0x78/0x4: ControllerVersion
- **Venom Firmware Structure**: Type string "VenomB", build date, firmware version, body size
- **Betty Firmware Structure**: Type string "BettyBND", build date, body size
- **Example Versions**: Nov 2020 (SwSeries 0x0004, ControllerVersion 0x0210, FW 2.50)
## System Role
DualSense controller firmware structure documentation.
