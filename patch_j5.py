#!/usr/bin/env python3
"""Nikon 1 J5 (Japanese-market body): full 32-language menu, including Traditional Chinese.

Input : J5_0101_patched_v11.bin from XCQi/Nikon-1-custom-firmware, release j5-patched-v11
        https://github.com/XCQi/Nikon-1-custom-firmware/releases/tag/j5-patched-v11
        v11 already clears the Japan-only "hidden" flag on the 30 extra language items. This script adds
        the three changes a Japanese-market body still needs: the language screen uses its international
        path, and the language list draws each name with the same fonts as the full UI.
Output: all 32 languages selectable with correct names and kept after power-off; all v11 features kept.

Usage : python3 patch_j5.py J5_0101_patched_v11.bin [-o J5_0101_patched_v11_alllang.bin]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nikonfw import patch, put_crc, sha256, xform, zero_remainder  # noqa: E402

INPUT_SHA256 = "2232768f7fa02d370b5971e1231b8653f48b0644f96f171c0821ee27b8765fdf"   # XCQi j5-patched-v11
OUTPUT_SHA256 = "974a1d37ce577c862021f042c1bd7cd58ebafc53c17c79837f7471bf6653ac95"  # tested on a J5

# Package layout (offsets into the decoded package)
IMAGE = 0x50                 # main image "ax1160_10100.bin"; runtime address = image offset + 0x80000
EMBEDDED_END = 0x175A6E2     # image ends here; its last 2 bytes are the embedded CRC
OUTER_END = 0x175A6E4        # outer CRC over [0, 0x175A6E2)


def pkg(runtime: int) -> int:
    return runtime - 0x80000 + IMAGE


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="J5_0101_patched_v11.bin (XCQi release j5-patched-v11)")
    ap.add_argument("-o", "--output", default="J5_0101_patched_v11_alllang.bin")
    a = ap.parse_args()

    raw = open(a.input, "rb").read()
    if sha256(raw) != INPUT_SHA256:
        sys.exit("input is not XCQi J5_0101_patched_v11.bin (SHA-256 mismatch)")

    dec = bytearray(xform(raw))
    if not (zero_remainder(dec[IMAGE:EMBEDDED_END]) and zero_remainder(dec[:OUTER_END])):
        sys.exit("CRC check of the input failed")

    # XCQi v11 has cleared byte 27 (0x80 = hidden on Japan-region bodies) of the 32 language items' masks
    for k in range(32):
        if dec[pkg(0x0144F37B + 0x20 * k)] != 0:
            sys.exit("unexpected language visibility flags")
    # 1) Language screen: replace both reads of property 1 (sales region, 0 = Japan) with "non-Japan",
    #    'bl 0x3C5554' -> 'movs r0,#1 ; str r0,[r3]', so the screen builds the 32-item international list
    patch(dec, pkg(0x00424B90), bytes.fromhex("a0f7e0fc"), bytes.fromhex("01201860"), "screen init, region read")
    patch(dec, pkg(0x00424E00), bytes.fromhex("a0f7a8fb"), bytes.fromhex("01201860"), "screen key handler, region read")
    # 2) The list draws each name after a temporary language switch whose font getter (veneer 0x2F6094)
    #    returns font set B, whose Arabic/Hindi fonts lack glyphs; point it at the set-A getter 0x5AF198
    patch(dec, pkg(0x002F6098), bytes.fromhex("b1f15a00"), bytes.fromhex("99f15a00"), "temp-switch font getter veneer")

    put_crc(dec, IMAGE, EMBEDDED_END)
    put_crc(dec, 0, OUTER_END)
    assert zero_remainder(dec[IMAGE:EMBEDDED_END]) and zero_remainder(dec[:OUTER_END])

    out = xform(bytes(dec))
    assert len(out) == len(raw) and out[:32] == raw[:32] and xform(out) == bytes(dec)
    with open(a.output, "wb") as f:
        f.write(out)
    h = sha256(out)
    print(f"wrote {a.output}\nSHA-256 {h}")
    print("matches the tested build" if h == OUTPUT_SHA256 else "WARNING: SHA-256 differs from the tested build")


if __name__ == "__main__":
    main()
