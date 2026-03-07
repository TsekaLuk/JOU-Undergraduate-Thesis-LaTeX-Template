#!/usr/bin/env python3
"""
Static contract checks for cross-platform font support.

This guards the repository-level promises around:
- Windows font-file probing
- WPS bundled font probing on macOS/Linux/Windows
- local path override hooks
- CI matrix coverage across the three desktop platforms
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
JOUFONTS = PROJECT_ROOT / "styles" / "joufonts.sty"
CHECK_FONTS = PROJECT_ROOT / "scripts" / "check_fonts.py"
WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "cross-platform-fonts.yml"
EXAMPLE = PROJECT_ROOT / "styles" / "joufontspaths.local.example.tex"


def main() -> int:
    failures: list[str] = []

    joufonts = JOUFONTS.read_text(encoding="utf-8")
    checks = CHECK_FONTS.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    required_joufonts_markers = [
        "C:/Windows/Fonts",
        "C:/Program Files/WPS Office/office6/fonts",
        "C:/Program Files (x86)/WPS Office/office6/fonts",
        "C:/Program Files/Kingsoft/WPS Office/office6/fonts",
        "styles/joufontspaths.local.tex",
        "times.ttf",
        "simsun.ttc",
        "simkai.ttf",
        "simfang.ttf",
        "jou@setupwindowslatin",
        "jou@setupwindowscjk",
    ]
    for marker in required_joufonts_markers:
        if marker not in joufonts:
            failures.append(f"styles/joufonts.sty 缺少跨平台字体探测标记: {marker}")

    required_check_markers = [
        "WINDIR",
        "ProgramFiles",
        "LOCALAPPDATA",
        "C:/Program Files/WPS Office/office6/fonts",
        "simsun.ttc",
        "simkai.ttf",
        "simfang.ttf",
    ]
    for marker in required_check_markers:
        if marker not in checks:
            failures.append(f"scripts/check_fonts.py 缺少 Windows/WPS 诊断标记: {marker}")

    required_workflow_markers = [
        "ubuntu-latest",
        "macos-latest",
        "windows-latest",
        "tests/test_cross_platform_font_support.py",
        "tests/test_thesis_alignment.py",
        "tests/test_cover_alignment.py",
    ]
    for marker in required_workflow_markers:
        if marker not in workflow:
            failures.append(f"CI workflow 缺少跨平台覆盖标记: {marker}")

    if not EXAMPLE.exists():
        failures.append("缺少本地字体路径覆盖示例文件 styles/joufontspaths.local.example.tex")

    print("跨系统字体支持检查")
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
