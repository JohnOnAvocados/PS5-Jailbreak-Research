# CP Box
## Source URL
https://www.psdevwiki.com/ps5/CP_Box
## System Layer
debugging
## Summary
The CP Box (model CPBH-100) is a test/debug device connecting to a PS5 TestKit via USB-C. It has Engineering and Normal modes, provides Ethernet connectivity (DEV LAN), and controls debug mode. Without a CP Box, TestKits boot in Release Mode. With CP Box, Assist Mode is available. Not hot-pluggable; must be connected before power-on.
## Key Concepts
- Model CPBH-100
- Two modes: Engineering Mode and Normal Mode
- Engineering Mode: CP Box powered, USB-C to PS5 only
- Normal Mode: USB-C to portable HDD + Ethernet to network + USB-C to PS5
- DEV LAN: Ethernet port connects to host computer
- CP Box status LEDs: CP INIT, NETWORK INIT, SPEED, LINK/ACT, STATUS
- Without CP Box: TestKit boots in Release Mode
- With CP Box: TestKit can switch to Assist Mode
- Assist Mode persists in memory even when powered off
- PS5 power-on checks for CP Box; shows error if hot-plugged
- CP Box can read PS5 info (serial, mode) even when PS5 is shut down
- Prototype CPB-K01: CXD90046GG main chip, 2x CP systems (recovery + normal)
- VR port (USB-C) activates for PS VR2 after cpupdate ver 2700
## System Role
TestKit debug interface and mode control hardware
