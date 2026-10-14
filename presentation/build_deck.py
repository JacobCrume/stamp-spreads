#!/usr/bin/env python3
"""Generate presentation/Stamp-pitch.pptx for INFO123 Video Presentation.

Strict brand fidelity and design pacing:
1. Cover Slide:
   - Deep Night Ink (#240340) full-bleed canvas.
   - Centered STAMP wordmark.
   - Centered tagline "PEEL. PRESS. TOAST." in Electric Lavender (#E24BFF).
   - Bottom center text "Commercial Business Pitch" in pure white (#FFFFFF).
   - Zero other elements on the cover.
2. Solution Section Product Showcase:
   - All 4 flavours' packaging shown side-by-side up front with very little text.
3. Natural Pacing (Zero Hero Moment Overload):
   - Measured metric callouts (54pt instead of screaming 80pt).
   - Dynamic rhythm: problem setup -> 4-pack product reveal -> physical gesture ->
     category data -> single clear tier chart -> whitespace & margin -> operations ->
     thoughtful AI reflections.
4. Bottom Center Wordmark on Every Content Slide:
   - Recolored to that slide's primary accent color.
5. Strict 3 Colors Plus Neutral Rule:
   - Cover & Ethics: Yeast (#240340 / #E24BFF / #FFFFFF)
   - Problem & Steering: Raspberry (#460820 / #FF467A / #FFFFFF)
   - Solution & Operations: Butter (#4A3000 / #FFD640 / #FFFFFF)
   - Market Opportunity & Economics: Peanut (#4E2408 / #FF8C30 / #FFFFFF)
"""

from __future__ import annotations

import tempfile
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from PIL import Image as PILImage
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parent.parent
OUT_PPTX = ROOT / "presentation" / "Stamp-pitch.pptx"
FONT_DIR = ROOT / "brand" / "fonts"

F_BOLD = fm.FontProperties(fname=str(FONT_DIR / "Manrope-700.ttf"))
F_SEMI = fm.FontProperties(fname=str(FONT_DIR / "Manrope-600.ttf"))
F_MED = fm.FontProperties(fname=str(FONT_DIR / "Manrope-500.ttf"))

SCHEMES = {
    "yeast": {
        "secondary": RGBColor(36, 3, 64),      # #240340 (Deep Night Ink)
        "primary": RGBColor(226, 75, 255),     # #E24BFF (Electric Lavender)
        "white": RGBColor(255, 255, 255),
        "primary_rgb": (226, 75, 255),
        "secondary_hex": "#240340",
        "primary_hex": "#E24BFF",
    },
    "butter": {
        "secondary": RGBColor(74, 48, 0),      # #4A3000 (Roasted Caramel Brown)
        "primary": RGBColor(255, 214, 64),     # #FFD640 (Electric Butter Gold)
        "white": RGBColor(255, 255, 255),
        "primary_rgb": (255, 214, 64),
        "secondary_hex": "#4A3000",
        "primary_hex": "#FFD640",
    },
    "raspberry": {
        "secondary": RGBColor(70, 8, 32),      # #460820 (Rich Berry)
        "primary": RGBColor(255, 70, 122),     # #FF467A (Neon Wild Raspberry)
        "white": RGBColor(255, 255, 255),
        "primary_rgb": (255, 70, 122),
        "secondary_hex": "#460820",
        "primary_hex": "#FF467A",
    },
    "peanut": {
        "secondary": RGBColor(78, 36, 8),      # #4E2408 (Deep Peanut Umber)
        "primary": RGBColor(255, 140, 48),     # #FF8C30 (Roasted Peanut Ochre)
        "white": RGBColor(255, 255, 255),
        "primary_rgb": (255, 140, 48),
        "secondary_hex": "#4E2408",
        "primary_hex": "#FF8C30",
    },
}


