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

    required_patterns = {
        "amsthm": r"RequirePackage\{amsthm\}",
        "mathtools": r"RequirePackage\{mathtools\}",
        "bm": r"RequirePackage\{bm\}",
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

    if not MAIN_PDF.exists():
        failures.append("缺少 main.pdf，无法验证学术功能示例")
    else:
        text = normalize(run(["pdftotext", "-layout", str(MAIN_PDF), "-"]))
        expected_snippets = [
            "示例：定理、证明与智能引用",
            "模型训练流程",
            "训练脚本片段",
            "推理时延/ms",
            "符号说明",
            "卷积神经网络",
            "附录横向表示例",
        ]
        for snippet in expected_snippets:
            if normalize(snippet) not in text:
                failures.append(f"PDF 未找到学术功能示例文本：{snippet}")

        fonts = run(["pdffonts", str(MAIN_PDF)])
        has_oss_stack = all(
            font_name in fonts for font_name in ["CourierPrime", "NotoSerifCJKsc", "Tinos"]
        )
        has_latin_commercial = all(
            marker in fonts for marker in ["TimesNewRoman", "CourierNew"]
        )
        has_cjk_commercial = (
            ("SimSun" in fonts and "KaiTi_GB2312" in fonts)
            or ("STSong" in fonts and "STKaiti" in fonts)
            or (
                ("FZShuSong" in fonts or "HYShuSongErKW" in fonts)
                and ("HYKaiTi" in fonts or "HYc1gj" in fonts)
                and ("HYZhongJianHei" in fonts or "HYZhongHeiKW" in fonts)
            )
        )
        if not has_oss_stack and not (has_latin_commercial and has_cjk_commercial):
            failures.append("main.pdf 未嵌入可接受的字体栈（开源兜底或系统商用字体均未满足）")

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
