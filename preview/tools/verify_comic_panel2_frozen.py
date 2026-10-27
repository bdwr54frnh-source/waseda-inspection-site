#!/usr/bin/env python3
"""第2コマ LIVE 固定確認（社長合格版 canonical/president-pass-2026-10-26）。"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "js/ec-live-clock.js": "a4b2e6079f576e762b22187bfbea0095cd822d1b54066f110a4fa4dd27e4dc75",
    "css/ec-comic-fullbleed.css": None,
}

CSS_FINGERPRINT_MARKERS = (
    "screen-final4",
    "46.2%",
    "35.1%",
    "12.65%",
    "comic-panel2-static-mask",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    js_path = ROOT / "js/ec-live-clock.js"
    css_path = ROOT / "css/ec-comic-fullbleed.css"
    js_hash = sha256(js_path)
    if js_hash != EXPECTED["js/ec-live-clock.js"]:
        raise SystemExit(f"ec-live-clock.js changed: {js_hash}")
    css_text = css_path.read_text(encoding="utf-8")
    for mark in CSS_FINGERPRINT_MARKERS:
        if mark not in css_text:
            raise SystemExit(f"ec-comic-fullbleed.css missing marker: {mark}")
    print("OK panel2 frozen", js_path.name, css_path.name)
    import subprocess

    subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_panel2_live_canonical.py")],
        check=True,
    )


if __name__ == "__main__":
    main()
