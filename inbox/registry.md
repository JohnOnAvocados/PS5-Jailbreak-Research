# Registry

**Source:** https://www.psdevwiki.com/ps5/Registry
**System Layer:** System Software
**Summary:** Complete listing of PS5 system registry (REGMGR) key entries, organized by functional category with hex identifiers.
**Key Concepts:** REGMGR, registry entries, system configuration, security settings, network configuration, video/audio settings, accessibility, developer environment, QA settings
**System Role:** Centralized system registry database storing all persistent configuration parameters for the PS5 operating system.

## Registry Key Entries

The PS5 system registry (managed by `SCE_REGMGR`) stores configuration data organized by category. Each entry has a unique hex key identifier.

### Registry (0x10xxxxx)

| Key | Name |
|---|---|
| 0x1010000 | SCE_REGMGR_ENT_KEY_REGISTRY_version_ps4 |
| 0x1020000 | SCE_REGMGR_ENT_KEY_REGISTRY_install |
| 0x1030000 | SCE_REGMGR_ENT_KEY_REGISTRY_update |
| 0x1040000 | SCE_REGMGR_ENT_KEY_REGISTRY_not_save |
| 0x1050000 | SCE_REGMGR_ENT_KEY_REGISTRY_recover |
| 0x1060000 | SCE_REGMGR_ENT_KEY_REGISTRY_downgrade_ps4 |
| 0x1070000 | SCE_REGMGR_ENT_KEY_REGISTRY_bootcount |
| 0x1080000 | SCE_REGMGR_ENT_KEY_REGISTRY_lastver |
| 0x1090000 | SCE_REGMGR_ENT_KEY_REGISTRY_ps4_only |
| 0x1100000 | SCE_REGMGR_ENT_KEY_REGISTRY_version |
| 0x1110000 | SCE_REGMGR_ENT_KEY_REGISTRY_downgrade |
| 0x1400000 | SCE_REGMGR_ENT_KEY_REGISTRY_init_flag |

### System (0x20xxxxx)

- System update mode, language, initialization, nickname, dimmer interval, EAP function, voice RC, profile version, button assignment, backup mode, memory test, game recording mode, shell function, pad connection, data transfer, base mode clock up, initialize phase, suppress features, sign-in experience, clear cache, NEO VDDNB VID offset, test button mode/param, fake thermal alerts
- Media codec activations: MPEG2, VC1, HEVC, HEVC (software)
- Platform privacy EU WS1
- Update settings: server URL, EULA version, PSCode, reboot flag, auto download, IDU version, next check, auto update, last version/updversion, config last modified, verify retry count, last release type, auto install, operated user, failed partial update, last system software version, last auto update version, build number, auto update interval, tool update check, beta server URL, check limit, ignore entcheck, strict verchk, config server URL
- Power settings: charge, sign-in, remote, controller off, auto off media/other, auto power down, suspend to RAM, standby start, power history, SP wakeup, session count, shutdown status, charge minutes, verbose report
- Notification invisible items
- System specific: IDU mode, show mode, arcade mode, arcade ID
- Download settings: autodl featured, default HDD, default PS5 storage, BGFT env slot, BGFT debug log/ntf/bwct
- Database: default player, manifest USB
- BGDC: last modified, server URL
- SELF: verification error count, integrity error count
- WCTL server environment
- Auto-mounter: previous HDD ID
- HDD write stats: last report, process time, real time duration, system internal/ext HDD read/write, game internal/ext HDD read/write
- SMR HDD: EAP boot from MOS, MC below threshold count, state change notification
- LIBC: internal memory peak size, shortage count

### Security/Parental (0x38xxxxx)

- Game rating, BD rating, BD age, DVD region, DVD rating, browser, create account, passcode, Morpheus, PAPC all OK, game age limit, game age limit region

### Date/Time (0x5xxxxxx)

- Time zone, date format, time format, summer time, auto set, is summer time, UTC offset, timezone offset, TZ data update, is TZ adjusted, RTC offset, RTC net/dbg/ad, RTC counter adjust, RTC error count, fake geoip, use test CDN, test server slot

### User (0x7xxxxxx)

- Auto login user, max used home user, init user, enable face RC, max used guest, max used shareplay, cumulative user, display account info, new user group

### Accessibility (0x9xxxxxx)

- Invert color, large text, bold text, contrast, shortcut, marquee speed, long press time, text size, color correction enable/type, intensity for protanopia/deuteranopia/tritanopia, reduce motion
- TTS: enable, speed, volume, readout, speech speed, voice type
- Debug: text to speech, large text, bold text, speech tag, use ext TTS dictionary, TTS debug log

### Video Output (0xAxxxxxx)

- Mode, color depth, signal range, screen size, enable CEC, YUV range, display area, HDMI history, screen size (unspecified), HDCP off mode, setting options, reset resolution flag, HDCP version, HDR, HDR confirmed, supersampling mode, HDR max FF TML, HDR max TML, HDR min TML, HDR TV category, HDMI history on storage, HDR metadata, display area type, 4K transfer rate, HDMI device link, system standby, HFR, disable HDCP, force HDR cap, layout, DP HDCP mode, fake monitor mode, VRR, VRR monitor type

