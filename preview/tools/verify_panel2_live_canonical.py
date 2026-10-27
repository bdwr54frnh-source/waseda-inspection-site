#!/usr/bin/env python3
"""第2コマ LIVE 正本（canonical/president-pass-2026-10-26）との一致確認。"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "canonical" / "president-pass-2026-10-26"
MANIFEST = CANON / "MANIFEST.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not MANIFEST.is_file():
        raise SystemExit(f"missing {MANIFEST}")
    spec = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = spec["sha256"]
    live_map = {
        "ec-live-clock.js": ROOT / "js" / "ec-live-clock.js",
        "ec-comic-fullbleed.css": ROOT / "css" / "ec-comic-fullbleed.css",
    }
    ok = True
    css_text = (ROOT / "css" / "ec-comic-fullbleed.css").read_text(encoding="utf-8")
    for mark in ("35.84% 33.48%", "46.2%", "comic-panel2-static-mask", "ec-live-clock.js 変更禁止"):
        if mark not in css_text:
            print("MISSING css marker", mark, file=sys.stderr)
            ok = False
    for name, exp in live_map.items():
        if name not in expected:
            continue
        live = live_map[name]
        got = sha256(live)
        if got != expected[name]:
            print("MISMATCH", name, "live", got, "canonical", expected[name], file=sys.stderr)
            ok = False
        else:
            print("OK", name)
    from PIL import Image
    import numpy as np

    canon_png = CANON / "elementary_code_rocky_8panel.png"
    live_png = ROOT / "assets" / "elementary_code_rocky_8panel.png"
    a = np.array(Image.open(canon_png).convert("RGB"))
    b = np.array(Image.open(live_png).convert("RGB"))
    p2 = np.abs(a[:, 256:512, :].astype(int) - b[:, 256:512, :].astype(int)).sum(axis=2)
    if (p2 > 0).any():
        print("MISMATCH rocky panel2 column pixels", file=sys.stderr)
        ok = False
    else:
        print("OK rocky panel2 column identical to canonical PNG")
    if not ok:
        raise SystemExit(1)
    print("OK panel2 live president-pass verify")


if __name__ == "__main__":
    main()
