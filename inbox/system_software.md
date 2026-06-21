# System Software
## Source URL
https://www.psdevwiki.com/ps5/System_Software
## System Layer
System Software / Firmware
## Summary
The PS5 System Software (firmware) is distributed via PS5UPDATE.PUP files hosted on SIE servers. Version information is provided through an updatelist.xml file, and PUP download URLs follow a structured pattern with region abbreviations, build dates, and SHA256 hashes.
## Key Concepts
- **updatelist.xml**: XML file on SIE servers listing available firmware versions and download URLs. URL format: `http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/<OBFUSCATED_STRING>/list/<TLD>/updatelist.xml`
- **PS5UPDATE.PUP**: PlayStation Update Package file. URL format: `http://<EXTLD>.ps5.update.playstation.net/update/ps5/official/<OBFUSCATED_STRING>/image/<YYYY_MMDD>/<TYPE>_<SHA256>/PS5UPDATE.PUP?dest=<TLD>`
- **Version Format (Long)**: `YY.SS-MM.mm.nn.nn-UU.UU.UU.U.b` where YY=build year last digits, SS=semester/counter, MM=major, mm=minor, nn.nn=extended minor, UU.*=unknown, b=0/1 (1 on CEX)
- **Version Format (Short)**: `MM.mm.nn` where MM=major, mm=minor, nn=auto_update_version derived value
- **Package Types**: sys (system), rec (recovery), sys_ex (system_ex)
- **Region EXTLD prefixes**: fjp01 (JP), fus01 (US), feu01 (EU), pc, djp01, dus01, deu01
- **Known OBFUSCATED_STRING**: `tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6`
## System Role
Central firmware distribution mechanism for PS5 retail, testkit, and devkit consoles.
