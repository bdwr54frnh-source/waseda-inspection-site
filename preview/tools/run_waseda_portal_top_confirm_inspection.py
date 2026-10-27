#!/usr/bin/env python3
"""ポータル top · PC / iPhone / Windows UA 相当."""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

PREVIEW = Path(__file__).resolve().parents[1]
QA = PREVIEW / "qa"
BASE = "http://127.0.0.1:8765"
URL = f"{BASE}/preview/waseda-portal-top-confirm.html?v=portal-2026-10-27-confirm"
INDEX = f"{BASE}/index.html?v=portal-2026-10-27-confirm"


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    report: dict = {"index_url": INDEX, "confirm_url": URL, "checks": []}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        configs = (
            ("pc1280", {"width": 1280, "height": 900}, None),
            ("iphone390", {"width": 390, "height": 844}, "iphone"),
            (
                "win_chrome",
                {"width": 1280, "height": 900},
                "windows",
            ),
        )
        for label, vp, kind in configs:
            kw: dict = {"viewport": vp}
            if kind == "iphone":
                kw["user_agent"] = (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                    "Mobile/15E148 Safari/604.1"
                )
            elif kind == "windows":
                kw["user_agent"] = (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            page = browser.new_page(**kw)
            page.goto(INDEX, wait_until="networkidle")
            title = page.title()
            meta = page.locator('meta[name="portal-template-version"]').get_attribute(
                "content"
            )
            has_outlook = page.locator('a[href^="mailto:waseda-inspection@outlook.com"]').count()
            has_info_mailto = page.locator('a[href^="mailto:info@waseda-inspection.com"]').count()
            portal = page.locator("#portal")
            page.locator("body").screenshot(path=str(QA / f"waseda-portal-top-{label}.png"))
            page.close()
            report["checks"].append(
                {
                    "label": label,
                    "title": title,
                    "portal_template_version": meta,
                    "outlook_mailto_count": has_outlook,
                    "info_mailto_count": has_info_mailto,
                    "portal_section": portal.count() == 1,
                }
            )
        browser.close()

    ok = all(
        c["title"].startswith("早稲田インスペクション")
        and c["portal_template_version"] == "portal-2026-10-27-confirm"
        and c["outlook_mailto_count"] >= 1
        and c["info_mailto_count"] == 0
        and c["portal_section"]
        for c in report["checks"]
    )
    out = QA / "waseda-portal-top-confirm-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("OK" if ok else "FAIL", out)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
