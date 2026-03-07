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

本项目依据《江苏海洋大学2026届毕业实习与设计（论文）工作手册》整理出一套可编译、可测试、可跨平台复现的 LaTeX 模板。

当前仓库包含：

- 1 份论文主模板 `main.tex`
- 18 份工作手册配套模板
- 1 套基于 WPS 导出 PDF 的 E2E 对齐测试
- 1 套内置开源字体方案，保证 Linux、macOS、Windows 一致编译
- 1 套三系统 CI 矩阵，持续校验 Windows / macOS / Linux 的论文构建与字体契约

项目的默认字体策略现在收敛为“学术规范四字体优先”：

- `楷体_GB2312`
- `宋体`
- `黑体`
- `Times New Roman`

仓库通过 `fonts/opensource/` 提供可再分发的开源兜底字体，并允许在 `fonts/proprietary/` 中放入用户自备、已获授权的标准字体文件。WPS 字体仍被支持，但只作为兼容兜底，不再作为默认优先路径。

## 核心特性

- `学术规范优先`：封面和正文优先命中 `楷体_GB2312 / 宋体 / 黑体 / Times New Roman`，更适合真实论文写作与交付。
- `手册基线校验`：以工作手册导出 PDF 为基线，校验分页锚点、表格网格、页面方向和产物页数。
- `跨平台一致编译`：默认使用仓库内置字体，不要求用户先手动安装 `楷体_GB2312`、`仿宋_GB2312` 或 `Times New Roman`。
- `模板全量覆盖`：论文正文之外，补齐了手册中的 18 份表单/报告/评分模板。
- `可选标准字体覆盖`：若本机已有合法字体授权，可把字体文件放入 `fonts/proprietary/`，模板会自动优先使用。
- `E2E 可执行标准`：源码契约、PDF 产物、论文专项检查都写进测试，不再靠人工口头确认。

## 预览

README 的展示面按“先看质感，再看完整度，再看覆盖面”来组织。所有预览图都可通过 `make readme-images` 重新生成。

### 论文封面：参考样页 vs 当前模板

![论文封面对比](docs/images/cover-compare.png)

### 论文主模板画廊

下面这张图展示当前模板的核心论文页面：封面、中文摘要、英文摘要、目录、正文首页、参考文献。

![论文模板画廊](docs/images/thesis-gallery.png)

### 关键版式细节：摘要与正文对比

README 不只放“成品图”，也保留关键页的横向对比，方便快速判断版式是否贴近手册。正文这里使用独立的 `body-sample.pdf` 与手册样页做一对一对比，避免拿真实论文内容去硬比手册说明页。
摘要对比图使用“标题 + 外框 + 摘要正文”的内容区裁剪，不把手册页底部的说明性注释一起放进 README 演示图。

![中文摘要对比](docs/images/abstract-compare.png)

![正文页对比](docs/images/body-compare.png)

### 配套表单画廊

下图展示 6 个代表性配套模板：选题审题表、任务书、开题报告（理工农医类）、中期检查表、评语表、答辩记录。

![表单模板画廊](docs/images/forms-gallery.png)

### 技术验证产物

用于排查残余字体或几何偏差的 overlay / diff / checker 产物保留在 `docs/assets/`，可通过 `make cover-diff` 重生成，不作为 README 首屏展示图。

- `docs/assets/thesis-cover-overlay-focus.png`
- `docs/assets/thesis-cover-diff-focus.png`
- `docs/assets/thesis-cover-checker-focus.png`

## 模板清单

### 论文正文

| 文档 | 文件 |
|------|------|
| 毕业设计（论文）说明书 | `main.tex` |

### 配套模板（18 个）

