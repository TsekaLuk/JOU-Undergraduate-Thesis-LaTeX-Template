#!/usr/bin/env python3
"""
Focused E2E checks for the undergraduate thesis template.

This script validates the rendered thesis against the handbook thesis sample
using page anchors instead of hard-coded page numbers.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).parent.parent
MAIN_PDF = PROJECT_ROOT / "main.pdf"
RENDER_DPI = 160


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
            raise RuntimeError(f"无法渲染第 {page} 页为 PNG")
        return Image.open(candidates[0]).convert("L").copy()


def group_positions(values: list[int]) -> list[tuple[int, int]]:
    if not values:
        return []
    groups: list[tuple[int, int]] = []
    start = values[0]
    prev = values[0]
    for value in values[1:]:
        if value == prev + 1:
            prev = value
            continue
        groups.append((start, prev))
        start = value
        prev = value
    groups.append((start, prev))
    return groups


def assert_abstract_frame(failures: list[str], pdf: Path, page: int, label: str) -> None:
    image = render_page(pdf, page)
    width, height = image.size
    threshold = 205

    vertical_hits = [
        x for x in range(width)
        if sum(1 for y in range(height) if image.getpixel((x, y)) < threshold) >= 1200
    ]
    horizontal_hits = [
        y for y in range(height)
        if sum(1 for x in range(width) if image.getpixel((x, y)) < threshold) >= 800
    ]

    vertical_groups = group_positions(vertical_hits)
    horizontal_groups = group_positions(horizontal_hits)

    if len(vertical_groups) < 2:
        failures.append(f"{label} 缺少可识别的左右外框线。")
        return
    if len(horizontal_groups) < 2:
        failures.append(f"{label} 缺少可识别的上下外框线。")
        return

    left = vertical_groups[0]
    right = vertical_groups[-1]
    top = horizontal_groups[0]
    bottom = horizontal_groups[-1]

    left_center = (left[0] + left[1]) / 2
    right_center = (right[0] + right[1]) / 2
    top_center = (top[0] + top[1]) / 2
    bottom_center = (bottom[0] + bottom[1]) / 2

    if not (170 <= left_center <= 230):
        failures.append(f"{label} 左边框位置异常，当前约为 x={left_center:.1f}。")
    if not (1090 <= right_center <= 1160):
        failures.append(f"{label} 右边框位置异常，当前约为 x={right_center:.1f}。")
    if not (200 <= top_center <= 290):
        failures.append(f"{label} 上边框位置异常，当前约为 y={top_center:.1f}。")
    if not (1600 <= bottom_center <= 1785):
        failures.append(f"{label} 下边框位置异常，当前约为 y={bottom_center:.1f}。")

    frame_width = right_center - left_center
    frame_height = bottom_center - top_center
    if not (880 <= frame_width <= 980):
        failures.append(f"{label} 外框宽度异常，当前约为 {frame_width:.1f}px。")
    if not (1320 <= frame_height <= 1540):
        failures.append(f"{label} 外框高度异常，当前约为 {frame_height:.1f}px。")


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


def bbox_lines(pdf: Path, page: int) -> list[dict[str, float | str]]:
    completed = subprocess.run(
        ["pdftotext", "-bbox-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
        check=True,
        text=True,
        capture_output=True,
    )
    html = completed.stdout
    lines: list[dict[str, float | str]] = []
    line_pattern = re.compile(
        r'<line xMin="(?P<xmin>[^"]+)" yMin="(?P<ymin>[^"]+)" '
        r'xMax="(?P<xmax>[^"]+)" yMax="(?P<ymax>[^"]+)">(?P<body>.*?)</line>',
        re.DOTALL,
    )
    word_pattern = re.compile(r"<word [^>]*>(?P<text>.*?)</word>", re.DOTALL)
    for match in line_pattern.finditer(html):
        words = word_pattern.findall(match.group("body"))
        text = "".join(words)
        lines.append(
            {
                "text": text,
                "xMin": float(match.group("xmin")),
                "xMax": float(match.group("xmax")),
                "yMin": float(match.group("ymin")),
                "yMax": float(match.group("ymax")),
            }
        )
    return lines


def assert_centered_heading(
    failures: list[str], pdf: Path, page: int, label: str, heading: str
) -> None:
    lines = bbox_lines(pdf, page)
    normalized_heading = normalize(heading)
    top_lines = [line for line in lines if line["yMin"] < 180]
    logical_lines: list[dict[str, float | str]] = []
    for line in sorted(top_lines, key=lambda item: (float(item["yMin"]), float(item["xMin"]))):
        if logical_lines and abs(float(line["yMin"]) - float(logical_lines[-1]["yMin"])) < 1.5:
            logical_lines[-1]["text"] = str(logical_lines[-1]["text"]) + str(line["text"])
            logical_lines[-1]["xMax"] = max(float(logical_lines[-1]["xMax"]), float(line["xMax"]))
            logical_lines[-1]["yMax"] = max(float(logical_lines[-1]["yMax"]), float(line["yMax"]))
        else:
            logical_lines.append(dict(line))

    candidates = [
        line for line in logical_lines if normalize(str(line["text"])) == normalized_heading
    ]
    if not candidates:
        failures.append(f"{label} 未在页首区域识别到标题“{heading}”。")
        return

    target = min(candidates, key=lambda word: abs(float(word["yMin"]) - 95))
    page_center = 595.28 / 2
    title_center = (float(target["xMin"]) + float(target["xMax"])) / 2
    if abs(title_center - page_center) > 18:
        failures.append(
            f"{label} 标题未居中，当前中心点约为 x={title_center:.1f}pt。"
        )


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
            "FZShuSong",
            "FZFangSong",
            "HYKaiTi",
            "HYc1gj",
            "HYZhongJianHei",
            "HYShuSongErKW",
            "HYZhongHeiKW",
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
    conclusion_page = require_page(
        failures, pages, "结论与展望页", "结论与展望", "这里填写结论与展望的内容"
    )
    acknowledgement_page = require_page(
        failures, pages, "致谢页", "致谢", "在此感谢导师的悉心指导"
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

    if cn_abstract_page is not None:
        assert_abstract_frame(failures, MAIN_PDF, cn_abstract_page, "中文摘要页")
    if en_abstract_page is not None:
        assert_abstract_frame(failures, MAIN_PDF, en_abstract_page, "外文摘要页")

    if conclusion_page is not None:
        assert_centered_heading(
            failures, MAIN_PDF, conclusion_page, "结论与展望页", "结论与展望"
        )
    if acknowledgement_page is not None:
        assert_centered_heading(
            failures, MAIN_PDF, acknowledgement_page, "致谢页", "致 谢"
        )
    if references_page is not None:
        assert_centered_heading(
            failures, MAIN_PDF, references_page, "参考文献页", "参 考 文 献"
        )

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
        if (
            acknowledgement_page is not None
            and references_page <= acknowledgement_page
        ):
            failures.append("参考文献页顺序异常，应位于致谢之后。")

    if licensed_mode:
        if not commercial_latin:
            failures.append("已检测到商业字体模式，但 PDF 未嵌入 Times New Roman 族字形。")
        if not commercial_cjk:
            failures.append("已检测到商业字体模式，但 PDF 未嵌入楷体_GB2312/宋体/黑体等中文标准字形。")
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
