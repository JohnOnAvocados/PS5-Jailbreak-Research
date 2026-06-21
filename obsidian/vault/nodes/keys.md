# Keys

## Source
inbox\keys.md

## System Layer
security_model

## Summary
# Keys
## Source URL
https://www.psdevwiki.com/ps5/Keys
## System Layer
security
## Summary
Comprehensive key material for PS5: ROM keys, SceShellCore keys (trophy, PKG metadata RSA-3072), kernel keys, passcode, mount image keys, portability EncDec keys, M.2 keys, RNPS keys, EMC keys, EAP keys (KBL and kernel), Communication Processor keys. Includes full RSA-3072 private key for PKG metadata signing. ## Key Concepts
- PS5 ROM Keys: multiple 256-byte keyseed sets (Key 2-9)
- PKG Metadata RSA-3072: full private key with P, Q, DP, DQ, QP CRT parameters
- SceShellCore Trophy Keys: same as PS4
- Kernel NID default_suffix: same as PS4
- Passcode: 512-byte key from Prospero Publishing Tools
- Portability EncDec Master Keys: 128-byte master key, blob, IV, hash
- Envelope Files: RSA workaround_ctl public verification key and master key ver
- M.2 dummy keys: 01234567890123456789012345678901 (used across FW 1.00-12.20)
- RNPS: AES-128-CBC MAC, RSA-2048/3072
- EMC IPL Cipher Key: AES-128-CBC for PS5 EMC revision c0
- EAP KBL: AES-128-CBC keys for kernel decryption
- EAP Kernel SELF: cipher key and RSA-3072 key pair
- Communication Processor: EMC/EAP/KBL key chain with HMAC-SHA1
- Key 2 (RSA) and Important Keys 3 for UCMD authentication
- Portability keys shared with PS4 for many services
## System Role
Cryptographic key material for PS5 boot chain, DRM, and content verification

## Concepts
keys, key, kernel, ps5, eap, emc, rsa-3072, aes-128-cbc, byte, kbl, master, metadata, pkg, portability, ps4

## Related Notes
- [[../nodes/acm_digital_library]]
- [[../nodes/build_strings]]
- [[../nodes/confidential_computing_consortium]]
- [[../nodes/google_cloud_confidential_computing]]
- [[../nodes/homebrew_enabler]]
- [[../nodes/ieee_xplore]]
- [[../nodes/intel_security]]
- [[../nodes/intel_security_overview]]
- [[../nodes/kernel_overview]]
- [[../nodes/mast1c0re_jit_pipeline]]
- [[../nodes/nist_sp_800_147_bios_protection_guidelines]]
- [[../nodes/nist_sp_800_193_platform_firmware_resiliency]]
- [[../nodes/nvidia_product_security]]
- [[../nodes/secure_boot_from_non_volatile_memory_for_programmable_soc_architectures]]
- [[../nodes/synopsys_firmware_security_blog]]
- [[../nodes/syscall_catalog]]
- [[../nodes/syscalls]]
- [[../nodes/towards_a_secure_operating_system]]
- [[../nodes/uefi_specifications]]
