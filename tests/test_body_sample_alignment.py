#!/usr/bin/env python3
"""
Pixel-oriented checks for the handbook body-style sample page.
"""

from __future__ import annotations

import pytest
from PIL import Image, ImageChops

from conftest import (
    BODY_SAMPLE_PDF,
    REFERENCE_PDF,
    normalize,
    page_text,
    pdf_page_count,
    render_page,
)

REFERENCE_PAGE = 45
CROP_BOX = (80, 90, 1135, 1500)
MAX_MEAN_DIFF = 22.5
MAX_RMS_DIFF = 66.0


# ── Helpers ─────────────────────────────────────────────────────────────────

def header_rule_rows(image: Image.Image) -> list[int]:
    return [
        y
        for y in range(image.height)
        if sum(1 for x in range(image.width) if image.getpixel((x, y)) < 210) >= 900
    ]


def diff_metrics(reference: Image.Image, current: Image.Image) -> tuple[float, float]:
    ref_crop = reference.crop(CROP_BOX)
    current_crop = current.crop(CROP_BOX)
    diff = ImageChops.difference(ref_crop, current_crop)
    hist = diff.histogram()
    pixels = ref_crop.size[0] * ref_crop.size[1]
    mean = sum(i * count for i, count in enumerate(hist)) / pixels
    rms = (sum((i**2) * count for i, count in enumerate(hist)) / pixels) ** 0.5
    return mean, rms


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def body_sample_pdf():
    if not BODY_SAMPLE_PDF.exists():
        pytest.skip("缺少 body-sample.pdf，请先运行 `make body-sample.pdf` 或 `make test`。")
    return BODY_SAMPLE_PDF


# ── Tests ───────────────────────────────────────────────────────────────────

def test_body_sample_is_single_page(body_sample_pdf):
    assert pdf_page_count(body_sample_pdf) == 1, "正文样页基线应只有 1 页。"


REQUIRED_ANCHORS = [
    "1绪论（一级标题）",
    "1.1××××××（二级标题）",
    "1.1.1××××（三级标题）",
    "2×××××（一级标题）",
    "*注：",
    "本页为正文式样",
]


@pytest.mark.parametrize("anchor", REQUIRED_ANCHORS)
def test_body_sample_has_anchor(body_sample_pdf, anchor: str):
    sample_text = normalize(page_text(body_sample_pdf, 1))
    assert anchor in sample_text, f"正文样页缺少锚点：{anchor}"


def test_header_rule_position(body_sample_pdf):
    if not REFERENCE_PDF.exists():
        pytest.skip("缺少参考手册 PDF")
    reference_image = render_page(REFERENCE_PDF, REFERENCE_PAGE)
    sample_image = render_page(body_sample_pdf, 1)

    ref_rows = header_rule_rows(reference_image)
    sample_rows = header_rule_rows(sample_image)

    assert ref_rows and sample_rows, "无法识别正文样页页眉横线。"
    assert abs(sample_rows[0] - ref_rows[0]) <= 6, \
        f"正文样页页眉横线位置异常，参考 y={ref_rows[0]}，当前 y={sample_rows[0]}。"


def test_pixel_diff_within_bounds(body_sample_pdf):
    if not REFERENCE_PDF.exists():
        pytest.skip("缺少参考手册 PDF")
    reference_image = render_page(REFERENCE_PDF, REFERENCE_PAGE)
    sample_image = render_page(body_sample_pdf, 1)

    mean_diff, rms_diff = diff_metrics(reference_image, sample_image)
    assert mean_diff <= MAX_MEAN_DIFF, \
        f"正文样页裁剪区域平均像素差过大：{mean_diff:.3f} > {MAX_MEAN_DIFF:.1f}。"
    assert rms_diff <= MAX_RMS_DIFF, \
        f"正文样页裁剪区域 RMS 像素差过大：{rms_diff:.3f} > {MAX_RMS_DIFF:.1f}。"
