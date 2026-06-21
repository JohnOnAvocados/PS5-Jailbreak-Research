# Debugging
## Source URL
https://www.psdevwiki.com/ps5/Debugging
## System Layer
Software / Debug Infrastructure
## Summary
Guide for setting up GDB-based debugging of PS5 payloads using gdbsrv, ps5-payload-sdk, and CLion IDE integration via WSL on Windows. The debug server communicates over port 2159.
## Key Concepts
- Requires jailbroken PS5 with ps5-payload-sdk and gdbsrv
- GDB version 15 tested with gdbsrv.elf
- Debug port is always 2159
- CLion GDB server configuration with persistent session
- Remote file transfer via GDB's `remote put` command
- Uses `monitor reset` for device reset
## System Role
Provides the methodology for remote debugging of homebrew applications on a jailbroken PS5 using industry-standard GDB tooling and IDE integration.
