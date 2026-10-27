#!/usr/bin/env python3
"""確認用: 8コマ吹き出し — 旧文字（グレー含む）完全消去後に新文案のみ"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from comic_bubble_util import replace_bubble_on_image

SRC = ROOT / "assets" / "elementary_code_correct_8panel.png"
OUT = ROOT / "assets" / "elementary_code_8panel_confirm_bubbles.png"


def main() -> None:
    base = Image.open(SRC).convert("RGBA")
    im = base.copy()

    # 各矩形は白吹き出し本文のみ（人物・イラスト・PC画面は含めない）
    bubbles: list[tuple[tuple[int, int, int, int], str, int]] = [
        ((20, 198, 302, 328), "時間の考え方は\nあとでAI CODEと\nつながるよ。\n②のMac時計とは\n別の話だよ。", 14),
        ((346, 198, 638, 290), "Macの中の時計は\n100分の1秒まで\nいつも表示しているよ", 14),
        ((672, 198, 912, 372), "発注の瞬間の\n世界時刻から\n毎回ちがう\n一意のAI CODE！\n（重複防止）", 13),
        ((996, 198, 1290, 388), "公式サーバーが\n発注ごとに固有の\nAI CODEを付ける。\n同時に来ても\n重ならない（一意性）", 13),
        (
            (20, 644, 304, 834),
            "氏名・住所・身分証の\n登録は不要！\nAI CODEと登録\nデバイスで接続前\nに認証するよ",
            12,
        ),
        (
            (346, 644, 638, 846),
            "人手非介在：\nサーバーが自動照合。\n人が都度OKしたり\n認証番号を入力する\n必要はない",
            12,
        ),
        (
            (670, 692, 962, 912),
            "なりすまし・重複を\n防ぐ仕組み。\n目標：毎秒1,000組\nの認証（設計中）。\n世界最速とは断定しない",
            11,
        ),
        (
            (996, 636, 1292, 1008),
            "個人情報を晒さず\n接続前に安全に\nつなぐ未来へ！\nAIといっしょに\nがんばろう！",
            11,
        ),
    ]

    for box, text, max_font in bubbles:
        replace_bubble_on_image(base, im, box, text, max_font=max_font)

    im.save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
