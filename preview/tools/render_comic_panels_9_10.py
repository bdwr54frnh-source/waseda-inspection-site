#!/usr/bin/env python3
"""確認用 ⑨⑩: 独立2コマ（正本の全身キャラ＋吹き出しのみ · 切れ端なし）"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from comic_bubble_util import fit_font, load_font

SRC = ROOT / "assets" / "elementary_code_correct_8panel.png"
OUT = ROOT / "assets" / "elementary_code_panels_9_10_confirm.png"

W = 1312
H = 580
TILE_W = W // 2
BLUE = (45, 110, 185)
BLUE_DARK = (30, 75, 140)
PANEL_BG = (245, 249, 255)


def draw_header(draw: ImageDraw.ImageDraw, ox: int, num: int, title: str) -> None:
    x0, x1 = ox + 8, ox + TILE_W - 8
    draw.rounded_rectangle((x0, 6, x1, 50), radius=12, outline=BLUE, width=2, fill=(235, 245, 255))
    draw.ellipse((x0 + 12, 12, x0 + 46, 46), fill=BLUE)
    draw.text((x0 + 29, 28), str(num), font=load_font(18), fill=(255, 255, 255), anchor="mm")
    draw.text((x0 + 56, 28), title, font=load_font(16), fill=BLUE_DARK, anchor="lm")


def draw_panel(
    canvas: Image.Image,
    ox: int,
    num: int,
    title: str,
    char_src: tuple[int, int, int, int],
    bubble_text: str,
    max_font: int,
) -> None:
    base = Image.open(SRC).convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    x0, x1 = ox + 8, ox + TILE_W - 8
    y0, y1 = 54, H - 6
    draw.rounded_rectangle((x0, y0, x1, y1), radius=14, outline=BLUE, width=3, fill=PANEL_BG)
    draw_header(draw, ox, num, title)

    char = base.crop(char_src).convert("RGBA")
    ch = min(220, y1 - y0 - 200)
    cw = int(char.width * (ch / char.height))
    char = char.resize((cw, ch), Image.Resampling.LANCZOS)
    px = x0 + (x1 - x0 - cw) // 2
    py = y0 + 56
    canvas.paste(char, (px, py), char)

    bubble = (x0 + 18, y1 - 188, x1 - 18, y1 - 22)
    draw.rounded_rectangle(bubble, radius=14, fill=(255, 255, 255), outline=(190, 210, 235), width=2)
    font = fit_font(draw, bubble_text, bubble, max_size=max_font, min_size=10)
    draw.multiline_text(
        (bubble[0] + 12, bubble[1] + 10),
        bubble_text,
        font=font,
        fill=(30, 30, 50),
        spacing=4,
    )


def main() -> None:
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((2, 2, W - 2, H - 2), radius=16, outline=BLUE, width=3)

    draw_panel(
        canvas,
        0,
        9,
        "検証した事実（参考測定）",
        (1010, 88, 1185, 268),
        "2026年10月10日\n（メモリ内 · 参考）\n25桁・30桁 各10万件\n生成サンプル内\n重複0件を確認。\n通信・端末間認証は\n含まない（公開資料）",
        13,
    )
    draw_panel(
        canvas,
        TILE_W,
        10,
        "世界の方式（確認範囲）",
        (720, 88, 895, 268),
        "Google型ログイン例：\nメール・電話等で\nアカウント確認。\n\nELEMENTARY CODE：\n登録不要 · AI CODE\n＋登録デバイスで\n接続前認証。\n\n条件が違うので\n世界最速とは断定しない。",
        11,
    )

    canvas.save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
