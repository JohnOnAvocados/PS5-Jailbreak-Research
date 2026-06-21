# etaHEN: Primary All-in-One PS5 Homebrew Enabler

## Source URL
https://github.com/etaHEN/etaHEN

## Domain
github.com

## System Layer
jailbreaking

## Summary
etaHEN by LightningMods is the primary all-in-one homebrew enabler for PS5, supporting FW 3.00-10.01 (latest version 2.4B). Replaces Debug Settings with a custom Toolbox UI and provides Rest Mode, Remote Play, Plugin/Payload ELF Menu, and External HDD Menu. Integrates Kstuff for fself/fpkg support, ItemzFlow for backup management, a game overlay (CPU/GPU temp, utilization, local IP), Direct PKG Installer v2 with WebUI on port 12800, FTP server on port 1337, Klog server on 9081, and ELF loader on port 9021. Includes game dumping, cheats/patches via Illusion plugin, Discord RPC, and controller shortcuts.

## Key Concepts
- Homebrew enabler replacing Debug Settings with Toolbox UI
- FW support: 3.00-10.01
- Kstuff integration for fself/fpkg loading
- ItemzFlow backup management integration
- Game Overlay: CPU/GPU temperature, utilization, local IP
- Direct PKG Installer v2 with WebUI (port 12800)
- FTP server (port 1337), Klog server (port 9081)
- ELF loader on port 9021 (john-tornblom's elfldr)
- etaHEN SDK for custom plugin extensions
- Illusion plugin for cheats and patches
- Discord RPC server (port 8000)
- Controller shortcut bindings
- Configurable via config.ini in /data/etaHEN

## Security Relevance
Operates as a post-exploitation framework that transforms a compromised kernel into a usable homebrew environment. By replacing the Sony Debug Settings with a custom Toolbox, it subverts Sony's code execution policy enforcement. The plugin SDK extends the attack surface by allowing third-party code to run with kernel-level privileges, bypassing all platform security controls.

## Relevance Tags
ps5, homebrew, enabler, payload, elf-loader, kstuff, fpkg, plugin, toolbox, lightningmods
