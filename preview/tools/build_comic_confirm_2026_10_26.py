#!/usr/bin/env python3
"""2026-10-26 確認用8コマ生成（原本上書き禁止 · 第3コマ台詞のみ · 別ファイル出力）。"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from clean_panel2_mac_png import MAC_POLY, SUBCAPTION_Y0, _inside_poly
from comic_bubble_util import replace_bubble_on_image

DATA = ROOT / "data" / "comic-panel3-dialogue.json"
ORIG_CORRECT = ROOT / "assets" / "originals" / "elementary_code_correct_8panel_READONLY.png"
ORIG_ROCKY_PASS = (
    ROOT / "assets" / "originals" / "elementary_code_rocky_8panel_LIVE_PASS_READONLY.png"
)
OUT_CORRECT = ROOT / "assets" / "elementary_code_8panel_confirm_2026-10-26.png"
OUT_ROCKY = ROOT / "assets" / "elementary_code_rocky_8panel.png"
OUT_ROCKY_ARCHIVE = ROOT / "assets" / "elementary_code_rocky_8panel_confirm_2026-10-26.png"
MAC_BLUE = np.array([4, 23, 56], dtype=np.uint8)
PANEL3_ROCKY = (512, 137, 768, 339)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_readonly_unchanged(path: Path, expected_hash: str | None) -> str:
    h = _sha256(path)
    if expected_hash and h != expected_hash:
        raise SystemExit(f"readonly modified: {path.name}")
    return h


def _box(raw: list[int] | tuple[int, ...]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = (int(v) for v in raw)
    return x0, y0, x1, y1


def _clean_panel2_mac_on_array(out: np.ndarray) -> None:
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
    patch[in_mac & digit] = MAC_BLUE
    out[y0:y1, x0:x1] = patch


def _assert_cols_unchanged(before: np.ndarray, after: np.ndarray, x1: int = 512) -> None:
    if not np.array_equal(before[:, :x1, :], after[:, :x1, :]):
        raise SystemExit(f"columns 0–{x1 - 1} changed")


def _assert_panel3_only_boxes(
    before: np.ndarray, after: np.ndarray, boxes: list[tuple[int, int, int, int]]
) -> None:
    px0, py0, px1, py1 = PANEL3_ROCKY
    mask = np.zeros(before.shape[:2], dtype=bool)
    for x0, y0, x1, y1 in boxes:
        mask[y0:y1, x0:x1] = True
    panel3 = np.zeros(before.shape[:2], dtype=bool)
    panel3[py0:py1, px0:px1] = True
    diff = np.any(before != after, axis=2)
    bad = diff & panel3 & ~mask
    if bad.any():
        raise SystemExit(f"panel3 changed outside speech box ({int(bad.sum())} px)")


def main() -> None:
    if not DATA.is_file():
        raise SystemExit(f"missing {DATA}")
    for p in (ORIG_CORRECT, ORIG_ROCKY_PASS):
        if not p.is_file():
            raise SystemExit(f"missing {p}")

    spec = json.loads(DATA.read_text(encoding="utf-8"))
    text = spec.get("panel3_dialogue_text", "").strip()
    if not text:
        raise SystemExit("panel3_dialogue_text empty")

    hash_before_correct = _sha256(ORIG_CORRECT)
    hash_before_rocky = _sha256(ORIG_ROCKY_PASS)

    # --- 1312×1199 依頼者正本 → 確認用（第3コマ吹き出しのみ）---
    base_c = Image.open(ORIG_CORRECT).convert("RGBA")
    out_c = base_c.copy()
    c_spec = spec["panel3_correct_speech"]
    c_box = _box(c_spec["box"])
    replace_bubble_on_image(
        base_c,
        out_c,
        c_box,
        text,
        max_font=int(c_spec.get("max_font", 11)),
    )
    out_c.save(OUT_CORRECT, optimize=True)

    # --- 1024×678 LIVE 合格原画 → 確認用（第3コマ台詞矩形のみ）---
    base_r = Image.open(ORIG_ROCKY_PASS).convert("RGBA")
    before_r = np.array(base_r.convert("RGB"))
    out_r = base_r.copy()
    r_spec = spec["panel3_rocky_speech"]
    r_box = _box(r_spec["box"])
    px0, py0, px1, py1 = PANEL3_ROCKY
    if r_box[0] < px0 or r_box[2] > px1 or r_box[1] < py0 or r_box[3] > py1:
        raise SystemExit(f"rocky speech box outside panel3 {r_box}")
    replace_bubble_on_image(
        base_r,
        out_r,
        r_box,
        text,
        max_font=int(r_spec.get("max_font", 9)),
    )
    after_r = np.array(out_r.convert("RGB"))
    _assert_cols_unchanged(before_r, after_r, 512)
    _assert_panel3_only_boxes(before_r, after_r, [r_box])
    out_r.save(OUT_ROCKY, optimize=True)
    out_r.save(OUT_ROCKY_ARCHIVE, optimize=True)

    _assert_readonly_unchanged(ORIG_CORRECT, hash_before_correct)
    _assert_readonly_unchanged(ORIG_ROCKY_PASS, hash_before_rocky)

    print("OK", OUT_CORRECT.name, OUT_ROCKY.name, OUT_ROCKY_ARCHIVE.name)
    print("readonly correct sha256", hash_before_correct[:16], "...")
    print("readonly rocky pass sha256", hash_before_rocky[:16], "...")


if __name__ == "__main__":
    main()
