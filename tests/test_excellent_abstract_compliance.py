#!/usr/bin/env python3
"""
Static and rendered checks for the school-level excellent abstract template.

This test focuses on the rules that are easy to regress silently:
- strict official-font enforcement
- fixed-width spacing for the title block and abstract label
- section-bound figure/table numbering
- hanging indent in the bibliography
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRY = PROJECT_ROOT / "templates" / "reports" / "excellent-thesis-abstract.tex"
STYLE = PROJECT_ROOT / "styles" / "jouexcellentabstract.sty"
PDF = PROJECT_ROOT / "templates" / "reports" / "excellent-thesis-abstract.pdf"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    entry = read(ENTRY)
    style = read(STYLE)

    required_entry_markers = [
        r"\JOUExcellentTripleEnSpace",
        r"\JOUExcellentDoubleEnSpace",
    ]
    for marker in required_entry_markers:
        if marker not in entry:
            failures.append(f"模板入口缺少固定空格控制标记：{marker}")

    required_style_markers = [
        r"\RequirePackage[strictfonts,preferwps]{../../styles/joufonts}",
        r"\renewcommand{\thefigure}{\thesection-\arabic{figure}}",
        r"\renewcommand{\thetable}{\thesection-\arabic{table}}",
        r"\setlength{\JOUExcellentReferenceHangIndent}{1.57em}",
        r"\DeclareCaptionLabelSeparator{jouexcellenttwospace}",
    ]
    for marker in required_style_markers:
        if marker not in style:
            failures.append(f"版式文件缺少关键合规标记：{marker}")

    if not PDF.exists():
        failures.append("缺少校优摘要 PDF，请先编译 templates/reports/excellent-thesis-abstract.tex")
    else:
        extracted = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", "-layout", str(PDF), "-"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        for snippet in ["图 1-1", "表 2-1", "English Title", "参考文献"]:
            if snippet not in extracted:
                failures.append(f"成品 PDF 未检测到关键文本：{snippet}")

        fonts = subprocess.run(
            ["pdffonts", str(PDF)],
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        if "TimesNewRoman" not in fonts:
            failures.append("成品 PDF 未嵌入 Times New Roman 族字形。")
        if not any(name in fonts for name in ["HYKaiTi", "HYc1gj"]):
            failures.append("成品 PDF 未嵌入 WPS 楷体族字形。")
        if not any(name in fonts for name in ["HYZhong", "HYZhongJianHei", "HYZhongHei"]):
            failures.append("成品 PDF 未嵌入 WPS 黑体族字形。")

    print("校优摘要模板合规检查")
    print("=" * 72)
    if failures:
        for idx, failure in enumerate(failures, 1):
            print(f"{idx}. {failure}")
        print(f"\n结果: FAIL ({len(failures)} 项异常)")
        return 1

    print("结果: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
