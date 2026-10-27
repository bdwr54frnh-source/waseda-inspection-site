#!/usr/bin/env python3
"""8コマ漫画のみ: 静止画 · オーバーレイなし · ec-live-clock 不要."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
COMIC_URL = (
    "http://127.0.0.1:8766/elementary-comic-live-confirm.html"
    "?v=comic-final-static-2026-10-27"
)
READONLY = (
    ROOT
    / "assets"
    / "originals"
    / "elementary_code_rocky_8panel_MASTER_BOY_DIALOG_2026-10-27_READONLY.png"
)
DISPLAY = ROOT / "assets" / "elementary_code_rocky_8panel.png"


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    png_ok = (
        READONLY.is_file()
        and DISPLAY.is_file()
        and hashlib.sha256(READONLY.read_bytes()).digest()
        == hashlib.sha256(DISPLAY.read_bytes()).digest()
    )
    report: dict = {"comic_url": COMIC_URL, "png_matches_readonly": png_ok, "checks": []}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, viewport, zoom in (
            ("100pct", {"width": 1024, "height": 800}, 1.0),
            ("75pct", {"width": 1024, "height": 800}, 0.75),
        ):
            page = browser.new_page(viewport=viewport)
            page.goto(COMIC_URL, wait_until="networkidle")
            if zoom != 1.0:
                page.evaluate("(z) => { document.body.style.zoom = z; }", zoom)
            has_world = page.evaluate(
                "() => !!document.querySelector('.ec-world-clocks-3, .comic-panel2-screen')"
            )
            page.locator(".comic-8-wrap").screenshot(
                path=str(QA / f"comic-final-static-{label}.png")
            )
            page.close()
            report["checks"].append(
                {"label": label, "no_overlay_no_world_on_comic": not has_world}
            )

        iphone = browser.new_page(
            viewport={"width": 390, "height": 844},
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                "Mobile/15E148 Safari/604.1"
            ),
        )
        iphone.goto(COMIC_URL, wait_until="networkidle")
        has_world = iphone.evaluate(
            "() => !!document.querySelector('.ec-world-clocks-3, .comic-panel2-screen')"
        )
        iphone.locator(".comic-8-wrap").screenshot(
            path=str(QA / "comic-final-static-iphone390.png")
        )
        iphone.close()
        browser.close()
        report["checks"].append(
            {"label": "iphone390", "no_overlay_no_world_on_comic": not has_world}
        )

    out = QA / "comic-final-static-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    all_ok = png_ok and all(c["no_overlay_no_world_on_comic"] for c in report["checks"])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("OK" if all_ok else "FAIL", out)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
