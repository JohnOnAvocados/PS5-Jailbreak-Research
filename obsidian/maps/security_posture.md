# PS5 Security Posture Map

## Root of Trust Chain

```
Boot ROM (immutable, fused keys)
  → Secure Loader (serial flash, RSA-4096 signed)
    → EMC/CP Box (southbridge firmware)
      → Hypervisor Loader
        → Kernel (SELF RSA-3072)
          → Secure Modules (0x8002xxxx runtime services)
```

## Isolation Layers

- [[hardware_architecture]] — AMD PSP, XOM at memory controller level, OTP fuses
- [[boot_chain]] — cryptographic stage transitions, anti-rollback nonces
- [[secure_boot]] — key hierarchy (RSA-4096 → RSA-3072 → AES-128-CBC)
- [[hypervisor_architecture]] — nested page tables, IOMMU, partition isolation
- [[iommu_architecture]] — DMA protection, device table, hypercall interface
- [[kernel_architecture]] — XOM enforcement, SceSbl dispatch, capability sandboxing
- [[syscall_catalog]] — 500+ syscalls, PS5-specific extensions, exploit targets
- [[security_model]] — Auth IDs, PAIDs, secure modules, Keystone

## Attack Surface Layers

| Layer | Attack Vector | Mitigation |
|-------|--------------|------------|
| Hardware | SPI flash dumping, voltage glitching | XOM, OTP fuses |
| Firmware | Boot ROM bug, Secure Loader decryption | Mask ROM, dual AES |
| Hypervisor | Hypercall interface, TMR OOB | Restricted hypercall count |
| Kernel | Syscall bugs, IOCTL mishandling | XOM, SMAP/SMEP, KASLR |
| Application | WebKit JS engine, BD-JB | Sandbox, nullfs, capability model |

## Known Exploit Categories

- **WebKit/V8** — userland entry point (Y2JB up to FW 13.40, [[y2jb_sandbox_escape]])
- **PS2 Emulator JIT** — design-level exploit (mast1c0re FW 2.00-13.00, [[mast1c0re_jit_pipeline]])
- **GPU DMA** — bypasses kernel .data write protection (FW >=6.00, [[gpu_dma_exploitation]])
- **Kernel** — privilege escalation (kqueueex, netcontrol, umtx_shm, [[syscall_catalog]])
- **Hypervisor** — full control (TMR OOB, Byepervisor, Prosperous, up to FW 6.02)
- **Boot Chain** — currently no public boot ROM exploits

## Key Security Properties

- Every boot stage is independently signed with distinct keys
- XOM is enforced at the hardware memory controller — no software can read protected pages
- Anti-rollback uses both OTP fuses AND revision nonces (dual enforcement)
- Security revisions progress monotonically: 0x00000001 → 0x0003FFFF
- Documented weakness: PKG RSA-3072 private key leaked with CRT parameters
- M.2 SSD encryption keys were static across FW 1.00-12.20

## Graph Reference

research/security_model/security_model.md
