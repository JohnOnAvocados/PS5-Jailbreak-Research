# TheFloW PS5 Security Research

## Source URL
https://github.com/TheOfficialFloW

## Domain
github.com

## System Layer
jailbreaking

## Summary
TheFloW (Andy Nguyen) is the most prolific PS5 security researcher, responsible for multiple critical vulnerabilities and exploits. BD-JB (Blu-ray Disc Java Sandbox Escape) chains 5 vulnerabilities in the BD-J stack for firmware-agnostic, ROP-less code execution — presented at HardWear.io 2022 and Hexacon 2022, extended to 7.61 via path traversal. Discovered CVE-2020-7457 (IPv6_2292PKTOPTIONS UAF), a kernel exploit via setsockopt race condition originally on PS4 and ported to PS5. Also discovered the sys_netcontrol UAF (ExploitNetControlImpl.java) working up to PS5 12.00 (patched in 12.02). BD-JB revisions added Remote JAR Loader, Kernel API (kread/kwrite), and 2x performance optimization. Published exFAT vulnerability PoC for PS5 (kernel panic, not fully exploited). Reports vulnerabilities to Sony via HackerOne bug bounty program ($50K max payout).

## Key Concepts
- BD-JB: Blu-ray Java sandbox escape chaining 5 vulnerabilities
- HardWear.io 2022 and Hexacon 2022 presentations
- CVE-2020-7457: IPv6 socket option use-after-free
- sys_netcontrol UAF for Netgraph exploitation
- Firmware-agnostic, ROP-less code execution via JIT
- BD-JB extended from 4.51 to 7.61 via path traversal
- BD-JB Remote JAR Loader and Kernel API integration
- 2x performance optimization in 2024 BD-JB revision
- exFAT vulnerability PoC (kernel panic only)
- HackerOne responsible disclosure to Sony ($50K max bounty)

## Security Relevance
TheFloW's work demonstrates the researcher perspective in the PS5 security ecosystem — identifying vulnerabilities across multiple attack surfaces (BD-J sandbox, network stack, filesystem). The progression from PS4-era vulnerabilities (CVE-2020-7457) adapted to PS5 shows cross-generational exploit portability when similar codebases are shared. Responsible disclosure via HackerOne, combined with public PoC releases after patching, represents the dual researcher role of finding bugs for both defensive (Sony bounty program) and offensive (public jailbreak) purposes.

## Relevance Tags
ps5, ps4, theflow, andy-nguyen, bd-j, exploit, vulnerability, disclosure, hackerone, jailbreak, kernel, ipv6
