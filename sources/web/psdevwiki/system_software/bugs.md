# Bugs
## Source URL
https://www.psdevwiki.com/ps5/Bugs
## System Layer
system_software
## Summary
Catalog of PS5 bugs organized by exploitability. Covers WebKit JSC bugs (get_by_id_with_this ProxyObject JSScope leak CVE, integer underflow CVE-2023-38600, mmap alignment issue), JIT-disabled bugs (CVE-2024-27833 SBFX overflow, CVE-2023-41993 clobberize, DFG Abstract Interpreter type confusion), non-exploitable memory exhaustion bugs (CVE-2023-28205 CloneDeserializer UaF, heap/string overflow). Also covers Chrome V8 CVEs (2025-6554, 2025-5419, 2024-0517) and Mozilla SpiderMonkey (CVE-2018-5093 WebAssembly Table underflow), all untested on PS5.
## Key Concepts
- WebKit JSC bugs organized by exploitability status
- get_by_id_with_this + ProxyObject: JSScope object leak, FW 6.00-9.60, patched FW 10.00
- CVE-2023-38600: integer underflow in genericTypedArrayViewProtoFuncCopyWithin, FW 6.00-8.60, patched FW 9.00
- mmap pointer address misalignment: HAVE_MAP_ALIGNED workaround in OptionsPlaystation.cmake
- CVE-2024-27833: JSC SBFX immediate overflow (JIT disabled on PS5, not exploitable)
- CVE-2023-41993: JSC DFG clobberize ByOffset nodes (JIT disabled, not exploitable)
- DFG Abstract Interpreter clobberWorld type confusion (JIT disabled, not exploitable)
- CVE-2023-28205: CloneDeserializer deserialize UaF, FW <= 7.61, crash only
- Chrome V8 CVEs: 2025-6554, 2025-5419, 2024-0517 — untested on PS5
- CVE-2025-6558: requires WebGL2, probably not affecting PS5
- CVE-2018-5093: SpiderMonkey WebAssembly Table integer underflow, untested
## System Role
Bug tracking for potential exploit development
