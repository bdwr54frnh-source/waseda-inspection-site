#!/usr/bin/env python3
"""第3コマの台詞文字だけ差し替え（合格 8コマ PNG · x<512 不変更）。

- 正本: canonical/president-pass-2026-10-26/elementary_code_rocky_8panel.png
- 座標: data/comic-panel3-dialogue.json の panel3_rocky_speech（1024×678 全局）
- Keynote 焼き込み・HTML 重ね・他コマ改変は行わない
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from comic_bubble_util import replace_bubble_on_image

DATA = ROOT / "data" / "comic-panel3-dialogue.json"
OUT_ROCKY = ROOT / "assets" / "elementary_code_rocky_8panel.png"
ROCKY_PASS = ROOT / "canonical" / "president-pass-2026-10-26" / "elementary_code_rocky_8panel.png"
PANEL3_BOUNDS = (512, 137, 768, 339)


def _box(raw: list[int]) -> tuple[int, int, int, int]:
    if len(raw) != 4:
        raise ValueError(f"box must be [x0,y0,x1,y1], got {raw}")
    x0, y0, x1, y1 = (int(v) for v in raw)
    return x0, y0, x1, y1


def _box_inside_panel3(box: tuple[int, int, int, int]) -> None:
    px0, py0, px1, py1 = PANEL3_BOUNDS
    x0, y0, x1, y1 = box
    if x0 < px0 or y0 < py0 or x1 > px1 or y1 > py1:
        raise SystemExit(f"speech box outside panel3 {box} not in {PANEL3_BOUNDS}")


def _assert_panel12_unchanged(before: Image.Image, after: Image.Image) -> None:
    a = np.array(before.convert("RGB"))
    b = np.array(after.convert("RGB"))
    if not np.array_equal(a[:, :512, :], b[:, :512, :]):
        diff = np.abs(a[:, :512, :].astype(int) - b[:, :512, :].astype(int)).sum(axis=2)
        raise SystemExit(f"panel 1–2 changed ({int((diff > 0).sum())} px)")


def _assert_only_speech_boxes_changed(
    before: Image.Image, after: Image.Image, boxes: list[tuple[int, int, int, int]]
) -> None:
    a = np.array(before.convert("RGB"))
    b = np.array(after.convert("RGB"))
    mask = np.zeros(a.shape[:2], dtype=bool)
    for x0, y0, x1, y1 in boxes:
        mask[y0:y1, x0:x1] = True
    px0, py0, px1, py1 = PANEL3_BOUNDS
    panel3 = np.zeros(a.shape[:2], dtype=bool)
    panel3[py0:py1, px0:px1] = True
    allowed = panel3 & mask
    outside = panel3 & ~allowed
    diff = np.any(a != b, axis=2)
    bad_outside = diff & outside
    if bad_outside.any():
        raise SystemExit(
            f"panel3 changed outside speech boxes ({int(bad_outside.sum())} px)"
        )


def main() -> None:
    if not DATA.is_file():
        raise SystemExit(f"missing {DATA}")
    if not ROCKY_PASS.is_file():
        raise SystemExit(f"missing {ROCKY_PASS}")

    spec = json.loads(DATA.read_text(encoding="utf-8"))
    blocks = spec.get("panel3_rocky_speech") or []
    if not blocks:
        raise SystemExit("panel3_rocky_speech is empty")

    rocky_base = Image.open(ROCKY_PASS).convert("RGBA")
    rocky_out = rocky_base.copy()
    boxes: list[tuple[int, int, int, int]] = []
    for block in blocks:
        box = _box(block["box"])
        _box_inside_panel3(box)
        boxes.append(box)
        replace_bubble_on_image(
            rocky_base,
            rocky_out,
            box,
            block["text"],
            max_font=int(block.get("max_font", 12)),
        )

    _assert_panel12_unchanged(rocky_base, rocky_out)
    _assert_only_speech_boxes_changed(rocky_base, rocky_out, boxes)
    rocky_out.save(OUT_ROCKY, optimize=True)
    print("OK", OUT_ROCKY.name, "<-", DATA.name, "boxes", len(boxes))


if __name__ == "__main__":
    main()
