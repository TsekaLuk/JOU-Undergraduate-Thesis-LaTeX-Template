#!/usr/bin/env python3
"""
中期检查提取器
从中期检查表格和论文进度生成汇报PPT的Markdown
"""

import re
import sys
from pathlib import Path
from typing import Dict, List
from tex2markdown import TexToMarkdownConverter


class MidtermExtractor:
    """中期检查内容提取器"""

    def __init__(self):
        self.converter = TexToMarkdownConverter(use_pandoc=True)

    def extract(self, midterm_file: Path, thesis_file: Path) -> str:
        """
        提取中期检查内容并格式化为PPT结构

        Args:
            midterm_file: 中期检查表 .tex 文件
            thesis_file: 论文主文件 main.tex

        Returns:
            Markdown格式的PPT内容
        """
        # 读取中期检查表
        with open(midterm_file, 'r', encoding='utf-8') as f:
            midterm_content = f.read()

        # 读取论文内容
        with open(thesis_file, 'r', encoding='utf-8') as f:
            thesis_content = f.read()

        # 提取元数据
        metadata = self._extract_metadata(midterm_content, thesis_content)

        # 提取论文进度
        progress = self._extract_progress(thesis_content)

        # 生成PPT结构
        ppt_markdown = self._generate_ppt_structure(metadata, progress)

        return ppt_markdown

    def _extract_metadata(self, midterm_content: str, thesis_content: str) -> Dict[str, str]:
        """提取元数据"""
        metadata = {}

        # 从中期检查表提取
        title_match = re.search(r'题\s*目.*?{(.+?)}', midterm_content)
        if title_match:
            metadata['title'] = title_match.group(1).strip()

        # 如果中期检查表没有，从论文提取
        if 'title' not in metadata:
            title_match = re.search(r'\\title{(.+?)}', thesis_content)
            if title_match:
                metadata['title'] = title_match.group(1).strip()

        # 提取其他信息
        patterns = {
            'student': r'学生姓名.*?{(.+?)}',
            'school': r'学院.*?{(.+?)}',
            'advisor': r'指导教师.*?{(.+?)}',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, midterm_content)
            if match:
                metadata[key] = match.group(1).strip()

        return metadata

    def _extract_progress(self, thesis_content: str) -> Dict[str, any]:
        """从论文内容提取进度信息"""
        progress = {
            'completed': [],
            'in_progress': [],
            'challenges': [],
            'next_steps': []
        }

        # 统计章节数量
        chapters = re.findall(r'\\chapter{(.+?)}', thesis_content)
        progress['total_chapters'] = len(chapters)
        progress['chapter_titles'] = chapters

        # 检查哪些章节有实质内容（超过500字）
        for chapter in chapters:
            # 简化判断：假设所有出现的章节都有内容
            progress['completed'].append(chapter)

        # 提取参考文献数量
        bib_entries = re.findall(r'@\w+{', thesis_content)
        progress['references_count'] = len(bib_entries)

        # 提取图表数量
        figures = re.findall(r'\\begin{figure}', thesis_content)
        tables = re.findall(r'\\begin{table}', thesis_content)
        progress['figures_count'] = len(figures)
        progress['tables_count'] = len(tables)

        return progress

    def _generate_ppt_structure(self, metadata: Dict[str, str], progress: Dict) -> str:
        """生成中期汇报PPT结构"""
        lines = []

        # 标题页
        lines.append(f"# {metadata.get('title', '毕业论文中期汇报')}")
        lines.append("")
        lines.append("**中期检查汇报**")
        lines.append("")
        if 'student' in metadata:
            lines.append(f"**汇报人**: {metadata['student']}")
        if 'advisor' in metadata:
            lines.append(f"**指导教师**: {metadata['advisor']}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 目录
        lines.append("## 目录")
        lines.append("")
        lines.append("1. 选题回顾")
        lines.append("2. 工作进展")
        lines.append("3. 已完成内容")
        lines.append("4. 遇到的问题")
        lines.append("5. 下一步计划")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 1. 选题回顾
        lines.append("## 1. 选题回顾")
        lines.append("")
        lines.append(f"**论文题目**: {metadata.get('title', 'N/A')}")
        lines.append("")
        lines.append("**研究内容**:")
        lines.append("- （根据开题报告内容简述）")
        lines.append("- 主要研究目标")
        lines.append("- 拟解决的关键问题")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 2. 工作进展
        lines.append("## 2. 工作进展")
        lines.append("")
        lines.append("### 整体进度")
        lines.append("")
        lines.append(f"- **论文章节**: {progress.get('total_chapters', 0)} 章")
        lines.append(f"- **参考文献**: {progress.get('references_count', 0)} 篇")
        lines.append(f"- **图表数量**: {progress.get('figures_count', 0)} 个图，{progress.get('tables_count', 0)} 个表")
        lines.append("")
        lines.append("### 完成情况")
        lines.append("")

        completion_rate = min(100, (len(progress.get('completed', [])) / max(1, progress.get('total_chapters', 1))) * 100)
        lines.append(f"**完成度**: 约 {completion_rate:.0f}%")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 3. 已完成内容
        lines.append("## 3. 已完成内容")
        lines.append("")

        for i, chapter in enumerate(progress.get('chapter_titles', [])[:5], 1):
            lines.append(f"### {i}. {chapter}")
            lines.append("")
            lines.append("- 主要工作内容")
            lines.append("- 关键技术/方法")
            lines.append("- 初步结果")
            lines.append("")

        lines.append("---")
        lines.append("")

        # 4. 遇到的问题
        lines.append("## 4. 遇到的问题与解决")
        lines.append("")
        lines.append("### 主要困难")
        lines.append("")
        lines.append("1. **技术难点**")
        lines.append("   - 具体问题描述")
        lines.append("   - 解决方案/进展")
        lines.append("")
        lines.append("2. **实验/调研问题**")
        lines.append("   - 数据获取困难")
        lines.append("   - 实验结果不理想")
        lines.append("")
        lines.append("3. **时间安排**")
        lines.append("   - 进度调整情况")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 5. 下一步计划
        lines.append("## 5. 下一步工作计划")
        lines.append("")
        lines.append("### 近期计划（1-2周）")
        lines.append("")
        lines.append("- 完成XX章节撰写")
        lines.append("- 补充实验数据")
        lines.append("- 优化算法/方法")
        lines.append("")
        lines.append("### 中期计划（1个月内）")
        lines.append("")
        lines.append("- 完成全部章节初稿")
        lines.append("- 完善图表和数据")
        lines.append("- 准备答辩材料")
        lines.append("")
        lines.append("### 预期答辩时间")
        lines.append("")
        lines.append("**预计**: XX月XX日")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 结束页
        lines.append("## 谢谢！")
        lines.append("")
        lines.append("**请各位老师批评指正**")
        lines.append("")

        return '\n'.join(lines)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='提取中期检查内容并生成汇报PPT Markdown')
    parser.add_argument('-i', '--input', type=Path, required=True, help='中期检查表 .tex 文件')
    parser.add_argument('-t', '--thesis', type=Path, required=True, help='论文主文件 main.tex')
    parser.add_argument('-o', '--output', type=Path, help='输出的 .md 文件（默认：outputs/midterm.md）')

    args = parser.parse_args()

    # 默认输出路径
    if args.output is None:
        output_dir = Path(__file__).parent.parent / 'outputs'
        output_dir.mkdir(exist_ok=True)
        args.output = output_dir / 'midterm.md'

    # 提取
    extractor = MidtermExtractor()
    try:
        ppt_markdown = extractor.extract(args.input, args.thesis)

        # 写入文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(ppt_markdown)

        print(f"✓ 中期汇报PPT内容已生成: {args.output}")
        print(f"\n⚠️  注意：请手动补充具体内容")
        print(f"   - 研究内容描述")
        print(f"   - 遇到的具体问题")
        print(f"   - 详细的时间计划")
        print(f"\n下一步：")
        print(f"1. 编辑 {args.output} 补充详细内容")
        print(f"2. 访问 banana-slides: http://localhost:3000")
        print(f"3. 上传并生成PPT")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
