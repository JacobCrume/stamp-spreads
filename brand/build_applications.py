"""Flat brand applications for Stamp.

The wordmark is the only mark. The pair is dark purple on light purple,
the same relationship as Toundra's dark green on lime. Supporting type is
Manrope, the text face of that identity.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_wordmark

ROOT = Path(__file__).resolve().parent
FONT = ROOT / "fonts"
LIGHT = (226, 75, 255)  # #E24BFF, the lime's role
DARK = (59, 7, 100)  # #3B0764, the forest green's role


def font(weight: int, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT / f"Manrope-{weight}.ttf"), size)


def render_wordmark(width: int) -> Image.Image:
    build_wordmark.main()
    svg = ROOT / "wordmark.svg"
    png = ROOT / "explorations" / "wordmark-ink.png"
    png.parent.mkdir(parents=True, exist_ok=True)
    import subprocess

    subprocess.check_call(
        [
            "magick",
            "-background",
            "none",
            str(svg),
            "-resize",
            f"{width}x",
            f"PNG32:{png}",
        ]
    )
    return Image.open(png).convert("RGBA")


def recolor(image: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            _, _, _, alpha = pixels[x, y]
            if alpha:
                pixels[x, y] = (*rgb, alpha)
    return image


def paste_center(canvas: Image.Image, sprite: Image.Image, y: int) -> None:
    x = (canvas.width - sprite.width) // 2
    canvas.paste(sprite, (x, y), sprite)


def text_center(draw: ImageDraw.ImageDraw, y: int, text: str, face, fill, canvas_w: int) -> int:
    box = draw.textbbox((0, 0), text, font=face)
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text(((canvas_w - w) / 2, y), text, font=face, fill=fill)
    return h


def lockup(background, ink, width, height, mark_width, path: Path) -> None:
    canvas = Image.new("RGB", (width, height), background)
    mark = recolor(render_wordmark(mark_width), ink)
    paste_center(canvas, mark, (height - mark.height) // 2)
    canvas.save(path, quality=95)


def pack() -> None:
    w, h = 1200, 1600
    canvas = Image.new("RGB", (w, h), DARK)
    draw = ImageDraw.Draw(canvas)
    mark = recolor(render_wordmark(980), LIGHT)
    top = 120
    paste_center(canvas, mark, top)
    y = top + mark.height + 48
    meta = font(600, 32)
    meta_h = text_center(draw, y, "80 g    ·    8 stamps    ·    12 months", meta, LIGHT, w)
    bar = 180
    flavour = font(800, 92)
    sub = font(500, 44)
    name_h = draw.textbbox((0, 0), "Salted Butter", font=flavour)[3]
    sub_h = draw.textbbox((0, 0), "salted butter spread", font=sub)[3]
    block = name_h + 28 + sub_h
    region_top = y + meta_h + 36
    region_bot = h - bar
    flavour_y = region_top + (region_bot - region_top - block) / 2
    text_center(draw, flavour_y, "Salted Butter", flavour, LIGHT, w)
    text_center(draw, flavour_y + name_h + 28, "salted butter spread", sub, LIGHT, w)
    draw.rectangle((0, h - bar, w, h), fill=LIGHT)
    tag = font(800, 48)
    box = draw.textbbox((0, 0), "Peel. Press. Toast.", font=tag)
    th = box[3] - box[1]
    text_center(draw, h - bar + (bar - th) / 2 - 8, "Peel. Press. Toast.", tag, DARK, w)
    canvas.save(ROOT / "pack.png")


def ad() -> None:
    w, h = 1080, 1350
    canvas = Image.new("RGB", (w, h), LIGHT)
    draw = ImageDraw.Draw(canvas)
    mark = recolor(render_wordmark(940), DARK)
    paste_center(canvas, mark, 430)
    y = 430 + mark.height + 64
    text_center(draw, y, "Peel. Press. Toast.", font(800, 54), DARK, w)
    text_center(draw, h - 120, "Toast spreads", font(600, 28), DARK, w)
    canvas.save(ROOT / "ad.png")


def main() -> None:
    lockup(LIGHT, DARK, 1800, 1000, 1500, ROOT / "logo.png")
    lockup(DARK, LIGHT, 1800, 1000, 1500, ROOT / "explorations" / "wordmark-on-dark.png")
    pack()
    ad()
    print("wrote logo, pack, ad")


if __name__ == "__main__":
    main()
