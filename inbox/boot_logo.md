# BootLogo

## Source URL
https://www.psdevwiki.com/ps5/BootLogo

## System Layer
System Software

## Summary
The PS5 BootLogo is displayed by SceSysAvControl and is a 256x256 "PS Logo" image, BPE encoded and embedded in the SceSysAvControl module.

## Key Concepts
- Module location: /SceSysAvControl.elf
- Image size: 256x256 pixels
- Encoding: BPE (Bit Pack Encoding) with some filter
- Search signature: `2A 80 80 07` (magic bytes for BPE encoded data, no header)
- Note: The signature may change in future firmware

## System Role
The boot logo is part of the early system initialization display chain, rendered by SceSysAvControl (Audio-Visual Control) during startup before the main UI loads.
