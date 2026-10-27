#!/usr/bin/env python3
"""PR #6 相当 · トップ確認（Mac / Windows UA · PC / iPhone 幅）."""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

PREVIEW = Path(__file__).resolve().parents[1]
QA = PREVIEW / "qa"
BASE = "http://127.0.0.1:8765"
CONFIRM = f"{BASE}/preview/waseda-portal-top-confirm.html"
INDEX = f"{BASE}/index.html?v=portal-pr6-inspect"

IMAGE_PATHS = (
    "assets/bg_gearwall.jpg",
    "assets/hp_app_cloud_world_kiyoshi.jpg",
    "assets/team-kiyoshi-approved-20261020.jpg",
    "assets/hp_promo_elementary_code_infographic.jpg",
    "assets/building.jpg",
)


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    report: dict = {
        "pr": 6,
        "branch": "confirm/hp-portal-2026-10-27",
        "confirm_url_local": CONFIRM,
        "index_url_local": INDEX,
        "main_merge": "未実施（社長承認待ち）",
        "assets_head": [],
        "checks": [],
    }

    import urllib.request

    for rel in IMAGE_PATHS:
        url = f"{BASE}/{rel}"
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as r:
                report["assets_head"].append(
                    {"path": rel, "status": r.status, "ok": r.status == 200}
                )
        except Exception as e:
            report["assets_head"].append(
                {"path": rel, "status": 0, "ok": False, "error": str(e)}
            )

    configs = (
        ("mac_chrome_pc1280", {"width": 1280, "height": 900}, "mac"),
        ("mac_safari_iphone390", {"width": 390, "height": 844}, "iphone"),
        ("win_chrome_pc1280", {"width": 1280, "height": 900}, "windows"),
        ("win_edge_1366", {"width": 1366, "height": 768}, "windows_edge"),
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, vp, kind in configs:
            ctx = browser.new_context(viewport=vp)
            if kind == "iphone":
                ctx = browser.new_context(
                    viewport=vp,
                    user_agent=(
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                        "Mobile/15E148 Safari/604.1"
                    ),
                )
            elif kind == "windows":
                ctx = browser.new_context(
                    viewport=vp,
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                )
            elif kind == "windows_edge":
                ctx = browser.new_context(
                    viewport=vp,
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
                    ),
                )
            else:
                ctx = browser.new_context(
                    viewport=vp,
                    user_agent=(
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                )

            page = ctx.new_page()
            page.route("**/analytics.js", lambda route: route.abort())
            page.goto(INDEX, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector("#portal", timeout=15000)

            meta = page.locator('meta[name="portal-template-version"]').get_attribute(
                "content"
            )
            title = page.title()
            outlook_n = page.locator(
                'a[href^="mailto:waseda-inspection@outlook.com"]'
            ).count()
            info_mailto_n = page.locator(
                'a[href^="mailto:info@waseda-inspection.com"]'
            ).count()

            blurb_fs = page.locator(".portal-card .blurb").first.evaluate(
                "el => getComputedStyle(el).fontSize"
            )
            blurb_lh = page.locator(".portal-card .blurb").first.evaluate(
                "el => getComputedStyle(el).lineHeight"
            )
            lead_fs = page.locator(".lead").first.evaluate(
                "el => getComputedStyle(el).fontSize"
            )
            portal_w = page.locator("#portal").evaluate(
                "el => el.getBoundingClientRect().width"
            )
            overflow_x = page.evaluate(
                "document.documentElement.scrollWidth > document.documentElement.clientWidth"
            )

            page.locator("#portal").screenshot(
                path=str(QA / f"waseda-pr6-portal-{label}.png")
            )
            page.screenshot(
                path=str(QA / f"waseda-pr6-full-{label}.png"),
                full_page=True,
            )
            ctx.close()

            report["checks"].append(
                {
                    "label": label,
                    "title": title,
                    "portal_template_version": meta,
                    "outlook_mailto_count": outlook_n,
                    "info_mailto_count": info_mailto_n,
                    "portal_blurb_font_size": blurb_fs,
                    "portal_blurb_line_height": blurb_lh,
                    "lead_font_size": lead_fs,
                    "portal_section_width_px": round(portal_w, 1),
                    "horizontal_overflow": overflow_x,
                }
            )
        browser.close()

    assets_ok = all(a["ok"] for a in report["assets_head"])
    checks_ok = all(
        c["portal_template_version"]
        in ("portal-2026-10-27-confirm", "portal-2026-10-27-live-parity")
        and c["title"].startswith("早稲田インスペクション")
        and c["outlook_mailto_count"] >= 1
        and c["info_mailto_count"] == 0
        and c["portal_blurb_font_size"] == "13px"
        and not c["horizontal_overflow"]
        for c in report["checks"]
    )
    mac_checks = [c for c in report["checks"] if "mac" in c["label"]]
    win_checks = [c for c in report["checks"] if "win" in c["label"]]
    report["mac_win_parity"] = {
        "blurb_font_size_match": len({c["portal_blurb_font_size"] for c in report["checks"]}) == 1,
        "portal_width_mac1280": next(
            (c["portal_section_width_px"] for c in mac_checks if "1280" in c["label"]),
            None,
        ),
        "portal_width_win1280": next(
            (c["portal_section_width_px"] for c in win_checks if "1280" in c["label"]),
            None,
        ),
    }

    report["pass"] = assets_ok and checks_ok and report["mac_win_parity"]["blurb_font_size_match"]

    out = QA / "waseda-portal-pr6-inspection-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("OK" if report["pass"] else "FAIL", out)
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
