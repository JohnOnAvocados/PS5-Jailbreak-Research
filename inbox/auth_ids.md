# Auth IDs

## Source URL
https://www.psdevwiki.com/ps5/Auth_IDs

## System Layer
Security / System Software

## Summary
Lists Authentication IDs (Auth IDs) used by PS5 system software to identify and authorize different system components, kernel modules, and applications.

## Key Concepts

### Main Auth IDs
- `4100000000000001` -> Secure Kernel
- `4100000000000002` -> Kernel
- `4100000000001001` -> ???
- `4100000000001002` -> ???
- `4100000000001101` -> ???
- `4100000000001102` -> ???

### System/System_Ex Auth IDs
- `4800000000000024` -> /system/common/lib/ScePlayReady.self
- `480000000000003b` -> /system/common/lib/ScePlayReady2.self
- `4800000000010001` -> /system/sys/set_upper.self
- `4800000010000010` -> /system/vsh/app/NPXS40109/webrtc_daemon.self
- `4900000000000002` -> Shared by many system libraries (.sprx files) in /system/common/lib/, /system/priv/lib/, /system_ex/app/, /system_ex/common_ex/lib/, /system_ex/priv_ex/lib/
- `4800000000001006` -> /system/vsh/app/NPXS40038/eboot.bin (and many other VSH app eboot.bin files)
- `4800000000010003` -> ./sys/decid.elf
- `4800000000000005` -> ./sys/orbis_audiod.elf
- `4800000000000007` -> ./sys/SceSysCore.elf
- `4800000000000010` -> ./vsh/SceShellCore.elf
- `4800000010000001` -> /system_ex/app/NPXS40140/BdmvPlayerCore.elf
- `4800000010000005` -> /system_ex/app/NPXS40140/cdc/bin/bdj.elf

### GnmDriver Auth
- `4900000000000007` -> /system/common/lib/libSceGnmDriver.sprx
- `4900000000000007` -> /system/common/lib/libSceGnmDriverCompat1.sprx
- `4900000000000007` -> /system/common/lib/libSceGnmDriverForNeoMode.sprx

### BD Player Auth
- `4900000000000003` -> /system_ex/app/NPXS40140/libAacs.sprx
- `4900000000000006` -> /system_ex/app/NPXS40140/libBdplus.sprx

## System Role
Auth IDs are used by the SceSbl (Secure Boot Loader) authentication system to verify and authorize module loading. The ID prefix indicates privilege level: 41 = kernel, 48 = system process, 49 = system library. Auth ID 4900000000000002 is the most common, used by the vast majority of system libraries.
