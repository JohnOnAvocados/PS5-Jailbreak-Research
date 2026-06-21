# Build Strings
## Source URL
https://www.psdevwiki.com/ps5/Build_Strings
## System Layer
System Software / Build System
## Summary
Documentation of PS5 firmware build strings extracted from kernel memory dumps and system logs, covering CP Box EMC, EAP KBL, Secure Loader, VBIOS, Kernel, and index.dat from SceShellCore across retail, testkit, and devkit firmware versions.
## Key Concepts
- **CP Box EMC**: TestKit version 1.0.1.0
- **CP Box EAP KBL**: EAP SDK versions from 5.501.000 (2019-2021), with Sycorax build strings (0.5.7.0 to 2.5.5.3)
- **Secure Loader**: Build string format contains "sys-revision" and "sys-repository-path" (e.g., "Oberon-KDE 2021/04/06 05:22 releases/03.00 171343 pprbld-w54.build.rd.scei.sony.co.jp")
- **VBIOS**: AMD ATOMBIOSBK strings (e.g., "AMDObrGeneri.2132099 .518911 . 06/15/20,23:33:14")
- **Kernel**: Build strings from sysctl kern.version (e.g., "r153000/releases/01.00 May 21 2020 05:17:55"), also contains equivalent PS4 SDK version
- **Index.dat from SceShellCore**: Output on boot (5-6s) on TestKit/DevKit/QA/UART-enabled CEX, contains release, build type, security/sys/middleware/vsh repository paths and revisions
- Key entries: UPD-version, release (hex), build (cex/testkit/devkit), security-revision, sys-revision, sdk-internal-build-number, middleware-revision, vsh-revision, Framework-Version
## System Role
Provides detailed build identification data for forensic analysis of PS5 firmware provenance and version tracking.
