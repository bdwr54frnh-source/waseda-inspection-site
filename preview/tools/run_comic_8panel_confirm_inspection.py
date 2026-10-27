#!/usr/bin/env python3
"""8コマ確認: 焼き込み PNG · 第2コマ静止 · PC/iPhone."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

PREVIEW = Path(__file__).resolve().parents[1]
QA = PREVIEW / "qa"
URL = (
    "http://127.0.0.1:8766/elementary-comic-live-confirm.html"
    "?v=8komamanga-001-2026-10-27"
)
MASTER = (
    PREVIEW
    / "assets"
    / "originals"
    / "elementary_code_rocky_8panel_FROM_8komamanga_001_2026-10-27_READONLY.png"
)
DISPLAY = PREVIEW / "assets" / "elementary_code_rocky_8panel.png"


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    png_ok = (
        MASTER.is_file()
        and DISPLAY.is_file()
        and hashlib.sha256(MASTER.read_bytes()).digest()
        == hashlib.sha256(DISPLAY.read_bytes()).digest()
    )
    report: dict = {
        "url": URL,
        "png_matches_master": png_ok,
        "size_px": [1024, 678],
        "checks": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, vp, ua in (
            ("pc1024", {"width": 1024, "height": 900}, False),
            ("iphone390", {"width": 390, "height": 844}, True),
        ):
            kw: dict = {"viewport": vp}
            if ua:
                kw["user_agent"] = (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                    "Mobile/15E148 Safari/604.1"
                )
            page = browser.new_page(**kw)
            page.goto(URL, wait_until="networkidle")
            has_p3 = page.locator(".comic-panel3-keynote img").count()
            has_p2_live = page.locator("#comic-panel2-clock").count()
            img = page.locator("#comic-rocky-8")
            w = img.evaluate("el => el.naturalWidth")
            h = img.evaluate("el => el.naturalHeight")
            page.locator(".comic-8-wrap").screenshot(
                path=str(QA / f"comic-8panel-{label}.png")
            )
            page.close()
            report["checks"].append(
                {
                    "label": label,
                    "panel3_overlay_count": has_p3,
                    "panel2_live_dom_count": has_p2_live,
                    "natural_size": [w, h],
                }
            )
        browser.close()

    out = QA / "comic-8panel-confirm-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = png_ok and all(
        c["panel3_overlay_count"] == 0
        and c["panel2_live_dom_count"] == 0
        and c["natural_size"] == [1024, 678]
        for c in report["checks"]
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("OK" if ok else "FAIL", out)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
