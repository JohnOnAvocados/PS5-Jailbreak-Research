# Backup And Restore

## Source URL
https://www.psdevwiki.com/ps5/Backup_And_Restore

## System Layer
System Software

## Summary
The Backup And Restore (BAR) utility allows PS5 users to back up and restore user data (settings, saved data, screenshots, video clips, games, patches) to/from an external USB drive.

## Key Concepts
- Creates `archive.dat` files on USB drive containing backup of built-in storage data
- Not present on systems with FW 1.02 and older that never connected to PSN
- Present at least since FW 2.10 (2020-11-06)
- Uses PFS (PlayStation File System) encryption for backup data
- Related kernel functions: `sceSblBarCreateContext`, `sceSblBarUpdateAad`, `sceSblBarUpdateDecrypt`, `sceSblBarUpdateEncrypt`, `sceSblBarFinishDecrypt`, `sceSblBarFinishEncrypt`

## System Role
The BAR system uses SceSbl encryption functions to create secure encrypted backups. Understanding the archive.dat format and associated crypto operations is relevant for data recovery and forensic analysis.
