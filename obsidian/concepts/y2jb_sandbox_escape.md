# Y2JB Sandbox Escape

## Concept Summary

The Y2JB (YouTube to Jailbreak) framework exploits CVE-2021-38003 — a V8 vulnerability where JSON.stringify leaks the internal TheHole sentinel value — within the PS5 YouTube TV application. Provides userland JavaScript code execution across FW 2.00-13.40, the broadest firmware range of any PS5 exploit, and remains unpatched over 5 years after Chrome patched it because the YouTube app is independently updatable.

The PS5 YouTube app uses Google's Cobalt API (version 21+) with an embedded V8 engine. The exploit chain: leak TheHole via crafted JSON.stringify → corrupt Map.size to -1 → OOB memory access → arbitrary R/W in V8 heap → libkernel base leak → ROP chain → kernel exploit delivery. Y2JB pairs with P2JB (kqueueex cr_ref, FW 9.00-12.70), netcontrol/POOPS (<=12.00), or Lapse (<=10.01) for the full jailbreak chain.

Key versions: Y2JB 1.4 introduced kexp shellcode handoff (eliminating USB), Y2JB 1.6 extended firmware range, and P2JB-Y2JB port 2.4 (matem6, May 2026) added in-sandbox ELF parsing and automated GPU DMA Debug Settings activation.

## Role in System

The primary userland entry point for digital (disc-less) PS5 consoles. Y2JB's unpatched status makes it the longest-lived public exploit in PS5 history. It is the only userland entry available on FW 12.70-13.40 after P2JB was patched.

## Connections

- [[jailbreak_comprehensive]]
- [[cve_timeline]]
- [[attack_surface]]
- [[security_model]]

## Graph Reference
research/userland/y2jb_sandbox_escape.md
