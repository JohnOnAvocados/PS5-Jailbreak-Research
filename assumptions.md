# Assumptions Register

## Format

Every assumption must be tracked with the following attributes:

| Attribute | Description |
|-----------|-------------|
| ID | Unique identifier: `ASM-NNN` |
| Statement | The claim being assumed |
| Reasoning | Why this assumption is reasonable |
| Confidence | Low / Medium / High |
| Evidence | Supporting facts or sources |
| Counterpoints | Reasons the assumption could be wrong |
| Status | Active / Validated / Invalidated |

---

## Entries

| ID | Statement | Reasoning | Confidence | Evidence | Counterpoints | Status |
|----|-----------|-----------|------------|----------|---------------|--------|
| ASM-001 | PS5 uses AMD-Vi IOMMU similar to desktop Ryzen | PS5 SoC derived from AMD semi-custom design | Medium | AMD-Vi standard across AMD CPUs | Sony may have modified or added custom virtualization features | Active |
| ASM-002 | Hypervisor uses stage-2 paging for memory isolation | Industry standard for Type 1 hypervisors | High | AMD SVM supports NPT; standard practice | Sony could use a simpler isolation mechanism | Active |
| ASM-003 | Boot chain mirrors PS4 architecture with modernized crypto | PS4 boot chain well-documented by Fail0verflow; Sony iterates | High | PS4 boot chain public knowledge | PS5 may have entirely new boot architecture | Active |
| ASM-004 | Kernel is FreeBSD-derived with moderate modification | PS3/PS4 both used FreeBSD-derived kernels; Sony has in-house expertise | High | PS4 kernel analysis is public | Sony may have switched to a different base or custom microkernel | Active |
| ASM-005 | WebKit is the primary initial attack vector below FW 5.50; BD-JB and LUA are co-primary on higher FWs | PS5 browser exists for initial access; BD-JB covers 1.00-7.61; LUA covers 2.00-LATEST; Y2JB covers 4.03-13.40 | High | WebKit patched in FW 5.50; BD-JB extended to 7.61 via path-traversal; LUA works on latest FW | Higher-FW jailbreaks now favor LUA/Y2JB over WebKit; WebKit is only one of multiple entry points | Active |
| ASM-006 | No JTAG accessible on production units | JTAG typically disabled on production consoles | Medium | Industry standard practice | Some consoles leave debug headers populated | Active |
| ASM-007 | PSN access is permanently unavailable on jailbroken consoles | Sony enforces firmware version checks and anti-tamper for PSN | High | All jailbreak guides and sources state this unequivocally | A sufficiently sophisticated spoof could theoretically bypass version check | Active |
| ASM-008 | The hypervisor layer has only been publicly exploited up to FW 6.02 | TheFloW's hypervisor exploit is the only public one; covers up to 6.02 | Medium | TheFloW's public writeup and source code | Unpublished private exploits may exist for higher FWs | Active |
| ASM-009 | BD-JB is not available on digital-edition consoles | BD-JB requires a physical Blu-ray disc drive for the initial access vector | High | Digital consoles lack optical disc hardware | A USB optical drive or software BD emulator could theoretically work | Active |
