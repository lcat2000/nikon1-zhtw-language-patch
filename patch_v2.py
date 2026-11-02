#!/usr/bin/env python3
"""Nikon 1 V2 (Japanese-market body): make the "日本語" language option use Traditional Chinese.

Input : V2__0122.bin, Nikon's official firmware C1.22 (A 1.22 / B 1.21)
        https://downloadcenter.nikonimglib.com/en/download/fw/267.html
Output: official firmware with only these data changes (no code is modified):
          * both language-value -> text-language tables map 0x18 (Japanese) to Traditional Chinese
          * module A version tag Ver.1.2200 -> Ver.1.2201, so a body already on C1.22 accepts it
        With --restore, only the version tag is changed (stock behaviour, re-installable on C1.22).

Usage : python3 patch_v2.py V2__0122.bin [-o V2__0122_zhTW.bin]
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
    False: "6e1a072c24d6665b37993f7bd64503dab601d1972947c693fc47fd2ffe34dc33",   # zhTW, tested on a V2
    True: "937f5feec2e820270c6ad5714c9d54662c28a108bce8e6cd3a28a5b3188528c0",    # stock restore
}

# Package layout (offsets into the decoded package)
A_START, A_END = 0x70, 0x70 + 0x1423E72          # module A "ax0830_12200.bin"; runtime = image offset + 0x50020000
B_START, B_END = A_END, A_END + 0x19002          # module B "bx0830_12100.bin" (not modified)
OUTER_END = B_END + 2                            # outer CRC over [0, B_END)
VERSION_TAG = 0xB8                               # "Ver.1.2200" in module A's header

# setting value -> text language, indexed by the language setting (0x18 = Japanese)
LANG_TABLE = [19, 17, 2, 1, 4, 22, 3, 13, 5, 21, 7, 18, 15, 26, 14, 11, 23, 16, 6, 24, 20, 28, 9, 8, 0, 10, 12, 27, 25]
TABLES = (0x50C592F0, 0x50CC0F4C)                # runtime addresses of the two copies
JAPANESE, TRAD_CHINESE = 0x18, 9


def pkg(runtime: int) -> int:
    return runtime - 0x50020000 + A_START


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="V2__0122.bin (Nikon official C1.22)")
    ap.add_argument("-o", "--output")
    ap.add_argument("--restore", action="store_true", help="build the stock-restore file instead")
    a = ap.parse_args()
    output = a.output or ("V2__0122_stock_restore.bin" if a.restore else "V2__0122_zhTW.bin")

    raw = open(a.input, "rb").read()
    if sha256(raw) != INPUT_SHA256:
        sys.exit("input is not the official V2__0122.bin (SHA-256 mismatch)")

    dec = bytearray(xform(raw))
    if not (zero_remainder(dec[A_START:A_END]) and zero_remainder(dec[B_START:B_END])
            and zero_remainder(dec[:OUTER_END])):
        sys.exit("CRC check of the input failed")

    if not a.restore:
        for t in TABLES:
            p = pkg(t)
            if list(struct.unpack("<29I", dec[p:p + 29 * 4])) != LANG_TABLE:
                sys.exit(f"unexpected language table at 0x{t:08x}")
            patch(dec, p + JAPANESE * 4, struct.pack("<I", 0), struct.pack("<I", TRAD_CHINESE),
                  f"language table 0x{t:08x}[0x18]")
    patch(dec, VERSION_TAG, b"Ver.1.2200", b"Ver.1.2201", "module A version tag")

    put_crc(dec, A_START, A_END)
    put_crc(dec, 0, OUTER_END)
    assert zero_remainder(dec[A_START:A_END]) and zero_remainder(dec[B_START:B_END]) and zero_remainder(dec[:OUTER_END])

    out = xform(bytes(dec))
    assert len(out) == len(raw) and out[:32] == raw[:32] and xform(out) == bytes(dec)
    with open(output, "wb") as f:
        f.write(out)
    h = sha256(out)
    print(f"wrote {output}\nSHA-256 {h}")
    print("matches the tested build" if h == OUTPUT_SHA256[a.restore] else "WARNING: SHA-256 differs from the tested build")


if __name__ == "__main__":
    main()
