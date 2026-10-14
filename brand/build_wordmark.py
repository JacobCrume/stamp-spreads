"""STAMP wordmark in the Toundra lettering system.

The Toundra wordmark is a custom drawing, not a retail font. These capitals
follow its measured construction: cap height 338, stem 110, counter 20,
semicircular outer arches, round feet. Manrope is the text face and is not
used for the wordmark.

Output is one filled even-odd path, all capitals.
"""

from pathlib import Path

INK = "#3B0764"
CAP = 338
STEM = 110
GAP = 20
TRACK = 18

OUT = Path(__file__).resolve().parent / "wordmark.svg"


def pill(cx, top, bot, half):
    """Closed vertical capsule. half is the radius (half the width)."""
    return (
        f"M {cx - half:.1f} {top + half:.1f} "
        f"A {half:.1f} {half:.1f} 0 0 1 {cx + half:.1f} {top + half:.1f} "
        f"L {cx + half:.1f} {bot - half:.1f} "
        f"A {half:.1f} {half:.1f} 0 0 1 {cx - half:.1f} {bot - half:.1f} Z"
    )


def letter_s():
    """Upright capital S. Horizontal arms with round ends, counters are straight slots.

    The earlier two-arc S curled at the terminals and read as a twist.
    """
    w = 250
    arm = 96.0
    gap = 24.0
    raw = 3 * arm + 2 * gap
    scale = CAP / raw
    arm *= scale
    gap *= scale
    r = arm / 2
    rg = gap / 2
    y1 = arm
    y2 = arm + gap
    y3 = y2 + arm
    y4 = y3 + gap
    y5 = CAP
    # Notch sits just inside a 110-wide stem, same stem as the other capitals.
    cx_u = STEM + rg
    cx_l = w - STEM - rg
    d = (
        f"M {r:.1f} 0 "
        f"H {w - r:.1f} "
        f"A {r:.1f} {r:.1f} 0 0 1 {w - r:.1f} {y1:.1f} "
        f"H {cx_u:.1f} "
        f"A {rg:.1f} {rg:.1f} 0 0 0 {cx_u:.1f} {y2:.1f} "
        f"H {w - r:.1f} "
        f"A {r:.1f} {r:.1f} 0 0 1 {w:.1f} {y2 + r:.1f} "
        f"V {y5 - r:.1f} "
        f"A {r:.1f} {r:.1f} 0 0 1 {w - r:.1f} {y5:.1f} "
        f"H {r:.1f} "
        f"A {r:.1f} {r:.1f} 0 0 1 {r:.1f} {y4:.1f} "
        f"H {cx_l:.1f} "
        f"A {rg:.1f} {rg:.1f} 0 0 0 {cx_l:.1f} {y3:.1f} "
        f"H {r:.1f} "
        f"A {r:.1f} {r:.1f} 0 0 1 0 {y3 - r:.1f} "
        f"V {r:.1f} "
        f"A {r:.1f} {r:.1f} 0 0 1 {r:.1f} 0 Z"
    )
    return w, "fill", d


def letter_t():
    # Capital T: a round-ended bar on a round-footed stem.
    bar_h = 78
    width = 250
    stem_x = (width - STEM) / 2
    d = (
        f"M {bar_h / 2:.1f} 0 "
        f"H {width - bar_h / 2:.1f} "
        f"A {bar_h / 2:.1f} {bar_h / 2:.1f} 0 0 1 {width - bar_h / 2:.1f} {bar_h:.1f} "
        f"H {stem_x + STEM:.1f} "
        f"V {CAP - STEM / 2:.1f} "
        f"A {STEM / 2:.1f} {STEM / 2:.1f} 0 0 1 {stem_x:.1f} {CAP - STEM / 2:.1f} "
        f"V {bar_h:.1f} "
        f"H {bar_h / 2:.1f} "
        f"A {bar_h / 2:.1f} {bar_h / 2:.1f} 0 0 1 {bar_h / 2:.1f} 0 Z"
    )
    return width, "fill", d


def letter_a():
    # Arch, closed pill counter, opening between the feet.
    w = 240
    r_top = w / 2
    r_foot = STEM / 2
    notch_top = 214
    d = (
        f"M 0 {r_top:.1f} "
        f"A {r_top:.1f} {r_top:.1f} 0 0 1 {w:.1f} {r_top:.1f} "
        f"L {w:.1f} {CAP - r_foot:.1f} "
        f"A {r_foot:.1f} {r_foot:.1f} 0 0 1 {w - STEM:.1f} {CAP - r_foot:.1f} "
        f"L {w - STEM:.1f} {notch_top + GAP / 2:.1f} "
        f"A {GAP / 2:.1f} {GAP / 2:.1f} 0 0 0 {STEM:.1f} {notch_top + GAP / 2:.1f} "
        f"L {STEM:.1f} {CAP - r_foot:.1f} "
        f"A {r_foot:.1f} {r_foot:.1f} 0 0 1 0 {CAP - r_foot:.1f} Z "
        + pill(w / 2, 78, 176, GAP / 2)
    )
    return w, "fill", d


