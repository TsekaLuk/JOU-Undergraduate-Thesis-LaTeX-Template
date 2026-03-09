<div align="center">

<img src="figures/jou-logo-full.png" alt="江苏海洋大学校徽" width="200"/>

# 江苏海洋大学本科毕业论文 LaTeX 模板

**JOU Undergraduate Thesis LaTeX Template**

*Jiangsu Ocean University Undergraduate Thesis LaTeX Template*

[![License: LPPL 1.3c](https://img.shields.io/badge/License-LPPL%201.3c-blue.svg)](https://www.latex-project.org/lppl.txt)
[![TeX Live](https://img.shields.io/badge/TeX%20Live-2020+-green.svg)](https://www.tug.org/texlive/)
[![XeLaTeX](https://img.shields.io/badge/Engine-XeLaTeX-orange.svg)](#)

简体中文 | [English](README_EN.md)

</div>

---

## 项目简介

本项目依据《江苏海洋大学2026届毕业实习与设计（论文）工作手册》整理出一套开箱即用的 LaTeX 论文模板，适合本地写作、配合 AI 工具使用。

当前仓库包含：

- 1 份论文主模板 `main.tex`
- 18 份工作手册配套模板
- 1 份校级优秀毕业实习与设计（论文）摘要模板
- 1 套内置开源字体，Linux、macOS、Windows 无需手动安装字体即可编译

模板已内置开源兜底字体，开箱即可编译。若本机已有宋体、黑体、楷体_GB2312、Times New Roman 等标准字体，模板会自动优先使用，适合正式提交。

## 发布渠道

- `GitHub 仓库`：完整版本，包含完整字体策略、最新修复、issue 跟踪，以此为准。
- `Overleaf Gallery`：轻量预览版，字体受限，不包含完整资源，不适合正式提交。

**建议克隆 GitHub 仓库**进行写作，不要只使用 Overleaf Gallery 版本。

## 核心特性

- `学术规范优先`：封面和正文优先使用楷体_GB2312 / 宋体 / 黑体 / Times New Roman，满足正式提交要求。
- `开箱即用`：内置开源兜底字体，无需额外安装系统字体，克隆后即可编译。
- `跨平台一致`：Windows、macOS、Linux 均可正常编译，输出结果一致。
- `模板全量覆盖`：除论文正文外，还包含手册中的 18 份表单/报告/评分模板。
- `自动字体适配`：若本机已有标准字体，模板自动优先使用；最终提交时可通过 `strictfonts` 选项强制校验。
- `版式对齐手册`：封面、摘要、目录、正文版式均依据工作手册规范实现，并通过 CI 持续验证。

## 预览

### 论文封面：参考样页 vs 当前模板

![论文封面对比](docs/images/cover-compare.png)

### 论文主模板画廊

下面这张图展示当前模板的核心论文页面：封面、中文摘要、英文摘要、目录、正文首页、参考文献。

![论文模板画廊](docs/images/thesis-gallery.png)

### 校优摘要专项模板

这套模板按《江苏海洋大学本科校级优秀毕业实习与设计（论文）摘要格式说明》的结构单独组织：首页保留题名、作者、指导教师与中文摘要全宽区块，正文与参考文献切换到双栏，英文标题与英文摘要在文末回到整页全宽。

![校优摘要模板预览](docs/images/excellent-abstract-gallery.png)

逐条对照见 [docs/reports/excellent-thesis-abstract-compliance.md](docs/reports/excellent-thesis-abstract-compliance.md)。

### 关键版式细节：摘要与正文对比

以下对比图展示摘要页与正文页和手册样页的排版对齐情况。

![中文摘要对比](docs/images/abstract-compare.png)

![正文页对比](docs/images/body-compare.png)

### 配套表单画廊

下图展示 6 个代表性配套模板：选题审题表、任务书、开题报告（理工农医类）、中期检查表、评语表、答辩记录。

![表单模板画廊](docs/images/forms-gallery.png)

## 模板清单

### 论文正文

| 文档 | 文件 |
|------|------|
| 毕业设计（论文）说明书 | `main.tex` |

### 配套模板

#### 工作手册模板（18 个）

| 类别 | 数量 | 文件 |
|------|------|------|
| 表格类 | 10 | `preliminary-materials-cover.tex`、`topic-selection.tex`、`internship-registration.tex`、`task-book-science.tex`、`task-book-humanities.tex`、`proposal-defense-record.tex`、`midterm-check.tex`、`defense-record.tex`、`topic-summary.tex`、`handbook-statistics.tex` |
| 报告类 | 5 | `internship-diary.tex`、`internship-report.tex`、`proposal-science.tex`、`proposal-humanities.tex`、`translation.tex` |
| 评价类 | 3 | `thesis-evaluation.tex`、`grading-science.tex`、`grading-humanities.tex` |

#### 专项申报模板（1 个）

| 文档 | 文件 |
|------|------|
| 校级优秀毕业实习与设计（论文）摘要 | `templates/reports/excellent-thesis-abstract.tex` |

更多说明见 [templates/README.md](templates/README.md)。

## 快速开始

### 本地编译（推荐）

本地编译可使用完整字体库，满足学校正式提交要求，并可配合 AI 工具辅助写作。

**环境要求：** TeX Live 2020+（推荐）或 MikTeX 2.9+，含 `xelatex`。运行自动化测试时还需要 Python 3.9+ 和 Poppler，普通写作用不到。

#### 安装 TeX 环境

**macOS**

```bash
brew install --cask mactex
```

**Windows**

安装 [TeX Live](https://www.tug.org/texlive/) 或 [MikTeX](https://miktex.org/)（二选一）。

**Linux**

```bash
# Ubuntu / Debian
sudo apt-get install texlive-xetex texlive-lang-chinese
```

#### 下载仓库字体

```bash
make fonts
```

该命令会拉取仓库默认使用的开源字体到 `fonts/opensource/`。这是默认编译模式，不需要额外安装系统字体。

#### 编译论文

```bash
make
```

或手动执行：

```bash
python3 scripts/download_fonts.py
latexmk -xelatex main.tex
```

#### 编译单个表单

```bash
cd templates/forms
latexmk -xelatex topic-selection.tex
```

### AI 工具辅助写作

本模板的 `.tex` 源文件结构清晰，非常适合配合 AI 编辑工具使用：

| 工具 | 使用方式 |
|------|----------|
| **Cursor / Trae** | 在 AI 原生编辑器中打开仓库，直接对话修改 `.tex` 文件 |
| **Claude Code** | 命令行 AI，适合批量修改内容、调整排版 |
| **Codex / OpenClaw / Antigravity** | 其他 AI 编程工具，均可直接编辑 `.tex` 源文件 |

> 推荐做法：用 AI 工具辅助填写内容与调整结构，用 `latexmk` 或 `make` 在本地编译预览。

### Overleaf（辅助预览，有限制）

Overleaf 可用于快速预览，但存在以下限制，**不建议用于最终提交版本**：

- 必须使用专用 Overleaf 发布包（Releases 页面的 `jouthesis-overleaf-*.zip`），与完整仓库版本不同
- **无法使用标准学术字体**（楷体_GB2312、宋体、黑体、Times New Roman），只能使用开源替代字体，字形略有差异
- 免费版每次编译有时间限制（约 20 秒）

## 字体策略

**毕业论文优先使用标准学术字体**，模板自动按以下优先级加载：

### 字体加载优先级

1. **📁 本地标准字体** (`fonts/proprietary/`)
   - 手动放入的正式字体文件
   - 最适合最终提交与本机高保真交付

2. **💻 系统标准学术字体**
   - Windows: 直接探测 `C:/Windows/Fonts` 中的 `times/simsun/simhei/simkai/simfang`
   - macOS: 优先探测系统 `STSong/STHeiti/STKaiti/STFangsong`
   - Linux: 优先探测系统已安装的 `Times New Roman / SimSun / SimHei / KaiTi / FangSong`

3. **🧩 WPS 兼容字体**
   - 仅在标准学术字体不完整时使用
   - 包括 WPS 安装目录和系统中的 `HY... / FZ...` 字体

4. **🆓 开源字体兜底** (`fonts/opensource/`)
   - 仅在前三者都不可用时使用
   - Tinos, Noto CJK, LXGW WenKai, FandolFang

### 检查字体状态

```bash
python3 scripts/check_fonts.py
```

该脚本会自动检测你的系统字体配置，并给出改进建议。

对 Windows 用户，脚本会额外检查：
- `C:/Windows/Fonts`
- `Program Files` / `Program Files (x86)` 下的 WPS 安装目录
- `LOCALAPPDATA` 下的 WPS 字体目录

若字体安装路径非标准位置，可参考 [styles/joufontspaths.local.example.tex](styles/joufontspaths.local.example.tex) 定义本地覆盖文件。

### 编译输出示例

**有标准学术字体时**（最佳）：
```
===============================================
Font Mode: system-licensed
Status: Using system academic standard fonts (Excellent)
===============================================
```

**无标准字体时**（开源字体 fallback）：
```
===============================================
Font Mode: oss
Status: Using open source academic fallback fonts (Preview)
===============================================

TIP: For best academic output, prefer KaiTi_GB2312,
     SimSun, SimHei, and Times New Roman.
     Check: python3 scripts/check_fonts.py
```

模板会**自动选择最佳可用字体**，开源字体完全可用于日常预览和开发。

**最终提交检查**（可选）:

如需确保使用标准正式字体，可启用严格模式：

```latex
\documentclass[strictfonts]{jouthesis}  % 最终提交前检查
```

### 字体映射表

| 学术标准字体 | 优先使用 | 开源兜底 |
|------|------|------|
| Times New Roman | 系统 / 本地 Times New Roman | Tinos |
| Courier New | 系统 / 本地 Courier New | Courier Prime |
| 宋体 | SimSun / STSong | Noto Serif CJK SC |
| 黑体 | SimHei / STHeiti | Noto Sans CJK SC |
| 楷体 / 楷体_GB2312 | KaiTi_GB2312 / KaiTi / STKaiti | LXGW WenKai GB |
| 仿宋 / 仿宋_GB2312 | FangSong / STFangsong | FandolFang |
| 方正小标宋简体 | FZXiaoBiaoSong-B05 | Noto Serif CJK SC Black |
| 华文行楷 | STXingkai | LXGW WenKai GB Medium |

注意：仓库不会分发商业字体文件。完整说明见 [fonts/README.md](fonts/README.md)。

## 项目结构

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

## 常见问题

### 如何填写姓名、学号、题目等个人信息？

编辑 `contents/shared/metadata.tex`，按注释提示填写即可。

### 如何添加新章节？

在 `contents/chapters/` 下新建 `chapterN.tex`，然后在 `main.tex` 中添加一行 `\include{contents/chapters/chapterN}`。

### 如何添加参考文献？

将文献条目写入 `references/refs.bib`，正文中用 `\cite{key}` 引用，编译时会自动生成参考文献列表。

### 编译时报”字体未找到”

先执行 `make fonts`（或 `python3 scripts/download_fonts.py`）。默认模式会自动下载开源兜底字体，不要求系统预装标准正式字体。

### 最终提交时需要标准字体吗？

学校通常要求使用标准字体（宋体、黑体、楷体_GB2312、Times New Roman）。若你的电脑上已有这些字体，模板会自动优先使用。若没有，编译结果仍使用开源替代字体，外观接近但有细微差别。如需强制检查，可在 `\documentclass` 选项中加 `strictfonts`：

```latex
\documentclass[strictfonts]{styles/jouthesis}
```

### 想用本机的方正或微软字体

把字体文件放入 `fonts/proprietary/`，文件名需与 [fonts/README.md](fonts/README.md) 中的约定一致。

### 目录没有出现某个章节

检查对应 `.tex` 文件是否已在 `main.tex` 中用 `\include` 引入，且章节命令使用的是 `\chapter{...}` 或 `\section{...}`。

### 编译后看不到参考文献

确保 `references/refs.bib` 中有对应条目，且正文中使用了 `\cite{...}`，然后重新完整编译（`latexmk -xelatex main.tex` 会自动处理多遍编译）。

### 附录怎么用？

在 `main.tex` 的 `\appendix` 之后 `\include{contents/appendices/appendixA}`，在附录文件中照常用 `\chapter{...}` 写内容即可。

## 文档

| 文件 | 内容 |
|------|------|
| [docs/README.md](docs/README.md) | 文档索引 |
| [docs/guides/usage.md](docs/guides/usage.md) | 论文正文使用说明 |
| [docs/guides/table-examples.md](docs/guides/table-examples.md) | 表格示例 |
| [docs/guides/assets.md](docs/guides/assets.md) | 图片资源说明 |
| [templates/README.md](templates/README.md) | 配套模板说明 |
| [fonts/README.md](fonts/README.md) | 字体策略与覆盖方式 |
| [slides/README.md](slides/README.md) | 演示文稿生成说明 |

## 开源许可

项目代码采用 [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt)。

仓库中的开源字体分别遵循其各自许可证，许可证副本位于 `fonts/opensource/licenses/`。
