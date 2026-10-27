#!/usr/bin/env python3
"""公開 https://waseda-inspection.com/ · Mac / Win / iPhone UA."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

QA = Path(__file__).resolve().parents[1] / "qa"
LIVE = "https://waseda-inspection.com/"


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    body = urllib.request.urlopen(LIVE, timeout=30).read()
    sha = hashlib.sha256(body).hexdigest()
    report: dict = {
        "live_url": LIVE,
        "live_sha256": sha,
        "live_bytes": len(body),
        "checks": [],
    }

    configs = (
        ("mac1280", {"width": 1280, "height": 900}, None),
        ("win1280", {"width": 1280, "height": 900}, "win"),
        ("iphone390", {"width": 390, "height": 844}, "iphone"),
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, vp, kind in configs:
            kw: dict = {"viewport": vp}
            if kind == "win":
                kw["user_agent"] = (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            elif kind == "iphone":
                kw["user_agent"] = (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                    "Mobile/15E148 Safari/604.1"
                )
            page = browser.new_page(**kw)
            page.goto(LIVE, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector("#portal", timeout=20000)
            report["checks"].append(
                {
                    "label": label,
                    "title": page.title(),
                    "portal_meta": page.locator(
                        'meta[name="portal-template-version"]'
                    ).get_attribute("content"),
                    "outlook_mailto": page.locator(
                        'a[href^="mailto:waseda-inspection@outlook.com"]'
                    ).count(),
                    "info_mailto": page.locator(
                        'a[href^="mailto:info@"]'
                    ).count(),
                    "overflow_x": page.evaluate(
                        "document.documentElement.scrollWidth > "
                        "document.documentElement.clientWidth"
                    ),
                }
            )
            page.locator("#portal").screenshot(
                path=str(QA / f"waseda-live-portal-{label}.png")
            )
            page.close()
        browser.close()

    ok = sha == "ee6f5e28ac5c6ac6de96f16ad62dbe0eb0d33391a0f7bc82038e223029ded5f4" and all(
        c["title"].startswith("早稲田インスペクション")
        and c["info_mailto"] == 0
        and c["outlook_mailto"] >= 1
        and not c["overflow_x"]
        for c in report["checks"]
    )
    out = QA / "waseda-live-https-inspection-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("OK" if ok else "FAIL", out)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
