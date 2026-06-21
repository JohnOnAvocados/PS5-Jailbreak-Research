# MMIO Prototype

## Source URL
https://www.psdevwiki.com/ps5/MMIO_Prototype

## System Layer
Hardware

## Summary
MMIO (Memory-Mapped I/O) mapping for prototype PS5 consoles (FW 0.85.070 and below), assuming no kASLR. Base address: 0xFFFFF80000000000.

## Key Concepts

| Region Name | Usage | Region Address | Device |
|-------------|-------|---------------|--------|
| nvme0 | Titania | 0xC4200000-0xC4203FFF, 0xC4000000-0xC40FFFFF | device 0.0 on pci1 |
| tpcie0 | Titania PCI Express glue | 0xA0000000-0xBFFFFFFF, 0xC0000000-0xC3FFFFFF | device 0.1 on pci1 |
| spcie0 | Salina PCI Express glue | 0x8500C000-0x8500CFFF, 0x85200000-0x853FFFFF, 0x85400000-0x8547FFFF | device 0.5 on pci1 |
| mtsc0 | Salina GBE controller | 0x85000000-0x85000FFF | device 0.2 on pci1 |
| ahci0 | SALINA sata0 AHCI | 0x85004000-0x85007FFF | device 0.3 on pci1 |
| ahci1 | SALINA sata1 AHCI | 0x85008000-0x8500BFFF | device 0.4 on pci1 |
| xhci0 | Salina USB host | 0x85600000-0x857FFFFF | device 0.6 on pci1 |
| apcie0 | Belize(Caliban) PCIe glue | 0x81300000-0x813FFFFF, 0x81400000-0x81407FFF, 0x81600000-0x817FFFFF | device 0.17 on pci1 |
| gc0 | GC (Graphics Core) | 0xD0000000-0xDFFFFFFF, 0xE0000000-0xE01FFFFF, 0xE0600000-0xE067FFFF | device 0.0 on pci2 |
| az0 | GPU/Azalia Audio | 0xE06C0000-0xE06C3FFF | device 0.1 on pci2 |
| sbl0 | Ariel PSP | 0xE0500000-0xE05FFFFF, 0xE06C6000-0xE06C7FFF | device 0.2 on pci2 |
| xhci1 | PPR USB host | 0xE0200000-0xE02FFFFF | device 0.4 on pci2 |
| xhci2 | PPR USB host | 0xE0300000-0xE03FFFFF | device 0.5 on pci2 |
| ajm0 | ACP (Audio Co-Processor) | 0xE0680000-0xE06BFFFF | device 0.6 on pci2 |
| mp40 | MP4 | 0xE0400000-0xE04FFFFF, 0xE06C4000-0xE06C5FFF | device 0.3 on pci2 |
| deci_shm_main0 | DECI5 shared memory | 0x880000000-0x89FFFFFFF | device 0.19 on pci1 |
| bxe0 | PCI BAR | 0x80000000-0x807FFFFF, 0x80800000-0x80FFFFFF, 0x81000000-0x8100FFFF | device 0.10 on pci1 |

### Codename Reference
- **Titania** = NVMe controller
- **Salina** = Southbridge (I/O hub)
- **Belize/Caliban** = PCIe bridge
- **Ariel** = PSP (Platform Security Processor)
- **GC** = Graphics Core (GPU)

## System Role
The prototype MMIO map reveals the PS5's physical hardware layout and address assignments. Essential for low-level hardware exploitation, DMA attacks, and understanding the PCI topology.
