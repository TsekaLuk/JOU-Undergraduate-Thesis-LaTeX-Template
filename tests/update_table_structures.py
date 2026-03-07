#!/usr/bin/env python3
"""
自动更新LaTeX模板表格结构以匹配Word XML

使用Word文档中提取的精确网格结构更新所有LaTeX模板
"""

import re
from pathlib import Path

# 从Word XML提取的精确表格网格结构
WORD_GRID_STRUCTURES = {
    "internship-registration": {
        "file": "templates/forms/internship-registration.tex",
        "grid": [1.49, 0.68, 3.18, 2.21, 7.48],  # 5列, 总15.04cm
        "description": "实习登记表（5列网格系统）"
    },
    "task-book-science": {
        "file": "templates/forms/task-book-science.tex",
        "grid": [1.49, 0.68, 3.18, 2.21, 7.48],  # 5列, 总15.04cm
        "description": "任务书（理工农医类）（5列网格系统）"
    },
    "task-book-humanities": {
        "file": "templates/forms/task-book-humanities.tex",
        "grid": [3.33, 9.67],  # 2列, 总13.00cm
        "description": "任务书（人文经管类）（2列系统）"
    },
}

def generate_latex_grid(grid_widths):
    """生成LaTeX tabular列定义"""
    cols = '|'.join([f"L{{{w}cm}}" for w in grid_widths])
    return f"|{cols}|"

def generate_multicolumn_width(grid_widths, start_col=0, span=None):
    """计算multicolumn的总宽度"""
    if span is None:
        span = len(grid_widths) - start_col
    total = sum(grid_widths[start_col:start_col+span])
    return f"{total:.2f}cm"

def update_template(template_info):
    """更新单个模板文件"""
    file_path = Path(template_info["file"])
    if not file_path.exists():
        print(f"  ⚠️  文件不存在: {file_path}")
        return False

    grid = template_info["grid"]
    total_width = sum(grid)

    print(f"\n{'='*70}")
    print(f"更新: {template_info['description']}")
    print(f"{'='*70}")
    print(f"文件: {file_path}")
    print(f"网格: {grid} (总宽 {total_width:.2f}cm)")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 生成新的列定义
    new_col_def = generate_latex_grid(grid)
    print(f"新列定义: \\begin{{tabular}}{{{new_col_def}}}")

    # 替换所有tabular环境的列定义
    # 匹配: \begin{tabular}{...}
    pattern = r'\\begin\{tabular\}\{[^}]+\}'
    matches = re.findall(pattern, content)

    if matches:
        print(f"\n找到 {len(matches)} 个表格定义:")
        for i, match in enumerate(matches[:3], 1):  # 只显示前3个
            print(f"  {i}. {match}")

        # 替换
        new_content = re.sub(
            pattern,
            f'\\\\begin{{tabular}}{{{new_col_def}}}',
            content
        )

        # 备份原文件
        backup_path = file_path.with_suffix('.tex.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ 已备份原文件: {backup_path}")

        # 写入新内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 已更新表格列定义")

        return True
    else:
        print("  ⚠️  未找到表格定义")
        return False

def main():
    """主函数"""
    print("\n" + "🔧 "*35)
    print("LaTeX模板表格结构自动更新工具")
    print("目标: 完全复刻Word XML中的精确网格结构")
    print("🔧 "*35)

    print("\n将更新以下模板:")
    for i, (name, info) in enumerate(WORD_GRID_STRUCTURES.items(), 1):
        grid_str = ' + '.join([f"{w}cm" for w in info['grid']])
        total = sum(info['grid'])
        print(f"  {i}. {info['description']}")
        print(f"     网格: {grid_str} = {total:.2f}cm")

    input("\n按Enter键开始更新...")

    success_count = 0
    for name, info in WORD_GRID_STRUCTURES.items():
        if update_template(info):
            success_count += 1

    print("\n" + "="*70)
    print("更新完成")
    print("="*70)
    print(f"✅ 成功更新: {success_count}/{len(WORD_GRID_STRUCTURES)}")
    print(f"📦 备份文件: *.tex.bak")

    print("\n下一步:")
    print("1. 编译测试: cd templates/forms && xelatex task-book-science.tex")
    print("2. 检查输出: 对比PDF与Word文档")
    print("3. 如有问题: 使用备份文件恢复 (mv *.tex.bak *.tex)")

    return success_count == len(WORD_GRID_STRUCTURES)

if __name__ == "__main__":
    exit(0 if main() else 1)
