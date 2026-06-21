# Partitions
## Source URL
https://www.psdevwiki.com/ps5/Partitions
## System Layer
Storage / Partition Table
## Summary
The PS5 internal SSD is divided into multiple partitions including system, system_ex, preinst, app_temp, system_data, update, swap, and user partitions, along with subpartitions for app_swap, hibernation, and additional swap areas.
## Key Concepts
- 13 main partitions on the SSD
- Partitions use tEXFAT, UFS2, or RAW (SCE_EVENT) filesystems
- System and system_ex have backup copies (system_b, system_ex_b)
- Swap partitions use SCE_EVENT raw format
- Bluray Revocation List (bd_rvlist) is an encrypted partition
- Partition sizes range from 1MiB (bd_rvlist) to 625GiB (user)
## System Role
Defines the storage layout of the PS5 internal SSD, separating system files, executables, user data, swap memory, and update storage into dedicated partitions.
