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
    page_text,
    pdf_page_count,
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
    "bracketed-super-cite-style": r"setcitestyle\{super,square,comma\}",
    "upcite-command": r"newcommand\{\\upcite\}",
    "printsymbols-command": r"newcommand\{\\printsymbols\}",
    "frontmatter-list-wrapper": r"newcommand\{\\JOUFrontMatterList\}",
    "list-of-tables-command": r"newcommand\{\\JOUListOfTables\}",
    "list-of-figures-command": r"newcommand\{\\JOUListOfFigures\}",
    "list-of-tables-and-figures-command": r"newcommand\{\\JOUListOfTablesAndFigures\}",
    "table-list-format": r"titlecontents\{table\}",
    "figure-list-format": r"titlecontents\{figure\}",
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


@pytest.fixture(scope="module")
def usage_guide_content() -> str:
    return (MAIN_FILE.parent / "docs" / "guides" / "usage.md").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def claude_content() -> str:
    return (MAIN_FILE.parent / "CLAUDE.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("name,pattern", list(CLS_PATTERNS.items()), ids=list(CLS_PATTERNS.keys()))
def test_cls_has_academic_capability(cls_content: str, name: str, pattern: str):
    assert re.search(pattern, cls_content), f"类文件缺少学术能力定义：{name}"


# ── Frontmatter list behavior ──────────────────────────────────────────────

def _frontmatter_list_macro(cls_content: str) -> str:
    start = cls_content.index(r"\newcommand{\JOUFrontMatterList}[3]")
    end = cls_content.index(r"\newcommand{\JOUListOfTables}", start)
    return cls_content[start:end]


def test_frontmatter_lists_do_not_write_themselves_to_toc(cls_content: str):
    macro = _frontmatter_list_macro(cls_content)
    assert r"\addcontentsline{toc}{chapter}" not in macro, \
        "附图/附表清单页不应把自身写入正文目录"


def test_frontmatter_lists_locally_suppress_lof_lot_chapter_spacing(cls_content: str):
    macro = _frontmatter_list_macro(cls_content)
    assert r"\let\JOUFrontMatterListSavedAddVspace\addvspace" in macro, \
        "清单宏未保存原始 \\addvspace，无法证明屏蔽是局部的"
    assert r"\renewcommand{\addvspace}[1]{}" in macro, \
        ".lof/.lot 中章节分组写入的 \\addvspace{10pt} 未在清单宏内部屏蔽"


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
    ("acknowledgement-macro", r"\\JOUAcknowledgementChapter\b"),
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


def test_main_documents_jou_frontmatter_lists(main_tex_content: str):
    assert re.search(r"\\JOUListOfTablesAndFigures\b", main_tex_content), \
        "main.tex 应示例化目录后的附表清单、附图清单入口。"


@pytest.mark.parametrize(("env_name", "keyword_command"), [
    ("cnabstract", "cnkeywords"),
    ("enabstract", "enkeywords"),
])
def test_main_abstract_examples_do_not_split_before_keywords(
    main_tex_content: str, env_name: str, keyword_command: str
):
    block = re.search(
        rf"\\begin\{{{env_name}\}}(?P<body>.*?)\\end\{{{env_name}\}}",
        main_tex_content,
        re.DOTALL,
    )
    assert block, f"main.tex 缺少 {env_name} 示例。"
    assert not re.search(rf"\n\s*\n\s*\\{keyword_command}\b", block.group("body")), \
        f"{env_name} 示例中摘要正文和关键词之间不应留空行。"


def test_usage_guide_uses_shared_backmatter_macros(usage_guide_content: str):
    assert r"\JOUBackmatterChapter{结论与展望}" in usage_guide_content, \
        "使用指南应引导结论章节走共享 backmatter 宏。"
    assert r"\JOUAcknowledgementChapter" in usage_guide_content, \
        "使用指南应引导致谢走共享 backmatter 宏。"
    assert r"\JOUPrintBibliography" in usage_guide_content, \
        "使用指南应引导参考文献走共享打印宏。"
    assert r"\chapter*{致\hspace{1em}谢}" not in usage_guide_content, \
        "使用指南不应继续传播手写致谢标题间距。"
    assert r"\addcontentsline{toc}{chapter}{致谢}" not in usage_guide_content, \
        "使用指南不应继续传播手写致谢目录项。"


def test_claude_documents_bracketed_upcite(claude_content: str):
    assert "上标引用 [1]" in claude_content, \
        "CLAUDE.md 应说明 \\upcite 保留方括号，而不是裸数字上标。"
    assert "上标引用 ¹" not in claude_content, \
        "CLAUDE.md 不应继续描述裸数字上标引用。"


@pytest.mark.parametrize(("env_name", "keyword_command"), [
    ("cnabstract", "cnkeywords"),
    ("enabstract", "enkeywords"),
])
def test_usage_guide_abstract_examples_do_not_split_before_keywords(
    usage_guide_content: str, env_name: str, keyword_command: str
):
    block = re.search(
        rf"\\begin\{{{env_name}\}}(?P<body>.*?)\\end\{{{env_name}\}}",
        usage_guide_content,
        re.DOTALL,
    )
    assert block, f"使用指南缺少 {env_name} 示例。"
    assert not re.search(rf"\n\s*\n\s*\\{keyword_command}\b", block.group("body")), \
        f"使用指南 {env_name} 示例不应在摘要正文和关键词之间留空行。"


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


def test_pdf_uses_bracketed_numeric_citations():
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf")
    citation_page = None
    for page in range(1, pdf_page_count(MAIN_PDF) + 1):
        text = normalize(page_text(MAIN_PDF, page))
        if normalize("研究背景与意义") in text and normalize("上标引用") in text:
            citation_page = text
            break
    assert citation_page is not None, "未找到正文引用示例所在页面。"
    assert normalize("参考文献[1]") in citation_page, \
        "正文 \\cite 输出应保留 GB/T 数字制方括号。"
    assert normalize("上标引用[2]") in citation_page, \
        "正文 \\upcite 输出应保留 GB/T 数字制方括号。"


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
