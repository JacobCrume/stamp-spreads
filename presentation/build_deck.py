#!/usr/bin/env python3
"""Generate presentation/Stamp-pitch.pptx for INFO123 Video Presentation.

Strictly adheres to:
1. The 3 Colors Plus Neutral Rule:
   - Each slide uses ONLY: 1 Secondary (screen bg), 1 Tertiary (cards),
     1 Primary (accent/highlights), plus Neutral White (#FFFFFF) for text.
   - Absolutely NO other colors mixed on the same slide.
2. Distinct Flavour Color Schemes across sections:
   - Slide 1: Yeast / Classic (Deep Night Ink #240340, Solid Purple #3B0764, Electric Lavender #E24BFF)
   - Slide 2: Butter (Caramel #4A3000, Deep Umber #2D1D00, Butter Gold #FFD640)
   - Slide 3: Raspberry (Rich Berry #460820, Dark Maroon #2D0414, Neon Raspberry #FF467A)
   - Slide 4: Peanut (Peanut Umber #4E2408, Dark Nut #2D1403, Peanut Ochre #FF8C30)
   - Slide 5: Yeast / Outro (Deep Night Ink #240340, Solid Purple #3B0764, Electric Lavender #E24BFF)
3. Ruthlessly Decluttered:
   - Huge, confident typography (titles 32–44pt, numbers 44–54pt).
   - Maximum 2–3 brief bullet points per card (3–6 words each).
   - Generous breathing space, flat solid surfaces, zero shadows, zero borders.
"""

from __future__ import annotations

from pathlib import Path
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
        "secondary": RGBColor(36, 3, 64),    # #240340
        "tertiary": RGBColor(59, 7, 100),    # #3B0764
        "primary": RGBColor(226, 75, 255),   # #E24BFF
        "white": RGBColor(255, 255, 255),
    },
    "butter": {
        "secondary": RGBColor(74, 48, 0),    # #4A3000
        "tertiary": RGBColor(45, 29, 0),     # #2D1D00
        "primary": RGBColor(255, 214, 64),   # #FFD640
        "white": RGBColor(255, 255, 255),
    },
    "raspberry": {
        "secondary": RGBColor(70, 8, 32),    # #460820
        "tertiary": RGBColor(45, 4, 20),     # #2D0414
        "primary": RGBColor(255, 70, 122),   # #FF467A
        "white": RGBColor(255, 255, 255),
    },
    "peanut": {
        "secondary": RGBColor(78, 36, 8),    # #4E2408
        "tertiary": RGBColor(45, 20, 3),     # #2D1403
        "primary": RGBColor(255, 140, 48),   # #FF8C30
        "white": RGBColor(255, 255, 255),
    },
}


# ---------------------------------------------------------------------------
# TEMPLATE PRIMITIVES (Strictly flat, shadowless, borderless)
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


