"""Shared helpers for Nikon 1 firmware packages (J5, V2).

Package format, as used by Nikon's legacy firmware scheme:
  * The first 32 bytes are a plaintext label (spaces).
  * Every later byte i is XORed with  T0[i & 0xFF] ^ T1[(i >> 8) & 0xFF] ^ T2[(i >> 16) & 0xFF].
    The same transform decodes and re-encodes.
  * Each module ends with a big-endian CRC-16/XMODEM (binascii.crc_hqx(data, 0)) so the
    whole module has a zero remainder; the package then ends with an outer CRC over
    everything before it, computed the same way.

The three 256-byte XOR tables were published by Simeon Pilgrim / the Nikon Hacker
project (Firmware1.cs in https://github.com/simeonpilgrim/nikon-firmware-tools).
"""
import binascii
import hashlib

T0 = bytes.fromhex(
    "bb8512a7d7111530535c72ca619fa3ac"
    "2dc7059cdf2237f5936f246b98b20d44"
    "8bcd3d3365f3f75289b73426798fc184"
    "87073ae2e00ca1f0a0774a7eff25b69d"
    "4f36f4c8a9a8700099c3322a1fda9b64"
    "eaba63c223afbf2c39169e6ddc310219"
    "2f47aee35b740f71d4fe50d63ed018a4"
    "e829805a7de545e1626ce6b59a78a57b"
    "038127b006f1e78ed2d91e3f5e95edfa"
    "2090eefddd4edb6a827a561b8a1c0957"
    "6e2be404ab67def61d2e46868ccbb814"
    "6610d1f28d0854b442f849d575be7668"
    "517cef96ce0ee9eb412859ecb1139140"
    "0acf5d01c93bc0aa88c592384b5fd3a6"
    "69a23558fbc60b177f213c83bccc4d97"
    "c46048f9bd73b9b31a55d84cadfc4394"
)
T1 = bytes.fromhex(
    "b60a9cbf545c808ffe1ef93a8cea782a"
    "01f7563839e572e6440c41738234cdc2"
    "1437c7bdd3f329aa8dc5e4eb9de9fbf1"
    "1f7d079353954a24054dce7e7f2822c8"
    "6e4055e365c33b0fe2dcedbc1b61ef0b"
    "92991d648e7ce160afa685ec4cb86923"
    "dbbaccc6ee0d2743f81132fc75d1a120"
    "7163882bd92e89683cf4df33fdac6cb3"
    "19c1105717fa79cf13f2863551b1d5cb"
    "a3ae94035fd86b317481bb3d1516f6b5"
    "4bf5776f49a8a7caad029a5e59259862"
    "1ab79f2fa0766db447b0a906da2d5bd7"
    "8a667ba5ff6ab9e0be9e2c36f0d2d097"
    "263ea2085d584f91708bc0900e005ae7"
    "4587b2831cc452d496de21047a3f1230"
    "6750094842abd6dd9ba418e8c94e4684"
)
T2 = bytes.fromhex(
    "bfb7800548daf077a093e50c0769e72f"
    "f40d6fd42c3b1e4371f51aa857314b6d"
    "358ec892ed0fc2d7b958b2c57b184a98"
    "3c11bbfdaa41b517e1f3225be4199b42"
    "81ff21a264b15e23c0de28fc99f10e9a"
    "d88378275fc376441f8653fa618d12f7"
    "50b3091bec4d516bd23390795d97b060"
    "1d63efe98f877506bc68a513d1263882"
    "ba041056af34623e305cace291452bcb"
    "ee472eb8a996a37cfeb6e0d3a6df5984"
    "32bdd5c639a1a7bead4e662df89edcc7"
    "7d037040208be6d97e85cc8a0116e85a"
    "ab4c742a3dc97229e37f52940a898c37"
    "1cea3ad66ab4c165553ff60836950b9f"
    "73cd7a15ce9c14cf46fb02cadb88f9c4"
    "49ebdd6c004f6ef26724d0259d54a4ae"
)

_PAIR = bytes(T0[i & 0xFF] ^ T1[i >> 8] for i in range(0x10000))  # T0 ^ T1 for one 64 KiB block


def xform(data: bytes) -> bytes:
    """Decode or encode a package (the transform is its own inverse)."""
    out = bytearray(data[:32])
    pair = int.from_bytes(_PAIR, "little")
    for blk in range(0, len(data), 0x10000):
        chunk = data[blk:blk + 0x10000]
        ks = pair ^ int.from_bytes(bytes([T2[(blk >> 16) & 0xFF]]) * 0x10000, "little")
        ks_bytes = ks.to_bytes(0x10000, "little")[:len(chunk)]
        x = (int.from_bytes(chunk, "little") ^ int.from_bytes(ks_bytes, "little")).to_bytes(len(chunk), "little")
        if blk == 0:
            x = data[:32] + x[32:]
        out += x if blk else x[32:]
    return bytes(out)


def crc16(data: bytes) -> int:
    return binascii.crc_hqx(data, 0)


def zero_remainder(data: bytes) -> bool:
    return crc16(data) == 0


def put_crc(buf: bytearray, start: int, end: int) -> None:
    """Write the CRC of buf[start:end-2] into buf[end-2:end] (big-endian)."""
    buf[end - 2:end] = crc16(bytes(buf[start:end - 2])).to_bytes(2, "big")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def patch(buf: bytearray, offset: int, old: bytes, new: bytes, what: str) -> None:
    cur = bytes(buf[offset:offset + len(old)])
    if cur != old:
        raise SystemExit(f"unexpected bytes for {what} at 0x{offset:x}: {cur.hex()} (expected {old.hex()})")
    buf[offset:offset + len(new)] = new
