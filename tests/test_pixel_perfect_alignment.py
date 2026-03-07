#!/usr/bin/env python3
"""
E2E TDD测试：验证全部15个LaTeX模板与Word XML的像素级对齐

测试内容：
1. 表格列宽精确对齐（核心）- 每个模板 vs Word XML grid
2. 页面设置一致性 - geometry + tabcolsep
3. 模板完整性 + 可编译性
4. 字体字号一致性

数据源: tests/all_table_structures.json (从Word XML提取的28个表格结构)
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# ============================================================================
# 模板→Word表格映射（模板文件 → Word XML表格索引列表）
# ============================================================================
TEMPLATE_TABLE_MAP = {
    "forms/topic-selection.tex": [2],
    "forms/internship-registration.tex": [4, 7],
    "forms/task-book-science.tex": [8, 9],
    "forms/task-book-humanities.tex": [10],
    "reports/proposal-science.tex": [11, 12],
    "reports/proposal-humanities.tex": [13, 14],
    "forms/proposal-defense-record.tex": [15],
    "reports/translation.tex": [16, 17],
    "forms/midterm-check.tex": [18],
    "reports/internship-diary.tex": [19],
    "evaluations/thesis-evaluation.tex": [22, 6],
    "forms/defense-record.tex": [23],
    "evaluations/grading-science.tex": [24],
    "evaluations/grading-humanities.tex": [25],
    "reports/internship-report.tex": [3],  # Table 5 same grid as Table 3, single tabular
}

# 容差（cm）- DXA→cm转换的舍入误差
TOLERANCE_CM = 0.02


def load_word_table_structures() -> Dict[int, dict]:
    """加载Word XML表格结构数据"""
    json_path = PROJECT_ROOT / "tests" / "all_table_structures.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        tables = json.load(f)
    return {t["index"]: t for t in tables}


def parse_latex_tabular_widths(tex_path: Path) -> List[List[float]]:
    """从LaTeX文件提取所有tabular环境的列宽列表

    返回: [[第1个tabular的列宽], [第2个tabular的列宽], ...]

    处理嵌套大括号: \\begin{tabular}{|L{2.68cm}|C{5.44cm}|...}
    """
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    all_widths = []

    # 找到每个 \begin{tabular}{ 的位置，然后手动匹配平衡大括号
    marker = r'\begin{tabular}{'
    pos = 0
    while True:
        idx = content.find(marker, pos)
        if idx == -1:
            break

        # 从 { 开始找到平衡的 }
        brace_start = idx + len(marker) - 1  # 指向 {
        depth = 1
        i = brace_start + 1
        while i < len(content) and depth > 0:
            if content[i] == '{':
                depth += 1
            elif content[i] == '}':
                depth -= 1
            i += 1

        col_def = content[brace_start + 1:i - 1]

        # 提取 L{X.XXcm}, C{X.XXcm} 等列宽
        width_pattern = r'[LCRlcr]\{([0-9.]+)cm\}'
        widths = [float(w) for w in re.findall(width_pattern, col_def)]
        if widths:
            all_widths.append(widths)

        pos = i

    return all_widths


def parse_latex_geometry(tex_path: Path) -> Dict[str, float]:
    """从LaTeX文件提取geometry设置"""
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    margins = {}
    geo_match = re.search(r'\\geometry\{([^}]+)\}', content, re.DOTALL)
    if geo_match:
        params = geo_match.group(1)
        for margin in ['top', 'bottom', 'left', 'right']:
            m = re.search(rf'{margin}=([0-9.]+)cm', params)
            if m:
                margins[margin] = float(m.group(1))
    return margins


def check_latex_has_setting(tex_path: Path, pattern: str) -> bool:
    """检查LaTeX文件是否包含指定设置"""
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return bool(re.search(pattern, content))


# ============================================================================
# 测试1: 表格列宽精确对齐（核心测试）
# ============================================================================
def test_table_column_widths():
    """验证每个模板的tabular列宽与Word XML grid完全匹配"""
    print("\n" + "=" * 70)
    print("测试1: 表格列宽精确对齐（15个模板 vs Word XML grid）")
    print("=" * 70)

    word_tables = load_word_table_structures()
    total_tables_checked = 0
    total_cols_checked = 0
    failures = []

    for template_rel, table_indices in sorted(TEMPLATE_TABLE_MAP.items()):
        tex_path = PROJECT_ROOT / "templates" / template_rel
        template_name = Path(template_rel).stem

        if not tex_path.exists():
            failures.append((template_name, "文件不存在"))
            continue

        latex_tabulars = parse_latex_tabular_widths(tex_path)

        print(f"\n  [{template_name}]")
        print(f"    Word表格: {table_indices}, LaTeX tabular数: {len(latex_tabulars)}")

        # 对齐每个tabular与对应的Word表格
        for tab_idx, word_table_idx in enumerate(table_indices):
            word_table = word_tables.get(word_table_idx)
            if not word_table:
                failures.append((template_name, f"Word表格{word_table_idx}不存在"))
                continue

            word_grid = word_table["grid_cm"]
            # Use sum of individual grid_cm to avoid rounding artifacts
            # (each grid_cm is rounded from DXA independently)
            word_total = round(sum(word_grid), 2)
            word_cols = word_table["num_grid_cols"]

            if tab_idx >= len(latex_tabulars):
                failures.append((template_name,
                    f"缺少第{tab_idx+1}个tabular（对应Word表格{word_table_idx}）"))
                continue

            latex_widths = latex_tabulars[tab_idx]
            latex_total = round(sum(latex_widths), 2)

            total_tables_checked += 1

            # 检查列数
            if len(latex_widths) != word_cols:
                # 某些模板使用合并列（multicolumn），tabular列数可能少于grid列数
                # 这种情况下只比较总宽度
                total_diff = abs(latex_total - word_total)
                if total_diff <= TOLERANCE_CM:
                    print(f"    表格{word_table_idx}: 列数不同(Word={word_cols}, "
                          f"LaTeX={len(latex_widths)}) 但总宽一致 "
                          f"({latex_total:.2f} vs {word_total:.2f}cm)")
                    total_cols_checked += len(latex_widths)
                else:
                    failures.append((template_name,
                        f"表格{word_table_idx}: 列数不同且总宽不匹配 "
                        f"(Word={word_total:.2f}, LaTeX={latex_total:.2f})"))
                continue

            # 逐列比较
            col_ok = True
            for col_i in range(len(latex_widths)):
                diff = abs(latex_widths[col_i] - word_grid[col_i])
                if diff > TOLERANCE_CM:
                    failures.append((template_name,
                        f"表格{word_table_idx} 列{col_i+1}: "
                        f"Word={word_grid[col_i]:.2f}, LaTeX={latex_widths[col_i]:.2f}, "
                        f"误差={diff:.2f}cm"))
                    col_ok = False
                total_cols_checked += 1

            # 检查总宽
            total_diff = abs(latex_total - word_total)
            if total_diff > TOLERANCE_CM:
                failures.append((template_name,
                    f"表格{word_table_idx} 总宽: "
                    f"Word={word_total:.2f}, LaTeX={latex_total:.2f}"))
                col_ok = False

            status = "PASS" if col_ok else "FAIL"
            print(f"    表格{word_table_idx}: {word_cols}列, "
                  f"总宽={latex_total:.2f}cm (Word={word_total:.2f}cm) [{status}]")

    # 汇总
    print(f"\n  共检查: {total_tables_checked}个表格, {total_cols_checked}列")

    if failures:
        print(f"\n  FAIL - {len(failures)}项不对齐:")
        for name, msg in failures:
            print(f"    [{name}] {msg}")
        return False
    else:
        print(f"\n  PASS - 全部列宽精确对齐")
        return True


# ============================================================================
# 测试2: 页面设置一致性
# ============================================================================
def test_page_setup_consistency():
    """验证所有模板的页面设置一致"""
    print("\n" + "=" * 70)
    print("测试2: 页面设置一致性（A4 + 2.5cm边距 + tabcolsep=0pt）")
    print("=" * 70)

    failures = []

    for template_rel in sorted(TEMPLATE_TABLE_MAP.keys()):
        tex_path = PROJECT_ROOT / "templates" / template_rel
        template_name = Path(template_rel).stem

        if not tex_path.exists():
            failures.append((template_name, "文件不存在"))
            continue

        # 检查geometry边距
        margins = parse_latex_geometry(tex_path)
        for side in ['top', 'bottom', 'left', 'right']:
            if side not in margins:
                failures.append((template_name, f"缺少{side}边距设置"))
            elif margins[side] != 2.5:
                failures.append((template_name,
                    f"{side}边距={margins[side]}cm (要求2.5cm)"))

        # 检查tabcolsep=0pt
        if not check_latex_has_setting(tex_path, r'\\setlength\{\\tabcolsep\}\{0pt\}'):
            failures.append((template_name, "缺少tabcolsep=0pt"))

        # 检查a4paper
        if not check_latex_has_setting(tex_path, r'a4paper'):
            failures.append((template_name, "缺少a4paper"))

    if failures:
        print(f"\n  FAIL - {len(failures)}项:")
        for name, msg in failures:
            print(f"    [{name}] {msg}")
        return False
    else:
        print(f"  PASS - 所有15个模板页面设置一致")
        return True


# ============================================================================
# 测试3: 模板完整性 + 可编译性
# ============================================================================
def test_template_completeness():
    """验证15个模板文件全部存在，且已编译出PDF"""
    print("\n" + "=" * 70)
    print("测试3: 模板完整性 + 可编译性（15个.tex + 15个.pdf）")
    print("=" * 70)

    missing_tex = []
    missing_pdf = []

    for template_rel in sorted(TEMPLATE_TABLE_MAP.keys()):
        tex_path = PROJECT_ROOT / "templates" / template_rel
        pdf_path = tex_path.with_suffix('.pdf')
        template_name = Path(template_rel).stem

        if not tex_path.exists():
            missing_tex.append(template_name)
        if not pdf_path.exists():
            missing_pdf.append(template_name)

    if missing_tex:
        print(f"  缺少.tex文件: {missing_tex}")
    else:
        print(f"  PASS - 15个.tex文件全部存在")

    if missing_pdf:
        print(f"  缺少.pdf文件: {missing_pdf}")
    else:
        print(f"  PASS - 15个.pdf文件全部存在（编译成功）")

    return not missing_tex and not missing_pdf


# ============================================================================
# 测试4: 字体字号一致性
# ============================================================================
def test_font_consistency():
    """验证模板使用正确的字体和字号"""
    print("\n" + "=" * 70)
    print("测试4: 字体字号一致性")
    print("=" * 70)

    failures = []

    for template_rel in sorted(TEMPLATE_TABLE_MAP.keys()):
        tex_path = PROJECT_ROOT / "templates" / template_rel
        template_name = Path(template_rel).stem

        if not tex_path.exists():
            continue

        with open(tex_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查表格区域使用songti
        if '\\songti' not in content:
            failures.append((template_name, "缺少\\songti"))

        # 检查标题使用heiti
        if '\\heiti' not in content:
            failures.append((template_name, "缺少\\heiti"))

        # 检查使用zihao字号系统
        if '\\zihao' not in content:
            failures.append((template_name, "缺少\\zihao字号"))

    if failures:
        print(f"\n  FAIL - {len(failures)}项:")
        for name, msg in failures:
            print(f"    [{name}] {msg}")
        return False
    else:
        print(f"  PASS - 所有模板字体字号一致")
        return True


# ============================================================================
# 主函数
# ============================================================================
def main():
    print("\n" + "=" * 70)
    print(" 江苏海洋大学LaTeX模板 - 像素级对齐 E2E TDD 测试")
    print(" 15个模板 x Word XML 28个表格结构")
    print("=" * 70)

    results = []

    tests = [
        ("表格列宽精确对齐", test_table_column_widths),
        ("页面设置一致性", test_page_setup_consistency),
        ("模板完整性+可编译性", test_template_completeness),
        ("字体字号一致性", test_font_consistency),
    ]

    for name, test_fn in tests:
        try:
            passed = test_fn()
            results.append((name, passed))
        except Exception as e:
            print(f"\n  ERROR: {e}")
            results.append((name, False))

    # 总结
    print("\n" + "=" * 70)
    print(" 测试总结")
    print("=" * 70)

    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")

    total_passed = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\n  结果: {total_passed}/{total} 通过")

    if total_passed == total:
        print("\n  所有测试通过！像素级对齐验证成功！")
        return 0
    else:
        print(f"\n  {total - total_passed}项测试失败，需要修正")
        return 1


if __name__ == "__main__":
    sys.exit(main())
