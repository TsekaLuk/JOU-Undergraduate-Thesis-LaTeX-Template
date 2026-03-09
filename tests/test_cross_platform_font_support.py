#!/usr/bin/env python3
"""
Static contract checks for cross-platform font support.

Guards the repository-level promises around:
- Windows font-file probing
- WPS bundled font probing on macOS/Linux/Windows
- local path override hooks
- CI matrix coverage across the three desktop platforms
"""

import pytest

from conftest import JOUFONTS_FILE, CHECK_FONTS_SCRIPT, WORKFLOW_FILE, FONTPATHS_EXAMPLE


@pytest.fixture(scope="module")
def joufonts_content() -> str:
    return JOUFONTS_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def check_fonts_content() -> str:
    return CHECK_FONTS_SCRIPT.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def workflow_content() -> str:
    return WORKFLOW_FILE.read_text(encoding="utf-8")


# ── joufonts.sty markers ───────────────────────────────────────────────────

JOUFONTS_MARKERS = [
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


@pytest.mark.parametrize("marker", JOUFONTS_MARKERS)
def test_joufonts_has_cross_platform_marker(joufonts_content: str, marker: str):
    assert marker in joufonts_content, f"styles/joufonts.sty 缺少跨平台字体探测标记: {marker}"


# ── check_fonts.py markers ─────────────────────────────────────────────────

CHECK_FONTS_MARKERS = [
    "WINDIR",
    "ProgramFiles",
    "LOCALAPPDATA",
    "C:/Program Files/WPS Office/office6/fonts",
    "simsun.ttc",
    "simkai.ttf",
    "simfang.ttf",
]


@pytest.mark.parametrize("marker", CHECK_FONTS_MARKERS)
def test_check_fonts_has_windows_wps_marker(check_fonts_content: str, marker: str):
    assert marker in check_fonts_content, f"scripts/check_fonts.py 缺少 Windows/WPS 诊断标记: {marker}"


# ── CI workflow markers ────────────────────────────────────────────────────

CI_MARKERS = [
    "ubuntu-latest",
    "macos-latest",
    "windows-latest",
    "pytest",
]


@pytest.mark.parametrize("marker", CI_MARKERS)
def test_ci_workflow_has_platform_marker(workflow_content: str, marker: str):
    assert marker in workflow_content, f"CI workflow 缺少跨平台覆盖标记: {marker}"


# ── local override example ─────────────────────────────────────────────────

def test_local_override_example_exists():
    assert FONTPATHS_EXAMPLE.exists(), "缺少本地字体路径覆盖示例文件 styles/joufontspaths.local.example.tex"
