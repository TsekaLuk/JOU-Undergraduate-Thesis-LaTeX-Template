<div align="center">

<img src="figures/jou-logo-full.png" alt="江苏海洋大学校徽" width="200"/>

# 江苏海洋大学本科毕业论文 LaTeX 模板

**JOU Undergraduate Thesis LaTeX Template**

*Jiangsu Ocean University Undergraduate Thesis LaTeX Template*

[![License: LPPL 1.3c](https://img.shields.io/badge/License-LPPL%201.3c-blue.svg)](https://www.latex-project.org/lppl.txt)
[![TeX Live](https://img.shields.io/badge/TeX%20Live-2020+-green.svg)](https://www.tug.org/texlive/)
[![XeLaTeX](https://img.shields.io/badge/Engine-XeLaTeX-orange.svg)](#)
[![CTAN](https://img.shields.io/badge/CTAN-Ready-success.svg)](#)

简体中文 | [English](README_EN.md)

</div>

---

## 项目简介

本 LaTeX 模板为江苏海洋大学本科生毕业设计（论文）提供完整解决方案，严格依据《江苏海洋大学2026届毕业实习与设计（论文）工作手册》制作。包含**论文正文 + 15 个配套表单**共 16 份文档，实现与官方 Word 模板的**像素级对齐**。

### 核心特性

- ✅ **像素级对齐** — 从 Word XML 精确提取表格网格结构（`w:tblGrid` → `w:gridCol`），列宽误差 < 0.01cm
- ✅ **全流程覆盖** — 涵盖选题 → 实习 → 任务书 → 开题 → 中期 → 翻译 → 答辩 → 评分全部环节
- ✅ **15 个配套表单** — 每个表单均为独立 `.tex` 文件，可单独编译
- ✅ **自动化测试** — E2E 测试验证 21 张表格的 126 列宽度（4/4 测试通过）
- ✅ **AI 生成 PPT** — 集成 [banana-slides](https://github.com/Anionex/banana-slides)，一键生成开题/中期/答辩演示文稿

---

## 效果预览

<div align="center">

### 论文封面
*即将添加：封面截图*

### 表单模板
*即将添加：表单示例图集*

### 编译流程
*即将添加：流程示意图*

</div>

---

## 模板清单

本模板包含 **16 份文档**，覆盖毕业论文全流程：

### 论文正文

| 文档 | 文件 |
|------|------|
| 毕业论文说明书 | `main.tex` |

### 配套表单（15 个）

<details>
<summary><b>表格类（7 个）</b></summary>

| 模板 | 文件 | 用途 |
|------|------|------|
| 选题、审题表 | `topic-selection.tex` | 选题申报与审核 |
| 实习登记表 | `internship-registration.tex` | 实习前登记 |
| 任务书（理工农医类） | `task-book-science.tex` | 任务分配（理工农医） |
| 任务书（人文经管类） | `task-book-humanities.tex` | 任务分配（人文经管） |
| 开题答辩记录 | `proposal-defense-record.tex` | 开题答辩记录 |
| 中期检查表 | `midterm-check.tex` | 进度检查评价 |
| 答辩记录 | `defense-record.tex` | 答辩过程记录 |

</details>

<details>
<summary><b>报告类（5 个）</b></summary>

| 模板 | 文件 | 用途 |
|------|------|------|
| 实习日记 | `internship-diary.tex` | 每日实习记录 |
| 实习报告书 | `internship-report.tex` | 实习总结报告 |
| 开题报告（理工农医类） | `proposal-science.tex` | 研究方案（理工农医） |
| 开题报告（人文经管类） | `proposal-humanities.tex` | 研究方案（人文经管） |
| 外文资料翻译 | `translation.tex` | 外文文献翻译 |

</details>

<details>
<summary><b>评价类（3 个）</b></summary>

| 模板 | 文件 | 用途 |
|------|------|------|
| 论文评语 | `thesis-evaluation.tex` | 指导/评阅/答辩评语 |
| 评分表（理工农医类） | `grading-science.tex` | 综合评分（理工农医） |
| 评分表（人文经管类） | `grading-humanities.tex` | 综合评分（人文经管） |

</details>

---

## 快速开始

### 环境要求

- **TeX 发行版**：TeX Live 2020+ 或 MikTeX 2.9+
- **编译器**：XeLaTeX（中文支持必需）
- **字体**：宋体、黑体、楷体_GB2312、仿宋_GB2312、Times New Roman

### 安装 TeX 环境

#### macOS

```bash
brew install --cask mactex
```

#### Windows

下载安装 [TeX Live](https://www.tug.org/texlive/) 或 [MikTeX](https://miktex.org/)

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# 或最小安装
sudo apt-get install texlive-xetex texlive-lang-chinese
```

### 编译论文

#### 编译论文正文

```bash
# 方法 1：使用 Makefile（推荐）
make

# 方法 2：手动编译
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex

# 方法 3：使用 latexmk
latexmk -xelatex main.tex
```

#### 编译单个表单

```bash
cd templates/forms
xelatex topic-selection.tex
```

#### 批量编译所有模板

```bash
for f in templates/{forms,reports,evaluations}/*.tex; do
  (cd "$(dirname "$f")" && xelatex "$(basename "$f")")
done
```

### 填写论文信息

编辑 `main.tex` 头部元数据：

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

## 高级功能

### AI 生成演示文稿（NEW!）

使用 [banana-slides](https://github.com/Anionex/banana-slides) 自动将论文转换为专业 PPT：

```bash
cd slides/
make all  # 生成全部三个 PPT（开题/中期/答辩）
```

详见 [slides/README.md](slides/README.md)

---

## 项目结构

```
JOU-Undergraduate-Thesis-LaTeX-Template/
├── main.tex                        # 论文主文件
├── Makefile                        # 编译自动化
├── LICENSE                         # LPPL 1.3c 许可证
├── styles/
│   └── jouthesis.cls               # 文档类（核心格式定义）
├── contents/
│   ├── chapters/                   # 论文章节
│   ├── appendices/                 # 附录
│   └── acknowledgements.tex        # 致谢
├── figures/                        # 图片和 Logo
├── references/
│   └── refs.bib                    # BibTeX 参考文献
├── templates/                      # 15 个配套表单
│   ├── forms/                      # 7 个表格类模板
│   ├── reports/                    # 5 个报告类模板
│   └── evaluations/                # 3 个评价类模板
├── slides/                         # 论文转 PPT 工具
│   ├── extractors/                 # 内容提取脚本
│   ├── templates/                  # Markdown 模板
│   └── Makefile                    # 自动化工作流
└── tests/
    ├── test_pixel_perfect_alignment.py
    └── all_table_structures.json
```

---

## 格式规范

### 页面设置

| 参数 | 规格 |
|------|------|
| 纸张大小 | A4 (210mm × 297mm) |
| 页边距 | 上下左右均 2.5cm |
| 行距 | 1.25 倍行距 |
| 页眉 | 五号楷体_GB2312，"江苏海洋大学本科生毕业论文" |
| 页脚 | 五号字，页码居中 |

### 字体字号

| 元素 | 字体 | 字号 |
|------|------|------|
| 一级标题 | 黑体 | 小三号（15pt），段前段后 0.5 行 |
| 二级标题 | 黑体 | 四号（14pt） |
| 三级标题 | 黑体 | 小四号（12pt） |
| 正文 | 宋体 | 小四号（12pt），首行缩进 2 字符 |
| 英文/数字 | Times New Roman | 12pt |
| 图表标题 | 楷体_GB2312 | 五号（10.5pt） |

---

## 质量保证

### 自动化测试

运行 E2E 测试验证像素级对齐：

```bash
python3 tests/test_pixel_perfect_alignment.py
```

**测试覆盖**（4/4 通过）：
- ✅ 表格列宽对齐（126 列 × 21 张表格 vs Word XML）
- ✅ 页面布局一致性（A4 + 2.5cm 边距）
- ✅ 模板完整性（15 个 `.tex` + 15 个 `.pdf`）
- ✅ 字体字号一致性

### 人工验证

所有模板文本（字段名称、表头、页脚、复选框选项）已与官方 Word 工作手册逐字核对，确保内容一致性。

---

## 使用文档

| 文档 | 内容 |
|------|------|
| [USAGE.md](USAGE.md) | 详细使用指南：章节、图表、公式、参考文献 |
| [TABLE-EXAMPLES.md](TABLE-EXAMPLES.md) | 表格示例：三线表、跨行列、定宽列 |
| [ASSETS.md](ASSETS.md) | 图片资源说明：Logo 使用与规范 |
| [templates/README.md](templates/README.md) | 表单文档：每个模板的用途与填写说明 |
| [slides/README.md](slides/README.md) | Paper2Slide 指南：自动化 PPT 生成流程 |

---

## 常见问题

<details>
<summary><b>编译报错"字体未找到"</b></summary>

确保系统已安装楷体_GB2312 和仿宋_GB2312。Windows 一般自带，macOS/Linux 需手动安装或通过 `fontconfig` 配置。

</details>

<details>
<summary><b>参考文献不显示</b></summary>

按顺序运行 4 次编译：`xelatex` → `bibtex` → `xelatex` → `xelatex`，或使用 `make` / `latexmk -xelatex`。

</details>

<details>
<summary><b>中文显示乱码</b></summary>

必须使用 `xelatex` 编译器，不要用 `pdflatex`。

</details>

<details>
<summary><b>模板找不到图片</b></summary>

在 `templates/` 子目录编译时，Logo 路径为 `../../figures/jou-name-large.png`（相对路径）。确保从正确目录运行 `xelatex`。

</details>

---

## 参与贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/your-feature`）
3. 提交更改（`git commit -m 'feat: add your feature'`）
4. 推送到分支（`git push origin feature/your-feature`）
5. 创建 Pull Request

---

## 开源许可

本项目采用 [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt) 发布。

**当前维护者**：[TsekaLuk](https://github.com/TsekaLuk)

本项目包含：
- 论文主模板：`main.tex`、`styles/jouthesis.cls`
- 配套表单模板：`templates/forms/*.tex`、`templates/reports/*.tex`、`templates/evaluations/*.tex`
- 论文转 PPT 工具：`slides/`

修改后的版本须使用不同名称。

---

## 引用格式

如果本模板对您的论文有帮助，可以引用：

```bibtex
@software{jou_thesis_template,
  author = {TsekaLuk},
  title = {江苏海洋大学本科毕业论文 LaTeX 模板},
  year = {2026},
  url = {https://github.com/TsekaLuk/JOU-Undergraduate-Thesis-LaTeX-Template},
  version = {1.0}
}
```

---

## 致谢

- 江苏海洋大学教务处提供官方 Word 模板
- 参考了 [THU Thesis](https://github.com/tuna/thuthesis)、[USTC Thesis](https://github.com/ustctug/ustcthesis) 等优秀模板
- [banana-slides](https://github.com/Anionex/banana-slides) 提供 AI 演示文稿生成支持

---

<div align="center">

**⭐ 如果这个模板对你有帮助，请给个 Star 支持一下！⭐**

*严格依据官方工作手册 | 像素级对齐 | E2E 测试验证*

用 ❤️ 为江苏海洋大学学生制作

</div>
