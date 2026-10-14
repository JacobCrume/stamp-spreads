#!/usr/bin/env python3
"""Build business-plan/Stamp-business-plan.pdf from business-plan/copy.md.

Prose words are the section paragraphs only. Headings, figure captions,
image paths, and markdown tables are not counted. The build stops if that
count is outside 1,500–2,500.

Branding strictly honors the clean, flat, modern Stamp web platform:
- Minimalist Cover Page: Deep Night Ink (#240340) with centered STAMP wordmark,
  PEEL. PRESS. TOAST., and white Commercial Business Plan at the bottom.
- Section Divider Pages: Bold full-bleed colored divider pages cycling across
  the 4 authentic brand flavour palettes (Yeast, Butter, Raspberry, Peanut),
  with primary-colored title and concise subtitle, and brand footer.
- Content Pages: Pure white (#FFFFFF) background with dark legible ink typography
  (#1A1024), primary-colored section headings, clickable links (#6D28D9), and
  brand footer (STAMP wordmark on bottom left, page number on bottom right).
- Bold Elevated Containers: Distinct solid surface (#EEF2F6), solid 5pt primary
  accent bar, and crisp bold typography. Zero wireframe borders.
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image as PILImage
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COPY_PATH = HERE / "copy.md"
OUT_PATH = HERE / "Stamp-business-plan.pdf"
FONT_DIR = ROOT / "brand" / "fonts"

MIN_WORDS = 1500
MAX_WORDS = 2500

LEFT = 48
RIGHT = 48
FRAME_BOTTOM = 54
FRAME_TOP = 50

# 4 Authentic Flavour Schemes from website/src/lib/theme.svelte.ts
SCHEMES = [
    {
        "id": "yeast",
        "name": "Yeast Extract",
        "primary": HexColor("#E24BFF"),       # Electric Lavender
        "secondary": HexColor("#240340"),     # Deep Night Ink
        "tertiary": HexColor("#3B0764"),      # Deep Solid Purple
        "rgb": (226, 75, 255),
    },
    {
        "id": "butter",
        "name": "Golden Butter",
        "primary": HexColor("#FFD640"),       # Electric Butter Gold
        "secondary": HexColor("#4A3000"),     # Roasted Caramel Brown
        "tertiary": HexColor("#2D1D00"),      # Deep Umber
        "rgb": (255, 214, 64),
    },
    {
        "id": "raspberry",
        "name": "Wild Raspberry",
        "primary": HexColor("#FF467A"),       # Neon Wild Raspberry
        "secondary": HexColor("#460820"),     # Rich Berry
        "tertiary": HexColor("#2D0414"),      # Dark Berry Maroon
        "rgb": (255, 70, 122),
    },
    {
        "id": "peanut",
        "name": "Roasted Peanut",
        "primary": HexColor("#FF8C30"),       # Roasted Peanut Ochre
        "secondary": HexColor("#4E2408"),     # Deep Peanut Umber
        "tertiary": HexColor("#2D1403"),      # Dark Roasted Nut Brown
        "rgb": (255, 140, 48),
    },
]

# Section Titles & Concise Subtitles
SECTION_METADATA: dict[str, dict[str, str]] = {
    "Executive summary": {
        "title": "Executive Summary",
        "subtitle": "The Utensil-Free Breakfast Revolution",
    },
    "Product": {
        "title": "Product Specification",
        "subtitle": "Four Culinary Varieties & Continuous Deposit Scaling",
    },
    "Market": {
        "title": "Market Analysis",
        "subtitle": "New Zealand Supermarket Scan Data & Premium Growth",
    },
    "Competitors": {
        "title": "Competitor Benchmarking",
        "subtitle": "Bulk Commodity Jars vs Format Innovation",
    },
    "Customer and brand": {
        "title": "Customer & Brand Identity",
        "subtitle": "Modern Mobile Professionals & Bold Minimalist Design",
    },
    "Marketing": {
        "title": "Marketing & Acquisition Strategy",
        "subtitle": "Digital-First Launch & High-Impact Sampling",
    },
    "Operations": {
        "title": "Operations & Manufacturing",
        "subtitle": "Contract Manufacturing, Cleanroom Packaging & QA",
    },
    "Information": {
        "title": "Information Systems & Architecture",
        "subtitle": "Relational Data Architecture & Supply Chain KPIs",
    },
    "Website demo and customer support chatbot": {
        "title": "Digital Platform & AI Support",
        "subtitle": "Interactive SvelteKit Web App & Automated Assistant",
    },
    "First 90 days": {
        "title": "Commercial Roadmap: First 90 Days",
        "subtitle": "Pilot Production, Regulatory Compliance & Retail Launch",
    },
}

REQUIRED_INPUTS = [
    "audio/stamp-jingle.mp3",
    "audio/lyrics.txt",
    "diagrams/manufacturer.md",
    "diagrams/process.png",
    "diagrams/erd.png",
    "diagrams/process-notes.md",
    "diagrams/information-notes.md",
]


class SolidParagraph(Paragraph):
    """Do not split a short paragraph containing a URL awkwardly across pages."""

    def split(self, avail_width, avail_height):
        _width, height = self.wrap(avail_width, avail_height)
        if height <= avail_height:
            return [self]
        if avail_height > 680:
            return Paragraph.split(self, avail_width, avail_height)
        return []


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Manrope", str(FONT_DIR / "Manrope-400.ttf")))
    pdfmetrics.registerFont(TTFont("Manrope-Med", str(FONT_DIR / "Manrope-500.ttf")))
    pdfmetrics.registerFont(TTFont("Manrope-Semi", str(FONT_DIR / "Manrope-600.ttf")))
    pdfmetrics.registerFont(TTFont("Manrope-Bold", str(FONT_DIR / "Manrope-700.ttf")))
    pdfmetrics.registerFontFamily(
        "Manrope",
        normal="Manrope",
        bold="Manrope-Bold",
        italic="Manrope-Med",
        boldItalic="Manrope-Semi",
    )


def styles() -> dict[str, ParagraphStyle]:
    return {
        "body": ParagraphStyle(
            "body",
            fontName="Manrope",
            fontSize=10.0,
            leading=15.0,
            textColor=HexColor("#1A1024"),
            spaceBefore=0,
            spaceAfter=9,
            alignment=TA_LEFT,
        ),
        "cap": ParagraphStyle(
            "cap",
            fontName="Manrope-Semi",
            fontSize=8.8,
            leading=12.5,
            textColor=HexColor("#334155"),
            spaceBefore=0,
            spaceAfter=0,
            alignment=TA_CENTER,
        ),
    }


def parse_copy(text: str) -> list[dict]:
    """Return sections of prose, figure, and row blocks."""
    sections: list[dict] = []
    current: dict | None = None
    prose: list[str] = []
    lines = text.splitlines()
    index = 0

    def flush() -> None:
        nonlocal prose
        if current is None:
            prose = []
            return
        chunk = "\n".join(prose).strip()
        prose = []
        if chunk:
            current["blocks"].append(("prose", chunk))

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("## "):
            flush()
            current = {"title": stripped[3:].strip(), "blocks": []}
            sections.append(current)
            index += 1
            continue
        if stripped == ":::figure":
            flush()
            if current is None:
                raise SystemExit("figure block before any section")
            index += 1
            fields: dict[str, str] = {}
            while index < len(lines) and lines[index].strip() != ":::":
                raw = lines[index].strip()
                if ":" in raw:
                    key, value = raw.split(":", 1)
                    fields[key.strip()] = value.strip()
                index += 1
            current["blocks"].append(("figure", fields))
            index += 1
            continue
        if stripped == ":::row":
            flush()
            if current is None:
                raise SystemExit("row block before any section")
            index += 1
            items: list[dict[str, str]] = []
            pending: dict[str, str] = {}
            while index < len(lines) and lines[index].strip() != ":::":
                raw = lines[index].strip()
                if raw.startswith("src:"):
                    if pending.get("src") and pending.get("caption"):
                        items.append(pending)
                    pending = {"src": raw.split(":", 1)[1].strip()}
                elif raw.startswith("caption:"):
                    pending["caption"] = raw.split(":", 1)[1].strip()
                index += 1
            if pending.get("src") and pending.get("caption"):
                items.append(pending)
            current["blocks"].append(("row", items))
            index += 1
            continue
        if stripped.startswith("# "):
            index += 1
            continue
        prose.append(line)
        index += 1
    flush()
    return sections


def prose_word_counts(sections: list[dict]) -> tuple[int, dict[str, int]]:
    per: dict[str, int] = {}
    total = 0
    for section in sections:
        parts: list[str] = []
        for block in section["blocks"]:
            if block[0] != "prose":
                continue
            for line in block[1].splitlines():
                if line.strip().startswith("|"):
                    continue
                parts.append(line)
        raw = "\n".join(parts)
        raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)
        raw = raw.replace("**", "").replace("*", "").replace("`", "")
        words = raw.split()
        per[section["title"]] = len(words)
        total += len(words)
    return total, per


def xml_text(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def soften(match: re.Match[str]) -> str:
        url = match.group(0)
        punct = ""
        while url and url[-1] in ".,;:!?)":
            punct = url[-1] + punct
            url = url[:-1]

        plain = url.replace("&amp;", "&")
        limit = 480

        def wide(value: str) -> float:
            return pdfmetrics.stringWidth(value, "Manrope", 10.0)

        if wide(plain) <= limit:
            return f'<a href="{url}" color="#6D28D9"><u>{url}</u></a>{punct}'
        pieces = url.split("/")
        lines: list[str] = []
        current = pieces[0]
        for piece in pieces[1:]:
            addition = "/" + piece
            trial = (current + addition).replace("&amp;", "&")
            if current and wide(trial) > limit:
                lines.append(current)
                current = addition
            else:
                current += addition
        if current:
            lines.append(current)
        display = "<br/>".join(lines)
        return f'<a href="{url}" color="#6D28D9"><u>{display}</u></a>{punct}'

    # Make raw URLs clickable hyperlinks
    text = re.sub(r"https?://[^\s<]+", soften, text)
    # Bold text
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def body_paragraph(text: str, style: ParagraphStyle):
    xml = xml_text(text)
    kind = SolidParagraph if "http" in xml else Paragraph
    return kind(xml, style)


def prepare_image(src: Path, dest: Path) -> tuple[int, int]:
    image = PILImage.open(src)
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        image = image.convert("RGBA")
        base = PILImage.new("RGBA", image.size, (238, 242, 246, 255))
        flat = PILImage.alpha_composite(base, image).convert("RGB")
    else:
        flat = image.convert("RGB")
    flat.save(dest, "PNG")
    return flat.size


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
# FLOWABLES & PAGE LAYOUTS
# ---------------------------------------------------------------------------

class MinimalCover(Flowable):
    """Ultra-minimalist cover page strictly matching user specifications."""

    def __init__(self, mark_path: str, px_w: int, px_h: int):
        super().__init__()
        self.mark_path = mark_path
        self.px_w = px_w
        self.px_h = px_h

    def wrap(self, avail_width, avail_height):
        self.avail_width = avail_width
        self.avail_height = avail_height
        return avail_width, avail_height

    def draw(self):
        canv = self.canv
        W = self.avail_width
        H = self.avail_height
        cx = W / 2

        # Centered STAMP Wordmark
        mark_w = 400
        mark_h = mark_w * self.px_h / self.px_w
        center_y = H / 2
        mark_y = center_y + 10
        mark_x = cx - mark_w / 2
        canv.drawImage(
            self.mark_path,
            mark_x,
            mark_y,
            mark_w,
            mark_h,
            mask="auto",
            preserveAspectRatio=True,
        )

        # Centered Tagline
        tag_y = mark_y - 36
        canv.setFillColor(HexColor("#E24BFF"))
        canv.setFont("Manrope-Bold", 24)
        canv.drawCentredString(cx, tag_y, "PEEL. PRESS. TOAST.")

        # Bottom text in white
        canv.setFillColor(white)
        canv.setFont("Manrope-Semi", 14)
        canv.drawCentredString(cx, 48, "Commercial Business Plan")


class CleanSectionPage(Flowable):
    """Dedicated full-bleed section divider page with wrapping primary title & subtitle."""

    def __init__(self, title: str, subtitle: str, scheme: dict):
        super().__init__()
        self.scheme = scheme
        title_style = ParagraphStyle(
            f"sec_title_{scheme['id']}",
            fontName="Manrope-Bold",
            fontSize=32,
            leading=38,
            textColor=scheme["primary"],
            spaceBefore=0,
            spaceAfter=14,
            alignment=TA_LEFT,
        )
        sub_style = ParagraphStyle(
            f"sec_sub_{scheme['id']}",
            fontName="Manrope-Semi",
            fontSize=15,
            leading=21,
            textColor=scheme["primary"],
            spaceBefore=0,
            spaceAfter=0,
            alignment=TA_LEFT,
        )
        self.title_p = Paragraph(xml_text(title), title_style)
        self.sub_p = Paragraph(xml_text(subtitle), sub_style) if subtitle else None

    def wrap(self, avail_width, avail_height):
        self.avail_width = avail_width
        self.avail_height = avail_height
        _w1, self.t_h = self.title_p.wrap(avail_width, avail_height)
        self.s_h = 0
        if self.sub_p:
            _w2, self.s_h = self.sub_p.wrap(avail_width, avail_height)
        return avail_width, avail_height

    def draw(self):
        canv = self.canv
        # Vertically align around 58% of available height
        total_h = self.t_h + (14 + self.s_h if self.sub_p else 0)
        y_top = (self.avail_height * 0.58) + total_h / 2

        self.title_p.drawOn(canv, 0, y_top - self.t_h)
        if self.sub_p:
            self.sub_p.drawOn(canv, 0, y_top - self.t_h - 14 - self.s_h)


class CleanFigureBlock(Flowable):
    """Bold, elevated visual block on white canvas."""

    def __init__(self, path: str, caption: str, max_height: float, pref_width: float | None, scheme: dict):
        super().__init__()
        self.path = path
        self.caption = caption
        self.max_height = max_height
        self.pref_width = pref_width
        self.scheme = scheme
        with PILImage.open(path) as image:
            self.px_w, self.px_h = image.size

    def wrap(self, avail_width, avail_height):
        self.avail_width = avail_width
        card_w = avail_width if self.pref_width is None else min(avail_width, self.pref_width)
        pad = 14
        inner_w = card_w - 2 * pad
        inner_max_h = self.max_height - 42
        scale = min(inner_w / self.px_w, inner_max_h / self.px_h)
        self.draw_w = self.px_w * scale
        self.draw_h = self.px_h * scale

        self.card_w = self.draw_w + 2 * pad
        cap_style = ParagraphStyle(
            f"fig_cap_{self.scheme['id']}",
            fontName="Manrope-Semi",
            fontSize=8.8,
            leading=12.5,
            textColor=HexColor("#334155"),
            alignment=TA_CENTER,
        )
        self.paragraph = Paragraph(xml_text(self.caption), cap_style)
        _cw, self.cap_h = self.paragraph.wrap(self.card_w - 20, 800)
        self.card_h = self.draw_h + pad + 16 + self.cap_h + 6
        return avail_width, self.card_h

    def draw(self):
        canv = self.canv
        cx = (self.avail_width - self.card_w) / 2
        W = self.card_w
        H = self.card_h
        r = 12

        canv.saveState()
        # 1. Bold elevated card surface (Slate 100 #EEF2F6)
        canv.setFillColor(HexColor("#EEF2F6"))
        canv.roundRect(cx, 0, W, H, r, stroke=0, fill=1)

        # 2. Bold top accent bar in section primary color
        bar_h = 5
        canv.setFillColor(self.scheme["primary"])
        canv.roundRect(cx, H - bar_h, W, bar_h, 2.5, stroke=0, fill=1)

        # 3. Image centered with generous padding
        img_x = cx + (W - self.draw_w) / 2
        img_y = self.cap_h + 12
        canv.drawImage(
            self.path,
            img_x,
            img_y,
            self.draw_w,
            self.draw_h,
            mask="auto",
            preserveAspectRatio=True,
        )

        # 4. Caption
        self.paragraph.drawOn(canv, cx + 10, 8)
        canv.restoreState()


class CleanImageRow(Flowable):
    """Bold elevated row of images on white canvas."""

    def __init__(self, items: list[tuple[str, str]], max_height: float, scheme: dict):
        super().__init__()
        self.items = items
        self.max_height = max_height
        self.scheme = scheme
        self.sizes = []
        for p, _c in items:
            with PILImage.open(p) as img:
                self.sizes.append(img.size)

    def wrap(self, avail_width, avail_height):
        count = len(self.items)
        gap = 14
        col_w = (avail_width - gap * (count - 1)) / count
        pad = 12
        inner_w = col_w - 2 * pad
        inner_max_h = self.max_height - 42
        self.cols = []
        row_h = 0
        cap_style = ParagraphStyle(
            f"row_cap_{self.scheme['id']}",
            fontName="Manrope-Semi",
            fontSize=8.2,
            leading=11.5,
            textColor=HexColor("#334155"),
            alignment=TA_CENTER,
        )

        for (path, caption), (px_w, px_h) in zip(self.items, self.sizes):
            scale = min(inner_w / px_w, inner_max_h / px_h)
            draw_w = px_w * scale
            draw_h = px_h * scale
            paragraph = Paragraph(xml_text(caption), cap_style)
            _cw, cap_h = paragraph.wrap(col_w - 16, 800)
            card_h = draw_h + pad + 16 + cap_h + 6
            row_h = max(row_h, card_h)
            self.cols.append((path, draw_w, draw_h, paragraph, cap_h, col_w, card_h))

        self.gap = gap
        self.avail_width = avail_width
        self.row_h = row_h
        return avail_width, row_h

    def draw(self):
        canv = self.canv
        x = 0
        bar_h = 5
        r = 12
        for path, draw_w, draw_h, paragraph, cap_h, col_w, card_h in self.cols:
            cy = self.row_h - card_h
            canv.saveState()
            # 1. Bold elevated card surface
            canv.setFillColor(HexColor("#EEF2F6"))
            canv.roundRect(x, cy, col_w, card_h, r, stroke=0, fill=1)

            # 2. Bold top accent bar
            canv.setFillColor(self.scheme["primary"])
            canv.roundRect(x, cy + card_h - bar_h, col_w, bar_h, 2.5, stroke=0, fill=1)

            # 3. Image
            img_x = x + (col_w - draw_w) / 2
            img_y = cy + cap_h + 12
            canv.drawImage(
                path,
                img_x,
                img_y,
                draw_w,
                draw_h,
                mask="auto",
                preserveAspectRatio=True,
            )

            paragraph.drawOn(canv, x + 8, cy + 8)
            canv.restoreState()
            x += col_w + self.gap


# ---------------------------------------------------------------------------
# PAGE BACKGROUND DRAWERS
# ---------------------------------------------------------------------------

def draw_cover_bg(canv, _doc):
    canv.saveState()
    canv.setFillColor(HexColor("#240340"))
    canv.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canv.restoreState()


def make_section_bg_drawer(scheme: dict, mark_path: str):
    def drawer(canv, doc):
        canv.saveState()
        W, H = A4
        canv.setFillColor(scheme["secondary"])
        canv.rect(0, 0, W, H, stroke=0, fill=1)

        # Footer: STAMP wordmark on bottom left, page number on bottom right
        mark_w = 54
        mark_h = 13.2
        canv.drawImage(mark_path, LEFT, 26, mark_w, mark_h, mask="auto", preserveAspectRatio=True)

        canv.setFillColor(scheme["primary"])
        canv.setFont("Manrope-Bold", 9)
        canv.drawRightString(W - RIGHT, 28, f"{doc.page}")
        canv.restoreState()
    return drawer


def make_content_bg_drawer(scheme: dict, mark_path: str):
    def drawer(canv, doc):
        canv.saveState()
        W, H = A4
        canv.setFillColor(white)
        canv.rect(0, 0, W, H, stroke=0, fill=1)

        # Footer: STAMP wordmark in section primary on bottom left, page on right
        mark_w = 54
        mark_h = 13.2
        canv.drawImage(mark_path, LEFT, 26, mark_w, mark_h, mask="auto", preserveAspectRatio=True)

        canv.setFillColor(scheme["primary"])
        canv.setFont("Manrope-Bold", 9)
        canv.drawRightString(W - RIGHT, 28, f"{doc.page}")
        canv.restoreState()
    return drawer


def resolve_src(src: str) -> Path:
    path = Path(src)
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"missing or empty image: {path}")
    return path


def check_inputs(copy_text: str) -> None:
    if "WAIT_FOR_INPUT" in copy_text or "TODO" in copy_text:
        raise SystemExit("copy.md still has placeholders; PDF not written")
    missing = []
    for relative in REQUIRED_INPUTS:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            missing.append(relative)
    if missing:
        raise SystemExit("missing inputs, PDF not written: " + ", ".join(missing))


def visual_flowables(kind: str, payload, work: Path, scheme: dict) -> list:
    if kind == "figure":
        src = resolve_src(payload["src"])
        caption = payload.get("caption", "").strip()
        if not caption:
            raise SystemExit(f"figure missing a caption: {src}")
        flat = work / f"fig-{len(list(work.iterdir()))}.png"
        prepare_image(src, flat)
        pref = float(payload["width"]) if payload.get("width") else None
        max_h = float(payload["max-height"]) if payload.get("max-height") else 380
        return [
            Spacer(1, 8),
            CleanFigureBlock(str(flat), caption, max_h, pref, scheme),
            Spacer(1, 12),
        ]
    if kind == "row":
        prepared = []
        for item in payload:
            src = resolve_src(item["src"])
            flat = work / f"row-{len(list(work.iterdir()))}.png"
            prepare_image(src, flat)
            prepared.append((str(flat), item["caption"]))
        return [Spacer(1, 8), CleanImageRow(prepared, 220, scheme), Spacer(1, 12)]
    raise SystemExit(f"unknown block {kind}")


def build_story(sections: list[dict], work: Path, marks: dict[str, tuple[str, int, int]]) -> list:
    story: list = []

    # 1. Cover Page
    cover_path, px_w, px_h = marks["yeast"]
    story.append(MinimalCover(cover_path, px_w, px_h))

    # 2. Iterate each section
    for sec_idx, section in enumerate(sections):
        scheme = SCHEMES[sec_idx % len(SCHEMES)]
        scheme_id = scheme["id"]
        meta = SECTION_METADATA.get(section["title"], {
            "title": section["title"],
            "subtitle": "",
        })

        # Section Divider Page (dedicated full-bleed colored divider)
        story.append(NextPageTemplate(f"section_{scheme_id}"))
        story.append(PageBreak())
        story.append(CleanSectionPage(
            title=meta["title"],
            subtitle=meta["subtitle"],
            scheme=scheme,
        ))

        # Switch to Content Page Template for this section
        story.append(NextPageTemplate(f"content_{scheme_id}"))
        story.append(PageBreak())

        # Section Heading on Content Page
        title_style = ParagraphStyle(
            f"title_{scheme_id}",
            fontName="Manrope-Bold",
            fontSize=20,
            leading=25,
            textColor=scheme["primary"],
            spaceBefore=0,
            spaceAfter=14,
            alignment=TA_LEFT,
        )
        story.append(Paragraph(xml_text(meta["title"]), title_style))

        # Process Section Blocks
        pending = None
        for index, (kind, payload) in enumerate(section["blocks"]):
            if kind == "prose":
                if pending is not None:
                    story.append(pending)
                    pending = None
                paragraphs = [part.strip() for part in payload.split("\n\n") if part.strip()]
                nxt = (
                    section["blocks"][index + 1][0]
                    if index + 1 < len(section["blocks"])
                    else ""
                )
                hold = nxt in {"figure", "row"} and len(paragraphs) > 0
                body = paragraphs[:-1] if hold else paragraphs
                for part in body:
                    story.append(body_paragraph(part, styles()["body"]))
                if hold:
                    pending = body_paragraph(paragraphs[-1], styles()["body"])
                continue

            visuals = visual_flowables(kind, payload, work, scheme)
            if pending is not None:
                story.append(KeepTogether([pending, *visuals]))
                pending = None
            else:
                story.extend(visuals)

        if pending is not None:
            story.append(pending)

    return story


def main() -> int:
    if not COPY_PATH.is_file() or COPY_PATH.stat().st_size == 0:
        raise SystemExit(f"missing copy: {COPY_PATH}")
    copy_text = COPY_PATH.read_text(encoding="utf-8")
    check_inputs(copy_text)
    sections = parse_copy(copy_text)
    if not sections:
        raise SystemExit("copy.md has no sections")
    total, per_section = prose_word_counts(sections)
    for title, count in per_section.items():
        print(f"{count:4d}  {title}")
    print(f"{total:4d}  TOTAL")
    if total < MIN_WORDS or total > MAX_WORDS:
        print(
            f"error: prose word count {total} is outside {MIN_WORDS}–{MAX_WORDS}",
            file=sys.stderr,
        )
        return 1

    register_fonts()
    with tempfile.TemporaryDirectory(prefix="stamp-plan-") as temporary:
        work = Path(temporary)

        # Generate recolored anti-aliased wordmarks for each scheme
        marks: dict[str, tuple[str, int, int]] = {}
        for s in SCHEMES:
            mark_p = work / f"mark_{s['id']}.png"
            w, h = create_recolored_wordmark(ROOT / "brand" / "logo.png", mark_p, s["rgb"])
            marks[s["id"]] = (str(mark_p), w, h)

        tmp_out = work / "plan.pdf"
        frame_h = A4[1] - FRAME_BOTTOM - FRAME_TOP
        frame_w = A4[0] - LEFT - RIGHT

        document = BaseDocTemplate(
            str(tmp_out),
            pagesize=A4,
            title="STAMP Commercial Business Plan",
            author="Jacob",
        )

        full_frame = Frame(LEFT, FRAME_BOTTOM, frame_w, frame_h, id="full", showBoundary=0)
        content_frame = Frame(LEFT, FRAME_BOTTOM, frame_w, frame_h, id="content", showBoundary=0)

        templates = [
            PageTemplate(id="cover", frames=[full_frame], onPage=draw_cover_bg)
        ]
        for s in SCHEMES:
            sid = s["id"]
            mark_path = marks[sid][0]
            templates.append(
                PageTemplate(
                    id=f"section_{sid}",
                    frames=[full_frame],
                    onPage=make_section_bg_drawer(s, mark_path),
                )
            )
            templates.append(
                PageTemplate(
                    id=f"content_{sid}",
                    frames=[content_frame],
                    onPage=make_content_bg_drawer(s, mark_path),
                )
            )
        document.addPageTemplates(templates)

        story = build_story(sections, work, marks)
        document.build(story)
        OUT_PATH.write_bytes(tmp_out.read_bytes())

    print(f"Successfully generated {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
