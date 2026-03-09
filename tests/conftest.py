"""Shared fixtures and helpers for the JOU thesis template test suite."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

import pytest
from PIL import Image


# ── Path constants ──────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAIN_PDF = PROJECT_ROOT / "main.pdf"
MAIN_NLS = PROJECT_ROOT / "main.nls"
MAIN_FILE = PROJECT_ROOT / "main.tex"
CLASS_FILE = PROJECT_ROOT / "styles" / "jouthesis.cls"
HEADINGS_FILE = PROJECT_ROOT / "styles" / "jouheadings.sty"
JOUFONTS_FILE = PROJECT_ROOT / "styles" / "joufonts.sty"
BODY_SAMPLE_TEX = PROJECT_ROOT / "samples" / "body-sample.tex"
BODY_SAMPLE_PDF = PROJECT_ROOT / "body-sample.pdf"
REFERENCE_PDF = PROJECT_ROOT / "references" / "江苏海洋大学2026届毕业实习与设计（论文）工作手册.pdf"
SPEC_PATH = PROJECT_ROOT / "tests" / "handbook_reference_spec.json"
TABLES_PATH = PROJECT_ROOT / "tests" / "all_table_structures.json"
FONT_DIR = PROJECT_ROOT / "fonts" / "opensource"
PROPRIETARY_TIMES = PROJECT_ROOT / "fonts" / "proprietary" / "TimesNewRoman-Regular.ttf"
CHECK_FONTS_SCRIPT = PROJECT_ROOT / "scripts" / "check_fonts.py"
WORKFLOW_FILE = PROJECT_ROOT / ".github" / "workflows" / "cross-platform-fonts.yml"
FONTPATHS_EXAMPLE = PROJECT_ROOT / "styles" / "joufontspaths.local.example.tex"
EXCELLENT_ENTRY = PROJECT_ROOT / "templates" / "reports" / "excellent-thesis-abstract.tex"
EXCELLENT_STYLE = PROJECT_ROOT / "styles" / "jouexcellentabstract.sty"
EXCELLENT_PDF = PROJECT_ROOT / "templates" / "reports" / "excellent-thesis-abstract.pdf"

RENDER_DPI = 160


# ── Utility functions ───────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Collapse all whitespace (including CJK ideographic space) for comparison."""
    text = text.replace("\u3000", " ")
    return re.sub(r"\s+", "", text)


def page_text(pdf: Path, page: int) -> str:
    """Extract the raw text of a single PDF page via pdftotext."""
    completed = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def pdf_page_count(pdf: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(pdf)],
        check=True,
        text=True,
        capture_output=True,
    )
    match = re.search(r"^Pages:\s+(\d+)$", completed.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError("无法从 pdfinfo 输出解析页数")
    return int(match.group(1))


def pdffonts(pdf: Path) -> str:
    completed = subprocess.run(
        ["pdffonts", str(pdf)],
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def render_page(pdf: Path, page: int, *, dpi: int = RENDER_DPI) -> Image.Image:
    """Render a single PDF page to a greyscale PIL Image."""
    with tempfile.TemporaryDirectory() as temp_dir:
        prefix = Path(temp_dir) / "page"
        subprocess.run(
            [
                "pdftoppm",
                "-f", str(page),
                "-l", str(page),
                "-r", str(dpi),
                "-png",
                str(pdf),
                str(prefix),
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        candidates = sorted(Path(temp_dir).glob("page-*.png"))
        if not candidates:
            raise RuntimeError(f"无法渲染 {pdf.name} 第 {page} 页为 PNG")
        return Image.open(candidates[0]).convert("L").copy()


def render_page_rgba(pdf: Path, page: int, prefix: Path) -> Path:
    """Render a single PDF page to an RGBA PNG at default DPI."""
    subprocess.run(
        ["pdftoppm", "-f", str(page), "-l", str(page), "-png", str(pdf), str(prefix)],
        check=True,
        capture_output=True,
        text=True,
    )
    candidates = sorted(prefix.parent.glob(f"{prefix.name}-*.png"))
    if not candidates:
        raise RuntimeError(f"未能渲染 {pdf.name} 第 {page} 页")
    return candidates[0]


def get_pdfinfo(pdf_path: Path) -> dict[str, str]:
    info_text = subprocess.run(
        ["pdfinfo", str(pdf_path)], check=True, text=True, capture_output=True,
    ).stdout
    info: dict[str, str] = {}
    for line in info_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    return info


# ── pytest fixtures ─────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def handbook_spec() -> dict:
    """Load the handbook reference spec JSON (used by pixel-perfect tests)."""
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def word_tables() -> dict[int, dict]:
    """Load the Word XML table structures index."""
    tables = json.loads(TABLES_PATH.read_text(encoding="utf-8"))
    return {t["index"]: t for t in tables}
