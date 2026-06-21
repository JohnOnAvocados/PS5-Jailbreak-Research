# Open Questions

Tracking format: `Q-{CRIT|IMP|MIN}-{NNN}` — assigned sequentially within each category.

---

## Critical

Questions whose answers block progress in downstream layers.

### Hardware Architecture
- `Q-CRIT-001` What is the exact SoC die revision in current retail units?
- `Q-CRIT-002` Is the full memory map documented anywhere (public or leaked)?
- `Q-CRIT-003` Are JTAG/SWD debug interfaces physically accessible on production boards?
- `Q-CRIT-004` What is the IOMMU page table format (page sizes, walk cache depth)?

### Firmware & Secure Boot
- `Q-CRIT-005` What is the root key source (fuse row, OTP, or both)?
- `Q-CRIT-006` Is the boot chain fully encrypted or only signed after Boot ROM?
- `Q-CRIT-007` How does the anti-rollback mechanism work? What triggers a fuse burn?
- `Q-CRIT-008` Are there any public boot chain vulnerabilities for PS5?

### Hypervisor
- `Q-CRIT-009` Is the hypervisor based on an existing project or fully proprietary?
- `Q-CRIT-010` What is the hypercall surface? How many hypercalls?
- `Q-CRIT-011` Does the hypervisor enforce W^X at stage-2 page tables?

### Kernel
- `Q-CRIT-012` What FreeBSD version is PS5's kernel derived from?
- `Q-CRIT-013` How much of the FreeBSD syscall table is modified or trimmed?
- `Q-CRIT-014` Is KASLR effective? Bits of entropy?

---

## Important

Questions that shape analysis depth but do not block progress.

- `Q-IMP-001` What is the firmware update delta mechanism (full flash vs parts)?
- `Q-IMP-002` Does the hypervisor virtualize the GPU or pass it through?
- `Q-IMP-003` What sandbox (if any) does the kernel enforce for userland processes?
- `Q-IMP-004` What is the WebKit version history mapped to firmware versions?
- `Q-IMP-005` What exploit techniques from PS4 are still viable on PS5?
- `Q-IMP-006` Is there a public Ghidra/IDA processor module for the custom RDNA?

---

## Important

Questions that shape analysis depth but do not block progress.

- `Q-IMP-001` What is the firmware update delta mechanism (full flash vs parts)?
- `Q-IMP-002` Does the hypervisor virtualize the GPU or pass it through?
- `Q-IMP-003` What sandbox (if any) does the kernel enforce for userland processes?
- `Q-IMP-004` What is the WebKit version history mapped to firmware versions?
- `Q-IMP-005` What exploit techniques from PS4 are still viable on PS5?
- `Q-IMP-006` Is there a public Ghidra/IDA processor module for the custom RDNA?
- `Q-IMP-007` How does the Y2JB LUA userland payload achieve persistence across FW versions including 13.40?
- `Q-IMP-008` What specific sysctl or kernel primitive does P2JB's kqueueex cr_ref overflow abuse?
- `Q-IMP-009` Can BD-JB's path-traversal exploit technique be adapted for digital-only consoles?
- `Q-IMP-010` What is the exact relationship between the WebKit, BD-JB, and LUA userland entry points in a typical chain?
- `Q-IMP-011` Are there any public kernel exploits for FW > 12.70, or is P2JB the current ceiling?
- `Q-IMP-012` What is the etaHEN 2.4B syscall hook mechanism and how does it enable homebrew?

## Minor

Detail-level questions that refine understanding but are not mission-critical.

- `Q-MIN-001` What is the exact clock speed and core count configuration?
- `Q-MIN-002` How much RAM is reserved for the system OS vs game OS?
- `Q-MIN-003` What filesystem does the firmware updater use?
- `Q-MIN-004` Does the console have a hidden service menu?
- `Q-MIN-005` What is the exact size of Boot ROM in bytes?
- `Q-MIN-006` What is the P2JB kqueueex spamming success rate across different FW versions?
- `Q-MIN-007` Does Sony's HackerOne bug bounty $50K payout apply to userland-only bugs, or only kernel/hypervisor?
- `Q-MIN-008` Who maintains the PS5 jailbreak compatibility Google Sheet, and how frequently is it updated?
- `Q-MIN-009` What anti-debugging or integrity checks do etaHEN and ItemzFlow employ?
- `Q-MIN-010` What is the current recovery/restore process if a jailbroken PS5 is updated accidentally?
