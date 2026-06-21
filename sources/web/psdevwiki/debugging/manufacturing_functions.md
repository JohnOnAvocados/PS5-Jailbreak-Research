# Manufacturing Functions
## Source URL
https://www.psdevwiki.com/ps5/Manufacturing_Functions
## System Layer
Security / Manufacturing
## Summary
Collection of SceSbl kernel functions used during manufacturing for drive authentication, secure reset, pairing, factory testing (FTTRM), manufacturing mode control, and secure RTC configuration.
## Key Concepts
- sceSblDriveSecureReset: Resets drive authentication for CS, debug, or QA modes
- sceSblDriveAuthSetHostKeyVolatile: IOCTL 0xC028530D on /dev/driveauth
- sceSblDriveAuthGetPairingRequest: IOCTL 0xC028530B on /dev/cd0
- sceSblDriveAuthSetPairingResData: IOCTL 0xC028530C on /dev/driveauth
- sceSblFttrmReadSector/WriteSector: IOCTL 0xC0185301/0xC0185302 on /dev/fttrm
- sceSblManuAuthLoadSecureModule: IOCTL 0x40184D01 on /dev/manuauth
- sceSblManuAuthGetManuMode/SetManuMode: Query/set manufacturing mode
- sceSblSrtcSetFrequencyOffset: IOCTL 0xC008530D on /dev/srtc
## System Role
Provides the factory-level authentication, pairing, and testing functions required during console manufacturing and QA processes.
