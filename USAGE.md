# 江苏海洋大学毕业论文 LaTeX 模板使用指南

## 目录

1. [快速开始](#快速开始)
2. [详细配置](#详细配置)
3. [章节编写](#章节编写)
4. [图表插入](#图表插入)
5. [参考文献](#参考文献)
6. [常见问题](#常见问题)

## 快速开始

### 第一步：环境检查

确保已安装：
- TeX Live 2020+ 或 MikTeX 2.9+
- XeLaTeX 编译器
- 中文字体（宋体、黑体、楷体_GB2312、仿宋_GB2312）

检查安装：
```bash
xelatex --version
```

### 第二步：填写基本信息

编辑 `main.tex` 文件开头：

```latex
\title{基于深度学习的图像识别算法研究}
\entitle{Research on Image Recognition Algorithm Based on Deep Learning}
\author{张三}
\studentid{2020123456}
\major{计算机与信息学院}
\class{计算机科学与技术 计科201}
\supervisor{李四（教授）}
\date{2026年6月}
```

### 第三步：编译

```bash
make
```

或

```bash
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

## 详细配置

### 封面信息

| 字段 | 说明 | 示例 |
|------|------|------|
| `\title{}` | 论文中文标题 | 基于深度学习的... |
| `\entitle{}` | 论文英文标题 | Research on ... |
| `\author{}` | 学生姓名 | 张三 |
| `\studentid{}` | 学号 | 2020123456 |
| `\major{}` | 学院名称 | 计算机与信息学院 |
| `\class{}` | 专业班级 | 计算机科学与技术 计科201 |
| `\supervisor{}` | 指导教师（职称） | 李四（教授） |
| `\date{}` | 日期 | 2026年6月 |

### 摘要编写

#### 中文摘要

```latex
\begin{cnabstract}
    本文研究了...（摘要内容约300字）

    \cnkeywords{深度学习；图像识别；卷积神经网络；特征提取}
\end{cnabstract}
```

**注意事项**：
- 摘要约300字
- 关键词3-5个
- 关键词之间用中文分号"；"分隔
- 最后一个关键词后无标点

#### 英文摘要

```latex
\begin{enabstract}
    This paper studies... (About 200-300 words)

    \enkeywords{Deep Learning; Image Recognition; CNN; Feature Extraction}
\end{enabstract}
```

**注意事项**：
- 关键词之间用英文分号"; "分隔（分号后有空格）
- 关键词首字母大写
- 最后一个关键词后无标点

## 章节编写

### 章节结构

```latex
\chapter{绪论}  % 一级标题

\section{研究背景}  % 二级标题

\subsection{国内研究现状}  % 三级标题

\subsubsection{详细内容}  % 四级标题（如需要）
```

### 章节编号规则

- 一级标题：1, 2, 3, ...
- 二级标题：1.1, 1.2, 1.3, ...
- 三级标题：1.1.1, 1.1.2, ...
- 建议不超过三级

### 段落格式

- **首行缩进**：自动缩进2个汉字
- **行距**：1.25倍行距（已自动设置）
- **对齐**：两端对齐（默认）

### 特殊章节

#### 结论与展望

```latex
\chapter*{结论与展望}
\addcontentsline{toc}{chapter}{结论与展望}

通过本文的研究，得出以下结论：...
```

#### 致谢

```latex
\chapter*{致\hspace{1em}谢}
\addcontentsline{toc}{chapter}{致谢}

在此感谢...
```

## 图表插入

### 插入图片

#### 基本用法

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.6\textwidth]{figures/architecture.png}
    \caption{系统架构图}
    \label{fig:architecture}
\end{figure}
```

#### 参数说明

- `[htbp]`：浮动位置（here, top, bottom, page）
- `width=0.6\textwidth`：图片宽度为页面宽度的60%
- `\caption{}`：图题（会自动编号）
- `\label{}`：标签，用于引用

#### 引用图片

```latex
如图\ref{fig:architecture}所示，系统架构包括...
```

#### 并排图片

```latex
\begin{figure}[htbp]
    \centering
    \begin{subfigure}{0.45\textwidth}
        \includegraphics[width=\textwidth]{figures/img1.png}
        \caption{子图1标题}
        \label{fig:sub1}
    \end{subfigure}
    \hfill
    \begin{subfigure}{0.45\textwidth}
        \includegraphics[width=\textwidth]{figures/img2.png}
        \caption{子图2标题}
        \label{fig:sub2}
    \end{subfigure}
    \caption{总图标题}
    \label{fig:total}
\end{figure}
```

### 插入表格

#### 基本三线表

```latex
\begin{table}[htbp]
    \centering
    \caption{实验结果对比}
    \label{tab:results}
    \begin{tabular}{cccc}
        \toprule
        方法 & 准确率(\%) & 召回率(\%) & F1值 \\
        \midrule
        方法A & 85.3 & 82.1 & 83.7 \\
        方法B & 88.6 & 85.9 & 87.2 \\
        本文方法 & 91.2 & 89.5 & 90.3 \\
        \bottomrule
    \end{tabular}
\end{table}
```

#### 引用表格

```latex
表\ref{tab:results}显示了不同方法的性能对比。
```

#### 跨页表格

```latex
\begin{longtable}{cccc}
    \caption{长表格标题} \label{tab:long} \\
    \toprule
    列1 & 列2 & 列3 & 列4 \\
    \midrule
    \endfirsthead

    \multicolumn{4}{c}{续表} \\
    \toprule
    列1 & 列2 & 列3 & 列4 \\
    \midrule
    \endhead

    \bottomrule
    \endfoot

    % 数据行
    数据1 & 数据2 & 数据3 & 数据4 \\
    % ... 更多行
\end{longtable}
```

### 数学公式

#### 行内公式

```latex
爱因斯坦质能方程 $E=mc^2$ 表明...
```

#### 行间公式

```latex
\begin{equation}
    f(x) = \int_{a}^{b} g(t) \, dt
    \label{eq:integral}
\end{equation}
```

#### 引用公式

```latex
根据式(\ref{eq:integral})可知...
```

#### 多行公式

```latex
\begin{align}
    x &= a + b + c \\
    y &= d + e + f \\
    z &= g + h + i
\end{align}
```

## 参考文献

### BibTeX格式

在 `references/refs.bib` 中添加文献：

#### 期刊论文

```bibtex
@article{zhang2026deep,
    author = {张三 and 李四 and 王五},
    title = {深度学习在图像识别中的应用},
    journal = {计算机学报},
    year = {2026},
    volume = {49},
    number = {3},
    pages = {456--468}
}
```

#### 会议论文

```bibtex
@inproceedings{li2025cnn,
    author = {Li, Si and Wang, Wu},
    title = {Improved CNN Architecture for Image Classification},
    booktitle = {Proceedings of CVPR 2025},
    year = {2025},
    pages = {1234--1243}
}
```

#### 书籍

```bibtex
@book{goodfellow2016deep,
    author = {Ian Goodfellow and Yoshua Bengio and Aaron Courville},
    title = {Deep Learning},
    publisher = {MIT Press},
    year = {2016},
    address = {Cambridge, MA}
}
```

#### 学位论文

```bibtex
@phdthesis{zhao2024thesis,
    author = {赵六},
    title = {基于深度学习的目标检测算法研究},
    school = {江苏海洋大学},
    year = {2024},
    address = {连云港}
}
```

### 引用文献

#### 单个引用

```latex
根据文献\cite{zhang2026deep}的研究...
```

#### 多个引用

```latex
已有研究\cite{zhang2026deep,li2025cnn,goodfellow2016deep}表明...
```

### 参考文献格式要求

按照《江苏海洋大学学报》参考文献著录格式：

- 按文中出现顺序编号
- 使用方括号 [1], [2], [3]
- 作者超过3人时写"等"或"et al."
- 中英文混排时，中文在前，英文在后

## 常见问题

### Q1: 如何调整图片大小？

```latex
% 按宽度缩放
\includegraphics[width=0.8\textwidth]{figures/img.png}

% 按高度缩放
\includegraphics[height=6cm]{figures/img.png}

% 按比例缩放
\includegraphics[scale=0.5]{figures/img.png}
```

### Q2: 如何强制图表位置？

```latex
% 使用 [H] 参数（需要 float 宏包）
\usepackage{float}

\begin{figure}[H]  % 强制在此处
    ...
\end{figure}
```

### Q3: 如何添加代码？

使用 `listings` 宏包：

```latex
\usepackage{listings}
\usepackage{xcolor}

\lstset{
    language=Python,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue},
    commentstyle=\color{gray},
    stringstyle=\color{red},
    numbers=left,
    numberstyle=\tiny,
    frame=single,
    breaklines=true
}

\begin{lstlisting}
def hello_world():
    print("Hello, World!")
\end{lstlisting}
```

### Q4: 如何添加附录？

```latex
% 在参考文献之后
\appendix
\chapter{附录A：实验数据}

这里是附录内容...
```

### Q5: 参考文献不显示怎么办？

确保完整编译流程：

```bash
xelatex main.tex   # 第1次
bibtex main        # 处理参考文献
xelatex main.tex   # 第2次
xelatex main.tex   # 第3次
```

或使用 Makefile：

```bash
make clean && make
```

### Q6: 如何生成图表清单？

在 `main.tex` 目录部分添加：

```latex
\listoffigures  % 图清单
\clearpage
\listoftables   % 表清单
\clearpage
```

### Q7: 如何修改页眉内容？

编辑 `styles/jouthesis.cls` 文件中的：

```latex
\fancyhead[C]{\zihao{5}\kaishu 江苏海洋大学本科生毕业论文}
```

### Q8: 如何添加页码范围？

默认从正文开始编页码。如需调整，在相应位置添加：

```latex
\pagenumbering{Roman}  % 大写罗马数字 I, II, III
\pagenumbering{roman}  % 小写罗马数字 i, ii, iii
\pagenumbering{arabic} % 阿拉伯数字 1, 2, 3
```

## 高级技巧

### 自定义命令

```latex
% 在导言区定义
\newcommand{\keyword}[1]{\textbf{#1}}

% 使用
\keyword{深度学习}是一种...
```

### 条件编译

```latex
% 在导言区
\newif\ifdraft
\drafttrue  % 草稿模式
%\draftfalse % 最终版本

% 在文档中
\ifdraft
    这是草稿版本的内容
\else
    这是最终版本的内容
\fi
```

### 批量处理图片

```latex
% 设置图片默认路径
\graphicspath{{figures/}{images/}}

% 设置默认扩展名
\DeclareGraphicsExtensions{.pdf,.png,.jpg}
```

## 检查清单

提交前请检查：

- [ ] 封面信息完整准确
- [ ] 摘要和关键词符合要求
- [ ] 目录自动生成正确
- [ ] 所有图表都有标题和编号
- [ ] 参考文献格式正确
- [ ] 页眉页脚显示正确
- [ ] 无编译错误和警告
- [ ] PDF可正常打开和打印

## 获取帮助

- 查看 [README.md](README.md)
- 提交 [Issue](https://github.com/TsekaLuk/JOU-Undergraduate-Thesis-LaTeX-Template/issues)
- 参考 [LaTeX常见问题](https://www.latexstudio.net/)

祝论文写作顺利！🎓
