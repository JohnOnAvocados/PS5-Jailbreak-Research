# Trophy00.ucp

**Source:** https://www.psdevwiki.com/ps5/Trophy00.ucp
**System Layer:** Filesystem
**Summary:** Binary container format for PS5 trophies (NpTrophy V2), replacing the TRP format from PS4 with JSON-based trophy definitions.
**Key Concepts:** NpTrophy V2, UCP magic, big-endian format, Table of Contents, HMAC, PNG assets, JSON trophy data
**System Role:** Trophy pack file format storing achievement data, icons, and metadata for PS5 and PC titles.

## Overview

PS5 and PC ports use NpTrophy V2 with a new trophy pack file format (.ucp). Previously PS4/PS3/Vita used TRP containing PNGs and XML. The new format still contains PNGs but uses JSON to define trophies. The entire format is big-endian, even on PC.

The uds00.ucp file uses the exact same format.

## Data Structure

| Offset | Type | Description |
|---|---|---|
| 0x00 | uint32 | Magic Number (0xB228C60A) |
| 0x04 | uint32 | Version (1) |
| 0x08 | uint64 | Total file size |
| 0x10 | uint32 | Number of Files |
| 0x14 | uint32 | Location of Table of Contents |
| 0x18 | uint64 | Unknown |
| 0x20 | char[0x10] | HMAC? |

## Table of Contents

The TOC is at 0x40 most of the time but can be anywhere.

| Offset | Type | Description |
|---|---|---|
| 0x40 | char[0x20] | Reserved (only once at the beginning) |
| 0x60 | char[0x20] | File Name |
| 0x80 | uint64 | File Offset (Absolute) |
| 0x88 | uint64 | File Size |
| 0x90 | char[0x10] | Reserved |
