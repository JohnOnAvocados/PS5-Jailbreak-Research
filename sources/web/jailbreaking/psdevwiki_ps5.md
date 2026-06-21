# PSDevWiki PS5

## Source URL
https://www.psdevwiki.com/ps5/

## Domain
psdevwiki.com

## System Layer
jailbreaking

## Summary
Community wiki for PS5 reverse engineering and developer documentation, created February 2019. Contains 70+ articles covering hardware specifications, SKU models, peripherals, vulnerabilities, exploit chains, homebrew development, system software internals, and service/debug hardware (CP Box).

## Key Concepts
- Hardware: Zen 2 CPU, RDNA 2 GPU, GDDR6 memory, storage, media, motherboard revisions, serial flash
- SKU Models: DevKit (debugging/hardware dev), TestKit (QA testing)
- Peripherals: DualSense controller protocol and HID interfaces
- Vulnerabilities: catalog of known bugs, exploit chains per firmware
- Homebrew Enabler: runtime payload loaders (etaHEN, Kstuff)
- Reverse Engineering: data structures, partition layouts, hypervisor internals, kernel structures, secure module (SM) analysis
- System Software: error codes, filesystem layout, PUP structure, title ID format, param.json schema, safe mode options, build string decoding, IDU/retail mode
- CP Box: service connectors, boot ROM流程, non-volatile storage (NVS) layout

## Security Relevance
Provides the complete hardware-software trust boundary map for PS5: Secure Boot chain, hypervisor isolation boundaries, kernel security mechanisms, and secure module authentication. Essential reference for understanding which security layers each exploit bypasses.

## Relevance Tags
ps5, wiki, hardware, software, reverse engineering, exploit, kernel, hypervisor, homebrew, development
