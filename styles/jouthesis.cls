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

% 基于ctexbook类，设置A4纸，单面打印，字体完全交由 joufonts.sty 管理
\LoadClass[a4paper,zihao=-4,openany,oneside,fontset=none]{ctexbook}

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
\RequirePackage[preferwps]{styles/joufonts} % 统一字体配置
\RequirePackage{styles/jouheadings} % 标题/页眉/目录统一规范
\RequirePackage[absolute,overlay]{textpos} % 摘要等页面的绝对定位
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
\setlength{\TPHorizModule}{1cm}
\setlength{\TPVertModule}{1cm}
\textblockorigin{0cm}{0cm}

% 行距设置 - 1.25倍行距
\linespread{1.25}

% 论文信息变量
\newcommand{\studentid}[1]{\def\@studentid{#1}}
\newcommand{\major}[1]{\def\@major{#1}}
\newcommand{\class}[1]{\def\@class{#1}}
\newcommand{\supervisor}[1]{\def\@supervisor{#1}}
\newcommand{\entitle}[1]{\def\@entitle{#1}}
\newcommand{\coverdate}[1]{\def\@coverdate{#1}}
\newcommand{\thesiscategory}[1]{\def\@thesiscategory{#1}}
\def\@thesiscategory{理工农医类}
\def\@coverdate{\@date}

% 页眉页脚设置
\newcommand{\jou@frontmatterstyle}{
    \fancyhf{}
    \fancyfoot[C]{\zihao{5}\thepage}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
}

\newcommand{\jou@bodystyle}{
    \fancyhf{}
    \fancyhead[L]{\zihao{5}\kaishu \JOUHeadingBodyHeaderLeftInline}
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

% 标题、段落与目录规范统一交由 jouheadings 维护
\JOUApplyBodySectioning
\JOUApplyBodyTextLayout

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
\newtheoremstyle{jouthm}%
    {0.6\baselineskip}%
    {0.6\baselineskip}%
    {\normalfont\songti}%
    {2em}%
    {\normalfont\heiti}%
    {：}%
    {0.5em}%
    {}
\newtheoremstyle{joudef}%
    {0.6\baselineskip}%
    {0.6\baselineskip}%
    {\normalfont\songti}%
    {2em}%
    {\normalfont\heiti}%
    {：}%
    {0.5em}%
    {}
\newtheoremstyle{jouremark}%
    {0.6\baselineskip}%
    {0.6\baselineskip}%
    {\normalfont\songti}%
    {2em}%
    {\normalfont\heiti}%
    {：}%
    {0.5em}%
    {}
\theoremstyle{jouthm}
\newtheorem{theorem}{定理}[chapter]
\newtheorem{lemma}[theorem]{引理}
\newtheorem{proposition}[theorem]{命题}
\newtheorem{corollary}[theorem]{推论}
\theoremstyle{joudef}
\newtheorem{definition}[theorem]{定义}
\newtheorem{example}[theorem]{例}
\theoremstyle{jouremark}
\newtheorem{remark}[theorem]{注}

% 伪代码环境
\floatname{algorithm}{算法}
\@addtoreset{algorithm}{chapter}
\renewcommand{\thealgorithm}{\thechapter.\arabic{algorithm}}
\algrenewcommand\algorithmicrequire{{\heiti 输入:}}
\algrenewcommand\algorithmicensure{{\heiti 输出:}}
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

\JOUApplyBodyReferenceNames

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
\newcommand{\JOUCoverHeader}{figures/jou-cover-header-clean.png}
\newcommand{\jou@coverrule}[1]{%
    \makebox[0pt][l]{\raisebox{-0.52ex}{\rule{#1}{0.35pt}}}%
}
\newcommand{\jou@coverunderline}[2]{%
    \jou@coverrule{#1}\makebox[#1][l]{#2\hfill}%
}

\newcommand{\jou@coverrowspace}{\\[0.24cm]}
\newcommand{\jou@coverlabelacademy}{\makebox[3.57cm][l]{学\hspace{1.41cm}院：}}
\newcommand{\jou@coverlabelclass}{\makebox[3.57cm][l]{专\hspace{0.37cm}业\hspace{0.37cm}班\hspace{0.37cm}级：}}
\newcommand{\jou@coverlabelstudent}{\makebox[3.57cm][l]{学\hspace{0.37cm}生\hspace{0.37cm}姓\hspace{0.37cm}名：}}
\newcommand{\jou@coverlabelsupervisor}{\makebox[3.57cm][l]{指\hspace{0.37cm}导\hspace{0.37cm}教\hspace{0.37cm}师：}}
\newcommand{\jou@coverlabelid}{\makebox[2.72cm][l]{学\hspace{0.55cm}号：}}
\newcommand{\jou@coverdatexoffset}{0.58cm}
\newcommand{\jou@coverdateyoffset}{0.00cm}
\newcommand{\jou@covermaintitlefont}{\JOUXiaobiaoSong\bfseries}
\newcommand{\jou@coverheavierkai}{\JOUCoverKai\bfseries}
\newcommand{\jou@coverdateformat}{%
    \makebox[\textwidth][c]{%
        \hspace*{\jou@coverdatexoffset}%
        \raisebox{\jou@coverdateyoffset}{\jou@coverheavierkai\zihao{3}\@coverdate}%
    }%
}

% 封面命令
\newcommand{\makecover}{
    \begin{titlepage}
        \thispagestyle{empty}
        \centering
        \vspace*{2.10cm}

        \includegraphics[width=11.05cm]{\JOUCoverHeader}\par
        \vspace{0.48cm}

        {\makebox[0pt][c]{\hspace*{-0.12cm}\jou@covermaintitlefont\zihao{2}本\hspace{0.42em}科\hspace{0.42em}毕\hspace{0.42em}业\hspace{0.42em}设\hspace{0.42em}计\hspace{0.42em}（论\hspace{0.42em}文）}\par}
        \vspace{3.56cm}

        {\makebox[0pt][c]{\hspace*{0.17cm}\jou@coverheavierkai\zihao{2}\scalebox{0.965}[1]{\@title}}\par}
        \vspace{0.53cm}

        {\makebox[0pt][c]{\hspace*{0.14cm}\rmfamily\bfseries\fontsize{21.5pt}{28pt}\selectfont \scalebox{0.960}[1]{\@entitle}}\par}
        \vspace{3.92cm}

        {\JOUCoverKai\zihao{4}
            \makebox[0pt][c]{\hspace*{0.16cm}\begin{tabular}{@{}p{3.57cm}p{3.43cm}p{2.72cm}p{3.10cm}@{}}
                {\jou@coverheavierkai \jou@coverlabelacademy} &
                \multicolumn{3}{@{}l@{}}{\jou@coverunderline{9.25cm}{\@major}}
                \jou@coverrowspace
                {\jou@coverheavierkai \jou@coverlabelclass} &
                \multicolumn{3}{@{}l@{}}{\jou@coverunderline{9.25cm}{\@class}}
                \jou@coverrowspace
                {\jou@coverheavierkai \jou@coverlabelstudent} &
                \jou@coverunderline{3.15cm}{\@author} &
                {\jou@coverheavierkai \jou@coverlabelid} &
                \jou@coverunderline{3.10cm}{\@studentid}
                \jou@coverrowspace
                {\jou@coverheavierkai \jou@coverlabelsupervisor} &
                \multicolumn{3}{@{}l@{}}{\jou@coverunderline{9.25cm}{\@supervisor}}\\
            \end{tabular}}\par
        }

        \vspace{1.51cm}
        {\jou@coverdateformat\par}
    \end{titlepage}

    % 原创性声明页
    \clearpage
    \thispagestyle{frontmatterstyle}
    \vspace*{1.8cm}
    {\centering\heiti\zihao{3}江苏海洋大学\\[0.5cm]}
    {\centering\heiti\zihao{3}毕业设计（论文）原创性声明\\[1cm]}

    {\zihao{-4}\songti
    本人郑重声明：所呈交的毕业设计（论文），是本人在导师的指导下，独立进行研究工作所取得的成果。除文中已经注明引用的内容外，本论文不包含任何其他个人或集体已经发表或撰写过的作品成果。对本文的研究做出重要贡献的个人和集体，均已在文中以明确方式标明。本人完全意识到本声明的法律结果由本人承担。
    }

    \vspace{2cm}
    作者签名：\underline{\hspace{4cm}} \hfill 日期：\underline{\hspace{3cm}}

    \vspace{2cm}
    {\centering\heiti\zihao{3}江苏海洋大学\\[0.5cm]}
    {\centering\heiti\zihao{3}毕业设计（论文）版权使用授权书\\[1cm]}

    {\zihao{-4}\songti
    本毕业设计（论文）作者同意学校保留并向国家有关部门或机构送交论文的复印件和电子版，允许论文被查阅和借阅。本人授权江苏海洋大学可以将本毕业设计（论文）的全部或部分内容编入有关数据库进行检索，可以采用影印、缩印或扫描等复制手段保存和汇编本毕业设计（论文）。
    }

    \vspace{2cm}
    作者签名：\underline{\hspace{4cm}} \hfill 指导教师签名：\underline{\hspace{4cm}}

    \vspace{1cm}
    日期：\underline{\hspace{3cm}} \hfill 日期：\underline{\hspace{3cm}}

    \clearpage
}

% 摘要页固定内容区 - 与手册样页对齐，但不复制说明注释
\newlength{\jou@abstractframewidth}
\setlength{\jou@abstractframewidth}{15.08cm}
\newlength{\jou@abstractframeheight}
\setlength{\jou@abstractframeheight}{22.90cm}
\newlength{\jou@abstractinnerwidth}
\setlength{\jou@abstractinnerwidth}{13.95cm}
\newlength{\jou@abstracttitlewidth}
\setlength{\jou@abstracttitlewidth}{16.00cm}
\newlength{\jou@abstractframeleft}
\setlength{\jou@abstractframeleft}{2.13cm}
\newlength{\jou@abstractframetop}
\setlength{\jou@abstractframetop}{3.86cm}
\newlength{\jou@abstracttitletop}
\setlength{\jou@abstracttitletop}{2.55cm}
\newlength{\jou@abstracttitleleft}
\setlength{\jou@abstracttitleleft}{1.66cm}

\newcommand{\jou@abstracttitleblock}[1]{%
    \begin{textblock*}{\jou@abstracttitlewidth}(\jou@abstracttitleleft,\jou@abstracttitletop)
        \centering\JOUAbstractHei\bfseries\zihao{4}#1
    \end{textblock*}%
}

\newcommand{\jou@abstractframebegin}[2]{%
    \begin{textblock*}{\jou@abstractframewidth}(\jou@abstractframeleft,\jou@abstractframetop)
    \begin{tabular}{|@{}p{\jou@abstractframewidth}@{}|}
        \hline
        \begin{minipage}[t][\jou@abstractframeheight][t]{\jou@abstractframewidth}
            \centering
            \vspace*{0.70cm}
            {#2\par}
            \vspace{0.92cm}
            \begin{minipage}[t]{\jou@abstractinnerwidth}
                \raggedright
                #1%
}

\newcommand{\jou@abstractframeend}{%
                \par
                \vfill
            \end{minipage}
        \end{minipage}\\
        \hline
    \end{tabular}%
    \end{textblock*}%
}

% 中文摘要环境
\newenvironment{cnabstract}{
    \clearpage
    \thispagestyle{frontmatterstyle}
    \mbox{}%
    \jou@abstracttitleblock{毕业设计（论文）中文摘要}
    \jou@abstractframebegin
        {\noindent{\JOUAbstractHei\bfseries\zihao{-4}摘\hspace{1em}要：}\zihao{-4}\songti}
        {\JOUAbstractHei\bfseries\zihao{4}\@title}
}{
    \jou@abstractframeend
    \null
    \clearpage
}

% 英文摘要环境
\newenvironment{enabstract}{
    \clearpage
    \thispagestyle{frontmatterstyle}
    \mbox{}%
    \jou@abstracttitleblock{毕业设计（论文）外文摘要}
    \jou@abstractframebegin
        {\noindent{\rmfamily\bfseries\zihao{-4}Abstract: }\rmfamily\zihao{-4}}
        {\rmfamily\bfseries\zihao{-4}\@entitle}
}{
    \jou@abstractframeend
    \null
    \clearpage
}

% 关键词命令
\newcommand{\cnkeywords}[1]{
    \par\vspace{0.82cm}
    \noindent{\JOUAbstractHei\bfseries\zihao{-4}关键词：}{\zihao{-4}\songti #1}
}

\newcommand{\enkeywords}[1]{
    \par\vspace{0.82cm}
    \noindent{\rmfamily\bfseries\zihao{-4}Keywords: }{\rmfamily\zihao{-4}#1}
}

\newcommand{\printsymbols}{
    \clearpage
    \thispagestyle{frontmatterstyle}
    \printnomenclature[2.5cm]
    \clearpage
}

% 目录格式
\JOUApplyBodyTocLayout

\endinput
