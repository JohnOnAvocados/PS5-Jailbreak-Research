# 25Q16JVNIM

## Source URL
https://www.psdevwiki.com/ps5/25Q16JVNIM

## System Layer
Hardware / Storage

## Summary
Winbond W25Q16JVXXX serial flash memory chip used in PS5. 16MB (128 Mbit) serial flash connected via SPI, storing boot-related data including the Secure Loader and NVS data.

## Key Concepts

### Pinout

| Pad | Internal Name | External Name | Type | Description |
|-----|---------------|---------------|------|-------------|
| 1 | /CS | /S50_SSB_SF_CS | | Chip Select Input |
| 2 | DO(IO1) | S50_SSB_SF_SIO1 | | Data Output (Data Input Output 1) |
| 3 | /WP(IO2) | 3.3V_SS_PG1 | | Write Protect Input (Data Input Output 2) |
| 4 | GND | GND | | Ground |
| 5 | DI(IO0) | S50_SSB_SF_SIO0 | | Data Input (Data Input Output 0) |
| 6 | CLK | S50G_SSB_SF_SCLK | | Serial Clock Input |
| 7 | /HOLD or /RESET(IO3) | 3.3V_SS_PG1 | | Hold or Reset Input (Data Input Output 3) |
| 8 | VCC | 3.3V_SS_PG1 | | Power Supply |

### Datasheet
- Winbond W25Q16JVXXX Datasheet
- Winbond W25Q16JVXX Datasheet

## System Role
The 25Q16JVNIM serial flash stores critical boot firmware including the Secure Loader IPL. It connects to the southbridge via SPI. Understanding its layout is essential for hardware-level analysis of the PS5 boot chain.
