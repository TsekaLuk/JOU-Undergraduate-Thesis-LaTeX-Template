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
- A three-OS CI matrix that keeps Windows, macOS, and Linux thesis builds under regression checks

The font strategy is now standards-first for academic writing:

- `KaiTi_GB2312`
- `SimSun`
- `SimHei`
- `Times New Roman`

The public repository does not redistribute commercial Foundertype or Microsoft fonts. Instead, it ships an open-source fallback layer in `fonts/opensource/`, supports user-provided licensed overrides in `fonts/proprietary/`, and treats WPS fonts as a compatibility fallback rather than the default target.

## Distribution Channels

- `GitHub repository`: the canonical maintained version, including the full font strategy, E2E tests, packaging scripts, and issue tracking.
- `Overleaf Gallery`: a lightweight community edition for discovery and quick preview.

If you are starting real thesis writing or need the latest fixes, use the GitHub repository first rather than relying only on the gallery copy.

## Highlights

- `Academic standards first`: the thesis prioritizes `KaiTi_GB2312 / SimSun / SimHei / Times New Roman` for real submission workflows.
- `Handbook baseline checks`: page anchors, page count, orientation, and Word XML table grids are checked against the handbook export.
- `Cross-platform builds`: the default setup does not require preinstalled `KaiTi_GB2312`, `FangSong_GB2312`, or `Times New Roman`.
- `Complete template set`: thesis + 18 auxiliary templates.
- `Optional licensed mode`: users with valid local font licenses can override the default font stack for higher fidelity.
- `Executable QA`: layout expectations are written into E2E tests instead of being left as informal guidance.

## Preview

The preview section is organized as a product page: first visual quality, then thesis completeness, then handbook coverage. Regenerate everything with `make readme-images`.

### Thesis cover: reference vs current template

![Thesis cover comparison](docs/images/cover-compare.png)

### Thesis template gallery

This gallery shows the current thesis workflow pages: cover, Chinese abstract, English abstract, table of contents, body page, and references.

![Thesis template gallery](docs/images/thesis-gallery.png)

### Detail checks: abstract and body comparison

The main hero image is not enough on its own, so the README also keeps focused comparisons for the abstract and body pages. For the body sample, the comparison uses a dedicated `body-sample.pdf` artifact instead of a real thesis chapter page, so the right-hand side matches the handbook sample semantics.
The abstract comparison is cropped to the title, frame, and abstract content area so the handbook note block does not dilute the README demo.

![Chinese abstract comparison](docs/images/abstract-compare.png)

![Body page comparison](docs/images/body-compare.png)

### Representative handbook forms

The gallery below shows six representative templates: topic selection, task book, science proposal, midterm check, thesis evaluation, and defense record.

![Forms gallery](docs/images/forms-gallery.png)

### Technical comparison artifacts

Overlay, diff, and checkerboard assets stay in `docs/assets/` for debugging residual font or geometry drift. Regenerate them with `make cover-diff`.

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

### Generate README preview images

```bash
make readme-images
```

## Font strategy

### Font priority

1. Local licensed standard fonts under `fonts/proprietary/`
2. System-standard academic fonts on Windows/macOS/Linux
3. WPS compatibility fonts
4. Bundled open-source fallback fonts

### Open-source fallback mapping

| Standard academic font | Bundled fallback |
|------|------|
| Times New Roman | Tinos |
| Courier New | Courier Prime |
| SimSun / STSong | Noto Serif CJK SC |
| SimHei / STHeiti | Noto Sans CJK SC |
| KaiTi / KaiTi_GB2312 / STKaiti | LXGW WenKai GB |
| FangSong / FangSong_GB2312 / STFangsong | FandolFang |
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

Run `make fonts` first. The default mode should not require any system-installed licensed standard fonts.

On Windows, the project now probes:
- `C:/Windows/Fonts`
- common `WPS Office/office6/fonts` install locations
- WPS font folders under `LOCALAPPDATA`

If the client machine uses a non-standard install path, use [styles/joufontspaths.local.example.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/joufontspaths.local.example.tex) as the local override template.

### I want to use local Foundertype or Microsoft fonts

Place your licensed font files under `fonts/proprietary/` using the filenames documented in [fonts/README.md](fonts/README.md).

### Why not promise strict pixel-perfect equality everywhere?

The public, reproducible contract is currently based on the WPS render baseline plus layout, pagination, and font-embedding checks. True per-pixel overlay matching requires the same renderer and the same exact font files on both sides.

## Documentation

| File | Purpose |
|------|---------|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/guides/usage.md](docs/guides/usage.md) | Thesis usage guide |
| [docs/guides/table-examples.md](docs/guides/table-examples.md) | Table examples |
| [docs/guides/assets.md](docs/guides/assets.md) | Image asset notes |
| [templates/README.md](templates/README.md) | Auxiliary template overview |
| [fonts/README.md](fonts/README.md) | Font tiers and override rules |
| [slides/README.md](slides/README.md) | Slide generation workflow |

## License

The template code is distributed under [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt).

Bundled open-source fonts remain under their own licenses, with copies stored in `fonts/opensource/licenses/`.
