#!/usr/bin/env python3
"""
Render the thesis cover and handbook sample cover, then generate comparison
artifacts for visual inspection.

Outputs:
- docs/assets/thesis-cover-overlay.png
- docs/assets/thesis-cover-overlay-focus.png
- docs/assets/thesis-cover-diff.png
- docs/assets/thesis-cover-diff-focus.png
- docs/assets/thesis-cover-checker.png
- docs/assets/thesis-cover-checker-focus.png
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageOps, ImageStat


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_PDF = PROJECT_ROOT / "references" / "江苏海洋大学2026届毕业实习与设计（论文）工作手册.pdf"
CURRENT_PDF = PROJECT_ROOT / "main.pdf"
TEMP_DIR = PROJECT_ROOT / "tmp" / "pdfs"
ASSET_DIR = PROJECT_ROOT / "docs" / "assets"
FOCUS_BOX = (150, 260, 1080, 1510)


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


def build_checkerboard(reference: Image.Image, current: Image.Image, block: int = 24) -> Image.Image:
    checker = Image.new("RGB", reference.size)
    for y in range(0, reference.size[1], block):
        for x in range(0, reference.size[0], block):
            source = reference if ((x // block) + (y // block)) % 2 == 0 else current
            checker.paste(
                source.crop((x, y, min(x + block, reference.size[0]), min(y + block, reference.size[1]))),
                (x, y),
            )
    return checker


def main() -> int:
    if not REFERENCE_PDF.exists():
        print(f"缺少参考 PDF: {REFERENCE_PDF}", file=sys.stderr)
        return 1
    if not CURRENT_PDF.exists():
        print(f"缺少当前论文 PDF: {CURRENT_PDF}", file=sys.stderr)
        return 1

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    reference_page = render_page(REFERENCE_PDF, 39, TEMP_DIR / "cover-ref")
    current_page = render_page(CURRENT_PDF, 1, TEMP_DIR / "cover-cur")

    reference = Image.open(reference_page).convert("RGBA")
    current = Image.open(current_page).convert("RGBA")
    if current.size != reference.size:
        current = current.resize(reference.size)

    reference_rgb = reference.convert("RGB")
    current_rgb = current.convert("RGB")

    overlay = Image.blend(reference, current, 0.5)
    diff = ImageOps.autocontrast(ImageChops.difference(reference_rgb, current_rgb), cutoff=1)
    checker = build_checkerboard(reference_rgb, current_rgb)

    overlay_path = ASSET_DIR / "thesis-cover-overlay.png"
    diff_path = ASSET_DIR / "thesis-cover-diff.png"
    checker_path = ASSET_DIR / "thesis-cover-checker.png"
    overlay_focus_path = ASSET_DIR / "thesis-cover-overlay-focus.png"
    diff_focus_path = ASSET_DIR / "thesis-cover-diff-focus.png"
    checker_focus_path = ASSET_DIR / "thesis-cover-checker-focus.png"

    overlay.save(overlay_path)
    diff.save(diff_path)
    checker.save(checker_path)
    overlay.crop(FOCUS_BOX).save(overlay_focus_path)
    diff.crop(FOCUS_BOX).save(diff_focus_path)
    checker.crop(FOCUS_BOX).save(checker_focus_path)

    grayscale_diff = ImageChops.difference(reference_rgb.convert("L"), current_rgb.convert("L"))
    diff_stats = ImageStat.Stat(grayscale_diff)

    print("封面对比产物已生成")
    print(f"overlay: {overlay_path}")
    print(f"diff   : {diff_path}")
    print(f"checker: {checker_path}")
    print(f"overlay-focus: {overlay_focus_path}")
    print(f"mean_abs_diff: {diff_stats.mean[0]:.3f}")
    print(f"rms_diff     : {diff_stats.rms[0]:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
