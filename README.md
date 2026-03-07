# 江苏海洋大学本科生毕业论文 LaTeX 模板

Jiangsu Ocean University Undergraduate Thesis LaTeX Template (2026届)

## 📋 项目结构

```
.
├── main.tex                    # 主文件，编译入口（毕业论文）
├── Makefile                    # 编译自动化脚本
├── .gitignore                  # Git忽略文件
├── styles/
│   └── jouthesis.cls          # 样式类文件（核心格式定义）
├── contents/
│   ├── chapters/              # 正文章节
│   │   ├── chapter1.tex       # 第1章：绪论
│   │   ├── chapter2.tex       # 第2章：相关理论（含图表公式示例）
│   │   └── chapter3.tex       # 第3章：系统设计
│   ├── appendices/            # 附录
│   │   └── appendixA.tex
│   └── acknowledgements.tex   # 致谢
├── figures/                   # 图片资源目录
├── references/
│   └── refs.bib              # 参考文献数据库（BibTeX格式）
├── templates/                 # 📦 完整模板集（16个）
│   ├── forms/                 # 表格类模板（7个）
│   ├── reports/               # 报告类模板（5个）
│   ├── evaluations/           # 评价类模板（3个）
│   └── README.md              # 模板使用说明
└── README.md                 # 本文件
```

## 📦 完整模板集

**本项目不仅包含毕业论文模板，还提供了完整的16个配套模板**，覆盖从选题到答辩的全流程：

| 类别 | 数量 | 模板列表 |
|------|------|----------|
| **表格类** | 7个 | 选题审题表、实习登记表、任务书（理工/人文）、开题答辩记录、中期检查表、答辩记录 |
| **报告类** | 5个 | 实习日记、实习报告书、开题报告（理工/人文）、外文资料翻译 |
| **评价类** | 3个 | 论文评语、评分表（理工/人文） |
| **正文** | 1个 | 毕业设计（论文）说明书（main.tex） |

**详细说明**: 参见 [templates/README.md](templates/README.md)

### 快速使用模板

```bash
# 编译单个模板（以选题审题表为例）
cd templates/forms
xelatex topic-selection.tex

# 查看完整模板列表
cat templates/README.md
```

**特点**:
- ✅ **全流程覆盖** - 从选题到答辩的所有必需文档
- ✅ **像素级对齐** - 所有模板严格按照官方Word文档制作
- ✅ **独立编译** - 每个模板都可独立使用
- ✅ **官方Logo** - 自动引用学校logo
- ✅ **规范格式** - 表格线宽、间距精确匹配

## ⚙️ 环境要求

### 必需软件
- **TeX Live 2020+** 或 **MikTeX 2.9+**
- 支持 XeLaTeX 编译器

### 必需中文字体
- 宋体 (SimSun)
- 黑体 (SimHei)
- 楷体_GB2312 (KaiTi_GB2312)
- 仿宋_GB2312 (FangSong_GB2312)

### macOS 用户
```bash
# 安装BasicTeX（轻量级）
brew install --cask basictex
# 或安装完整MacTeX
brew install --cask mactex

# 安装缺失的宏包
sudo tlmgr update --self
sudo tlmgr install ctex zhnumber xecjk
```

