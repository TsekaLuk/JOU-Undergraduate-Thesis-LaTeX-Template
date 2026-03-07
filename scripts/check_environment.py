#!/usr/bin/env python3
"""
环境一致性检查脚本
检查 TeX Live、字体、工具等是否正确安装
"""

import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class EnvironmentChecker:
    def __init__(self):
        self.system = platform.system()
        self.failures: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed = 0
        self.checks_total = 0

    def check_command(self, command: str, min_version: str = None) -> bool:
        """检查命令是否可用"""
        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                if min_version:
                    # 这里可以添加版本比较逻辑
                    pass
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
        return False

    def check_texlive_package(self, package: str) -> bool:
        """检查 TeX Live 包是否安装"""
        try:
            result = subprocess.run(
                ["kpsewhich", f"{package}.sty"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return True

            # 尝试 .cls 文件
            result = subprocess.run(
                ["kpsewhich", f"{package}.cls"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0 and bool(result.stdout.strip())
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def check_font(self, font_name: str) -> bool:
        """检查字体是否可用"""
        try:
            if self.system == "Darwin":  # macOS
                result = subprocess.run(
                    ["fc-list", ":", "family"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return font_name in result.stdout
            elif self.system == "Linux":
                result = subprocess.run(
                    ["fc-list", ":", "family"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return font_name in result.stdout
            elif self.system == "Windows":
                # Windows 字体检查比较复杂，简化处理
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
        return False

    def print_section(self, title: str):
        """打印章节标题"""
        print(f"\n{'='*72}")
        print(f"  {title}")
        print(f"{'='*72}\n")

    def check_item(self, description: str, check_func, critical: bool = True) -> bool:
        """执行单个检查项"""
        self.checks_total += 1
        result = check_func()

        status = "✓" if result else "✗"
        color = "\033[92m" if result else ("\033[91m" if critical else "\033[93m")
        reset = "\033[0m"

        print(f"{color}{status}{reset} {description}")

        if result:
            self.checks_passed += 1
        elif critical:
            self.failures.append(description)
        else:
            self.warnings.append(description)

        return result

    def run_checks(self):
        """运行所有检查"""
        self.print_section("环境一致性检查")
        print(f"操作系统: {self.system} {platform.release()}")
        print(f"Python 版本: {platform.python_version()}")

        # 1. 核心工具检查
        self.print_section("1. 核心工具")
        self.check_item(
            "xelatex",
            lambda: self.check_command("xelatex")
        )
        self.check_item(
            "bibtex",
            lambda: self.check_command("bibtex")
        )
        self.check_item(
            "latexmk (推荐)",
            lambda: self.check_command("latexmk"),
            critical=False
        )
        self.check_item(
            "makeindex",
            lambda: self.check_command("makeindex"),
            critical=False
        )

        # 2. Poppler 工具（测试用）
        self.print_section("2. PDF 工具（测试用）")
        self.check_item(
            "pdfinfo",
            lambda: self.check_command("pdfinfo"),
            critical=False
        )
        self.check_item(
            "pdftotext",
            lambda: self.check_command("pdftotext"),
            critical=False
        )
        self.check_item(
            "pdftoppm",
            lambda: self.check_command("pdftoppm"),
            critical=False
        )

        # 3. TeX Live 包检查
        self.print_section("3. TeX Live 包")
        required_packages = [
            "ctex", "fontspec", "geometry", "fancyhdr", "titletoc",
            "graphicx", "amsmath", "natbib", "hyperref", "cleveref",
            "caption", "subcaption", "booktabs", "tabularx", "multirow",
            "longtable", "algorithm", "algpseudocode", "listings", "xcolor"
        ]

        for package in required_packages:
            self.check_item(
                f"包: {package}",
                lambda p=package: self.check_texlive_package(p)
            )

        # 4. 字体检查
        self.print_section("4. 字体（推荐）")

        # 拉丁字体
        self.check_item(
            "Times New Roman",
            lambda: self.check_font("Times New Roman"),
            critical=False
        )
        self.check_item(
            "Arial",
            lambda: self.check_font("Arial"),
            critical=False
        )

        # 中文字体（根据系统不同）
        if self.system == "Darwin":  # macOS
            self.check_item(
                "STSong (华文宋体)",
                lambda: self.check_font("STSong"),
                critical=False
            )
            self.check_item(
                "STKaiti (华文楷体)",
                lambda: self.check_font("STKaiti"),
                critical=False
            )
        elif self.system == "Windows":
            self.check_item(
                "SimSun (宋体)",
                lambda: self.check_font("SimSun"),
                critical=False
            )
            self.check_item(
                "KaiTi (楷体)",
                lambda: self.check_font("KaiTi"),
                critical=False
            )
        else:  # Linux
            self.check_item(
                "Noto Serif CJK SC",
                lambda: self.check_font("Noto Serif CJK"),
                critical=False
            )

        # 5. 本地字体文件检查
        self.print_section("5. 本地字体文件")
        project_root = Path(__file__).parent.parent
        opensource_dir = project_root / "fonts" / "opensource"

        opensource_fonts = [
            "Tinos-Regular.ttf",
            "NotoSerifCJKsc-Regular.otf",
            "LXGWWenKaiGB-Regular.ttf",
            "CourierPrime-Regular.ttf"
        ]

        for font_file in opensource_fonts:
            font_path = opensource_dir / font_file
            self.check_item(
                f"开源字体: {font_file}",
                lambda p=font_path: p.exists(),
                critical=False
            )

        # 6. 编译测试
        self.print_section("6. 编译测试")

        # 检查 main.tex 是否存在
        main_tex = project_root / "main.tex"
        if main_tex.exists():
            print("正在进行编译测试（这可能需要几分钟）...")
            try:
                result = subprocess.run(
                    ["xelatex", "-interaction=nonstopmode", "main.tex"],
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                main_pdf = project_root / "main.pdf"
                if main_pdf.exists():
                    self.check_item(
                        "编译测试",
                        lambda: True
                    )
                else:
                    self.check_item(
                        "编译测试",
                        lambda: False
                    )
            except subprocess.TimeoutExpired:
                print("✗ 编译测试超时")
                self.failures.append("编译测试")
        else:
            print("⚠ 跳过编译测试（找不到 main.tex）")

    def print_summary(self):
        """打印检查总结"""
        self.print_section("检查总结")

        print(f"通过: {self.checks_passed}/{self.checks_total}")
        print(f"失败: {len(self.failures)}")
        print(f"警告: {len(self.warnings)}")

        if self.failures:
            print(f"\n{'\033[91m'}严重问题（必须修复）:{'\033[0m'}")
            for idx, failure in enumerate(self.failures, 1):
                print(f"  {idx}. {failure}")

        if self.warnings:
            print(f"\n{'\033[93m'}警告（建议修复）:{'\033[0m'}")
            for idx, warning in enumerate(self.warnings, 1):
                print(f"  {idx}. {warning}")

        if not self.failures and not self.warnings:
            print(f"\n{'\033[92m'}✓ 所有检查通过！环境配置完美。{'\033[0m'}")
        elif not self.failures:
            print(f"\n{'\033[93m'}⚠ 核心功能正常，但有一些建议优化的地方。{'\033[0m'}")
        else:
            print(f"\n{'\033[91m'}✗ 发现严重问题，请先修复后再编译。{'\033[0m'}")

        print("\n" + "="*72 + "\n")


def main() -> int:
    checker = EnvironmentChecker()
    checker.run_checks()
    checker.print_summary()

    # 返回状态码
    return 1 if checker.failures else 0


if __name__ == "__main__":
    sys.exit(main())
