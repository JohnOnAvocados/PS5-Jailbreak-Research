# Filesystem

**Source:** https://www.psdevwiki.com/ps5/Filesystem
**System Layer:** Filesystem
**Summary:** PS5 filesystem mount point tables detailing block device mappings, filesystem types, and mount flags for system, user, data, and sandbox partitions.
**Key Concepts:** exfatfs, ufs, bfs, nullfs, tmpfs, devfs, udf2, mount flags, sandbox mounts, NPXS title sandboxes
**System Role:** Defines the complete mount hierarchy for the PS5 operating system across all storage partitions and sandbox environments.

## Main Directory Filesystem

| Point | Directory | Filesystem | Flags |
|---|---|---|---|
| md0 | / | exfatfs | 0x5001 |
| devfs | /dev | devfs | 0x0 |
| tmpfs | /system_tmp | tmpfs | 0x1000 |
| dev/ssd0.system | /system | exfatfs | 0x1041 |
| dev/ssd0.system_ex | /system_ex | exfatfs | 0x1041 |
| dev/ssd0.system_data | /system_data | ufs | 0x10201000 |
| dev/ssd0.user | /user | bfs | 0x1000 |
| dev/ssd0.update | /update | exfatfs | 0x1040 |
| tmpfs | /mnt | tmpfs | 0x1000 |
| dev/ssd0.preinst | /preinst | exfatfs | 0x1041 |
| user/data | /data | nullfs | 0x1000 |

## Dev/Mnt Directory Filesystem

| Point | Directory | Filesystem | Flags |
|---|---|---|---|
| dev/cd0 | /mnt/disc | udf2 | 0x1001 |
| dev/lvd0 | /mnt/rnps | ufs | 0x10201000 |
| dev/da1s1 | /mnt/usb0 | exfatfs | 0x1000 |
| dev/md2 | /system_data/eap/rodata | ufs | 0x10201000 |

## Sandbox Mounts

Multiple NPXS title sandboxes (NPXS40087, NPXS40100, NPXS40142, NPXS40109, NPXS40039, NPXS40102, NPXS40153, NPXS40112, NPXS40101, NPXS40094, NPXS40028, NPXS40000, NPXS40085, NPXS40091, NPXS40173, NPXS40140, NPXS40142) mount various combinations of:
- nullfs binds from app0, disc, usb0, system_tmp, rnps, download0
- devfs entries per sandbox
- System, system_ex, system_data, preinst, user resources as read-only nullfs binds

## Other Mounts

Notable additional mount points include:
- user/devlog/app and user/devlog/system → /devlog (nullfs)
- system_ex/app/NPXS* → sandbox app0
- system_data/eap/rodata via md2 (ufs)
- Various system, system_ex, preinst, user subdirectories nullfs-bound into sandbox paths
- System_data/priv, system_data/common, user/common, user/temp directories shared into sandboxes
