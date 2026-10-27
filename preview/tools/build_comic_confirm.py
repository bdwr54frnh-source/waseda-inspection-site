#!/usr/bin/env python3
"""確認用漫画 PNG を一括生成（8コマ吹き出し + ⑨⑩）"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def main() -> None:
    for name in ("render_comic_bubble_text.py", "render_comic_panels_9_10.py", "verify_comic_ink.py"):
        r = subprocess.run([sys.executable, str(TOOLS / name)], check=False)
        if r.returncode != 0:
            raise SystemExit(r.returncode)
    print("build_comic_confirm: ok")


if __name__ == "__main__":
    main()
