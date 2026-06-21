# Vulnerabilities
## Source URL
https://www.psdevwiki.com/ps5/Vulnerabilities
## System Layer
security
## Summary
Comprehensive catalog of PS5 vulnerabilities across all layers. Covers usermode exploits (game savedata via mast1c0re/Lua/YARPE, BD-JB, WebKit, JavaScript engine in Netflix/YouTube apps), kernel exploits (kqueueex ucred leak, netcontrol double fdrop, fsc2h_ctrl stack free, aio_multi_delete double free, umtx_shm UaF, IPV6 UaF, exFAT overflow, SMAP bypass, GPU DMA copy, Meme Dumper), hypervisor exploits (TMR OOB, APIC pointers, debug flag, vtable in data segment), AMD Zen 2 hardware vulnerabilities (EntrySign, ZenBleed, Retbleed, Inception), southbridge EMC/EAP/EFC exploits, and secure loader/PSP vulnerabilities.
## Key Concepts
- BD-JB: FW <=4.51 (5 bugs by TheFloW), BD-JB2 FW <=7.61 (path traversal, patched FW 8.00), BD-JB-EX FW <=12.70
- WebKit: loadInSameDocument UaF (CVE-2022-22620) FW <=5.50; CSSFontFaceSet FW 3.00-4.51
- Netflix app: FW 4.03-12.40, multiple V8/SpiderMonkey CVEs, patched FW 12.60
- YouTube app (Y2JB): FW 2.00-13.40, V8 CVE-2021-38003 TheHole leak, not patched as of FW 13.40
- Chrome V8 CVE-2021-38003: JSON.stringify leaks TheHole value, used in Y2JB
- kqueueex (P2JB): ucred ref leak UaF, FW <=12.70, patched FW 13.00
- netcontrol: double fdrop on socket, FW <=12.00
- fsc2h_ctrl: kernel stack free, FW <=10.40
- aio_multi_delete: double free improper locking, FW <=10.01
- umtx_shm (UMTX2): UaF race condition (CVE-2024-43102), FW <=7.61
- IPV6_2292PKTOPTIONS UaF (CVE-2020-7457): FW 3.00-4.51
- GPU DMA copy: bypasses kernel .data write protection, FW >=6.00
- Hypervisor TMR heap OOB: <=6.02 (TheFloW)
- Byepervisor bugs: vtable in data segment, debug flag not wiped after rest mode, both <=2.70
- Prosperous hypervisor exploit: <=4.51 (TMR protection edit, fail0verflow/flatz 2026)
- AMD Zen 2: EntrySign (CVE-2024-36347), ZenBleed (CVE-2023-20593), Retbleed (CVE-2022-29900), Inception/SRSO (CVE-2023-20569)
- mast1c0re: PS2 emulator JIT native execution for Lua/Ren'Py/YARPE
## System Role
Vulnerability catalog for exploit research
