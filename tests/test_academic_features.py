#!/usr/bin/env python3
"""
Regression checks for the academic writing feature set in jouthesis.cls.

Verifies that the thesis class ships capabilities expected by a modern academic
template: theorem/proof environments, algorithms, code listings, clever
references, SI units, nomenclature, and superscript citation support.
"""

from __future__ import annotations

import re
import subprocess

import pytest

from conftest import (
    CLASS_FILE,
    HEADINGS_FILE,
    BODY_SAMPLE_TEX,
    MAIN_FILE,
    MAIN_PDF,
    MAIN_NLS,
    normalize,
)


# ── Class-file capability checks ───────────────────────────────────────────

CLS_PATTERNS = {
    "amsthm": r"RequirePackage\{amsthm\}",
    "mathtools": r"RequirePackage\{mathtools\}",
    "bm": r"RequirePackage\{bm\}",
    "jouheadings": r"RequirePackage\{styles/jouheadings\}",
    "algorithm": r"RequirePackage\{algorithm\}",
    "algpseudocode": r"RequirePackage\{algpseudocode\}",
    "listings": r"RequirePackage\{listings\}",
    "cleveref": r"RequirePackage\[.*\]\{cleveref\}",
    "bookmark": r"RequirePackage\{bookmark\}",
    "siunitx": r"RequirePackage\{siunitx\}",
    "threeparttable": r"RequirePackage\{threeparttable\}",
    "pdflscape": r"RequirePackage\{pdflscape\}",
    "nomencl": r"RequirePackage\[intoc\]\{nomencl\}",
    "supercite-option": r"DeclareOption\{supercite\}",
    "upcite-command": r"newcommand\{\\upcite\}",
    "printsymbols-command": r"newcommand\{\\printsymbols\}",
    "theorem-env": r"newtheorem\{theorem\}\{定理\}",
    "definition-env": r"newtheorem\{definition\}\[theorem\]\{定义\}",
}


@pytest.fixture(scope="module")
def cls_content() -> str:
    return CLASS_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def headings_content() -> str:
    return HEADINGS_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def main_tex_content() -> str:
    return MAIN_FILE.read_text(encoding="utf-8")


@pytest.mark.parametrize("name,pattern", list(CLS_PATTERNS.items()), ids=list(CLS_PATTERNS.keys()))
def test_cls_has_academic_capability(cls_content: str, name: str, pattern: str):
    assert re.search(pattern, cls_content), f"类文件缺少学术能力定义：{name}"


# ── Shared backmatter heading system ───────────────────────────────────────

def test_headings_has_backmatter_heading_macro(headings_content: str):
    assert re.search(r"newcommand\{\\JOUBackmatterHeadingOnly\}", headings_content), \
        "共享标题层缺少 backmatter 统一入口：backmatter-heading-macro"


def test_headings_has_backmatter_chapter_macro(headings_content: str):
    assert re.search(r"newcommand\{\\JOUBackmatterChapter\}", headings_content), \
        "共享标题层缺少 backmatter 统一入口：backmatter-chapter-macro"


def test_bibsection_uses_shared_heading(cls_content: str):
    assert re.search(
        r"renewcommand\{\\bibsection\}\{\\JOUBackmatterHeadingOnly\{\\bibname\}\}", cls_content
    ), "参考文献标题未接入共享 backmatter 标题入口。"


# ── main.tex backmatter usage ──────────────────────────────────────────────

@pytest.mark.parametrize("name,pattern", [
    ("conclusion-macro", r"\\JOUBackmatterChapter\{结论与展望\}"),
    ("acknowledgement-macro", r"\\JOUBackmatterChapter\{致谢\}"),
])
def test_main_uses_shared_backmatter(main_tex_content: str, name: str, pattern: str):
    assert re.search(pattern, main_tex_content), \
        f"main.tex 未使用共享 backmatter 标题入口：{name}"


@pytest.mark.parametrize("pattern", [
    r"\\chapter\*\{\\centering\s*结论与展望\}",
    r"\\chapter\*\{\\centering\s*致\\hspace\{2em\}谢\}",
    r"\\renewcommand\{\\bibname\}\{\\centering",
])
def test_no_manual_centering_in_main(main_tex_content: str, pattern: str):
    assert not re.search(pattern, main_tex_content), \
        "main.tex 仍保留手工居中 backmatter 标题逻辑，未完全收敛到共享规则。"