### Audio Output (0xBxxxxxx)

- Mode, headphone out, keytone, system BGM, connector type, codec, sound format, config options, speaker update/setting/layout/type, virtual surround HDMI
- Calibration: enable, flag, level left/right, delay left/right
- Measure enable, run options, remote play 3D audio

### Audio Input (0xCxxxxxx)

- Async SRC val0, global mute

### Bluetooth (0x128xxxxx)

- BT enable

### Network (0x14xxxxxx)

- IP: address, netmask, default route, DNS flag, primary/secondary DNS, IP config, DHCP hostname, auth name/key, leased IP/expiration
- Common: device, net flag, conf type, MTU, ether mode, AP auto config, current profile, profile flag, inet flag, DNS6 flag, primary DNS6
- WiFi: SSID, security, WEP key, WPA key, freq band, MTU, IP config, DHCP hostname, auth, IP settings, HTTP proxy
- AOSS: WPA AES/TKIP SSID/key, WEP128/64 SSID/key (2.4GHz and 5GHz)
- HTTP proxy: flag, server, port
- SSL cert ignore, PSN trace, RNPS cert path
- AP mode: flag, SSID, WPA key, channel
- Game AP WPA key, Settings AP WPA key/timestamp
- Debug: IP address, netmask, route, gateway, IP config, DHCP hostname, emulation type, always LAN, default GW, CP DNS addresses, single ethernet, routing, DHCP lease state, packet capture type/enable

### Network Platform (NP) (0x19xxxxxx)

- Patch auto download/install, cache PSSDC, B194260 mode, NP environment, debug, test patch, TPPS proxy, debug upgradable, fake plus, commerce, quick signup password, geo filtering, trophy debug, ignore fake RIF, patch check, video server debug, SF debug, fake rate limit, ignore title ID, NPDRM debug log/notification, SSL check secure/liveitem, plus recheck, regicam URL, manifest URL, per-act sync, geo location, EV fake clock, dailymotion language, disk cache quota, fake display name, deathstar URL, DS family URL, fake version, PBTC debug mode, JWT access token, premium recheck, DRM debug clock offset, web API logging, web API2 fake rate limit

### Camera (0x1Exxxxxx)

- Camera HW info, mute mic, camera2 HW info

### VR Tracker (0x20xxxxxx)

- VR tracker info, telemetry, vision manager interface, green DS4 track

### BD/DVD (0x23xxxxxx)

- BD menu/sound/caption language, NR, display mode, 50Hz output, DRC, BD audio mix, network connect, DVD menu/sound/caption language, sound format, S3D on HMD, flag

### Event (0x2Axxxxxx)

- Auto boot tick

### GLS (Game Live Streaming) (0x32xxxxxx)

- BC mode, social mode, broadcast URL, RPIN, IRC URL/channel/user/password, SF latency, debug info URL, EMB server URL, live quality

### Share (0x37xxxxxx)

- Sound mix, recording prohibit, controller share test, copy share item, recording time, status, controller share range, title check, controller share save

### Share Factory (0x39xxxxxx)

- Direct boot ID

### Browser (0x3Cxxxxxx)

- Enable cookie, enable JS, check signup
- Debug: CA list load mode, verify SSL, DFG JIT enabled, network debug config, check iframe, enable JS log, notification, debug mode

### Remote Play (0x41xxxxxx)

- Enable, AP flag, log enable, user bind mode, ignore prohibition, server version, 4K streaming

### Share Play (0x44xxxxxx)

- Mode, IP direct, resolution, bitrate, framerate, quality graph, ephemeral port, PCL check, store check, age check, GAV check, fake time limit

### Party (0x45xxxxxx)

- Volume down, voice priority, upstream bandwidth, party daemon for booting, running party daemon, pad speaker mix level, voice mix setting headphone/pad speaker, mute in game chat
- Debug: debug message, display debug info, max P2P connections, WAV file dump, grief report debug, P2P/bridge timeout, fake push drop rate, disable privacy guard, debug log level/filter

### Music (0x46xxxxxx)

- Repeat mode, shuffle mode, audio balance, mute mode

### Video Player (0x49xxxxxx)

- 1080/24p, closed caption settings (enable, content specific, char color/opacity/size, font type, char edge/edge color, char bg color/opacity, window color/opacity), video volume

### Video Edit (0x4Bxxxxxx)

- First time activation

### Music Unlimited (0x4Exxxxxx)

- Debug URL

### Project Spark (PRJSP) (0x4Fxxxxxx)

- App installed, enable zeroconf

### PlayGo (0x50xxxxxx)

- Content ID, package URL, scenario ID, DL content ID, auto download, JSON URL, package ex URL

### Morpheus/VR (0x50xxxxxx, 0x58xxxxxx)

