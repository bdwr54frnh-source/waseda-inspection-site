#!/usr/bin/env python3
"""ロリポップへ waseda-inspection をFTPアップ。

パスワードはチャットに貼らず、Macのダイアログで直接入力する。
資格情報はファイルに保存しない。
"""

from __future__ import annotations

import ftplib
import os
import subprocess
import sys
from pathlib import Path

HOST = "ftp.lolipop.jp"
DEFAULT_USER = "fakefur.jp-windy-hiji-5291"
LOCAL = Path(__file__).resolve().parent
FILES = [
    "index.html",
    "promo_banner_airface.jpg",
    "air_face_gold_wordmark.png",
]


def mac_prompt(title: str, message: str, *, hidden: bool, default: str = "") -> str:
    hidden_clause = " with hidden answer" if hidden else ""
    # AppleScript 文字列エスケープ
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    script = f'''
tell application "System Events"
  activate
end tell
try
  set r to display dialog "{esc(message)}" default answer "{esc(default)}"{hidden_clause} with title "{esc(title)}" buttons {{"キャンセル", "OK"}} default button "OK"
  if button returned of r is "キャンセル" then return ""
  return text returned of r
on error
  return ""
end try
'''
    out = subprocess.check_output(["osascript", "-e", script], text=True)
    return out.rstrip("\n")


def connect(user: str, password: str) -> ftplib.FTP:
    errors: list[str] = []
    try:
        ftp = ftplib.FTP_TLS(HOST, timeout=45)
        ftp.login(user, password)
        try:
            ftp.prot_p()
        except Exception:
            pass
        ftp.set_pasv(True)
        print("CONNECTED: FTP_TLS")
        return ftp
    except Exception as e:
        errors.append(f"FTP_TLS: {e}")
    try:
        ftp = ftplib.FTP(HOST, timeout=45)
        ftp.login(user, password)
        ftp.set_pasv(True)
        print("CONNECTED: FTP")
        return ftp
    except Exception as e:
        errors.append(f"FTP: {e}")
    raise RuntimeError(" / ".join(errors))


def pick_target_dir(ftp: ftplib.FTP) -> None:
    try:
        names = ftp.nlst()
    except Exception:
        names = []
    print("PWD:", ftp.pwd())
    print("ROOT entries:", ", ".join(sorted(names)[:60]))

    candidates = [n for n in names if "waseda" in n.lower() or "inspection" in n.lower()]
    for guess in (
        "waseda-inspection",
        "www.waseda-inspection.com",
        "waseda-inspection.com",
        "web",
        "public_html",
        "public",
    ):
        if guess in names and guess not in candidates:
            candidates.append(guess)

    if not candidates:
        print("ターゲットフォルダが見つからないため、カレントにアップロードします。")
        return

    # 候補が複数ならダイアログで選ぶ
    if len(candidates) == 1:
        choice = candidates[0]
    else:
        choice = mac_prompt(
            "アップロード先フォルダ",
            "候補をそのまま入力（例: " + " / ".join(candidates[:5]) + "）",
            hidden=False,
            default=candidates[0],
        )
        if not choice:
            raise SystemExit("フォルダ選択がキャンセルされました。")
    print("CD:", choice)
    ftp.cwd(choice)
    print("PWD now:", ftp.pwd())


def main() -> int:
    print("Macダイアログで FTP アカウントとパスワードを入力してください（チャット不要）。")
    user = mac_prompt(
        "Air Face FTP",
        "FTPアカウント（ロリポップ画面の表記をそのまま）",
        hidden=False,
        default=DEFAULT_USER,
    )
    if not user:
        print("キャンセルされました。")
        return 2
    password = mac_prompt(
        "Air Face FTP",
        f"FTPパスワードを入力（チャットには貼らない）\nアカウント: {user}",
        hidden=True,
    )
    if not password:
        print("キャンセルされました。")
        return 2

    missing = [f for f in FILES if not (LOCAL / f).is_file()]
    if missing:
        print("ローカル不足:", missing)
        return 3

    try:
        ftp = connect(user, password)
    except Exception as e:
        print("ログイン失敗:", e)
        print("アカウント表記とパスワードをロリポップ画面で再確認して、もう一度実行してください。")
        return 1
    finally:
        password = ""  # noqa: F841 — メモリ上の参照を早めに捨てる意図

    try:
        pick_target_dir(ftp)
        for name in FILES:
            path = LOCAL / name
            print(f"UPLOAD {name} ({path.stat().st_size} bytes)")
            with path.open("rb") as fh:
                ftp.storbinary(f"STOR {name}", fh)
            print(f"  OK {name}")
        print("DONE → https://www.waseda-inspection.com/ をハードリロードしてください。")
        return 0
    finally:
        try:
            ftp.quit()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
