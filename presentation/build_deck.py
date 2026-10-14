#!/usr/bin/env python3
"""Generate presentation/Stamp-pitch.pptx for INFO123 Video Presentation.

Strictly adheres to the Stamp web design system:
- 16:9 widescreen layout (13.333" x 7.5")
- Deep Night Ink (#240340) full-bleed canvas across all slides
- Flat, borderless, shadowless elevated cards in Deep Solid Purple (#3B0764)
- Saturated, high-contrast primary accents everywhere:
  - Electric Lavender (#E24BFF)
  - Butter Gold (#FFD640)
  - Wild Raspberry (#FF467A)
  - Peanut Ochre (#FF8C30)
- High-legibility typography: Pure White (#FFFFFF) headlines, Soft Lavender (#E9D5FF) body
- High-impact stat callouts and structured cue cards for talking-head video presentation
"""

from __future__ import annotations

from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent.parent
OUT_PPTX = ROOT / "presentation" / "Stamp-pitch.pptx"

# Authentic Brand Palette from website/src/lib/theme.svelte.ts
BG_NIGHT_INK = RGBColor(36, 3, 64)       # #240340 (Canvas background)
SURFACE_PURPLE = RGBColor(59, 7, 100)    # #3B0764 (Flat solid card surface)
SURFACE_ELEVATED = RGBColor(76, 12, 128) # #4C0C80 (Elevated container)

ACCENT_LAVENDER = RGBColor(226, 75, 255) # #E24BFF (Electric Lavender)
ACCENT_BUTTER = RGBColor(255, 214, 64)   # #FFD640 (Electric Butter Gold)
ACCENT_BERRY = RGBColor(255, 70, 122)    # #FF467A (Wild Raspberry)
ACCENT_PEANUT = RGBColor(255, 140, 48)   # #FF8C30 (Roasted Peanut Ochre)

TEXT_WHITE = RGBColor(255, 255, 255)     # #FFFFFF (Headlines & primary text)
TEXT_SOFT = RGBColor(233, 213, 255)      # #E9D5FF (Body & bullet points)
TEXT_MUTED = RGBColor(216, 180, 254)     # #D8B4FE (Subtitles & metadata)


# ---------------------------------------------------------------------------
# SLIDE TEMPLATE HELPERS (Zero borders, zero shadows, flat solid surfaces)
# ---------------------------------------------------------------------------

