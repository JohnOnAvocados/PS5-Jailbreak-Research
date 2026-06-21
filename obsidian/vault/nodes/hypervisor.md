# Hypervisor

## Source
inbox\hypervisor.md

## System Layer
hypervisor

## Summary
# Hypervisor
## Source URL
https://www.psdevwiki.com/ps5/Hypervisor
## System Layer
hypervisor
## Summary
PS5 uses a custom hypervisor (HV) for Virtualization-Based Security (VBS), protecting kernel integrity through nested paging (SLAT/NPT), control register filtering, MSR protection, and execute-only memory (xotext). On FW ≤ 2.70 the hypervisor is integrated into the kernel binary; later versions have it as a separately loaded component. ## Key Concepts
- Custom hypervisor (not based on existing projects)
- Virtualization-Based Security (VBS) for kernel integrity protection
- Separate loading: in-kernel (≤ 2.70) vs standalone (> 2.70)
- 17 hypercalls (vmmcalls: 0x00-0x10)
- VMMCALL_HV_GET_MESSAGE_CONF (0), GET_MESSAGE_COUNT (1)
- VMMCALL_HV_START_LOADING_SELF (2), FINISH_LOADING_SELF (3)
- VMMCALL_HV_SET_CPUID_PS4 (4), SET_CPUID_PPR (5)
- VMMCALL_HV_IOMMU_SET_GUEST_BUFFERS (6)
- VMMCALL_HV_IOMMU_ENABLE_DEVICE (7)
- VMMCALL_HV_IOMMU_BIND_PASID (8), UNBIND_PASID (9)
- VMMCALL_HV_IOMMU_CHECK_CMD_COMPLETION (10)
- VMMCALL_HV_IOMMU_CHECK_EVLOG_REGS (11)
- VMMCALL_HV_IOMMU_READ_DEVICE_TABLE (12)
- VMMCALL_HV_GET_TMR_VIOLATION_ERROR (13)
- VMMCALL_HV_VMCLOSURE_INVOCATION (14, FW ≥ 3.00)
- VMMCALL_HV_STARTUP_MP (15, FW ≥ 3.00)
- VMMCALL_HV_DISABLE_STARTUP_MP (16, FW ≥ 3.00)
- AMD Secure Virtual Machine (SVM) features used: NPT, GMET, CR/MSR interception
- Nested Page Tables (SLAT) for second-level address translation
- Guest Mode Execute Trap (GMET) prevents code execution from wrong privilege level
- xotext (execute-only memory, bit 58 in NPT PTEs) - hardware-backed via AMD collaboration
- Filtered CR0 bits: PG (31), WP (16), NE (5), PE (0)
- Filtered CR4 bits: SMAP (21), SMEP (20), VME (0)
- Masked EFER bits: nda/xotext (16), SVME (12), NXE (11)
- MSR Protection Map (MSRPM) bitmap for protected MSRs
- VMEXIT_CPUID handled (PS4 emulation)
- VMEXIT_RDPRU injected with #GP
- IOMMU management moved from kernel to hypervisor
- Only virtualizes kernel/usermode (GameOS), no multiple VMs
## System Role
Kernel integrity protection via hardware-assisted virtualization

## Concepts
hypervisor, kernel, protection, bits, integrity, msr, npt, xotext, amd, custom, execute-only, filtered, gmet, memory, nested

## Related Notes
- [[../nodes/amd_secure_encrypted_virtualization]]
- [[../nodes/crossline_breaking_amd_sev]]
- [[../nodes/gbatemp_ps5_exploit_guide]]
- [[../nodes/gpu_dma_exploitation]]
- [[../nodes/iommu_architecture]]
- [[../nodes/ps2_emulation]]
- [[../nodes/ps5_exploit_chains_overview]]
- [[../nodes/vulnerabilities]]
- [[../nodes/xom]]