def add_kicker(slide, left: Inches, top: Inches, text: str, primary_color: RGBColor):
    """Minimal, bold kicker headline without borders."""
    tb = slide.shapes.add_textbox(left, top, Inches(10), Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text.upper()
    p.font.name = "Manrope"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = primary_color
    return tb


def add_header(slide, left: Inches, top: Inches, kicker: str, title: str, subtitle: str, scheme: dict):
    """Decluttered standardized header zone."""
    add_kicker(slide, left, top, kicker, scheme["primary"])

    tb = slide.shapes.add_textbox(left, top + Inches(0.32), Inches(11.7), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = "Manrope"
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = scheme["white"]
    p_title.space_after = Pt(2)

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.name = "Manrope"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = False
    p_sub.font.color.rgb = scheme["primary"]


# ---------------------------------------------------------------------------
# SLIDE BUILDERS (Decluttered, ruthlessly cut, 3 colors + neutral)
# ---------------------------------------------------------------------------

def build_slide_1_hero(prs: pptx.Presentation):
    """Slide 1: Hero Title (Scheme: Yeast). Ruthlessly minimal."""
    s = SCHEMES["yeast"]
    slide = create_slide_canvas(prs, s["secondary"])

    left_x = Inches(1.2)
    top_y = Inches(1.8)

    # Wordmark / Brand
    tb = slide.shapes.add_textbox(left_x, top_y, Inches(7.5), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_brand = tf.paragraphs[0]
    p_brand.text = "STAMP"
    p_brand.font.name = "Manrope"
    p_brand.font.size = Pt(68)
    p_brand.font.bold = True
    p_brand.font.color.rgb = s["primary"]
    p_brand.space_after = Pt(4)

    p_tag = tf.add_paragraph()
    p_tag.text = "PEEL. PRESS. TOAST."
    p_tag.font.name = "Manrope"
    p_tag.font.size = Pt(28)
    p_tag.font.bold = True
    p_tag.font.color.rgb = s["white"]
    p_tag.space_after = Pt(16)

    p_sub = tf.add_paragraph()
    p_sub.text = "The Utensil-Free Breakfast Spread for Hot Toast"
    p_sub.font.name = "Manrope"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = s["primary"]
    p_sub.space_after = Pt(28)

    p_pres = tf.add_paragraph()
    p_pres.text = "Commercial Business Pitch  •  Jacob  •  INFO123 Business AI Project"
    p_pres.font.name = "Manrope"
    p_pres.font.size = Pt(12)
    p_pres.font.bold = True
    p_pres.font.color.rgb = s["white"]

    # Clean hero visual on right
    pack_path = ROOT / "brand" / "explorations" / "flavours" / "butter.png"
    if not pack_path.exists():
        pack_path = ROOT / "brand" / "pack.png"
    if pack_path.exists():
        slide.shapes.add_picture(str(pack_path), Inches(8.6), Inches(1.6), width=Inches(3.8))

    slide.notes_slide.notes_text_frame.text = (
        "TITLE SLIDE (0:00–0:08)\n"
        "Kia ora. I'm Jacob, and this is Stamp: a New Zealand breakfast spread innovation "
        "engineered for hot toast."
    )


def build_slide_2_pitch1(prs: pptx.Presentation):
    """Slide 2: Pitch 1 — Product Innovation (Scheme: Butter). Decluttered 2-card contrast."""
    s = SCHEMES["butter"]
    slide = create_slide_canvas(prs, s["secondary"])

    add_header(
        slide,
        left=Inches(0.9),
        top=Inches(0.6),
        kicker="01 / PRODUCT INNOVATION  •  PITCH PART 1 (30 SECONDS)",
        title="Peel. Press. Toast.",
        subtitle="Eliminating out-of-kitchen breakfast friction with a 10 g meltable spread disc.",
        scheme=s,
    )

    card_y = Inches(2.2)
    card_h = Inches(4.5)
    card_w = Inches(5.6)

    # ------------------
    # LEFT CARD: The Problem
    # ------------------
    add_flat_card(slide, Inches(0.9), card_y, card_w, card_h, s["tertiary"])

    tb_l = slide.shapes.add_textbox(Inches(1.3), card_y + Inches(0.4), card_w - Inches(0.8), card_h - Inches(0.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    p_lt = tf_l.paragraphs[0]
    p_lt.text = "THE PROBLEM"
    p_lt.font.name = "Manrope"
    p_lt.font.size = Pt(20)
    p_lt.font.bold = True
    p_lt.font.color.rgb = s["primary"]
    p_lt.space_after = Pt(20)

    problem_points = [
        "Jars Require Infrastructure",
        "Demands table knives, kitchen counters, and sink washing.",
        "",
        "Fails Mobile Consumers",
        "Students in halls, commuters, and desk workers cannot eat toast conveniently.",
        "",
        "Stationary & Bulky",
        "Heavy glass jars sit immobile in pantries rather than travelling on-the-go.",
    ]
    for idx, text in enumerate(problem_points):
        p = tf_l.add_paragraph()
        p.text = text
        p.font.name = "Manrope"
        if idx % 3 == 0:
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = s["white"]
            p.space_after = Pt(2)
        elif idx % 3 == 1:
            p.font.size = Pt(12)
            p.font.bold = False
            p.font.color.rgb = s["white"]
            p.space_after = Pt(14)

    # ------------------
    # RIGHT CARD: The Stamp Solution
    # ------------------
    add_flat_card(slide, Inches(6.8), card_y, card_w, card_h, s["tertiary"])

    tb_r = slide.shapes.add_textbox(Inches(7.2), card_y + Inches(0.4), card_w - Inches(0.8), card_h - Inches(0.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "THE STAMP SOLUTION"
    p_rt.font.name = "Manrope"
    p_rt.font.size = Pt(20)
    p_rt.font.bold = True
    p_rt.font.color.rgb = s["primary"]
    p_rt.space_after = Pt(20)

    solution_points = [
        "10 g Peel-and-Press Disc",
        "Pre-portioned spread mounted on food-grade release film.",
        "",
        "Thermal Spread Gesture",
        "Presses onto hot bread; melts evenly in seconds with zero cutlery.",
        "",
        "12-Month Ambient Stability",
        "Sealed card sheets provide verified shelf stability without refrigeration.",
    ]
    for idx, text in enumerate(solution_points):
        p = tf_r.add_paragraph()
        p.text = text
        p.font.name = "Manrope"
        if idx % 3 == 0:
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = s["white"]
            p.space_after = Pt(2)
        elif idx % 3 == 1:
            p.font.size = Pt(12)
            p.font.bold = False
            p.font.color.rgb = s["white"]
            p.space_after = Pt(14)

    slide.notes_slide.notes_text_frame.text = (
        "PITCH SLIDE 1 (0:08–0:34)\n"
        "Eating toast away from a full kitchen is broken. When you're in a student hall, flat, "
        "or office desk, nobody wants to lug a sticky 750-gram jar, track down a table knife, "
        "and wash it in an office sink.\n\n"
        "Stamp reinvents the format with a thin, 10-gram disc of real spread on release film. "
        "You peel it off, press it onto hot toast, and residual heat softens it into an even spread "
        "in seconds. No knife, no open jar, no morning mess.\n\n"
        "We launch with four distinct flavours: Salted Butter, Raspberry, Yeast extract, and Peanut—"
        "pantry-stable for 12 months in an 8-stamp card sheet."
    )


def build_slide_3_pitch2(prs: pptx.Presentation):
    """Slide 3: Pitch 2 — Market & Economics (Scheme: Raspberry). 3 Bold Stat Blocks."""
    s = SCHEMES["raspberry"]
    slide = create_slide_canvas(prs, s["secondary"])

    add_header(
        slide,
        left=Inches(0.9),
        top=Inches(0.6),
        kicker="02 / MARKET OPPORTUNITY  •  PITCH PART 2 (30 SECONDS)",
        title="$341M Category. 0 Rivals.",
        subtitle="Capturing the premium convenience gap in New Zealand breakfast retail.",
        scheme=s,
    )

    card_y = Inches(2.2)
    card_h = Inches(4.5)
    card_w = Inches(3.6)
    gap = Inches(0.35)
    cx = Inches(0.9)

    stat_cards = [
        (
            "$341M",
            "RETAIL CATEGORY",
            "+24% Revenue Growth",
            "Supermarket scan data shows spreads expanding from $275M to $341M NZD (2022–2025). Premium spreads surged +29% to $113M.",
        ),
        (
            "0",
            "FORMAT COMPETITORS",
            "100% Format Vacuum",
            "Across 154 existing New Zealand spread products, not a single brand offers a utensil-free, single-serve format.",
        ),
        (
            "$1.75",
            "GROSS CONTRIBUTION",
            "Strong Unit Economics",
            "Priced at $5.00 NZD per sheet (63¢ / toast portion). At an assumed $1.50 co-packing cost and 35% retail margin, Stamp retains $1.75 per sheet.",
        ),
    ]

    for num, headline, subhead, desc in stat_cards:
        add_flat_card(slide, cx, card_y, card_w, card_h, s["tertiary"])

        tb = slide.shapes.add_textbox(cx + Inches(0.3), card_y + Inches(0.4), card_w - Inches(0.6), card_h - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.name = "Manrope"
        p_num.font.size = Pt(48)
        p_num.font.bold = True
        p_num.font.color.rgb = s["primary"]
        p_num.space_after = Pt(4)

        p_h = tf.add_paragraph()
        p_h.text = headline
        p_h.font.name = "Manrope"
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = s["white"]
        p_h.space_after = Pt(2)

        p_sub = tf.add_paragraph()
        p_sub.text = subhead
        p_sub.font.name = "Manrope"
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = s["primary"]
        p_sub.space_after = Pt(16)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Manrope"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = s["white"]

        cx += card_w + gap

    slide.notes_slide.notes_text_frame.text = (
        "PITCH SLIDE 2 (0:34–0:58)\n"
        "Our analysis of New Zealand breakfast retail sales shows spreads revenue grew 24% to 341 million dollars, "
        "with the premium tier surging 29% to 113 million. Yet across 154 existing spread products, not one offers "
        "a single-serve portion format.\n\n"
        "Supermarket jars like Pic's or Fix & Fogg compete on bulk weight, but they are messy and stationary. "
        "At five dollars a sheet—just 63 cents a toast portion—Stamp captures premium convenience. With an assumed "
        "manufacturing cost of one-fifty, we retain a strong one-dollar-seventy-five gross margin per sheet. "
        "Stamp is ready to own portable breakfast."
    )


def build_slide_4_reflection1(prs: pptx.Presentation):
    """Slide 4: Reflection Q1 — Working with Generative AI (Scheme: Peanut). Ruthlessly decluttered."""
    s = SCHEMES["peanut"]
    slide = create_slide_canvas(prs, s["secondary"])

    add_header(
        slide,
        left=Inches(0.9),
        top=Inches(0.6),
        kicker="03 / PERSONAL REFLECTION  •  PART 2 (STUDENT'S OWN VOICE)",
        title="Steering & Verification",
        subtitle="Key takeaways from prompt engineering, session partitioning, and fact-checking.",
        scheme=s,
    )

    card_y = Inches(2.2)
    card_h = Inches(4.5)
    card_w = Inches(3.6)
    gap = Inches(0.35)
    cx = Inches(0.9)

    reflections = [
        (
            "01",
            "CONTEXT STEERING",
            "Role Personas & Negative Bans",
            "Enforcing strict negative constraints against therapeutic health claims and fake certification badges prevented generic hallucinations.",
            "Session Partitioning",
            "Isolating data analysis, brand spec, and copywriting into modular sessions eliminated context drift across the project.",
        ),
        (
            "02",
            "TURNING POINT",
            "Catching Butter Instability",
            "Caught an unrealistic AI assumption that dairy butter could sit ambiently; forced reformulation into cultured dairy spread.",
            "Independent Verification",
            "Manually cross-checked real supermarket scan formulas and live New World pricing rather than trusting raw AI figures.",
        ),
        (
            "03",
            "FUTURE PRACTICE",
            "AI as Drafter, Not Director",
            "Treating model outputs strictly as draft hypotheses requiring rigorous empirical validation.",
            "Locked Core Specifications",
            "Establishing fixed data schemas and non-negotiable brand specs before initiating generative drafting tasks.",
        ),
    ]

    for num, headline, sub1, desc1, sub2, desc2 in reflections:
        add_flat_card(slide, cx, card_y, card_w, card_h, s["tertiary"])

        tb = slide.shapes.add_textbox(cx + Inches(0.3), card_y + Inches(0.4), card_w - Inches(0.6), card_h - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.name = "Manrope"
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = s["primary"]
        p_num.space_after = Pt(2)

        p_h = tf.add_paragraph()
        p_h.text = headline
        p_h.font.name = "Manrope"
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = s["white"]
        p_h.space_after = Pt(14)

        # Point 1
        p_s1 = tf.add_paragraph()
        p_s1.text = "• " + sub1
        p_s1.font.name = "Manrope"
        p_s1.font.size = Pt(11)
        p_s1.font.bold = True
        p_s1.font.color.rgb = s["primary"]
        p_s1.space_after = Pt(2)

        p_d1 = tf.add_paragraph()
        p_d1.text = desc1
        p_d1.font.name = "Manrope"
        p_d1.font.size = Pt(10)
        p_d1.font.color.rgb = s["white"]
        p_d1.space_after = Pt(12)

        # Point 2
        p_s2 = tf.add_paragraph()
        p_s2.text = "• " + sub2
        p_s2.font.name = "Manrope"
        p_s2.font.size = Pt(11)
        p_s2.font.bold = True
        p_s2.font.color.rgb = s["primary"]
        p_s2.space_after = Pt(2)

        p_d2 = tf.add_paragraph()
        p_d2.text = desc2
        p_d2.font.name = "Manrope"
        p_d2.font.size = Pt(10)
        p_d2.font.color.rgb = s["white"]

        cx += card_w + gap

    slide.notes_slide.notes_text_frame.text = (
        "REFLECTION Q1 (1:00–1:55)\n"
        "[Jacob's personal reflection: speak directly to camera about your AI steering experience.]\n"
        "Key speaking cues:\n"
        "1. Mention how you structured distinct sessions rather than one massive unmanageable chat.\n"
        "2. Explain how you used explicit negative constraints (e.g. banning health claims and certification badges) "
        "and role personas to get reliable results.\n"
        "3. Share a concrete example where an AI model gave an unrealistic answer (e.g., assuming chilled butter could "
        "sit ambiently without dairy-spread reformulations) and how you caught and corrected it."
    )


def build_slide_5_reflection2(prs: pptx.Presentation):
    """Slide 5: Reflection Q2 — AI Slop & Ethics (Scheme: Yeast). Ruthlessly decluttered."""
    s = SCHEMES["yeast"]
    slide = create_slide_canvas(prs, s["secondary"])

    add_header(
        slide,
        left=Inches(0.9),
        top=Inches(0.6),
        kicker="04 / CRITICAL ETHICS  •  PART 2 (STUDENT'S OWN VOICE)",
        title="Authenticity & Accountability",
        subtitle="Combating AI slop, regulatory food liabilities, and human ownership.",
        scheme=s,
    )

    card_y = Inches(2.2)
    card_h = Inches(4.5)
    card_w = Inches(3.6)
    gap = Inches(0.35)
    cx = Inches(0.9)

    ethics = [
        (
            "01",
            "COMBATING 'AI SLOP'",
            "Stripping Hyperbolic Jargon",
            "Actively rejected generic corporate cliches ('game-changer', 'revolutionary journey') in favor of punchy facts: 'Peel. Press. Toast.'",
            "Physical Reality Over Fantasy",
            "Grounded product specifications in real packaging engineering (continuous deposit, release film) rather than impossible AI mockups.",
        ),
        (
            "02",
            "FOOD REGULATION",
            "The Hallucination Danger",
            "Unchecked models frequently invent fake organic labels, false 'gluten-free' badges, or illegal medical claims.",
            "FSANZ & Allergen Responsibility",
            "Enforced strict New Zealand food labeling standards and ensured life-threatening peanut and gluten warnings remained prominent.",
        ),
        (
            "03",
            "KNOWLEDGE WORKERS",
            "Non-Delegable Accountability",
            "When deploying AI commercially, legal, moral, and customer accountability can never be outsourced to an algorithm.",
            "Critical Thinking as Core Value",
            "The primary skill of the future knowledge worker is skepticism, verification, taste, and active human agency.",
        ),
    ]

    for num, headline, sub1, desc1, sub2, desc2 in ethics:
        add_flat_card(slide, cx, card_y, card_w, card_h, s["tertiary"])

        tb = slide.shapes.add_textbox(cx + Inches(0.3), card_y + Inches(0.4), card_w - Inches(0.6), card_h - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.name = "Manrope"
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = s["primary"]
        p_num.space_after = Pt(2)

        p_h = tf.add_paragraph()
        p_h.text = headline
        p_h.font.name = "Manrope"
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = s["white"]
        p_h.space_after = Pt(14)

        # Point 1
        p_s1 = tf.add_paragraph()
        p_s1.text = "• " + sub1
        p_s1.font.name = "Manrope"
        p_s1.font.size = Pt(11)
        p_s1.font.bold = True
        p_s1.font.color.rgb = s["primary"]
        p_s1.space_after = Pt(2)

        p_d1 = tf.add_paragraph()
        p_d1.text = desc1
        p_d1.font.name = "Manrope"
        p_d1.font.size = Pt(10)
        p_d1.font.color.rgb = s["white"]
        p_d1.space_after = Pt(12)

        # Point 2
        p_s2 = tf.add_paragraph()
        p_s2.text = "• " + sub2
        p_s2.font.name = "Manrope"
        p_s2.font.size = Pt(11)
        p_s2.font.bold = True
        p_s2.font.color.rgb = s["primary"]
        p_s2.space_after = Pt(2)

        p_d2 = tf.add_paragraph()
        p_d2.text = desc2
        p_d2.font.name = "Manrope"
        p_d2.font.size = Pt(10)
        p_d2.font.color.rgb = s["white"]

        cx += card_w + gap

    slide.notes_slide.notes_text_frame.text = (
        "REFLECTION Q2 (1:55–2:45)\n"
        "[Jacob's personal reflection: speak directly to camera on authenticity and ethics.]\n"
        "Key speaking cues:\n"
        "1. Explain how you actively stripped out generic corporate jargon in favour of plain, punchy facts.\n"
        "2. Emphasize the legal hazards of AI in food and beverage: hallucinated health benefits, "
        "false gluten-free claims, and allergen responsibility.\n"
        "3. Conclude with your takeaway: Generative AI accelerates drafting, but human judgment, taste, "
        "and ultimate accountability can never be outsourced to a model."
    )


def main():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide_1_hero(prs)
    build_slide_2_pitch1(prs)
    build_slide_3_pitch2(prs)
    build_slide_4_reflection1(prs)
    build_slide_5_reflection2(prs)

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"Successfully generated decluttered presentation: {OUT_PPTX}")


if __name__ == "__main__":
    main()
