\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{jouthesis}[2026/03/07 Jiangsu Ocean University Undergraduate Thesis Template]

\newif\ifjousupercite
\jousupercitefalse
\def\jouNatbibOptions{numbers,sort&compress}

\DeclareOption{supercite}{%
    \jousupercitetrue
    \def\jouNatbibOptions{super,numbers,sort&compress}%
}
\DeclareOption{inlinecite}{%
    \jousupercitefalse
    \def\jouNatbibOptions{numbers,sort&compress}%
}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexbook}}
\ProcessOptions\relax

% 基于ctexbook类，设置A4纸，单面打印
\LoadClass[a4paper,zihao=-4,openany,oneside]{ctexbook}

% 必要的宏包
\RequirePackage{geometry}      % 页面设置
\RequirePackage{fancyhdr}      % 页眉页脚
\RequirePackage{titletoc}      % 目录格式
\RequirePackage{graphicx}      % 插图
\RequirePackage{amsmath}       % 数学公式
\RequirePackage{amssymb}       % 数学符号
\RequirePackage{amsthm}        % 定理环境
\RequirePackage{mathtools}     % 增强数学功能
\RequirePackage{bm}            % 数学粗体
\RequirePackage[\jouNatbibOptions]{natbib} % 数字制参考文献
\RequirePackage{booktabs}      % 三线表
\RequirePackage{tabularx}      % 可伸缩表格
\RequirePackage{array}         % 增强表格功能
\RequirePackage{multirow}      % 跨行单元格
\RequirePackage{makecell}      % 单元格内换行
\RequirePackage{longtable}     % 跨页表格
\RequirePackage{threeparttable} % 表注
\RequirePackage{pdflscape}     % 横向页面
\RequirePackage{tablefootnote} % 表格脚注
\RequirePackage{caption}       % 图表标题
\RequirePackage{subcaption}    % 子图
\RequirePackage{float}         % [H] 浮动控制
\RequirePackage{algorithm}     % 算法浮动体
\RequirePackage{algpseudocode} % 伪代码
\RequirePackage{listings}      % 代码环境
\RequirePackage{siunitx}       % 数值与单位
\RequirePackage[intoc]{nomencl} % 符号表
\RequirePackage{xcolor}        % 颜色
\RequirePackage{enumerate}     % 列表
\RequirePackage{enumitem}      % 增强列表功能
\RequirePackage{setspace}      % 行距
\RequirePackage{indentfirst}   % 首行缩进
\RequirePackage{lastpage}      % 总页数引用
\RequirePackage{styles/joufonts} % 统一字体配置
\RequirePackage{hyperref}      % 超链接
\RequirePackage{bookmark}      % PDF书签
\RequirePackage[capitalize,nameinlink,noabbrev]{cleveref} % 智能引用

% 页面设置 - 精确按照Word文档要求
% Word中: pgSz w="11906" h="16838", pgMar top/right/bottom/left="1418"
% 1缇(twip) = 1/20 磅 = 1/1440 英寸
% 1418缇 ≈ 2.5cm
\geometry{
    a4paper,
    top=2.5cm,
    bottom=2.5cm,
    left=2.5cm,
    right=2.5cm,
    headheight=0.8cm,
    headsep=0.5cm,
    footskip=1cm
}

% 行距设置 - 1.25倍行距
\linespread{1.25}