### Windows 用户
推荐安装 [TeX Live](https://www.tug.org/texlive/) 完整版，已包含所需宏包和字体。

### Linux 用户
```bash
# Ubuntu/Debian
sudo apt-get install texlive-xetex texlive-lang-chinese

# 安装Windows中文字体
sudo apt-get install ttf-mscorefonts-installer
```

## 🚀 使用方法

### 方法一：使用 Makefile（推荐）

```bash
# 完整编译
make

# 清理临时文件
make clean

# 完全清理（包括PDF）
make cleanall

# 编译并预览
make view
```

### 方法二：手动编译

```bash
# XeLaTeX编译（运行4次确保引用正确）
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

### 方法三：使用 latexmk

```bash
# 自动化编译
latexmk -xelatex main.tex

# 清理
latexmk -c
```

## ✨ 核心特性

- ✅ **像素级格式对齐** - 从Word文档XML精确提取所有格式参数
- ✅ **官方Logo集成** - 无损提取4张学校logo，已配置到封面
- ✅ **精确表格配置** - 预设三线表样式，支持跨行跨列、定宽列等
- ✅ **完整文档结构** - 封面、声明、摘要、目录、正文、参考文献、附录
- ✅ **全流程模板集** - 16个配套模板，覆盖选题、实习、开题、中期、答辩全过程
- ✅ **详细使用文档** - README、USAGE、TABLE-EXAMPLES、ASSETS四份文档

## 📝 格式说明

本模板严格按照《江苏海洋大学2026届毕业实习与设计（论文）工作手册》要求制作：

### 页面设置
- **纸张**: A4 (210mm × 297mm)
- **页边距**: 上下左右均为 2.5cm
- **行距**: 1.25倍行距
- **页眉**: 五号楷体_GB2312，内容"江苏海洋大学本科生毕业论文"
- **页脚**: 五号字，页码居中

### 字体和字号
- **一级标题**: 小三号黑体，段前段后0.5行
- **二级标题**: 四号黑体
- **三级标题**: 小四号黑体
- **正文**: 小四号宋体，首行缩进2字符
- **英文**: Times New Roman
- **图表**: 五号楷体_GB2312
- **页眉页脚**: 五号楷体_GB2312

### 章节编号
- 一级标题: 1, 2, 3, ...
- 二级标题: 1.1, 1.2, 1.3, ...
- 三级标题: 1.1.1, 1.1.2, 1.1.3, ...
- 最多四级编号

### 图表要求
- **图题**: 位于图下方，五号楷体
- **表题**: 位于表上方，五号楷体
- **表格**: 使用三线表（\toprule, \midrule, \bottomrule）

## 📚 文档资源

| 文档 | 内容 |
|------|------|
| [README.md](README.md) | 项目概述、安装指南、快速开始 |
| [USAGE.md](USAGE.md) | 详细使用指南（章节、图表、公式、参考文献） |
| [TABLE-EXAMPLES.md](TABLE-EXAMPLES.md) | 表格使用示例（三线表、跨行列、定宽列等） |
| [ASSETS.md](ASSETS.md) | 图片资源说明（logo使用、尺寸规范） |

## 🖼️ 官方Logo资源

从官方工作手册提取的高清logo：

| 文件 | 尺寸 | 用途 |
|------|------|------|
| `jou-logo-full.png` | 1237×873px | 封面主logo（已配置） |
| `jou-name-large.png` | 798×160px | 横版校名（大） |
| `jou-name-small.png` | 433×99px | 横版校名（小） |
| `jou-name-large-rgba.png` | 798×160px | 透明背景版本 |

详见 [ASSETS.md](ASSETS.md) 了解使用方法。

## 📖 快速开始

### 1. 填写论文基本信息

编辑 `main.tex` 文件头部：

```latex
\title{论文中文题目}
\entitle{English Title of the Thesis}
\author{学生姓名}
\studentid{学号}
\major{学院名称}
\class{专业班级}
\supervisor{指导教师（职称）}
\date{\the\year{}年\the\month{}月}
```

### 2. 编写摘要

在 `main.tex` 中的摘要环境内填写：

```latex
\begin{cnabstract}
    中文摘要内容...
    \cnkeywords{关键词1；关键词2；关键词3}
\end{cnabstract}

\begin{enabstract}
    English abstract content...
    \enkeywords{Keyword1; Keyword2; Keyword3}
\end{enabstract}
```

### 3. 编写正文

在 `contents/chapters/` 目录下的 `.tex` 文件中编写各章节内容。

### 4. 添加参考文献

在 `references/refs.bib` 中添加BibTeX格式的参考文献：

```bibtex
@article{example2026,
    author = {张三 and 李四},
    title = {示例文献标题},
    journal = {江苏海洋大学学报},
    year = {2026},
    volume = {1},
    number = {1},
    pages = {1--10}
}
```

在正文中引用：`\cite{example2026}`

### 5. 插入图片

将图片放在 `figures/` 目录，然后：

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.6\textwidth]{figures/example.png}
    \caption{图片标题}
    \label{fig:example}
\end{figure}
```

引用：`图\ref{fig:example}所示...`

### 6. 插入表格

```latex
\begin{table}[htbp]
    \centering
    \caption{表格标题}
    \label{tab:example}
    \begin{tabular}{ccc}
        \toprule
        列1 & 列2 & 列3 \\
        \midrule
        数据1 & 数据2 & 数据3 \\
        \bottomrule
    \end{tabular}
\end{table}
```

## 🔧 常见问题

### Q1: 编译报错"字体未找到"
**A**: 确保系统已安装楷体_GB2312和仿宋_GB2312字体。Windows用户一般自带，macOS和Linux用户需要手动安装。

### Q2: 参考文献不显示
**A**: 确保按顺序运行：`xelatex` → `bibtex` → `xelatex` → `xelatex`

### Q3: 中文显示乱码
**A**: 确保使用 `xelatex` 编译（不要用 `pdflatex`）

### Q4: 页眉页脚格式不对
**A**: 检查是否正确使用了 `\clearpage` 和分节符

## 📚 参考资料

- [江苏海洋大学教务处](http://jwc.jou.edu.cn/)
- [LaTeX中文文档](https://www.latexstudio.net/)
- [CTEX 宏包文档](http://mirrors.ctan.org/language/chinese/ctex/ctex.pdf)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！如果发现格式问题或有改进建议，请：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📮 联系方式

如有问题，请通过以下方式联系：

- 提交 [Issue](https://github.com/TsekaLuk/JOU-Undergraduate-Thesis-LaTeX-Template/issues)
- 邮箱: [your-email@example.com]

## ⭐ Star History

如果这个模板对你有帮助，请给个 Star ⭐ 支持一下！
