#!/usr/bin/env python3
"""Generate presentation/Stamp-pitch.pptx for INFO123 Video Presentation.

Strictly adheres to:
1. Cover Slide: Almost identical to PDF Page 1 (Minimalist Deep Night Ink,
   centered STAMP wordmark, PEEL. PRESS. TOAST., and Commercial Business Pitch at the bottom).
2. Pure Flat Canvas (Zero Containers on slides):
   - No container boxes or frames cluttering the slides.
   - Clean, bold, confident typography floating on the rich background.
3. 1–3 Lines Maximum per Slide:
   - Ruthlessly cut all text.
   - Every slide delivers a single punchy statement or metric readable in 2 seconds.
4. Removed Administrative Headers:
   - No mechanical "01 / THE PROBLEM • PITCH PART 1" lines.
5. Strict 3 Colors Plus Neutral Rule across narrative sections:
   - Cover & Reflection 2: Yeast / Classic (#240340 secondary, #E24BFF primary, #FFFFFF neutral)
   - Product Innovation: Butter (#4A3000 secondary, #FFD640 primary, #FFFFFF neutral)
   - Market & Economics: Raspberry (#460820 secondary, #FF467A primary, #FFFFFF neutral)
   - Reflection 1 (Steering): Peanut (#4E2408 secondary, #FF8C30 primary, #FFFFFF neutral)
"""

from __future__ import annotations

import tempfile
from pathlib import Path
import numpy as np
from PIL import Image as PILImage
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent.parent
OUT_PPTX = ROOT / "presentation" / "Stamp-pitch.pptx"

# 4 Flavour Color Schemes strictly honoring the 3 colors + neutral rule
SCHEMES = {
    "yeast": {
        "secondary": RGBColor(36, 3, 64),    # #240340 (Deep Night Ink)
        "primary": RGBColor(226, 75, 255),   # #E24BFF (Electric Lavender)
        "white": RGBColor(255, 255, 255),
    },
    "butter": {
        "secondary": RGBColor(74, 48, 0),    # #4A3000 (Roasted Caramel Brown)
        "primary": RGBColor(255, 214, 64),   # #FFD640 (Electric Butter Gold)
        "white": RGBColor(255, 255, 255),
    },
    "raspberry": {
        "secondary": RGBColor(70, 8, 32),    # #460820 (Rich Berry)
        "primary": RGBColor(255, 70, 122),   # #FF467A (Neon Wild Raspberry)
        "white": RGBColor(255, 255, 255),
    },
    "peanut": {
        "secondary": RGBColor(78, 36, 8),    # #4E2408 (Deep Peanut Umber)
        "primary": RGBColor(255, 140, 48),   # #FF8C30 (Roasted Peanut Ochre)
        "white": RGBColor(255, 255, 255),
    },
}


def create_recolored_wordmark(src: Path, dest: Path, rgb: tuple[int, int, int]) -> tuple[int, int]:
    """Extract smooth, anti-aliased STAMP wordmark recolored to rgb."""
    img = PILImage.open(src).convert("RGBA")
    arr = np.array(img).astype(float)
    diff = np.sqrt(
        (arr[:, :, 0] - 226) ** 2
        + (arr[:, :, 1] - 75) ** 2
        + (arr[:, :, 2] - 255) ** 2
    )
    alpha = np.clip((diff - 20) / 60.0, 0, 1)
    out = np.zeros((img.height, img.width, 4), dtype=np.uint8)
    out[:, :, 0] = rgb[0]
    out[:, :, 1] = rgb[1]
    out[:, :, 2] = rgb[2]
    out[:, :, 3] = (alpha * 255).astype(np.uint8)
    res = PILImage.fromarray(out)
    bbox = res.getbbox()
    if bbox:
        pad = 20
        box = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(img.width, bbox[2] + pad),
            min(img.height, bbox[3] + pad),
        )
        cropped = res.crop(box)
    else:
        cropped = res
    cropped.save(dest, "PNG")
    return cropped.size


