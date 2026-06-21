# PS5 Concept Map

## Hardware Layer
- [[hardware_architecture]]

## Firmware Layer
- [[boot_chain]]
- [[secure_boot]]
- [[update_mechanism]]

## System Layer
- [[hypervisor_architecture]]
- [[kernel_architecture]]

## Security Layer
- [[security_model]]

## System View
- [[system_architecture]]

## Connection Summary

Hardware provides the physical foundation: SoC with
fused Boot ROM keys, AMD PSP for cryptography, OTP
fuses for security revision ratcheting, memory
controllers with XOM, and serial flash and NAND
storage. This immutable layer roots trust for the
entire system.

The firmware layer builds on hardware through three
interconnected concepts. The boot chain defines the
execution sequence from Boot ROM to kernel. Secure
boot provides cryptographic verification at each
stage using RSA-4096, RSA-3072, AES-128-CBC, and
revision nonces. The update mechanism delivers
authorized modifications through signed PUP files.
These form a closed loop: the boot chain depends on
secure boot for verification, updates modify boot
chain components, and the update mechanism is
verified by secure boot's key hierarchy.

The system layer operates on initialized firmware:
the hypervisor creates isolated execution domains,
and the kernel manages resources within hypervisor-
controlled space. The security model permeates all
layers — hardware OTP fuses, firmware cryptographic
verification, hypervisor memory isolation, and
secure module runtime services. Each layer constrains
the next, creating a unified chain of trust from
first power-on through every subsequent operation.
