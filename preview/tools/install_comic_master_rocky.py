#!/usr/bin/env python3
"""依頼者正本 PNG → 表示用（第2コマ含め静止画そのまま · LIVE 重ねなし）。"""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READONLY = (
    ROOT
    / "assets"
    / "originals"
    / "elementary_code_rocky_8panel_MASTER_BOY_DIALOG_2026-10-27_READONLY.png"
)
OUT = ROOT / "assets" / "elementary_code_rocky_8panel.png"
ARCHIVE = ROOT / "assets" / "elementary_code_rocky_8panel_from_master.png"


def main() -> None:
    if not READONLY.is_file():
        raise SystemExit(f"missing readonly master {READONLY}")
    hash_before = hashlib.sha256(READONLY.read_bytes()).hexdigest()
    shutil.copy2(READONLY, OUT)
    shutil.copy2(READONLY, ARCHIVE)
    if hashlib.sha256(READONLY.read_bytes()).hexdigest() != hash_before:
        raise SystemExit("readonly master was modified")
    print("OK", OUT.name, "static_copy_from_readonly")


if __name__ == "__main__":
    main()
