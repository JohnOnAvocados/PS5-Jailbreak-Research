# Serial Flash
## Source URL
https://www.psdevwiki.com/ps5/Serial_Flash
## System Layer
hardware
## Summary
The PS5 uses a Winbond W25Q16JVNIM serial flash (2 MB, 150mil package). Pinout diagram provided for SPI connection. Can be dumped via Raspberry Pi GPIO using flashrom tool.
## Key Concepts
- Winbond W25Q16JVNIM serial flash
- 2 MB (16 Mbit) capacity
- 150mil SOIC package
- SPI interface: /CS, /MISO, /WP, GND, VCC, /HOLD, SCLK, MOSI
- Dumpable via Raspberry Pi SPI interface
- flashrom tool compatibility
## System Role
Boot configuration and non-volatile parameter storage