def prepare_wordmarks(work_dir: Path) -> dict[str, Path]:
    """Generate recolored STAMP wordmarks with crisp transparency."""
    src = ROOT / "brand" / "explorations" / "wordmark-ink.png"
    im = PILImage.open(src).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]

    paths = {}
    for key, s in SCHEMES.items():
        out = np.zeros_like(arr)
        rgb = s["primary_rgb"]
        out[:, :, 0] = rgb[0]
        out[:, :, 1] = rgb[1]
        out[:, :, 2] = rgb[2]
        out[:, :, 3] = alpha
        dest = work_dir / f"wordmark_{key}.png"
        PILImage.fromarray(out).save(dest, "PNG")
        paths[key] = dest
    return paths


def generate_figures(work_dir: Path) -> dict[str, Path]:
    """Generate composite of 4 flavour packs and palette-matched charts."""
    # 1. Composite of all 4 flavours' packaging in a row
    flavour_dir = ROOT / "brand" / "explorations" / "flavours"
    packs = [
        PILImage.open(flavour_dir / "butter.png"),
        PILImage.open(flavour_dir / "raspberry.png"),
        PILImage.open(flavour_dir / "yeast.png"),
        PILImage.open(flavour_dir / "peanut.png"),
    ]
    target_h = 750
    target_w = int(target_h * (1200 / 1600))  # 562
    gap = 64
    total_w = 4 * target_w + 3 * gap
    composite = PILImage.new("RGBA", (total_w, target_h), (0, 0, 0, 0))
    for i, p in enumerate(packs):
        resized = p.resize((target_w, target_h), PILImage.Resampling.LANCZOS)
        x = i * (target_w + gap)
        composite.paste(resized, (x, 0), resized)
    four_packs_path = work_dir / "four_packs_row.png"
    composite.save(four_packs_path, "PNG")


    # 2. Spreads Category Tier Growth Chart on Peanut (#4E2408) - ZERO OUTLINES
    sales_csv = ROOT / "data" / "sales-clean.csv"
    frame = pd.read_csv(sales_csv)
    spreads = frame[frame["Category"] == "Spreads"].copy()
    spreads["year"] = spreads["Date"].str.slice(0, 4)
    part = spreads[spreads["year"].isin(["2022", "2025"])]
    totals = (
        part.groupby(["year", "Price Tier"])["Revenue (Thousands NZD)"].sum().unstack("year")
        / 1000
    )
    totals = totals.reindex(["Value", "Standard", "Premium"])

    bg_peanut = "#4E2408"
    primary_peanut = "#FF8C30"
    white_hex = "#FFFFFF"

    fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=200)
    fig.patch.set_facecolor(bg_peanut)
    ax.set_facecolor(bg_peanut)

    positions = np.arange(3)
    width = 0.35

    # Solid bars with no outlines (edgecolor='none', linewidth=0)
    rects1 = ax.bar(
        positions - width / 2,
        totals["2022"],
        width=width,
        label="2022 Revenue",
        color="#FFFFFF",
        edgecolor="none",
        linewidth=0,
        zorder=3,
    )
    rects2 = ax.bar(
        positions + width / 2,
        totals["2025"],
        width=width,
        label="2025 Revenue",
        color=primary_peanut,
        edgecolor="none",
        linewidth=0,
        zorder=3,
    )

    for rect in rects1:
        h = rect.get_height()
        ax.annotate(
            f"${h:.1f}M",
            (rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontproperties=F_BOLD,
            fontsize=9.5,
            color=white_hex,
        )

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(
            f"${h:.1f}M",
            (rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontproperties=F_BOLD,
            fontsize=9.5,
            color=primary_peanut,
        )

    ax.set_xticks(positions)
    ax.set_xticklabels(["Value", "Standard", "Premium"])
    for label in ax.get_xticklabels():
        label.set_fontproperties(F_BOLD)
        label.set_fontsize(11)
        label.set_color(white_hex)

    ax.set_ylabel("Revenue (Million NZD)", fontproperties=F_SEMI, fontsize=9.5, color=white_hex, labelpad=8)
    ax.grid(axis="y", linestyle="--", alpha=0.2, color=white_hex, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(axis="y", colors=white_hex)
    for label in ax.get_yticklabels():
        label.set_fontproperties(F_MED)
        label.set_fontsize(9)
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, max(totals.max()) * 1.22)

    legend = ax.legend(frameon=False, loc="upper left")
    for text in legend.get_texts():
        text.set_fontproperties(F_SEMI)
        text.set_fontsize(9.5)
        text.set_color(white_hex)

    fig.tight_layout()
    tier_path = work_dir / "chart_tier_peanut.png"
    fig.savefig(tier_path, dpi=200, facecolor=bg_peanut)
    plt.close(fig)

    # 3. Process Flow Diagram on Butter (#4A3000) - SOLID CARDS, ZERO OUTLINES
    bg_butter = "#4A3000"
    primary_butter = "#FFD640"
    ink_butter = "#241600"

    fig, ax = plt.subplots(figsize=(8.2, 3.2), dpi=200)
    fig.patch.set_facecolor(bg_butter)
    ax.set_facecolor(bg_butter)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)
    ax.axis("off")

    steps = [
        ("1. DEPOSIT", "Continuous 10g disc\non release liner"),
        ("2. CUT", "Precision rotary\ndie-cutting"),
        ("3. QA GATE", "Weight check\n10g ± 0.5g"),
        ("4. PACK", "8-disc card into\nhermetic envelope"),
    ]

    for i, (title, desc) in enumerate(steps):
        x = 3 + i * 24.5
        y = 8
        w = 21
        h = 24

        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.8,rounding_size=2",
            facecolor=primary_butter,
            edgecolor="none",
            linewidth=0,
        )
        ax.add_patch(rect)

        ax.text(
            x + w / 2,
            y + h - 5.5,
            title,
            ha="center",
            va="center",
            fontproperties=F_BOLD,
            fontsize=10.5,
            color=ink_butter,
        )

        ax.text(
            x + w / 2,
            y + 8,
            desc,
            ha="center",
            va="center",
            fontproperties=F_SEMI,
            fontsize=8.5,
            color=ink_butter,
            multialignment="center",
        )

        if i < len(steps) - 1:
            ax.annotate(
                "",
                xy=(x + w + 3.2, y + h / 2),
                xytext=(x + w + 0.3, y + h / 2),
                arrowprops=dict(arrowstyle="->", color=primary_butter, lw=2.0),
            )

    fig.tight_layout()
    process_path = work_dir / "diagram_process_butter.png"
    fig.savefig(process_path, dpi=200, facecolor=bg_butter)
    plt.close(fig)

    return {
        "four_packs": four_packs_path,
        "tier": tier_path,
        "process": process_path,
    }