def create_base_slide(prs: pptx.Presentation):
    """Create a new slide with a full-bleed Deep Night Ink (#240340) background."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_NIGHT_INK
    bg.line.fill.background()
    return slide


def add_flat_card(
    slide,
    left: Inches,
    top: Inches,
    width: Inches,
    height: Inches,
    bg_color: RGBColor = SURFACE_PURPLE,
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE,
):
    """Add a borderless, shadowless flat solid card."""
    card = slide.shapes.add_shape(shape_type, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.fill.background()
    return card


def add_kicker_badge(
    slide,
    left: Inches,
    top: Inches,
    text: str,
    text_color: RGBColor = ACCENT_LAVENDER,
    bg_color: RGBColor = SURFACE_PURPLE,
    width: Inches | None = None,
):
    """Add a clean flat solid pill badge for section kickers and timers."""
    est_width = width if width is not None else Inches(max(len(text) * 0.11 + 0.4, 1.8))
    badge = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, est_width, Inches(0.36)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.fill.background()

    tf = badge.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.05)

    p = tf.paragraphs[0]
    p.text = text.upper()
    p.font.name = "Manrope"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    return badge


def add_slide_header(
    slide,
    kicker: str,
    title: str,
    subtitle: str,
    kicker_color: RGBColor = ACCENT_LAVENDER,
):
    """Standardized top header zone matching the web brand."""
    left = Inches(0.8)
    top = Inches(0.5)

    # 1. Kicker Pill Badge
    add_kicker_badge(slide, left, top, kicker, text_color=kicker_color)

    # 2. Header Textbox (Title + Subtitle)
    tb = slide.shapes.add_textbox(left, top + Inches(0.44), Inches(11.7), Inches(1.05))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = "Manrope"
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_after = Pt(2)

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.name = "Manrope"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = TEXT_MUTED


# ---------------------------------------------------------------------------
# SLIDE BUILDERS
# ---------------------------------------------------------------------------

def build_slide_1_hero(prs: pptx.Presentation):
    """Slide 1: Hero Title Slide (Ultra-Bold, Clean, Iconic)."""
    slide = create_base_slide(prs)

    # Left content column
    left_x = Inches(0.9)

    # 1. Kicker Badge
    add_kicker_badge(slide, left_x, Inches(1.2), "COMMERCIAL PROPOSAL • INFO123 PROJECT", ACCENT_LAVENDER)

    # 2. Title & Tagline Textbox
    tb_title = slide.shapes.add_textbox(left_x, Inches(1.75), Inches(7.5), Inches(2.8))
    tf = tb_title.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_brand = tf.paragraphs[0]
    p_brand.text = "STAMP"
    p_brand.font.name = "Manrope"
    p_brand.font.size = Pt(64)
    p_brand.font.bold = True
    p_brand.font.color.rgb = ACCENT_LAVENDER
    p_brand.space_after = Pt(2)

    p_tag = tf.add_paragraph()
    p_tag.text = "PEEL. PRESS. TOAST."
    p_tag.font.name = "Manrope"
    p_tag.font.size = Pt(26)
    p_tag.font.bold = True
    p_tag.font.color.rgb = TEXT_WHITE
    p_tag.space_after = Pt(10)

    p_lead = tf.add_paragraph()
    p_lead.text = "The Single-Serve Breakfast Spread Discs for Hot Toast"
    p_lead.font.name = "Manrope"
    p_lead.font.size = Pt(16)
    p_lead.font.color.rgb = TEXT_MUTED

    # 3. Three Hero Pills
    badges_y = Inches(4.7)
    badges = [
        ("$5.00 NZD / Sheet", ACCENT_LAVENDER),
        ("12-Month Pantry Stable", ACCENT_BUTTER),
        ("No Jar Waste • Utensil-Free", ACCENT_BERRY),
    ]
    bx = left_x
    for label, col in badges:
        bw = Inches(len(label) * 0.11 + 0.5)
        add_kicker_badge(slide, bx, badges_y, label, text_color=col, width=bw)
        bx += bw + Inches(0.25)

    # 4. Presenter Info Card (Flat Solid Surface)
    card_pres = add_flat_card(slide, left_x, Inches(5.4), Inches(7.2), Inches(1.3))
    tb_pres = slide.shapes.add_textbox(left_x + Inches(0.3), Inches(5.55), Inches(6.6), Inches(1.0))
    tf_p = tb_pres.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0

    row1 = tf_p.paragraphs[0]
    row1.text = "PRESENTER: "
    row1.font.name = "Manrope"
    row1.font.size = Pt(12)
    row1.font.bold = True
    row1.font.color.rgb = ACCENT_LAVENDER
    run1 = row1.add_run()
    run1.text = "Jacob  |  INFO123 Business AI Project"
    run1.font.bold = True
    run1.font.color.rgb = TEXT_WHITE
    row1.space_after = Pt(4)

    row2 = tf_p.add_paragraph()
    row2.text = "LIVE PLATFORM: "
    row2.font.name = "Manrope"
    row2.font.size = Pt(11)
    row2.font.bold = True
    row2.font.color.rgb = ACCENT_BUTTER
    run2 = row2.add_run()
    run2.text = "stamp-spreads.vercel.app  •  github.com/JacobCrume/stamp-spreads"
    run2.font.bold = False
    run2.font.color.rgb = TEXT_SOFT

    # 5. Right Hero Image (Butter Pack Shot or Logo)
    pack_path = ROOT / "brand" / "explorations" / "flavours" / "butter.png"
    if not pack_path.exists():
        pack_path = ROOT / "brand" / "pack.png"
    if pack_path.exists():
        slide.shapes.add_picture(str(pack_path), Inches(8.7), Inches(1.5), width=Inches(3.8))

    # Speaker Notes
    slide.notes_slide.notes_text_frame.text = (
        "TITLE SLIDE (0:00–0:08)\n"
        "Kia ora. I'm Jacob, and this is Stamp: a New Zealand breakfast spread innovation "
        "engineered for hot toast. Over the next minute, I will present our product and "
        "market opportunity, followed by my personal reflection on building with generative AI."
    )


def build_slide_2_pitch1(prs: pptx.Presentation):
    """Slide 2: Pitch 1 — Product Innovation & Launch Range (0:08–0:34)."""
    slide = create_base_slide(prs)

    add_slide_header(
        slide,
        kicker="INVESTOR PITCH • PART 1 (30 SECONDS)",
        title="Product Innovation: Peel. Press. Toast.",
        subtitle="A calibrated 10 g disc on release film: no knife, no sticky jar, no morning wash-up.",
        kicker_color=ACCENT_LAVENDER,
    )

    card_y = Inches(2.0)
    card_h = Inches(4.9)

    # ------------------
    # LEFT CARD: The Problem & The Format Gesture
    # ------------------
    card_w1 = Inches(5.7)
    add_flat_card(slide, Inches(0.8), card_y, card_w1, card_h)

    tb_l = slide.shapes.add_textbox(Inches(1.15), card_y + Inches(0.35), Inches(5.0), card_h - Inches(0.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    p_title = tf_l.paragraphs[0]
    p_title.text = "The Out-of-Kitchen Friction"
    p_title.font.name = "Manrope"
    p_title.font.size = Pt(18)
    p_title.font.bold = True
    p_title.font.color.rgb = ACCENT_LAVENDER
    p_title.space_after = Pt(14)

    left_points = [
        ("The Jar Infrastructure Problem",
         "Eating toast away from home (office breakrooms, student halls, flat kitchens) demands cutlery, a sticky tub, and a sink to wash up. Cutlery-dependent spreads fail mobile consumers."),
        ("The Peel-and-Press Format",
         "Each Stamp delivers a calibrated 10 g disc mounted onto food-grade release film. Peel the disc, press it directly onto hot bread, and residual heat softens it into an even, velvety layer across the crumb."),
        ("12-Month Ambient Pantry Life",
         "Proprietary water-activity barrier formulation packaged in airtight card sheets provides verified 12-month ambient shelf stability without refrigeration."),
    ]

    for title, desc in left_points:
        p_pt = tf_l.add_paragraph()
        p_pt.text = "• " + title + "\n"
        p_pt.font.name = "Manrope"
        p_pt.font.size = Pt(12)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_WHITE
        p_pt.space_after = Pt(3)

        run_desc = p_pt.add_run()
        run_desc.text = desc
        run_desc.font.name = "Manrope"
        run_desc.font.size = Pt(11)
        run_desc.font.bold = False
        run_desc.font.color.rgb = TEXT_SOFT
        p_pt.space_after = Pt(10)

    # ------------------
    # RIGHT CARD: Four Launch Flavours
    # ------------------
    card_x2 = Inches(6.8)
    card_w2 = Inches(5.7)
    add_flat_card(slide, card_x2, card_y, card_w2, card_h)

    tb_r = slide.shapes.add_textbox(Inches(7.15), card_y + Inches(0.35), Inches(5.0), Inches(0.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "Four Launch Flavours"
    p_rt.font.name = "Manrope"
    p_rt.font.size = Pt(18)
    p_rt.font.bold = True
    p_rt.font.color.rgb = ACCENT_BUTTER

    flavours = [
        ("Salted Butter", "Cultured dairy spread (2 g salt / 78 g fat). Rich European style.", ACCENT_BUTTER),
        ("Wild Raspberry", "150 g fruit paste / 100 g. Natural pectin set, tart & vibrant.", ACCENT_BERRY),
        ("Yeast Extract", "80% autolysed yeast, 15.5% barley malt. Classic savoury umami.", ACCENT_LAVENDER),
        ("Roasted Peanut", "96% roasted peanuts + hard fat anti-oil separation barrier.", ACCENT_PEANUT),
    ]

    fy = card_y + Inches(0.9)
    for name, desc, col in flavours:
        fl_card = add_flat_card(slide, Inches(7.1), fy, Inches(5.1), Inches(0.68), bg_color=SURFACE_ELEVATED)
        tb_f = slide.shapes.add_textbox(Inches(7.25), fy + Inches(0.08), Inches(4.8), Inches(0.55))
        tf_f = tb_f.text_frame
        tf_f.word_wrap = True
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0

        p1 = tf_f.paragraphs[0]
        p1.text = name.upper() + "  "
        p1.font.name = "Manrope"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf_f.add_paragraph()
        p2.text = desc
        p2.font.name = "Manrope"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_SOFT
        fy += Inches(0.78)

    # Packaging shot below the flavours
    pack_path = ROOT / "brand" / "pack.png"
    if pack_path.exists():
        slide.shapes.add_picture(str(pack_path), Inches(8.3), Inches(5.4), height=Inches(1.4))

    # Speaker Notes
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
    """Slide 3: Pitch 2 — Market Opportunity & Unit Economics (0:34–0:58)."""
    slide = create_base_slide(prs)

    add_slide_header(
        slide,
        kicker="INVESTOR PITCH • PART 2 (30 SECONDS)",
        title="Market Opportunity & Unit Economics",
        subtitle="$341M New Zealand category, 24% revenue growth, and zero portion-format rivals.",
        kicker_color=ACCENT_BERRY,
    )

    # ------------------
    # TOP ROW: 3 Bold Stat Callouts
    # ------------------
    top_y = Inches(2.0)
    stat_h = Inches(1.25)
    stat_w = Inches(3.7)
    gap = Inches(0.3)
    sx = Inches(0.8)

    stats = [
        ("$341M", "Total NZ Spreads Category", "+24% growth from $275M (2022–2025)", ACCENT_LAVENDER),
        ("+29%", "Premium Tier Surge", "Surging from $88M to $113M NZD", ACCENT_BERRY),
        ("0", "Format Innovation Rivals", "154 existing products; zero peel-and-press", ACCENT_BUTTER),
    ]

    for num, headline, detail, col in stats:
        add_flat_card(slide, sx, top_y, stat_w, stat_h)
        tb_s = slide.shapes.add_textbox(sx + Inches(0.2), top_y + Inches(0.12), stat_w - Inches(0.4), stat_h - Inches(0.24))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0

        p_num = tf_s.paragraphs[0]
        p_num.text = num
        p_num.font.name = "Manrope"
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = col
        p_num.space_after = Pt(2)

        p_h = tf_s.add_paragraph()
        p_h.text = headline.upper()
        p_h.font.name = "Manrope"
        p_h.font.size = Pt(10)
        p_h.font.bold = True
        p_h.font.color.rgb = TEXT_WHITE
        p_h.space_after = Pt(1)

        p_d = tf_s.add_paragraph()
        p_d.text = detail
        p_d.font.name = "Manrope"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED

        sx += stat_w + gap

    # ------------------
    # BOTTOM ROW: 2 Split Cards (Economics & Chart)
    # ------------------
    bot_y = Inches(3.45)
    bot_h = Inches(3.45)

    # Left: Commercial Model & Margins
    add_flat_card(slide, Inches(0.8), bot_y, Inches(5.7), bot_h)

    tb_m = slide.shapes.add_textbox(Inches(1.15), bot_y + Inches(0.25), Inches(5.0), bot_h - Inches(0.5))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0

    p_mt = tf_m.paragraphs[0]
    p_mt.text = "Commercial Model & Margins"
    p_mt.font.name = "Manrope"
    p_mt.font.size = Pt(17)
    p_mt.font.bold = True
    p_mt.font.color.rgb = ACCENT_LAVENDER
    p_mt.space_after = Pt(8)

    econ_points = [
        ("Retail Pricing", "$5.00 NZD per 80 g sheet (8 stamps = 63¢ per toast portion). Highly accessible impulse price point for students and commuters."),
        ("Format Innovation Premium", "$6.25 NZD per 100 g. Commands a premium above the category's 90th percentile ($5.19/100g) because consumers buy convenience, not bulk volume."),
        ("Strong Unit Economics", "At an assumed $1.50 contract manufacturing benchmark and 35% supermarket margin, Stamp retains a healthy $1.75 gross contribution per sheet."),
    ]

    for title, desc in econ_points:
        p_pt = tf_m.add_paragraph()
        p_pt.text = "• " + title + ": "
        p_pt.font.name = "Manrope"
        p_pt.font.size = Pt(11)
        p_pt.font.bold = True
        p_pt.font.color.rgb = TEXT_WHITE
        p_pt.space_after = Pt(2)

        run = p_pt.add_run()
        run.text = desc
        run.font.name = "Manrope"
        run.font.size = Pt(10.5)
        run.font.bold = False
        run.font.color.rgb = TEXT_SOFT
        p_pt.space_after = Pt(6)

    # Right: Chart container with regenerated branded figure
    card_chart = add_flat_card(slide, Inches(6.8), bot_y, Inches(5.7), bot_h)
    fig_path = ROOT / "data" / "figures" / "02-spreads-revenue-by-tier-2022-vs-2025.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(6.95), bot_y + Inches(0.15), width=Inches(5.4))

    # Speaker Notes
    slide.notes_slide.notes_text_frame.text = (
        "PITCH SLIDE 2 (0:34–0:58)\n"
        "Our analysis of New Zealand breakfast retail sales shows spreads revenue grew 24% to "
        "341 million dollars, with the premium tier surging 29% to 113 million. Yet across 154 "
        "existing spread products, not one offers a single-serve portion format.\n\n"
        "Supermarket jars like Pic's or Fix & Fogg compete on bulk weight, but they are messy and stationary. "
        "At five dollars a sheet—just 63 cents a toast portion—Stamp captures premium convenience. With an assumed "
        "manufacturing cost of one-fifty, we retain a strong one-dollar-seventy-five gross margin per sheet. "
        "Stamp is ready to own portable breakfast."
    )


def build_slide_4_reflection1(prs: pptx.Presentation):
    """Slide 4: Reflection Q1 — Lessons in Working with Generative AI (1:00–1:55)."""
    slide = create_base_slide(prs)

    add_slide_header(
        slide,
        kicker="PERSONAL REFLECTION • PART 2 (STUDENT'S OWN VOICE)",
        title="Reflection Q1: Steering & Fact-Checking Generative AI",
        subtitle="Prompting architectures, context engineering, session partitioning, and verification.",
        kicker_color=ACCENT_BUTTER,
    )

    # Notice Pill: Talking-head requirement
    add_kicker_badge(
        slide,
        Inches(0.8),
        Inches(1.8),
        "TALKING-HEAD CUES • DELIVERED IN PERSONAL VOICE WITHOUT AI GENERATION",
        text_color=ACCENT_BUTTER,
        bg_color=SURFACE_PURPLE,
        width=Inches(6.2),
    )

    col_w = Inches(3.7)
    gap = Inches(0.3)
    left_x = Inches(0.8)
    card_y = Inches(2.3)
    card_h = Inches(4.6)

    columns = [
        ("Context & Steering", ACCENT_LAVENDER, [
            ("Role Personas & Negative Constraints", "Enforcing strict bans against health claims, therapeutic benefits, and certification badges to avoid marketing hallucinations."),
            ("Session Partitioning", "Isolating data cleaning, brand spec, and copywriting into modular sessions to eliminate context drift across complex multi-step workflows."),
            ("Locked Specification Artifact", "Maintaining a single source of truth across all tasks to ensure product metrics stayed rock-solid."),
        ]),
        ("Verification & Turning Point", ACCENT_BUTTER, [
            ("Auditing Raw Data Outliers", "Detecting aberrant price spikes (>$40) and uncleaned sales sums rather than blindly trusting unvalidated model aggregations."),
            ("The Specific Turning Point", "Catching hallucinated ambient table butter stability; forcing reformulation into cultured dairy spread to meet ambient shelf life."),
            ("Independent Fact-Checking", "Manually cross-referencing competitor shelf pricing directly against New World retail databases."),
        ]),
        ("Key Lessons Learned", ACCENT_BERRY, [
            ("AI as Drafter, Not Director", "Treating model outputs strictly as initial draft hypotheses that require empirical verification and human discernment."),
            ("Hybrid AI Architecture", "Pairing OpenRouter API customer support with locked system prompts and deterministic fallback logic."),
            ("What I Would Do Differently", "Establishing rigid data schemas and explicit verification tests before running exploratory generation."),
        ]),
    ]

    for title, col, points in columns:
        add_flat_card(slide, left_x, card_y, col_w, card_h)

        tb = slide.shapes.add_textbox(left_x + Inches(0.25), card_y + Inches(0.25), col_w - Inches(0.5), card_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Manrope"
        p_t.font.size = Pt(17)
        p_t.font.bold = True
        p_t.font.color.rgb = col
        p_t.space_after = Pt(12)

        for pt_title, pt_desc in points:
            p = tf.add_paragraph()
            p.text = "• " + pt_title + "\n"
            p.font.name = "Manrope"
            p.font.size = Pt(11.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE
            p.space_after = Pt(2)

            run = p.add_run()
            run.text = pt_desc
            run.font.name = "Manrope"
            run.font.size = Pt(10)
            run.font.bold = False
            run.font.color.rgb = TEXT_SOFT
            p.space_after = Pt(8)

        left_x += col_w + gap

    # Speaker Notes
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
    """Slide 5: Reflection Q2 — Critical Evaluation, AI Slop & Ethics (1:55–2:45)."""
    slide = create_base_slide(prs)

    add_slide_header(
        slide,
        kicker="PERSONAL REFLECTION • PART 2 (STUDENT'S OWN VOICE)",
        title="Reflection Q2: Authenticity, AI Slop & Knowledge Worker Ethics",
        subtitle="Combating generic marketing cliches, regulatory food liabilities, and human accountability.",
        kicker_color=ACCENT_BERRY,
    )

    # Notice Pill: Talking-head requirement
    add_kicker_badge(
        slide,
        Inches(0.8),
        Inches(1.8),
        "TALKING-HEAD CUES • DELIVERED IN PERSONAL VOICE WITHOUT AI GENERATION",
        text_color=ACCENT_BUTTER,
        bg_color=SURFACE_PURPLE,
        width=Inches(6.2),
    )

    col_w = Inches(3.7)
    gap = Inches(0.3)
    left_x = Inches(0.8)
    card_y = Inches(2.3)
    card_h = Inches(4.6)

    columns = [
        ("Combating 'AI Slop'", ACCENT_BERRY, [
            ("Stripping Marketing Clichés", "Actively rejecting hyperbolic corporate fluff ('revolutionizing breakfast journeys') in favor of plain, punchy facts: 'Peel. Press. Toast.'"),
            ("Authentic Physical Constraints", "Anchoring packaging in real industrial constraints (continuous deposit tooling, release film) rather than impossible AI mockups."),
            ("Deliberate Brand Personality", "Injecting bold, high-contrast visual identity and off-beat jingle tone to stand out from generic AI aesthetics."),
        ]),
        ("Regulatory & Legal Risks", ACCENT_BUTTER, [
            ("Food Hallucination Dangers", "Unchecked models frequently invent fake organic labels, false 'gluten-free' badges, or illegal therapeutic health claims."),
            ("Strict FSANZ Compliance", "Enforcing Food Standards Australia New Zealand labeling laws: distinguishing dairy spread from refrigerated table butter."),
            ("Allergen Responsibility", "Ensuring life-threatening peanut and gluten disclosures were prominent and never obscured by AI optimism."),
        ]),
        ("Ethics & Future Work", ACCENT_PEANUT, [
            ("Non-Delegable Accountability", "When deploying AI commercially, legal, moral, and customer accountability can never be outsourced to an algorithm."),
            ("Critical Thinking as Core Skill", "The primary value of the modern knowledge worker is skepticism, verification, taste, and boundary enforcement."),
            ("Human Agency", "Leveraging generative AI for execution velocity while retaining complete personal ownership of the final result."),
        ]),
    ]

    for title, col, points in columns:
        add_flat_card(slide, left_x, card_y, col_w, card_h)

        tb = slide.shapes.add_textbox(left_x + Inches(0.25), card_y + Inches(0.25), col_w - Inches(0.5), card_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Manrope"
        p_t.font.size = Pt(17)
        p_t.font.bold = True
        p_t.font.color.rgb = col
        p_t.space_after = Pt(12)

        for pt_title, pt_desc in points:
            p = tf.add_paragraph()
            p.text = "• " + pt_title + "\n"
            p.font.name = "Manrope"
            p.font.size = Pt(11.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE
            p.space_after = Pt(2)

            run = p.add_run()
            run.text = pt_desc
            run.font.name = "Manrope"
            run.font.size = Pt(10)
            run.font.bold = False
            run.font.color.rgb = TEXT_SOFT
            p.space_after = Pt(8)

        left_x += col_w + gap

    # Speaker Notes
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
    print(f"Successfully generated redesigned {OUT_PPTX}")


if __name__ == "__main__":
    main()
