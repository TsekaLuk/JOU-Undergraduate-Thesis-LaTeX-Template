#!/usr/bin/env python3
"""
答辩PPT提取器
从完整论文中提取核心内容，生成答辩演示文稿的Markdown
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from tex2markdown import TexToMarkdownConverter


class DefenseExtractor:
    """答辩PPT内容提取器"""

    # 答辩PPT标准结构
    STANDARD_STRUCTURE = [
        ('研究背景与意义', ['背景', '意义', '引言', 'introduction']),
        ('文献综述', ['综述', '相关工作', 'related work', '国内外研究']),
        ('研究内容与方法', ['研究内容', '方法', '技术方案', '系统设计']),
        ('实验与分析', ['实验', '结果', '分析', 'experiment', 'result']),
        ('结论与展望', ['结论', '总结', 'conclusion', '未来工作']),
    ]

    def __init__(self):
        self.converter = TexToMarkdownConverter(use_pandoc=True)

    def extract(self, thesis_file: Path, chapters_dir: Path) -> str:
        """
        提取答辩PPT内容

        Args:
            thesis_file: 论文主文件 main.tex
            chapters_dir: 章节目录 contents/chapters/

        Returns:
            Markdown格式的PPT内容
        """
        # 读取主文件
        with open(thesis_file, 'r', encoding='utf-8') as f:
            main_content = f.read()

        # 提取元数据
        metadata = self._extract_metadata(main_content)

        # 读取所有章节
        chapters = self._load_chapters(main_content, chapters_dir)

        # 提取核心内容
        core_content = self._extract_core_content(chapters)

        # 生成答辩PPT结构
        ppt_markdown = self._generate_defense_ppt(metadata, core_content)

        return ppt_markdown

    def _extract_metadata(self, main_content: str) -> Dict[str, str]:
        """提取论文元数据"""
        metadata = {}

        patterns = {
            'title': r'\\title{(.+?)}',
            'entitle': r'\\entitle{(.+?)}',
            'student': r'\\author{(.+?)}',
            'studentid': r'\\studentid{(.+?)}',
            'school': r'\\major{(.+?)}',
            'major': r'\\class{(.+?)}',
            'advisor': r'\\supervisor{(.+?)}',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, main_content)
            if match:
                metadata[key] = match.group(1).strip()

        return metadata

    def _load_chapters(self, main_content: str, chapters_dir: Path) -> List[Tuple[str, str]]:
        """加载所有章节内容"""
        chapters = []

        # 从主文件提取章节引用
        chapter_includes = re.findall(r'\\include{(.+?)}', main_content)

        for include_path in chapter_includes:
            # 跳过非章节文件
            if 'chapter' not in include_path.lower():
                continue

            # 构建完整路径
            chapter_file = Path(include_path.replace('contents/chapters/', ''))
            if not chapter_file.suffix:
                chapter_file = chapter_file.with_suffix('.tex')

            full_path = chapters_dir / chapter_file.name

            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 提取章节标题
                title_match = re.search(r'\\chapter{(.+?)}', content)
                title = title_match.group(1) if title_match else chapter_file.stem

                chapters.append((title, content))

        return chapters

    def _extract_core_content(self, chapters: List[Tuple[str, str]]) -> Dict[str, str]:
        """从章节中提取核心内容"""
        core_content = {}

        for title, content in chapters:
            # 转换为Markdown
            markdown = self.converter._convert_with_pandoc(content)

            # 根据章节标题匹配到标准结构
            matched_section = None
            for section_name, keywords in self.STANDARD_STRUCTURE:
                if any(kw in title.lower() for kw in keywords):
                    matched_section = section_name
                    break

            if matched_section:
                # 提取摘要（前500字或前3段）
                summary = self._extract_summary(markdown)
                core_content[matched_section] = {
                    'title': title,
                    'summary': summary,
                    'full_content': markdown
                }

        return core_content

    def _extract_summary(self, markdown: str, max_chars: int = 500) -> str:
        """提取章节摘要"""
        # 按段落分割
        paragraphs = [p.strip() for p in markdown.split('\n\n') if p.strip() and not p.strip().startswith('#')]

        # 取前3段或500字
        summary_parts = []
        total_chars = 0

        for para in paragraphs[:5]:
            if total_chars + len(para) > max_chars:
                break
            summary_parts.append(para)
            total_chars += len(para)

        return '\n\n'.join(summary_parts)

    def _generate_defense_ppt(self, metadata: Dict[str, str], core_content: Dict[str, str]) -> str:
        """生成答辩PPT结构"""
        lines = []

        # 标题页
        lines.append(f"# {metadata.get('title', '毕业论文答辩')}")
        lines.append("")
        if 'entitle' in metadata:
            lines.append(f"*{metadata['entitle']}*")
            lines.append("")
        lines.append(f"**答辩人**: {metadata.get('student', 'XXX')}")
        lines.append(f"**学号**: {metadata.get('studentid', 'XXXXXXXX')}")
        lines.append(f"**指导教师**: {metadata.get('advisor', 'XXX')}")
        lines.append("")
        lines.append(f"{metadata.get('school', 'XXX学院')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 目录
        lines.append("## 目录")
        lines.append("")
        available_sections = [s for s, _ in self.STANDARD_STRUCTURE if s in core_content]
        for i, section in enumerate(available_sections, 1):
            lines.append(f"{i}. {section}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 内容页
        section_counter = 1
        for section_name, keywords in self.STANDARD_STRUCTURE:
            if section_name not in core_content:
                continue

            section_data = core_content[section_name]

            lines.append(f"## {section_counter}. {section_name}")
            lines.append("")

            # 添加摘要内容
            lines.append(section_data['summary'])
            lines.append("")

            # 根据不同章节类型添加特殊内容
            if section_name == '研究内容与方法':
                lines.append(self._format_methodology(section_data['full_content']))
            elif section_name == '实验与分析':
                lines.append(self._format_experiments(section_data['full_content']))

            lines.append("---")
            lines.append("")

            section_counter += 1

        # 创新点（可选）
        lines.append("## 主要贡献与创新点")
        lines.append("")
        lines.append("1. **理论创新**")
        lines.append("   - （根据论文内容填写）")
        lines.append("")
        lines.append("2. **方法创新**")
        lines.append("   - （根据实现方法填写）")
        lines.append("")
        lines.append("3. **应用价值**")
        lines.append("   - （根据实际应用填写）")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 不足与展望
        lines.append("## 不足与展望")
        lines.append("")
        lines.append("### 存在的不足")
        lines.append("")
        lines.append("- 不足之处1")
        lines.append("- 不足之处2")
        lines.append("")
        lines.append("### 未来工作")
        lines.append("")
        lines.append("- 改进方向1")
        lines.append("- 改进方向2")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 结束页
        lines.append("## 谢谢！")
        lines.append("")
        lines.append("**欢迎各位老师批评指正**")
        lines.append("")

        return '\n'.join(lines)

    def _format_methodology(self, content: str) -> str:
        """格式化研究方法章节"""
        # 提取方法列表
        methods = re.findall(r'^\s*[-*]\s+(.+)$', content, re.MULTILINE)
        if methods:
            formatted = "### 主要方法\n\n"
            for i, method in enumerate(methods[:5], 1):
                formatted += f"{i}. {method.strip()}\n"
            return formatted

        return ""

    def _format_experiments(self, content: str) -> str:
        """格式化实验结果章节"""
        # 尝试提取表格或数据
        tables = re.findall(r'\|.+\|', content, re.MULTILINE)
        if tables:
            formatted = "### 实验结果\n\n"
            formatted += '\n'.join(tables[:10])  # 最多10行表格
            return formatted

        return ""


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='从完整论文提取答辩PPT内容')
    parser.add_argument('-i', '--input', type=Path, required=True, help='论文主文件 main.tex')
    parser.add_argument('-c', '--chapters', type=Path, required=True, help='章节目录 contents/chapters/')
    parser.add_argument('-o', '--output', type=Path, help='输出的 .md 文件（默认：outputs/defense.md）')

    args = parser.parse_args()

    # 默认输出路径
    if args.output is None:
        output_dir = Path(__file__).parent.parent / 'outputs'
        output_dir.mkdir(exist_ok=True)
        args.output = output_dir / 'defense.md'

    # 提取
    extractor = DefenseExtractor()
    try:
        ppt_markdown = extractor.extract(args.input, args.chapters)

        # 写入文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(ppt_markdown)

        print(f"✓ 答辩PPT内容已生成: {args.output}")
        print(f"\n⚠️  注意：请手动补充和调整内容")
        print(f"   - 主要贡献与创新点")
        print(f"   - 实验结果图表")
        print(f"   - 不足与展望")
        print(f"\n下一步：")
        print(f"1. 编辑 {args.output} 补充详细内容")
        print(f"2. 添加关键图表和数据")
        print(f"3. 访问 banana-slides: http://localhost:3000")
        print(f"4. 上传并生成答辩PPT")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
