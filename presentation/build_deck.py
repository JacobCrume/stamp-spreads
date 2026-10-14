#!/usr/bin/env python3
"""Generate presentation/Stamp-pitch.pptx for INFO123 Video Presentation.

Meets all brief specifications:
- 16:9 widescreen layout
- Slide 1: Title Slide (STAMP, Jacob, INFO123)
- Slide 2: Pitch 1 — Product Innovation & Launch Range (30 seconds)
- Slide 3: Pitch 2 — Market Opportunity & Competitive Advantage (30 seconds)
- Slide 4: Reflection Q1 — Lessons in Prompting, Steering & Fact-Checking (Structured shell)
- Slide 5: Reflection Q2 — Critical Evaluation of AI, Authenticity & Ethics (Structured shell)
"""

from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent.parent
OUT_PPTX = ROOT / "presentation" / "Stamp-pitch.pptx"

# Colors
COLOR_DARK_PURPLE = RGBColor(59, 7, 100)     # #3B0764
COLOR_LIGHT_PURPLE = RGBColor(226, 75, 255)  # #E24BFF
COLOR_TEXT_DARK = RGBColor(26, 16, 36)       # #1A1024
COLOR_TEXT_MUTED = RGBColor(99, 67, 128)     # #634380
COLOR_BG_CARD = RGBColor(251, 247, 255)      # #FBF7FF
COLOR_BORDER = RGBColor(235, 212, 255)       # #EBD4FF
COLOR_WHITE = RGBColor(255, 255, 255)


def add_header(slide, title_text: str, subtitle_text: str, kicker: str = ""):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.3))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if kicker:
        p_kicker = tf.paragraphs[0]
        p_kicker.text = kicker.upper()
        p_kicker.font.size = Pt(11)
        p_kicker.font.bold = True
        p_kicker.font.color.rgb = COLOR_LIGHT_PURPLE
        p_kicker.space_after = Pt(2)
        p_title = tf.add_paragraph()
    else:
        p_title = tf.paragraphs[0]

    p_title.text = title_text
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_DARK_PURPLE
    p_title.space_after = Pt(2)

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED


