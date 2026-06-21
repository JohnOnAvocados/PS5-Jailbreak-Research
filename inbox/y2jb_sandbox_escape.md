# Y2JB Sandbox Escape: V8 TheHole Exploitation on PS5 YouTube App

## Overview

The Y2JB (YouTube to Jailbreak) framework exploits CVE-2021-38003 — a V8 JavaScript engine vulnerability where `JSON.stringify()` can leak the internal `TheHole` sentinel value to script code — within the PS5 YouTube TV application. This provides userland JavaScript code execution across the broadest firmware range of any PS5 exploit: FW 2.00-13.40 (confirmed unpatched as of June 2026). When paired with a kernel exploit (P2JB for FW 9.00-12.70, netcontrol for <=12.00, Lapse for <=10.01), Y2JB completes the full userland-to-kernel jailbreak chain.

The exploit's persistence is remarkable: CVE-2021-38003 was patched in Chrome 95.0.4638.69 in October 2021, but remains exploitable on PS5 over 5 years later because the YouTube app is independently updatable through the PlayStation Store and Sony does not treat the V8 engine within YouTube as a critical security boundary. The app uses Google's Cobalt API (version 21+) with an embedded V8 engine, and the app binary is downloaded from PSN rather than included in system firmware — meaning Sony's system firmware patching cadence does not apply.

The Y2JB framework was developed primarily by Gezine, with P2JB-Y2JB porting by matem6 (2026), and has undergone multiple revisions: Y2JB 1.4 introduced kexp shellcode handoff (eliminating USB requirement for ELF loading), Y2JB 1.6 extended firmware range support, and the P2JB-Y2JB port (2.4) added in-sandbox ELF parsing and automated GPU DMA Debug Settings activation.

## YouTube App Architecture on PS5

### Application Model

The PS5 YouTube application is fundamentally different from system-level apps like the WebKit browser:

