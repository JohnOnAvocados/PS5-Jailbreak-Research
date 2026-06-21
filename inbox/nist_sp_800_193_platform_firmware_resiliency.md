# NIST SP 800-193: Platform Firmware Resiliency Guidelines

## Source URL
https://csrc.nist.gov/publications/detail/sp/800-193/final

## Domain
csrc.nist.gov

## System Layer (choose one)
boot_chain

## Summary
NIST Special Publication 800-193 (May 2018) provides technical guidelines for platform firmware resiliency against destructive attacks. The platform is defined as the collection of hardware and firmware components needed to boot and operate a system. The document promotes three security mechanisms: protection against unauthorized changes, detection of unauthorized changes that occur, and recovery from attacks rapidly and securely. Targets include BIOS, Option ROMs, and platform firmware. Implementers include OEMs, component/device suppliers, and system administrators.

## Key Concepts
- platform firmware resiliency against destructive attacks
- three pillars: protect, detect, recover
- roots of trust for integrity verification
- covers BIOS, Option ROM code signing
- platform firmware must resist unauthorized modification
- rapid recovery mechanisms required after attack
- applies to OEMs, component suppliers, and system administrators
- published May 2018 by Andrew Regenscheid (NIST)

## Security Relevance
SP 800-193 defines the resiliency requirements for platform firmware, which is the foundation of the boot chain. It directly relates to trusted boot models by mandating protection, detection, and recovery mechanisms for the lowest levels of system firmware.

## Relevance Tags
nist, platform firmware, resiliency, bios, option rom, code signing, root of trust, firmware security
