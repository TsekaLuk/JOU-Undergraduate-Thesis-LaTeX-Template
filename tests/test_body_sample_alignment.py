#!/usr/bin/env python3
"""
Pixel-oriented checks for the handbook body-style sample page.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops


PROJECT_ROOT = Path(__file__).parent.parent
REFERENCE_PDF = PROJECT_ROOT / "references" / "江苏海洋大学2026届毕业实习与设计（论文）工作手册.pdf"
BODY_SAMPLE_PDF = PROJECT_ROOT / "body-sample.pdf"
REFERENCE_PAGE = 45
RENDER_DPI = 160
CROP_BOX = (80, 90, 1135, 1500)
MAX_MEAN_DIFF = 22.5
MAX_RMS_DIFF = 66.0


def normalize(text: str) -> str:
    text = text.replace("\u3000", " ")
    return re.sub(r"\s+", "", text)


def page_text(pdf: Path, page: int) -> str:
    completed = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def pdf_page_count(pdf: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(pdf)],
        check=True,
        text=True,
        capture_output=True,
    )
    match = re.search(r"^Pages:\s+(\d+)$", completed.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError("无法从 pdfinfo 输出解析页数")
    return int(match.group(1))


def render_page(pdf: Path, page: int) -> Image.Image:
    with tempfile.TemporaryDirectory() as temp_dir:
        prefix = Path(temp_dir) / "page"
        subprocess.run(
            [
                "pdftoppm",
                "-f",
                str(page),
                "-l",
                str(page),
                "-r",
                str(RENDER_DPI),
                "-png",
                str(pdf),
                str(prefix),
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        candidates = sorted(Path(temp_dir).glob("page-*.png"))
        if not candidates:
            raise RuntimeError(f"无法渲染 {pdf} 第 {page} 页")
        return Image.open(candidates[0]).convert("L").copy()


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


def main() -> int:
    failures: list[str] = []

    if not BODY_SAMPLE_PDF.exists():
        print("FAIL - 缺少 body-sample.pdf，请先运行 `make body-sample.pdf` 或 `make test`。")
        return 1

    if pdf_page_count(BODY_SAMPLE_PDF) != 1:
        failures.append("正文样页基线应只有 1 页。")

    sample_text = normalize(page_text(BODY_SAMPLE_PDF, 1))
    required_patterns = [
        "1绪论（一级标题）",
        "1.1××××××（二级标题）",
        "1.1.1××××（三级标题）",
        "2×××××（一级标题）",
        "*注：",
        "本页为正文式样",
    ]
    for pattern in required_patterns:
        if pattern not in sample_text:
            failures.append(f"正文样页缺少锚点：{pattern}")

    reference_image = render_page(REFERENCE_PDF, REFERENCE_PAGE)
    sample_image = render_page(BODY_SAMPLE_PDF, 1)

    ref_rows = header_rule_rows(reference_image)
    sample_rows = header_rule_rows(sample_image)
    if not ref_rows or not sample_rows:
        failures.append("无法识别正文样页页眉横线。")
    else:
        if abs(sample_rows[0] - ref_rows[0]) > 6:
            failures.append(
                f"正文样页页眉横线位置异常，参考 y={ref_rows[0]}，当前 y={sample_rows[0]}。"
            )

    mean_diff, rms_diff = diff_metrics(reference_image, sample_image)
    if mean_diff > MAX_MEAN_DIFF:
        failures.append(
            f"正文样页裁剪区域平均像素差过大：{mean_diff:.3f} > {MAX_MEAN_DIFF:.1f}。"
        )
    if rms_diff > MAX_RMS_DIFF:
        failures.append(
            f"正文样页裁剪区域 RMS 像素差过大：{rms_diff:.3f} > {MAX_RMS_DIFF:.1f}。"
        )

    print("正文样页像素对齐检查")
    print("=" * 72)
    print(f"mean_abs_diff = {mean_diff:.3f}")
    print(f"rms_diff      = {rms_diff:.3f}")
    if failures:
        for idx, failure in enumerate(failures, 1):
            print(f"{idx}. {failure}")
        print(f"\n结果: FAIL ({len(failures)} 项不对齐)")
        return 1

    print("结果: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
