# NIST SP 800-147: BIOS Protection Guidelines

## Source URL
https://csrc.nist.gov/publications/detail/sp/800-147/final

## Domain
csrc.nist.gov

## System Layer (choose one)
boot_chain

## Summary
NIST SP 800-147 (April 2011) provides guidelines for preventing unauthorized modification of BIOS firmware on PC client systems. Covers conventional BIOS, EFI BIOS, and UEFI BIOS stored in system flash memory. Addresses the threat of persistent malware presence through BIOS corruption or implantation. Focuses on x86/x64 client platforms but is design-independent. Controls include authenticated BIOS updates, cryptographic signature verification, and write-protection mechanisms for flash memory.

## Key Concepts
- guidelines for BIOS firmware integrity on PC client systems
- covers conventional BIOS, EFI BIOS, and UEFI BIOS
- addresses threat of persistent BIOS-resident malware
- authenticated BIOS updates via digital signatures
- cryptographic verification before flash write operations
- write-protection mechanisms for system flash memory
- applies primarily to x86/x64 enterprise-class platforms
- authored by David Cooper, W. Polk, A. Regenscheid, M. Souppaya (NIST)
- published April 2011

## Security Relevance
This standard establishes the baseline for BIOS-level security that forms the first stage of the trusted boot chain. Authenticated firmware updates and flash protection are prerequisite mechanisms for any secure boot implementation.

## Relevance Tags
nist, bios, firmware protection, authenticated update, flash memory, boot chain, platform security
