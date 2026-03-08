# 江苏海洋大学工作手册模板说明

本目录收录工作手册中的 18 份配套模板，按 `表格类 / 报告类 / 评价类` 分类组织。所有模板均可独立编译，并统一通过 [styles/jouhandbook.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouhandbook.sty) 与 [styles/joufonts.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/joufonts.sty) 共享版式和字体策略。

## 目录结构

```text
templates/
├── forms/
│   ├── preliminary-materials-cover.tex
│   ├── topic-selection.tex
│   ├── internship-registration.tex
│   ├── task-book-science.tex
│   ├── task-book-humanities.tex
│   ├── proposal-defense-record.tex
│   ├── midterm-check.tex
│   ├── defense-record.tex
│   ├── topic-summary.tex
│   └── handbook-statistics.tex
├── reports/
│   ├── internship-diary.tex
│   ├── internship-report.tex
│   ├── proposal-science.tex
│   ├── proposal-humanities.tex
│   ├── excellent-thesis-abstract.tex
│   └── translation.tex
└── evaluations/
    ├── thesis-evaluation.tex
    ├── grading-science.tex
    └── grading-humanities.tex
```

## 模板清单

### 表格类

- `preliminary-materials-cover.tex`：前期工作材料封面
- `topic-selection.tex`：毕业设计（论文）选题、审题表
- `internship-registration.tex`：毕业实习登记表
- `task-book-science.tex`：任务书（理工农医类）
- `task-book-humanities.tex`：任务书（人文经管类）
- `proposal-defense-record.tex`：开题答辩记录
- `midterm-check.tex`：中期检查表
- `defense-record.tex`：答辩记录
- `topic-summary.tex`：选题情况汇总表
- `handbook-statistics.tex`：本科毕业实习与设计（论文）情况统计表

### 报告类

- `internship-diary.tex`：毕业实习日记
- `internship-report.tex`：毕业实习报告书
- `proposal-science.tex`：开题报告（理工农医类）
- `proposal-humanities.tex`：开题报告（人文经管类）
- `excellent-thesis-abstract.tex`：校级优秀毕业实习与设计（论文）摘要
- `translation.tex`：外文资料翻译

### 评价类

- `thesis-evaluation.tex`：毕业设计（论文）评语
- `grading-science.tex`：评分表（理工农医类）
- `grading-humanities.tex`：评分表（人文经管类）

## 编译方式

### 单个模板

```bash
cd templates/forms
latexmk -xelatex topic-selection.tex
```

`reports/` 和 `evaluations/` 目录中的模板用法相同。

校优摘要模板需要参考文献流程，建议在 `templates/reports/` 目录执行：

```bash
latexmk -xelatex -bibtex excellent-thesis-abstract.tex
```

该模板按 `references/江苏海洋大学本科校级优秀毕业实习与设计（论文）摘要格式说明.doc` 独立实现，同时复用 `contents/shared/metadata.tex` 中的题名、作者、学院、专业和导师元数据。该入口默认启用严格字体检查，缺少正式申报所需字体会直接停止编译。逐条对照见 [docs/reports/excellent-thesis-abstract-compliance.md](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/docs/reports/excellent-thesis-abstract-compliance.md)。

### 批量编译

在仓库根目录执行：

```bash
for f in templates/{forms,reports,evaluations}/*.tex; do
  (cd "$(dirname "$f")" && latexmk -xelatex "$(basename "$f")")
done
```

## 字体与跨平台策略

模板默认不依赖系统商业字体，而是通过仓库自带的开源字体保证一致编译：

- 西文衬线：`Tinos`
- 西文等宽：`Courier Prime`
- 中文正文：`Noto Serif CJK SC`
- 中文黑体：`Noto Sans CJK SC`
- 中文楷体：`LXGW WenKai GB`
- 中文仿宋：`FandolFang`

如果本机已有合法的方正或微软字体授权，可将对应字体文件放入 [fonts/proprietary/](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/fonts/proprietary/) 以覆盖默认映射。具体文件名见 [fonts/README.md](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/fonts/README.md)。

## 与测试的关系

这些模板受 [tests/test_pixel_perfect_alignment.py](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/tests/test_pixel_perfect_alignment.py) 约束。当前 E2E 会检查：

- 18 个工作手册模板的 `tex/pdf` 是否完整
- LaTeX 表格列宽是否对应 Word XML 表格网格
- 编译后 PDF 的页数、方向、分页锚点是否与手册基线一致
- 字体资源和 PDF 嵌入字体是否符合当前模式

校优摘要模板是额外的专项申报模板，不纳入当前工作手册基线 E2E 统计，但可独立编译。

## 说明

当前仓库公开可复现的标准是“工作手册 WPS 渲染基线对齐”。如果你需要再往前推进到逐像素叠图回归，需要在同一渲染器和同一字体资源下增加图像 diff 流程。