| Property | YouTube App | System WebKit |
|----------|-------------|---------------|
| Install method | PlayStation Store (PPSA01650) | System firmware |
| Update mechanism | Independent PSN updates | System firmware update |
| Engine | V8 (Chrome) or SpiderMonkey (Mozilla) | JavaScriptCore (WebKit) |
| Cobalt API | Yes (version 21+) | No |
| JIT status | Enabled (V8's TurboFan) | Disabled (PS5 WebKit) |
| DRM requirement | FW >=12.60 requires network license | N/A |
| Persistent storage | Cached HTML on HDD + user/download mount | N/A |

The app uses Google's **Cobalt** framework — a lightweight HTML5/CSS/JS application environment designed for smart TVs and streaming devices. Cobalt bundles its own V8 engine (versions 1.03+ of the app) or SpiderMonkey 45.0.2 JIT-less (version 1.02). This means the JavaScript engine is part of the application binary, not the system firmware.

### Cache-Based Attack Surface

A critical architectural vulnerability in the PS5 YouTube app design:

1. The app loads an **unencrypted HTML file** from HDD cache on startup
2. This HTML file is a cached YouTube page stored at a user-accessible path
3. The cached HTML is loaded from a **user folder** (`download/`) on the internal SSD
4. Downloaded contents are stored in an **image format** that gets mounted when the app is accessed
5. The HTML page is normally displayed for only ~2 seconds on app boot, but this limitation can be removed

This means an attacker can:
- Replace the cached HTML file with an exploit page
- The HTML page executes in the V8 engine context
- No license (.rif) is required to run the app (except FW >=12.60)
- No PSN login is required

### The Backup Restore Procedure

Y2JB exploitation requires a specific system backup restore procedure:

1. The attacker restores a prepared system backup containing the modified YouTube app cache
2. The backup places the exploit HTML/JS payload into the YouTube app's cache directory
3. When YouTube launches, it loads the modified cache as its startup page
4. The exploit JavaScript executes automatically within the V8 engine context
5. The remote JS loader (TCP port 50000) accepts payload delivery

This procedure is required because the YouTube app cache persists across reboots but requires specific setup.

### FW 12.60 DRM Lock

PS5 System Software 12.60 introduced a significant change: most "Media" applications that previously had no DRM now require a **network license** to run. On FW >=12.60, launching YouTube without PSN connectivity throws error CE-100096-6. This change impacts Y2JB usability on these firmware versions but does not patch the underlying V8 vulnerability — it merely gates access to the attack surface behind a network authentication requirement.

## CVE-2021-38003: The V8 TheHole Leak

### Root Cause

CVE-2021-38003 (Chrome Issue 1263462) is a vulnerability in V8's `JSON.stringify()` implementation. The root cause is in `JsonStringifier::SerializeObject()`:

**Normal flow:** When an exception occurs during serialization, `isolate->Throw()` is called which sets `isolate->pending_exception`. Later, the exception handling machinery fetches this value.

**Buggy flow:** In `SerializeElement()` → `Accumulate()` → `Extend()`, when `Accumulate()` detects an overflowed error, it returns `EXCEPTION`. However, `Extend()` does NOT check for overflow and does NOT call `isolate->Throw()`. When `pending_exception` is empty, it contains the sentinel value `TheHole` — a special V8 internal value meaning "no exception pending."

**The leak:** The `TheHole` value is returned to JavaScript code as if it were a normal object. This violates V8's internal assumption that `TheHole` will never be observable from script code.

### Exploitation Mechanism

Once `TheHole` is leaked to JavaScript, it enables memory corruption through V8's `Map` object:

1. **Leak TheHole:** Trigger `JSON.stringify()` on a crafted object that causes the `Extend()` path to return `EXCEPTION` without setting `pending_exception`, leaking `TheHole` to script.

2. **Corrupt Map.size:** Use `Map.prototype.set()` with `TheHole` as a key. V8's `Map` implementation does not expect `TheHole` values and can be tricked into setting `Map.size` to `-1`.

3. **Memory corruption:** A `Map` with `size = -1` causes out-of-bounds reads/writes when iterating or accessing elements. This breaks V8's memory safety assumptions.

4. **Arbitrary read/write:** By corrupting ArrayBuffer length fields or backing store pointers through the Map confusion, the attacker achieves `read8()`/`write8()` primitives within the V8 heap.

5. **Code execution:** From arbitrary read/write, the attacker:
   - Leaks libkernel base address from GOT entries
   - Builds a ROP chain using gadgets from `libkernel_web.sprx` or other loaded libraries
   - Uses Web Worker stack pivot for ROP chain execution
   - Bypasses Clang forward-edge CFI

The full chain: `JSON.stringify()` → `TheHole` leak → `Map.size = -1` → OOB access → arbitrary R/W → ROP → native code execution in the YouTube process.

### Relationship to CVE-2022-1364

CVE-2022-1364 is a related TheHole leak that uses a different root cause: incorrect escape analysis during Error object construction combined with optimization passes. The exploit technique (Map size corruption → memory corruption → RCE) is nearly identical to CVE-2021-38003. Google hardened TheHole handling by adding `CSA_CHECK(this, TaggedNotEqual(key, TheHoleConstant()))` checks to `Map.prototype.delete`, `Set.prototype.delete`, `WeakMap.prototype.delete`, and `WeakSet.prototype.delete` — but these checks apply to Chrome's V8, not necessarily the Cobalt-bundled V8 in PS5's YouTube app.

## Y2JB Framework Architecture

### Components

```
Y2JB Framework (Gezine)
├── System Backup (Y2JB backup restore file)
│   └── Modified YouTube app cache with exploit HTML/JS
├── Exploit JavaScript (y2jb.js)
│   ├── CVE-2021-38003 trigger → TheHole leak
│   ├── Map corruption → arbitrary R/W
│   ├── libkernel base leak
│   ├── ROP chain construction
│   └── Kernel exploit delivery (P2JB/netcontrol/Lapse)
├── Remote JS Loader (TCP port 50000)
│   └── Accepts payload JS after initial exploit
└── Payload Loader
    ├── Y2JB <=1.3: kexp shellcode handoff (USB ELF)
    ├── Y2JB 1.4: kexp-less, ELF from sandbox slots
    └── Y2JB 1.6: Extended FW range support
```

### Exploit Flow

```
1. System backup restored → modified YouTube cache on PS5
2. User launches YouTube app → app loads cached HTML/JS
3. V8 engine executes exploit JavaScript
4. CVE-2021-38003 triggered → TheHole leaked
5. Map/ArrayBuffer corruption → arbitrary R/W in V8 context
6. libkernel base address leaked via GOT read
7. ROP chain constructed (gadgets from libkernel_web.sprx)
8. ROP chain pivots to exploit kernel bug:
   - P2JB (9.00-12.70): cr_ref overflow via kqueueex
   - Netcontrol/POOPS (4.03-12.00): double fdrop UaF
   - Lapse (1.00-10.01): aio_multi_delete double free
9. Kernel R/W → ucred patching → root + SCE capabilities
10. Debug Settings enabled via GPU DMA memory patch
11. ELF loader launched on TCP port 9021
12. Payload sent from PC: any ELF binary
```

### The Remote JS Loader

Y2JB's remote JS loader (TCP port 50000) is a critical architectural component:

- It binds before the jailbreak runs
- It loops forever accepting JavaScript payloads
- It enables automated exploit delivery from a PC
- The PC sends `p2jb_complete.js` (or other exploit JS) to port 50000
- The JS loader injects the payload into the exploit context

## Y2JB Versions and Evolution

### Y2JB 1.0-1.3 (Initial)
- Basic TheHole exploit for YouTube app
- Required USB for ELF delivery
- Supported FW 4.03-10.01
- Paired with Lapse/umtx_shm kernel exploits

### Y2JB 1.4 (kexp Shellcode Handoff)
- **Key innovation:** Eliminated USB requirement
- kexp shellcode handoff delivers ELF loader without physical media
- Supported FW 4.03-12.00
- Paired with netcontrol/POOPS kernel exploits

### Y2JB 1.6 (Extended Range)
- Extended firmware support to higher OFW versions
- Supported FW 4.03-13.40 (userland only above 12.70)
- Kernel exploit support through 12.70
- Framework stability improvements

### P2JB-Y2JB Port 2.4 (matem6, May 2026)
- **ELF loader from Y2JB sandbox without kexp:**
  - Reads `elfldr_1320` directly from Y2JB sandbox slot
  - Uses `elf_parse()` and `elf_run()` functions
  - Replaces previous kexp shellcode-based delivery
- **Automated Debug Settings via GPU DMA:**
  - Direct GPU DMA writes to kernel read-only `.data`
  - Patches `security_flags`, `target_id`, `qa_flags`, `utoken_flags`
  - No separate tool needed for debug menu
- **Known limitation:** Closing YouTube host app causes kernel panic (post-jailbreak kernel-state cleanup not bulletproof)
- **Mitigation:** Apply BD-UN-JB persistent jailbreak before closing
- **Reliability:** `master_rfd > 34` aborts run — noisy host correlates with crashes at stage 0→1 transition

### FW Version Compatibility Matrix

| Y2JB Version | Userland FW | Kernel FW (paired) | Kernel Exploit |
|-------------|-------------|-------------------|----------------|
| 1.0-1.3 | 4.03-10.01 | 1.00-10.01 | Lapse, umtx_shm |
| 1.4 | 4.03-12.00 | 4.03-12.00 | Netcontrol/POOPS |
| 1.6 | 4.03-13.40 | 9.00-12.70 (P2JB) | P2JB, netcontrol |
| P2JB-Y2JB 2.4 | 9.00-12.40 | 9.00-12.40 | P2JB (cr_ref) |

## V8 Engine Version Analysis

The PS5 YouTube app ships with different JavaScript engines across versions:

| App Version | JS Engine | JIT Status | Cobalt Version | Exploit Status |
|-------------|-----------|------------|----------------|----------------|
| 1.02 | SpiderMonkey 45.0.2 | JIT-less | Unknown | Not publicly exploited |
| 1.03+ | Chrome V8 | TurboFan enabled | 21+ | Exploited (Y2JB) |

The transition from SpiderMonkey to V8 was significant for exploitability. V8's TurboFan JIT compiler is enabled in the Cobalt build for PS5, unlike the system WebKit where JIT is disabled. This means V8-specific exploitation techniques (TurboFan type confusion, JIT spraying) are viable.

Key unknowns:
- **Q-CRIT-002:** Exact V8 version bundled in the latest YouTube app for PS5 (determines which V8 CVEs are applicable beyond CVE-2021-38003)
- **Q-CRIT-003:** Whether the Cobalt V8 build includes Chrome's post-2021 TheHole hardening patches (CSA_CHECK additions to Map.prototype.delete, etc.)
- **Q-IMP-001:** Whether CVE-2022-1364 (related TheHole leak via escape analysis) also works if CVE-2021-38003 is patched in a future app update

## Sandbox Properties and Limitations

### What Y2JB Can Do (YouTube App Context)
- Execute arbitrary JavaScript within V8 engine
- Build ROP chains using libkernel gadgets
- Make syscalls (subject to process sandbox restrictions)
- Load ELF binaries from sandbox slots (Y2JB 1.4+)
- Listen on TCP port 50000 (remote JS loader)
- Deliver kernel exploits (P2JB, netcontrol, Lapse)

### What Y2JB Cannot Do (Without Kernel Exploit)
- Create network sockets (AF_INET/AF_INET6 blocked by credential sandbox)
- Access files outside sandbox (requires kernel-level fd_rdir/fd_jdir patching)
- Load kernel modules
- Disable kernel XOM
- Read kernel .text (hypervisor-enforced NPT xotext)
- Survive app close (YouTube process termination kills exploit state)
- Access system Debug Settings (requires GPU DMA kernel patching)

### Sandbox Escape Vectors (Theoretical)

The YouTube app runs as a userland process with the following security constraints:
- **Credential sandbox:** Limited Auth ID, restricted capability set
- **Filesystem sandbox:** fd_rdir/fd_jdir restrict visible filesystem
- **Network sandbox:** AF_INET/AF_INET6 socket creation disabled (ENOSYS)
- **Process sandbox:** No access to other process memory (unless kernel exploit)

Theoretical sandbox escape paths from Y2JB without a kernel exploit:

1. **V8 engine vulnerability in Cobalt context:** A separate V8 bug that provides kernel-level primitives (very unlikely given V8's sandbox)
2. **Cobalt API abuse:** Exploiting the Cobalt framework's system API access to reach kernel interfaces (undocumented)
3. **IPC attack:** Exploiting inter-process communication channels between YouTube and system services (theoretical)
4. **GPU DMA from userland:** If the YouTube process can submit GPU command buffers, GPU DMA bypass might be reachable without kernel exploit (theoretical, depends on IOMMU config)
5. **RPC through compiler process:** Similar to mast1c0re's bridge attack, if YouTube has a privileged companion process (unknown)

## Firmware 12.60 Impact

PS5 System Software 12.60 introduced network license requirements for media applications. This was a DRM change, not a security patch, but it significantly impacts Y2JB:

| Aspect | Pre-12.60 | Post-12.60 |
|--------|-----------|------------|
| App launch | No license required | Requires PSN network license |
| Error on failure | App runs normally | Error CE-100096-6 |
| Offline usability | Works offline | Requires internet connection |
| Exploit impact | Direct app launch | Must bypass license check or have internet |
| Patches CVE-2021-38003? | No | No (DRM change only) |

The license check is a gate, not a fix. An attacker with PSN access or a license bypass can still exploit the V8 vulnerability.

## Comparison with Other Userland Entry Points

| Property | Y2JB | WebKit (JSC) | BD-JB | mast1c0re |
|----------|------|---------------|-------|------------|
| FW Range | 2.00-13.40 | 1.00-5.50 | 1.00-12.70 | 2.00-13.00 |
| Engine | V8 (Cobalt) | JSC (WebKit) | Java JIT | PS2 emu JIT |
| JIT Enabled | Yes | No | Yes | Yes |
| Hardware Req | YouTube app | Web browser | BD drive + disc | Compatible game |
| Digital Console | Yes | Yes | No | Yes |
| Kernel Exploit | Required | Required | Optional | Optional |
| Native Code | ROP only | ROP only | JIT-based | Full native |
| Persistence | None (process) | None | None | None |
| Status | Active | Historical | Active (<=12.70) | Active (<=13.00) |

Y2JB's broadest firmware range and lack of hardware requirements make it the primary userland entry point for the PS5 jailbreak ecosystem. Its limitation is that it provides ROP-only execution (not arbitrary native code) and requires a separate kernel exploit for the full jailbreak chain.

## Open Questions

### V8 and Cobalt Internals
- Q-CRIT-002: Exact V8 version in latest YouTube app for PS5 — determines vulnerability surface
- Q-CRIT-003: Whether Cobalt build includes Chrome's post-2021 TheHole hardening
- Q-IMP-001: Applicability of CVE-2022-1364 if CVE-2021-38003 is eventually patched
- Q-IMP-002: Whether SpiderMonkey-based YouTube app versions (1.02) have separate exploitable bugs

### Sandbox Architecture
- Q-CRIT-004: Complete sandbox capability set for the YouTube process (Auth ID, capability flags, seccomp-bpf equivalent)
- Q-IMP-003: Whether the YouTube process can submit GPU command buffers (libSceGnmDriver access)
- Q-IMP-004: IPC channels between YouTube and system services (SceShellCore, NPXS services)
- Q-IMP-005: Whether Cobalt's system API surface provides privilege escalation paths

### Firmware Boundary
- Q-CRIT-005: Whether Y2JB userland entry works on FW 13.40+ (depends on YouTube app version installed)
- Q-IMP-006: Minimum YouTube app version vulnerable to CVE-2021-38003
- Q-MIN-001: Whether restoring an older YouTube app version is possible on latest FW

## References

### Primary Research
- CVE-2021-38003: Chrome Issue 1263462 (https://crbug.com/1263462)
- STAR Labs, "TheHole New World" (https://starlabs.sg/blog/2022/12-thehole-new-world-how-a-small-leak-will-sink-a-browser-cve-2021-38003/)
- Numen Cyber Labs, "From Leaking TheHole to Chrome Renderer RCE" (https://www.numencyber.com/from-leaking-thehole-to-chrome-renderer-rce-2/)
- Google TAG, "Protecting Android users from 0-Day attacks" (https://blog.google/threat-analysis-group/protecting-android-users-from-0-day-attacks/)

### Exploit Repositories
- Gezine/Y2JB (https://github.com/Gezine/Y2JB)
- matem6/P2JB-Y2JB-Porting (https://github.com/matem6/P2JB-Y2JB-Porting)
- DuskFal1/p2jb (https://github.com/DuskFal1/p2jb)
- RastaFairy/PS5-Toolkit-11.00 (https://github.com/RastaFairy/PS5-Toolkit-11.00)

### PSDevWiki
- https://www.psdevwiki.com/ps5/Vulnerabilities (YouTube app section)
- https://www.psdevwiki.com/ps5/Exploit_Chains
- https://www.psdevwiki.com/ps5/Homebrew_Enabler
- https://www.psdevwiki.com/ps5/System_Software (FW 12.60 DRM changes)

### Related Research Files
- [[jailbreak_comprehensive]] — full exploit history, chain compatibility, Y2JB+P2JB details
- [[cve_timeline]] — V8 CVE catalog, patching timeline
- [[webkit_kernel]] — WebKit and kernel exploit techniques
- [[mast1c0re_jit_pipeline]] — PS2 emulator JIT exploitation (contrasting approach)
- [[attack_surface]] — entry point ranking, userland attack surface enumeration
- [[security_model]] — Auth IDs, PAIDs, process sandbox model
