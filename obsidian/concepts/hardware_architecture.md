# Hardware Architecture

## Concept Summary

The PS5 hardware architecture is built around a custom semi-custom AMD APU that integrates a Zen 2 CPU complex with an RDNA 2 GPU on a single die, sharing a unified 16 GB GDDR6 memory pool via a 256-bit bus. The CPU provides 8 cores with 16 threads running at variable frequency up to 3.5 GHz, while the GPU delivers 36 compute units with ray tracing acceleration at up to 2.23 GHz, peaking at 10.28 TFLOPS. The system uses on-die codenames derived from Shakespeare (Oberon for the CPU partition, Ariel for the GPU) and Lord of the Rings (Azalia for the GPU subsystem).

Storage is one of the most distinctive hardware features — a custom 825 GB PCIe 4.0 NVMe SSD with a proprietary 12-channel flash controller achieves 5.5 GB/s raw sequential reads, with compression reaching 8-9 GB/s via the Kraken engine. An M.2 expansion slot supporting NVMe drives from 250 GB to 8 TB was added via system software 4.00. The southbridge and Embedded Micro Controller (EMC) functions are handled by a MediaTek-based chip that manages peripheral connectivity, power sequencing, thermal monitoring, and the SPI serial flash boot interface.

Three chassis generations have been released since launch: FAT (2020-2023), Slim (2023+), and Pro (2024+), each with distinct motherboard revisions. The system is powered by a 350W internal PSU with an Infineon VRM controller providing 8+2 phase power for the APU. Multiple firmware components manage hardware subsystems, each identified by hex codenames in the 0x4xxxxxxx and 0xCxxxxxxx ranges, covering the EMC, CP Box, WiFi/Bluetooth, TPM, USB-C controller, and SSD controller domains.

## Role in System

The hardware layer is the foundation upon which every other system component operates. The custom APU defines the computational capabilities available to all software layers, while the unified memory architecture means CPU and GPU share the same physical memory pool — affecting isolation boundaries and creating potential side-channel considerations. The southbridge/EMC chip manages low-level system initialization during boot, coordinating power sequencing before the main PSP-based boot chain takes over.

The various motherboard revisions across FAT, Slim, and Pro chassis mean that exploit compatibility may differ across hardware variants due to component changes and firmware differences. The serial flash is a critical component as it stores the initial boot firmware and configuration parameters, making it a primary attack surface for physical-access exploitation scenarios.

## Connections

- [[system_architecture]]
- [[boot_chain]]
- [[kernel_architecture]]
- [[hypervisor_architecture]]
- [[security_model]]
- [[iommu_architecture]]
- [[gpu_dma_exploitation]]

## Security Relevance

- Serial flash (Winbond W25Q16JVNIM on SPI bus) is the primary physical attack surface for boot-level dumping and reprogramming
- Unified GDDR6 memory pool complicates isolation boundaries between CPU and GPU security domains
- Motherboard revisions may affect exploit compatibility due to component-level changes
- Multiple firmware subsystems (TPM/Floyd, USB-C controller, SSD controller) each present independent attack surfaces

## Graph Reference

research/hardware/hardware_overview.md
