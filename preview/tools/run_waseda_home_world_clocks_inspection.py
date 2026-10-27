#!/usr/bin/env python3
"""waseda-inspection index.html · #world-clocks（3都市 LIVE + 代表ポスター順）."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PREVIEW = ROOT / "preview"
QA = PREVIEW / "qa"
URL = (
    "http://127.0.0.1:8767/index.html"
    "?v=home-world-clocks-sf-2026-10-27#world-clocks"
)
TICK_MS = 2000
IDS = ("world-clock-tokyo", "world-clock-london", "world-clock-sf")
POSTER = "assets/hp_promo_elementary_code_infographic.jpg"


def _state(page) -> dict:
    return page.evaluate(
        """(ids) => {
          const sec = document.getElementById('world-clocks');
          const poster = sec && sec.querySelector('.world-clocks-poster img');
          const order = sec ? Array.from(sec.children).map((n) => n.tagName + '.' + (n.className || n.id || '')) : [];
          const cities = {};
          ids.forEach((id) => {
            const el = document.getElementById(id);
            cities[id] = {
              digits: (el && el.textContent ? el.textContent : '').trim(),
              live: !!(el && el.classList.contains('is-live')),
            };
          });
          const ecPoster = document.querySelector('#elementary-code .media-frame-dark');
          return {
            cities,
            posterSrc: poster ? poster.getAttribute('src') || '' : '',
            order,
            ecSectionHasPosterFrame: !!ecPoster,
            hasComic: !!document.querySelector('.comic-8-wrap, #comic-rocky-8'),
          };
        }""",
        list(IDS),
    )


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    report: dict = {"url": URL, "tick_ms": TICK_MS, "checks": []}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, vp, ua in (
            ("pc920", {"width": 920, "height": 900}, False),
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
            page.locator("#world-clocks").scroll_into_view_if_needed()
            s0 = _state(page)
            page.locator("#world-clocks").screenshot(
                path=str(QA / f"waseda-home-world-clocks-{label}-t0.png")
            )
            page.wait_for_timeout(TICK_MS)
            s1 = _state(page)
            page.locator("#world-clocks").screenshot(
                path=str(QA / f"waseda-home-world-clocks-{label}-t1.png")
            )
            page.close()

            tick_ok = all(
                s0["cities"][i]["digits"] != s1["cities"][i]["digits"]
                and s0["cities"][i]["live"]
                for i in IDS
            )
            order_ok = False
            if s0["order"]:
                joined = " ".join(s0["order"]).lower()
                order_ok = (
                    joined.find("h2") >= 0
                    and joined.find("world-clocks-live") < joined.find("world-clocks-poster")
                )
            poster_ok = POSTER in (s0["posterSrc"] or "")
            report["checks"].append(
                {
                    "label": label,
                    "tick_ok": tick_ok,
                    "order_live_before_poster": order_ok,
                    "poster_unchanged_path": poster_ok,
                    "no_poster_in_ec_section": not s0["ecSectionHasPosterFrame"],
                    "no_comic_on_hp": not s0["hasComic"],
                    "cities_t0": {i: s0["cities"][i]["digits"] for i in IDS},
                    "cities_t1": {i: s1["cities"][i]["digits"] for i in IDS},
                }
            )
        browser.close()

    out = QA / "waseda-home-world-clocks-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = all(
        c["tick_ok"]
        and c["order_live_before_poster"]
        and c["poster_unchanged_path"]
        and c["no_poster_in_ec_section"]
        and c["no_comic_on_hp"]
        for c in report["checks"]
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("OK" if ok else "FAIL", out)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
