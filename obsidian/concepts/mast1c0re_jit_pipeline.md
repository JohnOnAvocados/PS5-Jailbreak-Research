# mast1c0re JIT Pipeline

## Concept Summary

The mast1c0re exploit family targets the PS2 emulator's dynamic recompiler (JIT compiler) on PS4 and PS5. It exploits a fundamental design-level vulnerability: the emulator must translate untrusted PS2 game savedata into native x86 code for emulation performance, creating a pipeline where attacker-controlled input becomes executable instructions. The JIT output buffer is NOT XOM-enforced, making generated x86 code readable, writable, and executable.

The emulator uses a two-process architecture: `eboot.bin` (can execute JIT code, cr_caps 0x20) and `ps2-emu-compiler.self` (can write JIT code, cr_caps 0x40), communicating through a shared memory bridge at fixed address 0x914104000. Exploitation spans three stages: (1) PS2 code execution via game savedata overflow, (2) emulator escape to native x86 ROP, (3) JIT compiler process takeover via bridge doorbell cmd 0x215 OOB write and VU0 object vtable hijack.

Supports FW 2.00-13.00, the broadest firmware range of any userland entry point. Variants include Luac0re (Lua scripting), UltraC0re (Jak X), and YARPE/YarP2JB (Ren'Py game engine). The exploit is portable across games because the emulator binary is bundled per-title and does not change with system firmware.

## Role in System

Represents the highest-firmware userland exploit path (FW 13.00 ceiling). Unlike Y2JB and WebKit exploits, mast1c0re provides full arbitrary native code execution by controlling both PS2 emulator processes — bypassing all standard userland mitigations without requiring a kernel exploit.

## Connections

- [[jailbreak_comprehensive]]
- [[cve_timeline]]
- [[attack_surface]]
- [[security_model]]

## Graph Reference
research/userland/mast1c0re_jit_pipeline.md
