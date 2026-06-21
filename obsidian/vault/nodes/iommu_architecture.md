# IOMMU Architecture: Hypervisor-Managed DMA Protection on PS5

## Source
inbox\iommu_architecture.md

## System Layer
hardware

## Summary
# IOMMU Architecture: Hypervisor-Managed DMA Protection on PS5

## Overview

The PS5 represents an architectural departure from standard AMD platforms in how I/O Memory Management Unit (IOMMU) control is handled. On conventional AMD systems (both Windows and Linux), the operating system kernel configures the IOMMU directly through MMIO register access. On PS5, IOMMU management has been moved entirely into the hypervisor layer — the kernel must request all IOMMU operations through 7 dedicated hypercalls (0x06-0x0C).

## Concepts
iommu, gpu, page, dma, kernel, device, table, data, bypass, hypervisor, domain, ps5, memory, command, translation

## Related Notes
- [[../nodes/25q16jvnim]]
- [[../nodes/amd_platform_security_processor]]
- [[../nodes/amd_secure_processor]]
- [[../nodes/aw_xm501]]
- [[../nodes/aws_nitro_system]]
- [[../nodes/codenames]]
- [[../nodes/cp_box]]
- [[../nodes/cxd90060gg]]
- [[../nodes/cxd90061gg]]
- [[../nodes/cxd90062gg]]
- [[../nodes/cxd90063r1]]
- [[../nodes/devices]]
- [[../nodes/disc_drive_media]]
- [[../nodes/etahen_homebrew_enabler]]
- [[../nodes/exploit_chains]]
- [[../nodes/gbatemp_ps5_exploit_guide]]
- [[../nodes/gpu]]
- [[../nodes/gpu_dma_exploitation]]
- [[../nodes/hardware_specifications]]
- [[../nodes/hd_camera]]
