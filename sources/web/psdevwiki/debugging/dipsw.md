# Dipsw
## Source URL
https://www.psdevwiki.com/ps5/Dipsw
## System Layer
Debugging / Boot Parameters
## Summary
There are 256 dipswitches (boot parameters) initialized at boot from the CP box MMIO region, gated by console type. Retail consoles can access none, TestKits can access a limited selection, DevKits can access most, and intdev-flagged DevKits can access all 256.
## Key Concepts
- 0x00: IsDevelopmentMode (libSceDipsw.sprx)
- 0x02: IsAssistMode (TestKit-accessible)
- 0x18: IsDisableRazor
- 0x1E: GetDiableBinaryVersionCheckValue
- 0x38: isKeepProcess (SceSysCore.elf)
- 0x66: Disable DSP (TestKit-accessible)
- 0x6D: IsCronos
- 0x78: GC Force Page Migration Window Enable
- 0x9B: MP3 (TEE) Enable
- 0xB5: Debug GC Enable
- 0xF1: manu_mode related
- Access levels: Retail (none), TestKit (limited), DevKit (most), intdev DevKit (all)
## System Role
Controls debug and development features at boot time, enabling or disabling specific system behaviors such as development mode, assist mode, GPU debugging, memory test modes, and manufacturing functions based on console type.
