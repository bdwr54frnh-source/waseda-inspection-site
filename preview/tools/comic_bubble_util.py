"""吹き出し内の旧文字を完全消去してから新文案を描画"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
WHITE_THRESH = 615
INK_THRESH = 248


def load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size=size, index=0)


def bubble_fill_color(bpx, box: tuple[int, int, int, int]) -> tuple[int, int, int]:
    x0, y0, x1, y1 = box
    samples = [
        bpx[x, y][:3]
        for y in range(y0, y1)
        for x in range(x0, x1)
        if bpx[x, y][0] + bpx[x, y][1] + bpx[x, y][2] >= WHITE_THRESH
    ]
    if not samples:
        return (255, 255, 255)
    return (
        sum(c[0] for c in samples) // len(samples),
        sum(c[1] for c in samples) // len(samples),
        sum(c[2] for c in samples) // len(samples),
    )


def _should_clear_manga_text(rgb: tuple[int, ...]) -> bool:
    r, g, b = rgb
    s = r + g + b
    if s >= WHITE_THRESH or s < INK_THRESH:
        return True
    if max(r, g, b) - min(r, g, b) < 28 and s < 585:
        return True
    return False


def obliterate_bubble_area(
    bpx,
    ipx,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int],
) -> None:
    """矩形内の白地と旧セリフ（グレー字含む）を消す。カラーイラストは残す。"""
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            rgb = bpx[x, y][:3]
            if is_illustration_pixel(rgb):
                continue
            if _should_clear_manga_text(rgb):
                a = bpx[x, y][3] if len(bpx[x, y]) > 3 else 255
                ipx[x, y] = (*fill, a)


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    max_size: int = 15,
    min_size: int = 9,
) -> ImageFont.FreeTypeFont:
    x0, y0, x1, y1 = box
    max_w, max_h = (x1 - x0 - 16), (y1 - y0 - 14)
    for size in range(max_size, min_size - 1, -1):
        font = load_font(size)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=3)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if tw <= max_w and th <= max_h:
            return font
    return load_font(min_size)


def replace_bubble_on_image(
    base: Image.Image,
    im: Image.Image,
    box: tuple[int, int, int, int],
    text: str,
    max_font: int = 14,
    inset: tuple[int, int] = (10, 8),
) -> None:
    bpx = base.load()
    ipx = im.load()
    fill = bubble_fill_color(bpx, box)
    obliterate_bubble_area(bpx, ipx, box, fill)
    obliterate_bubble_area(bpx, ipx, box, fill)
    draw = ImageDraw.Draw(im)
    font = fit_font(draw, text, box, max_size=max_font)
    x0, y0, _, _ = box
    draw.multiline_text((x0 + inset[0], y0 + inset[1]), text, font=font, fill=(30, 30, 50), spacing=3)


def replace_bubble_on_crop(
    base_crop: Image.Image,
    crop: Image.Image,
    box: tuple[int, int, int, int],
    text: str,
    max_font: int = 14,
) -> None:
    replace_bubble_on_image(base_crop, crop, box, text, max_font=max_font)


def is_illustration_pixel(rgb: tuple[int, ...]) -> bool:
    r, g, b = rgb
    s = r + g + b
    if s >= WHITE_THRESH or s < INK_THRESH:
        return False
    if g > r + 18 and g > b + 10 and g > 95:
        return True
    if b > r + 15 and b > g and b > 110:
        return True
    if r > 175 and g > 120 and b > 95 and r >= g:
        return True
    if r > 210 and g > 180 and b > 150:
        return True
    return False


def scrub_text_keep_art(base: Image.Image, im: Image.Image) -> None:
    """コマ内の旧セリフ・ラベルを消し、イラスト色だけ残す（⑨⑩用）。"""
    bpx, ipx = base.load(), im.load()
    w, h = base.size
    fill = (255, 255, 255)
    for y in range(h):
        for x in range(w):
            rgb = bpx[x, y][:3]
            s = rgb[0] + rgb[1] + rgb[2]
            if is_illustration_pixel(rgb):
                continue
            if s >= WHITE_THRESH or s < INK_THRESH:
                ipx[x, y] = (*fill, 255)
