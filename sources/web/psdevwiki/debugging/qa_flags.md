# QA Flags
## Source URL
https://www.psdevwiki.com/ps5/QA_Flags
## System Layer
Security / QA Token
## Summary
QA Flags are SELF-format tokens containing QA authorization information. They use a structured SELF format with header, segment, additional info, metadata, and encrypted body containing OpenPSID and QA flags.
## Key Concepts
- QA Token SELF structure: Header (0xC0 bytes) + Metadata (0x1E0 bytes) + Body
- Header Magic: 54 14 F5 EE
- Category: 06 for QA Token SELF
- Body encrypted with AES-CBC-CTS, signed with HMAC-SHA256 and RSA 3096
- Body fields: OpenPSID (0x10), QA FLAGS (0x10), padding, SHA256HMAC
- Known QAF name: QAF_SYS_DEV_I
- Validity period: 10 Oct 2019 - 4 Oct 2021 (725 days)
- Token size: 0x60 bytes
## System Role
Defines the format and cryptographic structure of QA authorization tokens that grant elevated privileges for development and testing on PS5 consoles.
