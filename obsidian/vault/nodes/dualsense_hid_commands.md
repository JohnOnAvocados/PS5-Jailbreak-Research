# DualSense HID Commands

## Source
inbox\dualsense_hid_commands.md

## System Layer
boot_chain

## Summary
# DualSense HID Commands
## Source URL
https://www.psdevwiki.com/ps5/DualSense_HID_Commands
## System Layer
hardware
## Summary
Comprehensive list of HID commands for the DualSense controller, organized by ReportID, DeviceID, and ActionID. ## Key Concepts
- **Get MCU Unique ID**: ReportID=128, DeviceID=1, ActionID=9
- **Read Device Info**: ReportID=128, DeviceID=1, ActionID=12
- **Erase Device Info**: ReportID=128, DeviceID=1, ActionID=13 (DANGER)
- **Reset**: ReportID=128, DeviceID=1, ActionID=1
- **Reboot Secure Boot Loader**: ReportID=128, RebootCmd=1
- **Get Firmware Info**: ReportID=32
- **Get BT Address**: ReportID=129, DeviceID=9, ActionID=2, DataLen=6
- **Set BT Address**: ReportID=128, DeviceID=9, ActionID=1, ReadCmd=2, DataLen=6
- **Set DFU Mode**: ReportID=160, DisableMode=0, EnablePBLMode=1, EnableSBLMode=2, EnableMode=1
- **Flash**: ReportID=240, DownloadCmd=0, DataLen=57, WriteCmd=1
- **NVS Lock**: ReportID=128, DeviceID=3, ActionID=1
- **NVS Unlock**: ReportID=128, DeviceID=3, ActionID=2
- **NVS Lock Status**: ReportID=128, DeviceID=3, ActionID=3 (Results: 0=Unlocked, 1=Locked)
- **Device IDs**: 1=Main MCU, 2=Power, 3=NVS, 5=Touch Panel, 6=Venom FW, 9=BT, 14=BT Patch, 15=Venom, 16=Spider DSP, 17=VDD External
## System Role
HID command interface for reverse engineering and firmware management of the DualSense controller.

## Concepts
reportid, actionid, deviceid, nvs, datalen, device, dualsense, get, hid, info, address, commands, controller, firmware, lock

## Related Notes
- [[../nodes/amd_security]]
- [[../nodes/arm_trusted_firmware]]
- [[../nodes/arxiv]]
- [[../nodes/arxiv_org_eprint_archive]]
- [[../nodes/auth_ids]]
- [[../nodes/backwards_compatibility]]
- [[../nodes/blackhat_archives]]
- [[../nodes/bond]]
- [[../nodes/boot_logo]]
- [[../nodes/build_strings]]
- [[../nodes/homebrew_enabler]]
- [[../nodes/hypervisor_loader]]
- [[../nodes/ieee_xplore_digital_library]]
- [[../nodes/keystone]]
- [[../nodes/magics]]
- [[../nodes/microsoft_firmware_security_research]]
- [[../nodes/ncc_group_research]]
- [[../nodes/nist_sp_800_155]]
- [[../nodes/oem_secure_boot]]
- [[../nodes/scesbl_functions]]
