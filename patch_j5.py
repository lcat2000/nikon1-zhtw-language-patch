#!/usr/bin/env python3
"""Nikon 1 J5 (Japanese-market body): make the "日本語" language option use Traditional Chinese.

Input : J5_0101_patched_v10.bin from XCQi/Nikon-1-custom-firmware, release j5-patched-v10
        https://github.com/XCQi/Nikon-1-custom-firmware/releases/tag/j5-patched-v10
Output: the same firmware (all XCQi v10 features kept) where the Japanese setting value 0x18
        shows, saves and restores as Traditional Chinese.

Usage : python3 patch_j5.py J5_0101_patched_v10.bin [-o J5_0101_patched_v10_zhTW.bin]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nikonfw import patch, put_crc, sha256, xform, zero_remainder  # noqa: E402

INPUT_SHA256 = "255fe4c3cf4b99cf3b0e5ee86e1bcfd854d693b08872b32ea679c2f10f7f8a15"   # XCQi j5-patched-v10
OUTPUT_SHA256 = "c948ff446af3a9e915f44520ea1eacf44859379f3236a1aa17e9b3bb08f7152c"  # tested on a J5

# Package layout (offsets into the decoded package)
IMAGE = 0x50                 # main image "ax1160_10100.bin"; runtime address = image offset + 0x80000
EMBEDDED_END = 0x175A6E2     # image ends here; its last 2 bytes are the embedded CRC
OUTER_END = 0x175A6E4        # outer CRC over [0, 0x175A6E2)


def pkg(runtime: int) -> int:
    return runtime - 0x80000 + IMAGE


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="J5_0101_patched_v10.bin (XCQi release j5-patched-v10)")
    ap.add_argument("-o", "--output", default="J5_0101_patched_v10_zhTW.bin")
    a = ap.parse_args()

    raw = open(a.input, "rb").read()
    if sha256(raw) != INPUT_SHA256:
        sys.exit("input is not XCQi J5_0101_patched_v10.bin (SHA-256 mismatch)")

    dec = bytearray(xform(raw))
    if not (zero_remainder(dec[IMAGE:EMBEDDED_END]) and zero_remainder(dec[:OUTER_END])):
        sys.exit("CRC check of the input failed")

    # 1) Language screen, Japan-only 2-item list at runtime 0x01599CA0: {u32 text_language, u32 setting_value}
    #    item 2 = (0 Japanese, 0x18) -> (9 Traditional Chinese, 0x18). The saved value stays 0x18.
    patch(dec, pkg(0x01599CA8), bytes.fromhex("0000000018000000"), bytes.fromhex("0900000018000000"),
          "Japan language list, item 2")
    # 2) Boot-time language apply (switch on the language setting): case 0x18 'movs r5,#0' -> 'movs r5,#9'
    patch(dec, pkg(0x0011F2CA), bytes.fromhex("0025"), bytes.fromhex("0925"), "boot language switch, case 0x18")

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
