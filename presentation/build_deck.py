#!/usr/bin/env python3
"""Generate presentation/Stamp-pitch.pptx for INFO123 Video Presentation.

Strictly adheres to:
1. Cover Slide: Almost identical to PDF Page 1 (Minimalist Deep Night Ink,
   centered STAMP wordmark, PEEL. PRESS. TOAST., and Commercial Business Pitch at the bottom).
2. Bite-sized, Single-Idea Slides:
   - One slide dedicated to each specific problem, solution, or insight.
   - Rapid-fire, dynamic presentation (~10-15s per slide) instead of text-dense walls.
3. The 3 Colors Plus Neutral Rule:
   - Each section uses ONLY: 1 Secondary (screen bg), 1 Tertiary (card surface),
     1 Primary (kicker, numbers, highlights), plus Neutral White (#FFFFFF).
   - Zero other colors mixed on the same slide.
4. Flavour Palette Grouping across related sections:
   - Cover & Outro: Yeast / Classic (#240340, #3B0764, #E24BFF, #FFFFFF)
   - Product Innovation: Butter (#4A3000, #2D1D00, #FFD640, #FFFFFF)
   - Market & Economics: Raspberry (#460820, #2D0414, #FF467A, #FFFFFF)
   - Reflection (Steering & Verification): Peanut (#4E2408, #2D1403, #FF8C30, #FFFFFF)
   - Reflection (Slop & Ethics): Yeast / Classic (#240340, #3B0764, #E24BFF, #FFFFFF)
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
        "tertiary": RGBColor(59, 7, 100),    # #3B0764 (Deep Solid Purple)
        "primary": RGBColor(226, 75, 255),   # #E24BFF (Electric Lavender)
        "white": RGBColor(255, 255, 255),
        "rgb": (226, 75, 255),
    },
    "butter": {
        "secondary": RGBColor(74, 48, 0),    # #4A3000 (Roasted Caramel Brown)
        "tertiary": RGBColor(45, 29, 0),     # #2D1D00 (Deep Umber)
        "primary": RGBColor(255, 214, 64),   # #FFD640 (Electric Butter Gold)
        "white": RGBColor(255, 255, 255),
        "rgb": (255, 214, 64),
    },
    "raspberry": {
        "secondary": RGBColor(70, 8, 32),    # #460820 (Rich Berry)
        "tertiary": RGBColor(45, 4, 20),     # #2D0414 (Dark Berry Maroon)
        "primary": RGBColor(255, 70, 122),   # #FF467A (Neon Wild Raspberry)
        "white": RGBColor(255, 255, 255),
        "rgb": (255, 70, 122),
    },
    "peanut": {
        "secondary": RGBColor(78, 36, 8),    # #4E2408 (Deep Peanut Umber)
        "tertiary": RGBColor(45, 20, 3),     # #2D1403 (Dark Roasted Nut Brown)
        "primary": RGBColor(255, 140, 48),   # #FF8C30 (Roasted Peanut Ochre)
        "white": RGBColor(255, 255, 255),
        "rgb": (255, 140, 48),
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


# ---------------------------------------------------------------------------
# TEMPLATE HELPERS (Strictly flat, shadowless, borderless)
# ---------------------------------------------------------------------------

def create_slide_canvas(prs: pptx.Presentation, bg_color: RGBColor):
    """Full-bleed flat canvas without borders or shadows."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()
    return slide


