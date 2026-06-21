# Save Data

**Source:** https://www.psdevwiki.com/ps5/Save_Data
**System Layer:** System Software
**Summary:** Save data storage locations, access methods, and PS4 save compatibility on PS5.
**Key Concepts:** savedata_prospero, Title ID, user home directory, sandbox mount points, kernel/usermode access, save mounter tools
**System Role:** Defines how game save data is stored, accessed, and managed within the PS5 system software.

## Location

PS5 save data is stored in `/user/home/<User ID>/savedata_prospero/<Title ID>`.

PS4 save data on PS5 is stored in `/user/home/<User ID>/savedata/<Title ID>`.

When mounted during a game's run, save data can be found at either:
- `/mnt/pfs/savedata_<User ID>_<Title ID>_<savedata name>`
- `/mnt/sandbox/<Title ID>/savedataX`

## Access

- Usermode exploit: access save data of currently mounted PS5 game
- Kernel exploit: access save data of any PS5 game (e.g., via FTP)
- The PS5 SSD is encrypted; no access to save data without running the PS5 System Software
- Save data directories are usually mounted as read-only during gameplay

## Tools

- Playstation-5-Save-Mounter by n0llptr: helps mount and edit save data without running the game

## Notes

Contrary to PS3 and PS4, the PS5 does not allow users to export save data to a USB storage device as a security measure to prevent exploitation via save data manipulation.