def letter_n():
    """Arch with the counter open at the baseline. Width 240."""
    w = STEM * 2 + GAP
    r_top = w / 2
    r_foot = STEM / 2
    return (
        f"M 0 {r_top:.1f} "
        f"A {r_top:.1f} {r_top:.1f} 0 0 1 {w:.1f} {r_top:.1f} "
        f"L {w:.1f} {CAP - r_foot:.1f} "
        f"A {r_foot:.1f} {r_foot:.1f} 0 0 1 {w - STEM:.1f} {CAP - r_foot:.1f} "
        f"L {w - STEM:.1f} 74 "
        f"A {GAP / 2:.1f} {GAP / 2:.1f} 0 0 0 {STEM:.1f} 74 "
        f"L {STEM:.1f} {CAP - r_foot:.1f} "
        f"A {r_foot:.1f} {r_foot:.1f} 0 0 1 0 {CAP - r_foot:.1f} Z"
    )


def letter_m():
    # Two of those arches sharing the middle stem.
    shift = STEM + GAP
    w = shift + STEM * 2 + GAP
    d = letter_n() + f" M {shift} 0 "  # placeholder, replaced below
    # Two subpaths, second translated by rewriting coordinates is harder,
    # so the builder special-cases M. This string is unused.
    return w, "fill", d


def letter_p():
    # Capital P. The counter is centered in the bowl: equal ink left and right,
    # and equal ink above and below. The left edge of the counter lines up
    # with the stem.
    w = STEM * 2 + 28
    bowl_bot = 176
    r_foot = STEM / 2
    r_top = 64
    r_bowl = 28
    counter_half = 14
    counter_h = 84
    top = (bowl_bot - counter_h) / 2
    d = (
        f"M 0 {r_top} "
        f"A {r_top} {r_top} 0 0 1 {r_top} 0 "
        f"H {w - r_top} "
        f"A {r_top} {r_top} 0 0 1 {w} {r_top} "
        f"V {bowl_bot - r_bowl} "
        f"A {r_bowl} {r_bowl} 0 0 1 {w - r_bowl} {bowl_bot} "
        f"H {STEM} "
        f"V {CAP - r_foot:.1f} "
        f"A {r_foot:.1f} {r_foot:.1f} 0 0 1 0 {CAP - r_foot:.1f} Z "
        + pill(w / 2, top, top + counter_h, counter_half)
    )
    return w, "fill", d


LETTERS = {
    "S": letter_s,
    "T": letter_t,
    "A": letter_a,
    "M": letter_m,
    "P": letter_p,
}


def build(word="STAMP"):
    x = 0
    parts = []
    strokes = []
    for ch in word:
        if ch == "M":
            shift = STEM + GAP
            width = shift + STEM * 2 + GAP
            n = letter_n()
            parts.append(
                f'<g transform="translate({x:.1f} 0)">{_fill(n)}</g>'
            )
            parts.append(
                f'<g transform="translate({x + shift:.1f} 0)">{_fill(n)}</g>'
            )
        else:
            width, kind, d = LETTERS[ch]()
            if kind == "fill":
                parts.append(f'<g transform="translate({x:.1f} 0)">{_fill(d)}</g>')
            else:
                strokes.append(
                    f'<path transform="translate({x:.1f} 0)" d="{d}" fill="none" '
                    f'stroke="{INK}" stroke-width="100" stroke-linecap="round" '
                    f'stroke-linejoin="round"/>'
                )
        x += width + TRACK
    total = x - TRACK
    pad_x, pad_top, pad_bot = 8, 8, 8
    height = CAP + pad_top + pad_bot
    body = f'<g transform="translate({pad_x} {pad_top})">\n' + "\n".join(parts + strokes) + "\n</g>"
    width = total + pad_x * 2
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height}" '
        f'fill="{INK}" role="img" aria-label="{word}">\n{body}\n</svg>\n'
    )
    return svg, width, height


def _fill(d):
    return f'<path d="{d}" fill-rule="evenodd"/>'


def main():
    svg, width, height = build()
    OUT.write_text(svg)
    print(f"wrote {OUT} {width:.0f}x{height:.0f}")


if __name__ == "__main__":
    main()