% 论文信息变量
\newcommand{\studentid}[1]{\def\@studentid{#1}}
\newcommand{\major}[1]{\def\@major{#1}}
\newcommand{\class}[1]{\def\@class{#1}}
\newcommand{\supervisor}[1]{\def\@supervisor{#1}}
\newcommand{\entitle}[1]{\def\@entitle{#1}}
\newcommand{\thesiscategory}[1]{\def\@thesiscategory{#1}}
\def\@thesiscategory{理工农医类}

% 页眉页脚设置
\newcommand{\jou@frontmatterstyle}{
    \fancyhf{}
    \fancyfoot[C]{\zihao{5}\thepage}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
}

\newcommand{\jou@bodystyle}{
    \fancyhf{}
    \fancyhead[L]{\zihao{5}\kaishu 江苏海洋大学二〇二六届本科毕业设计（论文）}
    \fancyhead[C]{\zihao{5}\kaishu \@thesiscategory}
    \fancyhead[R]{\zihao{5}\kaishu 第\thepage 页\ 共 \pageref*{LastPage} 页}
    \renewcommand{\headrulewidth}{0.4pt}
    \renewcommand{\footrulewidth}{0pt}
}

\fancypagestyle{frontmatterstyle}{\jou@frontmatterstyle}
\fancypagestyle{thesisbody}{\jou@bodystyle}
\fancypagestyle{plain}{\jou@frontmatterstyle}
\pagestyle{frontmatterstyle}

\newcommand{\usebodypagestyle}{
    \pagestyle{thesisbody}
    \fancypagestyle{plain}{\jou@bodystyle}
}

% 章节标题格式 - 严格按照要求
\renewcommand{\thechapter}{\arabic{chapter}}
\renewcommand{\thesection}{\thechapter.\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\ctexset{
    % 一级标题: 小三号黑体，段前段后0.5行
    chapter={
        format={\heiti\zihao{-3}\raggedright},
        name={,},
        number={\arabic{chapter}},
        aftername=\hspace{1em},
        beforeskip=0.5\baselineskip,
        afterskip=0.5\baselineskip
    },
    % 二级标题: 四号黑体，段前段后无间距
    section={
        format={\heiti\zihao{4}},
        beforeskip=0pt,
        afterskip=0pt,
        indent=0pt
    },
    % 三级标题: 小四号黑体，段前段后无间距
    subsection={
        format={\heiti\zihao{-4}},
        beforeskip=0pt,
        afterskip=0pt,
        indent=0pt
    }
}

% 正文格式: 小四号宋体，首行缩进2字符
\ctexset{
    punct=quanjiao,
    space=auto,
    autoindent=true
}

% 首行缩进2字符
\setlength{\parindent}{2em}

% 图表标题格式: 五号楷体_GB2312
\DeclareCaptionFont{kaiti5}{\zihao{5}\kaishu}
\captionsetup{
    font=kaiti5,
    labelsep=quad,
    skip=6pt
}
\captionsetup[table]{position=top}
\captionsetup[figure]{position=bottom}
\captionsetup[algorithm]{position=top}
\captionsetup[lstlisting]{position=top}

% 表格精确配置 - 像素级对齐
% 三线表线宽设置（匹配Word默认）
\setlength{\heavyrulewidth}{1.2pt}  % 粗线（上下边框）
\setlength{\lightrulewidth}{0.6pt}  % 细线（中线）
\setlength{\aboverulesep}{0pt}      % 线上间距
\setlength{\belowrulesep}{0pt}      % 线下间距
\setlength{\arrayrulewidth}{0.6pt}  % 竖线宽度

% 表格单元格内边距 - 像素级对齐配置
% 关键：\tabcolsep=0pt 确保列宽精确匹配 Word XML 表格网格
% 单元格内边距通过列定义(L/C/R)中的 \arraybackslash 控制
\setlength{\tabcolsep}{0pt}         % 零列间距（与 jouhandbook.sty 统一）
\renewcommand{\arraystretch}{1.2}   % 行高倍数

% 表格列类型定义
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}  % 左对齐定宽列
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}    % 居中定宽列
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}   % 右对齐定宽列

% 定理类环境
\theoremstyle{plain}
\newtheorem{theorem}{定理}[chapter]
\newtheorem{lemma}[theorem]{引理}
\newtheorem{proposition}[theorem]{命题}
\newtheorem{corollary}[theorem]{推论}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{定义}
\newtheorem{example}[theorem]{例}
\theoremstyle{remark}
\newtheorem{remark}[theorem]{注}

% 伪代码环境
\floatname{algorithm}{算法}
\@addtoreset{algorithm}{chapter}
\renewcommand{\thealgorithm}{\thechapter.\arabic{algorithm}}
\algrenewcommand\algorithmicrequire{\textbf{输入:}}
\algrenewcommand\algorithmicensure{\textbf{输出:}}
\algrenewcommand\algorithmiccomment[1]{\hfill$\triangleright$~#1}

% 代码环境
\renewcommand{\lstlistingname}{代码}
\renewcommand{\lstlistlistingname}{代码目录}
\lstdefinestyle{joucode}{
    basicstyle=\small\ttfamily,
    keywordstyle=\color{blue!60!black}\bfseries,
    commentstyle=\color{green!40!black},
    stringstyle=\color{red!60!black},
    numbers=left,
    numberstyle=\tiny\color{gray},
    stepnumber=1,
    numbersep=8pt,
    frame=single,
    rulecolor=\color{black!30},
    breaklines=true,
    breakatwhitespace=false,
    showstringspaces=false,
    columns=fullflexible,
    keepspaces=true,
    tabsize=4,
    xleftmargin=1.5em,
    xrightmargin=0.5em,
    captionpos=t
}
\lstset{style=joucode}

% 单位与数值
\sisetup{
    detect-all = true,
    per-mode = symbol,
    range-phrase = {--},
    range-units = single,
    group-separator = {,},
    group-minimum-digits = 4
}

% 符号表
\renewcommand{\nomname}{符号说明}
\makenomenclature

% 列表配置 - 精确间距
\setlist{
    nosep,                % 紧凑列表
    topsep=0pt,           % 列表前后间距
    partopsep=0pt,
    itemsep=0pt,          % 列表项间距
    parsep=0pt
}

% 超链接设置
\hypersetup{
    colorlinks=true,
    linkcolor=black,
    citecolor=black,
    urlcolor=blue,
    bookmarksnumbered=true,
    pdfstartview=FitH
}
\bookmarksetup{numbered=true,open=true}

% 智能引用名称
\crefname{figure}{图}{图}
\Crefname{figure}{图}{图}
\crefname{table}{表}{表}
\Crefname{table}{表}{表}
\crefname{equation}{式}{式}
\Crefname{equation}{式}{式}
\crefname{algorithm}{算法}{算法}
\Crefname{algorithm}{算法}{算法}
\crefname{theorem}{定理}{定理}
\Crefname{theorem}{定理}{定理}
\crefname{lemma}{引理}{引理}
\Crefname{lemma}{引理}{引理}
\crefname{proposition}{命题}{命题}
\Crefname{proposition}{命题}{命题}
\crefname{corollary}{推论}{推论}
\Crefname{corollary}{推论}{推论}
\crefname{definition}{定义}{定义}
\Crefname{definition}{定义}{定义}
\crefname{example}{例}{例}
\Crefname{example}{例}{例}
\crefname{remark}{注}{注}
\Crefname{remark}{注}{注}
\crefname{chapter}{第}{第}
\Crefname{chapter}{第}{第}
\crefname{section}{节}{节}
\Crefname{section}{节}{节}
\crefname{subsection}{小节}{小节}
\Crefname{subsection}{小节}{小节}
\crefname{lstlisting}{代码}{代码}
\Crefname{lstlisting}{代码}{代码}
\crefname{listing}{代码}{代码}
\Crefname{listing}{代码}{代码}

% 便捷引用命令
\newcommand{\figref}[1]{\cref{#1}}
\newcommand{\tabref}[1]{\cref{#1}}
\newcommand{\eqnref}[1]{\cref{#1}}
\newcommand{\algoref}[1]{\cref{#1}}
\newcommand{\thmref}[1]{\cref{#1}}
\newcommand{\coderef}[1]{\cref{#1}}
\ifjousupercite
    \newcommand{\upcite}[1]{\cite{#1}}
\else
    \newcommand{\upcite}[1]{\textsuperscript{\cite{#1}}}
\fi
\crefformat{chapter}{第#2#1#3章}
\Crefformat{chapter}{第#2#1#3章}
\crefformat{section}{#2#1#3节}
\Crefformat{section}{#2#1#3节}
\crefformat{subsection}{#2#1#3小节}
\Crefformat{subsection}{#2#1#3小节}


% 封面命令
\newcommand{\makecover}{
    \begin{titlepage}
        \thispagestyle{empty}
        \centering
        \vspace*{2.2cm}

        {\JOUXiaobiaoSong\zihao{2}本\hspace{1em}科\hspace{1em}毕\hspace{1em}业\hspace{1em}设\hspace{0.5em}计（论\hspace{0.5em}文）\par}
        \vspace{3.0cm}

        {\JOUXingkai\zihao{2}\@title\par}
        \vspace{0.7cm}

        {\bfseries\fontsize{22pt}{30pt}\selectfont \@entitle\par}
        \vspace{3.0cm}

        {\kaishu\zihao{4}
            \begin{tabular}{@{}p{2.6cm}p{10.0cm}@{}}
                学\hspace{2em}院： & \@major \\[0.95cm]
                专业班级： & \@class \\[0.95cm]
                学生姓名： & \@author \hfill 学\hspace{1em}号：\ \@studentid \\[0.95cm]
                指导教师： & \@supervisor \\[0.2cm]
            \end{tabular}\par
        }

        \vfill
        {\songti\zihao{4} \@date\par}
    \end{titlepage}

    % 原创性声明页
    \clearpage
    \thispagestyle{frontmatterstyle}
    \vspace*{1.8cm}
    {\centering\heiti\zihao{3}\textbf{江苏海洋大学}\\[0.5cm]}
    {\centering\heiti\zihao{3}\textbf{毕业设计（论文）原创性声明}\\[1cm]}

    {\zihao{-4}\songti
    本人郑重声明：所呈交的毕业设计（论文），是本人在导师的指导下，独立进行研究工作所取得的成果。除文中已经注明引用的内容外，本论文不包含任何其他个人或集体已经发表或撰写过的作品成果。对本文的研究做出重要贡献的个人和集体，均已在文中以明确方式标明。本人完全意识到本声明的法律结果由本人承担。
    }

    \vspace{2cm}
    作者签名：\underline{\hspace{4cm}} \hfill 日期：\underline{\hspace{3cm}}

    \vspace{2cm}
    {\centering\heiti\zihao{3}\textbf{江苏海洋大学}\\[0.5cm]}
    {\centering\heiti\zihao{3}\textbf{毕业设计（论文）版权使用授权书}\\[1cm]}

    {\zihao{-4}\songti
    本毕业设计（论文）作者同意学校保留并向国家有关部门或机构送交论文的复印件和电子版，允许论文被查阅和借阅。本人授权江苏海洋大学可以将本毕业设计（论文）的全部或部分内容编入有关数据库进行检索，可以采用影印、缩印或扫描等复制手段保存和汇编本毕业设计（论文）。
    }

    \vspace{2cm}
    作者签名：\underline{\hspace{4cm}} \hfill 指导教师签名：\underline{\hspace{4cm}}

    \vspace{1cm}
    日期：\underline{\hspace{3cm}} \hfill 日期：\underline{\hspace{3cm}}

    \clearpage
}

% 中文摘要环境
\newenvironment{cnabstract}{
    \clearpage
    \thispagestyle{frontmatterstyle}
    \vspace*{\baselineskip}
    {\centering\heiti\zihao{4}\textbf{毕业设计（论文）中文摘要}\par}
    \vspace{\baselineskip}
    {\centering\songti\zihao{4}\@title\par}
    \vspace{\baselineskip}
    \noindent{\heiti\zihao{-4}\textbf{摘\hspace{1em}要：}}
    \zihao{-4}\songti
}{
    \clearpage
}

% 英文摘要环境
\newenvironment{enabstract}{
    \clearpage
    \thispagestyle{frontmatterstyle}
    \vspace*{\baselineskip}
    {\centering\heiti\zihao{4}\textbf{毕业设计（论文）外文摘要}\par}
    \vspace{\baselineskip}
    {\centering\zihao{4}\textbf{\@entitle}\par}
    \vspace{\baselineskip}
    \noindent{\zihao{-4}\textbf{Abstract: }}
    \zihao{-4}
}{
    \clearpage
}

% 关键词命令
\newcommand{\cnkeywords}[1]{
    \vspace{\baselineskip}
    \noindent{\heiti\zihao{-4}\textbf{关键词：}}{\zihao{-4}\songti #1}
}

\newcommand{\enkeywords}[1]{
    \vspace{\baselineskip}
    \noindent{\zihao{-4}\textbf{Keywords: }}{\zihao{-4}#1}
}

\newcommand{\printsymbols}{
    \clearpage
    \thispagestyle{frontmatterstyle}
    \printnomenclature[2.5cm]
    \clearpage
}

% 目录格式
\renewcommand{\contentsname}{目\hspace{2em}录}
\setcounter{tocdepth}{1}
\titlecontents{chapter}[0pt]{\songti\zihao{-4}}
    {\thecontentslabel\hspace{1em}}{}
    {\titlerule*[0.5pc]{.}\contentspage}
\titlecontents{section}[2em]{\songti\zihao{-4}}
    {\thecontentslabel\hspace{1em}}{}
    {\titlerule*[0.5pc]{.}\contentspage}

\endinput