- VR2D gyro bias
- Update: server URL, enable update check
- Debug: demo mode, debug mode, social screen, debug text, ex mode chat, show tutorials, HMD auto detect, show safe area, play area warn, ignore separate, debug launch mode, VR capture, notification, show/override mincolor, mincolor RGB

### Play Together (0x55xxxxxx)

- Game played

### Voice Recognition (0x56xxxxxx)

- Client ID, vendor

### System Core (0x5Axxxxxx)

- Shell watch dog

### Companion App (0x64xxxxxx)

- Debug launch mode, debug IP check flag, user bind mode

### Core Dump (0x6Exxxxxx)

- Dump mode, internal mode, always encrypted dump, dump level, video duration/bitrate, system dump level, GPU dump, screenshot, skip error screen
- Uploader: enable, URL, auto upload, display items

### Crash Reporting (0x70xxxxxx)

- Enable report, keep core files, auto sending, operate status, attach video clip, QA auto send, fake optload, fake CFSS, set task title, server env

### System Logger (0x73xxxxxx)

- Platform privacy last modified (BI/tel/kmg), last confirmed, short term ID, last update short term ID
- Debug: config dir, user time, click through, dummy AWS, debug message, delivery mode/URL, priority default dir, skip root CA, autotest case/session ID/type

### System Logger 2 (0x74xxxxxx)

- Aggregator latest EMC error RTC, hOKeNPSID, hOKeNPSID TTL
- Debug: debug message filter titleid/eventname/regex

### PS Cloud (0x76xxxxxx)

- GF version, GKO SDK version, max streaming resolution

### RNPS (0x77xxxxxx)

- Update check, log level

### Developer Environment (0x78xxxxxx)

- Host: devkit name, host internal
- Tool: DL debug flags, region masquerade, boot param, GPIO0, preload check off, webcore module type, user agent type, HP3D lock, fake PFT mode, fake EAA subs mode, RNPS apps launch mode, add CPU expansion, vcodec budget, HDR scopes, GPU war, multi app rule, CPU/GPU frequency, voice out to pad speaker, pad usable PS4 device, VCN budget test, display notice screen forcibly, enable Lotus mic by mic button, pad play/pause emulation, slow SSD mode, WT mode/reset write count, restore when close app, RNPS apps show version, pad disable LED sync, skip adjust display, PlayGo core inspector
- TRC: notify, notify number, transparent
- System DL from host, preserve dmem, use default lib, dev auto assign, razor GPU, reg not save, use dev login, sys PRX preload, PA debug, GPU validate, system load, app suspend test, pad connection, mbus mode, force use cam, host overlay, PSCode masquerade, submit done exception, shutdown debug, shell debug, postmortem, pad auto detect, use host theme, compositor debug, VSH 4K rendering, theme preview, submit done, force GPU idle, QA flag masquerade, VSH GPU control, multi install, game heap trace, expose under 2K, fake NEO 4K mode, friend profile F, IPMI debug flags, login manager debug, sys heap trace, game intmem debug, SCE module debug, piglet RT shader cache, GC halt, ASAN prog/option, skip modal msg, video core debug, DD fake transaction
- Shell Core: boot disable, pathname, load config, host standby request
- Shell UI: debug menu, screenshot, shell crash, display title ID, webdriver, content info, webinspector, webprofile, webproxy, webpreference, fake beta
- Common Dialog: watch dog, crash test, suspend mode
- Keyboard: enable pause, enable print screen
- Voice Recognition: auto start, term of command, transition, recording mode
- Mono Debug: profiling, trace, trace mask, debug option, use new GC, enable full AOT
- BAPM: enable logger, logger mode, file/console/front panel output, cooked log
- APPDB: disable catalog server access
- Activate: auto renewal, prev date, prev result
- PS4 BC: test mode, feature open
- Memory: size, max size
- QA Game: SD fake space/owner, fake finalized, BD copy, AC fake space, SD rebuild, VR fake space, store country, SD format, skip ASM for AC, game recording target/area/force, DD boot block, PKG fake space/size, SD notify, ignore broken status, select M2 SSD, disable M2 fastcopy
- QA Standby: ACTest pattern/interval
- QA Power Test: navigation, shell mediaplay, disc player, PS video
- QA: EAP crash, auto test type, error masquerade, disable BG wave, enable ext HDD, intro video URL, fake ext HDD spec, enable EU WS1, BC QA mode, PS4 title category, PS4 SOC config, pseudolocalization

### Filesystem (0xC0xxxxxx)

- UFS compat PKG, compat PKG mode
- Game PROC: no limit PE SL data

### Modules (0xDExxxxxx)

- RA last modified
- Auto Mounter: M2 format at boot, M2 dirty flag, enable external HDD on CEX, M2 skip mount, M2 skip capability check
- Voice Agent: server URL, enable in-game voice OSK, voice agent feature flag
- HMD2: TV frame
- HMD2 Debug: fake mount, disable play area check, show safe area, fake lens separation distance, auto power on
