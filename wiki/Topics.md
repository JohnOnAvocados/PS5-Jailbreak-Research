# Topics Cross-Reference Index

Maps every major topic across wiki pages, research files, Obsidian concepts, and graph node IDs.

## Hardware

| Topic | Wiki Page | Research File | Obsidian Concept | Graph Node ID |
|-------|-----------|---------------|------------------|---------------|
| SoC (Oberon/Viola) | [Hardware](sections/hardware) | `research/hardware/hardware_overview.md` | [[hardware_architecture]] | `ps5_overview` |
| Southbridge (CXD90061GG) | [Southbridge_Architecture](Southbridge_Architecture) | `research/hardware/southbridge_analysis.md` | [[hardware_architecture]] | `southbridge` |
| Serial Flash (W25Q16JVNIM) | [Southbridge_Architecture](Southbridge_Architecture) | `research/hardware/southbridge_analysis.md` | [[hardware_architecture]] | `serial_flash` |
| GPU (RDNA 2) | [Hardware](sections/hardware) | `research/hardware/hardware_overview.md` | [[hardware_architecture]] | `gpu` |
| CPU (Zen 2) | [CPU Architecture](sections/cpu_architecture) | `research/hardware/hardware_overview.md` | [[hardware_architecture]] | `cpu` |
| Memory (GDDR6) | [Hardware](sections/hardware) | `research/hardware/hardware_overview.md` | [[hardware_architecture]] | `memory` |
| IOMMU/SMMU | [Southbridge_Architecture](Southbridge_Architecture) | `research/hypervisor/iommu_architecture.md` | [[iommu_architecture]] | `iommu` |
| NAND Storage | [Hardware](sections/hardware) | `research/hardware/hardware_overview.md` | [[hardware_architecture]] | `storage` |
| CP Box (CPBH-100) | [Southbridge_Architecture](Southbridge_Architecture) | `research/hardware/southbridge_analysis.md` | [[hardware_architecture]] | `cp_box` |
| DualSense | [Hardware](sections/hardware) | `research/hardware/hardware_attack_surface.md` | [[hardware_architecture]] | `dualsense` |
| Blu-ray Drive | [Hardware](sections/hardware) | `research/hardware/hardware_attack_surface.md` | [[hardware_architecture]] | `bluray_drive_firmware` |
| HDMI (MN864739) | [Hardware](sections/hardware) | `research/hardware/hardware_attack_surface.md` | [[hardware_architecture]] | `mn864739` |

## Firmware

| Topic | Wiki Page | Research File | Obsidian Concept | Graph Node ID |
|-------|-----------|---------------|------------------|---------------|
| Boot ROM | [Boot Chain](sections/boot_chain) | `research/firmware/boot_chain.md` | [[boot_chain]] | `secure_boot` |
| Secure Loader | [Boot Chain](sections/boot_chain) | `research/firmware/secure_boot.md` | [[boot_chain]] | `secure_loader` |
| PSP Firmware | [Firmware](sections/firmware) | (gap - no public analysis) | [[hardware_architecture]] | `amd_platform_security_processor` |
| EMC Firmware | [Southbridge_Architecture](Southbridge_Architecture) | `research/hardware/southbridge_analysis.md` | [[hardware_architecture]] | `emc` |
| EAP Firmware | [Southbridge_Architecture](Southbridge_Architecture) | `research/hardware/southbridge_analysis.md` | [[hardware_architecture]] | `eap` |
| HyLonome | [Hypervisor](sections/hypervisor) | `research/hypervisor/hypervisor.md` | [[hypervisor_architecture]] | `hypervisor_loader` |
| Anti-Rollback | [Boot Chain](sections/boot_chain) | `research/firmware/secure_boot.md` | [[boot_chain]] | `secure_boot` |
| Revision Nonces | [Boot Chain](sections/boot_chain) | `research/firmware/secure_boot.md` | [[boot_chain]] | `secure_boot` |
| Key Hierarchy | [Boot Chain](sections/boot_chain) | `research/firmware/secure_boot.md` | [[security_model]] | `keys` |
| PUP Format | [System Overview](sections/system_overview) | `research/firmware/update_mechanism.md` | [[system_architecture]] | `system_software` |

## Hypervisor

| Topic | Wiki Page | Research File | Obsidian Concept | Graph Node ID |
|-------|-----------|---------------|------------------|---------------|
| Hypervisor Architecture | [Hypervisor](sections/hypervisor) | `research/hypervisor/hypervisor.md` | [[hypervisor_architecture]] | `hypervisor` |
| Hypercalls (0x00-0x10) | [Hypervisor](sections/hypervisor) | `research/hypervisor/hypervisor.md` | [[hypervisor_architecture]] | `hypervisor` |
| IOMMU Hypercalls (0x06-0x0C) | (IOMMU section) | `research/hypervisor/iommu_architecture.md` | [[iommu_architecture]] | `iommu` |
| NPT/SLAT | [Hypervisor](sections/hypervisor) | `research/hypervisor/hypervisor.md` | [[hypervisor_architecture]] | `hypervisor` |
| xotext (EFER bit 16) | [Hypervisor](sections/hypervisor) | `research/hypervisor/hypervisor.md` | [[hypervisor_architecture]] | `xom` |
| TMR | [Hypervisor](sections/hypervisor) | `research/hypervisor/hypervisor.md` | [[hypervisor_architecture]] | `hypervisor` |
| VMClosure | [Hypervisor](sections/hypervisor) | `research/hypervisor/hypervisor.md` | [[hypervisor_architecture]] | `hypervisor` |

## Kernel

