# IOMMU Architecture

## Concept Summary

On PS5, I/O Memory Management Unit (IOMMU/System Memory Management Unit SMMU) control has been moved entirely from the kernel to the hypervisor — an architectural departure from standard AMD platforms. 7 of 17 hypercalls (0x06-0x0C) manage IOMMU operations: guest buffer registration, device enablement, PASID bind/unbind, command completion checking, event log reading, and device table reading.

Based on AMD-Vi specification, the IOMMU provides DMA remapping — controlling which physical memory regions DMA-capable devices (GPU, NVMe, USB, Wi-Fi/Bluetooth, audio) can access. All device DMA transactions pass through IOMMU address translation and permission checking. The hypervisor exclusively manages the device table (up to 65,536 entries), I/O page tables, command queues, and event logs.

The IOMMU is central to the GPU DMA copy bypass exploit: GPU DMA can write to kernel .data pages despite hypervisor write protection because CPU writes are blocked by NPT while DMA writes are controlled by IOMMU — two independent protection mechanisms with different configurations.

## Role in System

The IOMMU enforces the isolation boundary between devices and system memory. It is the only protection preventing DMA-based privilege escalation from compromised device firmware or userland processes with GPU access. The IOMMU hypercall interface is the most complex hypercall category and a key attack surface for hypervisor exploitation.

## Connections

- [[hypervisor_architecture]]
- [[hardware_architecture]]
- [[gpu_dma_exploitation]]
- [[kernel_architecture]]

## Graph Reference
research/hypervisor/iommu_architecture.md
