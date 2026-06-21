# UEFI Specifications

## Source URL
https://uefi.org/specifications

## Domain
uefi.org

## System Layer (choose one)
boot_chain

## Summary
The UEFI Specifications page is the official repository for the Unified Extensible Firmware Interface (UEFI) specification, maintained by the UEFI Forum. It hosts the core UEFI specification (currently version 2.x), which defines the interface between operating systems and platform firmware during boot. The specification covers boot services, runtime services, protocols, firmware management, authenticated variables, Secure Boot, and capsule update mechanisms.

## Key Concepts
- UEFI 2.x specification is the industry standard for firmware-OS interface
- defines boot services, runtime services, and protocols
- Authenticated Variables and Secure Boot are specified in UEFI
- platform firmware must implement signature verification (db/dbx/KEK/PK)
- capsule-based firmware update mechanism is defined
- specification covers both IA-32 and x64 architectures

## Security Relevance
The UEFI specification defines the foundational trusted boot chain for modern platforms. Secure Boot, authenticated variable updates, and measured boot are all specified here, making this the central document for understanding how boot integrity is enforced at the firmware-OS boundary.

## Relevance Tags
uefi, firmware, secure boot, boot chain, platform security, specification, authenticated variables
