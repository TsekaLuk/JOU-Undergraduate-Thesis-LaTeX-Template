#!/usr/bin/env python3
"""
通用 LaTeX → Markdown 转换器
用于将 .tex 文件转换为适合 banana-slides 的 Markdown 格式
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional


class TexToMarkdownConverter:
    """LaTeX 到 Markdown 转换器"""

    # 需要跳过的LaTeX环境和命令
    SKIP_PATTERNS = [
        r'\\begin{acknowledgements}.*?\\end{acknowledgements}',
        r'\\appendix',
        r'\\tableofcontents',
        r'\\listoffigures',
        r'\\listoftables',
    ]

    # 章节标题映射
    SECTION_MAPPING = {
        r'\\chapter{(.+?)}': '# {}',
        r'\\section{(.+?)}': '## {}',
        r'\\subsection{(.+?)}': '### {}',
        r'\\subsubsection{(.+?)}': '#### {}',
    }

    # 数学公式标记
    MATH_INLINE = (r'\$(.+?)\$', r'$\1$')
    MATH_DISPLAY = (r'\$\$(.+?)\$\$', r'$$\1$$')

    def __init__(self, use_pandoc: bool = True):
        """
        初始化转换器

        Args:
            use_pandoc: 是否使用pandoc进行转换（推荐，需要安装pandoc）
        """
        self.use_pandoc = use_pandoc

    def convert_file(self, input_file: Path, output_file: Path) -> bool:
        """
        转换单个 .tex 文件为 Markdown

        Args:
            input_file: 输入的 .tex 文件路径
            output_file: 输出的 .md 文件路径

        Returns:
            转换是否成功
        """
        if not input_file.exists():
            print(f"错误: 输入文件不存在: {input_file}")
            return False

        # 读取LaTeX内容
        with open(input_file, 'r', encoding='utf-8') as f:
            latex_content = f.read()

        # 转换为Markdown
        if self.use_pandoc and self._check_pandoc():
            markdown_content = self._convert_with_pandoc(latex_content)
        else:
            markdown_content = self._convert_manual(latex_content)

        # 后处理：清理和优化
        markdown_content = self._post_process(markdown_content)

        # 写入输出文件
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✓ 转换完成: {output_file}")
        return True

    def _check_pandoc(self) -> bool:
        """检查pandoc是否安装"""
        try:
            subprocess.run(['pandoc', '--version'],
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("警告: 未找到pandoc，使用手动转换（质量可能较低）")
            print("建议安装pandoc: brew install pandoc")
            return False

    def _convert_with_pandoc(self, latex_content: str) -> str:
        """使用pandoc进行转换"""
        # 预处理：移除不需要的部分
        latex_content = self._preprocess_latex(latex_content)

        try:
            result = subprocess.run(
                ['pandoc', '-f', 'latex', '-t', 'markdown', '--wrap=none'],
                input=latex_content.encode('utf-8'),
                capture_output=True,
                check=True
            )
            return result.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            print(f"pandoc转换失败: {e.stderr.decode('utf-8')}")
            print("回退到手动转换...")
            return self._convert_manual(latex_content)

    def _convert_manual(self, latex_content: str) -> str:
        """手动转换（正则替换）"""
        content = self._preprocess_latex(latex_content)

        # 转换章节标题
        for latex_cmd, md_format in self.SECTION_MAPPING.items():
            content = re.sub(latex_cmd, lambda m: md_format.format(m.group(1)), content)

        # 转换列表环境
        content = self._convert_lists(content)

        # 转换数学公式
        content = re.sub(self.MATH_INLINE[0], self.MATH_INLINE[1], content)
        content = re.sub(self.MATH_DISPLAY[0], self.MATH_DISPLAY[1], content, flags=re.DOTALL)

        # 转换强调
        content = re.sub(r'\\textbf{(.+?)}', r'**\1**', content)
        content = re.sub(r'\\emph{(.+?)}', r'*\1*', content)

        # 移除常见LaTeX命令
        content = re.sub(r'\\[a-zA-Z]+(\[.*?\])?{', '', content)
        content = re.sub(r'}', '', content)

        # 清理空行
        content = re.sub(r'\n{3,}', '\n\n', content)

        return content

    def _preprocess_latex(self, content: str) -> str:
        """预处理：移除不需要的LaTeX部分"""
        # 移除注释
        content = re.sub(r'%.*?\n', '\n', content)

        # 移除导言区（\documentclass 到 \begin{document}）
        content = re.sub(
            r'\\documentclass.*?\\begin{document}',
            '',
            content,
            flags=re.DOTALL
        )

        # 移除结尾
        content = re.sub(r'\\end{document}.*', '', content, flags=re.DOTALL)

        # 移除跳过的环境
        for pattern in self.SKIP_PATTERNS:
            content = re.sub(pattern, '', content, flags=re.DOTALL)

        return content

    def _convert_lists(self, content: str) -> str:
        """转换列表环境"""
        # itemize → 无序列表
        content = re.sub(
            r'\\begin{itemize}(.*?)\\end{itemize}',
            lambda m: self._process_items(m.group(1), '-'),
            content,
            flags=re.DOTALL
        )

        # enumerate → 有序列表
        content = re.sub(
            r'\\begin{enumerate}(.*?)\\end{enumerate}',
            lambda m: self._process_items(m.group(1), '1.'),
            content,
            flags=re.DOTALL
        )

        return content

    def _process_items(self, items_text: str, marker: str) -> str:
        """处理列表项"""
        items = re.findall(r'\\item\s+(.+?)(?=\\item|$)', items_text, re.DOTALL)
        result = []
        for i, item in enumerate(items):
            item = item.strip()
            if marker == '1.':
                result.append(f"{i+1}. {item}")
            else:
                result.append(f"{marker} {item}")
        return '\n' + '\n'.join(result) + '\n'

    def _post_process(self, content: str) -> str:
        """后处理：优化Markdown格式"""
        # 确保标题前后有空行
        content = re.sub(r'([^\n])\n(#{1,6}\s)', r'\1\n\n\2', content)
        content = re.sub(r'(#{1,6}\s.+?)\n([^\n#])', r'\1\n\n\2', content)

        # 清理多余空行
        content = re.sub(r'\n{3,}', '\n\n', content)

        # 移除LaTeX残留
        content = re.sub(r'\\\\', '\n', content)  # \\ → 换行
        content = re.sub(r'\\,|\\;|\\:|\\!', ' ', content)  # 空格命令

        # 清理首尾空白
        content = content.strip()

        return content

    def extract_metadata(self, latex_content: str) -> Dict[str, str]:
        """提取LaTeX文档的元数据（标题、作者等）"""
        metadata = {}

        # 提取标题
        title_match = re.search(r'\\title{(.+?)}', latex_content)
        if title_match:
            metadata['title'] = title_match.group(1)

        # 提取作者
        author_match = re.search(r'\\author{(.+?)}', latex_content)
        if author_match:
            metadata['author'] = author_match.group(1)

        # 提取日期
        date_match = re.search(r'\\date{(.+?)}', latex_content)
        if date_match:
            metadata['date'] = date_match.group(1)

        return metadata


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='将 LaTeX 文件转换为 Markdown 格式（用于 banana-slides）'
    )
    parser.add_argument('input', type=Path, help='输入的 .tex 文件')
    parser.add_argument('-o', '--output', type=Path, help='输出的 .md 文件（默认：同名.md）')
    parser.add_argument('--no-pandoc', action='store_true', help='不使用pandoc，强制手动转换')

    args = parser.parse_args()

    # 确定输出文件名
    if args.output is None:
        args.output = args.input.with_suffix('.md')

    # 转换
    converter = TexToMarkdownConverter(use_pandoc=not args.no_pandoc)
    success = converter.convert_file(args.input, args.output)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
