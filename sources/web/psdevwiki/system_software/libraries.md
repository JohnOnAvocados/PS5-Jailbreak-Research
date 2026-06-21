# Libraries

## Source URL
https://www.psdevwiki.com/ps5/Libraries

## System Layer
System Software

## Summary
Complete list of PS5 system library names and their SceSysModule IDs used for dynamic module loading.

## Key Concepts
The table lists 300+ system libraries with their unique module IDs (hex values like 0x8000001C). Libraries are loaded via SceSysModule system service. Notable categories:

### Graphics
- libSceGnmDriver (0x80000052) - GPU driver
- libSceVideoOut (0x80000022) - Video output
- libSceAudioOut (0x80000001) - Audio output
- libSceComposite (0x8000008A) - Compositor

### Networking
- libSceNet (0x8000001C)
- libSceNetCtl (0x80000009)
- libSceHttp (0x8000000A)
- libSceSsl (0x8000000B)
- libSceNpCommon (0x8000000C) through various NP libs

### Security
- libSceDipsw (0x80000029) - Dipswitch access
- libSceDeci5 (0x10A) - DECI5 debug interface
- libSceDbgAssist (0x8000003D)

### Media
- libSceAudiodec (0x88), libSceVdecCore (0x80000015)
- libSceJpegDec (0x8A), libScePngDec (0x8C)
- libSceAvPlayer (0xA5)
- libScePlayReady (0xC3), libScePlayReady2 (0x108)

### Web/Runtime
- libSceWeb (0x80000072), libSceWebKit2 (0x80000073)
- libSceNKWeb (0x80000079), libSceNKWebKit (0x8000007A)
- libSceJscCompiler (0x80000070)

### Storage
- libSceSaveData (0x8000000F)
- libSceBgft (0x8000002A) - Background download
- libSceAutoMounterClient (0xCD)

## System Role
Library ID registry for PS5's SceSysModule dynamic linker. Critical for understanding process module imports and system capability mapping.
