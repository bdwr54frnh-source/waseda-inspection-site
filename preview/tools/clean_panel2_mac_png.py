#!/usr/bin/env python3
"""第2コマ Mac 液晶 clip 内の固定時計（白・黄）だけ消す。第1・第3コマ列は触らない。"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "assets" / "masters" / "elementary_code_rocky_8panel_master.png"
OUT = ROOT / "assets" / "elementary_code_rocky_8panel.png"
MAC_BLUE = np.array([4, 23, 56], dtype=np.uint8)
# 1024×678 · screen-final4 と同型（第2コマ列 x≤511 にクリップ）
MAC_POLY = np.array(
    [
        (367, 227),
        (511, 221),
        (511, 277),
        (370, 243),
    ],
    dtype=np.float64,
)
# 「(0.01秒まで表示)」行（y≥253）は残す
SUBCAPTION_Y0 = 253


def _inside_poly(xs: np.ndarray, ys: np.ndarray, poly: np.ndarray) -> np.ndarray:
    """Vectorized ray-cast; xs/ys are 1d same length."""
    n = len(poly)
    inside = np.zeros(xs.shape[0], dtype=bool)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        cond = ((yi > ys) != (yj > ys)) & (
            xs < (xj - xi) * (ys - yi) / (yj - yi + 1e-9) + xi
        )
        inside ^= cond
        j = i
    return inside


def main() -> None:
    if not MASTER.is_file():
        raise SystemExit(f"missing {MASTER}")
    base = np.array(Image.open(MASTER).convert("RGB"))
    out = base.copy()
    if OUT.is_file():
        prev = np.array(Image.open(OUT).convert("RGB"))
        out[:, 512:, :] = prev[:, 512:, :]
        out[137:339, 512:768] = prev[137:339, 512:768]

    x0, x1 = 256, 512
    y0, y1 = 175, SUBCAPTION_Y0
    patch = out[y0:y1, x0:x1].copy()
    h, w = patch.shape[:2]
    gx, gy = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
    flat_x = gx.ravel().astype(np.float64)
    flat_y = gy.ravel().astype(np.float64)
    in_mac = _inside_poly(flat_x, flat_y, MAC_POLY).reshape(h, w)

    r, g, b = patch[:, :, 0], patch[:, :, 1], patch[:, :, 2]
    digit = (
        ((r > 175) & (g > 165) & (b > 165))
        | ((r > 190) & (g > 140) & (b < 130))
        | ((r > 140) & (g > 140) & (b > 140) & (r + g + b > 420))
    )
    replace = in_mac & digit
    patch[replace] = MAC_BLUE
    out[y0:y1, x0:x1] = patch

    Image.fromarray(out).save(OUT, optimize=True)
    ys, xs = np.where(replace)
    print(
        "OK",
        OUT.name,
        "mac_poly pixels cleaned",
        int(replace.sum()),
        "bbox",
        (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)
        if replace.any()
        else None,
    )


if __name__ == "__main__":
    main()
