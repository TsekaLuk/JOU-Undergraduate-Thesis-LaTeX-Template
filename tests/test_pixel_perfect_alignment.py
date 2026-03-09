#!/usr/bin/env python3
"""
WPS render-baseline E2E tests for the JOU handbook templates.

This test suite defines "alignment" as a concrete contract against the
WPS-exported handbook PDF:

1. The reference assets are present and stable.
2. Every supported template exists and has a compiled PDF artifact.
3. The LaTeX source uses the Word XML table grid assigned to that template.
4. The compiled PDF matches the handbook in page count and orientation.
5. Every template page lands on the expected content break, validated by
   matching anchor phrases against the corresponding handbook page.

The authoritative spec lives in tests/handbook_reference_spec.json.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


PROJECT_ROOT = Path(__file__).parent.parent
SPEC_PATH = PROJECT_ROOT / "tests" / "handbook_reference_spec.json"
TABLES_PATH = PROJECT_ROOT / "tests" / "all_table_structures.json"
TOLERANCE_CM = 0.02
FONT_DIR = PROJECT_ROOT / "fonts" / "opensource"
PROPRIETARY_TIMES = PROJECT_ROOT / "fonts" / "proprietary" / "TimesNewRoman-Regular.ttf"


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def load_word_table_structures() -> Dict[int, dict]:
    tables = json.loads(TABLES_PATH.read_text(encoding="utf-8"))
    return {table["index"]: table for table in tables}


def normalize_text(text: str) -> str:
    text = text.replace("\u3000", " ")
    text = re.sub(r"\s+", "", text)
    return text


def run_command(cmd: List[str]) -> str:
    completed = subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def get_pdfinfo(pdf_path: Path) -> Dict[str, str]:
    info_text = run_command(["pdfinfo", str(pdf_path)])
    info: Dict[str, str] = {}
    for line in info_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    return info


def extract_pdf_page_text(pdf_path: Path, page: int) -> str:
    return run_command(
        ["pdftotext", "-enc", "UTF-8", "-layout", "-f", str(page), "-l", str(page), str(pdf_path), "-"]
    )


def extract_pdffonts(pdf_path: Path) -> str:
    return run_command(["pdffonts", str(pdf_path)])


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


def expected_orientation(page_size: str) -> str:
    match = re.search(r"([0-9.]+)\s+x\s+([0-9.]+)\s+pts", page_size)
    if not match:
        raise ValueError(f"Unable to parse page size: {page_size}")
    width = float(match.group(1))
    height = float(match.group(2))
    return "landscape" if width > height else "portrait"


def print_header(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def test_reference_baseline(spec: dict) -> bool:
    print_header("测试1: WPS参考基线存在且稳定")
    reference = spec["reference"]
    failures: List[str] = []

    docx_path = PROJECT_ROOT / reference["docx"]
    pdf_path = PROJECT_ROOT / reference["pdf"]

    if not docx_path.exists():
        failures.append(f"缺少参考 DOCX: {docx_path}")
    else:
        print(f"  PASS - 参考 DOCX 存在: {reference['docx']}")

    if not pdf_path.exists():
        failures.append(f"缺少参考 PDF: {pdf_path}")
    else:
        pdfinfo = get_pdfinfo(pdf_path)
        pages = int(pdfinfo["Pages"])
        page_size = pdfinfo["Page size"]
        if pages != reference["expected_pages"]:
            failures.append(
                f"参考 PDF 页数={pages}，预期={reference['expected_pages']}"
            )
        else:
            print(f"  PASS - 参考 PDF 页数={pages}")

        if reference["page_size"] not in page_size:
            failures.append(f"参考 PDF 不是 A4: {page_size}")
        else:
            print(f"  PASS - 参考 PDF 页面={page_size}")

        print(f"  基准来源: {reference['renderer']}")

    if failures:
        print("\n  FAIL:")
        for failure in failures:
            print(f"    {failure}")
        return False
    return True


def test_template_catalog(spec: dict) -> bool:
    print_header("测试2: 模板目录完整性（18个模板全部纳入E2E）")
    failures: List[str] = []

    for template in spec["templates"]:
        tex_path = PROJECT_ROOT / template["tex"]
        pdf_path = PROJECT_ROOT / template["pdf"]
        if not tex_path.exists():
            failures.append(f"[{template['id']}] 缺少 TEX: {template['tex']}")
        if not pdf_path.exists():
            failures.append(f"[{template['id']}] 缺少 PDF: {template['pdf']}")

    if failures:
        print("\n  FAIL:")
        for failure in failures:
            print(f"    {failure}")
        return False

    print(f"  PASS - {len(spec['templates'])} 个模板的 TEX/PDF 全部存在")
    return True


def test_source_table_mapping(spec: dict, word_tables: Dict[int, dict]) -> bool:
    print_header("测试3: LaTeX源码表格网格与Word XML映射一致")
    failures: List[str] = []
    total_tables = 0
    total_cols = 0

    for template in spec["templates"]:
        tex_path = PROJECT_ROOT / template["tex"]
        latex_tabulars = parse_latex_tabular_widths(tex_path)
        table_indices = template["table_indices"]

        if len(latex_tabulars) != len(table_indices):
            failures.append(
                f"[{template['id']}] tabular数量={len(latex_tabulars)}，"
                f"预期={len(table_indices)}"
            )
            continue

        for tabular_idx, word_index in enumerate(table_indices):
            word_table = word_tables[word_index]
            word_grid = word_table["grid_cm"]
            word_total = round(sum(word_grid), 2)
            latex_grid = latex_tabulars[tabular_idx]
            latex_total = round(sum(latex_grid), 2)

            total_tables += 1

            if len(word_grid) != len(latex_grid):
                failures.append(
                    f"[{template['id']}] 表格{word_index}列数不一致 "
                    f"(Word={len(word_grid)}, LaTeX={len(latex_grid)})"
                )
                continue

            for col_idx, width in enumerate(latex_grid):
                diff = abs(width - word_grid[col_idx])
                if diff > TOLERANCE_CM:
                    failures.append(
                        f"[{template['id']}] 表格{word_index} 第{col_idx + 1}列 "
                        f"Word={word_grid[col_idx]:.2f}cm LaTeX={width:.2f}cm"
                    )
                total_cols += 1

            if abs(latex_total - word_total) > TOLERANCE_CM:
                failures.append(
                    f"[{template['id']}] 表格{word_index}总宽 "
                    f"Word={word_total:.2f}cm LaTeX={latex_total:.2f}cm"
                )

    print(f"  共检查 {total_tables} 个表格，{total_cols} 列")

    if failures:
        print("\n  FAIL:")
        for failure in failures:
            print(f"    {failure}")
        return False

    print("  PASS - 所有模板的表格列宽映射与 Word XML 一致")
    return True


def test_source_layout_contract(spec: dict) -> bool:
    print_header("测试4: LaTeX源码页面声明符合约定")
    failures: List[str] = []

    for template in spec["templates"]:
        tex_path = PROJECT_ROOT / template["tex"]

        if not source_has_pattern(tex_path, r"a4paper"):
            failures.append(f"[{template['id']}] 缺少 a4paper 声明")
        if not source_has_pattern(tex_path, r"\\geometry\{"):
            failures.append(f"[{template['id']}] 缺少 geometry 设置")
        if (
            not source_has_pattern(tex_path, r"\\setlength\{\\tabcolsep\}\{0pt\}")
            and not source_loads_shared_handbook_style(tex_path)
        ):
            failures.append(f"[{template['id']}] 缺少 tabcolsep=0pt")

        wants_landscape = template["orientation"] == "landscape"
        has_landscape = source_has_pattern(tex_path, r"landscape")
        if wants_landscape and not has_landscape:
            failures.append(f"[{template['id']}] 应为 landscape，但源码未声明")
        if not wants_landscape and has_landscape:
            failures.append(f"[{template['id']}] 应为 portrait，但源码含 landscape")

    if failures:
        print("\n  FAIL:")
        for failure in failures:
            print(f"    {failure}")
        return False

    print("  PASS - 所有模板都声明了 A4/geometry/tabcolsep，方向与 spec 一致")
    return True


def test_compiled_pdf_contract(spec: dict) -> bool:
    print_header("测试5: 编译产物页数与方向对齐手册")
    failures: List[str] = []

    for template in spec["templates"]:
        pdf_path = PROJECT_ROOT / template["pdf"]
        pdfinfo = get_pdfinfo(pdf_path)
        page_count = int(pdfinfo["Pages"])
        page_size = pdfinfo["Page size"]
        orientation = expected_orientation(page_size)

        if page_count != template["expected_pages"]:
            failures.append(
                f"[{template['id']}] 页数={page_count}，预期={template['expected_pages']}"
            )

        if "A4" not in page_size:
            failures.append(f"[{template['id']}] 页面不是 A4: {page_size}")

        if orientation != template["orientation"]:
            failures.append(
                f"[{template['id']}] 方向={orientation}，预期={template['orientation']}"
            )

    if failures:
        print("\n  FAIL:")
        for failure in failures:
            print(f"    {failure}")
        return False

    print("  PASS - 所有编译产物的页数、纸张和方向符合手册基线")
    return True


def test_reference_page_anchors(spec: dict) -> bool:
    print_header("测试6: WPS参考页与模板页的分页锚点一致")
    failures: List[str] = []
    reference_pdf = PROJECT_ROOT / spec["reference"]["pdf"]

    for template in spec["templates"]:
        template_pdf = PROJECT_ROOT / template["pdf"]
        template_pages = int(get_pdfinfo(template_pdf)["Pages"])

        for page_check in template["page_anchors"]:
            if page_check["template_page"] > template_pages:
                failures.append(
                    f"[{template['id']}] 缺少第{page_check['template_page']}页，"
                    f"当前只有{template_pages}页"
                )
                continue

            template_text = normalize_text(
                extract_pdf_page_text(template_pdf, page_check["template_page"])
            )
            reference_text = normalize_text(
                extract_pdf_page_text(reference_pdf, page_check["reference_page"])
            )

            for phrase in page_check["phrases"]:
                target = normalize_text(phrase)
                if target not in reference_text:
                    failures.append(
                        f"[{template['id']}] 参考页{page_check['reference_page']} "
                        f"缺少锚点“{phrase}”"
                    )
                if target not in template_text:
                    failures.append(
                        f"[{template['id']}] 模板页{page_check['template_page']} "
                        f"缺少锚点“{phrase}”"
                    )

    if failures:
        print("\n  FAIL:")
        for failure in failures:
            print(f"    {failure}")
        return False

    print("  PASS - 每个模板页都落在与手册相同的内容分段上")
    return True


def test_font_stack_contract(spec: dict) -> bool:
    print_header("测试7: 跨平台字体资源与嵌入字体契约")
    failures: List[str] = []

    required_fonts = [
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

    for filename in required_fonts:
        if not (FONT_DIR / filename).exists():
            failures.append(f"缺少开源字体文件: fonts/opensource/{filename}")

    if not source_has_pattern(PROJECT_ROOT / "styles" / "jouthesis.cls", r"styles/joufonts"):
        failures.append("styles/jouthesis.cls 未加载公共字体层 styles/joufonts。")

    if not source_has_pattern(PROJECT_ROOT / "styles" / "jouhandbook.sty", r"joufonts"):
        failures.append("styles/jouhandbook.sty 未加载公共字体层 joufonts。")

    representative_pdfs = [
        PROJECT_ROOT / "main.pdf",
        PROJECT_ROOT / "templates" / "forms" / "topic-selection.pdf",
    ]
    font_output = "\n".join(extract_pdffonts(pdf) for pdf in representative_pdfs if pdf.exists())

    if "LMRoman" in font_output:
        failures.append("代表性 PDF 仍嵌入了 Latin Modern Roman，说明未完全切换到仓库字体。")

    uses_times = "TimesNewRoman" in font_output
    uses_oss_stack = all(marker in font_output for marker in ["Tinos", "NotoSerifCJKsc", "NotoSansCJKsc"])
    uses_system_commercial = (
        ("SimSun" in font_output and "KaiTi" in font_output)
        or ("STSong" in font_output and "STKaiti" in font_output)
    )
    uses_wps_stack = (
        ("FZShuSong" in font_output or "HYShuSongErKW" in font_output or "FZSSK" in font_output)
        and ("HYKaiTi" in font_output or "HYc1gj" in font_output)
        and ("HYZhongJianHei" in font_output or "HYZhongHeiKW" in font_output)
    )

    if PROPRIETARY_TIMES.exists():
        if not uses_times:
            failures.append("检测到 proprietary 字体模式，但代表性 PDF 未嵌入 Times New Roman。")
    elif not (uses_oss_stack or (uses_times and (uses_system_commercial or uses_wps_stack))):
        failures.append("代表性 PDF 未落在可接受的字体契约内（OSS / 系统商用 / WPS 字体栈均不满足）。")

    if failures:
        print("\n  FAIL:")
        for failure in failures:
            print(f"    {failure}")
        return False

    print("  PASS - 仓库内字体资源完整，代表性 PDF 使用了统一字体栈")
    return True


def main() -> int:
    spec = load_spec()
    word_tables = load_word_table_structures()

    print_header("江苏海洋大学模板对齐 E2E TDD（手册基线）")
    print(f"参考 DOCX: {spec['reference']['docx']}")
    print(f"参考 PDF : {spec['reference']['pdf']}")
    print(f"模板数量 : {len(spec['templates'])}")

    tests: List[Tuple[str, bool]] = []
    test_functions = [
        ("WPS参考基线", lambda: test_reference_baseline(spec)),
        ("模板目录完整性", lambda: test_template_catalog(spec)),
        ("Word XML表格映射", lambda: test_source_table_mapping(spec, word_tables)),
        ("源码页面声明", lambda: test_source_layout_contract(spec)),
        ("编译产物页数/方向", lambda: test_compiled_pdf_contract(spec)),
        ("分页锚点一致性", lambda: test_reference_page_anchors(spec)),
        ("跨平台字体契约", lambda: test_font_stack_contract(spec)),
    ]

    for name, test_fn in test_functions:
        try:
            tests.append((name, test_fn()))
        except Exception as exc:
            print(f"\n  ERROR - {name}: {exc}")
            tests.append((name, False))

    print_header("测试总结")
    passed_count = sum(1 for _, passed in tests if passed)
    for name, passed in tests:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")

    print(f"\n  结果: {passed_count}/{len(tests)} 通过")
    if passed_count == len(tests):
        print("\n  所有手册基线 E2E 测试通过。")
        return 0

    print(f"\n  仍有 {len(tests) - passed_count} 项失败，需要继续收敛模板版式。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
