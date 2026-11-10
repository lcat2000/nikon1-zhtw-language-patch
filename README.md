# Nikon 1 J5 / V2 — Traditional Chinese for Japanese-market bodies

English | [繁體中文](README.zh-TW.md)

Japanese-market Nikon 1 bodies only offer **English** and **日本語** in the language menu, even though the firmware contains every language. These scripts patch the firmware so that a Japanese-market body can use **Traditional Chinese (繁體中文)**:

- **J5:** the full 32-language menu, with correct names; Traditional Chinese, Japanese and every other language can be selected and are kept after power-off.
- **V2:** the **日本語** option shows, saves and restores Traditional Chinese.

The repository contains **scripts only**. No Nikon or XCQi firmware is included: you download the original file yourself and the script patches it locally.

| Camera | Base firmware (input) | Script | Result | Tested |
|---|---|---|---|---|
| Nikon 1 **J5** | **XCQi custom firmware `J5_0101_patched_v11.bin`** — [release j5-patched-v11](https://github.com/XCQi/Nikon-1-custom-firmware/releases/tag/j5-patched-v11) | `patch_j5.py` | All 32 languages | One Japanese-market J5 |
| Nikon 1 **V2** | **Nikon official firmware C1.22** (`V2__0122.bin`, A 1.22 / B 1.21) — [Nikon Download Center](https://downloadcenter.nikonimglib.com/en/download/fw/267.html) | `patch_v2.py` | 日本語 → Traditional Chinese | One Japanese-market V2 |

- **J5 is a modification of XCQi's patched v11**, not of Nikon's firmware. All v11 features are kept (Wi-Fi/Delete button assignment, MF magnification settings, Fn2, mechanical-lens support, FT1 improvements, 1-second intervals). Read [XCQi's J5 guide](https://github.com/XCQi/Nikon-1-custom-firmware/blob/main/cameras/J5/README.md) for those features and their limitations.
- **V2 is a modification of Nikon's original firmware.**

> **Disclaimer.** This is unofficial, experimental firmware modification, unaffiliated with Nikon or XCQi. Flashing modified firmware is at your own risk. Each build has been tested on one camera only. Copyright in the original firmware belongs to Nikon; the J5 base build is XCQi's work.

## What you get

**J5**

- The language menu lists all 32 languages, each name in its own script (Български … 简体中文, 繁體中文, हिन्दी, 日本語, 한글, فارسی, ภาษาไทย). Arabic and Persian names are right-aligned, as on international bodies.
- Select **繁體中文**; it stays selected after power-off. Japanese remains available.

**V2**

- The language menu still shows two items: **English** and **日本語**.
- Selecting **日本語** switches the whole UI to **Traditional Chinese**, and it stays Traditional Chinese after power-off.
- The item label still reads **日本語** (see [Known limitations](#known-limitations)), and Japanese is no longer available.

## Requirements

Python 3.8 or newer. No third-party packages.

## Usage

### J5

1. Download `J5_0101_patched_v11.bin` from [XCQi's release j5-patched-v11](https://github.com/XCQi/Nikon-1-custom-firmware/releases/tag/j5-patched-v11).
2. Run:
   ```sh
   python3 patch_j5.py J5_0101_patched_v11.bin -o J5_0101_patched_v11_alllang.bin
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
| J5 input — XCQi `J5_0101_patched_v11.bin` | `2232768f7fa02d370b5971e1231b8653f48b0644f96f171c0821ee27b8765fdf` |
| J5 output | `974a1d37ce577c862021f042c1bd7cd58ebafc53c17c79837f7471bf6653ac95` |
| V2 input — Nikon `V2__0122.bin` | `a60ade410b8c9702d4193483fc4fd8ca63a5ba5a792c741de2b2ebbd1fb8b060` |
| V2 output | `6e1a072c24d6665b37993f7bd64503dab601d1972947c693fc47fd2ffe34dc33` |
| V2 restore | `937f5feec2e820270c6ad5714c9d54662c28a108bce8e6cd3a28a5b3188528c0` |

## Installing on the camera

Use a fully charged battery. Do not switch off or remove the card during the update.

1. Copy the output file to the **root** of the memory card. Keep only one `.bin` file on the card.
   - **V2:** rename the file to `V2__0122.bin` (two underscores).
   - **J5:** the file name used in testing worked as is; if the update entry does not appear, rename it to `J5_0101.bin`.
2. **Setup menu → Firmware version → Update**, and follow the prompts.
3. After the update, open the **Language** menu:
   - **J5:** select **繁體中文**.
   - **V2:** select the second item, **日本語**; the menus switch to Traditional Chinese.

   A firmware update can reset the language, so select it again if needed.
4. Switch the camera off and on to confirm the setting is kept.

The version screen continues to show the old version number. This is expected.

## Going back

- **J5:** install XCQi's `J5_0101_stock_restore.bin` to restore stock functions (see XCQi's guide). XCQi's original `J5_0101_patched_v11.bin` can also be installed, but on a Japanese-market body its language screen still prepares only two rows, so the language list may not work correctly; select English or 日本語 before installing it.
- **V2:** install `V2__0122_stock_restore.bin` built with `--restore`, renamed to `V2__0122.bin`. It is Nikon's official C1.22 with only the version tag raised to `1.2201`, because a body already on C1.22 may refuse to reinstall the identical official file.

If the menus are in a language you cannot read, **Firmware version** and **Language** are in the same positions in the Setup menu as before.

## Known limitations

- **J5:** only the language menu and Traditional Chinese were checked on the camera; other languages' menus have not been reviewed.
- **V2: the label still reads 日本語, and Japanese is unavailable.** The language list draws each name with its own fixed font; replacing the label with 繁體中文 displayed four empty boxes, so the label was left unchanged.
- **V2:** a few UI layout decisions in the firmware are keyed to "the language setting is Japanese"; they now apply while Traditional Chinese is shown. No problems were seen in testing.
- Each build was tested on a single Japanese-market body. Behaviour on other bodies, other regions or other firmware versions is unknown. Do not use these scripts on other models.

## How it works

### Container, encryption and CRCs (J5 and V2)

Nikon 1 firmware packages use Nikon's legacy XOR scheme: after a 32-byte plaintext label, byte *i* is XORed with three 256-byte tables indexed by bits 0–7, 8–15 and 16–23 of *i*. Each module ends with a CRC-16/XMODEM giving a zero remainder, and the package ends with an outer CRC computed the same way. `nikonfw.py` implements this; the tables are from Simeon Pilgrim's Nikon Hacker tools.

### What restricts a Japanese-market body

The region is stored in the camera (property 1, 0 = Japan). On the J5 it is used in three places that matter here:

1. **Item masks.** Each of the 32 language items has a 32-byte condition mask; byte 27 = `0x80` hides the item on a Japan-region body. Only English and 日本語 are clear. This controls how many rows the list shows **and** which saved language values survive a power cycle: while the flags are set, choosing another language takes effect immediately but reverts to Japanese after restarting.
2. **Language screen.** The screen reads the region and, for Japan, builds a 2-item list (English, 日本語) from its own table instead of the 32-item international list. Forcing only this part, with the masks still set, produced two rows that showed Български and Čeština, because the masks still allowed only two rows.
3. **Name fonts.** The list draws each name after a temporary switch to that language. That switch takes its fonts from a second, reduced font set whose Arabic and Hindi fonts lack glyphs needed by those names (Arabic and Persian showed as boxes, Hindi lost its न्द conjunct). Switching the UI language itself uses the full font set.

XCQi's v11 clears the masks (1); `patch_j5.py` adds (2) and (3), so the J5 behaves like an international body in the language menu. On the V2, where the equivalent of (1) is still in place, the patch instead keeps the saved value **0x18**, which the body accepts, and changes what 0x18 *means*.

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

Module A runtime address = image offset + `0x50020000`; module A starts at package offset `0x70`. Only data is changed, no code.

| Change | Runtime address | Package offset | Bytes |
|---|---|---|---|
| Setting → text-language table, entry 0x18: 0 (Japanese) → 9 (Traditional Chinese) | `0x50C59350` | `0xC393C0` | `00` → `09` |
| Second copy of the same table, entry 0x18: 0 → 9 | `0x50CC0FAC` | `0xCA101C` | `00` → `09` |
| Module A version tag `Ver.1.2200` → `Ver.1.2201` (so a body on C1.22 offers the update) | — | `0xC1` | `30` → `31` |
| Module A CRC | — | `0x1423EE0` | recomputed |

Text-language indices are those of the firmware's string/font tables: 8 = Simplified Chinese, 9 = Traditional Chinese. Module B (`bx0830_12100`, B 1.21) is not modified. The version-tag approach follows XCQi's finding on the J5 that the update check compares the main image's header tag.

## Credits

- **XCQi** — [Nikon-1-custom-firmware](https://github.com/XCQi/Nikon-1-custom-firmware): the J5 patched v11 firmware this J5 build is based on, its language-item flag change, and the container, CRC and update-recognition notes.
- **Simeon Pilgrim / Nikon Hacker** — [nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools): the firmware XOR tables.

## License

The scripts in this repository are released under the [MIT License](LICENSE). This license does not cover Nikon's firmware or XCQi's firmware, which are not distributed here.