| Topic | Wiki Page | Research File | Obsidian Concept | Graph Node ID |
|-------|-----------|---------------|------------------|---------------|
| Kernel Overview | [Kernel](sections/kernel) | `research/kernel/kernel.md` | [[kernel_architecture]] | `kernel_overview` |
| Syscall Catalog | [Kernel_Exploit_Landscape](Kernel_Exploit_Landscape) | `research/kernel/syscall_catalog.md` | [[syscall_catalog]] | `syscalls` |
| IOCTL Devices | [Kernel](sections/kernel) | `research/kernel/kernel.md` | [[kernel_architecture]] | `ioctl` |
| Secure Modules | [Kernel](sections/kernel) | `research/kernel/kernel.md` | [[security_model]] | `secure_modules` |
| SceSbl | [Kernel](sections/kernel) | `research/kernel/kernel.md` | [[kernel_architecture]] | `scesbl_functions` |
| GPU DMA Exploit | [Kernel_Exploit_Landscape](Kernel_Exploit_Landscape) | `research/kernel/gpu_dma_exploitation.md` | [[gpu_dma_exploitation]] | `gpu_dma` |
| XOM | [Memory Protection](sections/memory_protection) | `research/kernel/kernel.md` | [[kernel_architecture]] | `xom` |

## Userland

| Topic | Wiki Page | Research File | Obsidian Concept | Graph Node ID |
|-------|-----------|---------------|------------------|---------------|
| Y2JB / V8 TheHole | (Y2JB section) | `research/userland/y2jb_sandbox_escape.md` | [[y2jb_sandbox_escape]] | `y2jb_ps5_framework` |
| mast1c0re JIT | (mast1c0re section) | `research/userland/mast1c0re_jit_pipeline.md` | [[mast1c0re_jit_pipeline]] | `mast1c0re_jit` |
| BD-JB (Blu-ray Java) | (BD-JB section) | `research/exploit_history/jailbreak_comprehensive.md` | [[jailbreak_comprehensive]] | `bd_jb_bluray_exploit` |
| WebKit | (WebKit section) | `research/exploit_history/webkit_kernel.md` | [[jailbreak_comprehensive]] | `vulnerabilities` |
| PS2 Emulation | (mast1c0re section) | `research/userland/mast1c0re_jit_pipeline.md` | [[mast1c0re_jit_pipeline]] | `ps2_emulation` |
| YouTube App | (Y2JB section) | `research/userland/y2jb_sandbox_escape.md` | [[y2jb_sandbox_escape]] | `y2jb_ps5_framework` |

## Exploit History

| Topic | Wiki Page | Research File | Obsidian Concept | Graph Node ID |
|-------|-----------|---------------|------------------|---------------|
| Full Jailbreak History | [Exploit_Compatibility_Matrix](Exploit_Compatibility_Matrix) | `research/exploit_history/jailbreak_comprehensive.md` | [[jailbreak_comprehensive]] | `ps5_jailbreak_current_state` |
| CVE Timeline | (CVE section) | `research/exploit_history/cve_timeline.md` | [[jailbreak_comprehensive]] | `vulnerabilities` |
| Exploit Chains | [Exploit_Compatibility_Matrix](Exploit_Compatibility_Matrix) | `research/exploit_history/jailbreak_comprehensive.md` | [[jailbreak_comprehensive]] | `exploit_chains` |
| Hypervisor Exploits | [Hypervisor](sections/hypervisor) | `research/exploit_history/boot_hypervisor.md` | [[hypervisor_architecture]] | `hypervisor` |
| Kernel Exploits | [Kernel_Exploit_Landscape](Kernel_Exploit_Landscape) | `research/kernel/syscall_catalog.md` | [[syscall_catalog]] | `syscalls` |
| Homebrew Enablers | [System Overview](sections/system_overview) | `research/exploit_history/jailbreak_comprehensive.md` | [[jailbreak_comprehensive]] | `etahen_homebrew_enabler` |

## Security Model

| Topic | Wiki Page | Research File | Obsidian Concept | Graph Node ID |
|-------|-----------|---------------|------------------|---------------|
| Auth IDs | [Security Model](sections/security_model) | `research/security_model/security_model.md` | [[security_model]] | `auth_ids` |
| PAIDs | [Security Model](sections/security_model) | `research/security_model/security_model.md` | [[security_model]] | `program_authority_id` |
| SELF Signing | [Security Model](sections/security_model) | `research/security_model/security_model.md` | [[security_model]] | `magics` |
| Keystone | [Security Model](sections/security_model) | `research/security_model/security_model.md` | [[security_model]] | `keystone` |
| Key Hierarchy | [Boot Chain](sections/boot_chain) | `research/firmware/secure_boot.md` | [[security_model]] | `keys` |

## Analysis

| Topic | Wiki Page | Research File | Obsidian Concept | Graph Node ID |
|-------|-----------|---------------|------------------|---------------|
| Research Roadmap (15 gaps) | [Research Roadmap](research/analysis/research_roadmap) | `research/analysis/research_roadmap.md` | [[system_architecture]] | - |
| Attack Surface | (Hardware section) | `research/hardware/hardware_attack_surface.md` | [[hardware_architecture]] | `attack_surface` |
| Obsidian Concept Map | [Concept Map](obsidian/maps/concept_map) | `obsidian/maps/concept_map.md` | - | - |
| Obsidian Security Posture | [Security Posture](obsidian/maps/security_posture) | `obsidian/maps/security_posture.md` | - | - |
| Pipeline Report | [Pipeline Report](reports/final_system_summary) | `reports/final_system_summary.md` | - | - |

## Graph Node Legend

| Field | Meaning |
|-------|---------|
| Edge count | Number of connections this node has to other nodes |
| Layer | System layer classification (hardware, firmware, hypervisor, etc.) |
| Source | Whether from psdevwiki, research document, or inbox |