def add_flat_card(slide, left: Inches, top: Inches, width: Inches, height: Inches, fill_color: RGBColor):
    """Flat solid card surface."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    card.line.fill.background()
    return card


def add_single_topic_content(
    slide,
    kicker: str,
    headline: str,
    subtitle: str,
    takeaways: list[tuple[str, str]],
    scheme: dict,
):
    """Clean, decluttered single-topic layout."""
    left = Inches(1.2)
    top = Inches(0.9)

    # 1. Kicker
    tb_k = slide.shapes.add_textbox(left, top, Inches(10.5), Inches(0.4))
    tf_k = tb_k.text_frame
    tf_k.word_wrap = False
    tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = kicker.upper()
    p_k.font.name = "Manrope"
    p_k.font.size = Pt(13)
    p_k.font.bold = True
    p_k.font.color.rgb = scheme["primary"]

    # 2. Headline & Subtitle
    tb_h = slide.shapes.add_textbox(left, top + Inches(0.45), Inches(10.8), Inches(1.7))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0

    p_title = tf_h.paragraphs[0]
    p_title.text = headline
    p_title.font.name = "Manrope"
    p_title.font.size = Pt(40)
    p_title.font.bold = True
    p_title.font.color.rgb = scheme["white"]
    p_title.space_after = Pt(6)

    p_sub = tf_h.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.name = "Manrope"
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = scheme["primary"]

    # 3. Takeaway Cards (1 or 2 clean cards)
    card_y = Inches(3.2)
    card_w = Inches(5.2) if len(takeaways) == 2 else Inches(10.8)
    card_h = Inches(3.3)
    gap = Inches(0.4)

    for i, (point_title, point_desc) in enumerate(takeaways):
        cx = left + i * (card_w + gap)
        add_flat_card(slide, cx, card_y, card_w, card_h, scheme["tertiary"])

        tb_c = slide.shapes.add_textbox(cx + Inches(0.4), card_y + Inches(0.4), card_w - Inches(0.8), card_h - Inches(0.8))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

        p_pt = tf_c.paragraphs[0]
        p_pt.text = point_title
        p_pt.font.name = "Manrope"
        p_pt.font.size = Pt(19)
        p_pt.font.bold = True
        p_pt.font.color.rgb = scheme["primary"]
        p_pt.space_after = Pt(12)

        p_pd = tf_c.add_paragraph()
        p_pd.text = point_desc
        p_pd.font.name = "Manrope"
        p_pd.font.size = Pt(14)
        p_pd.font.color.rgb = scheme["white"]


def add_single_metric_content(
    slide,
    kicker: str,
    metric_number: str,
    headline: str,
    detail: str,
    scheme: dict,
):
    """Massive, bold single-metric layout."""
    left = Inches(1.2)
    top = Inches(1.0)

    # 1. Kicker
    tb_k = slide.shapes.add_textbox(left, top, Inches(10.5), Inches(0.4))
    tf_k = tb_k.text_frame
    tf_k.word_wrap = False
    tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = kicker.upper()
    p_k.font.name = "Manrope"
    p_k.font.size = Pt(13)
    p_k.font.bold = True
    p_k.font.color.rgb = scheme["primary"]

    # 2. Main Stat Card
    card_y = Inches(1.8)
    card_w = Inches(10.8)
    card_h = Inches(4.7)
    add_flat_card(slide, left, card_y, card_w, card_h, scheme["tertiary"])

    tb_c = slide.shapes.add_textbox(left + Inches(0.6), card_y + Inches(0.6), card_w - Inches(1.2), card_h - Inches(1.2))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

    p_num = tf_c.paragraphs[0]
    p_num.text = metric_number
    p_num.font.name = "Manrope"
    p_num.font.size = Pt(72)
    p_num.font.bold = True
    p_num.font.color.rgb = scheme["primary"]
    p_num.space_after = Pt(8)

    p_h = tf_c.add_paragraph()
    p_h.text = headline
    p_h.font.name = "Manrope"
    p_h.font.size = Pt(28)
    p_h.font.bold = True
    p_h.font.color.rgb = scheme["white"]
    p_h.space_after = Pt(12)

    p_d = tf_c.add_paragraph()
    p_d.text = detail
    p_d.font.name = "Manrope"
    p_d.font.size = Pt(16)
    p_d.font.color.rgb = scheme["primary"]


# ---------------------------------------------------------------------------
# BITE-SIZED SLIDE GENERATOR
# ---------------------------------------------------------------------------

def build_presentation(work_dir: Path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Generate smooth recolored wordmark for Yeast cover
    cover_mark_path = work_dir / "cover_wordmark.png"
    px_w, px_h = create_recolored_wordmark(
        ROOT / "brand" / "logo.png", cover_mark_path, (226, 75, 255)
    )

    # -----------------------------------------------------------------------
    # SLIDE 1: Minimalist Cover (Identical to PDF Page 1)
    # -----------------------------------------------------------------------
    s_yeast = SCHEMES["yeast"]
    slide1 = create_slide_canvas(prs, s_yeast["secondary"])

    # Centered Wordmark
    mark_w = Inches(5.8)
    mark_h = mark_w * (px_h / px_w)
    mark_x = (prs.slide_width - mark_w) / 2
    mark_y = Inches(2.3)
    slide1.shapes.add_picture(str(cover_mark_path), mark_x, mark_y, width=mark_w, height=mark_h)

    # Centered Tagline
    tb_tag = slide1.shapes.add_textbox(Inches(1.5), mark_y + mark_h + Inches(0.3), Inches(10.333), Inches(0.8))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = False
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "PEEL. PRESS. TOAST."
    p_tag.font.name = "Manrope"
    p_tag.font.size = Pt(28)
    p_tag.font.bold = True
    p_tag.font.color.rgb = s_yeast["primary"]
    p_tag.alignment = PP_ALIGN.CENTER

    # Centered Commercial Business Pitch at bottom
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
        "TITLE SLIDE (0:00–0:08)\n"
        "Kia ora. I'm Jacob, and this is Stamp: a New Zealand breakfast spread innovation engineered for hot toast."
    )

    # -----------------------------------------------------------------------
    # SECTION 1: Product Innovation & Problem (Scheme: Butter)
    # -----------------------------------------------------------------------
    s_butter = SCHEMES["butter"]

    # Slide 2: The Infrastructure Problem
    slide2 = create_slide_canvas(prs, s_butter["secondary"])
    add_single_topic_content(
        slide2,
        kicker="01 / THE PROBLEM  •  PITCH PART 1",
        headline="Jars Require Infrastructure.",
        subtitle="Table knives, kitchen counters, and sink washing. Breakfast away from home is broken.",
        takeaways=[
            ("Cutlery Dependency", "Office breakrooms, university halls, and student flats lack clean table knives and preparation space."),
            ("Stationary & Bulky", "Heavy 750 g glass jars sit immobile in cupboards rather than travelling conveniently in work bags."),
        ],
        scheme=s_butter,
    )
    slide2.notes_slide.notes_text_frame.text = (
        "PROBLEM SLIDE (0:08–0:18)\n"
        "Eating toast away from a full kitchen is broken. When you're in a student hall, flat, "
        "or office desk, nobody wants to lug a sticky 750-gram jar, track down a table knife, "
        "and wash it in an office sink."
    )

    # Slide 3: The Solution (Peel & Press Format)
    slide3 = create_slide_canvas(prs, s_butter["secondary"])
    add_single_topic_content(
        slide3,
        kicker="02 / THE SOLUTION  •  PITCH PART 1",
        headline="10 g Spread Disc on Release Film.",
        subtitle="Peel it off. Press onto hot toast. Residual thermal energy softens it in seconds.",
        takeaways=[
            ("Thermal Melt Gesture", "Residual heat from toasted bread softens the disc into an even, velvety layer with zero cutlery."),
            ("Calibrated Portion Control", "Pre-portioned 10 g servings eliminate cross-contamination, messy sticky jars, and food waste."),
        ],
        scheme=s_butter,
    )
    slide3.notes_slide.notes_text_frame.text = (
        "SOLUTION SLIDE (0:18–0:28)\n"
        "Stamp reinvents the format with a thin, 10-gram disc of real spread on release film. "
        "You peel it off, press it onto hot toast, and residual heat softens it into an even spread in seconds."
    )

    # Slide 4: Format & Stability
    slide4 = create_slide_canvas(prs, s_butter["secondary"])
    add_single_topic_content(
        slide4,
        kicker="03 / THE FORMAT  •  PITCH PART 1",
        headline="12-Month Ambient Pantry Life.",
        subtitle="Pocketable 8-stamp card sheets. Verified ambient stability with zero refrigeration.",
        takeaways=[
            ("Continuous Deposit Packaging", "Hermetically sealed card sheets protect against moisture and air, maintaining 12-month ambient shelf life."),
            ("Four Launch Varieties", "Salted Butter, Wild Raspberry whole fruit paste, Savoury Yeast extract, and Roasted Peanut."),
        ],
        scheme=s_butter,
    )
    slide4.notes_slide.notes_text_frame.text = (
        "FORMAT SLIDE (0:28–0:34)\n"
        "We launch with four distinct flavours: Salted Butter, Raspberry, Yeast extract, and Peanut—"
        "pantry-stable for 12 months in an 8-stamp card sheet."
    )

    # -----------------------------------------------------------------------
    # SECTION 2: Market Opportunity & Unit Economics (Scheme: Raspberry)
    # -----------------------------------------------------------------------
    s_berry = SCHEMES["raspberry"]

    # Slide 5: Market Scale
    slide5 = create_slide_canvas(prs, s_berry["secondary"])
    add_single_metric_content(
        slide5,
        kicker="04 / MARKET SCALE  •  PITCH PART 2",
        metric_number="$341M",
        headline="New Zealand Spreads Category.",
        detail="+24% category revenue growth (2022–2025). Premium branded spreads surged +29% to $113M NZD.",
        scheme=s_berry,
    )
    slide5.notes_slide.notes_text_frame.text = (
        "MARKET SCALE SLIDE (0:34–0:42)\n"
        "Our analysis of New Zealand breakfast retail sales shows spreads revenue grew 24% to 341 million dollars, "
        "with the premium tier surging 29% to 113 million."
    )

    # Slide 6: The Competitive Format Void
    slide6 = create_slide_canvas(prs, s_berry["secondary"])
    add_single_metric_content(
        slide6,
        kicker="05 / COMPETITIVE VOID  •  PITCH PART 2",
        metric_number="0 Rivals",
        headline="Across 154 Supermarket Spreads.",
        detail="Not a single brand offers a utensil-free single-serve format. Jars compete on bulk weight; Stamp wins on convenience.",
        scheme=s_berry,
    )
    slide6.notes_slide.notes_text_frame.text = (
        "COMPETITIVE VOID SLIDE (0:42–0:50)\n"
        "Yet across 154 existing spread products, not one offers a single-serve portion format. "
        "Supermarket jars like Pic's or Fix & Fogg compete on bulk weight, but they are messy and stationary."
    )

    # Slide 7: Unit Economics
    slide7 = create_slide_canvas(prs, s_berry["secondary"])
    add_single_metric_content(
        slide7,
        kicker="06 / UNIT ECONOMICS  •  PITCH PART 2",
        metric_number="$1.75 Margin",
        headline="$5.00 NZD per 8-Stamp Sheet.",
        detail="Just 63¢ per toast serving. At an assumed $1.50 contract manufacturing cost and 35% retail margin, Stamp captures $1.75 contribution.",
        scheme=s_berry,
    )
    slide7.notes_slide.notes_text_frame.text = (
        "ECONOMICS SLIDE (0:50–0:58)\n"
        "At five dollars a sheet—just 63 cents a toast portion—Stamp captures premium convenience. With an assumed "
        "manufacturing cost of one-fifty, we retain a strong one-dollar-seventy-five gross margin per sheet. "
        "Stamp is ready to own portable breakfast."
    )

    # -----------------------------------------------------------------------
    # SECTION 3: Reflection 1 — AI Steering & Verification (Scheme: Peanut)
    # -----------------------------------------------------------------------
    s_peanut = SCHEMES["peanut"]

    # Slide 8: Context Steering & Negative Bans
    slide8 = create_slide_canvas(prs, s_peanut["secondary"])
    add_single_topic_content(
        slide8,
        kicker="07 / REFLECTION  •  CONTEXT STEERING",
        headline="Strict Negative Constraints.",
        subtitle="Banning hallucinated health claims and partitioning sessions to prevent context drift.",
        takeaways=[
            ("Negative Prompt Guards", "Enforcing strict bans against therapeutic health benefits and fake organic badges eliminated marketing fluff."),
            ("Session Partitioning", "Isolating data cleaning, brand spec, and copywriting into modular sessions eliminated context decay."),
        ],
        scheme=s_peanut,
    )
    slide8.notes_slide.notes_text_frame.text = (
        "REFLECTION SLIDE 1 (1:00–1:20)\n"
        "To steer generative AI effectively, I structured distinct sessions rather than one massive chat, and "
        "enforced strict negative constraints against fake certification badges and medical claims."
    )

    # Slide 9: The Pivotal Turning Point
    slide9 = create_slide_canvas(prs, s_peanut["secondary"])
    add_single_topic_content(
        slide9,
        kicker="08 / REFLECTION  •  TURNING POINT",
        headline="Catching Butter Instability.",
        subtitle="Rejecting unrealistic model assumptions about ambient dairy shelf life.",
        takeaways=[
            ("The Hallucinated Assumption", "AI assumed standard churned butter could sit ambiently in a pantry for 12 months without spoiling."),
            ("The Human Formulation Pivot", "Caught the food science flaw and forced reformulation into a cultured dairy spread to ensure shelf stability."),
        ],
        scheme=s_peanut,
    )
    slide9.notes_slide.notes_text_frame.text = (
        "TURNING POINT SLIDE (1:20–1:40)\n"
        "My key pivotal moment was catching an unrealistic AI assumption that dairy butter could sit ambiently without spoilage. "
        "I intervened to enforce a shelf-stable cultured dairy spread formula."
    )

    # Slide 10: Verification & Fact-Checking
    slide10 = create_slide_canvas(prs, s_peanut["secondary"])
    add_single_topic_content(
        slide10,
        kicker="09 / REFLECTION  •  VERIFICATION",
        headline="AI as Drafter, Not Director.",
        subtitle="Auditing raw retail scan outliers and independently verifying competitor prices.",
        takeaways=[
            ("Data Cleaning Audits", "Manually audited raw breakfast sales data to catch aberrant price outliers (>$40) and formula errors."),
            ("Live Shelf Benchmarks", "Directly cross-referenced New World retail prices (Pic's $7.79, Fix & Fogg $11.99) rather than trusting AI estimates."),
        ],
        scheme=s_peanut,
    )
    slide10.notes_slide.notes_text_frame.text = (
        "VERIFICATION SLIDE (1:40–1:55)\n"
        "I audited raw supermarket scan data to spot price outliers and independently verified competitor prices on New World "
        "rather than blindly trusting model calculations."
    )

    # -----------------------------------------------------------------------
    # SECTION 4: Reflection 2 — Authenticity, AI Slop & Ethics (Scheme: Yeast)
    # -----------------------------------------------------------------------
    s_yeast = SCHEMES["yeast"]

    # Slide 11: Combating AI Slop
    slide11 = create_slide_canvas(prs, s_yeast["secondary"])
    add_single_topic_content(
        slide11,
        kicker="10 / REFLECTION  •  AUTHENTICITY",
        headline="Banning Corporate Buzzwords.",
        subtitle="Stripping hyperbolic marketing cliches for punchy facts: Peel. Press. Toast.",
        takeaways=[
            ("Rejecting Slop Phrases", "Actively stripped generic corporate fluff ('game-changer', 'revolutionary journey') to maintain authentic tone."),
            ("Physical Reality Grounding", "Anchored packaging in real industrial tooling (continuous deposit, release film) rather than AI fantasy mockups."),
        ],
        scheme=s_yeast,
    )
    slide11.notes_slide.notes_text_frame.text = (
        "AUTHENTICITY SLIDE (1:55–2:15)\n"
        "To combat AI slop, I actively stripped out corporate buzzwords in favour of plain, punchy facts, and "
        "grounded packaging in real physical manufacturing constraints."
    )

    # Slide 12: Food Regulation & Allergen Responsibility
    slide12 = create_slide_canvas(prs, s_yeast["secondary"])
    add_single_topic_content(
        slide12,
        kicker="11 / REFLECTION  •  REGULATION",
        headline="Zero Hallucination Tolerance.",
        subtitle="Strict FSANZ food compliance and non-negotiable allergen disclosures.",
        takeaways=[
            ("The Legal Hazard", "Unchecked AI frequently invents fake organic labels or dangerous 'gluten-free' badges (hazardous for Yeast extract)."),
            ("Enforcing Standards", "Complied strictly with Food Standards Australia New Zealand and ensured peanut and gluten warnings remained prominent."),
        ],
        scheme=s_yeast,
    )
    slide12.notes_slide.notes_text_frame.text = (
        "REGULATION SLIDE (2:15–2:30)\n"
        "In food and beverage, AI hallucinations are a severe legal hazard. I enforced strict compliance with "
        "New Zealand Food Standards and ensured life-threatening allergen warnings were never obscured."
    )

    # Slide 13: Human Accountability
    slide13 = create_slide_canvas(prs, s_yeast["secondary"])
    add_single_topic_content(
        slide13,
        kicker="12 / REFLECTION  •  ETHICS",
        headline="Accountability Remains Human.",
        subtitle="Legal, moral, and customer responsibility can never be outsourced to an algorithm.",
        takeaways=[
            ("Non-Delegable Agency", "When deploying AI commercially, accountability for safety and truth rests entirely with the human practitioner."),
            ("The Core Worker Value", "Critical thinking, skepticism, taste, and verification are the irreplaceable skills of future knowledge workers."),
        ],
        scheme=s_yeast,
    )
    slide13.notes_slide.notes_text_frame.text = (
        "ETHICS SLIDE (2:30–2:50)\n"
        "Ultimately, accountability can never be outsourced to a model. Generative AI accelerates execution, "
        "but human judgment, taste, skepticism, and moral ownership remain essential."
    )

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"Successfully generated {OUT_PPTX} (13 decluttered slides)")


def main():
    with tempfile.TemporaryDirectory(prefix="stamp-slides-") as tmpdir:
        build_presentation(Path(tmpdir))


if __name__ == "__main__":
    main()
