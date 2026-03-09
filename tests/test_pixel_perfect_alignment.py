#!/usr/bin/env python3
"""
WPS render-baseline E2E tests for the JOU handbook templates.

Defines "alignment" as a concrete contract against the WPS-exported handbook PDF:

1. The reference assets are present and stable.
2. Every supported template exists and has a compiled PDF artifact.
3. The LaTeX source uses the Word XML table grid assigned to that template.
4. The compiled PDF matches the handbook in page count and orientation.
5. Every template page lands on the expected content break, validated by
   matching anchor phrases against the corresponding handbook page.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import pytest

from conftest import (
    PROJECT_ROOT,
    FONT_DIR,
    PROPRIETARY_TIMES,
    normalize,
    get_pdfinfo,
    pdffonts as extract_pdffonts,
)


SPEC_PATH = PROJECT_ROOT / "tests" / "handbook_reference_spec.json"
TABLES_PATH = PROJECT_ROOT / "tests" / "all_table_structures.json"
TOLERANCE_CM = 0.02


# ── Helpers ─────────────────────────────────────────────────────────────────

def expected_orientation(page_size: str) -> str:
    match = re.search(r"([0-9.]+)\s+x\s+([0-9.]+)\s+pts", page_size)
    if not match:
        raise ValueError(f"Unable to parse page size: {page_size}")
    width = float(match.group(1))
    height = float(match.group(2))
    return "landscape" if width > height else "portrait"


def parse_latex_tabular_widths(tex_path: Path) -> List[List[float]]:
    content = tex_path.read_text(encoding="utf-8")
    all_widths: List[List[float]] = []

    marker = r"\begin{tabular}{"
    pos = 0
    while True:
        idx = content.find(marker, pos)
        if idx == -1:
            break

        brace_start = idx + len(marker) - 1
        depth = 1
        i = brace_start + 1
        while i < len(content) and depth > 0:
            if content[i] == "{":
                depth += 1
            elif content[i] == "}":
                depth -= 1
            i += 1

        col_def = content[brace_start + 1 : i - 1]
        widths = [float(w) for w in re.findall(r"[LCRlcr]\{([0-9.]+)cm\}", col_def)]
        if widths:
            all_widths.append(widths)
        pos = i

    return all_widths


def source_has_pattern(tex_path: Path, pattern: str) -> bool:
    return bool(re.search(pattern, tex_path.read_text(encoding="utf-8"), re.DOTALL))


def source_loads_shared_handbook_style(tex_path: Path) -> bool:
    return source_has_pattern(tex_path, r"jouhandbook")


def extract_pdf_page_text(pdf_path: Path, page: int) -> str:
    import subprocess
    return subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", "-f", str(page), "-l", str(page), str(pdf_path), "-"],
        check=True, text=True, capture_output=True,
    ).stdout


# ── Test 1: Reference baseline ─────────────────────────────────────────────

def test_reference_docx_exists(handbook_spec):
    docx = PROJECT_ROOT / handbook_spec["reference"]["docx"]
    assert docx.exists(), f"缺少参考 DOCX: {docx}"


def test_reference_pdf_exists(handbook_spec):
    pdf = PROJECT_ROOT / handbook_spec["reference"]["pdf"]
    assert pdf.exists(), f"缺少参考 PDF: {pdf}"


def test_reference_pdf_page_count(handbook_spec):
    pdf = PROJECT_ROOT / handbook_spec["reference"]["pdf"]
    if not pdf.exists():
        pytest.skip("缺少参考 PDF")
    info = get_pdfinfo(pdf)
    pages = int(info["Pages"])
    expected = handbook_spec["reference"]["expected_pages"]
    assert pages == expected, f"参考 PDF 页数={pages}，预期={expected}"


def test_reference_pdf_is_a4(handbook_spec):
    pdf = PROJECT_ROOT / handbook_spec["reference"]["pdf"]
    if not pdf.exists():
        pytest.skip("缺少参考 PDF")
    info = get_pdfinfo(pdf)
    assert handbook_spec["reference"]["page_size"] in info["Page size"], \
        f"参考 PDF 不是 A4: {info['Page size']}"


# ── Test 2: Template catalog ───────────────────────────────────────────────

def test_template_catalog_complete(handbook_spec):
    failures = []
    for t in handbook_spec["templates"]:
        if not (PROJECT_ROOT / t["tex"]).exists():
            failures.append(f"[{t['id']}] 缺少 TEX: {t['tex']}")
        if not (PROJECT_ROOT / t["pdf"]).exists():
            failures.append(f"[{t['id']}] 缺少 PDF: {t['pdf']}")
    assert not failures, "\n".join(failures)


# ── Test 3: Table grid mapping ─────────────────────────────────────────────

def test_source_table_mapping(handbook_spec, word_tables):
    failures = []
    for template in handbook_spec["templates"]:
        tex_path = PROJECT_ROOT / template["tex"]
        latex_tabulars = parse_latex_tabular_widths(tex_path)
        table_indices = template["table_indices"]

        if len(latex_tabulars) != len(table_indices):
            failures.append(
                f"[{template['id']}] tabular数量={len(latex_tabulars)}，预期={len(table_indices)}"
            )
            continue

        for tabular_idx, word_index in enumerate(table_indices):
            wt = word_tables[word_index]
            word_grid = wt["grid_cm"]
            latex_grid = latex_tabulars[tabular_idx]

            if len(word_grid) != len(latex_grid):
                failures.append(
                    f"[{template['id']}] 表格{word_index}列数不一致 "
                    f"(Word={len(word_grid)}, LaTeX={len(latex_grid)})"
                )
                continue

            for col_idx, width in enumerate(latex_grid):
                if abs(width - word_grid[col_idx]) > TOLERANCE_CM:
                    failures.append(
                        f"[{template['id']}] 表格{word_index} 第{col_idx+1}列 "
                        f"Word={word_grid[col_idx]:.2f}cm LaTeX={width:.2f}cm"
                    )

            word_total = round(sum(word_grid), 2)
            latex_total = round(sum(latex_grid), 2)
            if abs(latex_total - word_total) > TOLERANCE_CM:
                failures.append(
                    f"[{template['id']}] 表格{word_index}总宽 Word={word_total:.2f}cm LaTeX={latex_total:.2f}cm"
                )

    assert not failures, "\n".join(failures)


# ── Test 4: Source layout contract ─────────────────────────────────────────

def test_source_layout_contract(handbook_spec):
    failures = []
    for t in handbook_spec["templates"]:
        tex = PROJECT_ROOT / t["tex"]
        if not source_has_pattern(tex, r"a4paper"):
            failures.append(f"[{t['id']}] 缺少 a4paper 声明")
        if not source_has_pattern(tex, r"\\geometry\{"):
            failures.append(f"[{t['id']}] 缺少 geometry 设置")
        if (
            not source_has_pattern(tex, r"\\setlength\{\\tabcolsep\}\{0pt\}")
            and not source_loads_shared_handbook_style(tex)
        ):
            failures.append(f"[{t['id']}] 缺少 tabcolsep=0pt")

        wants_landscape = t["orientation"] == "landscape"
        has_landscape = source_has_pattern(tex, r"landscape")
        if wants_landscape and not has_landscape:
            failures.append(f"[{t['id']}] 应为 landscape，但源码未声明")
        if not wants_landscape and has_landscape:
            failures.append(f"[{t['id']}] 应为 portrait，但源码含 landscape")

    assert not failures, "\n".join(failures)


# ── Test 5: Compiled PDF contract ──────────────────────────────────────────

def test_compiled_pdf_contract(handbook_spec):
    failures = []
    for t in handbook_spec["templates"]:
        pdf = PROJECT_ROOT / t["pdf"]
        if not pdf.exists():
            failures.append(f"[{t['id']}] 缺少编译产物 PDF")
            continue
        info = get_pdfinfo(pdf)
        page_count = int(info["Pages"])
        page_size = info["Page size"]
        orientation = expected_orientation(page_size)

        if page_count != t["expected_pages"]:
            failures.append(f"[{t['id']}] 页数={page_count}，预期={t['expected_pages']}")
        if "A4" not in page_size:
            failures.append(f"[{t['id']}] 页面不是 A4: {page_size}")
        if orientation != t["orientation"]:
            failures.append(f"[{t['id']}] 方向={orientation}，预期={t['orientation']}")

    assert not failures, "\n".join(failures)


# ── Test 6: Page anchors ───────────────────────────────────────────────────

def test_reference_page_anchors(handbook_spec):
    ref_pdf = PROJECT_ROOT / handbook_spec["reference"]["pdf"]
    if not ref_pdf.exists():
        pytest.skip("缺少参考 PDF")

    failures = []
    for t in handbook_spec["templates"]:
        template_pdf = PROJECT_ROOT / t["pdf"]
        if not template_pdf.exists():
            failures.append(f"[{t['id']}] 缺少编译产物 PDF")
            continue
        template_pages = int(get_pdfinfo(template_pdf)["Pages"])

        for pc in t["page_anchors"]:
            if pc["template_page"] > template_pages:
                failures.append(
                    f"[{t['id']}] 缺少第{pc['template_page']}页，当前只有{template_pages}页"
                )
                continue

            template_text = normalize(extract_pdf_page_text(template_pdf, pc["template_page"]))
            reference_text = normalize(extract_pdf_page_text(ref_pdf, pc["reference_page"]))

            for phrase in pc["phrases"]:
                target = normalize(phrase)
                if target not in reference_text:
                    failures.append(
                        f"[{t['id']}] 参考页{pc['reference_page']} 缺少锚点 '{phrase}'"
                    )
                if target not in template_text:
                    failures.append(
                        f"[{t['id']}] 模板页{pc['template_page']} 缺少锚点 '{phrase}'"
                    )

    assert not failures, "\n".join(failures)


# ── Test 7: Font stack contract ────────────────────────────────────────────

REQUIRED_OPENSRC_FONTS = [
    "Tinos-Regular.ttf",
    "Tinos-Bold.ttf",
    "CourierPrime-Regular.ttf",
    "CourierPrime-Bold.ttf",
    "NotoSerifCJKsc-Regular.otf",
    "NotoSerifCJKsc-Bold.otf",
    "NotoSerifCJKsc-Black.otf",
    "NotoSansCJKsc-Regular.otf",
    "NotoSansCJKsc-Bold.otf",
    "LXGWWenKaiGB-Regular.ttf",
    "LXGWWenKaiGB-Medium.ttf",
    "FandolFang-Regular.otf",
]


@pytest.mark.parametrize("filename", REQUIRED_OPENSRC_FONTS)
def test_opensource_font_file_exists(filename: str):
    assert (FONT_DIR / filename).exists(), f"缺少开源字体文件: fonts/opensource/{filename}"


def test_cls_loads_joufonts():
    assert source_has_pattern(PROJECT_ROOT / "styles" / "jouthesis.cls", r"styles/joufonts"), \
        "styles/jouthesis.cls 未加载公共字体层 styles/joufonts。"


def test_handbook_style_loads_joufonts():
    assert source_has_pattern(PROJECT_ROOT / "styles" / "jouhandbook.sty", r"joufonts"), \
        "styles/jouhandbook.sty 未加载公共字体层 joufonts。"


def test_representative_pdf_font_contract():
    representative_pdfs = [
        PROJECT_ROOT / "main.pdf",
        PROJECT_ROOT / "templates" / "forms" / "topic-selection.pdf",
    ]
    existing_pdfs = [p for p in representative_pdfs if p.exists()]
    if not existing_pdfs:
        pytest.skip("缺少代表性 PDF 产物")

    font_output = "\n".join(extract_pdffonts(pdf) for pdf in existing_pdfs)

    assert "LMRoman" not in font_output, \
        "代表性 PDF 仍嵌入了 Latin Modern Roman，说明未完全切换到仓库字体。"

    uses_times = "TimesNewRoman" in font_output
    uses_oss = all(m in font_output for m in ["Tinos", "NotoSerifCJKsc", "NotoSansCJKsc"])
    uses_sys_commercial = (
        ("SimSun" in font_output and "KaiTi" in font_output)
        or ("STSong" in font_output and "STKaiti" in font_output)
    )
    uses_wps = (
        ("FZShuSong" in font_output or "HYShuSongErKW" in font_output or "FZSSK" in font_output)
        and ("HYKaiTi" in font_output or "HYc1gj" in font_output)
        and ("HYZhongJianHei" in font_output or "HYZhongHeiKW" in font_output)
    )

    if PROPRIETARY_TIMES.exists():
        assert uses_times, \
            "检测到 proprietary 字体模式，但代表性 PDF 未嵌入 Times New Roman。"
    else:
        assert uses_oss or (uses_times and (uses_sys_commercial or uses_wps)), \
            "代表性 PDF 未落在可接受的字体契约内（OSS/系统商用/WPS 字体栈均不满足）。"
