# Online Connections

**Source:** https://www.psdevwiki.com/ps5/Online_Connections
**System Layer:** System Software
**Summary:** CDN URL structures for PS5 game updates, title update metadata formats (XML/JSON), delta packages, and notable PlayStation Network hostnames.
**Key Concepts:** Title Update XML, Title Update JSON, Delta Package, PlayGo Information PKG, PlayGo Chunk CRC, RNPS hostnames, CDN URL structure, sgst.prod.dl.playstation.net
**System Role:** Defines the online content delivery network architecture for game updates and system services.

## Games and Applications

### Title Update XML

The version.txt file is downloaded from a URL specified in the param.json file of any PS5 application. It contains information about patches available online: the URL to the JSON file, and the URL to the Delta Package PKG if it exists.

Format:
`https://sgst.prod.dl.playstation.net/sgst/prod/00/np/<NP Title ID>/<Hash>-version.xml`

Examples:
- `https://sgst.prod.dl.playstation.net/sgst/prod/00/np/PPSA01280_00/d8ec167a-59da-4e54-8e2c-1161c706516a-version.xml`
- `https://sgst.prod.dl.playstation.net/sgst/prod/00/np/PPSA02306_00/84f670bc-edde-4891-9cdb-ce0fd951705b-version.xml`

### Title Update JSON

Downloaded from the URL specified in the Title Update XML. Contains: URL to Title Update Application PKG, URL to Title Update PlayGo Information PKG, URL to Title Update PlayGo Chunk CRC.

Format:
`https://sgst.prod.dl.playstation.net/sgst/prod/00/<NP Title ID>/app/info/<Revision>/f_<Hash>/<Content ID>.json`

### Delta Package

Format:
`http://gst.prod.dl.playstation.net/gst/prod/00/<NP Title ID>/app/pkg/<Revision>/f_<Hash>/<Content ID>-DP.pkg`

### Title Update Application PKG (Piece 1)

Format:
`http://gst.prod.dl.playstation.net/gst/prod/00/<NP Title ID>/app/pkg/<Revision>/f_<Hash>/<Content ID>.pkg`

### Title Update PlayGo Information PKG (Piece 2)

Format:
`https://sgst.prod.dl.playstation.net/sgst/prod/00/<NP Title ID>/app/info/<Revision>/f_<Hash>/<Content ID>_sc.pkg`

### Title Update PlayGo Chunk CRC

Format:
`https://sgst.prod.dl.playstation.net/sgst/prod/00/<NP Title ID>/app/info/<Revision>/f_<Hash>/<Content ID>.crc`

## Notable Hostnames

### RNPS Hostnames

- chimera-lambda.rnps.dl.playstation.net
- control-center.rnps.dl.playstation.net
- feature-discovery-device-dialog.rnps.dl.playstation.net
- gaming-lounge.rnps.dl.playstation.net
- home-lambda.rnps.dl.playstation.net
- home.rnps.dl.playstation.net
- igc-browse.rnps.dl.playstation.net
- invitation-dialog.rnps.dl.playstation.net
- millenniumfalcon.rnps.dl.playstation.net
- monte-carlo.rnps.dl.playstation.net
- notification-overlay.rnps.dl.playstation.net
- player-selection-dialog.rnps.dl.playstation.net
- ppr-crl.rnps.dl.playstation.net
- profile.rnps.dl.playstation.net
- ps5-multi-bundle-ota.rnps.dl.playstation.net
- uam-fs.rnps.dl.playstation.net

### Unclassified Hostnames

- asm.np.community.playstation.net
- ps5.np.playstation.net
- static-resource.np.community.playstation.net
- uef.np.dl.playstation.net
