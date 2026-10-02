#!/usr/bin/env python3
"""assets/ 内のスクショ一覧を manifest.json に書く（HP #app-gallery 用）。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
SCREENSHOTS = ASSETS / "screenshots"
OUT = SCREENSHOTS / "manifest.json"

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
GALLERY_SKIP = {
    "founder_portrait.jpg",
    "apple_music_glass_tile_clean.jpg",
    "apple_music_glass_tile_serial.jpg",
    "apple_music_glass_tile_edited.jpg",
    "apple_music_glass_tile_source.jpg",
    "essentials_jacket_woman.png",
    "bg_gearwall.jpg",
    "team_season.jpg",
    "building.jpg",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def collect() -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(path: Path, label: str | None = None) -> None:
        key = rel(path)
        if key in seen or not path.is_file():
            return
        seen.add(key)
        items.append({"path": key, "label": label or path.name})

    if SCREENSHOTS.is_dir():
        for path in sorted(SCREENSHOTS.iterdir()):
            if path.suffix.lower() in IMAGE_EXT and path.name != "manifest.json":
                add(path)

    for path in sorted(ASSETS.iterdir()):
        if path.suffix.lower() not in IMAGE_EXT:
            continue
        name = path.name
        if name in GALLERY_SKIP:
            continue
        if name.startswith("apple_music_glass_tile_") and name not in (
            "apple_music_glass_tile_clean.jpg",
            "apple_music_glass_tile_serial.jpg",
        ):
            continue
        if name.startswith("app_screen_") or name.startswith("screenshot_"):
            add(path)

    return items


def main() -> int:
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    items = collect()
    OUT.write_text(
        json.dumps({"generated": True, "items": items}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(items)} entries → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
