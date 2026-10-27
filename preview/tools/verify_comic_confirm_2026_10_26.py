#!/usr/bin/env python3
"""2026-10-26 確認用 PNG · 第2コマ列＝LIVE合格 readonly · 原本 hash 不変。"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "comic-panel3-dialogue.json"
ORIG_CORRECT = ROOT / "assets" / "originals" / "elementary_code_correct_8panel_READONLY.png"
ORIG_ROCKY = ROOT / "assets" / "originals" / "elementary_code_rocky_8panel_LIVE_PASS_READONLY.png"
OUT_ROCKY = ROOT / "assets" / "elementary_code_rocky_8panel.png"
HASH_STORE = ROOT / "assets" / "originals" / "SHA256.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not OUT_ROCKY.is_file():
        raise SystemExit(f"missing {OUT_ROCKY}")
    spec = json.loads(DATA.read_text(encoding="utf-8"))
    box = spec["panel3_rocky_speech"]["box"]
    x0, y0, x1, y1 = (int(v) for v in box)

    pass_img = np.array(Image.open(ORIG_ROCKY).convert("RGB"))
    out_img = np.array(Image.open(OUT_ROCKY).convert("RGB"))

    if not np.array_equal(pass_img[:, :512, :], out_img[:, :512, :]):
        raise SystemExit("panel 1–2 columns differ from LIVE pass readonly")

    panel3 = np.zeros(pass_img.shape[:2], dtype=bool)
    panel3[137:339, 512:768] = True
    allowed = np.zeros(pass_img.shape[:2], dtype=bool)
    allowed[y0:y1, x0:x1] = True
    diff = np.any(pass_img != out_img, axis=2)
    bad = diff & panel3 & ~allowed
    if bad.any():
        raise SystemExit(f"panel3 diff outside speech box ({int(bad.sum())} px)")

    if HASH_STORE.is_file():
        stored = json.loads(HASH_STORE.read_text(encoding="utf-8"))
        for name, path in (
            ("correct_readonly", ORIG_CORRECT),
            ("rocky_pass_readonly", ORIG_ROCKY),
        ):
            got = sha256(path)
            if stored.get(name) and stored[name] != got:
                raise SystemExit(f"readonly hash changed: {name}")
    else:
        HASH_STORE.write_text(
            json.dumps(
                {
                    "correct_readonly": sha256(ORIG_CORRECT),
                    "rocky_pass_readonly": sha256(ORIG_ROCKY),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    print("OK comic confirm 2026-10-26 verify")


if __name__ == "__main__":
    main()
