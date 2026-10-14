"""Flavour pack fronts and backs.

Same layout on every flavour, a different bright/dark pair, and a line drawing.
The drawings follow the Toundra icon style: one even stroke, round caps, no fill.
The back carries the ingredient list, allergens, and a calculated nutrition panel.
"""

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_wordmark

ROOT = Path(__file__).resolve().parent
FONT = ROOT / "fonts"
OUT = ROOT / "explorations" / "flavours"
STROKE = 14

# Bright field-colour and dark ink, one pair per flavour.
# Same roles as the house purple: light type on a dark pack.
# Ingredient runs are (text, Manrope weight). Allergen names are the bold runs.
FLAVOURS = [
    {
        "id": "butter",
        "name": "Salted Butter",
        "light": (255, 214, 64),
        "dark": (74, 48, 0),
        "ingredients": [
            ("Cultured butterfat (", 500),
            ("milk", 800),
            ("), salt.", 500),
        ],
        "contains": [("Contains: ", 800), ("milk", 800), (".", 800)],
    },
    {
        "id": "raspberry",
        "name": "Raspberry",
        "light": (255, 70, 122),
        "dark": (70, 8, 32),
        "ingredients": [
            (
                "Raspberries, sugar, lemon juice. Made with 150 g of raspberries per 100 g.",
                500,
            ),
        ],
        "contains": [],
    },
    {
        "id": "yeast",
        "name": "Yeast extract",
        "light": (226, 75, 255),
        "dark": (59, 7, 100),
        "ingredients": [
            ("Yeast extract (80%), barley malt extract (", 500),
            ("barley", 800),
            ("), salt, vegetable concentrate.", 500),
        ],
        "contains": [("Contains: ", 800), ("barley", 800), (" (gluten).", 800)],
    },
    {
        "id": "peanut",
        "name": "Peanut",
        "light": (255, 140, 48),
        "dark": (78, 36, 8),
        "ingredients": [("Peanuts (96%), vegetable fat, salt.", 500)],
        "contains": [("Contains: ", 800), ("peanuts", 800), (".", 800)],
    },
]

FACILITY = "Made in a facility that handles milk and peanuts."
RADIUS = 64


def font(weight: int, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT / f"Manrope-{weight}.ttf"), size)


def svg_wrap(body: str, w: int = 640, h: int = 360) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'fill="none" stroke="#000" stroke-width="{STROKE}" '
        f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
    )


def icon_butter() -> str:
    # Scored butter block. The ground line is the bottom edge, so the two strokes do not double.
    return svg_wrap(
        """
        <line x1="88" y1="292" x2="552" y2="292"/>
        <path d="M168 292 V152 A28 28 0 0 1 196 124 H416 A28 28 0 0 1 444 152 V292"/>
        <line x1="270" y1="124" x2="270" y2="214"/>
        <line x1="372" y1="124" x2="372" y2="214"/>
        <path d="M112 108 l16 -26 l16 26 l-16 26 z"/>
        <path d="M492 86 l14 -22 l14 22 l-14 22 z"/>
        <path d="M534 140 l11 -18 l11 18 l-11 18 z"/>
        """
    )


