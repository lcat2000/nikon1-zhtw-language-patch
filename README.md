# Nikon 1 J5 / V2 — Traditional Chinese for Japanese-market bodies

English | [繁體中文](README.zh-TW.md)

Japanese-market Nikon 1 bodies only offer **English** and **日本語** in the language menu, even though the firmware contains every language. These scripts patch the firmware so that a Japanese-market body gets the full international language menu, including **Traditional Chinese (繁體中文)**:

- **J5:** all 32 languages.
- **V2:** all 29 languages.

On both cameras every language is listed with its correct name, and Traditional Chinese, Japanese and the other languages can be selected and are kept after power-off.

The repository contains **scripts only**. No Nikon or XCQi firmware is included: you download the original file yourself and the script patches it locally.

| Camera | Base firmware (input) | Script | Result | Tested |
|---|---|---|---|---|
| Nikon 1 **J5** | **XCQi custom firmware `J5_0101_patched_v11.bin`** — [release j5-patched-v11](https://github.com/XCQi/Nikon-1-custom-firmware/releases/tag/j5-patched-v11) | `patch_j5.py` | All 32 languages | One Japanese-market J5 |
| Nikon 1 **V2** | **Nikon official firmware C1.22** (`V2__0122.bin`, A 1.22 / B 1.21) — [Nikon Download Center](https://downloadcenter.nikonimglib.com/en/download/fw/267.html) | `patch_v2.py` | All 29 languages | One Japanese-market V2 |

- **J5 is a modification of XCQi's patched v11**, not of Nikon's firmware. All v11 features are kept (Wi-Fi/Delete button assignment, MF magnification settings, Fn2, mechanical-lens support, FT1 improvements, 1-second intervals). Read [XCQi's J5 guide](https://github.com/XCQi/Nikon-1-custom-firmware/blob/main/cameras/J5/README.md) for those features and their limitations.
- **V2 is a modification of Nikon's original firmware.**

> **Disclaimer.** This is unofficial, experimental firmware modification, unaffiliated with Nikon or XCQi. Flashing modified firmware is at your own risk. Each build has been tested on one camera only. Copyright in the original firmware belongs to Nikon; the J5 base build is XCQi's work.

## What you get

- **J5:** the language menu lists all 32 languages, each name in its own script (Български … 简体中文, 繁體中文, हिन्दी, 日本語, 한글, فارسی, ภาษาไทย). Arabic and Persian names are right-aligned, as on international bodies.
- **V2:** the language menu lists all 29 languages and scrolls like an international body (Čeština … عربي, 简体中文, 繁體中文, हिन्दी, 日本語, 한글, ภาษาไทย).
- On both: select **繁體中文**; it stays selected after power-off. Japanese remains available.

## Requirements

Python 3.8 or newer. No third-party packages.

## Usage

### J5

1. Download `J5_0101_patched_v11.bin` from [XCQi's release j5-patched-v11](https://github.com/XCQi/Nikon-1-custom-firmware/releases/tag/j5-patched-v11).
2. Run:
   ```sh
   python3 patch_j5.py J5_0101_patched_v11.bin -o J5_0101_patched_v11_alllang.bin
   ```

### V2

1. Download Nikon firmware C1.22 from the [Nikon Download Center](https://downloadcenter.nikonimglib.com/en/download/fw/267.html) and extract `V2__0122.bin` (run `F-V2-V122W.exe` on Windows, or open `F-V2-V122M.dmg` on macOS; the file is in `V2Update/`).
2. Run:
   ```sh
   python3 patch_v2.py V2__0122.bin -o V2__0122_alllang.bin
   python3 patch_v2.py V2__0122.bin --restore -o V2__0122_stock_restore.bin   # optional: for going back
   ```

Each script checks the input's SHA-256, verifies its CRCs, applies the patch, recomputes the CRCs, re-encodes, and checks that the output matches the expected build.

### Expected SHA-256

| File | SHA-256 |
|---|---|
| J5 input — XCQi `J5_0101_patched_v11.bin` | `2232768f7fa02d370b5971e1231b8653f48b0644f96f171c0821ee27b8765fdf` |
| J5 output | `974a1d37ce577c862021f042c1bd7cd58ebafc53c17c79837f7471bf6653ac95` |
| V2 input — Nikon `V2__0122.bin` | `a60ade410b8c9702d4193483fc4fd8ca63a5ba5a792c741de2b2ebbd1fb8b060` |
| V2 output | `2039ff9f8e8c6fb6d4cee51eaed8801cded7e7b6557bd545b9aa22892b9e2f24` |
| V2 restore | `a1be10028644099b2121b8e667463e42b99707d4844e27a7d60c8fc95810d1f4` |

## Installing on the camera

Use a fully charged battery. Do not switch off or remove the card during the update.

1. Copy the output file to the **root** of the memory card. Keep only one `.bin` file on the card.
   - **V2:** rename the file to `V2__0122.bin` (two underscores).
   - **J5:** the file name used in testing worked as is; if the update entry does not appear, rename it to `J5_0101.bin`.
2. **Setup menu → Firmware version → Update**, and follow the prompts.
3. After the update, open the **Language** menu and select **繁體中文**. A firmware update can reset the language, so select it again if needed.
4. Switch the camera off and on to confirm the setting is kept.

The version screen continues to show the old version number. This is expected.

**V2, upgrading from the earlier build of this repository** (the one where 日本語 showed Traditional Chinese): install the new file directly; this was tested. The saved value that showed Traditional Chinese means Japanese again, so the menus may come up in Japanese until you select 繁體中文.

## Going back

- **J5:** install XCQi's `J5_0101_stock_restore.bin` to restore stock functions (see XCQi's guide). XCQi's original `J5_0101_patched_v11.bin` can also be installed, but on a Japanese-market body its language screen still prepares only two rows, so the language list may not work correctly; select English or 日本語 before installing it.
- **V2:** install `V2__0122_stock_restore.bin` built with `--restore`, renamed to `V2__0122.bin`. It is Nikon's official C1.22 with only the version tag raised to `1.2203`, above the patched build's `1.2202`, in case the camera only offers an update for a higher tag. The restore file has not been installed on a camera.

If the menus are in a language you cannot read, **Firmware version** and **Language** are in the same positions in the Setup menu as before.

## Known limitations

- Only the language menu and Traditional Chinese were checked on the cameras; other languages' menus have not been reviewed.
- Each build was tested on a single Japanese-market body. Behaviour on other bodies, other regions or other firmware versions is unknown. Do not use these scripts on other models.

## How it works

### Container, encryption and CRCs (J5 and V2)

Nikon 1 firmware packages use Nikon's legacy XOR scheme: after a 32-byte plaintext label, byte *i* is XORed with three 256-byte tables indexed by bits 0–7, 8–15 and 16–23 of *i*. Each module ends with a CRC-16/XMODEM giving a zero remainder, and the package ends with an outer CRC computed the same way. `nikonfw.py` implements this; the tables are from Simeon Pilgrim's Nikon Hacker tools.

The camera decides whether to offer an update from the version tag in the main image's header (XCQi's finding on the J5). The V2 builds therefore raise the tag of the official C1.22 file; on the test V2, C1.22 → `1.2201` (earlier build) → `1.2202` was accepted.

### What restricts a Japanese-market body

The region is stored in the camera. The two cameras use it differently.

**J5** (region = property 1, 0 = Japan) — three places:

1. **Item masks.** Each of the 32 language items has a 32-byte condition mask; byte 27 = `0x80` hides the item on a Japan-region body. Only English and 日本語 are clear. This controls how many rows the list shows **and** which saved language values survive a power cycle: while the flags are set, choosing another language takes effect immediately but reverts to Japanese after restarting.
2. **Language screen.** The screen reads the region and, for Japan, builds a 2-item list (English, 日本語) from its own table instead of the 32-item international list. Forcing only this part, with the masks still set, produced two rows that showed Български and Čeština, because the masks still allowed only two rows.
3. **Name fonts.** The list draws each name after a temporary switch to that language. That switch takes its fonts from a second, reduced font set whose Arabic and Hindi fonts lack glyphs needed by those names (Arabic and Persian showed as boxes, Hindi lost its न्द conjunct). Switching the UI language itself uses the full font set.

XCQi's v11 clears the masks (1); `patch_j5.py` adds (2) and (3).

**V2** (region = menu setting `0x25B`, stored in property `0x2C2`; Japan = item ID `0x800004A3`). The V2's menu items also have condition masks (35 conditions per item), but the language items carry none. The restriction is in the code of the language screen (setting `0x7C`, screen `0x6C`), which compares the current region with Japan in three places:

1. **On entering the screen**, it replaces the 29-item list with two items: English (`0x080002EB`) and 日本語 (`0x08000302`).
2. **A second handler of the screen** hides several screen parts.
3. **The list layout** hides every row except positions 3 (English) and 26 (日本語) and positions those two rows.

`patch_v2.py` changes each comparison so it never matches, and the screen behaves as on an international body. Unlike the J5, all language names displayed correctly without a font change.

### J5 (base: XCQi patched v11)

Runtime address = image offset + `0x80000`; image starts at package offset `0x50`.

| Change | Runtime address | Package offset | Bytes |
|---|---|---|---|
| (XCQi v11) Japan-hide flag cleared on 30 language items, byte 27 of each 32-byte mask | `0x0144F37B` + `0x20`·k | `0x13CF3CB` + `0x20`·k | `80` → `00` (already in v11) |
| Language screen init: region read `bl 0x3C5554` → `movs r0,#1; str r0,[r3]` | `0x00424B90` | `0x3A4BE0` | `a0 f7 e0 fc` → `01 20 18 60` |
| Language screen key handler: same replacement | `0x00424E00` | `0x3A4E50` | `a0 f7 a8 fb` → `01 20 18 60` |
| Temporary-switch font getter veneer: set B `0x5AF1B0` → set A `0x5AF198` | `0x002F6098` | `0x2760E8` | `b1 f1 5a 00` → `99 f1 5a 00` |
| Embedded CRC | — | `0x175A6E0` | recomputed |

The veneer at `0x2F6094` has no other caller than the temporary language switch (three calls), so the font change affects only the language list. Both font sets have the same metrics.

### V2 (base: Nikon official C1.22)

Module A runtime address = image offset + `0x50020000`; module A starts at package offset `0x70`. The three changes are in ARM code. In each, the register compared with the current region already holds the Japan item ID `0x800004A3`, loaded from a literal pool just before; comparing that register with 0 always gives "not equal", so the international path is taken.

| Change | Runtime address | Package offset | Bytes |
|---|---|---|---|
| Screen enter: `cmp r0,r1` → `cmp r1,#0` | `0x50343E10` | `0x323E80` | `01 00 50 e1` → `00 00 51 e3` |
| Screen parts: `cmp r1,r2` → `cmp r2,#0` | `0x50343E84` | `0x323EF4` | `02 00 51 e1` → `00 00 52 e3` |
| List layout: `cmp r0,r1` → `cmp r1,#0` | `0x501978F4` | `0x177964` | `01 00 50 e1` → `00 00 51 e3` |
| Module A version tag `Ver.1.2200` → `Ver.1.2202` (restore file: `Ver.1.2203`) | — | `0xC1` | `30` → `32` (`33`) |
| Module A CRC | — | `0x1423EE0` | recomputed |

Module B (`bx0830_12100`, B 1.21) is not modified.

## Credits

- **XCQi** — [Nikon-1-custom-firmware](https://github.com/XCQi/Nikon-1-custom-firmware): the J5 patched v11 firmware this J5 build is based on, its language-item flag change, and the container, CRC and update-recognition notes.
- **Simeon Pilgrim / Nikon Hacker** — [nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools): the firmware XOR tables.

## License

The scripts in this repository are released under the [MIT License](LICENSE). This license does not cover Nikon's firmware or XCQi's firmware, which are not distributed here.
