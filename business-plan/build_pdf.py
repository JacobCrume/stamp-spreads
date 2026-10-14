#!/usr/bin/env python3
"""Build business-plan/Stamp-business-plan.pdf from business-plan/copy.md.

Prose words are the section paragraphs only. Headings, figure captions,
image paths, and markdown tables are not counted. The build stops if that
count is outside 1,500–2,500.
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    HRFlowable,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


class SolidParagraph(Paragraph):
    """Do not split a short paragraph, so a wrapped URL is not left on the next page."""

    def split(self, avail_width, avail_height):
        _width, height = self.wrap(avail_width, avail_height)
        if height <= avail_height:
            return [self]
        if avail_height > 680:
            return Paragraph.split(self, avail_width, avail_height)
        return []

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COPY_PATH = HERE / "copy.md"
OUT_PATH = HERE / "Stamp-business-plan.pdf"
FONT_DIR = ROOT / "brand" / "fonts"

PURPLE = HexColor("#E24BFF")
INK = HexColor("#3B0764")
TEXT = HexColor("#1A1024")
MUTED = HexColor("#4A3560")
BG_PURPLE = (226, 75, 255)

MIN_WORDS = 1500
MAX_WORDS = 2500

LEFT = 46
RIGHT = 46
FRAME_BOTTOM = 52
FRAME_TOP = 48

REQUIRED_INPUTS = [
    "audio/stamp-jingle.mp3",
    "audio/lyrics.txt",
    "diagrams/manufacturer.md",
    "diagrams/process.png",
    "diagrams/erd.png",
    "diagrams/process-notes.md",
    "diagrams/information-notes.md",
]


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
        "h": ParagraphStyle(
            "h",
            fontName="Manrope-Bold",
            fontSize=15,
            leading=18,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=2,
            alignment=TA_LEFT,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Manrope",
            fontSize=10.5,
            leading=14.4,
            textColor=TEXT,
            spaceBefore=0,
            spaceAfter=8,
            alignment=TA_LEFT,
        ),
        "cap": ParagraphStyle(
            "cap",
            fontName="Manrope-Med",
            fontSize=8.5,
            leading=11,
            textColor=INK,
            spaceBefore=0,
            spaceAfter=0,
            alignment=TA_CENTER,
        ),
        "cover_kicker": ParagraphStyle(
            "cover_kicker",
            fontName="Manrope-Semi",
            fontSize=13,
            leading=16,
            textColor=INK,
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
        # Break only URLs wider than the text frame. Break on a slash, not a missing glyph.
        url = match.group(0)
        plain = url.replace("&amp;", "&")
        limit = 490

        def wide(value: str) -> float:
            return pdfmetrics.stringWidth(value, "Manrope", 10.5)

        if wide(plain) <= limit:
            return url
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
        return "<br/>".join(lines)

    text = re.sub(r"https?://[^\s<]+", soften, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def body_paragraph(text: str, style: ParagraphStyle):
    xml = xml_text(text)
    kind = SolidParagraph if "http" in xml else Paragraph
    return kind(xml, style)


def prepare_image(src: Path, dest: Path) -> tuple[int, int]:
    image = PILImage.open(src).convert("RGBA")
    base = PILImage.new("RGBA", image.size, (255, 255, 255, 255))
    flat = PILImage.alpha_composite(base, image).convert("RGB")
    flat.save(dest, "PNG")
    return flat.size


def knock_out_wordmark(src: Path, dest: Path) -> tuple[int, int]:
    image = PILImage.open(src).convert("RGBA")
    pixels = image.load()
    width, height = image.size
    min_x, min_y, max_x, max_y = width, height, 0, 0
    found = False
    for y in range(height):
        for x in range(width):
            red, green, blue, _alpha = pixels[x, y]
            if (
                abs(red - BG_PURPLE[0]) > 18
                or abs(green - BG_PURPLE[1]) > 18
                or abs(blue - BG_PURPLE[2]) > 18
            ):
                pixels[x, y] = (red, green, blue, 255)
                found = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            else:
                pixels[x, y] = (red, green, blue, 0)
    if not found:
        raise SystemExit(f"no wordmark ink found in {src}")
    pad = 20
    box = (
        max(0, min_x - pad),
        max(0, min_y - pad),
        min(width, max_x + 1 + pad),
        min(height, max_y + 1 + pad),
    )
    crop = image.crop(box)
    crop.save(dest, "PNG")
    return crop.size


class CoverPage(Flowable):
    def __init__(self, path: str, width_px: int, height_px: int):
        super().__init__()
        self.path = path
        self.px_w = width_px
        self.px_h = height_px

    def wrap(self, avail_width, avail_height):
        self.avail_width = avail_width
        self.avail_height = avail_height
        return avail_width, avail_height

    def draw(self):
        draw_w = min(self.avail_width - 10, 450)
        draw_h = draw_w * self.px_h / self.px_w
        # date, name, kicker, gap, wordmark — centered a little above the middle
        block_h = draw_h + 26 + 36 + 28 + 14
        bottom = max(36, (self.avail_height - block_h) / 2 - 8)
        name_y = bottom + 28
        kicker_y = name_y + 36
        image_y = kicker_y + 26
        image_x = (self.avail_width - draw_w) / 2
        self.canv.drawImage(
            self.path,
            image_x,
            image_y,
            draw_w,
            draw_h,
            mask="auto",
            preserveAspectRatio=True,
        )
        self.canv.setFillColor(INK)
        self.canv.setFont("Manrope-Semi", 13)
        self.canv.drawCentredString(self.avail_width / 2, kicker_y, "Business plan")
        self.canv.setFont("Manrope-Bold", 22)
        self.canv.drawCentredString(self.avail_width / 2, name_y, "Jacob")
        self.canv.setFont("Manrope", 12)
        self.canv.drawCentredString(self.avail_width / 2, bottom, "30 September 2026")


class FigureBlock(Flowable):
    def __init__(self, path: str, caption: str, max_height: float, pref_width: float | None):
        super().__init__()
        self.path = path
        self.caption = caption
        self.max_height = max_height
        self.pref_width = pref_width
        with PILImage.open(path) as image:
            self.px_w, self.px_h = image.size

    def wrap(self, avail_width, avail_height):
        max_w = avail_width if self.pref_width is None else min(avail_width, self.pref_width)
        scale = min(max_w / self.px_w, self.max_height / self.px_h)
        self.draw_w = self.px_w * scale
        self.draw_h = self.px_h * scale
        self.paragraph = Paragraph(xml_text(self.caption), styles()["cap"])
        _cw, self.cap_h = self.paragraph.wrap(self.draw_w, 800)
        self.avail_width = avail_width
        self.height = self.draw_h + 5 + self.cap_h
        return avail_width, self.height

    def draw(self):
        image_x = (self.avail_width - self.draw_w) / 2
        self.canv.drawImage(
            self.path,
            image_x,
            self.cap_h + 5,
            self.draw_w,
            self.draw_h,
            mask="auto",
            preserveAspectRatio=True,
        )
        self.paragraph.drawOn(self.canv, image_x, 0)


class ImageRow(Flowable):
    def __init__(self, items: list[tuple[str, str]], max_height: float):
        super().__init__()
        self.items = items
        self.max_height = max_height
        self.sizes = []
        for path, _caption in items:
            with PILImage.open(path) as image:
                self.sizes.append(image.size)

    def wrap(self, avail_width, avail_height):
        count = len(self.items)
        gap = 12
        col_w = (avail_width - gap * (count - 1)) / count
        self.cols = []
        row_h = 0
        cap_style = styles()["cap"]
        for (path, caption), (px_w, px_h) in zip(self.items, self.sizes):
            scale = min(col_w / px_w, self.max_height / px_h)
            draw_w = px_w * scale
            draw_h = px_h * scale
            paragraph = Paragraph(xml_text(caption), cap_style)
            _cw, cap_h = paragraph.wrap(col_w, 800)
            self.cols.append((path, draw_w, draw_h, paragraph, cap_h, col_w))
            row_h = max(row_h, draw_h + 5 + cap_h)
        self.gap = gap
        self.avail_width = avail_width
        self.row_h = row_h
        return avail_width, row_h

    def draw(self):
        x = 0
        for path, draw_w, draw_h, paragraph, cap_h, col_w in self.cols:
            image_x = x + (col_w - draw_w) / 2
            image_y = self.row_h - draw_h
            self.canv.drawImage(
                path,
                image_x,
                image_y,
                draw_w,
                draw_h,
                mask="auto",
                preserveAspectRatio=True,
            )
            paragraph.drawOn(self.canv, x, image_y - 5 - cap_h)
            x += col_w + self.gap


def draw_cover(canvas, _doc) -> None:
    canvas.saveState()
    canvas.setFillColor(PURPLE)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setTitle("STAMP business plan")
    canvas.setAuthor("Jacob")
    canvas.restoreState()


def draw_body(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(white)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setStrokeColor(PURPLE)
    canvas.setLineWidth(1.5)
    canvas.line(LEFT, A4[1] - 34, A4[0] - RIGHT, A4[1] - 34)
    canvas.line(LEFT, 40, A4[0] - RIGHT, 40)
    canvas.setFillColor(INK)
    canvas.setFont("Manrope-Semi", 8.5)
    canvas.drawString(LEFT, 24, "STAMP")
    canvas.setFont("Manrope", 8.5)
    canvas.drawRightString(A4[0] - RIGHT, 24, f"{doc.page}")
    canvas.setTitle("STAMP business plan")
    canvas.setAuthor("Jacob")
    canvas.restoreState()


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


def build_story(sections: list[dict], work: Path, wordmark: tuple[str, int, int]) -> list:
    style = styles()
    story: list = []
    path, px_w, px_h = wordmark
    story.append(CoverPage(path, px_w, px_h))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    for section_index, section in enumerate(sections):
        if section_index:
            story.append(CondPageBreak(88))
        story.append(Paragraph(xml_text(section["title"]), style["h"]))
        story.append(
            HRFlowable(
                width="100%",
                thickness=1.25,
                color=PURPLE,
                spaceBefore=1,
                spaceAfter=8,
            )
        )
        pending = None
        for index, (kind, payload) in enumerate(section["blocks"]):
            if kind == "prose":
                if pending is not None:
                    story.append(pending)
                    pending = None
                paragraphs = [part.strip() for part in payload.split("\n\n") if part.strip()]
                nxt = section["blocks"][index + 1][0] if index + 1 < len(section["blocks"]) else ""
                hold = nxt in {"figure", "row"} and len(paragraphs) > 0
                body = paragraphs[:-1] if hold else paragraphs
                for part in body:
                    story.append(body_paragraph(part, style["body"]))
                if hold:
                    pending = body_paragraph(paragraphs[-1], style["body"])
                continue
            visuals = visual_flowables(kind, payload, work)
            if pending is not None:
                story.append(KeepTogether([pending, *visuals]))
                pending = None
            else:
                story.extend(visuals)
        if pending is not None:
            story.append(pending)
    return story


def visual_flowables(kind: str, payload, work: Path) -> list:
    if kind == "figure":
        src = resolve_src(payload["src"])
        caption = payload.get("caption", "").strip()
        if not caption:
            raise SystemExit(f"figure missing a caption: {src}")
        flat = work / f"fig-{len(list(work.iterdir()))}.png"
        prepare_image(src, flat)
        pref = float(payload["width"]) if payload.get("width") else None
        max_h = float(payload["max-height"]) if payload.get("max-height") else 400
        return [
            Spacer(1, 2),
            FigureBlock(str(flat), caption, max_h, pref),
            Spacer(1, 8),
        ]
    if kind == "row":
        prepared = []
        for item in payload:
            src = resolve_src(item["src"])
            flat = work / f"row-{len(list(work.iterdir()))}.png"
            prepare_image(src, flat)
            prepared.append((str(flat), item["caption"]))
        return [Spacer(1, 2), ImageRow(prepared, 230), Spacer(1, 8)]
    raise SystemExit(f"unknown block {kind}")


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
        mark = work / "wordmark.png"
        px_w, px_h = knock_out_wordmark(ROOT / "brand" / "logo.png", mark)
        story = build_story(sections, work, (str(mark), px_w, px_h))
        tmp_out = work / "plan.pdf"
        frame_h = A4[1] - FRAME_BOTTOM - FRAME_TOP
        frame_w = A4[0] - LEFT - RIGHT
        document = BaseDocTemplate(
            str(tmp_out),
            pagesize=A4,
            title="STAMP business plan",
            author="Jacob",
        )
        document.addPageTemplates(
            [
                PageTemplate(
                    id="cover",
                    frames=[
                        Frame(
                            36,
                            36,
                            A4[0] - 72,
                            A4[1] - 72,
                            id="cover",
                            showBoundary=0,
                        )
                    ],
                    onPage=draw_cover,
                ),
                PageTemplate(
                    id="body",
                    frames=[
                        Frame(
                            LEFT,
                            FRAME_BOTTOM,
                            frame_w,
                            frame_h,
                            id="body",
                            showBoundary=0,
                        )
                    ],
                    onPage=draw_body,
                ),
            ]
        )
        document.build(story)
        OUT_PATH.write_bytes(tmp_out.read_bytes())
    print(f"wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