def icon_raspberry() -> str:
    # Pyramid of drupelets sitting on the ground line, plus one leaf.
    # Circles stay separate and only just touch, so the cluster does not turn into a flower.
    circles = [
        (320, 164, 20),
        (286, 208, 26),
        (354, 208, 26),
        (258, 258, 28),
        (320, 264, 28),
        (382, 258, 28),
    ]
    dots = "\n".join(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>' for cx, cy, r in circles)
    leaf = """
        <path d="M314 150 C292 118 248 112 240 140 C268 128 292 134 316 154"/>
        <line x1="312" y1="150" x2="252" y2="126"/>
        <line x1="88" y1="292" x2="552" y2="292"/>
    """
    return svg_wrap(dots + leaf)


def icon_stampmite() -> str:
    # Two barley ears. Geometric grains, no jar silhouette.
    def ear(cx: int) -> str:
        parts = [f'<line x1="{cx}" y1="48" x2="{cx}" y2="292"/>']
        for i, y in enumerate(range(78, 268, 28)):
            side = -1 if i % 2 == 0 else 1
            grain = 22 - i
            parts.append(
                f'<ellipse cx="{cx + side * 26}" cy="{y}" rx="{grain}" ry="12" '
                f'transform="rotate({side * -38} {cx + side * 26} {y})"/>'
            )
        parts.append(f'<path d="M{cx - 6} 58 l-20 -24 M{cx + 6} 58 l20 -24"/>')
        return "\n".join(parts)

    return svg_wrap(ear(230) + ear(410) + '<line x1="88" y1="292" x2="552" y2="292"/>')


def _peanut(cx: int, cy: int, scale: float) -> str:
    # Horizontal shell: two lobes and a waist, the usual peanut drawing.
    shell = (
        '<path d="M-96 6 '
        'C-96 -30 -58 -42 -28 -26 '
        'C-12 -16 -2 -16 14 -24 '
        'C52 -44 104 -22 104 12 '
        'C104 40 62 48 26 34 '
        'C10 26 0 26 -14 34 '
        'C-50 48 -96 36 -96 6 Z"/>'
        '<path d="M-6 -22 C2 -6 4 10 0 30"/>'
    )
    return f'<g transform="translate({cx} {cy}) scale({scale})">{shell}</g>'


def icon_peanut() -> str:
    return svg_wrap(
        _peanut(220, 236, 1.05)
        + _peanut(455, 248, 0.72)
        + '<line x1="88" y1="292" x2="552" y2="292"/>'
    )


ICONS = {
    "butter": icon_butter,
    "raspberry": icon_raspberry,
    "yeast": icon_stampmite,
    "peanut": icon_peanut,
}


def sig3(value: float) -> float:
    """Round to at most three significant figures, the nutrition-panel rule."""
    if value == 0:
        return 0
    import math

    power = math.floor(math.log10(abs(value)))
    factor = 10 ** (power - 2)
    return round(value / factor) * factor


def gram(value: float) -> str:
    if value < 0.05:
        return "0 g"
    return f"{value:.1f} g"


def milligram(value: float) -> str:
    if value < 5:
        return "<5 mg"
    return f"{round(value)} mg"


def panels() -> None:
    """Fill each flavour's nutrition rows from the industrial proportions.

    Butter is 97.5 g cultured butterfat and 2.5 g salt per 100 g. Saturated
    fat uses the share in Anchor salted butter (49.1 g of 81.4 g fat).
    Raspberry is the home cook scaled to 100 g of finished paste.
    Yeast extract is 80 g yeast-extract paste, 15.5 g barley malt extract,
    2.5 g salt, and 2 g vegetable concentrate. Peanut is 96 g roasted peanuts,
    2.3 g hard vegetable fat, and 1.7 g salt.
    """
    # name, per 100 g: energy kJ, protein, fat, sat, carb, sugars, fibre, sodium mg
    raw = {
        "butter": (97.5 * 37, 0, 97.5, 97.5 * (49.1 / 81.4), 0, 0, 0, 2.5 * 393),
        "raspberry": raspberry_panel(),
        "yeast": yeast_panel(),
        "peanut": peanut_panel(),
    }
    labels = [
        ("Energy", 0, "kj"),
        ("Protein", 1, "g"),
        ("Fat, total", 2, "g"),
        ("– saturated", 3, "g"),
        ("Carbohydrate", 4, "g"),
        ("– sugars", 5, "g"),
        ("Dietary fibre", 6, "g"),
        ("Sodium", 7, "mg"),
    ]
    for flavour in FLAVOURS:
        energy, protein, fat, sat, carb, sugars, fibre, sodium = raw[flavour["id"]]
        energy = sig3(energy)
        values = (energy, protein, fat, sat, carb, sugars, fibre, sodium)
        rows = []
        for name, index, unit in labels:
            total = values[index]
            serve = total / 10
            if unit == "kj":
                shown = (f"{round(serve)} kJ", f"{round(total)} kJ")
            elif unit == "mg":
                shown = (milligram(serve), milligram(total))
            else:
                shown = (gram(serve), gram(total))
            rows.append((name, *shown))
        flavour["nutrition"] = rows
        print(flavour["id"], rows)


def raspberry_panel() -> tuple:
    # 120 g raspberries, 30 g sugar, 5 g lemon juice, cooked down to 80 g.
    # Raspberry and lemon figures are per 100 g of the raw ingredient.
    raspberry = (1.20, 0.65, 0.019, 5.44, 4.42, 6.5, 0.001)
    lemon = (0.35, 0.24, 0.04, 6.60, 2.52, 0.3, 0.001)
    protein = fat = sat = carb = sugars = fibre = sodium = 0.0
    for grams, profile in ((120, raspberry), (5, lemon)):
        share = grams / 100
        protein += profile[0] * share
        fat += profile[1] * share
        sat += profile[2] * share
        carb += profile[3] * share
        sugars += profile[4] * share
        fibre += profile[5] * share
        sodium += profile[6] * share
    carb += 30
    sugars += 30
    scale = 100 / 80
    protein, fat, sat, carb, sugars, fibre, sodium = (
        n * scale for n in (protein, fat, sat, carb, sugars, fibre, sodium)
    )
    sodium *= 1000
    energy = protein * 17 + fat * 37 + carb * 17 + fibre * 8
    return energy, protein, fat, sat, carb, sugars, fibre, sodium


def yeast_panel() -> tuple:
    # Per 100 g of each ingredient: protein, fat, sat, carb, sugars, fibre, sodium g.
    # Yeast-extract paste: protein 27.8 g and carbohydrate 11.8 g, of which about
    # 2 g is fibre, from a published paste profile. Sodium is dried yeast extract
    # at 3.6 g, scaled to a paste with 37% moisture.
    yeast = (27.8, 0.4, 0.1, 9.8, 1.5, 2.0, 2.27)
    malt = (4.3, 0.5, 0.1, 74.0, 55.2, 1.5, 0.020)
    veg = (4.32, 0.47, 0.06, 14.8, 12.2, 4.1, 0.059)
    protein = fat = sat = carb = sugars = fibre = sodium = 0.0
    for grams, profile in ((80, yeast), (15.5, malt), (2, veg)):
        share = grams / 100
        protein += profile[0] * share
        fat += profile[1] * share
        sat += profile[2] * share
        carb += profile[3] * share
        sugars += profile[4] * share
        fibre += profile[5] * share
        sodium += profile[6] * share
    sodium += 2.5 * 0.393
    sodium *= 1000
    energy = protein * 17 + fat * 37 + carb * 17 + fibre * 8
    return energy, protein, fat, sat, carb, sugars, fibre, sodium


def peanut_panel() -> tuple:
    # Roasted peanuts follow the published Fix & Fogg smooth panel, which is
    # 99.95% peanuts, with that pinch of salt removed before we add our own.
    # Hard vegetable fat is taken as fully fat, 70% saturated.
    scale = 96 / 100
    protein = 26.9 * scale
    fat = 46.0 * scale + 2.3
    sat = 5.9 * scale + 2.3 * 0.70
    carb = 15.6 * scale
    sugars = 5.5 * scale
    fibre = 7.7 * scale
    sodium = 1.7 * 393
    energy = 2486 * scale + 2.3 * 37
    return energy, protein, fat, sat, carb, sugars, fibre, sodium


def render_svg(svg: str, width: int, name: str) -> Image.Image:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.svg"
    png = OUT / f"{name}-ink.png"
    path.write_text(svg)
    subprocess.check_call(
        ["magick", "-background", "none", str(path), "-resize", f"{width}x", f"PNG32:{png}"]
    )
    return Image.open(png).convert("RGBA")


def recolor(image: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y][3]:
                pixels[x, y] = (*rgb, pixels[x, y][3])
    return image


def wordmark(width: int) -> Image.Image:
    build_wordmark.main()
    png = ROOT / "explorations" / "wordmark-ink.png"
    subprocess.check_call(
        [
            "magick",
            "-background",
            "none",
            str(ROOT / "wordmark.svg"),
            "-resize",
            f"{width}x",
            f"PNG32:{png}",
        ]
    )
    return Image.open(png).convert("RGBA")


def text_center(draw, y, text, face, fill, canvas_w) -> int:
    # box[3] is the ink bottom measured from the draw point, so the next line clears the letters.
    box = draw.textbbox((0, 0), text, font=face)
    w = box[2] - box[0]
    draw.text(((canvas_w - w) / 2, y), text, font=face, fill=fill)
    return box[3]


def round_corners(image: Image.Image, radius: int = RADIUS) -> Image.Image:
    image = image.convert("RGBA")
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, image.width - 1, image.height - 1), radius=radius, fill=255
    )
    image.putalpha(mask)
    return image


