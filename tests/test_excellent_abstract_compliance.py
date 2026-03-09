#!/usr/bin/env python3
"""
Static and rendered checks for the school-level excellent abstract template.

Focuses on rules that are easy to regress silently:
- strict official-font enforcement
- fixed-width spacing for the title block and abstract label
- section-bound figure/table numbering
- hanging indent in the bibliography
"""

from __future__ import annotations

import subprocess

import pytest

from conftest import EXCELLENT_ENTRY, EXCELLENT_STYLE, EXCELLENT_PDF


# ── Source-level checks ─────────────────────────────────────────────────────

ENTRY_MARKERS = [
    r"\JOUExcellentTripleEnSpace",
    r"\JOUExcellentDoubleEnSpace",
]


@pytest.mark.parametrize("marker", ENTRY_MARKERS)
def test_entry_has_spacing_markers(marker: str):
    entry = EXCELLENT_ENTRY.read_text(encoding="utf-8")
    assert marker in entry, f"模板入口缺少固定空格控制标记：{marker}"


STYLE_MARKERS = [
    r"\RequirePackage[strictfonts,preferwps]{../../styles/joufonts}",
    r"\renewcommand{\thefigure}{\thesection-\arabic{figure}}",
    r"\renewcommand{\thetable}{\thesection-\arabic{table}}",
    r"\setlength{\JOUExcellentReferenceHangIndent}{1.57em}",
    r"\DeclareCaptionLabelSeparator{jouexcellenttwospace}",
]


@pytest.mark.parametrize("marker", STYLE_MARKERS)
def test_style_has_compliance_markers(marker: str):
    style = EXCELLENT_STYLE.read_text(encoding="utf-8")
    assert marker in style, f"版式文件缺少关键合规标记：{marker}"


# ── Rendered PDF checks ────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def excellent_pdf_text() -> str:
    if not EXCELLENT_PDF.exists():
        pytest.skip("缺少校优摘要 PDF，请先编译 templates/reports/excellent-thesis-abstract.tex")
    return subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", str(EXCELLENT_PDF), "-"],
        check=True, text=True, capture_output=True,
    ).stdout


@pytest.fixture(scope="module")
def excellent_pdf_fonts() -> str:
    if not EXCELLENT_PDF.exists():
        pytest.skip("缺少校优摘要 PDF")
    return subprocess.run(
        ["pdffonts", str(EXCELLENT_PDF)],
        check=True, text=True, capture_output=True,
    ).stdout


@pytest.mark.parametrize("snippet", ["图 1-1", "表 2-1", "English Title", "参考文献"])
def test_excellent_pdf_contains_text(excellent_pdf_text: str, snippet: str):
    assert snippet in excellent_pdf_text, f"成品 PDF 未检测到关键文本：{snippet}"


def test_excellent_pdf_embeds_times(excellent_pdf_fonts: str):
    assert "TimesNewRoman" in excellent_pdf_fonts, "成品 PDF 未嵌入 Times New Roman 族字形。"


def test_excellent_pdf_embeds_wps_kai(excellent_pdf_fonts: str):
    assert any(name in excellent_pdf_fonts for name in ["HYKaiTi", "HYc1gj"]), \
        "成品 PDF 未嵌入 WPS 楷体族字形。"


def test_excellent_pdf_embeds_wps_hei(excellent_pdf_fonts: str):
    assert any(name in excellent_pdf_fonts for name in ["HYZhong", "HYZhongJianHei", "HYZhongHei"]), \
        "成品 PDF 未嵌入 WPS 黑体族字形。"