def create_slide_canvas(prs: pptx.Presentation, bg_color: RGBColor):
    """Full-bleed flat canvas without borders or shadows."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()
    return slide


def add_statement_slide(
    prs: pptx.Presentation,
    scheme_key: str,
    line1: str,
    line2: str,
    line3: str | None = None,
    line1_color: str = "primary",
    line2_color: str = "white",
    line3_color: str = "primary",
    line1_size: int = 22,
    line2_size: int = 46,
    line3_size: int = 22,
    notes: str = "",
):
    """Add a minimal, container-free slide with 1-3 lines of bold text."""
    s = SCHEMES[scheme_key]
    slide = create_slide_canvas(prs, s["secondary"])

    # Centered vertically in slide
    left = Inches(1.3)
    width = Inches(10.7)
    height = Inches(4.0)

    # Calculate vertical position based on number of lines
    top = Inches(2.2) if line3 else Inches(2.6)

    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p1 = tf.paragraphs[0]
    p1.text = line1
    p1.font.name = "Manrope"
    p1.font.size = Pt(line1_size)
    p1.font.bold = True
    p1.font.color.rgb = s[line1_color]
    p1.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = line2
    p2.font.name = "Manrope"
    p2.font.size = Pt(line2_size)
    p2.font.bold = True
    p2.font.color.rgb = s[line2_color]
    p2.space_after = Pt(14)

    if line3:
        p3 = tf.add_paragraph()
        p3.text = line3
        p3.font.name = "Manrope"
        p3.font.size = Pt(line3_size)
        p3.font.bold = False if line3_color == "primary" else True
        p3.font.color.rgb = s[line3_color]

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    return slide


def add_metric_slide(
    prs: pptx.Presentation,
    scheme_key: str,
    metric_number: str,
    headline: str,
    detail: str,
    notes: str = "",
):
    """Add a container-free, massive metric slide with 3 lines total."""
    s = SCHEMES[scheme_key]
    slide = create_slide_canvas(prs, s["secondary"])

    left = Inches(1.3)
    top = Inches(1.8)
    width = Inches(10.7)
    height = Inches(4.2)

    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p1 = tf.paragraphs[0]
    p1.text = metric_number
    p1.font.name = "Manrope"
    p1.font.size = Pt(80)
    p1.font.bold = True
    p1.font.color.rgb = s["primary"]
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = headline
    p2.font.name = "Manrope"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = s["white"]
    p2.space_after = Pt(12)

    p3 = tf.add_paragraph()
    p3.text = detail
    p3.font.name = "Manrope"
    p3.font.size = Pt(22)
    p3.font.bold = False
    p3.font.color.rgb = s["primary"]

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    return slide


# ---------------------------------------------------------------------------
# PRESENTATION BUILDER
# ---------------------------------------------------------------------------

def build_presentation(work_dir: Path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # -----------------------------------------------------------------------
    # SLIDE 1: Cover (Identical to PDF Page 1: Centered Wordmark, Tagline, Bottom Pitch)
    # -----------------------------------------------------------------------
    cover_mark_path = work_dir / "cover_wordmark.png"
    px_w, px_h = create_recolored_wordmark(
        ROOT / "brand" / "logo.png", cover_mark_path, (226, 75, 255)
    )

    s_yeast = SCHEMES["yeast"]
    slide1 = create_slide_canvas(prs, s_yeast["secondary"])

    # Centered Wordmark
    mark_w = Inches(5.8)
    mark_h = mark_w * (px_h / px_w)
    mark_x = (prs.slide_width - mark_w) / 2
    mark_y = Inches(2.3)
    slide1.shapes.add_picture(str(cover_mark_path), mark_x, mark_y, width=mark_w, height=mark_h)

    # Centered Tagline
    tb_tag = slide1.shapes.add_textbox(Inches(1.5), mark_y + mark_h + Inches(0.35), Inches(10.333), Inches(0.8))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = False
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "PEEL. PRESS. TOAST."
    p_tag.font.name = "Manrope"
    p_tag.font.size = Pt(28)
    p_tag.font.bold = True
    p_tag.font.color.rgb = s_yeast["primary"]
    p_tag.alignment = PP_ALIGN.CENTER

    # Centered Bottom Text
    tb_bot = slide1.shapes.add_textbox(Inches(1.5), Inches(6.4), Inches(10.333), Inches(0.6))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = False
    p_bot = tf_bot.paragraphs[0]
    p_bot.text = "Commercial Business Pitch"
    p_bot.font.name = "Manrope"
    p_bot.font.size = Pt(16)
    p_bot.font.color.rgb = s_yeast["white"]
    p_bot.alignment = PP_ALIGN.CENTER

    slide1.notes_slide.notes_text_frame.text = (
        "TITLE (0:00–0:08)\n"
        "Kia ora. I'm Jacob, and this is Stamp: a New Zealand breakfast spread innovation engineered for hot toast."
    )

    # -----------------------------------------------------------------------
    # SECTION 1: Product Innovation & Problem (Scheme: Butter)
    # -----------------------------------------------------------------------

    # Slide 2: The Problem
    add_statement_slide(
        prs,
        scheme_key="butter",
        line1="The Problem",
        line2="Jars Require Infrastructure.",
        line3="Table knives, kitchen counters, and sink washing.",
        line1_size=22,
        line2_size=48,
        line3_size=22,
        notes="PROBLEM (0:08–0:15)\nEating toast away from a full kitchen is broken.",
    )

    # Slide 3: Who Fails
    add_statement_slide(
        prs,
        scheme_key="butter",
        line1="Eating Away from Home is Broken.",
        line2="Students in halls. Commuters. Desk workers.",
        line1_color="white",
        line2_color="primary",
        line1_size=46,
        line2_size=26,
        notes="WHO FAILS (0:15–0:22)\nIn a hall, flat, or desk, nobody wants to lug a sticky 750g jar, hunt for a knife, and wash it in an office sink.",
    )

    # Slide 4: The Solution
    add_statement_slide(
        prs,
        scheme_key="butter",
        line1="The Solution",
        line2="10 g Spread Disc on Release Film.",
        line3="Peel it off. Press onto hot toast.",
        line1_size=22,
        line2_size=48,
        line3_size=22,
        notes="SOLUTION (0:22–0:28)\nStamp reinvents the format with a thin, 10-gram disc of real spread on release film.",
    )

    # Slide 5: The Thermal Melt Gesture
    add_statement_slide(
        prs,
        scheme_key="butter",
        line1="Zero Cutlery Needed.",
        line2="Residual heat melts it across the crumb in seconds.",
        line1_color="white",
        line2_color="primary",
        line1_size=48,
        line2_size=24,
        notes="MELT GESTURE (0:28–0:34)\nYou press it onto hot toast, and residual thermal energy melts it into an even spread in seconds.",
    )

    # Slide 6: Ambient Stability & Flavours
    add_statement_slide(
        prs,
        scheme_key="butter",
        line1="12-Month Ambient Life.",
        line2="Salted Butter. Raspberry. Yeast. Peanut.",
        line1_color="white",
        line2_color="primary",
        line1_size=48,
        line2_size=24,
        notes="STABILITY & RANGE (0:34–0:40)\nFour launch varieties in an 8-stamp card sheet, shelf-stable for 12 months with zero refrigeration.",
    )

    # -----------------------------------------------------------------------
    # SECTION 2: Market Opportunity & Unit Economics (Scheme: Raspberry)
    # -----------------------------------------------------------------------

    # Slide 7: Market Scale
    add_metric_slide(
        prs,
        scheme_key="raspberry",
        metric_number="$341M",
        headline="New Zealand Spreads Category.",
        detail="+24% category revenue growth (2022–2025).",
        notes="MARKET SCALE (0:40–0:46)\nCleaned supermarket scan data shows the spreads category expanded 24% to 341 million dollars.",
    )

    # Slide 8: Premium Growth
    add_metric_slide(
        prs,
        scheme_key="raspberry",
        metric_number="+29%",
        headline="Premium Tier Surging.",
        detail="Expanding from $88M to $113M NZD.",
        notes="PREMIUM GROWTH (0:46–0:52)\nPremium branded spreads surged 29% to 113 million, significantly outperforming commodity tiers.",
    )

    # Slide 9: Competitive Void
    add_metric_slide(
        prs,
        scheme_key="raspberry",
        metric_number="0 Rivals",
        headline="Across 154 Supermarket Spreads.",
        detail="Zero single-serve or utensil-free formats in New Zealand retail.",
        notes="COMPETITIVE VOID (0:52–0:58)\nAcross 154 spread products, not one offers a portion format. Jars compete on bulk weight; Stamp wins on convenience.",
    )

    # Slide 10: Unit Economics
    add_metric_slide(
        prs,
        scheme_key="raspberry",
        metric_number="$1.75 Margin",
        headline="$5.00 NZD per 8-Stamp Sheet.",
        detail="63¢ per serving on an assumed $1.50 co-packing cost.",
        notes="ECONOMICS (0:58–1:04)\nAt five dollars a sheet—63 cents a serving—we retain a strong one-seventy-five gross margin.",
    )

    # -----------------------------------------------------------------------
    # SECTION 3: Reflection 1 — AI Steering & Verification (Scheme: Peanut)
    # -----------------------------------------------------------------------

    # Slide 11: Negative Constraints
    add_statement_slide(
        prs,
        scheme_key="peanut",
        line1="Negative Constraints.",
        line2="Banning AI Marketing Hype.",
        line3="No fake certification badges. No medical health claims.",
        line1_size=22,
        line2_size=48,
        line3_size=22,
        notes="CONSTRAINTS (1:04–1:18)\nIn steering AI, I enforced strict negative prompt constraints against fake badges and health claims.",
    )

    # Slide 12: Session Partitioning
    add_statement_slide(
        prs,
        scheme_key="peanut",
        line1="Modular Sessions.",
        line2="Separating data, branding, and copy eliminated context drift.",
        line1_color="white",
        line2_color="primary",
        line1_size=48,
        line2_size=22,
        notes="PARTITIONING (1:18–1:30)\nI partitioned distinct sessions for data cleaning, branding, and copy to prevent context rot.",
    )

    # Slide 13: Turning Point
    add_statement_slide(
        prs,
        scheme_key="peanut",
        line1="Catching Butter Instability.",
        line2="AI assumed table butter could sit ambiently.",
        line3="Human intervention forced dairy spread reformulation.",
        line1_color="white",
        line2_color="primary",
        line3_color="primary",
        line1_size=46,
        line2_size=24,
        line3_size=20,
        notes="TURNING POINT (1:30–1:45)\nMy pivotal moment was catching an unrealistic AI claim that dairy butter could sit ambiently without spoilage.",
    )

    # Slide 14: Verification
    add_statement_slide(
        prs,
        scheme_key="peanut",
        line1="AI as Drafter, Not Director.",
        line2="Auditing scan price spikes. Verifying live supermarket shelves.",
        line1_color="white",
        line2_color="primary",
        line1_size=46,
        line2_size=22,
        notes="VERIFICATION (1:45–1:58)\nI audited raw scan data outliers and manually verified shelf prices on New World instead of trusting model summaries.",
    )

    # -----------------------------------------------------------------------
    # SECTION 4: Reflection 2 — Authenticity, AI Slop & Ethics (Scheme: Yeast)
    # -----------------------------------------------------------------------

    # Slide 15: Banning Buzzwords
    add_statement_slide(
        prs,
        scheme_key="yeast",
        line1="Banning Corporate Buzzwords.",
        line2="Stripping AI hype for plain facts: Peel. Press. Toast.",
        line1_color="white",
        line2_color="primary",
        line1_size=48,
        line2_size=24,
        notes="AUTHENTICITY (1:58–2:15)\nTo combat AI slop, I stripped corporate clichés and grounded packaging in real continuous deposit tooling.",
    )

    # Slide 16: Food Regulation
    add_statement_slide(
        prs,
        scheme_key="yeast",
        line1="Zero Hallucination Tolerance.",
        line2="Strict FSANZ food laws and prominent allergen warnings.",
        line1_color="white",
        line2_color="primary",
        line1_size=48,
        line2_size=24,
        notes="REGULATION (2:15–2:30)\nIn food and beverage, AI hallucinations are a severe legal hazard. I enforced strict FSANZ compliance and allergen safety.",
    )

    # Slide 17: Human Accountability
    add_statement_slide(
        prs,
        scheme_key="yeast",
        line1="Accountability Remains Human.",
        line2="Moral and legal ownership can never be outsourced.",
        line1_color="white",
        line2_color="primary",
        line1_size=48,
        line2_size=24,
        notes="ETHICS & WRAP (2:30–2:45)\nGenerative AI accelerates velocity, but human skepticism, taste, discernment, and moral ownership remain essential.",
    )

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"Successfully generated {OUT_PPTX} (17 minimal, container-free slides)")


def main():
    with tempfile.TemporaryDirectory(prefix="stamp-slides-") as tmpdir:
        build_presentation(Path(tmpdir))


if __name__ == "__main__":
    main()
