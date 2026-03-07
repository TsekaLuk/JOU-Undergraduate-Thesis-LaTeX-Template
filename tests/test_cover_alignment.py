#!/usr/bin/env python3
"""
Rendered cover-page regression checks for the undergraduate thesis template.

This test compares the compiled thesis cover against the handbook sample cover
at the rendered-image level instead of only using text anchors.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).parent.parent
MAIN_PDF = PROJECT_ROOT / "main.pdf"
REFERENCE_PDF = PROJECT_ROOT / "references" / "江苏海洋大学2026届毕业实习与设计（论文）工作手册.pdf"


def render_page(pdf: Path, page: int, prefix: Path) -> Path:
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            str(page),
            "-l",
            str(page),
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
        raise RuntimeError(f"未能渲染 {pdf.name} 第 {page} 页")
    return candidates[0]


def content_clusters(image_path: Path, gap: int = 65) -> list[tuple[int, int, int, int]]:
    image = Image.open(image_path).convert("RGBA")
    bg = image.getpixel((0, 0))
    width, height = image.size
    rows: list[tuple[int, int, int]] = []

    for y in range(height):
        xs = []
        for x in range(width):
            pixel = image.getpixel((x, y))
            if sum(abs(pixel[idx] - bg[idx]) for idx in range(3)) > 80:
                xs.append(x)
        if len(xs) > 10:
            rows.append((y, min(xs), max(xs)))

    clusters: list[tuple[int, int, int, int]] = []
    if not rows:
        return clusters

    start_y, end_y = rows[0][0], rows[0][0]
    min_x, max_x = rows[0][1], rows[0][2]

    for y, row_min_x, row_max_x in rows[1:]:
        if y - end_y > gap:
            clusters.append((start_y, end_y, min_x, max_x))
            start_y = y
            min_x = row_min_x
            max_x = row_max_x
        else:
            min_x = min(min_x, row_min_x)
            max_x = max(max_x, row_max_x)
        end_y = y

    clusters.append((start_y, end_y, min_x, max_x))
    return clusters


def blue_pixel_count(image_path: Path, box: tuple[int, int, int, int]) -> int:
    image = Image.open(image_path).convert("RGB")
    left, top, right, bottom = box
    count = 0
    for y in range(top, bottom):
        for x in range(left, right):
            red, green, blue = image.getpixel((x, y))
            if blue > 110 and blue > red + 30 and blue > green + 20:
                count += 1
    return count


def long_underline_rows(image_path: Path, y_start: int, y_end: int) -> int:
    image = Image.open(image_path).convert("RGBA")
    bg = image.getpixel((0, 0))
    width, _ = image.size
    rows = 0
    for y in range(y_start, y_end):
        dark_pixels = 0
        for x in range(width):
            pixel = image.getpixel((x, y))
            if sum(abs(pixel[idx] - bg[idx]) for idx in range(3)) > 80:
                dark_pixels += 1
        if dark_pixels > 350:
            rows += 1
    return rows


def main() -> int:
    failures: list[str] = []

    if not MAIN_PDF.exists():
        print("FAIL - 缺少 main.pdf，请先编译论文模板")
        return 1
    if not REFERENCE_PDF.exists():
        print("FAIL - 缺少参考手册 PDF")
        return 1

    with tempfile.TemporaryDirectory(prefix="jou-cover-") as tmp_dir:
        tmp = Path(tmp_dir)
        current_cover = render_page(MAIN_PDF, 1, tmp / "current")
        reference_cover = render_page(REFERENCE_PDF, 39, tmp / "reference")

        current_clusters = content_clusters(current_cover)
        reference_clusters = content_clusters(reference_cover)[:4]

        if len(current_clusters) != 4:
            failures.append(f"封面视觉簇数量异常，期望 4 组，当前为 {len(current_clusters)} 组。")
        if len(reference_clusters) != 4:
            failures.append("参考封面解析异常，未得到 4 组基准版面簇。")

        if not failures:
            tolerances = [
                (35, 60, 60, 60),
                (30, 30, None, None),
                (40, 100, 40, 40),
                (120, 120, 30, 30),
            ]
            names = ["校徽与校名区", "题名区", "信息区", "年月区"]

            for idx, (name, tol) in enumerate(zip(names, tolerances)):
                current = current_clusters[idx]
                reference = reference_clusters[idx]
                start_tol, end_tol, left_tol, right_tol = tol
                if abs(current[0] - reference[0]) > start_tol:
                    failures.append(
                        f"{name} 顶部位置偏差过大：当前 {current[0]}，参考 {reference[0]}。"
                    )
                if abs(current[1] - reference[1]) > end_tol:
                    failures.append(
                        f"{name} 底部位置偏差过大：当前 {current[1]}，参考 {reference[1]}。"
                    )
                if left_tol is not None and abs(current[2] - reference[2]) > left_tol:
                    failures.append(
                        f"{name} 左边界偏差过大：当前 {current[2]}，参考 {reference[2]}。"
                    )
                if right_tol is not None and abs(current[3] - reference[3]) > right_tol:
                    failures.append(
                        f"{name} 右边界偏差过大：当前 {current[3]}，参考 {reference[3]}。"
                    )

        blue_pixels = blue_pixel_count(current_cover, (150, 250, 1050, 550))
        if blue_pixels < 10000:
            failures.append("封面顶部未检测到足够的蓝色 logo/校名字样区域，疑似缺失校徽或校名图。")

        underline_rows = long_underline_rows(current_cover, 1100, 1450)
        if underline_rows < 3:
            failures.append("封面信息区未检测到足够的长下划线行。")

    print("封面视觉回归检查")
    print("=" * 72)
    if failures:
        for idx, failure in enumerate(failures, 1):
            print(f"{idx}. {failure}")
        print(f"\n结果: FAIL ({len(failures)} 项不对齐)")
        return 1

    print("结果: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
