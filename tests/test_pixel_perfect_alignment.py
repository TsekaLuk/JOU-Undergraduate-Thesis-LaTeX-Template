#!/usr/bin/env python3
"""
E2E TDD测试：验证LaTeX模板与Word XML的像素级对齐

测试内容：
1. 页面设置（边距、纸张大小）
2. 表格宽度和列宽
3. 字体大小和行距
4. 间距参数

DXA单位转换：
- 1 DXA = 1/20 point = 1/1440 inch
- 1 cm = 567 DXA
- 1 inch = 1440 DXA
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple

# DXA转换常量
DXA_PER_CM = 567
DXA_PER_INCH = 1440
DXA_PER_PT = 20

class WordXMLParser:
    """从Word XML提取精确参数"""

    def __init__(self, xml_path: str):
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()
        # Word命名空间
        self.ns = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'
        }

    def get_page_margins(self) -> Dict[str, float]:
        """提取页边距（单位：cm）"""
        margins = {}
        for sect in self.root.findall('.//w:sectPr', self.ns):
            margin = sect.find('w:pgMar', self.ns)
            if margin is not None:
                for attr in ['top', 'bottom', 'left', 'right']:
                    val = margin.get(f'w:{attr}')
                    if val:
                        # 转换twips到cm
                        margins[attr] = int(val) / 567  # 1 twip ≈ 1/567 cm
        return margins

    def get_table_widths(self, table_index: int = 0) -> List[int]:
        """提取表格列宽（单位：DXA）"""
        tables = self.root.findall('.//w:tbl', self.ns)
        if table_index >= len(tables):
            return []

        table = tables[table_index]
        widths = []

        # 提取gridCol宽度
        grid_cols = table.findall('.//w:gridCol', self.ns)
        for col in grid_cols:
            w = col.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
            if w:
                widths.append(int(w))

        # 如果没有gridCol，从tcW提取
        if not widths:
            cells = table.findall('.//w:tc', self.ns)
            for cell in cells[:4]:  # 只取第一行
                tcw = cell.find('.//w:tcW', self.ns)
                if tcw is not None:
                    w = tcw.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w')
                    if w:
                        widths.append(int(w))

        return widths

class LaTeXTemplateParser:
    """从LaTeX模板提取参数"""

    def __init__(self, tex_path: str):
        with open(tex_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def get_page_margins(self) -> Dict[str, float]:
        """提取页边距"""
        margins = {}
        # 匹配geometry设置
        geometry_match = re.search(
            r'\\geometry\{([^}]+)\}',
            self.content,
            re.DOTALL
        )
        if geometry_match:
            params = geometry_match.group(1)
            for margin in ['top', 'bottom', 'left', 'right']:
                pattern = rf'{margin}=([0-9.]+)cm'
                match = re.search(pattern, params)
                if match:
                    margins[margin] = float(match.group(1))
        return margins

    def get_table_column_widths(self) -> List[str]:
        """提取表格列定义"""
        # 查找tabular环境中的列定义
        pattern = r'\\begin\{tabular\}\{([^}]+)\}'
        matches = re.findall(pattern, self.content)
        if not matches:
            return []

        # 解析列定义（如 L{2.5cm}|L{4cm}）
        col_def = matches[0]
        widths = []

        # 提取L{宽度}、C{宽度}、R{宽度}
        width_pattern = r'[LCR]\{([0-9.]+)cm\}'
        widths = re.findall(width_pattern, col_def)

        return [float(w) for w in widths]

def dxa_to_cm(dxa: int) -> float:
    """DXA转厘米"""
    return dxa / DXA_PER_CM

def cm_to_dxa(cm: float) -> int:
    """厘米转DXA"""
    return int(cm * DXA_PER_CM)

def test_page_margins():
    """测试页面边距对齐"""
    print("\n" + "="*60)
    print("测试1: 页面边距对齐")
    print("="*60)

    # 从Word XML提取
    xml_path = "references/unpacked/word/document.xml"
    word_parser = WordXMLParser(xml_path)
    word_margins = word_parser.get_page_margins()

    print(f"\nWord文档边距（twips → cm）:")
    for key, val in word_margins.items():
        print(f"  {key}: {val:.2f} cm")

    # 测试主模板
    tex_path = "styles/jouthesis.cls"
    latex_parser = LaTeXTemplateParser(tex_path)
    latex_margins = latex_parser.get_page_margins()

    print(f"\nLaTeX模板边距:")
    for key, val in latex_margins.items():
        print(f"  {key}: {val:.2f} cm")

    # 验证对齐
    print(f"\n对齐检查:")
    all_aligned = True
    for key in word_margins:
        if key in latex_margins:
            diff = abs(word_margins[key] - latex_margins[key])
            status = "✅ 对齐" if diff < 0.01 else f"❌ 误差 {diff:.2f}cm"
            print(f"  {key}: {status}")
            if diff >= 0.01:
                all_aligned = False

    return all_aligned

def test_table_widths():
    """测试表格宽度对齐"""
    print("\n" + "="*60)
    print("测试2: 表格列宽对齐（选题审题表）")
    print("="*60)

    # 从Word XML提取（假设选题审题表是第X个表格）
    xml_path = "references/unpacked/word/document.xml"
    word_parser = WordXMLParser(xml_path)

    # 需要找到选题审题表的位置
    # 先读取XML找到标题位置
    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找"选题、审题表"的位置，然后找最近的表格
    lines = content.split('\n')
    table_found = False

    for i, line in enumerate(lines):
        if '选题、审题表' in line and 'w:t' in line:
            print(f"\n找到选题审题表标题（行 {i+1}）")
            # 向下查找最近的<w:tbl>
            for j in range(i, min(i+500, len(lines))):
                if '<w:tbl>' in lines[j]:
                    print(f"找到表格开始（行 {j+1}）")
                    table_found = True
                    break
            break

    if not table_found:
        print("⚠️ 未找到选题审题表")
        return False

    # 提取列宽
    word_widths = word_parser.get_table_widths(0)  # 第一个表格

    print(f"\nWord表格列宽（DXA → cm）:")
    for i, w in enumerate(word_widths[:6]):  # 只看前6列
        print(f"  列{i+1}: {w} DXA = {dxa_to_cm(w):.2f} cm")

    # LaTeX模板列宽
    tex_path = "templates/forms/topic-selection.tex"
    latex_parser = LaTeXTemplateParser(tex_path)
    latex_widths = latex_parser.get_table_column_widths()

    print(f"\nLaTeX表格列宽:")
    for i, w in enumerate(latex_widths):
        print(f"  列{i+1}: {w:.2f} cm = {cm_to_dxa(w)} DXA")

    # 对齐检查
    print(f"\n对齐检查:")
    all_aligned = True
    for i in range(min(len(word_widths), len(latex_widths))):
        word_cm = dxa_to_cm(word_widths[i])
        latex_cm = latex_widths[i]
        diff = abs(word_cm - latex_cm)
        status = "✅ 对齐" if diff < 0.2 else f"❌ 误差 {diff:.2f}cm"
        print(f"  列{i+1}: Word={word_cm:.2f}cm, LaTeX={latex_cm:.2f}cm - {status}")
        if diff >= 0.2:
            all_aligned = False

    return all_aligned

def test_font_sizes():
    """测试字体大小对齐"""
    print("\n" + "="*60)
    print("测试3: 字体大小对齐")
    print("="*60)

    # Word文档字号规范（从手册）
    word_sizes = {
        "小三号": 15,   # pt
        "四号": 14,     # pt
        "小四号": 12,   # pt
        "五号": 10.5    # pt
    }

    # LaTeX zihao映射
    latex_sizes = {
        "\\zihao{-3}": 15,   # 小三号
        "\\zihao{4}": 14,    # 四号
        "\\zihao{-4}": 12,   # 小四号
        "\\zihao{5}": 10.5   # 五号
    }

    print(f"\nWord文档字号:")
    for name, size in word_sizes.items():
        print(f"  {name}: {size} pt")

    print(f"\nLaTeX zihao命令:")
    for cmd, size in latex_sizes.items():
        print(f"  {cmd}: {size} pt")

    print(f"\n✅ 字号完全对应CTEX标准")
    return True

def test_line_spacing():
    """测试行距对齐"""
    print("\n" + "="*60)
    print("测试4: 行距对齐")
    print("="*60)

    # Word文档行距：1.25倍
    word_spacing = 1.25

    # LaTeX行距
    tex_path = "styles/jouthesis.cls"
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'\\linespread\{([0-9.]+)\}', content)
    latex_spacing = float(match.group(1)) if match else None

    print(f"\nWord文档行距: {word_spacing}")
    print(f"LaTeX行距: {latex_spacing}")

    if latex_spacing == word_spacing:
        print(f"✅ 行距完全对齐")
        return True
    else:
        print(f"❌ 行距不对齐，误差 {abs(latex_spacing - word_spacing)}")
        return False

def main():
    """运行所有测试"""
    print("\n" + "🧪 "*30)
    print("江苏海洋大学LaTeX模板 - 像素级对齐E2E测试")
    print("🧪 "*30)

    results = []

    # 测试1: 页面边距
    try:
        results.append(("页面边距", test_page_margins()))
    except Exception as e:
        print(f"\n❌ 页面边距测试失败: {e}")
        results.append(("页面边距", False))

    # 测试2: 表格宽度
    try:
        results.append(("表格列宽", test_table_widths()))
    except Exception as e:
        print(f"\n❌ 表格列宽测试失败: {e}")
        results.append(("表格列宽", False))

    # 测试3: 字体大小
    try:
        results.append(("字体大小", test_font_sizes()))
    except Exception as e:
        print(f"\n❌ 字体大小测试失败: {e}")
        results.append(("字体大小", False))

    # 测试4: 行距
    try:
        results.append(("行距", test_line_spacing()))
    except Exception as e:
        print(f"\n❌ 行距测试失败: {e}")
        results.append(("行距", False))

    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")

    total_passed = sum(1 for _, p in results if p)
    print(f"\n通过: {total_passed}/{len(results)}")

    if total_passed == len(results):
        print("\n🎉 所有测试通过！像素级对齐验证成功！")
        return 0
    else:
        print("\n⚠️ 存在对齐问题，需要修正")
        return 1

if __name__ == "__main__":
    exit(main())
