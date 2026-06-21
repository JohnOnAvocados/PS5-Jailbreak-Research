# IDU Mode

**Source:** https://www.psdevwiki.com/ps5/IDU_Mode
**System Layer:** System Software
**Summary:** IDU (Individual Display Unit) mode for kiosk/demo PS5 consoles.
**Key Concepts:** IDU Daemon, IDU Client, IDU Utility, Kiosk mode, Demo mode, Title IDs, sflash/NOR flag, PSN restriction
**System Role:** Specialized system mode for retail demo/kiosk consoles that restricts functionality and manages demo content delivery.

## Overview

IDU (Individual Display Unit) is a mode designed for Kiosk/Demo PS5 consoles meant to demonstrate different game demos, features, etc., usually found in game/electronic stores.

On the PS4, IDU Mode is automatically activated and all content is automatically transferred by inserting a PS4 IDU Disc. This could be the same situation for the PS5, however no PS5 IDU disc has been dumped as of today.

A Kiosk/Demo PS5 console that has used the PS5 IDU disc to install the IDU Utility Normal application has been found. The IDU Utility Normal is an application installed on PS5 internal storage with a size of 3.87 MB.

### Key Characteristics
- Similar to a game hub with quick launch demos, information, icons, and videos (trailers)
- When no bundle is installed, a splash screen with "Content unavailable" is displayed
- IDU mode restricts both application launching and PlayStation Network features
- Activating IDU Mode flashes a value to sflash/NOR that prevents removal even when reinstalling or updating firmware

### Setup/Settings
- Select Country or Region
- Select Language: Multiple languages (same ones PS5 supports)
- Select Region: Multiple regions (same ones PS5 supports)
- Disable Downloads: ON/OFF
- Allow Game Downloads: ON/OFF (controls automatic game demo downloads)
- Allow Video Downloads: ON/OFF (controls automatic trailer downloads)
- Disable Attract Mode Audio: ON/OFF
- Virtual Controller: ON/OFF

### Status Screen
- System Software Version: Current installed firmware
- System Hardware ID: Console's ID (not usually shown in Settings)
- Client Version: Console's IDU client version (similar to PS4's OMSK)
- Device Name: Device name, same as found in Settings
- Installed Bundle: Bundle version, could be found on the disc
- Bundle Name: Bundle name, could be the same name as the disc

## Internal Title IDs

10 different Title IDs referring to IDU have been found inside PS5's firmware:

| Title ID | Internal Name | Information |
|---|---|---|
| NPXS40069 | TITLEID_SIE_IDU_DAEMON | IDU Daemon - activates recognizing and installing retail packages (IDU demos) from server |
| NPXS45085 | TITLEID_SIE_IDU_CLIENT | IDU Client - main application providing GUI to the whole process |
| NPXS45181 | TITLEID_SIE_IDU_UTILITY_FULL | IDU Utility Full Operation switch |
| NPXS45182 | TITLEID_SIE_IDU_UTILITY_NORMAL | IDU Utility Normal Operation switch |
| NPXS21005 | TITLEID_SCE_DAEMON_IDU | IDU Daemon (same ID as PS4, possibly for backwards compatibility) |
| NPXS29005 | TITLEID_SCE_APP_IDU | IDU OMSK Client (same ID as PS4, possibly for backwards compatibility) |
| NPXS29800 | TITLEID_SCE_IDU_UTILITY | IDU Utility, possibly controllable only via disc |
| NPXS29801 | TITLEID_SCE_IDU_UTILITY_REGION | IDU Utility Region switch |
| PPSL07787 | TITLEID_SIE_IDU_CLIENT_FOR_E1 | IDU Client for E1 (purpose unknown) |
| PPSA01759 | TITLEID_SIE_IDU_CLIENT_FOR_PROD | IDU Client for Production (purpose unknown) |