def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Purple Background)
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_DARK_PURPLE
    bg1.line.color.rgb = COLOR_DARK_PURPLE

    # Accent line
    accent = slide1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.6), Inches(1.5), Inches(0.08)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = COLOR_LIGHT_PURPLE
    accent.line.color.rgb = COLOR_LIGHT_PURPLE

    # Title box
    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.5), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "STAMP"
    p0.font.size = Pt(54)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_LIGHT_PURPLE
    p0.space_after = Pt(6)

    p1 = tf1.add_paragraph()
    p1.text = "Peel. Press. Toast."
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "The Single-Serve Breakfast Spread for Hot Toast"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(220, 195, 245)
    p2.space_after = Pt(36)

    p3 = tf1.add_paragraph()
    p3.text = "Presenter: Jacob  |  Course: INFO123 Business AI Project  |  Date: October 2026"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(200, 175, 230)

    # Logo on right
    logo_path = ROOT / "brand" / "logo.png"
    if logo_path.exists():
        slide1.shapes.add_picture(str(logo_path), Inches(8.8), Inches(2.3), width=Inches(3.3))

    slide1.notes_slide.notes_text_frame.text = (
        "TITLE SLIDE (0:00–0:10)\n"
        "Welcome. I'm Jacob, and this is Stamp: a New Zealand breakfast spread innovation "
        "designed for hot toast. Over the next minute, I'll walk you through our product "
        "and market opportunity, followed by my personal reflection on building with generative AI."
    )

    # -------------------------------------------------------------
    # SLIDE 2: Pitch 1 — Product Innovation & Launch Range (0:10–0:30)
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(
        slide2,
        "Product Innovation: Peel. Press. Toast.",
        "A single-serve 10 g disc on release film: no knife, no open jar, no morning wash-up.",
        "INVESTOR PITCH — PART 1 (30 SECONDS)"
    )

    # Left Card: How it works & core benefits
    card1 = slide2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.1)
    )
    card1.fill.solid()
    card1.fill.fore_color.rgb = COLOR_BG_CARD
    card1.line.color.rgb = COLOR_BORDER

    tb2_left = slide2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.2), Inches(4.7))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "The Problem & The Gesture"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(8)

    points = [
        "Jars Require Infrastructure: Toast eaten away from home (office desks, flats, university halls) demands a knife, an open tub, and a sink to wash up.",
        "The Stamp Solution: A thin 10 g disc of real spread on release film nested in a pocketable card sheet. Peel off, press onto hot toast, and residual heat softens it into an even layer in seconds.",
        "12-Month Pantry Life: Industrial formulation and sealed release film provide 12 months ambient shelf life without refrigeration."
    ]
    for pt in points:
        title, body = pt.split(": ", 1)
        p = tf2_l.add_paragraph()
        p.text = "• " + title + ": "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(6)
        run = p.add_run()
        run.text = body
        run.font.bold = False
        run.font.size = Pt(12)
        run.font.color.rgb = COLOR_TEXT_DARK

    # Right Card: Launch Range & Pack shot
    card2 = slide2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1)
    )
    card2.fill.solid()
    card2.fill.fore_color.rgb = COLOR_BG_CARD
    card2.line.color.rgb = COLOR_BORDER

    tb2_right = slide2.shapes.add_textbox(Inches(7.2), Inches(2.0), Inches(5.0), Inches(2.2))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "Four Launch Flavours"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(6)

    fl_points = [
        "Salted Butter: Cultured dairy spread (2 g salt / 78 g fat).",
        "Raspberry: Slow-cooked whole fruit paste (150 g fruit / 100 g).",
        "Yeast Extract: Savory umami paste (80% yeast, 15.5% barley malt).",
        "Peanut: 96% roasted peanuts + hard fat anti-separation stabilizer."
    ]
    for fp in fl_points:
        p = tf2_r.add_paragraph()
        p.text = "✔ " + fp
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(3)

    # Insert pack shot
    pack_path = ROOT / "brand" / "pack.png"
    if pack_path.exists():
        slide2.shapes.add_picture(str(pack_path), Inches(7.5), Inches(4.3), height=Inches(2.3))

    slide2.notes_slide.notes_text_frame.text = (
        "PITCH SLIDE 1 (0:10–0:30)\n"
        "Eating toast away from a kitchen is broken: you have to carry a heavy jar, find a knife, "
        "and wash it in an office or hall sink. Stamp fixes this with a peel-and-press spread disc. "
        "You peel a 10-gram portion off the release film, press it directly onto hot toast, and the "
        "heat melts it into an even layer in seconds. We launch with four distinct flavours: Salted Butter, "
        "Raspberry, Yeast extract, and Peanut—all packaged in an 8-stamp card sheet with a 12-month pantry shelf life."
    )

    # -------------------------------------------------------------
    # SLIDE 3: Pitch 2 — Market Opportunity & Unit Economics (0:30–1:00)
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(
        slide3,
        "Market Opportunity & Competitive Advantage",
        "$341M category with 24% growth, premium tier expansion, and zero portion-format rivals.",
        "INVESTOR PITCH — PART 2 (30 SECONDS)"
    )

    # Left: Economics & Market stats
    card3_left = slide3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.1)
    )
    card3_left.fill.solid()
    card3_left.fill.fore_color.rgb = COLOR_BG_CARD
    card3_left.line.color.rgb = COLOR_BORDER

    tb3_left = slide3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.2), Inches(4.7))
    tf3_l = tb3_left.text_frame
    tf3_l.word_wrap = True

    p = tf3_l.paragraphs[0]
    p.text = "Verified NZ Breakfast Data"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(8)

    mkt_points = [
        "Category Expansion: New Zealand spreads revenue grew 24% from $275M (2022) to $341M NZD (2025). Premium spreads grew fastest (+29%, reaching $113M).",
        "The Format Vacuum: Across 154 spread names in the market, not a single brand offers a single-serve, peel-and-press format.",
        "Unit Economics: Priced at $5.00 NZD per 80 g sheet ($6.25/100g). Above jar medians ($2.15/100g) because buyers pay for portion control and pocket convenience.",
        "Attractive Margins: At assumed $1.50 contract manufacturing cost and 35% retail margin, Stamp retains $1.75 contribution per sheet."
    ]
    for pt in mkt_points:
        title, body = pt.split(": ", 1)
        p = tf3_l.add_paragraph()
        p.text = "• " + title + ": "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(5)
        run = p.add_run()
        run.text = body
        run.font.bold = False
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_TEXT_DARK

    # Right: Chart figure
    fig_path = ROOT / "data" / "figures" / "02-spreads-revenue-by-tier-2022-vs-2025.png"
    if fig_path.exists():
        slide3.shapes.add_picture(str(fig_path), Inches(6.9), Inches(1.8), width=Inches(5.6))

    slide3.notes_slide.notes_text_frame.text = (
        "PITCH SLIDE 2 (0:30–1:00)\n"
        "Our analysis of New Zealand breakfast retail sales shows spreads grew 24% to 341 million dollars, "
        "with the premium tier expanding to 113 million. Yet out of 154 existing spread products, not one "
        "offers a portion format. Jars like Fix and Fogg or Pic's are cheaper per 100 grams, but they're "
        "bulky and messy. At 5 dollars a sheet, or 63 cents a toast portion, Stamp captures premium convenience "
        "for commuters, students, and desk workers. With a healthy 1.75 contribution margin per sheet, Stamp is "
        "ready to lead an entirely new format in breakfast."
    )

    # -------------------------------------------------------------
    # SLIDE 4: Reflection Q1 — Working with Generative AI (1:00–1:55)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(
        slide4,
        "Reflection Q1: Lessons in Working with Generative AI",
        "Prompting techniques, context engineering, session management, and verification.",
        "PERSONAL REFLECTION — PART 2 (STUDENT'S OWN WORDS)"
    )

    # Guidance notice box
    nb4 = slide4.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.55)
    )
    nb4.fill.solid()
    nb4.fill.fore_color.rgb = RGBColor(254, 242, 242)
    nb4.line.color.rgb = RGBColor(239, 68, 68)
    tf_nb4 = nb4.text_frame
    p_nb4 = tf_nb4.paragraphs[0]
    p_nb4.text = "CRITICAL BRIEF REQUIREMENT: Deliver in your personal voice. AI assistance was strictly prohibited for reflection text."
    p_nb4.font.size = Pt(10)
    p_nb4.font.bold = True
    p_nb4.font.color.rgb = RGBColor(185, 28, 28)

    # 3 Structured reflection columns
    col_w = Inches(3.7)
    gap = Inches(0.3)
    left_margin = Inches(0.8)

    # Col 1: Context & Steering
    col1 = slide4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left_margin, Inches(2.5), col_w, Inches(4.4)
    )
    col1.fill.solid()
    col1.fill.fore_color.rgb = COLOR_BG_CARD
    col1.line.color.rgb = COLOR_BORDER
    tf_c1 = col1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "Context & Steering"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(8)

    prompts_c1 = [
        "Prompting Beyond Defaults: How role personas, explicit negative constraints, and output formats prevented generic responses.",
        "Session Partitioning: Why separating data cleaning, visual identity, and copy prevented context drift across 13 stages.",
        "Prompting Artifact: Carrying locked spec decisions forward rather than re-prompting."
    ]
    for item in prompts_c1:
        p = tf_c1.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(6)

    # Col 2: Fact-Checking & Turning Point
    col2 = slide4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left_margin + col_w + gap, Inches(2.5), col_w, Inches(4.4)
    )
    col2.fill.solid()
    col2.fill.fore_color.rgb = COLOR_BG_CARD
    col2.line.color.rgb = COLOR_BORDER
    tf_c2 = col2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "Verification & Pivotal Moment"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(8)

    prompts_c2 = [
        "Catching Raw Data Errors: Detecting aberrant price outliers (>$40) and missing revenues in raw dataset rather than trusting uncleaned sums.",
        "The Specific Turning Point: A concrete moment when AI output hallucinated or failed, and the exact steps taken to correct it.",
        "Independent Sourcing: Verifying real competitor shelf prices directly on New World instead of relying on AI guesses."
    ]
    for item in prompts_c2:
        p = tf_c2.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(6)

    # Col 3: Lessons for Future
    col3 = slide4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left_margin + (col_w + gap) * 2, Inches(2.5), col_w, Inches(4.4)
    )
    col3.fill.solid()
    col3.fill.fore_color.rgb = COLOR_BG_CARD
    col3.line.color.rgb = COLOR_BORDER
    tf_c3 = col3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "Key Lessons Learned"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(8)

    prompts_c3 = [
        "AI as Junior Drafter, Not Director: Treating model outputs as hypotheses that require rigorous empirical validation.",
        "Hybrid AI Architecture: Integrating OpenRouter API with a locked system prompt and instant deterministic fallback to eliminate hallucinations.",
        "What I Would Do Differently: Specific adjustments for future enterprise AI workflows."
    ]
    for item in prompts_c3:
        p = tf_c3.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(6)

    slide4.notes_slide.notes_text_frame.text = (
        "REFLECTION Q1 (1:00–1:55)\n"
        "[Jacob's personal reflection: speak directly to camera about your AI steering experience.]\n"
        "Key speaking cues:\n"
        "1. Discuss how you structured sessions to avoid context rot across tasks.\n"
        "2. Detail the pivotal moment where you caught a major AI mistake (e.g. invalid pricing assumptions, "
        "unrealistic manufacturing claims, or raw data price spikes) and how you corrected it.\n"
        "3. Share the single most important lesson you will carry into future professional AI projects."
    )

    # -------------------------------------------------------------
    # SLIDE 5: Reflection Q2 — Critical Evaluation & AI Ethics (1:55–2:50)
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(
        slide5,
        "Reflection Q2: Critical Evaluation of AI, Authenticity & Ethics",
        "Combating 'AI slop', regulatory liability, and ethics for future knowledge workers.",
        "PERSONAL REFLECTION — PART 2 (STUDENT'S OWN WORDS)"
    )

    # Guidance notice box
    nb5 = slide5.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.55)
    )
    nb5.fill.solid()
    nb5.fill.fore_color.rgb = RGBColor(254, 242, 242)
    nb5.line.color.rgb = RGBColor(239, 68, 68)
    tf_nb5 = nb5.text_frame
    p_nb5 = tf_nb5.paragraphs[0]
    p_nb5.text = "CRITICAL BRIEF REQUIREMENT: Deliver in your personal voice. AI assistance was strictly prohibited for reflection text."
    p_nb5.font.size = Pt(10)
    p_nb5.font.bold = True
    p_nb5.font.color.rgb = RGBColor(185, 28, 28)

    # 3 Structured reflection columns
    # Col 1: Fighting AI Slop
    col1_5 = slide5.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left_margin, Inches(2.5), col_w, Inches(4.4)
    )
    col1_5.fill.solid()
    col1_5.fill.fore_color.rgb = COLOR_BG_CARD
    col1_5.line.color.rgb = COLOR_BORDER
    tf_c1_5 = col1_5.text_frame
    tf_c1_5.word_wrap = True
    p = tf_c1_5.paragraphs[0]
    p.text = "Combating 'AI Slop'"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(8)

    slop_points = [
        "Rejecting Generic Fluff: AI defaults to superlative marketing cliches ('revolutionizing breakfast'). Enforcing concise, plain-spoken prose made Stamp authentic.",
        "Authentic Physical Design: Anchoring packaging in real industrial constraints (foil release liners, ambient butterfat stability) rather than impossible fantasy designs.",
        "Human Taste & Tone: Deliberately choosing an off-beat, energetic sound and visual palette."
    ]
    for item in slop_points:
        p = tf_c1_5.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(6)

    # Col 2: Regulatory & Legal Liability
    col2_5 = slide5.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left_margin + col_w + gap, Inches(2.5), col_w, Inches(4.4)
    )
    col2_5.fill.solid()
    col2_5.fill.fore_color.rgb = COLOR_BG_CARD
    col2_5.line.color.rgb = COLOR_BORDER
    tf_c2_5 = col2_5.text_frame
    tf_c2_5.word_wrap = True
    p = tf_c2_5.paragraphs[0]
    p.text = "Regulatory & Legal Risks"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(8)

    reg_points = [
        "The Hallucination Danger: Left unconstrained, AI frequently invents fake organic labels, false 'gluten-free' badges, or illegal medical claims.",
        "Strict Enforced Bans: Banning health and therapeutic claims; legally distinguishing 'spread' from refrigerated table butter under FSANZ standards.",
        "Allergen Responsibility: Ensuring life-threatening peanut and gluten disclosures were never obscured by AI optimism."
    ]
    for item in reg_points:
        p = tf_c2_5.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(6)

    # Col 3: Ethical Implications for Knowledge Workers
    col3_5 = slide5.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left_margin + (col_w + gap) * 2, Inches(2.5), col_w, Inches(4.4)
    )
    col3_5.fill.solid()
    col3_5.fill.fore_color.rgb = COLOR_BG_CARD
    col3_5.line.color.rgb = COLOR_BORDER
    tf_c3_5 = col3_5.text_frame
    tf_c3_5.word_wrap = True
    p = tf_c3_5.paragraphs[0]
    p.text = "Ethics & Future Work"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_PURPLE
    p.space_after = Pt(8)

    eth_points = [
        "Accountability Remains Human: When a business deploys AI, legal, moral, and customer accountability cannot be offloaded to an algorithm.",
        "Value of Critical Thinking: The essential role of the knowledge worker is skepticism, verification, and boundary-setting.",
        "Personal Perspective: What it means to work ethically alongside AI without surrendering personal agency or judgment."
    ]
    for item in eth_points:
        p = tf_c3_5.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_after = Pt(6)

    slide5.notes_slide.notes_text_frame.text = (
        "REFLECTION Q2 (1:55–2:50)\n"
        "[Jacob's personal reflection: speak directly to camera on authenticity and ethics.]\n"
        "Key speaking cues:\n"
        "1. How did you actively prevent AI slop from entering Stamp's branding and copy?\n"
        "2. Address the severe ethical/legal risks of AI generating food claims (allergens, false certifications).\n"
        "3. Conclude with your personal stance as a future knowledge worker on ethics and responsibility."
    )

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"Presentation saved to {OUT_PPTX}")


if __name__ == "__main__":
    build_presentation()
