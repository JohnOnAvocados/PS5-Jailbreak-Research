# Boot Chain

## Concept Summary

The PS5 boot chain is a multi-stage secure boot process that proceeds from power-on through hardware initialization, firmware loading, and cryptographic verification, culminating in kernel launch. The entire sequence is orchestrated by the AMD Platform Security Processor (PSP), a dedicated ARM-based cryptoprocessor embedded in the SoC that handles all early boot cryptographic operations including RSA-4096/RSA-3072 signature verification, AES-128-CBC encryption and decryption, SHA-256 hashing, and secure key ring management.

The boot chain consists of five primary stages. Stage 0 is the Boot ROM, an immutable mask ROM etched into the SoC die serving as the hardware root of trust. Stage 1 is the Secure Loader (SCE SBL or IPL), the first mutable firmware component, stored on the serial flash and loaded by the Boot ROM into PSP memory. Stage 2 involves the EMC (Embedded Micro Controller) initialization phase, where the southbridge chip manages low-level power sequencing and hardware initialization using its own independent firmware. Stage 3 is the Hypervisor Loader, which initializes virtualization structures including two-stage MMU translation, IOMMU configuration, and interrupt virtualization. Stage 4 is the kernel load, where the final SELF-format kernel binary is verified, decrypted, and launched.

Every stage is cryptographically signed and verified before execution proceeds, forming a chain of trust. The Secure Loader body undergoes dual-layer AES-CBC encryption — the first layer uses a global firmware key, while the second layer is keyed to a revision-specific nonce. Anti-rollback protection is enforced through a monotonically increasing security revision field and a per-revision nonce, preventing booting any firmware older than the currently installed version.

## Role in System

The boot chain is the initialization pathway that transforms the raw hardware into a running system. The serial flash (Winbond W25Q16JVNIM) stores the Secure Loader and EMC firmware at known offsets, while the NAND flash stores the main system software. All critical boot components are physically accessible via the SPI bus, representing both a debugging capability and an attack surface.

The PSP manages the key hierarchy throughout the boot process, passing key rings from the Secure Loader to subsequent stages. The Hypervisor Loader uses the RSA-4096 chain inherited from the Secure Loader to verify the kernel, ensuring the entire boot path from Boot ROM to hypervisor is covered by a single chain of signatures. Keystone XOM (eXecute-Only Memory) protection ensures that critical security code in the boot ROM and Secure Loader cannot be read or dumped even from kernel context.

## Connections

- [[hardware_architecture]]
- [[secure_boot]]
- [[hypervisor_architecture]]
- [[kernel_architecture]]
- [[security_model]]

## Security Relevance

- Immutable Boot ROM is the ultimate root of trust — any vulnerability is permanent and unpatcheable at the hardware level
- Dual-layer AES-CBC encryption prevents booting arbitrary firmware even with access to global signing keys
- Anti-rollback mechanism uses both a security revision field and a per-revision nonce for defense against downgrade attacks
- Serial flash accessed via SPI bus is observable with hardware probing tools, representing a physical attack surface

## Graph Reference

research/firmware/boot_chain.md
