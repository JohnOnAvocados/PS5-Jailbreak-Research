# Kernel Syscall Catalog: Complete Reference for PS5 Exploit Development

## Source
inbox\syscall_catalog.md

## System Layer
firmware

## Summary
# Kernel Syscall Catalog: Complete Reference for PS5 Exploit Development

## Overview

The PS5 kernel is a heavily modified FreeBSD 11.0 derivative (__FreeBSD_version 1100122) with 500+ syscalls organized across five ranges: standard BSD (0x00-0x5F), extended BSD and networking (0x60-0x8F), POSIX extensions (0x90-0xFF), modern BSD (0x100-0x17F), and PS4/PS5 specific extensions (0x180+). The syscall dispatch uses three distinct sysvec structures: PS4 SELF (backward compatibility), FreeBSD ELF64 (standard, normally unused), and Native SELF (PS5 processes). Console naming conventions reveal the syscall provenance: `sys_compat.*` for PS4 wrappers, `sys_compat4/6/7.*` for FreeBSD legacy compat, `sys_number*` for unnamed PS5-specific entries, and `sys_obsolete*` for deprecated syscalls.

## Concepts
ps5, syscalls, syscall, ps4, freebsd, kernel, exploit, dev, memory, ps5-specific, compatibility, range, ioctl, reference, socket

## Related Notes
- [[../nodes/backup_and_restore]]
- [[../nodes/backwards_compatibility]]
- [[../nodes/bd_jb_bluray_exploit]]
- [[../nodes/bluray_drive_firmware]]
- [[../nodes/bond]]
- [[../nodes/demo_games]]
- [[../nodes/devices]]
- [[../nodes/dualsense]]
- [[../nodes/dualsense_dfu_modes]]
- [[../nodes/emc]]
- [[../nodes/error_codes]]
- [[../nodes/firmware_changelog]]
- [[../nodes/game_titles]]
- [[../nodes/game_update_information]]
- [[../nodes/gbatemp_ps5_exploit_guide]]
- [[../nodes/gpu_dma_exploitation]]
- [[../nodes/homebrew_enabler]]
- [[../nodes/ioctl]]
- [[../nodes/iommu_architecture]]
- [[../nodes/jigkick_files]]
