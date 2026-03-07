#!/usr/bin/env python3
"""
Focused E2E checks for the undergraduate thesis template.

This script validates the rendered thesis against the handbook thesis sample
using page anchors instead of hard-coded page numbers.
"""

import re
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
MAIN_PDF = PROJECT_ROOT / "main.pdf"


def normalize(text: str) -> str:
    text = text.replace("\u3000", " ")
    return re.sub(r"\s+", "", text)


def page_text(pdf: Path, page: int) -> str:
    completed = subprocess.run(
        ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
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


def pdffonts(pdf: Path) -> str:
    completed = subprocess.run(
        ["pdffonts", str(pdf)],
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def find_page(pages: dict[int, str], *patterns: str) -> int | None:
    normalized_patterns = [normalize(pattern) for pattern in patterns]
    for page, text in pages.items():
        if all(pattern in text for pattern in normalized_patterns):
            return page
    return None


def require_page(
    failures: list[str], pages: dict[int, str], description: str, *patterns: str
) -> int | None:
    page = find_page(pages, *patterns)
    if page is None:
        failures.append(f"未找到“{description}”对应页面，缺少锚点：{' / '.join(patterns)}。")
    return page


def main() -> int:
    failures = []

    if not MAIN_PDF.exists():
        print("FAIL - 缺少 main.pdf，请先编译论文模板")
        return 1

    page_count = pdf_page_count(MAIN_PDF)
    pages = {
        page: normalize(page_text(MAIN_PDF, page))
        for page in range(1, page_count + 1)
    }
    fonts = pdffonts(MAIN_PDF)
    commercial_latin = any(
        marker in fonts
        for marker in ["TimesNewRoman", "Times-Roman", "Times New Roman"]
    )
    commercial_cjk = any(
        marker in fonts
        for marker in [
            "STSong",
            "STKaiti",
            "STFangsong",
            "STHeiti",
            "SimSun",
            "KaiTi",
            "KaiTi_GB2312",
            "FangSong",
            "FangSong_GB2312",
        ]
    )
    licensed_mode = commercial_latin and commercial_cjk

    cover_page = require_page(failures, pages, "封面", "学院", "学号", "指导教师")
    declaration_page = require_page(
        failures, pages, "原创性声明页", "原创性声明", "版权使用授权书"
    )
    cn_abstract_page = require_page(
        failures, pages, "中文摘要页", "毕业设计（论文）中文摘要", "摘 要"
    )
    en_abstract_page = require_page(
        failures, pages, "外文摘要页", "毕业设计（论文）外文摘要", "Abstract:"
    )
    toc_page = require_page(failures, pages, "目录页", "目", "录", "绪论")
    body_page = require_page(
        failures, pages, "正文首页", "理工农医类", "绪论", "研究背景与意义"
    )
    references_page = require_page(
        failures, pages, "参考文献页", "参考文献", "示例文献标题"
    )

    if cover_page is not None and cover_page != 1:
        failures.append(f"封面应位于第1页，当前位于第 {cover_page} 页。")

    if declaration_page is not None and declaration_page != 2:
        failures.append(f"原创性声明与授权书应位于第2页，当前位于第 {declaration_page} 页。")

    if (
        declaration_page is not None
        and cn_abstract_page is not None
        and cn_abstract_page != declaration_page + 1
    ):
        failures.append("中文摘要页应紧跟原创性声明页。")

    if (
        cn_abstract_page is not None
        and en_abstract_page is not None
        and en_abstract_page != cn_abstract_page + 1
    ):
        failures.append("外文摘要页应紧跟中文摘要页。")

    if toc_page is not None:
        if "第1章" in pages[toc_page]:
            failures.append("目录仍采用“第1章”体例，手册目录样式要求使用阿拉伯数字“1”。")
        if "江苏海洋大学二〇二六届本科毕业设计（论文）" in pages[toc_page]:
            failures.append("目录页不应沿用正文章节页眉。")

    if body_page is not None:
        if "第1章" in pages[body_page]:
            failures.append("正文一级标题仍显示为“第1章”，手册正文样式要求为“1 绪论”。")
        if "1绪论" not in pages[body_page]:
            failures.append("正文首页缺少“1 绪论”样式的一级标题。")

    if (
        toc_page is not None
        and body_page is not None
        and body_page <= toc_page
    ):
        failures.append("正文首页必须出现在目录页之后。")

    if references_page is not None:
        if body_page is not None and references_page <= body_page:
            failures.append("参考文献页顺序异常，应位于正文之后。")

    if licensed_mode:
        if not commercial_latin:
            failures.append("已检测到商业字体模式，但 PDF 未嵌入 Times New Roman 族字形。")
        if not commercial_cjk:
            failures.append("已检测到商业字体模式，但 PDF 未嵌入楷体/宋体等中文标准字形。")
    else:
        expected_fonts = ["Tinos", "NotoSerifCJKsc", "LXGWWenKaiGB", "CourierPrime"]
        for font_name in expected_fonts:
            if font_name not in fonts:
                failures.append(f"OSS 字体模式下缺少嵌入字体：{font_name}。")
    if "LMRoman" in fonts:
        failures.append("PDF 嵌入了 Latin Modern Roman，而不是手册要求的 Times New Roman/对应字形。")

    print("毕业论文样式检查")
    print("=" * 72)
    if failures:
        for idx, failure in enumerate(failures, 1):
            print(f"{idx}. {failure}")
        print(f"\n结果: FAIL ({len(failures)} 项不对齐)")
        return 1

    print(f"结果: PASS ({page_count} 页)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
