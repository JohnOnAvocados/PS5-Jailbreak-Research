# Y2JB Sandbox Escape: V8 TheHole Exploitation on PS5 YouTube App

## Source
inbox\y2jb_sandbox_escape.md

## System Layer
memory_protection

## Summary
# Y2JB Sandbox Escape: V8 TheHole Exploitation on PS5 YouTube App

## Overview

The Y2JB (YouTube to Jailbreak) framework exploits CVE-2021-38003 — a V8 JavaScript engine vulnerability where `JSON.stringify()` can leak the internal `TheHole` sentinel value to script code — within the PS5 YouTube TV application. This provides userland JavaScript code execution across the broadest firmware range of any PS5 exploit: FW 2.00-13.40 (confirmed unpatched as of June 2026). When paired with a kernel exploit (P2JB for FW 9.00-12.70, netcontrol for <=12.00, Lapse for <=10.01), Y2JB completes the full userland-to-kernel jailbreak chain.

## Concepts
youtube, app, y2jb, exploit, kernel, thehole, ps5, sandbox, system, cobalt, engine, cve-2021-38003, map, process, version

## Related Notes
- [[../nodes/auth_ids]]
- [[../nodes/bugs]]
- [[../nodes/build_strings]]
- [[../nodes/devices]]
- [[../nodes/exploit_chains]]
- [[../nodes/gbatemp_ps5_exploit_guide]]
- [[../nodes/gpu_dma_exploitation]]
- [[../nodes/homebrew_enabler]]
- [[../nodes/ioctl]]
- [[../nodes/iommu_architecture]]
- [[../nodes/kernel_overview]]
- [[../nodes/lapse_kernel_exploit]]
- [[../nodes/mast1c0re_jit_pipeline]]
- [[../nodes/modal_browser]]
- [[../nodes/official_firmware]]
- [[../nodes/p2jb_kernel_exploit]]
- [[../nodes/poops_kernel_exploit]]
- [[../nodes/program_authority_id]]
- [[../nodes/ps1_emulation]]
- [[../nodes/ps2_emulation]]
