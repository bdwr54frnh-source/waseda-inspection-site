#!/usr/bin/env python3
"""第3コマだけ差し替えて 8コマ1枚 PNG に焼き込む（1024×678 正本）。"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ORIG = Path(
    "/Users/kiyoshisekine/.cursor/projects/Users-kiyoshisekine-Desktop-AirQuick-Final-3/assets/"
    "Cursor_Composer________-fdae092c-7bff-4b2e-9114-5ea46b84885f.jpg"
)
REV = Path(
    "/Users/kiyoshisekine/.cursor/projects/Users-kiyoshisekine-Desktop-AirQuick-Final-3/assets/"
    "__________2026-10-26_18.17.40-1946ef98-05b6-4771-b0f0-28284250ad6d.jpg"
)
# 4列上段 · 1024×678 実測（HTML 重ねと同じ枠）
PANEL3 = (512, 137, 768, 339)
OUT_PREVIEW = ROOT / "assets" / "elementary_code_rocky_8panel.png"
OUT_MIRROR = ROOT.parent / "assets" / "elementary_code_rocky_8panel.png"


def cover_into_panel(src: Image.Image, tw: int, th: int) -> Image.Image:
    sw, sh = src.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(round(sw * scale)), int(round(sh * scale))
    scaled = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return scaled.crop((left, top, left + tw, top + th))


def main() -> None:
    x0, y0, x1, y1 = PANEL3
    tw, th = x1 - x0, y1 - y0
    orig = Image.open(ORIG).convert("RGB")
    rev = Image.open(REV).convert("RGB")
    if orig.size != (1024, 678):
        raise SystemExit(f"unexpected orig size {orig.size}")
    patch = cover_into_panel(rev, tw, th)
    out = orig.copy()
    out.paste(patch, (x0, y0))
    out.save(OUT_PREVIEW, optimize=True)
    out.save(OUT_MIRROR, optimize=True)
    print("OK", OUT_PREVIEW, OUT_MIRROR, "panel3", PANEL3)


if __name__ == "__main__":
    main()
