# UMTX Jailbreak: WebKit-Based PS5 Kernel Exploit

## Source URL
https://github.com/idlesauce/umtx2

## Domain
github.com

## System Layer
jailbreaking

## Summary
UMTX Jailbreak by idlesauce (based on work by shahrilnet, n0llptr, SpecterDev, ChendoChap) is a WebKit-based kernel exploit and jailbreak for PS5 supporting FW 1.00-5.50. Uses PSFree 150b by abc as the WebKit userland entry point. Exploits a use-after-free vulnerability in the FreeBSD umtx (user mutex) subsystem to achieve kernel code execution. Includes a payload menu system, dual ELF loader support (ports 9020 and 9021), and auto-loads john-tornblom's ELF loader. Offers a WebKit-only mode for sending payloads and clearing appcache. Hosted on CloudFlare Pages and GitHub Pages, with a Media PKG for direct browser access. Works on digital (disc-less) consoles via the WebKit attack surface.

## Key Concepts
- WebKit-based userland entry via PSFree 150b
- UMTX kernel vulnerability: use-after-free in FreeBSD umtx subsystem
- FW support: 1.00-5.50
- Payload menu system
- Auto-loading ELF loader (john-tornblom)
- Dual ELF loader support (ports 9020 and 9021)
- WebKit-only mode for payload delivery
- Hosted on CloudFlare Pages and GitHub Pages
- Media PKG for direct WebKit invocation
- Digital console compatible (no disc drive required)

## Security Relevance
Targets the umtx (user mutex) kernel subsystem — a FreeBSD synchronization primitive. Use-after-free in kernel synchronization code is particularly dangerous because it can be triggered from userland via WebKit, allowing browser-originated kernel compromise. The WebKit attack vector is critical as it enables jailbreaking on digital-only consoles that lack a Blu-ray drive, expanding the attack surface to all PS5 hardware variants.

## Relevance Tags
ps5, jailbreak, webkit, umtx, kernel, exploit, use-after-free, freebsd, elf-loader, userland
