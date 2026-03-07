# 表格使用示例 - 像素级对齐

## 基本三线表（最常用）

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

## 定宽列表格（精确控制列宽）

```latex
\begin{table}[htbp]
    \centering
    \caption{系统功能模块说明}
    \label{tab:modules}
    \begin{tabular}{C{2cm}L{4cm}L{6cm}}
        \toprule
        模块名称 & 主要功能 & 技术实现 \\
        \midrule
        数据采集 & 从传感器获取数据 & 使用Python的serial库读取串口数据 \\
        数据处理 & 对原始数据进行预处理 & 使用NumPy进行数据标准化和降维 \\
        模型训练 & 训练深度学习模型 & 基于PyTorch实现CNN网络 \\
        \bottomrule
    \end{tabular}
\end{table}
```

**列类型说明**：
- `C{宽度}`: 居中对齐的定宽列
- `L{宽度}`: 左对齐的定宽列
- `R{宽度}`: 右对齐的定宽列
- `c/l/r`: 自动宽度的居中/左对齐/右对齐列

## 跨行单元格

```latex
\begin{table}[htbp]
    \centering
    \caption{不同算法性能对比}
    \label{tab:multirow}
    \begin{tabular}{ccccc}
        \toprule
        \multirow{2}{*}{算法} & \multicolumn{2}{c}{训练集} & \multicolumn{2}{c}{测试集} \\
        \cmidrule(lr){2-3} \cmidrule(lr){4-5}
        & 准确率 & 损失 & 准确率 & 损失 \\
        \midrule
        算法A & 95.2 & 0.12 & 92.1 & 0.18 \\
        算法B & 96.5 & 0.09 & 93.4 & 0.15 \\
        本文算法 & 97.8 & 0.07 & 94.9 & 0.11 \\
        \bottomrule
    \end{tabular}
\end{table}
```

## 跨页长表格

```latex
\begin{longtable}{clcc}
    \caption{详细实验数据} \label{tab:long} \\
    \toprule
    序号 & 样本名称 & 测试值 & 标准值 \\
    \midrule
    \endfirsthead

    \multicolumn{4}{c}{续表 \thetable} \\
    \toprule
    序号 & 样本名称 & 测试值 & 标准值 \\
    \midrule
    \endhead

    \bottomrule
    \endfoot

    \bottomrule
    \endlastfoot

    1 & 样本A & 95.2 & 95.0 \\
    2 & 样本B & 96.5 & 96.0 \\
    % ... 更多数据行
    100 & 样本Z & 94.8 & 95.0 \\
\end{longtable}
```

## 单元格内换行

```latex
\begin{table}[htbp]
    \centering
    \caption{研究阶段划分}
    \label{tab:makecell}
    \begin{tabular}{cL{8cm}}
        \toprule
        阶段 & 主要工作内容 \\
        \midrule
        第一阶段 & \makecell[l]{
            1. 文献调研和需求分析 \\
            2. 确定技术路线 \\
            3. 搭建实验环境
        } \\
        第二阶段 & \makecell[l]{
            1. 算法设计与实现 \\
            2. 模型训练与优化 \\
            3. 性能测试与评估
        } \\
        \bottomrule
    \end{tabular}
\end{table}
```

## 精确对齐技巧

### 1. 数字右对齐（小数点对齐）

使用 `siunitx` 宏包（需要在导言区添加 `\usepackage{siunitx}`）：

```latex
\begin{tabular}{S[table-format=2.1]S[table-format=2.1]}
    \toprule
    {准确率(\%)} & {F1值} \\
    \midrule
    95.2 & 93.5 \\
    96.8 & 95.1 \\
    100.0 & 98.9 \\
    \bottomrule
\end{tabular}
```

### 2. 表格宽度控制

固定总宽度：

```latex
\begin{tabularx}{\textwidth}{lXr}
    \toprule
    左列 & 中间可伸缩列 & 右列 \\
    \midrule
    数据1 & 这是一段较长的文字，会自动换行以适应表格宽度 & 100 \\
    \bottomrule
\end{tabularx}
```

### 3. 表格线条样式

```latex
% 局部调整线宽
\toprule[1.5pt]  % 加粗顶线
\midrule[0.5pt]  % 细中线
\bottomrule[1.5pt]  % 加粗底线

% 部分列的线
\cmidrule(lr){2-4}  % 第2到第4列的中线，左右留白
```

## 常见问题

### Q: 表格太宽超出页面？

**方法1**: 使用 `tabularx` 并设置可伸缩列：
```latex
\begin{tabularx}{\textwidth}{lXXr}
```

**方法2**: 缩小字号：
```latex
\begin{table}[htbp]
    \centering
    \small  % 或 \footnotesize
    \caption{...}
    ...
\end{table}
```

**方法3**: 横向放置：
```latex
\usepackage{rotating}

\begin{sidewaystable}
    ...
\end{sidewaystable}
```

### Q: 如何调整表格内文字的垂直对齐？

```latex
% 使用 m{宽度} 代替 p{宽度} 实现垂直居中
\begin{tabular}{m{2cm}m{4cm}m{4cm}}
```

### Q: 表格标题如何实现多行？

```latex
\caption{这是第一行标题 \\
         这是第二行标题}
```

## 精确参数说明

模板中已配置的精确参数：

| 参数 | 值 | 说明 |
|------|-----|------|
| `\heavyrulewidth` | 1.2pt | 粗线宽度（顶线和底线） |
| `\lightrulewidth` | 0.6pt | 细线宽度（中线） |
| `\tabcolsep` | 6pt | 列间距 |
| `\arraystretch` | 1.2 | 行高倍数 |

这些参数已经过精确调整，以匹配Word文档中表格的默认样式。
