<div align="center">

# JOU-Undergraduate-Thesis-LaTeX-Template

**江苏海洋大学本科生毕业设计（论文）LaTeX 模板**

*Jiangsu Ocean University Undergraduate Thesis LaTeX Template*

[![License: LPPL 1.3c](https://img.shields.io/badge/License-LPPL%201.3c-blue.svg)](https://www.latex-project.org/lppl.txt)
[![TeX Live](https://img.shields.io/badge/TeX%20Live-2020+-green.svg)](https://www.tug.org/texlive/)
[![XeLaTeX](https://img.shields.io/badge/Engine-XeLaTeX-orange.svg)](#)
[![Templates](https://img.shields.io/badge/Templates-15%20Forms-purple.svg)](#-模板全景)
[![Tests](https://img.shields.io/badge/E2E%20Tests-4%2F4%20Passed-brightgreen.svg)](#-质量保证)
[![Paper2Slide](https://img.shields.io/badge/Paper2Slide-AI%20PPT-ff69b4.svg)](slides/README.md)

---

**严格依据《江苏海洋大学2026届毕业实习与设计（论文）工作手册》制作**

**像素级对齐 Word 官方模板 | 15 个配套表单 + 论文正文 | E2E 自动化验证 | AI 生成答辩 PPT**

</div>

---

## 亮点速览

```
                    Word XML 精确提取
                          |
      ┌───────────────────┼───────────────────┐
      v                   v                   v
  表格网格结构        页面布局参数         字体字号规范
  (28张表格)         (A4 + 2.5cm边距)     (宋体/黑体/楷体)
      |                   |                   |
      └───────────────────┼───────────────────┘
                          v
              15 个 LaTeX 模板 + 论文正文
                          |
                          v
              E2E TDD 自动化测试验证
              (126列 × 21张表格 全部通过)
```

- **像素级对齐** — 从 Word 文档 XML 中精确提取全部28张表格的网格结构（`w:tblGrid` → `w:gridCol`），列宽误差 < 0.01cm
- **全流程覆盖** — 选题 → 实习 → 任务书 → 开题 → 中期 → 翻译 → 答辩 → 评分，16 份文档一站齐备
- **独立编译** — 每个模板均为完整 `.tex` 文件，`xelatex` 一键生成 PDF
- **自动化验证** — E2E 测试自动对比 LaTeX 列宽与 Word XML 参数，4/4 测试通过
- **🎨 Paper2Slide** — 集成 banana-slides，一键将论文内容转为专业答辩PPT（开题/中期/答辩三种场景）

---

## 模板全景

<table>
<tr>
<td width="33%" valign="top">

### 表格类（7个）

| 模板 | 文件 |
|------|------|
| 选题审题表 | `topic-selection` |
| 实习登记表 | `internship-registration` |
| 任务书（理工） | `task-book-science` |
| 任务书（人文） | `task-book-humanities` |
| 开题答辩记录 | `proposal-defense-record` |
| 中期检查表 | `midterm-check` |
| 答辩记录 | `defense-record` |

</td>
<td width="33%" valign="top">

### 报告类（5个）

| 模板 | 文件 |
|------|------|
| 实习日记 | `internship-diary` |
| 实习报告书 | `internship-report` |
| 开题报告（理工） | `proposal-science` |
| 开题报告（人文） | `proposal-humanities` |
| 外文资料翻译 | `translation` |

</td>
<td width="34%" valign="top">

### 评价类（3个）

| 模板 | 文件 |
|------|------|
| 论文评语 | `thesis-evaluation` |
| 评分表（理工） | `grading-science` |
| 评分表（人文） | `grading-humanities` |

### 论文正文（1个）

| 模板 | 文件 |
|------|------|
| 毕业论文说明书 | `main.tex` |

</td>
</tr>
</table>

### 建议填写顺序

```
实习登记表 → 实习日记 → 实习报告书
    ↓
选题审题表 → 任务书
    ↓
开题报告 → 开题答辩记录
    ↓
外文资料翻译 → 中期检查表
    ↓
毕业论文说明书
    ↓
论文评语 → 答辩记录 → 评分表
```

---

## 快速开始

### 1. 安装 TeX 环境

<details>
<summary><b>macOS</b></summary>

```bash
# 安装 MacTeX（推荐完整版）
brew install --cask mactex

# 或 BasicTeX（轻量版，需手动补包）
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install ctex zhnumber xecjk enumitem makecell multirow
```

</details>

<details>
<summary><b>Windows</b></summary>

下载安装 [TeX Live](https://www.tug.org/texlive/) 完整版，已包含所需宏包和字体。

</details>

<details>
<summary><b>Linux</b></summary>

```bash
# Ubuntu / Debian
sudo apt-get install texlive-full
# 或最小安装
sudo apt-get install texlive-xetex texlive-lang-chinese
```

</details>

### 2. 编译论文正文

```bash
# 方式一：Makefile（推荐）
make

# 方式二：手动编译
xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex

# 方式三：latexmk
latexmk -xelatex main.tex
```

### 3. 编译配套模板

```bash
# 编译单个模板
cd templates/forms
xelatex topic-selection.tex

# 批量编译全部模板
for f in templates/forms/*.tex templates/reports/*.tex templates/evaluations/*.tex; do
  (cd "$(dirname "$f")" && xelatex "$(basename "$f")")
done
```

### 4. 填写论文信息

编辑 `main.tex` 头部：

```latex
\title{论文中文题目}
\entitle{English Title of the Thesis}
\author{学生姓名}
\studentid{学号}
\major{学院名称}
\class{专业班级}
\supervisor{指导教师（职称）}
```

### 5. 🎨 生成演示文稿（NEW!）

**一键将论文转为答辩PPT**，集成 [banana-slides](https://github.com/Anionex/banana-slides) 实现AI辅助生成：

```bash
cd slides/

# 生成全部三个PPT Markdown（开题、中期、答辩）
make all

# 或单独生成
make proposal  # 开题报告PPT
make midterm   # 中期汇报PPT
make defense   # 答辩PPT
```

**下一步**：访问 `http://localhost:3000` 上传生成的 `.md` 文件到 banana-slides，选择风格模板，生成专业 PPTX。

详见 [slides/README.md](slides/README.md)

---

## 项目结构

```
JOU-Undergraduate-Thesis-LaTeX-Template/
├── main.tex                        # 论文主文件（编译入口）
├── Makefile                        # 编译自动化
├── styles/
│   └── jouthesis.cls               # 论文样式类（核心格式定义）
├── contents/
│   ├── chapters/                   # 正文章节
│   │   ├── chapter1.tex            #   第1章
│   │   ├── chapter2.tex            #   第2章（含图表公式示例）
│   │   └── chapter3.tex            #   第3章
│   ├── appendices/
│   │   └── appendixA.tex           # 附录
│   └── acknowledgements.tex        # 致谢
├── figures/                        # 图片资源
│   ├── jou-logo-full.png           #   校徽（封面用, 1237×873px）
│   ├── jou-name-large.png          #   横版校名（表单用, 798×160px）
│   ├── jou-name-small.png          #   横版校名（小, 433×99px）
│   └── jou-name-large-rgba.png     #   透明背景版本
├── references/
│   └── refs.bib                    # 参考文献（BibTeX）
├── templates/                      # 配套模板集（15个）
│   ├── forms/                      #   表格类（7个）
│   ├── reports/                    #   报告类（5个）
│   └── evaluations/                #   评价类（3个）
├── slides/                         # 论文转PPT工具（NEW!）
│   ├── README.md                   #   Paper2Slide 使用指南
│   ├── Makefile                    #   自动化生成工作流
│   ├── extractors/                 #   LaTeX内容提取脚本
│   │   ├── tex2markdown.py         #     通用转换器
│   │   ├── extract_proposal.py     #     开题报告提取器
│   │   ├── extract_midterm.py      #     中期检查提取器
│   │   └── extract_defense.py      #     答辩PPT提取器
│   ├── templates/                  #   Markdown模板
│   │   ├── proposal_template.md    #     开题报告模板
│   │   ├── midterm_template.md     #     中期汇报模板
│   │   └── defense_template.md     #     答辩PPT模板
│   └── outputs/                    #   生成的Markdown和PPT
└── tests/
    ├── test_pixel_perfect_alignment.py   # E2E 像素级对齐测试
    └── all_table_structures.json         # Word XML 表格参考数据
```

---

## 格式规范

本模板严格按照《江苏海洋大学2026届毕业实习与设计（论文）工作手册》制作。

### 页面设置

| 参数 | 规格 |
|------|------|
| 纸张 | A4 (210mm × 297mm) |
| 页边距 | 上下左右均 2.5cm |
| 行距 | 1.25倍行距 |
| 页眉 | 五号楷体_GB2312，"江苏海洋大学本科生毕业论文" |
| 页脚 | 五号字，页码居中 |

### 字体字号

| 元素 | 字体 | 字号 |
|------|------|------|
| 一级标题 | 黑体 | 小三号，段前段后0.5行 |
| 二级标题 | 黑体 | 四号 |
| 三级标题 | 黑体 | 小四号 |
| 正文 | 宋体 | 小四号，首行缩进2字符 |
| 英文/数字 | Times New Roman | 同正文 |
| 图表标题 | 楷体_GB2312 | 五号 |
| 表单标题 | 黑体 | 三号 |
| 表单正文 | 宋体 | 小四号 |

### 必需字体

- 宋体 (SimSun)
- 黑体 (SimHei)
- 楷体_GB2312 (KaiTi_GB2312)
- 仿宋_GB2312 (FangSong_GB2312)
- Times New Roman

---

## 质量保证

### E2E 像素级对齐测试

```bash
cd JOU-Undergraduate-Thesis-LaTeX-Template
python3 tests/test_pixel_perfect_alignment.py
```

测试覆盖 4 个维度：

| 测试项 | 内容 | 状态 |
|--------|------|------|
| 表格列宽对齐 | 21张表格 × 126列，逐列对比 Word XML 参数 | PASS |
| 页面设置一致性 | A4纸 + 2.5cm边距 + `tabcolsep=0pt` | PASS |
| 模板完整性 | 15个 `.tex` + 15个 `.pdf` 全部存在 | PASS |
| 字体字号一致性 | 宋体 + 小四号表格 / 黑体 + 三号标题 | PASS |

### 内容一致性验证

所有模板的预设文本（字段名称、节标题、脚注说明、复选框选项）已与 Word 官方工作手册逐字核对，确保一致。

---

## 常见问题

<details>
<summary><b>编译报错"字体未找到"</b></summary>

确保系统已安装楷体_GB2312和仿宋_GB2312。Windows 一般自带，macOS/Linux 需手动安装或使用 `fontconfig` 配置。

</details>

<details>
<summary><b>参考文献不显示</b></summary>

按顺序运行 4 次编译：`xelatex` → `bibtex` → `xelatex` → `xelatex`，或使用 `make` / `latexmk -xelatex`。

</details>

<details>
<summary><b>中文显示乱码</b></summary>

必须使用 `xelatex` 编译，不要用 `pdflatex`。

</details>

<details>
<summary><b>模板编译找不到图片</b></summary>

在 `templates/` 子目录编译时，logo 路径为 `../../figures/jou-name-large.png`（相对路径）。请确保从正确目录运行 `xelatex`。

</details>

<details>
<summary><b>如何只使用部分模板？</b></summary>

每个模板都是独立的 `.tex` 文件，互不依赖。不需要的模板直接忽略即可。

</details>

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [USAGE.md](USAGE.md) | 详细使用指南：章节、图表、公式、参考文献 |
| [TABLE-EXAMPLES.md](TABLE-EXAMPLES.md) | 表格使用示例：三线表、跨行列、定宽列 |
| [ASSETS.md](ASSETS.md) | 图片资源说明：logo 使用与尺寸规范 |
| [templates/README.md](templates/README.md) | 模板详细说明：每个表单的用途与填写指引 |
| [slides/README.md](slides/README.md) | **Paper2Slide 指南**：论文转PPT自动化流程（NEW!）|

---

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建分支 `git checkout -b feature/your-feature`
3. 提交更改 `git commit -m 'feat: add your feature'`
4. 推送分支 `git push origin feature/your-feature`
5. 创建 Pull Request

---

## 许可证

本项目采用 [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt) 发布。修改后的版本须更改名称。

---

<div align="center">

**如果这个模板对你有帮助，请给个 Star 支持一下！**

*严格依据官方工作手册制作，像素级对齐 Word 模板*

</div>
