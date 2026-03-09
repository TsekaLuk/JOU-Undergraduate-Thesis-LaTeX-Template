# JOU Undergraduate Thesis LaTeX Template

江苏海洋大学本科毕业论文 LaTeX 模板。编译器：XeLaTeX。

## 关键文件

| 文件 | 用途 |
|------|------|
| `main.tex` | 论文主入口，控制整体结构 |
| `contents/shared/metadata.tex` | 个人信息（姓名、学号、题目、导师等） |
| `contents/chapters/chapter*.tex` | 正文各章节 |
| `references/refs.bib` | BibTeX 参考文献库 |
| `contents/acknowledgements.tex` | 致谢正文 |
| `contents/appendices/appendixA.tex` | 附录 A |
| `styles/jouthesis.cls` | 文档类主文件 |
| `styles/joufonts.sty` | 字体检测与加载 |
| `styles/jouheadings.sty` | 标题、目录、页眉样式 |
| `fonts/proprietary/` | 放入用户自备标准字体文件（可选） |

## 编译命令

```bash
make              # 完整编译论文（推荐）
make fonts        # 下载内置开源字体（首次使用前运行）
make clean        # 清理临时文件
make cleanall     # 清理所有产物（含 PDF）
make view         # 编译并打开 PDF
make wordcount    # 统计正文字数
make test         # 运行 E2E 对齐测试
make help         # 显示所有命令说明
```

手动编译（等价）：

```bash
python3 scripts/download_fonts.py
latexmk -xelatex main.tex
```

## 用户填写个人信息

编辑 `contents/shared/metadata.tex`：

```latex
\def\JOUSharedTitleCN{论文中文题目}
\def\JOUSharedTitleEN{English Title}
\def\JOUSharedAuthorName{姓名}
\def\JOUSharedStudentId{学号}
\def\JOUSharedCollege{学院名称}
\def\JOUSharedProgram{专业名称}
\def\JOUSharedClassName{班级}
\def\JOUSharedSupervisorName{导师姓名}
\def\JOUSharedSupervisorTitle{职称}
\def\JOUSharedThesisCategory{理工农医类}   % 或"文科类"
\def\JOUSharedDate{2026年6月}
\def\JOUSharedCoverDate{年\hspace{2em}月}  % 封面留空让学生手填
```

## 常用 LaTeX 命令

### 论文结构

```latex
% 无编号章节（结论、致谢等后置章节）
\JOUBackmatterChapter{结论与展望}

% 打印参考文献（默认读取 references/refs.bib）
\JOUPrintBibliography
\JOUPrintBibliography[references/other]  % 自定义路径

% 附录章节（第一参数显示在目录，第二参数为章节标题）
\JOUAppendixChapter{附录 A 补充数据}{补充数据}

% 打印符号说明表
\printsymbols
```

### 摘要

```latex
\begin{cnabstract}
    摘要内容...
    \cnkeywords{关键词1；关键词2；关键词3}
\end{cnabstract}

\begin{enabstract}
    Abstract content...
    \enkeywords{Keyword1; Keyword2; Keyword3}
\end{enabstract}
```

### 交叉引用

```latex
\figref{fig:label}    % 图引用 → "图 1.1"
\tabref{tab:label}    % 表引用 → "表 1.1"
\eqnref{eq:label}     % 公式引用 → "式 (1.1)"
\algoref{alg:label}   % 算法引用
\coderef{lst:label}   % 代码引用
```

### 参考文献引用

```latex
\cite{key}        % 普通引用 [1]
\upcite{key}      % 上标引用 ¹（已有标准字体时）
```

## 文档类选项

```latex
\documentclass{styles/jouthesis}               % 默认（自动字体检测）
\documentclass[strictfonts]{styles/jouthesis}  % 严格模式：缺标准字体则报错
```

## 字体策略（自动检测，优先级从高到低）

1. `fonts/proprietary/` — 用户手动放入的标准字体文件
2. 系统学术字体 — `SimSun / SimHei / KaiTi_GB2312 / Times New Roman` 等
3. WPS 字体 — `HY... / FZ...` 系列
4. `fonts/opensource/` — 内置开源兜底（Tinos / Noto CJK / LXGW WenKai / FandolFang）

检查当前字体状态：

```bash
python3 scripts/check_fonts.py
```

## 添加新章节

1. 在 `contents/chapters/` 下新建 `chapterN.tex`
2. 在 `main.tex` 的 `\mainmatter` 后添加：

```latex
\include{contents/chapters/chapterN}
```

## 项目结构

```
JOU-Undergraduate-Thesis-LaTeX-Template/
├── main.tex                        # 论文主文件
├── Makefile                        # 构建脚本
├── contents/
│   ├── shared/metadata.tex         # 个人信息（必填）
│   ├── chapters/                   # 正文章节
│   ├── appendices/                 # 附录
│   ├── acknowledgements.tex        # 致谢
│   └── excellent-abstract/         # 校优摘要内容
├── references/refs.bib             # 参考文献库
├── fonts/
│   ├── opensource/                 # 内置开源字体（make fonts 下载）
│   └── proprietary/                # 放入自备标准字体（可选）
├── styles/
│   ├── jouthesis.cls               # 文档类
│   ├── joufonts.sty                # 字体策略
│   ├── jouheadings.sty             # 标题/目录样式
│   └── jouhandbook.sty             # 配套表单样式
├── templates/
│   ├── forms/                      # 18 份配套表单
│   └── reports/                    # 报告/摘要模板
└── scripts/
    ├── download_fonts.py           # 字体下载脚本
    └── check_fonts.py              # 字体状态检查
```
