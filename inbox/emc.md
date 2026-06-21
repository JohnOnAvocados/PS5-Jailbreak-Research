# EMC
## Source URL
https://www.psdevwiki.com/ps5/EMC
## System Layer
security
## Summary
The PS5 EMC (Embedded Micro Controller) uses hardware revision CXD90061GG with software versions ranging from 0.7.6 (prototype) to 1.14.3 (FW 9.20). EMC version can be extracted from serial flash at offset 0x4000 (0x7E000 bytes) using blsunpack.
## Key Concepts
- CXD90061GG hardware revision
- EMC v0.7.6: SDK 0.85.070 (prototype/DevKit)
- EMC v1.0.4: FW 1.01-1.14 (TestKit, Retail)
- EMC v1.2.3: FW 2.XX (TestKit)
- EMC v1.4.2: FW 3.00 (Retail)
- EMC v1.6.0: FW 4.00 (TestKit)
- EMC v1.8.2: FW 5.00 (Retail)
- EMC v1.8.3: FW 5.50 (Retail)
- EMC v1.14.3: FW 9.20 (Retail)
- Extracted from serial flash offset 0x4000, length 0x7E000
- SLB2 segment extraction via blsunpack
- C0080001 file contains EMC version
## System Role
Embedded controller firmware for power-on initialization
