\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{jouthesis}[2026/03/07 Jiangsu Ocean University Undergraduate Thesis Template]

% 基于ctexbook类，设置A4纸，单面打印
\LoadClass[a4paper,zihao=-4,openany,oneside]{ctexbook}

% 必要的宏包
\RequirePackage{geometry}      % 页面设置
\RequirePackage{fancyhdr}      % 页眉页脚
\RequirePackage{titletoc}      % 目录格式
\RequirePackage{graphicx}      % 插图
\RequirePackage{amsmath}       % 数学公式
\RequirePackage{amssymb}       % 数学符号
\RequirePackage{booktabs}      % 三线表
\RequirePackage{longtable}     % 跨页表格
\RequirePackage{caption}       % 图表标题
\RequirePackage{subcaption}    % 子图
\RequirePackage{hyperref}      % 超链接
\RequirePackage{xcolor}        % 颜色
\RequirePackage{enumerate}     % 列表
\RequirePackage{setspace}      % 行距
\RequirePackage{indentfirst}   % 首行缩进

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

% 页眉页脚设置
\pagestyle{fancy}
\fancyhf{}
% 页眉: 五号楷体_GB2312
\fancyhead[C]{\zihao{5}\kaishu 江苏海洋大学本科生毕业论文}
% 页脚: 页码居中
\fancyfoot[C]{\zihao{5}\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% 章节标题格式 - 严格按照要求
\ctexset{
    % 一级标题: 小三号黑体，段前段后0.5行
    chapter={
        format={\centering\heiti\zihao{-3}},
        nameformat={},
        titleformat={},
        number=\arabic{chapter},
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

% 超链接设置
\hypersetup{
    colorlinks=true,
    linkcolor=black,
    citecolor=black,
    urlcolor=blue,
    bookmarksnumbered=true,
    pdfstartview=FitH
}

% 论文信息变量
\newcommand{\studentid}[1]{\def\@studentid{#1}}
\newcommand{\major}[1]{\def\@major{#1}}
\newcommand{\class}[1]{\def\@class{#1}}
\newcommand{\supervisor}[1]{\def\@supervisor{#1}}
\newcommand{\entitle}[1]{\def\@entitle{#1}}

% 封面命令
\newcommand{\makecover}{
    \begin{titlepage}
        \centering
        \vspace*{1cm}

        % 学校logo（如果有的话，请放在figures目录）
        % \includegraphics[width=9cm]{figures/jou-logo.png}\\[1cm]

        {\heiti\zihao{-1} 江苏海洋大学}\\[0.5cm]
        {\heiti\zihao{2} \textbf{本科毕业设计（论文）}}\\[3cm]

        % 中文标题: 二号楷体加粗
        {\heiti\zihao{2}\textbf{\@title}}\\[0.5cm]

        % 英文标题: 二号Times New Roman加粗
        {\fontsize{22pt}{\baselineskip}\selectfont\textbf{\@entitle}}\\[3cm]

        % 信息表格: 四号楷体
        {\kaishu\zihao{4}
            \begin{tabular}{rl}
                学\hspace{2em}院： & \underline{\makebox[8cm][c]{\@major}} \\[0.8cm]
                专业班级： & \underline{\makebox[8cm][c]{\@class}} \\[0.8cm]
                学生姓名： & \underline{\makebox[8cm][c]{\@author}} \\[0.8cm]
                学\hspace{2em}号： & \underline{\makebox[8cm][c]{\@studentid}} \\[0.8cm]
                指导教师： & \underline{\makebox[8cm][c]{\@supervisor}} \\[0.8cm]
            \end{tabular}
        }

        \vfill
        {\songti\zihao{4} \@date}
    \end{titlepage}
    \clearpage

    % 原创性声明页
    \thispagestyle{empty}
    \vspace*{2cm}
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
    \thispagestyle{plain}
    % 标题: 四号黑体居中，前空一行，段前段后0.5行
    \vspace*{\baselineskip}
    {\centering\heiti\zihao{4}\textbf{\@title}\\[\baselineskip]}
    % "摘要"二字: 小四号黑体顶格
    {\heiti\zihao{-4}\textbf{摘\hspace{1em}要：}}
    % 正文: 小四号宋体
    \zihao{-4}\songti
}{
    \clearpage
}

% 英文摘要环境
\newenvironment{enabstract}{
    \clearpage
    \thispagestyle{plain}
    % 标题: 四号Times New Roman加粗居中，前空一行，段前段后0.5行
    \vspace*{\baselineskip}
    {\centering\zihao{4}\textbf{\@entitle}\\[\baselineskip]}
    % "Abstract": 小四号加粗顶格
    {\zihao{-4}\textbf{Abstract: }}
    % 正文: 小四号Times New Roman
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

% 目录格式
\renewcommand{\contentsname}{目\hspace{2em}录}
\titlecontents{chapter}[0pt]{\songti\zihao{-4}}
    {\thecontentslabel\hspace{1em}}{}
    {\titlerule*[0.5pc]{.}\contentspage}
\titlecontents{section}[2em]{\songti\zihao{-4}}
    {\thecontentslabel\hspace{1em}}{}
    {\titlerule*[0.5pc]{.}\contentspage}

\endinput
