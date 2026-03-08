#!/usr/bin/env python3
"""
Generate README-ready preview images for the thesis template.

Outputs:
- docs/images/cover-compare.png
- docs/images/abstract-compare.png
- docs/images/body-compare.png
- docs/images/thesis-gallery.png
- docs/images/excellent-abstract-gallery.png
- docs/images/forms-gallery.png
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_PDF = PROJECT_ROOT / "references" / "江苏海洋大学2026届毕业实习与设计（论文）工作手册.pdf"
CURRENT_PDF = PROJECT_ROOT / "main.pdf"
BODY_SAMPLE_PDF = PROJECT_ROOT / "body-sample.pdf"
EXCELLENT_ABSTRACT_PDF = PROJECT_ROOT / "templates" / "reports" / "excellent-thesis-abstract.pdf"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "images"
TEMP_DIR = PROJECT_ROOT / "tmp" / "readme-images"
RESAMPLING = getattr(Image, "Resampling", Image)
DPI = 140
CONTENT_BOX = (760, 1080)
FORM_CONTENT_BOX = (500, 700)
GALLERY_TILE_BOX = (360, 470)
EXCELLENT_TILE_BOX = (420, 610)


@dataclass(frozen=True)
class CompareSpec:
    name: str
    title: str
    reference_page: int
    current_page: int
    crop_box: tuple[int, int, int, int]
    reference_label: str
    current_label: str


@dataclass(frozen=True)
class FormSpec:
    label: str
    pdf: Path
    crop_box: tuple[int, int, int, int]
    page: int = 1
    trim: bool = True


@dataclass(frozen=True)
class GallerySpec:
    label: str
    pdf: Path
    page: int
    crop_box: tuple[int, int, int, int]
    trim: bool = False


COMPARE_SPECS = (
    CompareSpec(
        name="cover-compare",
        title="Thesis Cover",
        reference_page=39,
        current_page=1,
        crop_box=(150, 260, 1080, 1510),
        reference_label="Reference (WPS PDF)",
        current_label="Current LaTeX PDF",
    ),
    CompareSpec(
        name="abstract-compare",
        title="Chinese Abstract",
        reference_page=41,
        current_page=3,
        crop_box=(170, 210, 1140, 820),
        reference_label="Reference (WPS PDF)",
        current_label="Current LaTeX PDF",
    ),
    CompareSpec(
        name="body-compare",
        title="Body Sample Page",
        reference_page=45,
        current_page=1,
        crop_box=(80, 90, 1135, 1500),
        reference_label="Reference (WPS PDF)",
        current_label="Current LaTeX Sample PDF",
    ),
)

FORM_SPECS = (
    FormSpec("Topic Selection", PROJECT_ROOT / "templates" / "forms" / "topic-selection.pdf", (40, 40, 1180, 1450)),
    FormSpec("Task Book", PROJECT_ROOT / "templates" / "forms" / "task-book-science.pdf", (70, 40, 1130, 1450)),
    FormSpec("Proposal Report", PROJECT_ROOT / "templates" / "reports" / "proposal-science.pdf", (160, 60, 1080, 1120)),
    FormSpec("Midterm Check", PROJECT_ROOT / "templates" / "forms" / "midterm-check.pdf", (40, 40, 1180, 1450)),
    FormSpec("Thesis Evaluation", PROJECT_ROOT / "templates" / "evaluations" / "thesis-evaluation.pdf", (60, 40, 1160, 1450)),
    FormSpec("Defense Record", PROJECT_ROOT / "templates" / "forms" / "defense-record.pdf", (120, 50, 1110, 1180)),
)

THESIS_GALLERY_SPECS = (
    GallerySpec("Cover", CURRENT_PDF, 1, (150, 260, 1080, 1510)),
    GallerySpec("Chinese Abstract", CURRENT_PDF, 3, (150, 140, 1160, 980)),
    GallerySpec("English Abstract", CURRENT_PDF, 4, (150, 140, 1160, 980)),
    GallerySpec("Table of Contents", CURRENT_PDF, 5, (70, 70, 1140, 930)),
    GallerySpec("Body Page", CURRENT_PDF, 7, (70, 70, 1140, 930)),
    GallerySpec("References", CURRENT_PDF, 14, (70, 70, 1140, 930)),
)

EXCELLENT_GALLERY_SPECS = (
    GallerySpec("Page 1", EXCELLENT_ABSTRACT_PDF, 1, (65, 55, 1135, 1545)),
    GallerySpec("Page 2", EXCELLENT_ABSTRACT_PDF, 2, (65, 55, 1135, 1545)),
)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if bold:
        candidates = (
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        )
    else:
        candidates = (
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "C:/Windows/Fonts/arial.ttf",
        )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


TITLE_FONT = load_font(34, bold=True)
LABEL_FONT = load_font(22, bold=True)


def render_page(pdf: Path, page: int, prefix: Path) -> Path:
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            str(page),
            "-l",
            str(page),
            "-r",
            str(DPI),
            "-png",
            str(pdf),
            str(prefix),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    candidates = sorted(prefix.parent.glob(f"{prefix.name}-*.png"))
    if not candidates:
        raise RuntimeError(f"Failed to render page {page} from {pdf}")
    return candidates[0]


def clamp_crop_box(image: Image.Image, crop_box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    left, top, right, bottom = crop_box
    width, height = image.size
    left = max(0, min(left, width - 1))
    top = max(0, min(top, height - 1))
    right = max(left + 1, min(right, width))
    bottom = max(top + 1, min(bottom, height))
    return (left, top, right, bottom)


def trim_whitespace(image: Image.Image, margin: int = 12) -> Image.Image:
    background = Image.new("RGB", image.size, "#ffffff")
    diff = ImageChops.difference(image, background).convert("L")
    bbox = diff.point(lambda value: 255 if value > 10 else 0).getbbox()
    if bbox is None:
        return image
    left, top, right, bottom = bbox
    return image.crop(
        (
            max(0, left - margin),
            max(0, top - margin),
            min(image.width, right + margin),
            min(image.height, bottom + margin),
        )
    )


def prepare_image(
    pdf: Path,
    page: int,
    crop_box: tuple[int, int, int, int],
    max_size: tuple[int, int],
    trim: bool = False,
) -> Image.Image:
    png_path = render_page(pdf, page, TEMP_DIR / f"{pdf.stem}-p{page}")
    image = Image.open(png_path).convert("RGB")
    cropped = image.crop(clamp_crop_box(image, crop_box))
    if trim:
        cropped = trim_whitespace(cropped)
    return ImageOps.contain(cropped, max_size, method=RESAMPLING.LANCZOS)


def draw_centered_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, font: ImageFont.ImageFont, fill: str) -> None:
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = left + (right - left - width) / 2
    y = top + (bottom - top - height) / 2
    draw.text((x, y), text, font=font, fill=fill)


def compose_compare(spec: CompareSpec) -> Path:
    left_image = prepare_image(REFERENCE_PDF, spec.reference_page, spec.crop_box, CONTENT_BOX)
    current_pdf = BODY_SAMPLE_PDF if spec.name == "body-compare" else CURRENT_PDF
    right_image = prepare_image(current_pdf, spec.current_page, spec.crop_box, CONTENT_BOX)

    margin = 36
    gap = 28
    title_height = 56
    label_height = 36
    panel_padding = 16
    panel_width = CONTENT_BOX[0] + panel_padding * 2
    panel_height = CONTENT_BOX[1] + panel_padding * 2
    width = margin * 2 + panel_width * 2 + gap
    height = margin * 2 + title_height + label_height + panel_height

    canvas = Image.new("RGB", (width, height), "#f4f4f6")
    draw = ImageDraw.Draw(canvas)
    draw_centered_text(draw, (0, margin - 6, width, margin + title_height), spec.title, TITLE_FONT, "#16181d")

    top = margin + title_height
    for idx, (label, image) in enumerate(((spec.reference_label, left_image), (spec.current_label, right_image))):
        x0 = margin + idx * (panel_width + gap)
        draw_centered_text(draw, (x0, top, x0 + panel_width, top + label_height), label, LABEL_FONT, "#303540")
        panel_top = top + label_height
        panel_box = (x0, panel_top, x0 + panel_width, panel_top + panel_height)
        draw.rounded_rectangle(panel_box, radius=16, fill="#ffffff", outline="#d8dbe2", width=2)
        image_x = x0 + panel_padding + (CONTENT_BOX[0] - image.width) // 2
        image_y = panel_top + panel_padding + (CONTENT_BOX[1] - image.height) // 2
        canvas.paste(image, (image_x, image_y))

    output_path = OUTPUT_DIR / f"{spec.name}.png"
    canvas.save(output_path, optimize=True)
    return output_path


def compose_forms_gallery() -> Path:
    return compose_gallery(
        title="Representative Handbook Forms",
        specs=tuple(
            GallerySpec(spec.label, spec.pdf, spec.page, spec.crop_box, trim=spec.trim)
            for spec in FORM_SPECS
        ),
        output_name="forms-gallery.png",
        columns=3,
        content_box=GALLERY_TILE_BOX,
    )


def compose_gallery(
    title: str,
    specs: tuple[GallerySpec, ...],
    output_name: str,
    columns: int,
    content_box: tuple[int, int],
) -> Path:
    margin = 36
    gap = 24
    title_height = 56
    row_gap = 24
    label_height = 34
    panel_padding = 14
    rows = (len(specs) + columns - 1) // columns
    tile_width = content_box[0] + panel_padding * 2
    tile_height = content_box[1] + panel_padding * 2 + label_height
    width = margin * 2 + tile_width * columns + gap * (columns - 1)
    height = margin * 2 + title_height + tile_height * rows + row_gap * max(0, rows - 1)

    canvas = Image.new("RGB", (width, height), "#f4f4f6")
    draw = ImageDraw.Draw(canvas)
    draw_centered_text(draw, (0, margin - 6, width, margin + title_height), title, TITLE_FONT, "#16181d")

    start_y = margin + title_height
    for idx, spec in enumerate(specs):
        if not spec.pdf.exists():
            raise RuntimeError(f"Missing gallery PDF: {spec.pdf}")
        row = idx // columns
        col = idx % columns
        x0 = margin + col * (tile_width + gap)
        y0 = start_y + row * (tile_height + row_gap)
        panel_box = (x0, y0, x0 + tile_width, y0 + tile_height)
        draw.rounded_rectangle(panel_box, radius=16, fill="#ffffff", outline="#d8dbe2", width=2)
        draw_centered_text(draw, (x0, y0 + 4, x0 + tile_width, y0 + label_height), spec.label, LABEL_FONT, "#303540")

        image = prepare_image(spec.pdf, spec.page, spec.crop_box, content_box, trim=spec.trim)
        image_x = x0 + panel_padding + (content_box[0] - image.width) // 2
        image_y = y0 + label_height + panel_padding + (content_box[1] - image.height) // 2
        canvas.paste(image, (image_x, image_y))

    output_path = OUTPUT_DIR / output_name
    canvas.save(output_path, optimize=True)
    return output_path


def compose_thesis_gallery() -> Path:
    return compose_gallery(
        title="Thesis Template Pages",
        specs=THESIS_GALLERY_SPECS,
        output_name="thesis-gallery.png",
        columns=3,
        content_box=GALLERY_TILE_BOX,
    )


def compose_excellent_gallery() -> Path:
    return compose_gallery(
        title="Excellent Thesis Abstract Template",
        specs=EXCELLENT_GALLERY_SPECS,
        output_name="excellent-abstract-gallery.png",
        columns=2,
        content_box=EXCELLENT_TILE_BOX,
    )


def main() -> int:
    if not REFERENCE_PDF.exists():
        print(f"Missing reference PDF: {REFERENCE_PDF}", file=sys.stderr)
        return 1
    if not CURRENT_PDF.exists():
        print(f"Missing thesis PDF: {CURRENT_PDF}", file=sys.stderr)
        return 1
    if not EXCELLENT_ABSTRACT_PDF.exists():
        print(f"Missing excellent abstract PDF: {EXCELLENT_ABSTRACT_PDF}", file=sys.stderr)
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    generated = [compose_compare(spec) for spec in COMPARE_SPECS]
    generated.append(compose_thesis_gallery())
    generated.append(compose_excellent_gallery())
    generated.append(compose_forms_gallery())

    print("README preview images generated:")
    for path in generated:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
