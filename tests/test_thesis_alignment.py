#!/usr/bin/env python3
"""
Focused E2E checks for the undergraduate thesis template.

Validates the rendered thesis against the handbook sample using page anchors
instead of hard-coded page numbers.
"""

from __future__ import annotations

import re

import pytest

from conftest import (
    MAIN_PDF,
    normalize,
    page_text,
    pdf_page_count,
    pdffonts,
    render_page,
)


# ── Helpers ─────────────────────────────────────────────────────────────────

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


def _assert_abstract_frame(pdf, page: int, label: str):
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

    assert len(vertical_groups) >= 2, f"{label} 缺少可识别的左右外框线。"
    assert len(horizontal_groups) >= 2, f"{label} 缺少可识别的上下外框线。"

    left = vertical_groups[0]
    right = vertical_groups[-1]
    top = horizontal_groups[0]
    bottom = horizontal_groups[-1]

    left_center = (left[0] + left[1]) / 2
    right_center = (right[0] + right[1]) / 2
    top_center = (top[0] + top[1]) / 2
    bottom_center = (bottom[0] + bottom[1]) / 2

    assert 170 <= left_center <= 230, f"{label} 左边框位置异常，当前约为 x={left_center:.1f}。"
    assert 1090 <= right_center <= 1160, f"{label} 右边框位置异常，当前约为 x={right_center:.1f}。"
    assert 200 <= top_center <= 290, f"{label} 上边框位置异常，当前约为 y={top_center:.1f}。"
    assert 1600 <= bottom_center <= 1785, f"{label} 下边框位置异常，当前约为 y={bottom_center:.1f}。"

    frame_width = right_center - left_center
    frame_height = bottom_center - top_center
    assert 880 <= frame_width <= 980, f"{label} 外框宽度异常，当前约为 {frame_width:.1f}px。"
    assert 1320 <= frame_height <= 1540, f"{label} 外框高度异常，当前约为 {frame_height:.1f}px。"


def bbox_lines(pdf, page: int) -> list[dict]:
    import subprocess
    completed = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-bbox-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
        check=True, text=True, capture_output=True,
    )
    html = completed.stdout
    lines: list[dict] = []
    line_pattern = re.compile(
        r'<line xMin="(?P<xmin>[^"]+)" yMin="(?P<ymin>[^"]+)" '
        r'xMax="(?P<xmax>[^"]+)" yMax="(?P<ymax>[^"]+)">(?P<body>.*?)</line>',
        re.DOTALL,
    )
    word_pattern = re.compile(r"<word [^>]*>(?P<text>.*?)</word>", re.DOTALL)
    for match in line_pattern.finditer(html):
        words = word_pattern.findall(match.group("body"))
        text = "".join(words)
        lines.append({
            "text": text,
            "xMin": float(match.group("xmin")),
            "xMax": float(match.group("xmax")),
            "yMin": float(match.group("ymin")),
            "yMax": float(match.group("ymax")),
        })
    return lines


def _assert_centered_heading(pdf, page: int, label: str, heading: str):
    lines = bbox_lines(pdf, page)
    normalized_heading = normalize(heading)
    top_lines = [line for line in lines if line["yMin"] < 180]
    logical_lines: list[dict] = []
    for line in sorted(top_lines, key=lambda item: (float(item["yMin"]), float(item["xMin"]))):
        if logical_lines and abs(float(line["yMin"]) - float(logical_lines[-1]["yMin"])) < 1.5:
            logical_lines[-1]["text"] = str(logical_lines[-1]["text"]) + str(line["text"])
            logical_lines[-1]["xMax"] = max(float(logical_lines[-1]["xMax"]), float(line["xMax"]))
            logical_lines[-1]["yMax"] = max(float(logical_lines[-1]["yMax"]), float(line["yMax"]))
        else:
            logical_lines.append(dict(line))

    candidates = [line for line in logical_lines if normalize(str(line["text"])) == normalized_heading]
    assert candidates, f"{label} 未在页首区域识别到标题 '{heading}'。"

    target = min(candidates, key=lambda w: abs(float(w["yMin"]) - 95))
    page_center = 595.28 / 2
    title_center = (float(target["xMin"]) + float(target["xMax"])) / 2
    assert abs(title_center - page_center) <= 18, f"{label} 标题未居中，当前中心点约为 x={title_center:.1f}pt。"


def _find_page(pages: dict[int, str], *patterns: str) -> int | None:
    normalized_patterns = [normalize(p) for p in patterns]
    for page, text in pages.items():
        if all(p in text for p in normalized_patterns):
            return page
    return None


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def thesis_pages() -> dict[int, str]:
    """Load all thesis pages as normalized text, keyed by page number."""
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf，请先编译论文模板")
    count = pdf_page_count(MAIN_PDF)
    return {p: normalize(page_text(MAIN_PDF, p)) for p in range(1, count + 1)}


@pytest.fixture(scope="module")
def thesis_fonts() -> str:
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf")
    return pdffonts(MAIN_PDF)


# ── Page ordering tests ────────────────────────────────────────────────────

def test_cover_on_page_one(thesis_pages):
    cover = _find_page(thesis_pages, "学院", "学号", "指导教师")
    assert cover is not None, "未找到封面页"
    assert cover == 1, f"封面应位于第1页，当前位于第 {cover} 页。"


def test_declaration_on_page_two(thesis_pages):
    decl = _find_page(thesis_pages, "原创性声明", "版权使用授权书")
    assert decl is not None, "未找到原创性声明页"
    assert decl == 2, f"原创性声明与授权书应位于第2页，当前位于第 {decl} 页。"


