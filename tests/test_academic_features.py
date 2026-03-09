#!/usr/bin/env python3
"""
Regression checks for the academic writing feature set in jouthesis.cls.

This script verifies that the thesis class ships common paper-writing
capabilities expected by a modern academic template:

- theorem / proof environments
- algorithms and pseudocode
- code listings
- clever references
- SI units and table notes
- nomenclature / symbol list support
- superscript citation support
"""

import re
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
CLASS_FILE = PROJECT_ROOT / "styles" / "jouthesis.cls"
HEADINGS_FILE = PROJECT_ROOT / "styles" / "jouheadings.sty"
BODY_SAMPLE_FILE = PROJECT_ROOT / "samples" / "body-sample.tex"
MAIN_FILE = PROJECT_ROOT / "main.tex"
MAIN_PDF = PROJECT_ROOT / "main.pdf"
MAIN_NLS = PROJECT_ROOT / "main.nls"


def run(cmd: list[str]) -> str:
    completed = subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def normalize(text: str) -> str:
    text = text.replace("\u3000", " ")
    return re.sub(r"\s+", "", text)


def main() -> int:
    failures: list[str] = []
    cls = CLASS_FILE.read_text(encoding="utf-8")
    headings = HEADINGS_FILE.read_text(encoding="utf-8")
    main_tex = MAIN_FILE.read_text(encoding="utf-8")

    required_patterns = {
        "amsthm": r"RequirePackage\{amsthm\}",
        "mathtools": r"RequirePackage\{mathtools\}",
        "bm": r"RequirePackage\{bm\}",
        "jouheadings": r"RequirePackage\{styles/jouheadings\}",
        "algorithm": r"RequirePackage\{algorithm\}",
        "algpseudocode": r"RequirePackage\{algpseudocode\}",
        "listings": r"RequirePackage\{listings\}",
        "cleveref": r"RequirePackage\[.*\]\{cleveref\}",
        "bookmark": r"RequirePackage\{bookmark\}",
        "siunitx": r"RequirePackage\{siunitx\}",
        "threeparttable": r"RequirePackage\{threeparttable\}",
        "pdflscape": r"RequirePackage\{pdflscape\}",
        "nomencl": r"RequirePackage\[intoc\]\{nomencl\}",
        "supercite-option": r"DeclareOption\{supercite\}",
        "upcite-command": r"newcommand\{\\upcite\}",
        "printsymbols-command": r"newcommand\{\\printsymbols\}",
        "theorem-env": r"newtheorem\{theorem\}\{定理\}",
        "definition-env": r"newtheorem\{definition\}\[theorem\]\{定义\}",
    }

    for name, pattern in required_patterns.items():
        if not re.search(pattern, cls):
            failures.append(f"类文件缺少学术能力定义：{name}")

    shared_backmatter_patterns = {
        "backmatter-heading-macro": r"newcommand\{\\JOUBackmatterHeadingOnly\}",
        "backmatter-chapter-macro": r"newcommand\{\\JOUBackmatterChapter\}",
    }
    for name, pattern in shared_backmatter_patterns.items():
        if not re.search(pattern, headings):
            failures.append(f"共享标题层缺少 backmatter 统一入口：{name}")

    if not re.search(r"renewcommand\{\\bibsection\}\{\\JOUBackmatterHeadingOnly\{\\bibname\}\}", cls):
        failures.append("参考文献标题未接入共享 backmatter 标题入口。")

    main_backmatter_patterns = {
        "conclusion-macro": r"\\JOUBackmatterChapter\{结论与展望\}",
        "acknowledgement-macro": r"\\JOUBackmatterChapter\{致谢\}",
    }
    for name, pattern in main_backmatter_patterns.items():
        if not re.search(pattern, main_tex):
            failures.append(f"main.tex 未使用共享 backmatter 标题入口：{name}")

    manual_centering_patterns = [
        r"\\chapter\*\{\\centering\s*结论与展望\}",
        r"\\chapter\*\{\\centering\s*致\\hspace\{2em\}谢\}",
        r"\\renewcommand\{\\bibname\}\{\\centering",
    ]
    for pattern in manual_centering_patterns:
        if re.search(pattern, main_tex):
            failures.append("main.tex 仍保留手工居中 backmatter 标题逻辑，未完全收敛到共享规则。")

    if re.search(r"\\printsymbols\b", main_tex):
        failures.append("main.tex 默认示例论文不应直接插入符号说明页。")

    if not BODY_SAMPLE_FILE.exists():
        failures.append("缺少 samples/body-sample.tex，无法验证正文样页与正文标题系统复用。")
    else:
        body_sample = BODY_SAMPLE_FILE.read_text(encoding="utf-8")
        shared_heading_patterns = {
            "shared-chapter-line": r"\\JOUChapterHeadingLine",
            "shared-section-line": r"\\JOUSectionHeadingLine",
            "shared-subsection-line": r"\\JOUSubsectionHeadingLine",
            "shared-header-macro": r"\\JOUMakeBodyHeader",
        }
        for name, pattern in shared_heading_patterns.items():
            if not re.search(pattern, body_sample):
                failures.append(f"正文样页未复用统一标题系统：{name}")

    if not MAIN_PDF.exists():
        failures.append("缺少 main.pdf，无法验证学术功能示例")
    else:
        text = normalize(run(["pdftotext", "-enc", "UTF-8", "-layout", str(MAIN_PDF), "-"]))
        expected_snippets = [
            "示例：定理、证明与智能引用",
            "模型训练流程",
            "训练脚本片段",
            "推理时延/ms",
            "附录横向表示例",
        ]
        for snippet in expected_snippets:
            if normalize(snippet) not in text:
                failures.append(f"PDF 未找到学术功能示例文本：{snippet}")

        unexpected_snippets = ["符号说明", "卷积神经网络"]
        for snippet in unexpected_snippets:
            if normalize(snippet) in text:
                failures.append(f"默认示例论文不应展示符号表示例文本：{snippet}")

        fonts = run(["pdffonts", str(MAIN_PDF)])
        has_oss_stack = all(
            font_name in fonts
            for font_name in ["CourierPrime", "NotoSerifCJKsc", "LXGWWenKaiGB"]
        ) and any(font_name in fonts for font_name in ["NotoSansCJKsc", "FandolHei"])
        has_latin_standard = any(
            marker in fonts
            for marker in ["TimesNewRoman", "Times-Roman", "Tinos", "texgyretermes"]
        ) and any(
            marker in fonts
            for marker in ["CourierNew", "CourierPrime", "lmmono", "LMMono", "LMMono10"]
        )
        has_song_family = any(
            marker in fonts
            for marker in [
                "SimSun",
                "STSong",
                "FZShuSong",
                "FZSSK",
                "HYShuSongErKW",
                "NotoSerifCJKsc",
                "FandolSong",
            ]
        )
        has_kai_family = any(
            marker in fonts
            for marker in [
                "KaiTi_GB2312",
                "KaiTi",
                "STKaiti",
                "HYKaiTi",
                "HYc1gj",
                "LXGWWenKaiGB",
                "FandolKai",
            ]
        )
        has_hei_family = any(
            marker in fonts
            for marker in [
                "SimHei",
                "STHeiti",
                "HYZhongJianHei",
                "HYZhongHeiKW",
                "HYQiHei",
                "NotoSansCJKsc",
                "FandolHei",
            ]
        )
        has_standard_cjk_stack = has_song_family and has_kai_family and has_hei_family
        if not has_oss_stack and not (has_latin_standard and has_standard_cjk_stack):
            failures.append("main.pdf 未嵌入可接受的标准学术字体栈（正文/楷体/黑体/西文字体）。")

    if not MAIN_NLS.exists():
        failures.append("缺少 main.nls，说明符号表索引尚未生成")
    elif not MAIN_NLS.read_text(encoding="utf-8").strip():
        failures.append("main.nls 为空，符号表未成功生成")

    print("学术写作能力检查")
    print("=" * 72)
    if failures:
        for idx, failure in enumerate(failures, 1):
            print(f"{idx}. {failure}")
        print(f"\n结果: FAIL ({len(failures)} 项缺失)")
        return 1

    print("结果: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
