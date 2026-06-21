# OEM Secure Boot

## Source URL
https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-secure-boot

## Domain
learn.microsoft.com

## System Layer (choose one)
boot_chain

## Summary
Microsoft's OEM guidance for implementing Secure Boot on Windows devices. Secure boot ensures a device boots using only software trusted by the OEM. The firmware checks signatures of each boot component (UEFI drivers, Option ROMs, EFI applications, OS). Requires UEFI v2.3.1 Errata C, signature databases (db, dbx, KEK), firmware signing with RSA-2048 SHA-256, and rollback protection. The boot sequence proceeds from firmware verification through Windows Boot Manager, driver loading, kernel startup, antimalware loading, and user-mode initialization.

## Key Concepts
- Secure Boot verifies signatures of all boot software components
- requires UEFI v2.3.1 Errata C with SecureBoot=1 and SetupMode=0
- signature database (db) lists trusted signers; dbx lists revoked signatures
- Key Enrollment Key (KEK) database manages db/dbx updates
- Platform Key (PK) locks firmware; can update KEK or disable Secure Boot
- firmware signing must use RSA-2048 with SHA-256 minimum
- signature databases stored in firmware NV-RAM at manufacturing time
- Windows Boot Manager is signed by Microsoft; backup copy exists
- rollback protection prevents downgrade of firmware to older versions
- Secure Boot certificates from 2011 begin expiring June 2026

## Security Relevance
This document describes the OEM-side implementation of the Secure Boot chain of trust, which is a critical component of platform trusted boot. It shows how hardware root of trust propagates through UEFI firmware to the OS loader.

## Relevance Tags
secure boot, uefi, firmware, oem, windows, signature verification, chain of trust