def test_no_printsymbols_in_default(main_tex_content: str):
    assert not re.search(r"\\printsymbols\b", main_tex_content), \
        "main.tex 默认示例论文不应直接插入符号说明页。"


# ── Body sample reuses shared heading system ───────────────────────────────

SHARED_HEADING_PATTERNS = {
    "shared-chapter-line": r"\\JOUChapterHeadingLine",
    "shared-section-line": r"\\JOUSectionHeadingLine",
    "shared-subsection-line": r"\\JOUSubsectionHeadingLine",
    "shared-header-macro": r"\\JOUMakeBodyHeader",
}


@pytest.mark.parametrize("name,pattern", list(SHARED_HEADING_PATTERNS.items()))
def test_body_sample_reuses_heading_system(name: str, pattern: str):
    if not BODY_SAMPLE_TEX.exists():
        pytest.skip("缺少 samples/body-sample.tex")
    body_sample = BODY_SAMPLE_TEX.read_text(encoding="utf-8")
    assert re.search(pattern, body_sample), f"正文样页未复用统一标题系统：{name}"


# ── Rendered PDF feature snippets ──────────────────────────────────────────

EXPECTED_SNIPPETS = [
    "示例：定理、证明与智能引用",
    "模型训练流程",
    "训练脚本片段",
    "推理时延/ms",
    "附录横向表示例",
]

UNEXPECTED_SNIPPETS = [
    "符号说明",
    "卷积神经网络",
]


@pytest.fixture(scope="module")
def main_pdf_text() -> str:
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf")
    text = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", str(MAIN_PDF), "-"],
        check=True, text=True, capture_output=True,
    ).stdout
    return normalize(text)


@pytest.mark.parametrize("snippet", EXPECTED_SNIPPETS)
def test_pdf_has_academic_snippet(main_pdf_text: str, snippet: str):
    assert normalize(snippet) in main_pdf_text, f"PDF 未找到学术功能示例文本：{snippet}"


@pytest.mark.parametrize("snippet", UNEXPECTED_SNIPPETS)
def test_pdf_lacks_symbols_table_snippet(main_pdf_text: str, snippet: str):
    assert normalize(snippet) not in main_pdf_text, \
        f"默认示例论文不应展示符号表示例文本：{snippet}"


# ── Font stack validation ──────────────────────────────────────────────────

def test_pdf_has_acceptable_font_stack():
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf")
    fonts = subprocess.run(
        ["pdffonts", str(MAIN_PDF)], check=True, text=True, capture_output=True,
    ).stdout

    has_oss_stack = all(
        f in fonts for f in ["CourierPrime", "NotoSerifCJKsc", "LXGWWenKaiGB"]
    ) and any(f in fonts for f in ["NotoSansCJKsc", "FandolHei"])

    has_latin_standard = any(
        m in fonts for m in ["TimesNewRoman", "Times-Roman", "Tinos", "texgyretermes"]
    ) and any(
        m in fonts for m in ["CourierNew", "CourierPrime", "lmmono", "LMMono", "LMMono10"]
    )

    has_song = any(m in fonts for m in [
        "SimSun", "STSong", "FZShuSong", "FZSSK", "HYShuSongErKW", "NotoSerifCJKsc", "FandolSong",
    ])
    has_kai = any(m in fonts for m in [
        "KaiTi_GB2312", "KaiTi", "STKaiti", "HYKaiTi", "HYc1gj", "LXGWWenKaiGB", "FandolKai",
    ])
    has_hei = any(m in fonts for m in [
        "SimHei", "STHeiti", "HYZhongJianHei", "HYZhongHeiKW", "HYQiHei", "NotoSansCJKsc", "FandolHei",
    ])
    has_standard_cjk = has_song and has_kai and has_hei

    assert has_oss_stack or (has_latin_standard and has_standard_cjk), \
        "main.pdf 未嵌入可接受的标准学术字体栈（正文/楷体/黑体/西文字体）。"


# ── Nomenclature ───────────────────────────────────────────────────────────

def test_nomenclature_index_generated():
    assert MAIN_NLS.exists(), "缺少 main.nls，说明符号表索引尚未生成"
    assert MAIN_NLS.read_text(encoding="utf-8").strip(), "main.nls 为空，符号表未成功生成"
