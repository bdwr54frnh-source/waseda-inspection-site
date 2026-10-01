#!/usr/bin/env python3
"""Push homepage branch to GitHub using Mac dialog for credentials (not chat)."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path("/Users/mac/Desktop/AirQuick_Final_3")
REMOTE_URL = "https://github.com/bdwr54frnh-source/AirQuick-Final-3.git"
BRANCH = "feature/world-airship-with-boost"


def mac_prompt(title: str, message: str, *, hidden: bool, default: str = "") -> str:
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    hidden_clause = " with hidden answer" if hidden else ""
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
    return subprocess.check_output(["osascript", "-e", script], text=True).rstrip("\n")


def main() -> int:
    user = mac_prompt(
        "GitHub Push",
        "GitHub ユーザー名（例: bdwr54frnh-source）",
        hidden=False,
        default="bdwr54frnh-source",
    )
    if not user:
        print("CANCELLED")
        return 2
    token = mac_prompt(
        "GitHub Push",
        "Personal Access Token を貼り付け（チャットには貼らない）\n権限: Contents 書き込み / リポジトリアクセス",
        hidden=True,
    )
    if not token:
        print("CANCELLED")
        return 2

    # askpass で対話プロンプトを回避
    askpass = tempfile.NamedTemporaryFile("w", delete=False, suffix=".sh")
    askpass_path = askpass.name
    user_q = user.replace("'", "'\\''")
    token_q = token.replace("'", "'\\''")
    askpass.write(
        f"""#!/bin/sh
case "$1" in
  *Username*) echo '{user_q}' ;;
  *) echo '{token_q}' ;;
esac
"""
    )
    askpass.close()
    os.chmod(askpass_path, 0o700)

    env = os.environ.copy()
    env["GIT_ASKPASS"] = askpass_path
    env["SSH_ASKPASS"] = askpass_path
    env["GIT_TERMINAL_PROMPT"] = "0"
    # リモート確認
    subprocess.run(["git", "remote", "set-url", "origin", REMOTE_URL], cwd=REPO, check=True)

    print("Fetching...")
    fetch = subprocess.run(
        ["git", "fetch", "origin"],
        cwd=REPO,
        env=env,
        text=True,
        capture_output=True,
    )
    print(fetch.stdout)
    print(fetch.stderr)
    if fetch.returncode != 0:
        print("FETCH_FAILED", fetch.returncode)
        os.unlink(askpass_path)
        token = ""
        return 1

    print("Pushing", BRANCH, "...")
    push = subprocess.run(
        ["git", "push", "-u", "origin", BRANCH],
        cwd=REPO,
        env=env,
        text=True,
        capture_output=True,
    )
    print(push.stdout)
    print(push.stderr)
    os.unlink(askpass_path)
    token = ""
    if push.returncode != 0:
        print("PUSH_FAILED", push.returncode)
        return 1
    print("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
