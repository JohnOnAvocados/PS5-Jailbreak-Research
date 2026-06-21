# AMD Platform Security Processor

## Source URL
https://en.wikipedia.org/wiki/AMD_Platform_Security_Processor

## Domain
en.wikipedia.org

## System Layer (choose one)
cpu_architecture

## Summary
The AMD Platform Security Processor (PSP), also known as AMD Secure Technology, is a trusted execution environment subsystem integrated into AMD microprocessors since approximately 2013. It is a dedicated ARM Cortex-A5 with TrustZone extension embedded on the CPU die as a coprocessor. The PSP manages boot process, initializes security mechanisms, and monitors system events. It is the first processor to run on system power-up and controls release of x86 cores.

## Key Concepts
- ARM Cortex-A5 with TrustZone running proprietary firmware
- Boot ROM performs initial hardware init and SPI ROM verification
- Loads AGESA (off-chip firmware) from SPI flash into PSP memory
- PSP activates x86 cores only after security checks pass
- Firmware stored in ordinary UEFI image for easy extraction/analysis
- Runs in system DRAM with full MMIO access — no memory isolation
- Provides RNG for RDRAND instruction and TPM services
- Used for hardware downcoring (fusing off cores during manufacturing)

## Security Relevance
The PSP is the root of trust in the AMD platform — it runs before the x86 cores and manages all security-critical boot paths. Its proprietary firmware cannot be audited (AMD refused open-sourcing). Its full access to system DRAM and lack of memory isolation from user-mode applications make it a high-value attack surface. Multiple vulnerabilities (CTS Labs 2018, Cfir Cohen 2017) have been reported.

## Relevance Tags
amd psp, platform security processor, secure processor, arm cortex-a5, trustzone, amd secure technology, boot rom, firmware security
