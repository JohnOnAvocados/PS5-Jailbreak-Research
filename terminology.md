# Terminology

## Hardware
- **SoC** — System on Chip; AMD semi-custom APU integrating Zen 2 CPU + RDNA 2 GPU
- **IOMMU** — I/O Memory Management Unit; translates device DMA addresses to physical memory
- **OTP / eFuse** — One-Time Programmable memory; used for root key storage and anti-rollback
- **Exception Level** — Privilege ring on x86 (Ring 0-3) or ARM (EL0-3); PS5 uses x86 with additional firmware SMM

## Firmware
- **Boot ROM** — Mask ROM, first code executed on power-on; immutable
- **Bootloader** — Intermediate firmware stage(s) that load and verify the next stage
- **Secure Boot** — Cryptographic chain-of-trust from Boot ROM to OS kernel
- **Anti-rollback** — Mechanism preventing downgrade to older firmware versions

## Virtualization
- **Hypervisor** — Software layer managing virtual machines and enforcing isolation
- **Stage-2 Page Tables** — Second level of address translation used by hypervisor to control guest memory access
- **Hypercall** — Synchronous call from guest to hypervisor (analogous to syscall)
- **VM Exit** — Transition from guest VM back to hypervisor (e.g., on privileged instruction)

## Kernel
- **KASLR** — Kernel Address Space Layout Randomization; randomizes kernel base address
- **SMAP / SMEP** — Supervisor Mode Access/Execution Prevention; prevents kernel from accessing/executing user pages
- **W^X** — Write XOR Execute policy; memory pages are either writable or executable, never both
- **Capsicum** — FreeBSD capability-based sandbox framework
- **syscall** — System call; user-to-kernel transition interface

## Exploitation
- **CVE** — Common Vulnerabilities and Exposures; standardized vulnerability identifier
- **WebKit** — Browser engine used by PS5's web browser; initial attack vector on FW ≤ 5.50
- **ROP / JOP** — Return-Oriented / Jump-Oriented Programming; code reuse attack techniques
- **BD-JB** — Blu-ray Disc Java exploit; userland entry vector using BD-Java on physical discs (FW 1.00-7.61)
- **Y2JB** — Userland payload framework by LightningMods using LUA scripts; covers FW 4.03-13.40
- **P2JB** — Kernel exploit by LightningMods targeting cr_ref/kqueueex syscall; covers FW 9.00-12.70
- **Lapse** — Kernel exploit by Gezine using semaphore UAF; covers FW 1.00-10.01
- **Poops** — Kernel exploit by ChendoChap via sys_netcontrol UAF; covers FW 4.03-12.00
- **UMTX2** — Kernel exploit via umtx syscall; covers FW 1.00-7.61
- **kqueueex** — Kernel syscall abused by P2JB for cr_refcount overflow; requires up to 7 hours of spamming
- **etaHEN** — Homebrew enabler (payload loader) by LightningMods; current version 2.4B
- **ItemzFlow** — Backup manager and homebrew launcher for PS5; current version 1.08
- **payload** — A binary program injected into kernel memory to enable homebrew execution
- **cr_ref** — A kernel reference count structure targeted by the P2JB overflow exploit
- **sys_netcontrol** — A network control syscall that Poops exploits via use-after-free
- **userland** — Unprivileged execution context (EL0); first stage of jailbreak before kernel access
- **homebrew** — Unauthorized third-party software running on a jailbroken console
- **OFW** — Official Firmware; Sony's signed, production firmware releases
