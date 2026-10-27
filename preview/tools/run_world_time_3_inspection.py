#!/usr/bin/env python3
"""世界時刻3都市 LIVE（漫画ページと別 URL · 2秒差分）."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
URL = (
    "http://127.0.0.1:8766/world-time-3cities-live-confirm.html"
    "?v=world-time-3-2026-10-27&ecConfirmLive=1"
)
TICK_MS = 2000
IDS = ("world-clock-tokyo", "world-clock-london", "world-clock-sf")


def _state(page) -> dict:
    return page.evaluate(
        """(ids) => {
          const out = {};
          ids.forEach((id) => {
            const el = document.getElementById(id);
            out[id] = {
              digits: (el && el.textContent ? el.textContent : '').trim(),
              live: !!(el && el.classList.contains('is-live'))
            };
          });
          const comic = document.querySelector('.comic-8-wrap');
          return { cities: out, hasComic: !!comic };
        }""",
        list(IDS),
    )


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    report: dict = {"url": URL, "tick_ms": TICK_MS, "checks": []}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, vp, zoom, ua in (
            ("100pct", {"width": 1024, "height": 800}, 1.0, False),
            ("iphone390", {"width": 390, "height": 844}, 1.0, True),
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
            if zoom != 1.0:
                page.evaluate("(z) => { document.body.style.zoom = z; }", zoom)
            s0 = _state(page)
            page.screenshot(path=str(QA / f"world-time-3-{label}-t0.png"), full_page=True)
            page.wait_for_timeout(TICK_MS)
            s1 = _state(page)
            page.screenshot(path=str(QA / f"world-time-3-{label}-t1.png"), full_page=True)
            page.close()
            tick_ok = all(
                s0["cities"][i]["digits"] != s1["cities"][i]["digits"]
                and s0["cities"][i]["live"]
                for i in IDS
            )
            report["checks"].append(
                {
                    "label": label,
                    "tick_ok": tick_ok,
                    "no_comic_on_page": not s0["hasComic"] and not s1["hasComic"],
                    "cities_t0": {i: s0["cities"][i]["digits"] for i in IDS},
                    "cities_t1": {i: s1["cities"][i]["digits"] for i in IDS},
                }
            )
        browser.close()

    out = QA / "world-time-3-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = all(c["tick_ok"] and c["no_comic_on_page"] for c in report["checks"])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("OK" if ok else "FAIL", out)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
