#!/usr/bin/env python3
"""Meme Sprint 3 entry: write the rogue-agent meme to /output/entry.png.

The meme is drawn procedurally by draw.py (PIL + DejaVu, no network, no
clock, no randomness), so the two grader runs render the same bytes. If
Pillow is missing in the sandbox, fall back to the pre-rendered entry.png
shipped beside this file — the same picture, drawn by the same code.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Gate (from the kit's RULES.txt): /output/entry.png must be a whole PNG or
JPEG, at most 1 MiB (1,048,576 bytes) and 1024 by 1024 pixels. This file
checks those caps before it writes anything.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def check_png(path):
    """Refuse to ship a file the gate would reject: bad magic, oversize,
    or over 1024 px a side. A corrupt copy fails silently in v1; here it
    fails loudly before anything is written."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png: not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png: %d bytes, over the 1 MiB cap" % size)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit("entry.png: %dx%d, over 1024 px a side"
                         % (width, height))
    return width, height, size


def render_or_copy(tmp_path):
    """Draw the meme fresh with draw.py; fall back to the shipped PNG."""
    try:
        sys.path.insert(0, HERE)
        import draw
        draw.render(tmp_path)
        return "drawn"
    except Exception as exc:  # noqa: BLE001 - sandbox may lack Pillow
        print("draw.py unavailable (%s); using shipped entry.png" % exc)
        shutil.copyfile(os.path.join(HERE, "entry.png"), tmp_path)
        return "copied"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    tmp_path = os.path.join(HERE, ".entry-tmp.png")
    try:
        mode = render_or_copy(tmp_path)
        width, height, size = check_png(tmp_path)
    finally:
        pass
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(tmp_path, os.path.join(out_dir, "entry.png"))
    os.remove(tmp_path)
    print("entry.png %dx%d %d bytes -> %s (%s)"
          % (width, height, size, out_dir, mode))


if __name__ == "__main__":
    main()
