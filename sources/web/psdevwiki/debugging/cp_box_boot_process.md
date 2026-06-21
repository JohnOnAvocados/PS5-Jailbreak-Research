# CP Box Boot Process
## Source URL
https://www.psdevwiki.com/ps5/CP_Box_Boot_Process
## System Layer
debugging
## Summary
Complete boot log from a PS5 EAP (Embedded Application Processor) running FreeBSD 9.0-RELEASE on a Marvell PJ4C ARM core at 500 MHz with 512 MB DDR3 RAM. Shows initialization sequence: KBL boot, kernel loading, device enumeration (USB, SDIO, I2C, GPIO), network configuration via DHCP, CP firmware update check, and service daemon startup.
## Key Concepts
- EAP SDK Version: 5.501.000
- Sycorax Version: 01.00.01.01
- Subsystem ID: 0x00040100 (Belize2 A0)
- CPU: Marvell PJ4C rev 2 (ARM), 500 MHz
- DDR clock: 800 MHz
- 512 MB real memory, ~473 MB available
- FreeBSD 9.0-RELEASE ARM
- Devices: UART, RTC, SDHCI/SDIO, Belize GbE, XHCI USB 3.0
- DECI5 debug interface initialization
- I2C GPIO controllers (TCA9539) and LED driver (TLC59116)
- Ethernet MAC: 78:c8:81:d8:51:1b
- DHCP network configuration
- CP firmware update sequence (status 0 = no update needed)
- Services: emcd, uartd, disabler, DECI5s, DECI5
- Boards ID: 0x2001010101010501
- Total boot time ~50 seconds to CP ready
## System Role
Communication Processor boot sequence reference
