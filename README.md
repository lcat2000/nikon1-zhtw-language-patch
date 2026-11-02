# Nikon 1 J5 / V2 — Traditional Chinese for Japanese-market bodies

English | [繁體中文](README.zh-TW.md)

Japanese-market Nikon 1 bodies only offer **English** and **日本語** in the language menu, even though the firmware contains every language. These scripts patch the firmware so that the **日本語** option shows, saves and restores **Traditional Chinese (繁體中文)**.

The repository contains **scripts only**. No Nikon or XCQi firmware is included: you download the original file yourself and the script patches it locally.

| Camera | Base firmware (input) | Script | Tested |
|---|---|---|---|
| Nikon 1 **J5** | **XCQi custom firmware `J5_0101_patched_v10.bin`** — [release j5-patched-v10](https://github.com/XCQi/Nikon-1-custom-firmware/releases/tag/j5-patched-v10) | `patch_j5.py` | One Japanese-market J5 |
| Nikon 1 **V2** | **Nikon official firmware C1.22** (`V2__0122.bin`, A 1.22 / B 1.21) — [Nikon Download Center](https://downloadcenter.nikonimglib.com/en/download/fw/267.html) | `patch_v2.py` | One Japanese-market V2 |

- **J5 is a modification of XCQi's patched v10**, not of Nikon's firmware. All v10 features (Wi-Fi/Fn2 button, mechanical-lens support, FT1 improvements, 1-second intervals) are kept. Read [XCQi's J5 guide](https://github.com/XCQi/Nikon-1-custom-firmware/blob/main/cameras/J5/README.md) for those features and their limitations.
- **V2 is a modification of Nikon's original firmware.**

> **Disclaimer.** This is unofficial, experimental firmware modification, unaffiliated with Nikon or XCQi. Flashing modified firmware is at your own risk. Each build has been tested on one camera only. Copyright in the original firmware belongs to Nikon; the J5 base build is XCQi's work.

## What you get

- Language menu still shows two items: **English** and **日本語**.
- Selecting **日本語** switches the whole UI to **Traditional Chinese**, and it stays Traditional Chinese after power-off.
- The item label still reads **日本語** (see [Known limitations](#known-limitations)).
- Japanese is no longer available. To get Japanese back, install the restore file (below).

## Requirements

Python 3.8 or newer. No third-party packages.

## Usage

### J5

1. Download `J5_0101_patched_v10.bin` from [XCQi's release j5-patched-v10](https://github.com/XCQi/Nikon-1-custom-firmware/releases/tag/j5-patched-v10).
2. Run:
   ```sh
   python3 patch_j5.py J5_0101_patched_v10.bin -o J5_0101_patched_v10_zhTW.bin
   ```
   The script checks the input's SHA-256, verifies its CRCs, applies the patch, recomputes the CRCs, re-encodes, and checks that the output matches the tested build.

### V2

1. Download Nikon firmware C1.22 from the [Nikon Download Center](https://downloadcenter.nikonimglib.com/en/download/fw/267.html) and extract `V2__0122.bin` (run `F-V2-V122W.exe` on Windows, or open `F-V2-V122M.dmg` on macOS; the file is in `V2Update/`).
2. Run:
   ```sh
   python3 patch_v2.py V2__0122.bin -o V2__0122_zhTW.bin
   python3 patch_v2.py V2__0122.bin --restore -o V2__0122_stock_restore.bin   # optional: for going back
   ```

### Expected SHA-256

| File | SHA-256 |
|---|---|
| J5 input — XCQi `J5_0101_patched_v10.bin` | `255fe4c3cf4b99cf3b0e5ee86e1bcfd854d693b08872b32ea679c2f10f7f8a15` |
| J5 output | `c948ff446af3a9e915f44520ea1eacf44859379f3236a1aa17e9b3bb08f7152c` |
| V2 input — Nikon `V2__0122.bin` | `a60ade410b8c9702d4193483fc4fd8ca63a5ba5a792c741de2b2ebbd1fb8b060` |
| V2 output | `6e1a072c24d6665b37993f7bd64503dab601d1972947c693fc47fd2ffe34dc33` |
| V2 restore | `937f5feec2e820270c6ad5714c9d54662c28a108bce8e6cd3a28a5b3188528c0` |

## Installing on the camera

Use a fully charged battery. Do not switch off or remove the card during the update.

1. Copy the output file to the **root** of the memory card. Keep only one `.bin` file on the card.
   - **V2:** rename the file to `V2__0122.bin` (two underscores).
   - **J5:** the file name used in testing worked as is; if the update entry does not appear, rename it to `J5_0101.bin`.
2. **Setup menu → Firmware version → Update**, and follow the prompts.
3. After the update, open the **Language** menu and select the second item, **日本語**. The menus switch to Traditional Chinese. (A firmware update can reset the language, so select it again if needed.)
4. Switch the camera off and on to confirm the setting is kept.

The version screen continues to show the old version number. This is expected.

## Going back

- **J5:** install XCQi's original `J5_0101_patched_v10.bin` (Japanese returns, v10 features kept), or XCQi's `J5_0101_stock_restore.bin` (stock functions; see XCQi's guide).
- **V2:** install `V2__0122_stock_restore.bin` built with `--restore`, renamed to `V2__0122.bin`. It is Nikon's official C1.22 with only the version tag raised to `1.2201`, because a body already on C1.22 may refuse to reinstall the identical official file.

If the menus are in a language you cannot read, **Firmware version** and **Language** are in the same positions in the Setup menu as before.

## Known limitations

- **The label still reads 日本語.** The language list draws each name with its own fixed font. On the V2, replacing the label with 繁體中文 displayed four empty boxes because that font has no glyphs for those characters, so the label was left unchanged. The J5 label is likewise unchanged.
- **Japanese is unavailable** while the patch is installed.
- A few UI layout decisions in the firmware are keyed to "the language setting is Japanese"; they now apply while Traditional Chinese is shown. No problems were seen in testing; report anything odd.
- Both builds were tested on a single Japanese-market body each. Behaviour on other bodies, other regions, or other firmware versions is unknown. Do not use these scripts on other models.

## How it works

### Container, encryption and CRCs (J5 and V2)

Nikon 1 firmware packages use Nikon's legacy XOR scheme: after a 32-byte plaintext label, byte *i* is XORed with three 256-byte tables indexed by bits 0–7, 8–15 and 16–23 of *i*. Each module ends with a CRC-16/XMODEM giving a zero remainder, and the package ends with an outer CRC computed the same way. `nikonfw.py` implements this; the tables are from Simeon Pilgrim's Nikon Hacker tools.

### Why not unlock all languages?

On a Japanese-market body the region is stored in the camera and checked by the firmware in more than one place:

1. The language screen shows a 2-item list (English, 日本語) instead of the 32-item international list. Forcing the screen into international mode on the J5 changed the language mapping, but the screen still showed only two rows (Български and Čeština).
2. A language chosen this way is shown immediately, but **is not kept after power-off**: only the English (3) and Japanese (0x18) setting values persist on a Japanese body.

So instead of fighting the region checks, the patch keeps the saved value **0x18**, which the body accepts and saves normally, and changes what 0x18 *means*.

### J5 (base: XCQi patched v10)

Runtime address = image offset + `0x80000`; image starts at package offset `0x50`.

| Change | Runtime address | Package offset | Bytes |
|---|---|---|---|
| Japan 2-item language list, item 2: text language 0 (Japanese) → 9 (Traditional Chinese); setting value stays 0x18 | `0x01599CA8` | `0x1519CF8` | `00 00 00 00 18 00 00 00` → `09 00 00 00 18 00 00 00` |
| Boot-time language apply, `switch(setting)` case 0x18: `movs r5,#0` → `movs r5,#9` | `0x0011F2CA` | `0x9F31A` | `00 25` → `09 25` |
| Embedded CRC | — | `0x175A6E0` | recomputed |

Text-language indices are those of the firmware's string/font tables: 8 = Simplified Chinese, 9 = Traditional Chinese. Neither change overlaps XCQi's v10 edits; the boot function is identical in stock C1.01 and v10.

### V2 (base: Nikon official C1.22)

Module A runtime address = image offset + `0x50020000`; module A starts at package offset `0x70`. Only data is changed, no code.

| Change | Runtime address | Package offset | Bytes |
|---|---|---|---|
| Setting → text-language table, entry 0x18: 0 → 9 | `0x50C59350` | `0xC393C0` | `00` → `09` |
| Second copy of the same table, entry 0x18: 0 → 9 | `0x50CC0FAC` | `0xCA101C` | `00` → `09` |
| Module A version tag `Ver.1.2200` → `Ver.1.2201` (so a body on C1.22 offers the update) | — | `0xC1` | `30` → `31` |
| Module A CRC | — | `0x1423EE0` | recomputed |

Module B (`bx0830_12100`, B 1.21) is not modified. The version-tag approach follows XCQi's finding on the J5 that the update check compares the main image's header tag.

## Credits

- **XCQi** — [Nikon-1-custom-firmware](https://github.com/XCQi/Nikon-1-custom-firmware): the J5 patched v10 firmware this J5 patch is built on, and the container, CRC and update-recognition notes.
- **Simeon Pilgrim / Nikon Hacker** — [nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools): the firmware XOR tables.

## License

The scripts in this repository are released under the [MIT License](LICENSE). This license does not cover Nikon's firmware or XCQi's firmware, which are not distributed here.