| 类别 | 数量 | 文件 |
|------|------|------|
| 表格类 | 10 | `preliminary-materials-cover.tex`、`topic-selection.tex`、`internship-registration.tex`、`task-book-science.tex`、`task-book-humanities.tex`、`proposal-defense-record.tex`、`midterm-check.tex`、`defense-record.tex`、`topic-summary.tex`、`handbook-statistics.tex` |
| 报告类 | 5 | `internship-diary.tex`、`internship-report.tex`、`proposal-science.tex`、`proposal-humanities.tex`、`translation.tex` |
| 评价类 | 3 | `thesis-evaluation.tex`、`grading-science.tex`、`grading-humanities.tex` |

更多说明见 [templates/README.md](templates/README.md)。

## 快速开始

### 环境要求

- TeX 发行版：TeX Live 2020+ 或 MikTeX 2.9+
- 编译器：`xelatex`
- 测试工具：`pdfinfo`、`pdftotext`、`pdffonts`（Poppler）
- Python：3.9+

### 安装 TeX 环境

#### macOS

```bash
brew install --cask mactex
brew install poppler
```

#### Windows

- 安装 [TeX Live](https://www.tug.org/texlive/) 或 [MikTeX](https://miktex.org/)
- 安装 [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)

#### Linux

```bash
# Ubuntu / Debian
sudo apt-get install texlive-xetex texlive-lang-chinese poppler-utils
```

### 下载仓库字体

```bash
make fonts
```

该命令会拉取仓库默认使用的开源字体到 `fonts/opensource/`。这是默认编译模式，不需要额外安装系统字体。

### 编译论文

```bash
make
```

或手动执行：

```bash
python3 scripts/download_fonts.py
latexmk -xelatex main.tex
```

### 编译单个表单

```bash
cd templates/forms
latexmk -xelatex topic-selection.tex
```

### 运行测试

```bash
make test
```

### 生成 README 预览图

```bash
make readme-images
```

等价于：

```bash
python3 tests/test_pixel_perfect_alignment.py
python3 tests/test_thesis_alignment.py
```

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

若客户机器使用了非标准安装路径，可使用 [styles/joufontspaths.local.example.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/joufontspaths.local.example.tex) 定义本地覆盖文件。

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

## 质量保证

### `tests/test_pixel_perfect_alignment.py`

校验工作手册模板的基线契约：

- 参考 `docx/pdf` 是否存在
- 18 个模板的 `tex/pdf` 是否完整
- LaTeX 表格列宽与 Word XML 表格网格是否一致
- 产物 PDF 的页数、方向、分页锚点是否匹配
- 字体资源和嵌入字体是否符合仓库约定

### `tests/test_thesis_alignment.py`

专项校验论文主模板：

- 封面、声明、摘要、目录、正文、参考文献等关键页顺序
- 目录和正文标题体例
- 页眉关键字与分页关系
- 嵌入字体是否符合当前字体模式

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

### 编译时报“字体未找到”

先执行 `make fonts`。默认模式不要求系统预装标准正式字体。

### 想用本机的方正或微软字体

把字体文件放入 `fonts/proprietary/`，文件名需与 [fonts/README.md](fonts/README.md) 中的约定一致。

### 为什么 README 不再直接承诺“绝对像素级一致”

当前仓库对齐标准已经写进 E2E，但公开可复现的是“WPS 渲染基线 + 版式/分页/字体契约”。如果你要进一步做逐像素叠图，需要在同一字体资源和同一渲染器环境下再增加图像 diff 流程。

## 文档

| 文件 | 内容 |
|------|------|
| [USAGE.md](USAGE.md) | 论文正文使用说明 |
| [TABLE-EXAMPLES.md](TABLE-EXAMPLES.md) | 表格示例 |
| [ASSETS.md](ASSETS.md) | 图片资源说明 |
| [templates/README.md](templates/README.md) | 配套模板说明 |
| [fonts/README.md](fonts/README.md) | 字体策略与覆盖方式 |
| [slides/README.md](slides/README.md) | 演示文稿生成说明 |

## 开源许可

项目代码采用 [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt)。

仓库中的开源字体分别遵循其各自许可证，许可证副本位于 `fonts/opensource/licenses/`。
