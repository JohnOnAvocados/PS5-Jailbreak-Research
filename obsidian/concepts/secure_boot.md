# Secure Boot

## Concept Summary

The PS5 secure boot architecture implements a
cryptographic chain of trust spanning every stage
from power-on through kernel execution. At the
hardware root, immutable Boot ROM stores keyseed
sets (Keys 2-9) fused into silicon at manufacture
time. The AMD Platform Security Processor (PSP)
manages all cryptographic operations within an
isolated secure environment, deriving actual key
material from ROM seeds without exposing raw keys
outside the secure processor. Each boot stage
verifies the next cryptographically before
transferring control.

The key hierarchy uses RSA-4096 for the Secure
Loader header signature, RSA-3072 for kernel and
package signing, and dual-layer AES-128-CBC for
firmware body protection. The first AES layer uses
a global firmware key common across all versions.
The second layer is keyed to a revision-specific
nonce (SHA-256 at header offset 0x120), uniquely
binding each firmware release. Without the correct
nonce, the Secure Loader body cannot be decrypted
even with all other key material. Stage-specific
key domains (EMC, EAP, KBL) are independently
managed with HMAC-SHA1 integrity protection,
preventing compromise of one domain from cascading.

Beyond initial boot, secure modules (0x8002xxxx)
provide trusted runtime services after kernel load.
These include authmgr, kms, pup, pfs, driveauth,
pltauth, npdrm, otpaccess, otpctrl, and others,
all running within the PSP's isolated environment.
The pup module (0x80021002) handles verification
of PS5UPDATE.PUP files during system updates.

Keystone execute-only memory (XOM) is a hardware
feature integrated into the memory controller. XOM
pages can be fetched and executed but cannot be read
or written by any software — including kernel and
hypervisor. XOM protects Boot ROM routines, PSP
firmware, secure module code, key derivation
functions, and OTP access control, configured
during early boot and persisting throughout
operation.

## Role in System

Secure boot is the foundational verification layer.
It ensures every component from Secure Loader
(serial flash offset 0x800) through EMC firmware
(offset 0x4000), Hypervisor Loader, and kernel is
authentic before execution. Four stage transitions
enforce this: Stage 0 to 1 (Boot ROM validates
Secure Loader magic E4 DB 7C 02 and RSA-4096
signature against ROM Key 2), Stage 1 to 2 (dual
AES-CBC decryption, SHA-256 integrity, security
revision check), Stage 2 to 3 (EMC returns control,
Hypervisor Loader verified), Stage 3 to 4 (kernel
SELF RSA-3072 verified, EAP decrypted, HMAC-SHA1
validated, virtualization activated).

Anti-rollback operates at every transition. OTP
fuses store the minimum allowed security revision,
burned irreversibly per update. Each stage checks
against the OTP minimum. Revision nonces provide
secondary enforcement by binding Layer 2 decryption
keys to unique SHA-256 nonces. Security revisions
progress from 0x00000001 (FW 0.85-1.XX) through
0x0003FFFF (FW 11.00+).

## Connections

- [[boot_chain]]
- [[hardware_architecture]]
- [[security_model]]
- [[kernel_architecture]]
- [[update_mechanism]]

## Security Relevance

- Boot ROM is immutable and unpatcheable — any
  exploitable bug is permanent and represents the
  highest-value target in the system
- Key hierarchy depth ensures domain isolation:
  RSA-4096, RSA-3072, AES-128-CBC, and stage-
  specific keys are independently managed so
  no single compromise breaks the entire chain
- XOM prevents runtime extraction of security code
  even from kernel level by blocking read/write at
  the hardware memory controller level
- Documented weaknesses: PKG RSA-3072 private key
  leak with CRT parameters, static M.2 keys across
  FW 1.00-12.20, PS4 key sharing, CP Box debug
  infrastructure with Assist Mode on TestKits
## Graph Reference
research/firmware/secure_boot.md
