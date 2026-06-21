# Update Mechanism

## Concept Summary

The PS5 firmware update system delivers system
software through Sony's CDN as PUP (PlayStation
Update Package) files. Three update types exist.
Recovery PUP is a complete system image for full
reinstallation via Safe Mode Option 7 — it wipes
user data, writes boot chain components to serial
flash, and restores the console to factory state.
System PUP preserves user data and performs partial
upgrade (800-1200 MB), used for standard firmware
upgrades via internet or Safe Mode Option 3.
System_ex PUP provides targeted component updates
between major releases (100-300 MB) for security
patches or feature additions without full downloads.

All three types are cryptographically verified by
the pup secure module (0x80021002) before any
writes. The PUP structure includes a header (type,
version, size, segment count), RSA-3072 signature
block, manifest with per-segment SHA-256 hashes
and target partitions, and compressed or encrypted
data segments. Segments may use zlib compression,
AES-128-CBC encryption from the boot chain key
hierarchy, and per-segment RSA-3072 signing. The
signature chain is rooted in the same RSA-4096
hierarchy used by the boot chain.

The update process has three phases. Download: the
PS5 fetches updatelist.xml, compares versions, and
downloads the PUP from a URL embedding its SHA-256
hash. Verification: the pup module validates the
RSA-3072 signature, per-segment signatures, and
SHA-256 integrity. If verification fails, the
download is discarded. Installation: the system
reboots into update mode, decrypts segments, writes
to NAND partitions, burns new OTP fuses, and re-
verifies through the boot chain on next startup.
The process is atomic — if interrupted, the system
boots from the previous version or enters recovery.

Safe Mode provides recovery when system software is
corrupted. Accessed by holding the power button for
seven seconds until two beeps, it loads only PSP,
EMC, a minimal kernel, USB mass storage, basic
display, and DualSense via USB. Seven options:
Restart, Change Video Output, Update System Software
(USB or internet), Restore Default Settings, Rebuild
Database, Reset PS5 (data wipe only), and Reset PS5
with Reinstall System Software. USB requires the
file at PS5/UPDATE/PS5UPDATE.PUP on FAT32 or exFAT
with anti-downgrade at PUP metadata and OTP levels.

## Role in System

The update mechanism is the only official channel
for modifying PS5 firmware after manufacturing. It
sits at the intersection of boot chain and system
software, able to update boot components (Secure
Loader, EMC, Hypervisor Loader, kernel), system
partitions, secure modules, configuration, and
language data. Every modification is verified by
the secure boot infrastructure, creating a closed
trust loop. The version history tracks firmware
from FW 1.00 (May 2020) through FW 13.40 (May 2026)
using long format (YY.SS-MM.mm.nn.nn-UU.UU.UU.U.b)
encoding build year, release counter, versions, and
branch, plus short format (MM.mm.nn) for users. OTP
fuses advance with each update as a one-way ratchet.

## Connections

- [[secure_boot]]
- [[boot_chain]]
- [[system_architecture]]
- [[security_model]]

## Security Relevance

- Anti-downgrade enforced at multiple layers: PUP
  metadata comparison, OTP fuse burning during
  installation, and boot chain re-verification on
  every subsequent boot
- USB recovery path trades CDN authentication for
  physical access, but all paths require valid Sony
  signatures verified by the pup module before
  any writes occur
- OTP fuse irreversibility is the ultimate
  enforcement — once a revision is committed, the
  console can never boot below it, making bricking
  a real risk of failed updates
- Static CDN token (tJMRE80IbXnE9YuG0jzTXgKEjIMoabr6)
  across all regions, M.2 dummy keys static across
  FW 1.00-12.20, and PS4 key sharing represent
  design weaknesses in an otherwise robust system

## Graph Reference
research/firmware/update_mechanism.md
