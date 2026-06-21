# Y2JB PS5 Framework

## Source URL
https://github.com/Gezine/Y2JB

## Domain
github.com

## System Layer
jailbreaking

## Summary
Y2JB is a YouTube-based userland exploit framework for PS5 developed by Gezine. Exploits the PS5 YouTube TV application to execute arbitrary JavaScript via the V8 engine on FW 4.03-13.40. When paired with the P2JB kernel exploit, achieves full jailbreak on FW 9.00-12.70. Provides remote JS loader on port 50000 for automated exploit delivery.

## Key Concepts
- Userland entry via YouTube TV app V8 engine JavaScript execution
- Supported firmware: 4.03-13.40 (userland only on >12.70, full jailbreak on 9.00-12.70)
- Y2JB 1.4+: kexp shellcode handoff eliminating USB requirement for ELF loader
- Y2JB 1.6: extended firmware range support for higher OFW versions
- Supports digital/disc-less PS5 consoles (no BD reader required)
- Remote JS loader listens on TCP port 50000 for payload delivery
- Auto-loads kernel exploit and payload manager in sequence
- Compatible with BD-UN-JB for persistent unpatcher delivery across reboots
- Requires system backup restore procedure and specific YouTube app version
- Pairing with P2JB enables cr_ref overflow kernel exploit chain

## Security Relevance
Demonstrates application-level sandbox escape via a first-party Sony application (YouTube). The V8 engine provides sufficient JS capability to build a ROP chain and escalate to kernel exploitation. Represents a userland trust boundary bypass that does not require physical media.

## Relevance Tags
ps5, jailbreak, y2jb, youtube, userland, exploit, framework, gezine, p2jb, v8
