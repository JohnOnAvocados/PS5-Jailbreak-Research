# PS4 Emulation

## Source URL
https://www.psdevwiki.com/ps5/PS4_Emulation

## System Layer
System Software

## Summary
PS5 supports PS4 backward compatibility since FW ~2.00 through a PS4 emulation layer. Games can run via disc insertion or digital purchase.

## Key Concepts
- Available since FW 2.00+
- Supports both disc and digital PS4 games
- PS4 emulator revisions are tracked via Build Strings
- PS4 emulator likely runs as a hypervisor guest or at a privileged level

## System Role
The PS4 emulator is a critical component of the PS5 system software, enabling the entire PS4 game library. Its implementation involves syscall translation, GPU command buffer remapping, and CPU mode switching.
