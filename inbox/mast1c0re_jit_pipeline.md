# mast1c0re: PS2 Emulator JIT Pipeline — Deep Analysis

## Overview

The mast1c0re exploit family targets the PS2 emulator's dynamic recompiler (JIT compiler) on PS4 and PS5. It exploits a fundamental design-level gap: the emulator must translate untrusted PS2 game data into native x86 code for performance, creating a pipeline where attacker-controlled input becomes executable instructions. This is not a patched vulnerability but an architectural property — the JIT must process untrusted savedata through a code-generation pipeline. No software mitigation can fully close this without disabling PS2 backward compatibility entirely.

The exploit spans three stages: (1) PS2 code execution via game savedata overflow, (2) PS2 emulator escape to native x86 userland ROP, and (3) JIT compiler process takeover for arbitrary native code execution with the compiler's elevated privileges. The attack is further amplified by multiple delivery vehicles — Lua scripting, Ren'Py game engine exploits, YARPE (Yet Another Ren'Py Exploit), and the Artemis Engine — each providing different game-specific entry points into the same underlying emulator vulnerability.

mast1c0re Part 2 supports FW 2.00-13.00, making it the broadest-firmware-range userland entry point on the PS5 (surpassing even Y2JB's 2.00-13.40 range when considering the full exploit chain). Unlike Y2JB and WebKit exploits, mast1c0re's JIT output buffer is NOT XOM-enforced, meaning the generated x86 code can be read, written, and executed — a critical advantage for post-exploitation.

## Emulator Architecture

### Two-Process Design

The PS2 emulator is divided into two separate processes with complementary security privileges:

| Process | Binary | Role | JIT Privilege | Kernel Capability Flag |
|---------|--------|------|---------------|----------------------|
| Application | `eboot.bin` | Emulation main loop, PS2 hardware callbacks, game logic | Can EXECUTE JIT code (RX) | `sceSblACMgrIsJitApplicationProcess` (cr_caps 0x20) |
| Compiler | `ps2-emu-compiler.self` | Dynamic recompilation, code generation | Can WRITE JIT code (RWX) | `sceSblACMgrIsJitCompilerProcess` (cr_caps 0x40) |

This split is a security measure: the compiler process (which handles untrusted data from game savedata) can write code but not execute it directly, while the application process can execute code but cannot write it. An attacker who compromises only one process cannot achieve arbitrary native code execution — they would need to control both.

The JIT compiler process has higher kernel capabilities (cr_caps 0x40) than the application (cr_caps 0x20). Notably, the compiler process can create network sockets (AF_INET/AF_INET6), while the application process has these syscalls blocked via kernel credential restrictions (`ENOSYS` for socket creation). This means the compiler process is both the more powerful and more restricted target.

### Inter-Process Communication: The Bridge

The two processes communicate through a shared memory region called the bridge:

- **Region name:** `ps2_bridge_comm_rw`
- **Fixed address:** `0x914104000` (mapped identically in both process address spaces)
- **Function:** Bidirectional communication for JIT compilation requests and code delivery

The bridge mechanism works via a doorbell protocol. The application process sends compilation requests through the bridge, and the compiler process reads them, performs JIT compilation, and writes the resulting x86 code back. The bridge contains command codes, data buffers, and completion signals.

A critical vulnerability in the bridge protocol is **doorbell command `0x215`**, which provides an out-of-bounds write into the compiler's heap. This OOB write is the primary vector for crossing from the application process into the compiler process.

### Emulator Bundling: Firmware Independence

A crucial architectural property: the PS2 emulator binary is **bundled inside each PS2-classic package**, not part of the PS5 system firmware. Each PS2 classic title (downloaded from the PlayStation Store) ships with its own copy of `eboot.bin` and `ps2-emu-compiler.self`. This means:

1. The emulator version varies per game title, not per firmware version
2. Sony cannot patch the emulator across all titles via a system update — each title must be individually updated
3. Older emulator builds persist in the wild as long as the corresponding game remains downloadable
4. The core exploit mechanism (bridge protocol, OOB in cmd 0x215, VU0 object vtable dispatch) is shared across emulator builds

Part B of the exploit chain (the emulator escape and JIT compiler takeover) targets the emulator itself, not any specific game. The same technique works across multiple PS2 classic titles with only offset adjustments needed. A portability checker (`scripts/check_portable.py` in the UltraC0re repository) scans a JIT-compiler dump for the exact signatures — the `cmd 0x215` OOB-write doorbell, the hijackable `method70` vcall on a heap object, and the required ROP gadget set.

### Two PS2 Emulation Methods on PS5

PS5 has two distinct PS2 emulation paths with different security implications:

#### Method 1: PS4 SDK PS2 Emulator (via PS4 Backward Compatibility)
- Uses `PS2emu` from PS4 PKG, running through PS4 emulation layer on PS5
- Available since FW ~2.00
- Games have CUSA (PS4) Title ID prefix
- Version numbering: XX.YY (PS4 format)
- **This is the emulator that mast1c0re was originally developed against**
- Running as a PS4 process means fewer PS5-specific security restrictions

#### Method 2: PS5 SDK PS2 Emulator (Native)
- Direct PS5 PS2 emulator compiled with PS5 SDK
- Available since FW 9.00 (May 2024)
- Games have PPSA (PS5) Title ID prefix
- PKG size differs from PS4 version
- Version numbering: XX.000.0YY
- **Supports game savestates** — indicating tighter hypervisor/kernel integration
- The native emulator likely has a different security model, but the JIT compiler attack surface persists

Whether the native PS5 emulator has the same JIT vulnerabilities as the PS4-compat path is an open question. The native emulator's tighter hypervisor/kernel integration (required for savestates) may close some attack vectors while potentially introducing new ones.

## Exploit Chain: Three Stages

### Stage 1: PS2 Code Execution (Game-Specific)

The first stage achieves arbitrary MIPS code execution within the PS2 emulation context. This is game-specific — each exploitable game title has a different vulnerability that allows code execution in the PS2 guest.

#### Star Wars: Racer Revenge (Primary Vector)
- **Title IDs:** CUSA03474 (USA), CUSA03492 (EU)
- **Vulnerability:** Stack buffer overflow via crafted savedata
- The savedata image is modified to be larger than the original (original savedata too small to fit exploit files)
- Savedata must be resigned for the target console
- **Trigger:** Navigate to "OPTIONS -> HALL OF FAME" in the game menu

#### Okage: Shadow King (Original mast1c0re Vector)
- Used in McCaulay's original mast1c0re repository
- Also a savedata-based buffer overflow

#### Jak X (UltraC0re Vector)
- **Vulnerability:** PS2 VMC save format exploitation
- Reversed the PS2 VMC save format (header/body/footer, CRC32, recomputed ECC)
- Profile-name overflow gives control of `$pc` in the PS2 guest
- **Part A is game-specific** — must be redone per title

#### Artemis Engine (Lua-Based)
- Lua scripting engine embedded in certain PS4 games
- Lua sandbox escape provides userland code execution
- Used by maj0r and n0llptr for P2JB kernel exploit delivery (2026)

### Stage 2: Emulator Escape (Application Process Takeover)

Once PS2 code execution is achieved, the attacker targets the emulator's native code to escape the PS2 sandbox and gain code execution in the `eboot.bin` process.

#### Technique: Partial Pointer Overwrite

Address Space Layout Randomization (ASLR) is active on both PS4 and PS5. However, the page size is 0x4000 (16 KB), meaning the least significant 14 bits of any code address are always the same. The attacker exploits this by overwriting only the least significant byte of a function pointer — a **partial pointer overwrite** — which is fully deterministic despite ASLR.

For example, if a target function's address always ends in `0x50`, changing it to `0x51` redirects execution to `pc + 1` — a deterministic shift regardless of the base address.

#### Vector: IOP RAM Pointer Redirection

The PS2 emulator uses memory read/write callbacks to handle PS2 hardware access. Specific PS2 memory addresses (documented on ps2tek) control hardware functionality and require emulator intervention. The attacker overwrites the emulator's internal pointer to IOP RAM (normally pointing to the fixed address `0x9000000000`) so that PS2 reads/writes to IOP RAM are redirected to attacker-controlled memory.

#### Vector: SMAP/DEV9 Register Corruption (UltraC0re method)

UltraC0re uses a different escape path by driving the emulated SMAP/DEV9 network-adapter registers (`SCMD`/`NCMD`). This triggers an OOB that corrupts `gNStatusBuffer` and then the native IO-read dispatch table, redirecting a function pointer to give native x86-64 RIP control in the `eboot.bin` process.

#### Result: Native ROP in Application Process

After the escape, the attacker has:
- Base address leaks (anti-ASLR for eboot, libc, libkernel)
- Arbitrary read/write primitives
- Ability to make direct syscalls
- RWX memory via `sceKernelJitCreateMapAliasSharedMemory`
- A ROP chain in the `eboot.bin` process

However, the application process can **execute** JIT code but **cannot write** it. To create truly arbitrary native code (not just ROP), the attacker must also compromise the compiler process.

### Stage 3: JIT Compiler Process Takeover

This is the most technically sophisticated stage — crossing from the `eboot.bin` process into the `ps2-emu-compiler.self` process to achieve full arbitrary native code execution.

#### The Bridge OOB: cmd 0x215

The bridge shared memory between the two processes uses a doorbell mechanism. Doorbell command `0x215` contains an out-of-bounds write vulnerability: it reads a 4-byte signed integer at a controlled offset within the bridge region and uses it as an array index for a write operation **without bounds checking**.

The bridge is mapped at `0x914104000` in both processes. The attacker controls which index is written via `ptrWithinBridgeRegion` at `0x914105B30`.

Two OOB write variants exist:
1. **Vulnerability 1:** OOB write with detectable stride — can be used but timing is less predictable
2. **Vulnerability 3:** OOB write with stride of `0x10` (a factor of the page size) — offsets within different pages are **consistent across different runs**, making this the preferred variant

#### Heap ASLR Bypass via InstructionMappingCache

The compiler process's `SceLibcHeap` is allocated on the heap. The `instructionMappingCache` array is stored at a predictable offset within the heap. Key insight: the heap randomization has only 10 bits of entropy (`2^10 == 1024` possible positions), making it feasible to brute force.

The attacker picks an OOB write index that targets address `0x201000860` — guaranteed to corrupt `instructionMappingCache` at one of 1024 possible offsets. An oracle attack identifies exactly which entry was corrupted: request the compiler to JIT each of the 1024 PS2 addresses that could correspond with the corrupted cache entry until an anomalous result is found. Once the index is identified, the array base address can be calculated, revealing the heap base address (`- 0x860`), and from that the address of anything else on the heap.

#### VU0 Object Vtable Hijacking

The compiler process maintains a **VU0 object** (Vector Unit 0, part of the PS2's Emotion Engine) on its `SceLibcHeap`. This object has a virtual method table (vtable) and a virtual method at index 70 (`method70`).

The attack uses `cmd 0x215` in two phases:
1. **First `cmd 0x215`:** Plants a **fake vtable** and a **fake stack** onto the VU0 object in the compiler's heap
2. **Second `cmd 0x215` with `jmp_vtable` flag:** Triggers the compiler to perform a virtual call through `method70` on the corrupted VU0 object — but the vtable now points to attacker-controlled data

Result: **RIP control inside the `ps2-emu-compiler.self` process**.

#### Persistent ROP Framework in the Compiler

Once inside the compiler process, the attacker doesn't just execute a one-shot payload — they establish a **persistent ROP framework**:

1. The hijacked call stack-pivots into a controlled ROP frame
2. The ROP frame is turned into a **persistent spin-loop**
3. The `eboot.bin` (Lua-side) acts as a **producer/consumer** over the bridge
4. The Lua code feeds calls/syscalls into the spin-loop and reads results
5. This creates a **remote-call primitive** into the privileged `0x40` process

No further compilation is needed — the attacker now has arbitrary call capability in the compiler process.

#### Socket Creation for Full Network Capability

The primary reason for taking over the compiler process: the application process (`eboot.bin`) has `AF_INET`/`AF_INET6` socket creation blocked (`ENOSYS`). The compiler process (`cr_caps 0x40`) can create sockets. The exploit chain:

1. Uses the remote-call primitive to invoke `socket(AF_INET)` in the compiler process
2. Passes the resulting file descriptor back to `eboot.bin` via `SCM_RIGHTS` (fd-pass over Unix domain sockets)
3. `eboot.bin` does `bind`/`listen`/`accept` natively
4. Runs whatever Lua code is sent over the network connection

This is the **final unlock** — full network-capable native code execution without any kernel exploit.

## Variants and Delivery Vectors

### mast1c0re (Original — CTurt/McCaulay)
- **Games:** Okage: Shadow King, Star Wars: Racer Revenge (added later)
- **Technique:** PS2 stack buffer overflow -> emulator escape -> native ROP
- **Repository:** github.com/McCaulay/mast1c0re
- **Toolchain:** Requires PS2SDK to compile PS2 shellcode, okrager for savedata patching
- **Firmware support:** PS4 all, PS5 2.00-13.00
- **Payload:** Native userland ROP execution

### mast1c0re Part 2 (CTurt — JIT Compiler Attack)
- **Extension:** Adds JIT compiler process takeover (Stage 3)
- **Technique:** Bridge `cmd 0x215` OOB write -> `instructionMappingCache` heap oracle -> VU0 vtable hijack -> persistent ROP in compiler
- **Firmware support:** PS4/PS5 (requires emulator with `sys_jitshm_create` limit), PS5 FW <=13.00
- **Key innovation:** Full arbitrary native code (not just ROP) by controlling both processes
- **Sony response:** 65MB JIT code allocation limit introduced in FW 6.00, but doesn't fix the root cause

### Luac0re (Gezine — Lua-Enhanced mast1c0re)
- **Repository:** github.com/Gezine/Luac0re
- **Games:** Star Wars: Racer Revenge (CUSA03474/CUSA03492)
- **Technique:** Minimal PS2 shellcode to escape ps2emu, then leverages embedded Lua 5.3 interpreter in the game executable for exploit development
- **Key advantage:** Lua scripting for easier exploit development instead of raw PS2SDK compilation
- **Version 2.0+:** JIT compiler exploit added for arbitrary native code execution on latest PS4/PS5 firmwares without kernel exploit
- **Bypasses:** Non-AF_UNIX domain socket restriction (PS5 FW 8.00+)
- **Chains with:** Poopsploit (kernel exploit, FW <=12.00), P2JB (FW 9.00-12.70)
- **Tools:** remote_lua_loader for savedata resigning

### UltraC0re (matem6 — Jak X-Based)
- **Repository:** github.com/matem6/UltraC0re
- **Game:** Jak X (PS2-on-PS5)
- **Vulnerability:** Profile-name overflow in VMC save format -> PS2 PC control
- **Escape:** SMAP/DEV9 register corruption -> IO-read dispatch table corruption
- **Compiler takeover:** Bridge `cmd 0x215` OOB -> VU0 vtable -> persistent ROP
- **Key innovation:** Full documented 5-stage chain, portability analyzer script
- **Contribution:** Demonstrated that Part B (emulator escape + compiler takeover) is **portable across games** — the emulator binary is bundled per-title and doesn't change with system firmware
- **Portability checker:** `scripts/check_portable.py` scans JIT-compiler dumps for exploit signatures

### YARPE (Helloyunho — Ren'Py Game Engine Exploit)
- **Repository:** github.com/Helloyunho/yarpe
- **Game:** Arcade Spirits: The New Challengers (Ren'Py engine game)
- **Technique:** Ren'Py scripting engine sandbox escape -> userland code execution
- **Delivers:** Python-based payload to kernel exploit chain
- **Firmware:** PS5 4.03-12.XX

### YarP2JB (matem6 — Ren'Py + P2JB Chain)
- **Repository:** github.com/matem6/YarP2JB
- **Combines:** YARPE userland entry + P2JB kernel exploit
- **Game:** Arcade Spirits: The New Challengers
- **Technique:** Ren'Py sandbox escape -> P2JB cr_ref overflow via kqueueex -> GPU DMA Debug Settings -> in-place ELF loader
- **Firmware:** PS5 9.00-12.70 (validated on 11.60 and 10.40)
- **Notable:** Closes the game after completion without kernel panic
- **In-place ELF loading:** Pre-allocates region before leak, patches `vm_map_entry` protection byte via kernel R/W to make it RWX — bypasses per-process `vm_map_entry` limit that blocks a second payload. On PS4 edition, temporarily swaps `sysent` to PS5-native so PS5 ELF syscalls resolve correctly.
- **Runtime:** ~45 min (PS5 edition), ~52 min (PS4 edition on PS5)

### Artemis Engine Lua (n0llptr, maj0r)
- **Technique:** Artemis Engine (game engine) Lua sandbox escape
- **Delivers:** P2JB kernel exploit via Lua
- **Firmware:** PS5, combined with mast1c0re-P2JB chain

## JIT Code Allocation Limit (Sony's Response)

Sony's primary response to the mast1c0re research was not to fix the root cause (which would require redesigning the emulator architecture) but to limit the blast radius. PS5 firmware 6.00 (and equivalent PS4 firmware) introduced a global variable `allocatedJitMemoryTowardsLimit` in `kern_jitshm.c`:

```c
// sys/freebsd/sys/kern/kern_jitshm.c (conceptual reconstruction)
static uint64_t allocatedJitMemoryTowardsLimit;

int sys_jitshm_create(...) {
    if (allocatedJitMemoryTowardsLimit + requested_size > 65 * 1024 * 1024) {
        return ENOMEM; // JIT allocation limit reached
    }
    allocatedJitMemoryTowardsLimit += requested_size;
    // ... proceed with allocation
}
```

**Limit: 65 MB of total JIT code allocation.**

This limits but does not prevent exploitation. The attacker can still:
1. Use the 65 MB for exploit setup
2. Reuse freed JIT pages (the limit tracks cumulative allocation, not live pages — this may or may not be enforced depending on implementation)
3. Use non-JIT techniques (ROP) for the initial compromise before transitioning to JIT code

Sony's reasoning (per CTurt's analysis): their primary concern was preventing the mast1c0re framework from being used to load patched retail PS4 games. The 65 MB limit was deemed sufficient to block practical game loading while preserving legitimate PS2 emulation functionality.

## Relationship to Other Userland Exploits

### Y2JB (YouTube V8)
- Y2JB uses CVE-2021-38003 (JSON.stringify TheHole leak) in the YouTube app's V8 engine
- Firmware range: 2.00-13.40 (slightly broader than mast1c0re)
- Requires specific YouTube app version and system backup restore procedure
- **Not a JIT exploit** — V8's JIT may be disabled or constrained on PS5
- Cannot create arbitrary native code without separate kernel exploit
- Pairs with P2JB for full chain (Y2JB+P2JB is the primary jailbreak path for FW 9.00-12.70)

### BD-JB (Blu-ray Java)
- Chains 5 bugs in Blu-ray Java stack for userland code execution
- Firmware range up to 12.70 (BD-JB-EX)
- Requires physical BD-R disc and disc drive
- **Also uses JIT exploitation but in Java, not PS2 emulator**
- ROP-less code execution via Java JIT, bypassing XOM
- TheFloW's presentation at HardWear.io 2022 and Hexacon 2022

### Comparison Table

| Property | mast1c0re | Y2JB | BD-JB |
|----------|-----------|------|-------|
| FW Range | 2.00-13.00 | 2.00-13.40 | 1.00-12.70 |
| Nature | Design gap (unpatchable) | CVE (unpatched) | CVE chain (patched each iteration) |
| Hardware Req | Compatible game | YouTube app | BD-R disc + drive |
| Code Execution | Full native via JIT takeover | JS only | Java JIT -> ROP-less |
| Kernel Exploit? | Optional (bypasses need) | Required | Optional |
| Sandbox Escape | Yes (dual process) | Yes (YouTube app) | Yes (BD-J) |
| Network Sockets | Yes (via compiler process) | No (sandboxed) | Requires kernel |
| Status | Active (FW 13.00 ceiling) | Active (userland only past 12.70) | Patched at 13.00 |

## Key Technical Insights

### Why mast1c0re Cannot Be Fully Patched

The PS2 emulator JIT is a **dynamic recompiler** — it must translate MIPS R5900 (Emotion Engine) and R3000A (I/O Processor) instructions into x86-64 at runtime for acceptable emulation performance. The JIT processes PS2 game data (including savedata) through a code-generation pipeline:

1. PS2 MIPS instructions are decoded
2. Intermediate representation is constructed
3. x86-64 code is emitted into memory
4. The generated code is executed (by the application process) or made executable (by the compiler process)

This pipeline inherently processes untrusted data (savedata is attacker-controlled) and produces executable code. The trust boundary between "game data" and "executable code" cannot be enforced in software without either:
- Disabling the JIT entirely (making emulation unusably slow)
- Moving the trust boundary (validating all PS2 code before JIT compilation, which is equivalent to solving the halting problem)
- Hardware-enforced separation (which would require custom silicon)

### The JIT Privilege Asymmetry

Sony's security investment in the two-process model is substantial but has a fundamental weakness: the bridge protocol between the two processes creates an attack surface that defeats the compartmentalization. The `cmd 0x215` OOB write allows an attacker who controls the application process to corrupt the compiler process's heap — effectively merging the two privilege domains.

This is analogous to a hypervisor escape where a VM guest exploits a VM-exit handling bug to compromise the hypervisor. The bridge is the "VM exit" of the emulator architecture.

### Platform Portability

The emulator binary (`ps2-emu-compiler.self` and `eboot.bin`) is bundled with each PS2 classic game PKG, NOT part of the system firmware. This means:
- Different games may ship with different emulator versions
- Sony must patch each game title individually to fix the emulator
- Older emulator builds persist as long as the game is still downloadable
- The exploit developer only needs to find ONE game with a vulnerable emulator build
- Part B (bridge OOB, VU0 hijack) is portable across games with only offset adjustments

The UltraC0re `check_portable.py` script formalizes this: it scans any `ps2-emu-compiler.self` dump for the `cmd 0x215` signature, hijackable `method70` vcall, and required ROP gadgets, instantly determining exploit viability across titles.

### The 65 MB Mitigation's Insufficiency

The JIT code allocation limit (introduced FW 6.00, 65 MB cap) is a side-channel mitigation, not a root cause fix. It limits what an attacker can do with JIT code (e.g., prevents loading a full game) but does not prevent:
- Compromise of the compiler process (no JIT code needed for the exploit itself)
- Execution of small payloads (shellcode binders, kernel exploit launchers)
- ROP chains that don't require JIT pages

## Open Questions

### Emulator Build Variation
- Q-CRIT-001: Which specific PS2 classic titles ship with vulnerable emulator builds vs. patched builds? Is there a comprehensive matrix?
- Q-CRIT-002: Does the PS5-native PS2 emulator (Method 2, FW >=9.00) use the same `ps2-emu-compiler.self` binary or a significantly different architecture?
- Q-IMP-001: Can the JIT compiler process takeover be detected by the hypervisor through anomalous memory access patterns or syscall frequency?

### JIT Compiler Internals
- Q-IMP-002: What is the complete `instructionMappingCache` data structure? How many entries, what is the cache line format, what is the eviction policy?
- Q-IMP-003: What other bridge doorbell commands exist beyond `cmd 0x215`? Are there additional OOB or logic vulnerabilities in less-examined commands?
- Q-IMP-004: What is the exact VU0 object structure in the compiler's heap? What is the full vtable layout, and what other virtual methods could be hijacked?

### Native PS5 Emulator Differences
- Q-CRIT-003: Does the native PS5 PS2 emulator (Method 2) still use the two-process split (application + compiler)? If not, what is the new architecture?
- Q-CRIT-004: Does the native emulator support savestates through hypervisor integration, and does this create new attack surfaces (hypercall interface, TMR interaction)?
- Q-IMP-005: Is the `cmd 0x215` doorbell OOB present in the native emulator, or was it fixed in the PS5 SDK rebuild?

### Kernel-Level Implications
- Q-IMP-006: Can the JIT compiler process's `cr_caps 0x40` be leveraged for kernel exploit delivery? The compiler can create network sockets — can it also access kernel APIs inaccessible from userland?
- Q-MIN-001: How does `sys_jitshm_create` interact with the hypervisor's NPT and xotext protection? Is JIT shared memory also XOM-protected?

## Attack Surface Expansion

### Games Confirmed as Vectors
- Star Wars: Racer Revenge (CUSA03474 USA, CUSA03492 EU) — Primary (Luac0re)
- Okage: Shadow King — Original (mast1c0re)
- Jak X — UltraC0re vector
- Arcade Spirits: The New Challengers — Ren'Py vector (YARPE/YarP2JB)
- Any game with Artemis Engine Lua interpreter — P2JB delivery
- Any Ren'Py engine game — theoretical YARPE vector

### Future Game Discovery Methodology
1. Scan PS2 classic PKG files for `ps2-emu-compiler.self` binary
2. Run `check_portable.py` against extracted compiler dump
3. Look for signature match: `cmd 0x215` doorbell + `method70` vcall + ROP gadgets
4. If match found, identify the PS2 game's savedata vulnerability (game-specific, Part A)
5. For Ren'Py games: scan for `renpy` module in extracted game data
6. For Lua games: scan for embedded Lua 5.3 interpreter in `eboot.bin`

## References

### Primary Research
- CTurt, "mast1c0re: Hacking the PS4/PS5 through the PS2 Emulator - Part 1 - Escape" (https://cturt.github.io/mast1c0re.html)
- CTurt, "mast1c0re: Hacking the PS4/PS5 through the PS2 Emulator - Part 2 - Compiler Attack" (https://cturt.github.io/mast1c0re-2.html)
- McCaulay, "mast1c0re: Part 3 - Escaping the Emulator" (https://mccaulay.co.uk/mast1c0re-part-3-escaping-the-emulator/)

### Exploit Repositories
- McCaulay/mast1c0re (https://github.com/McCaulay/mast1c0re)
- Gezine/Luac0re (https://github.com/Gezine/Luac0re)
- matem6/UltraC0re (https://github.com/matem6/UltraC0re)
- matem6/YarP2JB (https://github.com/matem6/YarP2JB)
- Helloyunho/yarpe (https://github.com/Helloyunho/yarpe)

### PSDevWiki
- https://www.psdevwiki.com/ps5/Vulnerabilities
- https://www.psdevwiki.com/ps5/Homebrew_Enabler
- https://www.psdevwiki.com/ps5/Exploit_Chains
- https://www.psdevwiki.com/ps5/PS2_Emulation

### Reference Emulator Code (PCSX2)
- PCSX2 recompiler architecture (https://github.com/PCSX2/pcsx2)
- R5900-32 recompiler: ix86-32/iR5900.cpp
- PCSX2 JIT compiler port to amd64 documentation (common/doc/PCSX2%20JIT%20compiler%20port%20to%20amd64t.md)

### Related Research
- [[jailbreak_comprehensive]] — full jailbreak history, exploit chain compatibility, mast1c0re FW range context
- [[cve_timeline]] — CVE reference for V8, WebKit, kernel vulnerabilities
- [[webkit_kernel]] — WebKit and kernel exploit techniques, chain composition
- [[attack_surface]] — entry point ranking, mast1c0re as highest-FW path, JIT output gap
- [[mitigation_assessment]] — XOM, JIT disable, JIT code limit assessments
- [[security_model]] — Auth IDs, PAIDs, JIT process capability model
- [[hardware_attack_surface]] — GDDR6 shared memory, GPU DMA, physical attack surface
