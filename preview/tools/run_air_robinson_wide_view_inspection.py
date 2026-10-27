#!/usr/bin/env python3
"""AIR ROBINSON ワイドビュー確認（PC 21:9 · iPhone · 250m 視線）."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

PREVIEW = Path(__file__).resolve().parents[1]
QA = PREVIEW / "qa"
HOME = (
    "http://127.0.0.1:8767/preview/air-robinson-home-entry-confirm.html"
    "?v=ar-wide-2026-10-27"
)
WIDE = (
    "http://127.0.0.1:8767/preview/air-robinson-wide-view-confirm.html"
    "?v=ar-wide-2026-10-27"
)


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    report: dict = {"home_url": HOME, "wide_url": WIDE, "checks": []}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, vp in (
            ("pc219", {"width": 1680, "height": 720}),
            ("iphone390", {"width": 390, "height": 844}),
        ):
            page = browser.new_page(viewport=vp)
            page.goto(HOME, wait_until="networkidle")
            page.screenshot(path=str(QA / f"ar-robinson-home-{label}.png"), full_page=True)
            icon_ok = page.locator("img[src*='hp_air_robinson_tile']").count() == 1
            page.goto(WIDE, wait_until="networkidle")
            page.wait_for_selector("#ar-wide-stage")
            ratio = page.evaluate(
                """() => {
                  const el = document.getElementById('ar-wide-stage');
                  const r = el.getBoundingClientRect();
                  return r.width / Math.max(1, r.height);
                }"""
            )
            page.locator("#ar-wide-stage").screenshot(
                path=str(QA / f"ar-robinson-wide-{label}.png")
            )
            low = page.evaluate(
                """() => {
                  const img = document.getElementById('ar-scenery');
                  const s = document.getElementById('alt-slider');
                  s.value = '180';
                  s.dispatchEvent(new Event('input', { bubbles: true }));
                  return Number(img.dataset.pitchDeg || 0);
                }"""
            )
            high = page.evaluate(
                """() => {
                  const img = document.getElementById('ar-scenery');
                  const s = document.getElementById('alt-slider');
                  s.value = '800';
                  s.dispatchEvent(new Event('input', { bubbles: true }));
                  return Number(img.dataset.pitchDeg || 0);
                }"""
            )
            routes = page.locator("#route-list button").count()
            has_comic = page.evaluate(
                "() => !!document.querySelector('.comic-8-wrap, #comic-rocky-8')"
            )
            page.close()
            report["checks"].append(
                {
                    "label": label,
                    "icon_on_home": icon_ok,
                    "aspect_ratio_21_9": abs(ratio - 21 / 9) < 0.08,
                    "pitch_low_under_250": low,
                    "pitch_high_reduced": high,
                    "pitch_low_near_40": 38 <= low <= 42,
                    "pitch_high_below_15": high < 15,
                    "five_routes": routes == 5,
                    "no_comic": not has_comic,
                }
            )
        browser.close()

    out = QA / "ar-robinson-wide-view-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = all(
        c["icon_on_home"]
        and c["aspect_ratio_21_9"]
        and c["pitch_low_near_40"]
        and c["pitch_high_below_15"]
        and c["five_routes"]
        and c["no_comic"]
        for c in report["checks"]
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("OK" if ok else "FAIL", out)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
