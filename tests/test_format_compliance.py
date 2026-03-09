#!/usr/bin/env python3
"""
格式规范符合性测试

验证LaTeX模板是否符合《江苏海洋大学2026届毕业实习与设计（论文）工作手册》格式要求。

注意：工作手册只规定格式要求，不提供具体表格模板。
因此本测试验证：
1. 页面设置（纸张、边距）
2. 字体字号
3. 行距
4. 表格格式（三线表规范）
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import CLASS_FILE, PROJECT_ROOT


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def cls_content() -> str:
    return CLASS_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def headings_content() -> str:
    return (PROJECT_ROOT / "styles" / "jouheadings.sty").read_text(encoding="utf-8")


# ── 1. 页面设置 ────────────────────────────────────────────────────────────

def test_paper_is_a4(cls_content: str):
    match = re.search(r"\\geometry\{([^}]+)\}", cls_content, re.DOTALL)
    assert match, "未找到 geometry 设置"
    assert "a4paper" in match.group(1), "纸张不是 A4"


@pytest.mark.parametrize("margin", ["top", "bottom", "left", "right"])
def test_margin_is_25cm(cls_content: str, margin: str):
    geo = re.search(r"\\geometry\{([^}]+)\}", cls_content, re.DOTALL)
    assert geo, "未找到 geometry 设置"
    match = re.search(rf"{margin}=([0-9.]+)cm", geo.group(1))
    assert match, f"未找到 {margin} 边距设置"
    assert float(match.group(1)) == 2.5, f"{margin} 边距为 {match.group(1)}cm，要求 2.5cm"


# ── 2. 行距 ────────────────────────────────────────────────────────────────

def test_line_spacing_is_125(cls_content: str):
    match = re.search(r"\\linespread\{([0-9.]+)\}", cls_content)
    assert match, "未找到行距设置"
    assert float(match.group(1)) == 1.25, f"行距为 {match.group(1)} 倍，要求 1.25 倍"


# ── 3. 字体字号 ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("pattern,name,desc", [
    (r"chapter=\{.*?format=\{\\JOUHeadingHei\\zihao\{-3\}", "一级标题", "小三号黑体"),
    (r"section=\{.*?format=\{\\JOUHeadingHei\\zihao\{-4\}", "二级标题", "小四号黑体"),
    (r"subsection=\{.*?format=\{\\JOUHeadingHei\\zihao\{-4\}", "三级标题", "小四号黑体"),
])
def test_heading_font_sizes(headings_content: str, pattern: str, name: str, desc: str):
    assert re.search(pattern, headings_content, re.DOTALL), \
        f"{name} 未找到 {desc} 设置"


# ── 4. 表格宏包（三线表） ─────────────────────────────────────────────────

REQUIRED_TABLE_PACKAGES = {
    "booktabs": "三线表",
    "array": "表格增强",
    "multirow": "跨行单元格",
    "makecell": "单元格内换行",
}


@pytest.mark.parametrize("pkg,desc", list(REQUIRED_TABLE_PACKAGES.items()))
def test_table_package_loaded(cls_content: str, pkg: str, desc: str):
    assert f"RequirePackage{{{pkg}}}" in cls_content, f"缺少 {desc} 支持宏包 {pkg}"


def test_three_line_table_widths(cls_content: str):
    assert "\\heavyrulewidth" in cls_content, "三线表 heavyrulewidth 未配置"
    assert "\\lightrulewidth" in cls_content, "三线表 lightrulewidth 未配置"


# ── 5. 模板完整性 ─────────────────────────────────────────────────────────

REQUIRED_TEMPLATES = {
    "forms/topic-selection.tex": "选题审题表",
    "forms/internship-registration.tex": "实习登记表",
    "forms/task-book-science.tex": "任务书（理工）",
    "forms/task-book-humanities.tex": "任务书（人文）",
    "forms/proposal-defense-record.tex": "开题答辩记录",
    "forms/midterm-check.tex": "中期检查表",
    "forms/defense-record.tex": "答辩记录",
    "reports/internship-diary.tex": "实习日记",
    "reports/internship-report.tex": "实习报告",
    "reports/proposal-science.tex": "开题报告（理工）",
    "reports/proposal-humanities.tex": "开题报告（人文）",
    "reports/excellent-thesis-abstract.tex": "校优摘要",
    "reports/translation.tex": "外文翻译",
    "evaluations/thesis-evaluation.tex": "论文评语",
    "evaluations/grading-science.tex": "评分表（理工）",
    "evaluations/grading-humanities.tex": "评分表（人文）",
}


@pytest.mark.parametrize("template,desc", list(REQUIRED_TEMPLATES.items()))
def test_template_exists(template: str, desc: str):
    path = PROJECT_ROOT / "templates" / template
    assert path.exists(), f"{desc} 模板缺失：{template}"


# ── 6. 学校视觉资源 ──────────────────────────────────────────────────────

REQUIRED_LOGOS = [
    "jou-logo-full.png",
    "jou-name-large.png",
    "jou-name-small.png",
    "jou-name-large-rgba.png",
    "jou-cover-header-clean.png",
]


@pytest.mark.parametrize("logo", REQUIRED_LOGOS)
def test_logo_file_exists(logo: str):
    assert (PROJECT_ROOT / "figures" / logo).exists(), f"缺少 logo 文件：{logo}"


def test_cover_header_configured(cls_content: str):
    assert "\\newcommand{\\JOUCoverHeader}{figures/jou-cover-header-clean.png}" in cls_content, \
        "封面页眉资源未配置"


# ── 7. 摘要页字体规则 ─────────────────────────────────────────────────────

def test_abstract_uses_preferwps(cls_content: str):
    assert "\\RequirePackage[preferwps]{styles/joufonts}" in cls_content, \
        "主模板未启用 preferwps 字体路由"


def test_cn_abstract_title_heiti_4(cls_content: str):
    assert r"{\JOUAbstractHei\bfseries\zihao{4}\@title}" in cls_content, \
        "中文摘要题名不是四号黑体"


def test_cn_abstract_label_font_split(cls_content: str):
    expected = r"{\noindent{\JOUAbstractHei\bfseries\zihao{-4}摘\hspace{1em}要：}\zihao{-4}\songti}"
    assert expected in cls_content, \
        "中文摘要标签/正文字体规则不符合预期"
