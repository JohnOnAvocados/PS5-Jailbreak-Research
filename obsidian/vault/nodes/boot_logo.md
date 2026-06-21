# BootLogo

## Source
inbox\boot_logo.md

## System Layer
boot_chain

## Summary
# BootLogo

## Source URL
https://www.psdevwiki.com/ps5/BootLogo

## System Layer
System Software

## Summary
The PS5 BootLogo is displayed by SceSysAvControl and is a 256x256 "PS Logo" image, BPE encoded and embedded in the SceSysAvControl module. ## Key Concepts
- Module location: /SceSysAvControl.elf
- Image size: 256x256 pixels
- Encoding: BPE (Bit Pack Encoding) with some filter
- Search signature: `2A 80 80 07` (magic bytes for BPE encoded data, no header)
- Note: The signature may change in future firmware

## System Role
The boot logo is part of the early system initialization display chain, rendered by SceSysAvControl (Audio-Visual Control) during startup before the main UI loads.

## Concepts
scesysavcontrol, system, bootlogo, bpe, encoded, encoding, image, logo, module, ps5, signature, x256, audio-visual, before, bit

## Related Notes
- [[../nodes/amd_security]]
- [[../nodes/arm_trusted_firmware]]
- [[../nodes/arxiv]]
- [[../nodes/arxiv_org_eprint_archive]]
- [[../nodes/auth_ids]]
- [[../nodes/backwards_compatibility]]
- [[../nodes/blackhat_archives]]
- [[../nodes/build_strings]]
- [[../nodes/dualsense_hid_commands]]
- [[../nodes/homebrew_enabler]]
- [[../nodes/hypervisor_loader]]
- [[../nodes/ieee_xplore_digital_library]]
- [[../nodes/kernel_overview]]
- [[../nodes/keystone]]
- [[../nodes/languages]]
- [[../nodes/libraries]]
- [[../nodes/m2_ssd]]
- [[../nodes/magics]]
- [[../nodes/microsoft_firmware_security_research]]
- [[../nodes/ncc_group_research]]
