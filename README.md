<div align="center">

<img src="figures/jou-logo-full.png" alt="江苏海洋大学校徽" width="200"/>

# JOU Undergraduate Thesis LaTeX Template

**江苏海洋大学本科生毕业设计（论文）LaTeX 模板**

*Jiangsu Ocean University Undergraduate Thesis LaTeX Template*

[![License: LPPL 1.3c](https://img.shields.io/badge/License-LPPL%201.3c-blue.svg)](https://www.latex-project.org/lppl.txt)
[![TeX Live](https://img.shields.io/badge/TeX%20Live-2020+-green.svg)](https://www.tug.org/texlive/)
[![XeLaTeX](https://img.shields.io/badge/Engine-XeLaTeX-orange.svg)](#)
[![CTAN](https://img.shields.io/badge/CTAN-Ready-success.svg)](#)

[English](README_EN.md) | 简体中文

</div>

---

## Overview

This LaTeX template provides a complete solution for Jiangsu Ocean University undergraduate thesis, strictly following the *2026 Graduation Internship and Thesis Work Manual*. It includes **16 document templates** (thesis + 15 auxiliary forms) with **pixel-perfect alignment** to official Word templates.

### Key Features

- ✅ **Pixel-Perfect Alignment** — Extracted from Word XML (`w:tblGrid` → `w:gridCol`), column width error < 0.01cm
- ✅ **Complete Workflow** — Covers all stages: topic selection → internship → proposal → midterm → defense → grading
- ✅ **15 Auxiliary Forms** — Independent `.tex` files for all required forms
- ✅ **Automated Testing** — E2E tests verify 126 columns across 21 tables (4/4 PASS)
- ✅ **AI Presentation Generator** — Integrated [banana-slides](https://github.com/Anionex/banana-slides) for automatic PPT generation

---

## Preview

<div align="center">

### Thesis Cover Page
*Coming soon: Cover page screenshot*

### Form Templates
*Coming soon: Form templates gallery*

### Compilation Workflow
*Coming soon: Workflow diagram*

</div>

---

## Templates Overview

This template package includes **16 documents** covering the entire thesis workflow:

### Thesis Main Document

| Document | File |
|----------|------|
| Thesis Manuscript | `main.tex` |

### Form Templates (15)

<details>
<summary><b>Forms (7 templates)</b></summary>

| Template | File | Purpose |
|----------|------|---------|
| Topic Selection Form | `topic-selection.tex` | Topic proposal and approval |
| Internship Registration | `internship-registration.tex` | Internship registration |
| Task Book (Science) | `task-book-science.tex` | Task assignment (Sci/Eng/Med/Agr) |
| Task Book (Humanities) | `task-book-humanities.tex` | Task assignment (Hum/Econ/Mgmt) |
| Proposal Defense Record | `proposal-defense-record.tex` | Proposal defense minutes |
| Midterm Check Form | `midterm-check.tex` | Progress evaluation |
| Defense Record | `defense-record.tex` | Final defense minutes |

</details>

<details>
<summary><b>Reports (5 templates)</b></summary>

| Template | File | Purpose |
|----------|------|---------|
| Internship Diary | `internship-diary.tex` | Daily internship log |
| Internship Report | `internship-report.tex` | Internship summary report |
| Proposal Report (Science) | `proposal-science.tex` | Research proposal (Sci/Eng/Med/Agr) |
| Proposal Report (Humanities) | `proposal-humanities.tex` | Research proposal (Hum/Econ/Mgmt) |
| Translation | `translation.tex` | Foreign literature translation |

</details>

<details>
<summary><b>Evaluations (3 templates)</b></summary>

| Template | File | Purpose |
|----------|------|---------|
| Thesis Evaluation | `thesis-evaluation.tex` | Advisor/reviewer comments |
| Grading Form (Science) | `grading-science.tex` | Final grading (Sci/Eng/Med/Agr) |
| Grading Form (Humanities) | `grading-humanities.tex` | Final grading (Hum/Econ/Mgmt) |

</details>

---

## Quick Start

### Prerequisites

- **TeX Distribution**: TeX Live 2020+ or MikTeX 2.9+
- **Compiler**: XeLaTeX (required for Chinese support)
- **Fonts**: SimSun, SimHei, KaiTi_GB2312, FangSong_GB2312, Times New Roman

### Installation

#### macOS

```bash
brew install --cask mactex
```

#### Windows

Download and install [TeX Live](https://www.tug.org/texlive/) or [MikTeX](https://miktex.org/).

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# Or minimal installation
sudo apt-get install texlive-xetex texlive-lang-chinese
```

### Compilation

#### Compile Thesis

```bash
# Method 1: Using Makefile (recommended)
make

# Method 2: Manual compilation
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex

# Method 3: Using latexmk
latexmk -xelatex main.tex
```

#### Compile Individual Forms

```bash
cd templates/forms
xelatex topic-selection.tex
```

#### Batch Compile All Templates

```bash
for f in templates/{forms,reports,evaluations}/*.tex; do
  (cd "$(dirname "$f")" && xelatex "$(basename "$f")")
done
```

### Configuration

Edit metadata in `main.tex`:

```latex
\title{论文中文题目}
\entitle{English Title of the Thesis}
\author{学生姓名}
\studentid{学号}
\major{学院名称}
\class{专业班级}
\supervisor{指导教师（职称）}
```

---

## Advanced Features

### AI Presentation Generator (NEW!)

Automatically convert your thesis to professional PowerPoint presentations for proposal/midterm/defense using [banana-slides](https://github.com/Anionex/banana-slides).

```bash
cd slides/
make all  # Generate all three presentations
```

See [slides/README.md](slides/README.md) for details.

---

## Project Structure

```
JOU-Undergraduate-Thesis-LaTeX-Template/
├── main.tex                        # Thesis main file
├── Makefile                        # Build automation
├── LICENSE                         # LPPL 1.3c license
├── styles/
│   └── jouthesis.cls               # Document class (core formatting)
├── contents/
│   ├── chapters/                   # Thesis chapters
│   ├── appendices/                 # Appendices
│   └── acknowledgements.tex        # Acknowledgements
├── figures/                        # Images and logos
├── references/
│   └── refs.bib                    # BibTeX bibliography
├── templates/                      # 15 auxiliary form templates
│   ├── forms/                      # 7 form templates
│   ├── reports/                    # 5 report templates
│   └── evaluations/                # 3 evaluation templates
├── slides/                         # Paper-to-Slide toolkit
│   ├── extractors/                 # Content extraction scripts
│   ├── templates/                  # Markdown templates
│   └── Makefile                    # Automated workflow
└── tests/
    ├── test_pixel_perfect_alignment.py
    └── all_table_structures.json
```

---

## Format Specifications

### Page Layout

| Parameter | Specification |
|-----------|---------------|
| Paper Size | A4 (210mm × 297mm) |
| Margins | 2.5cm (top/bottom/left/right) |
| Line Spacing | 1.25 |
| Header | 5pt KaiTi_GB2312, "江苏海洋大学本科生毕业论文" |
| Footer | 5pt, centered page number |

### Typography

| Element | Font | Size |
|---------|------|------|
| Chapter Title | SimHei (Heiti) | 15pt (小三号) |
| Section Title | SimHei (Heiti) | 14pt (四号) |
| Subsection Title | SimHei (Heiti) | 12pt (小四号) |
| Body Text | SimSun (Songti) | 12pt (小四号) |
| English/Numbers | Times New Roman | 12pt |
| Figure/Table Caption | KaiTi_GB2312 | 10.5pt (五号) |

---

## Quality Assurance

### Automated Testing

Run E2E tests to verify pixel-perfect alignment:

```bash
python3 tests/test_pixel_perfect_alignment.py
```

**Test Coverage** (4/4 PASS):
- ✅ Table column widths (126 columns × 21 tables vs Word XML)
- ✅ Page layout consistency (A4 + 2.5cm margins)
- ✅ Template completeness (15 `.tex` + 15 `.pdf`)
- ✅ Font/size consistency

### Manual Verification

All template text (field names, headers, footers, checkboxes) has been manually verified against the official Word handbook for content consistency.

---

## Documentation

| Document | Description |
|----------|-------------|
| [USAGE.md](USAGE.md) | Detailed usage guide: chapters, figures, tables, equations, references |
| [TABLE-EXAMPLES.md](TABLE-EXAMPLES.md) | Table examples: three-line tables, merged cells, fixed-width columns |
| [ASSETS.md](ASSETS.md) | Image assets guide: logo usage and specifications |
| [templates/README.md](templates/README.md) | Form template documentation: purpose and filling instructions |
| [slides/README.md](slides/README.md) | Paper-to-Slide guide: automated PPT generation workflow |

---

## Troubleshooting

<details>
<summary><b>Font not found error</b></summary>

Ensure KaiTi_GB2312 and FangSong_GB2312 are installed. Windows includes them by default. macOS/Linux users need to install manually or configure via `fontconfig`.

</details>

<details>
<summary><b>Bibliography not showing</b></summary>

Run the compilation sequence 4 times: `xelatex` → `bibtex` → `xelatex` → `xelatex`, or use `make` / `latexmk -xelatex`.

</details>

<details>
<summary><b>Chinese text displays as gibberish</b></summary>

Must use `xelatex` compiler, not `pdflatex`.

</details>

<details>
<summary><b>Template cannot find images</b></summary>

When compiling from `templates/` subdirectory, logo path is `../../figures/jou-name-large.png` (relative path). Ensure you run `xelatex` from the correct directory.

</details>

---

## Contributing

Contributions are welcome! Please:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

---

## License

This work is licensed under the [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt).

**Current Maintainer**: [TsekaLuk](https://github.com/TsekaLuk)

This work consists of:
- Main thesis template: `main.tex`, `styles/jouthesis.cls`
- Auxiliary form templates: `templates/forms/*.tex`, `templates/reports/*.tex`, `templates/evaluations/*.tex`
- Paper-to-Slide toolkit: `slides/`

Modified versions must use a different name.

---

## Citation

If you use this template in your thesis, please consider citing:

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

- Official Word templates provided by Jiangsu Ocean University
- Inspired by [THU Thesis](https://github.com/tuna/thuthesis), [USTC Thesis](https://github.com/ustctug/ustcthesis)
- [banana-slides](https://github.com/Anionex/banana-slides) for AI presentation generation

---

<div align="center">

**⭐ If this template helps you, please give it a Star! ⭐**

*Strictly following official guidelines | Pixel-perfect alignment | E2E tested*

Made with ❤️ for JOU students

</div>

---

## Sources

- [Overleaf Thesis Templates](https://www.overleaf.com/latex/templates/tagged/thesis)
- [Overleaf Gallery](https://www.overleaf.com/gallery/tagged/thesis)
- [Overleaf LibGuides](https://overleaf.libguides.com/Thesis)
