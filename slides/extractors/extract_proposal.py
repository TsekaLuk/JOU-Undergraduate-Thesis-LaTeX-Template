#!/usr/bin/env python3
"""
开题报告提取器
从开题报告LaTeX模板提取内容，生成适合PPT的Markdown
"""

import re
import sys
from pathlib import Path
from typing import Dict, List
from tex2markdown import TexToMarkdownConverter


class ProposalExtractor:
    """开题报告内容提取器"""

    # 开题报告关键章节（优先级排序）
    KEY_SECTIONS = [
        ('研究背景与意义', ['背景', '意义', '目的', '价值']),
        ('国内外研究现状', ['研究现状', '文献综述', '相关工作']),
        ('研究内容', ['主要内容', '研究内容', '工作内容']),
        ('研究目标', ['预期目标', '研究目标', '目标']),
        ('研究方法', ['研究方法', '技术路线', '实现方案']),
        ('技术路线', ['技术路线', '实施方案', '技术方案']),
        ('可行性分析', ['可行性', '条件分析']),
        ('工作计划', ['进度安排', '时间安排', '计划']),
        ('参考文献', ['参考文献', '主要文献']),
    ]

    def __init__(self):
        self.converter = TexToMarkdownConverter(use_pandoc=True)

    def extract(self, input_file: Path) -> str:
        """
        提取开题报告内容并格式化为PPT结构

        Args:
            input_file: 开题报告 .tex 文件

        Returns:
            Markdown格式的PPT内容
        """
        # 读取LaTeX文件
        with open(input_file, 'r', encoding='utf-8') as f:
            latex_content = f.read()

        # 提取元数据
        metadata = self._extract_metadata(latex_content)

        # 转换为Markdown
        markdown = self.converter._convert_with_pandoc(latex_content)

        # 提取章节内容
        sections = self._extract_sections(markdown)

        # 生成PPT结构的Markdown
        ppt_markdown = self._generate_ppt_structure(metadata, sections)

        return ppt_markdown

    def _extract_metadata(self, latex_content: str) -> Dict[str, str]:
        """提取开题报告元数据"""
        metadata = {}

        # 论文题目
        title_patterns = [
            r'\\题目\s*&\s*\\multicolumn.*?{(.+?)}',
            r'题\s*目.*?\n.*?{(.+?)}',
        ]
        for pattern in title_patterns:
            match = re.search(pattern, latex_content, re.DOTALL)
            if match:
                metadata['title'] = match.group(1).strip()
                break

        # 学生姓名
        name_patterns = [
            r'\\学生姓名\s*&.*?{(.+?)}',
            r'姓\s*名.*?{(.+?)}',
        ]
        for pattern in name_patterns:
            match = re.search(pattern, latex_content)
            if match:
                metadata['student'] = match.group(1).strip()
                break

        # 指导教师
        advisor_patterns = [
            r'\\指导教师.*?{(.+?)}',
            r'指导教师.*?{(.+?)}',
        ]
        for pattern in advisor_patterns:
            match = re.search(pattern, latex_content)
            if match:
                metadata['advisor'] = match.group(1).strip()
                break

        # 学院/专业
        major_patterns = [
            r'\\学院\s*&.*?{(.+?)}',
            r'学\s*院.*?{(.+?)}',
        ]
        for pattern in major_patterns:
            match = re.search(pattern, latex_content)
            if match:
                metadata['school'] = match.group(1).strip()
                break

        return metadata

    def _extract_sections(self, markdown: str) -> Dict[str, str]:
        """从Markdown中提取关键章节内容"""
        sections = {}

        # 按二级标题分割
        parts = re.split(r'\n## (.+?)\n', markdown)

        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                section_title = parts[i].strip()
                section_content = parts[i + 1].strip()

                # 匹配到关键章节
                for key_name, keywords in self.KEY_SECTIONS:
                    if any(kw in section_title for kw in keywords):
                        sections[key_name] = section_content
                        break

        return sections

    def _generate_ppt_structure(self, metadata: Dict[str, str], sections: Dict[str, str]) -> str:
        """生成PPT结构的Markdown"""
        lines = []

        # 标题页
        lines.append(f"# {metadata.get('title', '开题报告')}")
        lines.append("")
        if 'student' in metadata:
            lines.append(f"**答辩人**: {metadata['student']}")
        if 'advisor' in metadata:
            lines.append(f"**指导教师**: {metadata['advisor']}")
        if 'school' in metadata:
            lines.append(f"**学院**: {metadata['school']}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 目录页
        lines.append("## 目录")
        lines.append("")
        section_order = [s[0] for s in self.KEY_SECTIONS if s[0] in sections]
        for i, section_name in enumerate(section_order, 1):
            lines.append(f"{i}. {section_name}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 内容页（每个章节一页）
        for section_name in section_order:
            content = sections[section_name]

            lines.append(f"## {section_name}")
            lines.append("")

            # 处理内容：如果太长，提取要点
            content = self._format_section_content(section_name, content)

            lines.append(content)
            lines.append("")
            lines.append("---")
            lines.append("")

        # 结束页
        lines.append("## 谢谢！")
        lines.append("")
        lines.append("**欢迎各位老师批评指正**")
        lines.append("")

        return '\n'.join(lines)

    def _format_section_content(self, section_name: str, content: str) -> str:
        """格式化章节内容，使其适合PPT展示"""
        # 如果内容过长（>500字），尝试提取列表或要点
        if len(content) > 500:
            # 尝试提取列表项
            list_items = re.findall(r'^\s*[-*]\s+(.+)$', content, re.MULTILINE)
            if list_items:
                return '\n'.join(f"- {item.strip()}" for item in list_items[:6])

            # 尝试提取编号列表
            numbered_items = re.findall(r'^\s*\d+\.\s+(.+)$', content, re.MULTILINE)
            if numbered_items:
                return '\n'.join(f"{i+1}. {item.strip()}" for i, item in enumerate(numbered_items[:6]))

            # 按段落分割，取前3段
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            if len(paragraphs) > 3:
                content = '\n\n'.join(paragraphs[:3]) + '\n\n...'

        # 特殊处理：工作计划转为表格
        if section_name == '工作计划':
            content = self._format_schedule(content)

        # 特殊处理：参考文献精简
        if section_name == '参考文献':
            refs = re.findall(r'^\s*\[?\d+\]?\s*(.+)$', content, re.MULTILINE)
            if refs:
                content = '\n'.join(f"{i+1}. {ref.strip()}" for i, ref in enumerate(refs[:8]))

        return content

    def _format_schedule(self, content: str) -> str:
        """将工作计划格式化为表格"""
        # 尝试提取时间安排信息
        schedule_items = re.findall(
            r'(第?[一二三四五六七八九十\d]+阶段|[一二三四五六七八九十\d]+月|Week\s*\d+)[\s：:]+(.+?)(?=第?[一二三四五六七八九十\d]+阶段|[一二三四五六七八九十\d]+月|Week\s*\d+|$)',
            content,
            re.DOTALL
        )

        if schedule_items:
            lines = ["| 阶段 | 时间 | 内容 |", "|------|------|------|"]
            for i, (phase, description) in enumerate(schedule_items[:6], 1):
                desc = description.strip().replace('\n', ' ')[:100]
                lines.append(f"| 第{i}阶段 | {phase.strip()} | {desc} |")
            return '\n'.join(lines)

        return content


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='提取开题报告内容并生成PPT Markdown')
    parser.add_argument('-i', '--input', type=Path, required=True, help='开题报告 .tex 文件')
    parser.add_argument('-o', '--output', type=Path, help='输出的 .md 文件（默认：outputs/proposal.md）')

    args = parser.parse_args()

    # 默认输出路径
    if args.output is None:
        output_dir = Path(__file__).parent.parent / 'outputs'
        output_dir.mkdir(exist_ok=True)
        args.output = output_dir / 'proposal.md'

    # 提取
    extractor = ProposalExtractor()
    try:
        ppt_markdown = extractor.extract(args.input)

        # 写入文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(ppt_markdown)

        print(f"✓ 开题报告PPT内容已生成: {args.output}")
        print(f"\n下一步：")
        print(f"1. 访问 banana-slides: http://localhost:3000")
        print(f"2. 上传文件: {args.output}")
        print(f"3. 选择「学术汇报」风格模板")
        print(f"4. 生成并下载 PPTX")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
