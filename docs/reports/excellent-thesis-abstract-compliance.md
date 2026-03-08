# 校优摘要模板合规复核

## 基线

- 官方来源：[references/江苏海洋大学本科校级优秀毕业实习与设计（论文）摘要格式说明.doc](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/references/江苏海洋大学本科校级优秀毕业实习与设计（论文）摘要格式说明.doc)
- 模板入口：[templates/reports/excellent-thesis-abstract.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.tex)
- 版式实现：[styles/jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty)
- 共享字体策略：[styles/joufonts.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/joufonts.sty)
- 最近复核成品：[templates/reports/excellent-thesis-abstract.pdf](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.pdf)

## 结论

这份模板现在已经把此前明确发现的 4 个硬差异修掉了：
- 图表编号改为节号绑定，成品为 `图 1-1`、`表 2-1`
- 校优模板默认启用 `strictfonts`，没有官方字体就拒绝编译，不再静默回退开源字体
- 首部与标题相关空格改为按英文空格宽度测量的固定间距
- 参考文献列表改为 1.57 字符悬挂缩进

但如果严格按“Word 参数逐项字面一致”理解，仍有 3 项属于“等价实现”而不是“字面逐项复制”：
- 页面设置通过 `geometry + twoside + inner/outer` 实现对称页边距
- 双栏通过 `multicols` 和物理栏距实现，不直接使用“22.34 字符”这个 Word 单位
- 页眉距页顶通过 `geometry/headheight/headsep` 组合实现，不是 Word 的原始参数界面

## 逐条状态

1. `摘要约 3000 字、5 页以内`
状态：`结构承载，内容由作者负责`
说明：模板只提供结构，不会强制生成 3000 字内容或自动截断到 5 页；当前示例稿为 2 页。

2. `A4、上 3cm、下 2cm、左 1.7cm、右 2cm、左装订线、对称页边距`
状态：`等价实现`
说明：模板使用 `twoside + inner=1.7cm + outer=2cm + top=3cm + bottom=2cm`，对应官方意图。
位置：[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L22)

3. `中文题目 16 号黑体居中，1.25 倍行距`
状态：`已落实`
说明：入口文档使用 16pt 黑体居中，行距由样式文件统一设置为 1.25。
位置：[excellent-thesis-abstract.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.tex#L16)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L36)

4. `作者/导师同行，学院/专业同行，三英文空格，导师上标`
状态：`已落实`
说明：当前使用按正文楷体测量得到的三英文空格宽度，不再是弹性 `\hspace` 近似值。
位置：[excellent-thesis-abstract.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.tex#L19)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L55)

5. `摘  要 / 关键词 为 9.5 号，标签黑体，正文楷体，左右缩进 1.5 字符`
状态：`已落实`
说明：摘要块和关键词块都使用 9.5pt 楷体，标签为黑体；“摘  要”内部空隙改为按两英文空格宽度测量后的固定间距；左右内缩 1.5em。
位置：[excellent-thesis-abstract.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.tex#L27)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L52)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L113)

6. `正文与参考文献双栏，等栏宽，栏距 2.02 字符`
状态：`等价实现`
说明：模板使用 `multicols` 双栏，并将栏距设为 `2.02em`；这是 LaTeX 下对官方双栏意图的物理版面实现。
位置：[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L38)
[excellent-thesis-abstract.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.tex#L34)

7. `阿拉伯数字分级编号，编号与标题间两个英文空格；首页左下角教师简介`
状态：`已落实`
说明：一级、二级、三级标题的编号与标题间距都改为按两英文空格宽度测量的固定值；首页教师简介继续用 `textpos` 绝对定位实现。
位置：[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L58)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L82)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L146)

8. `一级标题 13 号黑体，二级标题 11 号黑体，三级以下 9.5 号楷体，三级标题后正文不另起段`
状态：`已落实`
说明：三级标题仍为 run-in，并把标题后正文间距也改成两英文空格宽度。
位置：[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L82)

9. `图表尽量单栏；图表标题小五号楷体加粗；文中提示如图（表）*-*所示`
状态：`已落实`
说明：图表编号现在按节重置，示例正文已渲染为 `如图 1-1 所示`、`表 2-1`；图表标题字体改为使用带加粗能力的楷体族。
位置：[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L104)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L120)
[body.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/contents/excellent-abstract/body.tex#L7)

10. `页眉居中，距页顶 2.3cm，10.5 号黑体`
状态：`等价实现`
说明：页眉内容、字号、居中方式已落实；纵向位置通过 `geometry + fancyhdr` 控制。
位置：[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L59)

11. `参考文献按学报格式，顺序编号，数量不超过 6`
状态：`结构已落实，数量由内容负责`
说明：样式使用 `gbt7714-numerical`，数量限制不在模板中硬编码。
位置：[excellent-thesis-abstract.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.tex#L47)

12. `参考文献标题 11 号黑体居中；正文小五号；悬挂缩进 1.57 字符；后接作者简介`
状态：`已落实`
说明：参考文献列表改为显式 1.57em 悬挂缩进，标题和作者简介继续保持独立块。
位置：[excellent-thesis-abstract.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.tex#L40)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L50)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L124)

13. `英文标题 16 号 Times New Roman 加粗居中；英文摘要/关键词 10.5 号 Times New Roman；标签加粗`
状态：`已落实`
说明：校优模板现在默认启用严格字体校验，缺少官方字体将直接报错，因此不再默默使用开源替代字体冒充正式稿。
位置：[excellent-thesis-abstract.tex](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/templates/reports/excellent-thesis-abstract.tex#L55)
[jouexcellentabstract.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/jouexcellentabstract.sty#L4)
[joufonts.sty](/Users/tseka_luk/Documents/江苏海洋大学个人事物工作/JOU-Undergraduate-Thesis-LaTeX-Template/styles/joufonts.sty#L948)

## 当前口径

- 如果按“成稿结构、编号、字体约束、空格规则、参考文献缩进”来验收，这份模板现在可按正式申报稿口径使用。
- 如果按“Word 对话框中的每个参数值和实现路径都逐字逐项复制”来验收，规则 2、6、10 仍应视为 LaTeX 等价实现，而不是 Word 原生命令复刻。
