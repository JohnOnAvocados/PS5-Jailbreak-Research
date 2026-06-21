# Updatelist.xml

**Source:** https://www.psdevwiki.com/ps5/Updatelist.xml
**System Layer:** Filesystem
**Summary:** XML format used by the PS5 to check for system firmware updates, including version metadata, PUP download URLs, and conditional title requirements.
**Key Concepts:** updatelist.xml, region codes, PUP URL, SDK version, force_update, conditional_requirement, entitlement_list, finished_test_list
**System Role:** Firmware update manifest XML that directs the PS5 to available system software update packages and conditional title requirements.

## Overview

The PS5 checks for updates by sending a GET request to `fus01.ps5.update.playstation.net/update/ps5/official/<random_string>/list/<region>/updatelist.xml` where `<region>` is the console's region code.

The format is the same as PS4's ps4-updatelist.xml and PS Vita's psp2-updatelist.xml. Differences: it is named "updatelist.xml" (not "ps5-updatelist.xml"), and Sony added a random string in the URL after the "official" folder.

## Region Codes

au, br, cn, eu, jp, kr, mx, ru, sa, tw, uk, us

## Structure

### system_pup
Contains firmware PUP information:
- `upd_version`: Firmware version (e.g. "02.20.00.00")
- `sdk_version`: SDK version (e.g. "02.20.00.07-00.00.00.0.0")
- `auto_update_version`: Auto-update version (e.g. "00.00")
- `label`: Release label (e.g. "20.02.02.20.00.07-00.00.00.0.0")
- `update_data`: Contains `update_type` ("full") and `image` with `size` attribute and PUP download URL

### force_update
Contains minimum required system version and optional `conditional_requirement` entries:
- `conditional_requirement`: Per-title minimum firmware requirement; attributes: `type="title"`, `id` (PPSA ID), `sdk_version`, `upd_version`, `auto_update_version`

### entitlement_list
List of beta entitlement IDs for firmware access control.

### finished_test_list
List of completed beta test versions with `sdk_version` and `upd_version`.
