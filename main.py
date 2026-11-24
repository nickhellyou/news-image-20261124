#!/usr/bin/env python3
"""Entry program for news-image-20261124: copy the bundled front page to
the output directory. Standard library only, no network, deterministic.
"""
import hashlib
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
# sha256 of the bundled entry.png, recorded at build time.
EXPECTED_SHA256 = "8014cfb1c888f0e873000802b82c268221058a64c2dd185576c60843976a7d42"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SOURCE.read_bytes()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit(f"entry.png is {width}x{height}, over the 1024 cap")
    print(f"entry.png dimensions: {width}x{height}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"entry.png sha256 mismatch: {digest}")
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    copied = target.read_bytes()
    if hashlib.sha256(copied).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("copied entry.png sha256 mismatch")
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
