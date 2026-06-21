# Watermarks

**Source:** https://www.psdevwiki.com/ps5/Watermarks
**System Layer:** System Software
**Summary:** PUP (PlayStation Update Package) watermarking system for tracing SDK and firmware content to authorized developers.
**Key Concepts:** PUP watermark, DevNet user ID, serial number, content traceability, SDK distribution tracking
**System Role:** Anti-leak mechanism that embeds identifying information in firmware and SDK packages to trace distribution back to specific developers.

## Overview

SDK Content, as well as Factory content, both contain watermarks that can trace the location of the devteam (in the case of SDKs and PUPs) as well as the factory team (in the case of the factory content) linked to the content.

### Old PUP Watermarks

Old-format PUP watermarks contain DevNet user ID, organization name, company name, date of PUP download, and host IP address:

```
User id:1951884
Org name:SCEE Customer Services
Company name:SCE UK (SCEE Customer Services)
Date PUP downloaded:2013-10-28 14:26
Host IP address:217.18.20.253
```

### New PUP Watermarks

New-format PUP watermarks contain a serial number that associates with the user who downloaded the PUP. The serial number must be provided to the DevNet development team to get user and org details:

```
PUP serial number:10356016
```