def create_slide_canvas(prs: pptx.Presentation, bg_color: RGBColor):
    """Full-bleed flat canvas without borders or shadows."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()
    return slide


def add_bottom_wordmark(slide, mark_path: Path):
    """Anchor the STAMP wordmark subtly in the bottom center of the slide."""
    w = Inches(1.5)
    h = Inches(0.367)
    left = (Inches(13.333) - w) / 2
    top = Inches(6.75)
    slide.shapes.add_picture(str(mark_path), left, top, width=w, height=h)


def add_statement_slide(
    prs: pptx.Presentation,
    scheme_key: str,
    mark_paths: dict[str, Path],
    line1: str,
    line2: str,
    line3: str | None = None,
    line1_color: str = "primary",
    line2_color: str = "white",
    line3_color: str = "primary",
    line1_size: int = 22,
    line2_size: int = 44,
    line3_size: int = 22,
    notes: str = "",
):
    """Minimal, container-free slide with 1-3 lines of confident text."""
    s = SCHEMES[scheme_key]
    slide = create_slide_canvas(prs, s["secondary"])

    left = Inches(1.3)
    width = Inches(10.7)
    height = Inches(4.0)
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

    add_bottom_wordmark(slide, mark_paths[scheme_key])

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    return slide


def add_metric_slide(
    prs: pptx.Presentation,
    scheme_key: str,
    mark_paths: dict[str, Path],
    metric_number: str,
    headline: str,
    detail: str,
    notes: str = "",
):
    """Well-proportioned metric slide avoiding hero overload (54pt metric)."""
    s = SCHEMES[scheme_key]
    slide = create_slide_canvas(prs, s["secondary"])

    left = Inches(1.3)
    top = Inches(2.1)
    width = Inches(10.7)
    height = Inches(4.0)

    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p1 = tf.paragraphs[0]
    p1.text = metric_number
    p1.font.name = "Manrope"
    p1.font.size = Pt(54)
    p1.font.bold = True
    p1.font.color.rgb = s["primary"]
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = headline
    p2.font.name = "Manrope"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = s["white"]
    p2.space_after = Pt(12)

    p3 = tf.add_paragraph()
    p3.text = detail
    p3.font.name = "Manrope"
    p3.font.size = Pt(20)
    p3.font.bold = False
    p3.font.color.rgb = s["primary"]

    add_bottom_wordmark(slide, mark_paths[scheme_key])

    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    return slide


def add_figure_slide(
    prs: pptx.Presentation,
    scheme_key: str,
    mark_paths: dict[str, Path],
    headline: str,
    detail: str,
    img_path: Path,
    img_width: float = 6.8,
    img_top: float = 2.4,
    notes: str = "",
):
    """Slide pairing 2 lines of text with a centered figure."""
    s = SCHEMES[scheme_key]
    slide = create_slide_canvas(prs, s["secondary"])

    # Header text
    left = Inches(1.3)
    top = Inches(0.9)
    width = Inches(10.7)
    height = Inches(1.4)

    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p1 = tf.paragraphs[0]
    p1.text = headline
    p1.font.name = "Manrope"
    p1.font.size = Pt(34)
    p1.font.bold = True
    p1.font.color.rgb = s["white"]
    p1.space_after = Pt(6)

    p2 = tf.add_paragraph()
    p2.text = detail
    p2.font.name = "Manrope"
    p2.font.size = Pt(20)
    p2.font.bold = False
    p2.font.color.rgb = s["primary"]

    # Centered Figure
    fig_w = Inches(img_width)
    fig_x = (prs.slide_width - fig_w) / 2
    slide.shapes.add_picture(str(img_path), fig_x, Inches(img_top), width=fig_w)

    add_bottom_wordmark(slide, mark_paths[scheme_key])

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

    mark_paths = prepare_wordmarks(work_dir)
    figs = generate_figures(work_dir)

    # -----------------------------------------------------------------------
    # SLIDE 1: Cover (Identical to PDF Page 1: Centered Wordmark, Tagline, Bottom Pitch)
    # -----------------------------------------------------------------------
    s_yeast = SCHEMES["yeast"]
    slide1 = create_slide_canvas(prs, s_yeast["secondary"])

    # Centered Wordmark
    mark_w = Inches(5.8)
    mark_h = Inches(1.419)
    mark_x = (prs.slide_width - mark_w) / 2
    mark_y = Inches(2.3)
    slide1.shapes.add_picture(str(mark_paths["yeast"]), mark_x, mark_y, width=mark_w, height=mark_h)

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
        "TITLE (0:00–0:07)\n"
        "Kia ora. I'm Jacob, and this is Stamp: a New Zealand breakfast spread innovation engineered for hot toast."
    )

    # -----------------------------------------------------------------------
    # SECTION 1: The Problem (Scheme: Raspberry #460820 / #FF467A / #FFFFFF)
    # -----------------------------------------------------------------------

    # Slide 2: The Core Problem
    add_statement_slide(
        prs,
        scheme_key="raspberry",
        mark_paths=mark_paths,
        line1="The Problem",
        line2="Jars Require Infrastructure.",
        line3="Table knives, kitchen benches, and hot running water.",
        line1_size=22,
        line2_size=46,
        line3_size=22,
        notes="PROBLEM (0:07–0:14)\nEating toast away from a full residential kitchen is fundamentally broken.",
    )

    # Slide 3: Who Fails
    add_statement_slide(
        prs,
        scheme_key="raspberry",
        mark_paths=mark_paths,
        line1="Eating Away from Home is Broken.",
        line2="Desk workers, commuters, and students in dorms.",
        line3="Nobody carries a 500g sticky glass jar.",
        line1_color="white",
        line2_color="primary",
        line3_color="white",
        line1_size=44,
        line2_size=26,
        line3_size=22,
        notes="WHO FAILS (0:14–0:21)\nIn an office or student flat, nobody wants to lug a sticky jar, hunt for a knife, and wash it in a shared sink.",
    )

    # Slide 4: The Unmet Need
    add_statement_slide(
        prs,
        scheme_key="raspberry",
        mark_paths=mark_paths,
        line1="The Unmet Need.",
        line2="Consumers abandon toast for dry cereal bars.",
        line3="Portability has never existed for real breakfast spreads.",
        line1_color="white",
        line2_color="primary",
        line3_color="white",
        line1_size=44,
        line2_size=26,
        line3_size=22,
        notes="UNMET NEED (0:21–0:28)\nBecause jars are tethered to kitchens, consumers compromise on dry bars or skip breakfast altogether.",
    )

    # -----------------------------------------------------------------------
    # SECTION 2: Solution & Product Showcase (Scheme: Butter #4A3000 / #FFD640 / #FFFFFF)
    # -----------------------------------------------------------------------

    # Slide 5: The Solution — All 4 Flavours Up Front with Very Little Text
    add_figure_slide(
        prs,
        scheme_key="butter",
        mark_paths=mark_paths,
        headline="The Solution.",
        detail="10 g spread discs on release film.",
        img_path=figs["four_packs"],
        img_width=10.2,
        img_top=2.45,
        notes="SOLUTION SHOWCASE (0:28–0:36)\nStamp reinvents the format: calibrated 10-gram spread discs on release film across four launch flavours.",
    )

    # Slide 6: The Physical Gesture (Zero Cutlery / Thermal Melt)
    add_statement_slide(
        prs,
        scheme_key="butter",
        mark_paths=mark_paths,
        line1="Zero Cutlery. Pure Physics.",
        line2="Residual toast heat melts the disc in seconds.",
        line3="Peel off the liner. Press onto hot toast. Zero utensils or mess.",
        line1_color="white",
        line2_color="primary",
        line3_color="white",
        line1_size=44,
        line2_size=26,
        line3_size=20,
        notes="GESTURE (0:36–0:43)\nYou press the disc onto hot bread, and residual thermal energy melts it evenly across the crumb in seconds.",
    )

    # Slide 7: Form Factor & Shelf Stability
    add_statement_slide(
        prs,
        scheme_key="butter",
        mark_paths=mark_paths,
        line1="12-Month Ambient Life.",
        line2="High-stability emulsification for room temperature.",
        line3="Hermetically sealed 8-stamp card sheets for pantry and bag.",
        line1_color="white",
        line2_color="primary",
        line3_color="white",
        line1_size=44,
        line2_size=24,
        line3_size=20,
        notes="STABILITY & FORMAT (0:43–0:50)\nEngineered for room-temperature pantry and bag storage with full 12-month ambient stability.",
    )

    # -----------------------------------------------------------------------
    # SECTION 3: Market Opportunity & Unit Economics (Scheme: Peanut #4E2408 / #FF8C30 / #FFFFFF)
    # -----------------------------------------------------------------------

    # Slide 8: Market Scale Metric (Measured, 54pt)
    add_metric_slide(
        prs,
        scheme_key="peanut",
        mark_paths=mark_paths,
        metric_number="$341M Category",
        headline="New Zealand Spreads Market.",
        detail="+24% category revenue growth across 2022–2025.",
        notes="MARKET SCALE (0:50–0:57)\nCleaned supermarket scan data shows the New Zealand spreads category expanded 24% to 341 million dollars.",
    )

    # Slide 9: Premium Shift Visual (Tier Growth Chart)
    add_figure_slide(
        prs,
        scheme_key="peanut",
        mark_paths=mark_paths,
        headline="Premium Spreads Surging +29%.",
        detail="Consumers trading up from commodity tiers into quality formats.",
        img_path=figs["tier"],
        img_width=6.6,
        img_top=2.35,
        notes="PREMIUM SURGE (0:57–1:05)\nPremium branded spreads surged 29% to 113 million dollars, massively outperforming commodity tiers.",
    )

    # Slide 10: Competitive Void
    add_metric_slide(
        prs,
        scheme_key="peanut",
        mark_paths=mark_paths,
        metric_number="0 Rivals",
        headline="Across 154 Supermarket Spreads.",
        detail="Zero single-serve or utensil-free formats in NZ retail.",
        notes="COMPETITIVE VOID (1:05–1:12)\nAcross 154 supermarket spreads, every single product is a jar. Not one offers a utensil-free portion format.",
    )

    # Slide 11: Unit Economics
    add_metric_slide(
        prs,
        scheme_key="peanut",
        mark_paths=mark_paths,
        metric_number="35% Gross Margin",
        headline="$5.00 Retail • $1.75 Margin per Pack.",
        detail="63¢ per serving on an assumed $1.50 contract packaging cost.",
        notes="UNIT ECONOMICS (1:12–1:19)\nAt 63 cents a serving, we retain a strong $1.75 gross margin to fund distribution and marketing.",
    )

    # -----------------------------------------------------------------------
    # SECTION 4: Operations & Lean Scaling (Scheme: Butter #4A3000 / #FFD640 / #FFFFFF)
    # -----------------------------------------------------------------------

    # Slide 12: Co-Manufacturing Process Figure
    add_figure_slide(
        prs,
        scheme_key="butter",
        mark_paths=mark_paths,
        headline="Contract Co-Manufacturing.",
        detail="Continuous deposit tooling onto food-grade release liner.",
        img_path=figs["process"],
        img_width=8.0,
        img_top=2.5,
        notes="MANUFACTURING (1:19–1:27)\nProduction leverages existing contract rotary-die deposition lines, eliminating custom factory tooling.",
    )

    # Slide 13: Lean Capex Pilot
    add_statement_slide(
        prs,
        scheme_key="butter",
        mark_paths=mark_paths,
        line1="Lean Capex Pilot.",
        line2="Partnering with Auckland contract food packagers.",
        line3="Zero heavy machinery outlay required for market entry.",
        line1_color="white",
        line2_color="primary",
        line3_color="white",
        line1_size=44,
        line2_size=24,
        line3_size=20,
        notes="LEAN PILOT (1:27–1:35)\nBy partnering with established contract packers in Auckland, we validate consumer demand with minimal capex.",
    )

    # -----------------------------------------------------------------------
    # SECTION 5: Reflection 1 — AI Steering & Verification (Scheme: Raspberry #460820 / #FF467A / #FFFFFF)
    # -----------------------------------------------------------------------

    # Slide 14: Negative Constraints
    add_statement_slide(
        prs,
        scheme_key="raspberry",
        mark_paths=mark_paths,
        line1="Negative Constraints.",
        line2="Banning AI Marketing Hype.",
        line3="Explicit negative prompts barred fake badges and health claims.",
        line1_size=22,
        line2_size=46,
        line3_size=22,
        notes="CONSTRAINTS (1:35–1:48)\nIn steering AI, I enforced strict negative prompt constraints against fake certification badges and medical health claims.",
    )

    # Slide 15: Modular Session Architecture
    add_statement_slide(
        prs,
        scheme_key="raspberry",
        mark_paths=mark_paths,
        line1="Modular Architecture.",
        line2="Separating data, branding, and copy eliminated context drift.",
        line1_color="white",
        line2_color="primary",
        line1_size=46,
        line2_size=24,
        notes="ARCHITECTURE (1:48–2:00)\nI partitioned distinct sessions for data cleaning, branding, and copy to prevent context rot and hallucinated metrics.",
    )

    # Slide 16: The Turning Point: Catching Spoilage
    add_statement_slide(
        prs,
        scheme_key="raspberry",
        mark_paths=mark_paths,
        line1="Catching Dairy Instability.",
        line2="AI assumed table butter could sit ambiently.",
        line3="Human intervention forced high-stability emulsion.",
        line1_color="white",
        line2_color="primary",
        line3_color="white",
        line1_size=44,
        line2_size=26,
        line3_size=22,
        notes="TURNING POINT (2:00–2:12)\nMy pivotal turning point was catching an unrealistic AI claim that dairy butter could sit ambiently without spoilage.",
    )

    # Slide 17: AI as Drafter, Not Director
    add_statement_slide(
        prs,
        scheme_key="raspberry",
        mark_paths=mark_paths,
        line1="AI as Drafter, Not Director.",
        line2="Auditing raw scan outliers and verifying live supermarket shelves.",
        line1_color="white",
        line2_color="primary",
        line1_size=44,
        line2_size=24,
        notes="VERIFICATION (2:12–2:22)\nI audited raw scan data outliers and manually verified shelf prices on New World instead of trusting model summaries.",
    )

    # -----------------------------------------------------------------------
    # SECTION 6: Reflection 2 — Authenticity, AI Slop & Ethics (Scheme: Yeast #240340 / #E24BFF / #FFFFFF)
    # -----------------------------------------------------------------------

    # Slide 18: Combating AI Slop
    add_statement_slide(
        prs,
        scheme_key="yeast",
        mark_paths=mark_paths,
        line1="Combating AI Slop.",
        line2="Stripping corporate buzzwords for plain human facts.",
        line3="Peel. Press. Toast.",
        line1_color="white",
        line2_color="primary",
        line3_color="white",
        line1_size=46,
        line2_size=26,
        line3_size=24,
        notes="AUTHENTICITY (2:22–2:30)\nTo combat AI slop, I stripped corporate clichés and grounded packaging in real continuous deposit tooling.",
    )

    # Slide 19: Zero Hallucination Tolerance
    add_statement_slide(
        prs,
        scheme_key="yeast",
        mark_paths=mark_paths,
        line1="Zero Hallucination Tolerance.",
        line2="Strict FSANZ food laws and mandatory allergen warnings.",
        line1_color="white",
        line2_color="primary",
        line1_size=46,
        line2_size=24,
        notes="REGULATION (2:30–2:38)\nIn food and beverage, AI hallucinations are a severe legal hazard. I enforced strict FSANZ compliance and allergen safety.",
    )

    # Slide 20: Human Accountability
    add_statement_slide(
        prs,
        scheme_key="yeast",
        mark_paths=mark_paths,
        line1="Accountability Remains Human.",
        line2="Moral, regulatory, and commercial ownership cannot be outsourced.",
        line1_color="white",
        line2_color="primary",
        line1_size=46,
        line2_size=24,
        notes="ETHICS & WRAP (2:38–2:45)\nGenerative AI accelerates velocity, but human skepticism, taste, discernment, and moral ownership remain essential.",
    )

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"Successfully generated {OUT_PPTX} (20 well-paced, visual slides)")


def main():
    with tempfile.TemporaryDirectory(prefix="stamp-slides-") as tmpdir:
        build_presentation(Path(tmpdir))


if __name__ == "__main__":
    main()