def draw_right(draw, right_x, y, text, face, fill) -> None:
    width = draw.textlength(text, font=face)
    draw.text((right_x - width, y), text, font=face, fill=fill)


def draw_runs(draw, runs, x, y, max_w, fill, size, line_h) -> int:
    cursor_x = x
    for text, weight in runs:
        face = font(weight, size)
        parts = text.split(" ")
        for index, part in enumerate(parts):
            token = part if index == 0 else " " + part
            if token == "":
                continue
            width = draw.textlength(token, font=face)
            if cursor_x > x and cursor_x + width > x + max_w:
                y += line_h
                cursor_x = x
                token = token.lstrip()
                width = draw.textlength(token, font=face)
            draw.text((cursor_x, y), token, font=face, fill=fill)
            cursor_x += width
    return y + line_h


def pack_image(flavour: dict, mark: Image.Image) -> Image.Image:
    w, h = 1200, 1600
    bar = 168
    light, dark = flavour["light"], flavour["dark"]
    canvas = Image.new("RGB", (w, h), dark)
    draw = ImageDraw.Draw(canvas)
    sprite = recolor(mark, light)
    x = (w - sprite.width) // 2
    canvas.paste(sprite, (x, 108), sprite)
    y = 108 + sprite.height + 36
    meta_h = text_center(
        draw, y, "80 g    ·    8 stamps    ·    12 months", font(600, 30), light, w
    )
    icon = recolor(render_svg(ICONS[flavour["id"]](), 720, flavour["id"]), light)
    name_face = font(800, 84)
    sub_face = font(500, 44)
    name_h = draw.textbbox((0, 0), flavour["name"], font=name_face)[3]
    sub_h = draw.textbbox((0, 0), "spread", font=sub_face)[3]
    block = icon.height + 24 + name_h + 12 + sub_h
    region_top = y + meta_h + 28
    region_bot = h - bar
    icon_y = region_top + (region_bot - region_top - block) / 2
    canvas.paste(icon, ((w - icon.width) // 2, int(icon_y)), icon)
    name_y = int(icon_y) + icon.height + 24
    text_center(draw, name_y, flavour["name"], name_face, light, w)
    text_center(draw, name_y + name_h + 12, "spread", sub_face, light, w)
    draw.rectangle((0, h - bar, w, h), fill=light)
    tag = font(800, 46)
    box = draw.textbbox((0, 0), "Peel. Press. Toast.", font=tag)
    th = box[3] - box[1]
    text_center(draw, h - bar + (bar - th) / 2 - 6, "Peel. Press. Toast.", tag, dark, w)
    return round_corners(canvas)


def back_image(flavour: dict, mark: Image.Image) -> Image.Image:
    w, h = 1200, 1600
    bar = 136
    pad = 76
    light, dark = flavour["light"], flavour["dark"]
    canvas = Image.new("RGB", (w, h), dark)
    draw = ImageDraw.Draw(canvas)
    max_w = w - pad * 2
    sprite = recolor(mark, light)
    canvas.paste(sprite, ((w - sprite.width) // 2, 48), sprite)
    y = 48 + sprite.height + 18
    name_h = text_center(draw, y, flavour["name"], font(800, 60), light, w)
    y += name_h + 10
    y += text_center(draw, y, "spread", font(500, 32), light, w) + 18
    icon = recolor(render_svg(ICONS[flavour["id"]](), 300, flavour["id"] + "-mini"), light)
    canvas.paste(icon, ((w - icon.width) // 2, int(y)), icon)
    y += icon.height + 12
    draw.text((pad, y), "INGREDIENTS", font=font(800, 26), fill=light)
    y += 38
    y = draw_runs(draw, flavour["ingredients"], pad, y, max_w, light, 28, 38)
    y += 4
    if flavour["contains"]:
        y = draw_runs(draw, flavour["contains"], pad, y, max_w, light, 28, 38)
    y = draw_runs(draw, [(FACILITY, 500)], pad, y, max_w, light, 28, 38)
    y += 18
    draw.text((pad, y), "NUTRITION INFORMATION", font=font(800, 26), fill=light)
    y += 40
    info = font(500, 26)
    draw.text((pad, y), "Servings per package: 8", font=info, fill=light)
    y += 34
    draw.text((pad, y), "Serving size: 10 g", font=info, fill=light)
    y += 42
    head = font(700, 24)
    right_100 = w - pad
    right_serve = w - pad - 280
    draw_right(draw, right_serve, y, "Per serving", head, light)
    draw_right(draw, right_100, y, "Per 100 g", head, light)
    y += 36
    draw.line((pad, y, right_100, y), fill=light, width=2)
    y += 12
    row_face = font(500, 26)
    for name, per, hundred in flavour["nutrition"]:
        indent = 24 if name.startswith("–") else 0
        draw.text((pad + indent, y), name, font=row_face, fill=light)
        draw_right(draw, right_serve, y, per, row_face, fill=light)
        draw_right(draw, right_100, y, hundred, row_face, fill=light)
        y += 36
    y += 8
    draw.line((pad, y, right_100, y), fill=light, width=2)
    footer = (
        "Store in a cool, dry pantry.",
        "Best before 30 SEP 2027   ·   Lot L260930",
        "Stamp, Auckland, New Zealand",
        "Net 80 g",
    )
    footer_top = h - bar - 36 - 34 * len(footer)
    if y + 16 > footer_top:
        print("back overflow", flavour["id"], y, footer_top)
    y = footer_top
    for line in footer:
        draw.text((pad, y), line, font=info, fill=light)
        y += 34
    draw.rectangle((0, h - bar, w, h), fill=light)
    tag = font(800, 40)
    box = draw.textbbox((0, 0), "Peel. Press. Toast.", font=tag)
    th = box[3] - box[1]
    text_center(draw, h - bar + (bar - th) / 2 - 4, "Peel. Press. Toast.", tag, dark, w)
    return round_corners(canvas)


def contact(images: list[Image.Image], path: Path, columns: int = 2) -> None:
    thumb_w = 520
    gap = 28
    thumbs = [
        image.resize((thumb_w, int(thumb_w * image.height / image.width)), Image.Resampling.LANCZOS)
        for image in images
    ]
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (thumb_w * columns + gap * (columns + 1), thumbs[0].height * rows + gap * (rows + 1)),
        (236, 232, 228),
    )
    for i, thumb in enumerate(thumbs):
        col, row = i % columns, i // columns
        sheet.paste(thumb, (gap + col * (thumb_w + gap), gap + row * (thumb.height + gap)), thumb)
    sheet.save(path)
    print("wrote", path)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    panels()
    mark = wordmark(980)
    mark_back = wordmark(560)
    fronts, backs = [], []
    for flavour in FLAVOURS:
        front = pack_image(flavour, mark)
        back = back_image(flavour, mark_back)
        front_path = OUT / f"{flavour['id']}.png"
        back_path = OUT / f"{flavour['id']}-back.png"
        front.save(front_path)
        back.save(back_path)
        fronts.append(front)
        backs.append(back)
        print("wrote", front_path)
        print("wrote", back_path)
    for stale in OUT.glob("stampmite*"):
        stale.unlink()
        print("removed", stale)
    contact(fronts, ROOT / "explorations" / "flavour-packs.png")
    contact(backs, ROOT / "explorations" / "flavour-backs.png")


if __name__ == "__main__":
    main()
