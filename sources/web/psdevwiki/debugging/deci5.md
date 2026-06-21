# DECI5
## Source URL
https://www.psdevwiki.com/ps5/DECI5
## System Layer
Debugging / Communication Protocol
## Summary
DECI5 is the Debug Communication Interface protocol for communicating with PS5 DevKits and TestKits via the Communication Processor (CP). It defines shared memory nodes, channel types (fix and ring), and a comprehensive set of kernel-level functions for inter-processor debug communication.
## Key Concepts
- Shared Memory Nodes: DECI_SHM_NODE_MAGIC1_CP, MAGIC1_EAP, MAGIC1_MAIN, MAGIC1_MP3, MAGIC1_MP4, MAGIC1_SYCORAX
- Two channel types: fix channels (dedicated) and ring channels (buffered)
- Communication targets: EAP, MAIN, MP3, MP4, SYCORAX
- Functions for channel creation, attachment, buffer management, interrupt handling, and signal processing
- CP (Communication Processor) manages data routing between targets
- Supports mailbox interrupts and signal-based event handling (SIG0-SIG3)
## System Role
Provides the low-level debug communication infrastructure between the host developer workstation and the PS5's various processors (CP, EAP, MAIN, MP3, MP4, Sycorax) for debugging and development purposes.
