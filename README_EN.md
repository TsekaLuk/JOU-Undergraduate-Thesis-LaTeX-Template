<div align="center">

<img src="figures/jou-logo-full.png" alt="Jiangsu Ocean University Logo" width="200"/>

# JOU Undergraduate Thesis LaTeX Template

**江苏海洋大学本科毕业论文 LaTeX 模板**

[![License: LPPL 1.3c](https://img.shields.io/badge/License-LPPL%201.3c-blue.svg)](https://www.latex-project.org/lppl.txt)
[![TeX Live](https://img.shields.io/badge/TeX%20Live-2020+-green.svg)](https://www.tug.org/texlive/)
[![XeLaTeX](https://img.shields.io/badge/Engine-XeLaTeX-orange.svg)](#)

English | [简体中文](README.md)

</div>

---

## Overview

This repository provides a reproducible LaTeX workflow for the Jiangsu Ocean University undergraduate thesis package defined by the *2026 Graduation Internship and Thesis Work Manual*.

The repository currently includes:

- `main.tex` for the thesis body
- 18 handbook templates for forms, reports, and grading sheets
- WPS-PDF-based end-to-end alignment checks
- A bundled open-source font stack for consistent builds on Linux, macOS, and Windows

The public repository does not redistribute commercial Foundertype or Microsoft fonts. Instead, it ships a default open-source font layer in `fonts/opensource/` and supports optional user-provided licensed overrides in `fonts/proprietary/`.

## Highlights

- `WPS baseline alignment`: page anchors, page count, orientation, and Word XML table grids are checked against the handbook export.
- `Cross-platform builds`: the default setup does not require preinstalled `KaiTi_GB2312`, `FangSong_GB2312`, or `Times New Roman`.
- `Complete template set`: thesis + 18 auxiliary templates.
- `Optional licensed mode`: users with valid local font licenses can override the default font stack for higher fidelity.
- `Executable QA`: layout expectations are written into E2E tests instead of being left as informal guidance.

## Quick Start

### Requirements

- TeX Live 2020+ or MikTeX 2.9+
- `xelatex`
- Python 3.9+
- `pdfinfo`, `pdftotext`, `pdffonts` from Poppler for the test suite

### Install TeX and Poppler

#### macOS

```bash
brew install --cask mactex
brew install poppler
```

#### Windows

- Install [TeX Live](https://www.tug.org/texlive/) or [MikTeX](https://miktex.org/)
- Install [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)

#### Linux

```bash
sudo apt-get install texlive-xetex texlive-lang-chinese poppler-utils
```

### Download bundled fonts

```bash
make fonts
```

This downloads the repository-managed open-source fonts into `fonts/opensource/`.

### Build the thesis

```bash
make
```

Or:

```bash
python3 scripts/download_fonts.py
latexmk -xelatex main.tex
```

### Build one handbook form

```bash
cd templates/forms
latexmk -xelatex topic-selection.tex
```

### Run the tests

```bash
make test
```

## Font strategy

### Default open-source mapping

| Handbook / Word font | Bundled fallback |
|------|------|
| Times New Roman | Tinos |
| Courier New | Courier Prime |
| SimSun / STSong-like serif Chinese | Noto Serif CJK SC |
| Hei / sans Chinese | Noto Sans CJK SC |
| KaiTi / KaiTi_GB2312 | LXGW WenKai GB |
| FangSong_GB2312 | FandolFang |
| FangZheng XiaoBiaoSong | Noto Serif CJK SC Black |
| Xingkai styles | LXGW WenKai GB Medium |

### Optional proprietary overrides

If you have a valid commercial font license, place the expected files under `fonts/proprietary/`. The template will automatically prefer them. See [fonts/README.md](fonts/README.md) for the exact filenames.

## Tests

### `tests/test_pixel_perfect_alignment.py`

Checks the handbook template contract:

- reference `docx/pdf` availability
- all 18 template `tex/pdf` artifacts
- Word XML table grid to LaTeX width mapping
- output PDF page count, orientation, and content anchors
- bundled font assets and embedded font stack

### `tests/test_thesis_alignment.py`

Checks the thesis template:

- cover, declaration, abstracts, TOC, body, references ordering
- heading style contract for TOC and body
- page-header anchors
- embedded fonts for OSS mode or licensed mode

## Repository layout

```text
JOU-Undergraduate-Thesis-LaTeX-Template/
├── main.tex
├── Makefile
├── contents/
├── docs/
├── figures/
├── fonts/
│   ├── opensource/
│   └── proprietary/
├── references/
├── scripts/
├── styles/
│   ├── joufonts.sty
│   ├── jouhandbook.sty
│   └── jouthesis.cls
├── templates/
└── tests/
```

## FAQ

### Missing font errors

Run `make fonts` first. The default mode should not require any system-installed commercial fonts.

### I want to use local Foundertype or Microsoft fonts

Place your licensed font files under `fonts/proprietary/` using the filenames documented in [fonts/README.md](fonts/README.md).

### Why not promise strict pixel-perfect equality everywhere?

The public, reproducible contract is currently based on the WPS render baseline plus layout, pagination, and font-embedding checks. True per-pixel overlay matching requires the same renderer and the same exact font files on both sides.

## Documentation

| File | Purpose |
|------|---------|
| [USAGE.md](USAGE.md) | Thesis usage guide |
| [TABLE-EXAMPLES.md](TABLE-EXAMPLES.md) | Table examples |
| [ASSETS.md](ASSETS.md) | Image asset notes |
| [templates/README.md](templates/README.md) | Auxiliary template overview |
| [fonts/README.md](fonts/README.md) | Font tiers and override rules |
| [slides/README.md](slides/README.md) | Slide generation workflow |

## License

The template code is distributed under [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt).

Bundled open-source fonts remain under their own licenses, with copies stored in `fonts/opensource/licenses/`.
