# Secure Loader

## Source
inbox\secure_loader.md

## System Layer
boot_chain

## Summary
# Secure Loader

## Source URL
https://www.psdevwiki.com/ps5/Secure_Loader

## System Layer
Security / Boot ROM

## Summary
The PS5 Secure Loader is the Initial Program Loader (IPL) running on the AMD Platform Security Processor (PSP). It is the main loader of the Hypervisor, Hypervisor Loader, and Kernel. ## Key Concepts

### Header Structure (at NAND Group 0 offset 0x800)

| Offset | Offset from NAND Group 0 | Size | Description | Notes |
|--------|--------------------------|------|-------------|-------|
| 0x0 | 0x800 | 4 | Magic | E4 DB 7C 02 |
| 0x4 | 0x804 | 4 | Header Size | Little Endian (0x400) |
| 0x8 | 0x808 | 4 | Entry Point | Little Endian (0xB0) |
| 0xC | 0x80C | 4 | Body Size | Little Endian (e.g.

## Concepts
revision, loader, header, security, body, boot, endian, firmware, ipl, little, nonce, offset, padding, secure, size

## Related Notes
- [[../nodes/amd_platform_security_processor]]
- [[../nodes/amd_secure_processor]]
- [[../nodes/amd_security]]
- [[../nodes/arm_trusted_firmware]]
- [[../nodes/arxiv]]
- [[../nodes/arxiv_org_eprint_archive]]
- [[../nodes/auth_ids]]
- [[../nodes/backwards_compatibility]]
- [[../nodes/blackhat_archives]]
- [[../nodes/bond]]
- [[../nodes/boot_logo]]
- [[../nodes/build_strings]]
- [[../nodes/dualsense_dfu_modes]]
- [[../nodes/dualsense_hid_commands]]
- [[../nodes/homebrew_enabler]]
- [[../nodes/hypervisor_loader]]
- [[../nodes/ieee_xplore_digital_library]]
- [[../nodes/intel_security]]
- [[../nodes/keystone]]
- [[../nodes/magics]]
