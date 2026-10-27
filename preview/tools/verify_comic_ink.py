#!/usr/bin/env python3
"""吹き出し矩形内のインク量チェック（確認用）"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from comic_bubble_util import INK_THRESH

BOXES_8 = [
    (20, 198, 302, 328),
    (346, 198, 638, 290),
    (670, 198, 928, 354),
    (996, 198, 1290, 388),
    (20, 644, 304, 834),
    (346, 644, 638, 846),
    (670, 692, 962, 912),
    (996, 636, 1292, 1008),
]


def count_ink(path: Path, boxes: list[tuple[int, int, int, int]]) -> int:
    im = Image.open(path).convert("RGB")
    px = im.load()
    n = 0
    for box in boxes:
        x0, y0, x1, y1 = box
        for y in range(y0, y1):
            for x in range(x0, x1):
                if sum(px[x, y]) < INK_THRESH:
                    n += 1
    return n


def main() -> None:
    p8 = ROOT / "assets" / "elementary_code_8panel_confirm_bubbles.png"
    if not p8.is_file():
        raise SystemExit("missing 8panel png")
    ink = count_ink(p8, BOXES_8)
    print("8panel ink pixels in boxes:", ink)
    if ink > 32000:
        raise SystemExit("too much ink in boxes")
    print("verify_comic_ink: ok")


if __name__ == "__main__":
    main()
