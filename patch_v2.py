#!/usr/bin/env python3
"""Nikon 1 V2 (Japanese-market body): full 29-language menu, including Traditional Chinese.

Input : V2__0122.bin, Nikon's official firmware C1.22 (A 1.22 / B 1.21)
        https://downloadcenter.nikonimglib.com/en/download/fw/267.html
Output: official firmware with three one-instruction changes in the language screen. Each place that
        tests "region is Japan" now always takes the international path, so the language menu lists all
        29 languages. The module A version tag Ver.1.2200 -> Ver.1.2202 makes the camera offer the update.
        With --restore, only the version tag is changed (Ver.1.2203): stock behaviour, installable after
        the patched build.

Usage : python3 patch_v2.py V2__0122.bin [-o V2__0122_alllang.bin]
        python3 patch_v2.py V2__0122.bin --restore [-o V2__0122_stock_restore.bin]
"""
import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nikonfw import patch, put_crc, sha256, xform, zero_remainder  # noqa: E402

INPUT_SHA256 = "a60ade410b8c9702d4193483fc4fd8ca63a5ba5a792c741de2b2ebbd1fb8b060"  # official V2__0122.bin
OUTPUT_SHA256 = {
    False: "2039ff9f8e8c6fb6d4cee51eaed8801cded7e7b6557bd545b9aa22892b9e2f24",   # all languages, tested on a V2
    True: "a1be10028644099b2121b8e667463e42b99707d4844e27a7d60c8fc95810d1f4",    # stock restore (Ver.1.2203)
}

# Package layout (offsets into the decoded package)
A_START, A_END = 0x70, 0x70 + 0x1423E72          # module A "ax0830_12200.bin"; runtime = image offset + 0x50020000
B_START, B_END = A_END, A_END + 0x19002          # module B "bx0830_12100.bin" (not modified)
OUTER_END = B_END + 2                            # outer CRC over [0, B_END)
VERSION_TAG = 0xB8                               # "Ver.1.2200" in module A's header
TAG = {False: b"Ver.1.2202", True: b"Ver.1.2203"}

# The region setting (menu setting 0x25B, property 0x2C2) reports Japan as item ID 0x800004A3. The language
# screen (setting 0x7C, screen 0x6C) compares the current region item with that constant in three places
# (ARM code). Each "cmp rX, rY" is replaced by "cmp rY, #0", where rY holds the constant just loaded from a
# literal pool, so the comparison is always "not equal" and the international path is taken.
JAPAN_ITEM = 0x800004A3
PATCHES = [
    # runtime,    literal holding JAPAN_ITEM, old bytes,   new bytes,   description
    (0x50343E10, 0x50344030, "010050e1", "000051e3",
     "screen enter: Japan -> list only English and Japanese  (cmp r0,r1 -> cmp r1,#0)"),
    (0x50343E84, 0x50344030, "020051e1", "000052e3",
     "screen parts: Japan -> hide several screen parts        (cmp r1,r2 -> cmp r2,#0)"),
    (0x501978F4, 0x50197B1C, "010050e1", "000051e3",
     "list layout: Japan -> hide all rows but 3 and 26      (cmp r0,r1 -> cmp r1,#0)"),
]


def pkg(runtime: int) -> int:
    return runtime - 0x50020000 + A_START


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="V2__0122.bin (Nikon official C1.22)")
    ap.add_argument("-o", "--output")
    ap.add_argument("--restore", action="store_true", help="build the stock-restore file instead")
    a = ap.parse_args()
    output = a.output or ("V2__0122_stock_restore.bin" if a.restore else "V2__0122_alllang.bin")

    raw = open(a.input, "rb").read()
    if sha256(raw) != INPUT_SHA256:
        sys.exit("input is not the official V2__0122.bin (SHA-256 mismatch)")

    dec = bytearray(xform(raw))
    if not (zero_remainder(dec[A_START:A_END]) and zero_remainder(dec[B_START:B_END])
            and zero_remainder(dec[:OUTER_END])):
        sys.exit("CRC check of the input failed")

    if not a.restore:
        for runtime, literal, old, new, what in PATCHES:
            if struct.unpack_from("<I", dec, pkg(literal))[0] != JAPAN_ITEM:
                sys.exit(f"unexpected literal at 0x{literal:08x}")
            patch(dec, pkg(runtime), bytes.fromhex(old), bytes.fromhex(new), what)
    patch(dec, VERSION_TAG, b"Ver.1.2200", TAG[a.restore], "module A version tag")

    put_crc(dec, A_START, A_END)
    put_crc(dec, 0, OUTER_END)
    assert zero_remainder(dec[A_START:A_END]) and zero_remainder(dec[B_START:B_END]) and zero_remainder(dec[:OUTER_END])

    out = xform(bytes(dec))
    assert len(out) == len(raw) and out[:32] == raw[:32] and xform(out) == bytes(dec)
    with open(output, "wb") as f:
        f.write(out)
    h = sha256(out)
    print(f"wrote {output}\nSHA-256 {h}")
    if h == OUTPUT_SHA256[a.restore]:
        print("matches the tested build" if not a.restore else "matches the expected build")
    else:
        print("WARNING: SHA-256 differs from the expected build")


if __name__ == "__main__":
    main()
