# File Structures

**Source:** https://www.psdevwiki.com/ps5/File_Structures
**System Layer:** Filesystem
**Summary:** PS5 root directory listing with permissions and the standard application package directory tree.
**Key Concepts:** Root directory structure, read-only/writable mount points, PKG directory tree, eboot.bin, param.json, trophy files, PlayGo files
**System Role:** Defines the expected layout of the PS5 filesystem root and the internal structure of application packages.

## Root Directory Structure (via FTP payload)

| Directory | Type | Permissions | R/W |
|---|---|---|---|
| adm | folder | drwxr-xr-x 775 | read only |
| app_temp0 | folder | drwxr-xr-x 775 | read only |
| app_temp1 | folder | drwxr-xr-x 775 | read only |
| app_tmp | folder | drwxr-xr-x 775 | read only |
| data | folder | drwxr-xr-x 775 | YES |
| dev | folder | drwxr-xr-x 775 | read only |
| eap_user | folder | drwxr-xr-x 775 | read only |
| eap_vsh | folder | drwxr-xr-x 775 | read only |
| devbin | folder | drwxr-xr-x 775 | read only |
| devlog | folder | drwxr-xr-x 775 | read only |
| hdd | folder | drwxr-xr-x 775 | read only |
| host | folder | drwxr-xr-x 775 | read only |
| host0 | folder | drwxr-xr-x 775 | read only |
| hostapp | folder | drwxr-xr-x 775 | read only |
| mnt | folder | drwxr-xr-x 775 | YES |
| preinst | folder | drwxr-xr-x 775 | YES |
| preinst2 | folder | drwxr-xr-x 775 | read only |
| system | folder | drwxr-xr-x 775 | YES |
| system_data | folder | drwxr-xr-x 775 | YES |
| system_ex | folder | drwxr-xr-x 775 | YES |
| system_tmp | folder | drwxr-xr-x 775 | YES |
| update | folder | drwxr-xr-x 775 | YES |
| usb | folder | drwxr-xr-x 775 | read only |
| user | folder | drwxr-xr-x 775 | YES |

Root ELF files (read only): decid_update.elf, first_img_writer.elf, mini-syscore.elf, safemode.elf, SceSysAvControl.elf, setipaddr.elf

## Application Package Directory Tree

Required structure inside a PS5 application PKG:

- `eboot.bin` - Boot file (required)
- Arbitrary files and directories used by the application
- `sce_modules/` - Directory for system libraries; `*.prx` files (Lib.prx required)
- `sce_sys/` - System directory
  - `about/` - About directory; `right.sprx`
  - `trophy2/` - Trophy Service directory; `npbind.dat`, `trophy00.ucp`
  - `uds/` - UDS Services directory; `npbind.dat`, `uds00.ucp`
- `icon0.dds` / `icon0.png` - Still image icon (with language variants `icon0_*png`)
- `imagedigs.dat`
- `keystone`
- `license.dat`
- `license.info`
- `nptite.dat` - File for verifying the title
- `origin-param.json`
- `origin-relocinfo.dat`
- `param.json` - Param file
- `pfs-version.dat`
- `pic0.dds` / `pic0.png` - Background image
- `pic1.dds` / `pic1.png` - Startup image (with language variants)
- `pic2.dds` / `pic2.png` - Startup foreground image (with language variants)
- `playgo-chunk.dat`
- `playgo-ficm.dat`
- `playgo-hash-table.dat`
- `playgo-scenario.json` - PlayGo scenario information
- `save_data.png` - Save data icon
- `shareoverlayimage.png` - Overlay image for share features
- `snd0.at9` - BGM audio file
- `target-param.json`
- `target-relocinfo.dat`
