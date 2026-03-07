<div align="center">

<img src="figures/jou-logo-full.png" alt="Jiangsu Ocean University Logo" width="200"/>

# JOU Undergraduate Thesis LaTeX Template

**江苏海洋大学本科生毕业设计（论文）LaTeX 模板**

*Jiangsu Ocean University Undergraduate Thesis LaTeX Template*

[![License: LPPL 1.3c](https://img.shields.io/badge/License-LPPL%201.3c-blue.svg)](https://www.latex-project.org/lppl.txt)
[![TeX Live](https://img.shields.io/badge/TeX%20Live-2020+-green.svg)](https://www.tug.org/texlive/)
[![XeLaTeX](https://img.shields.io/badge/Engine-XeLaTeX-orange.svg)](#)
[![CTAN](https://img.shields.io/badge/CTAN-Ready-success.svg)](#)

English | [简体中文](README.md)

</div>

---

## About

This LaTeX template provides a complete, ready-to-use solution for undergraduate thesis at Jiangsu Ocean University (JOU), strictly adhering to the *2026 Graduation Internship and Thesis Work Manual*.

The template includes **16 document templates**:
- 1 main thesis document
- 15 auxiliary forms (internship, proposal, defense, grading, etc.)

All templates achieve **pixel-perfect alignment** with official Word templates through precise extraction of table grid structures from Word XML.

---

## Highlights

- **🎯 Pixel-Perfect** — Column widths extracted from Word XML (`w:tblGrid` → `w:gridCol`), error < 0.01cm
- **📚 Complete Workflow** — Covers all thesis stages from topic selection to final grading
- **🔧 Independent Templates** — Each form is a standalone `.tex` file for easy compilation
- **✅ Automated Testing** — E2E tests verify 126 columns across 21 tables (4/4 PASS)
- **🎨 AI PowerPoint** — Integrated tool to auto-generate presentation slides from thesis

---

## Quick Start

### 1. Install TeX Distribution

**Requirement**: TeX Live 2020+ or MikTeX 2.9+

- **macOS**: `brew install --cask mactex`
- **Windows**: Download [TeX Live](https://www.tug.org/texlive/) or [MikTeX](https://miktex.org/)
- **Linux**: `sudo apt-get install texlive-full`

### 2. Compile Thesis

```bash
# Clone repository
git clone https://github.com/TsekaLuk/JOU-Undergraduate-Thesis-LaTeX-Template.git
cd JOU-Undergraduate-Thesis-LaTeX-Template

# Compile using Makefile (recommended)
make

# Or compile manually
xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex
```

### 3. Edit Your Information

Open `main.tex` and update:

```latex
\title{Your Thesis Title in Chinese}
\entitle{Your Thesis Title in English}
\author{Your Name}
\studentid{Your Student ID}
\major{Your School}
\class{Your Major and Class}
\supervisor{Your Supervisor (Title)}
```

---

## Template Overview

### Main Thesis

| File | Description |
|------|-------------|
| `main.tex` | Main thesis document |

### Auxiliary Forms (15 templates)

**Forms (7)**
- Topic Selection Form
- Internship Registration
- Task Book (Science/Humanities editions)
- Proposal Defense Record
- Midterm Check Form
- Defense Record

**Reports (5)**
- Internship Diary
- Internship Report
- Proposal Report (Science/Humanities editions)
- Foreign Literature Translation

**Evaluations (3)**
- Thesis Evaluation
- Grading Form (Science/Humanities editions)

See [templates/README.md](templates/README.md) for detailed descriptions.

---

## Advanced Features

### AI Presentation Generator

Automatically convert your thesis into professional PowerPoint presentations:

```bash
cd slides/
make all  # Generates proposal/midterm/defense PPTs
```

Powered by [banana-slides](https://github.com/Anionex/banana-slides) with AI-assisted layout and styling.

See [slides/README.md](slides/README.md) for setup and usage.

---

## Project Structure

```
├── main.tex                   # Main thesis file
├── Makefile                   # Build automation
├── styles/
│   └── jouthesis.cls          # Document class
├── contents/
│   ├── chapters/              # Thesis chapters
│   ├── appendices/            # Appendices
│   └── acknowledgements.tex   # Acknowledgements
├── templates/                 # 15 auxiliary forms
│   ├── forms/                 # 7 form templates
│   ├── reports/               # 5 report templates
│   └── evaluations/           # 3 evaluation templates
├── slides/                    # Paper-to-Slide toolkit
└── tests/                     # E2E tests
```

---

## Format Specifications

### Page Layout

- Paper: A4 (210mm × 297mm)
- Margins: 2.5cm all sides
- Line Spacing: 1.25
- Header: "江苏海洋大学本科生毕业论文" (5pt KaiTi_GB2312)
- Footer: Centered page number (5pt)

### Typography

- **Chinese**: SimSun (Songti) 12pt body text, SimHei (Heiti) for headings
- **English**: Times New Roman 12pt
- **Captions**: KaiTi_GB2312 10.5pt

---

## Testing

Run automated tests to verify template accuracy:

```bash
python3 tests/test_pixel_perfect_alignment.py
```

Tests cover:
- Table column widths (126 columns × 21 tables)
- Page layout consistency
- Template completeness
- Font/size consistency

All tests: ✅ 4/4 PASS

---

## Documentation

| File | Content |
|------|---------|
| [USAGE.md](USAGE.md) | Detailed usage: chapters, figures, tables, equations |
| [TABLE-EXAMPLES.md](TABLE-EXAMPLES.md) | Table formatting examples |
| [ASSETS.md](ASSETS.md) | Logo and image specifications |
| [templates/README.md](templates/README.md) | Form template documentation |
| [slides/README.md](slides/README.md) | Presentation generation guide |

---

## Troubleshooting

**Font errors?**
- Install KaiTi_GB2312 and FangSong_GB2312 fonts
- Windows: pre-installed
- macOS/Linux: install manually or via `fontconfig`

**Bibliography not showing?**
- Run 4-step compilation: `xelatex` → `bibtex` → `xelatex` → `xelatex`
- Or use `make` / `latexmk -xelatex`

**Chinese text garbled?**
- Must use `xelatex` compiler (not `pdflatex`)

---

## Contributing

Contributions welcome! Please:

1. Fork this repository
2. Create a feature branch
3. Commit your changes
4. Push and create a Pull Request

---

## License

Licensed under [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt).

**Maintainer**: [TsekaLuk](https://github.com/TsekaLuk)

Modified versions must use a different name.

---

## Citation

```bibtex
@software{jou_thesis_template,
  author = {TsekaLuk},
  title = {JOU Undergraduate Thesis LaTeX Template},
  year = {2026},
  url = {https://github.com/TsekaLuk/JOU-Undergraduate-Thesis-LaTeX-Template},
  version = {1.0}
}
```

---

## Acknowledgements

- Jiangsu Ocean University for official Word templates
- Inspired by [THU Thesis](https://github.com/tuna/thuthesis), [USTC Thesis](https://github.com/ustctug/ustcthesis)
- [banana-slides](https://github.com/Anionex/banana-slides) for AI presentation generation

---

<div align="center">

**⭐ Star this project if it helps you! ⭐**

*Official guidelines compliant | Pixel-perfect | E2E tested*

Made with ❤️ for JOU students

</div>