def test_cn_abstract_follows_declaration(thesis_pages):
    decl = _find_page(thesis_pages, "原创性声明", "版权使用授权书")
    cn_abstract = _find_page(thesis_pages, "毕业设计（论文）中文摘要", "摘 要")
    if decl is not None and cn_abstract is not None:
        assert cn_abstract == decl + 1, "中文摘要页应紧跟原创性声明页。"


def test_en_abstract_follows_cn(thesis_pages):
    cn_abstract = _find_page(thesis_pages, "毕业设计（论文）中文摘要", "摘 要")
    en_abstract = _find_page(thesis_pages, "毕业设计（论文）外文摘要", "Abstract:")
    if cn_abstract is not None and en_abstract is not None:
        assert en_abstract == cn_abstract + 1, "外文摘要页应紧跟中文摘要页。"


def test_body_after_toc(thesis_pages):
    toc = _find_page(thesis_pages, "目", "录", "绪论")
    body = _find_page(thesis_pages, "理工农医类", "绪论", "研究背景与意义")
    if toc is not None and body is not None:
        assert body > toc, "正文首页必须出现在目录页之后。"


def test_references_ordering(thesis_pages):
    body = _find_page(thesis_pages, "理工农医类", "绪论", "研究背景与意义")
    ack = _find_page(thesis_pages, "致谢", "在此感谢导师的悉心指导")
    refs = _find_page(thesis_pages, "参考文献", "示例文献标题")
    if refs is not None and body is not None:
        assert refs > body, "参考文献页顺序异常，应位于正文之后。"
    if refs is not None and ack is not None:
        assert refs > ack, "参考文献页顺序异常，应位于致谢之后。"


# ── Abstract frame checks ──────────────────────────────────────────────────

def test_cn_abstract_frame(thesis_pages):
    cn = _find_page(thesis_pages, "毕业设计（论文）中文摘要", "摘 要")
    if cn is not None:
        _assert_abstract_frame(MAIN_PDF, cn, "中文摘要页")


def test_en_abstract_frame(thesis_pages):
    en = _find_page(thesis_pages, "毕业设计（论文）外文摘要", "Abstract:")
    if en is not None:
        _assert_abstract_frame(MAIN_PDF, en, "外文摘要页")


# ── Heading centering checks ───────────────────────────────────────────────

def test_conclusion_heading_centered(thesis_pages):
    page = _find_page(thesis_pages, "结论与展望", "这里填写结论与展望的内容")
    if page is not None:
        _assert_centered_heading(MAIN_PDF, page, "结论与展望页", "结论与展望")


def test_acknowledgement_heading_centered(thesis_pages):
    page = _find_page(thesis_pages, "致谢", "在此感谢导师的悉心指导")
    if page is not None:
        _assert_centered_heading(MAIN_PDF, page, "致谢页", "致 谢")


def test_references_heading_centered(thesis_pages):
    page = _find_page(thesis_pages, "参考文献", "示例文献标题")
    if page is not None:
        _assert_centered_heading(MAIN_PDF, page, "参考文献页", "参 考 文 献")


# ── TOC and body style checks ──────────────────────────────────────────────

def test_toc_uses_arabic_numbering(thesis_pages):
    toc = _find_page(thesis_pages, "目", "录", "绪论")
    if toc is not None:
        assert "第1章" not in thesis_pages[toc], \
            "目录仍采用'第1章'体例，手册目录样式要求使用阿拉伯数字'1'。"


def test_toc_no_body_header(thesis_pages):
    toc = _find_page(thesis_pages, "目", "录", "绪论")
    if toc is not None:
        assert "江苏海洋大学二〇二六届本科毕业设计（论文）" not in thesis_pages[toc], \
            "目录页不应沿用正文章节页眉。"


def test_body_uses_arabic_heading(thesis_pages):
    body = _find_page(thesis_pages, "理工农医类", "绪论", "研究背景与意义")
    if body is not None:
        assert "第1章" not in thesis_pages[body], \
            "正文一级标题仍显示为'第1章'，手册正文样式要求为'1 绪论'。"
        assert "1绪论" in thesis_pages[body], "正文首页缺少'1 绪论'样式的一级标题。"


# ── Font embedding ──────────────────────────────────────────────────────────

def test_no_latin_modern(thesis_fonts):
    assert "LMRoman" not in thesis_fonts, \
        "PDF 嵌入了 Latin Modern Roman，而不是手册要求的 Times New Roman/对应字形。"


def test_font_stack_consistent(thesis_fonts):
    commercial_latin = any(m in thesis_fonts for m in ["TimesNewRoman", "Times-Roman", "Times New Roman"])
    commercial_cjk = any(m in thesis_fonts for m in [
        "STSong", "STKaiti", "STFangsong", "STHeiti",
        "SimSun", "KaiTi", "KaiTi_GB2312", "FangSong", "FangSong_GB2312",
        "FZShuSong", "FZFangSong", "HYKaiTi", "HYc1gj", "HYZhongJianHei",
        "HYShuSongErKW", "HYZhongHeiKW",
    ])
    licensed_mode = commercial_latin and commercial_cjk

    if licensed_mode:
        assert commercial_latin, "已检测到商业字体模式，但 PDF 未嵌入 Times New Roman 族字形。"
        assert commercial_cjk, "已检测到商业字体模式，但 PDF 未嵌入楷体_GB2312/宋体/黑体等中文标准字形。"
    else:
        expected = ["Tinos", "NotoSerifCJKsc", "LXGWWenKaiGB", "CourierPrime"]
        for font in expected:
            assert font in thesis_fonts, f"OSS 字体模式下缺少嵌入字体：{font}。"
