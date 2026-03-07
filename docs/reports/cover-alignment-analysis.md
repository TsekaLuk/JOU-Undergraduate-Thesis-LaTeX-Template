# 封面对齐深度分析

## 视觉对比结果

### 对比指标
- **mean_abs_diff**: 7.268（平均像素差异）
- **rms_diff**: 39.168（均方根差异）
- **视觉回归测试**: ✅ PASS（结构在容差范围内）

### Diff 图像洞察

通过分析 `thesis-cover-overlay.png`、`thesis-cover-diff.png` 和 `thesis-cover-checker.png`，发现以下关键问题：

## 🔍 核心问题定位

### 1. 字体加粗不一致 ⚠️ CRITICAL

#### 参考 PDF 实际使用的字体（第39页）

```
pdffonts 输出：
- HYZhongHeiKW          ← "本科毕业设计（论文）"大标题
- STKaiti               ← 中文题目（通过 AutoFakeBold 模拟加粗）
- TimesNewRomanPS-BoldMT ← English Title（真实 Bold 字体）
- HYShuSongErKW         ← 信息填写区
```

#### 当前 LaTeX 模板的问题

**问题 A：双重加粗**

```latex
% styles/jouthesis.cls:341
{\JOUCoverKai\bfseries\zihao{2}\@title\par}
     ↑           ↑
     |           └─ 额外的 \bfseries 指令
     └─ 已定义为 [AutoFakeBold=2.2]
```

`\JOUCoverKai` 在 `joufonts.sty:314/333/349` 中定义时已经包含 `AutoFakeBold=2.2`：
```latex
\newCJKfontfamily\JOUCoverKai{HYKaiTiKW}[AutoFakeBold=2.2]
```

**再叠加 `\bfseries` 导致过度加粗**，产生的笔画粗细与参考 PDF 不一致。

**问题 B："本科毕业设计（论文）"字体错误**

```latex
% styles/jouthesis.cls:338
{\JOUHei\bfseries\zihao{2}本\hspace{1em}科...}
```

- 当前使用：`\JOUHei`（黑体） + `\bfseries`
- 参考 PDF：`HYZhongHeiKW`（汉仪中黑）

黑体本身已经是粗体风格，再加 `\bfseries` 可能导致过粗。

**问题 C：English Title 字体未指定**

```latex
% styles/jouthesis.cls:344
{\bfseries\fontsize{22pt}{28pt}\selectfont \@entitle\par}
```

- 没有显式指定 Times New Roman
- 可能使用默认拉丁字体（不一定是 Times New Roman）

### 2. 字距微调差异

**"本科毕业设计（论文）"字距**

当前代码（jouthesis.cls:338）：
```latex
本\hspace{1em}科\hspace{1em}毕\hspace{1em}业\hspace{1em}设\hspace{0.5em}计\hspace{0.5em}（论\hspace{0.5em}文）
```

从 diff 图可见，每个字符都有白色光晕，说明：
- 字符位置略有偏移
- `\hspace` 值可能需要微调
- 不同字体的字符宽度不同，导致整体对齐偏移

### 3. 表格列宽对齐

当前表格定义（jouthesis.cls:348）：
```latex
\begin{tabular}{@{}p{3.324cm}p{3.676cm}p{2.228cm}p{3.769cm}@{}}
```

**Checker 图显示**：信息区文字有"断裂"效果，表明：
- 下划线长度可能不精确
- 列宽总和: 3.324 + 3.676 + 2.228 + 3.769 = 12.997cm
- 需要对比参考 PDF 的实际列宽

### 4. 字体权重不匹配

**参考 PDF 的字体选择逻辑**：
- **HYZhongHeiKW**（汉仪中黑）：本身就是粗黑体，无需加粗
- **STKaiti** + AutoFakeBold：楷体通过算法模拟加粗
- **TimesNewRomanPS-BoldMT**：使用真实的 Bold 字重字体文件

**当前模板的加粗逻辑**：
- 使用 `\bfseries` 全局加粗
- 可能导致字重不一致

---

## 🎯 优化方案

### 方案 A：移除冗余加粗指令（推荐）

#### 1. 修复中文题目双重加粗

**修改 `styles/jouthesis.cls:341`**：
```latex
% BEFORE
{\JOUCoverKai\bfseries\zihao{2}\@title\par}

% AFTER（移除 \bfseries）
{\JOUCoverKai\zihao{2}\@title\par}
```

**原因**：`\JOUCoverKai` 已经定义了 `AutoFakeBold=2.2`，无需额外加粗。

#### 2. 修复"本科毕业设计（论文）"加粗

**修改 `styles/jouthesis.cls:338`**：
```latex
% BEFORE
{\JOUHei\bfseries\zihao{2}本\hspace{1em}科...}

% AFTER（移除 \bfseries，黑体本身已经很粗）
{\JOUHei\zihao{2}本\hspace{1em}科...}
```

#### 3. 明确指定 English Title 字体

**修改 `styles/jouthesis.cls:344`**：
```latex
% BEFORE
{\bfseries\fontsize{22pt}{28pt}\selectfont \@entitle\par}

% AFTER（明确使用 Times New Roman Bold）
{\fontspec{Times New Roman Bold}\fontsize{22pt}{28pt}\selectfont \@entitle\par}
```

或者定义一个新的字体命令：
```latex
% 在 joufonts.sty 中添加
\newfontfamily\JOUTimesRomanBold{Times New Roman Bold}

% 在 jouthesis.cls 中使用
{\JOUTimesRomanBold\fontsize{22pt}{28pt}\selectfont \@entitle\par}
```

#### 4. 修复表格标签加粗

**修改 `styles/jouthesis.cls:349-361`**：
```latex
% BEFORE
{\JOUCoverKai\bfseries 学\hspace{1.6em}院：}

% AFTER（保留 \bfseries 作为标签强调，但考虑移除）
{\JOUCoverKai 学\hspace{1.6em}院：}
```

**或者**：如果参考 PDF 标签确实加粗，保留 `\bfseries`，但需要验证效果。

### 方案 B：调整 AutoFakeBold 参数

如果方案 A 导致楷体太细，可以微调 `AutoFakeBold` 参数：

**修改 `styles/joufonts.sty:314/333/349`**：
```latex
% 尝试不同的 AutoFakeBold 值
\newCJKfontfamily\JOUCoverKai{HYKaiTiKW}[AutoFakeBold=1.8]  % 降低加粗程度
\newCJKfontfamily\JOUCoverKai{HYKaiTiKW}[AutoFakeBold=2.5]  % 增加加粗程度
```

### 方案 C：使用真实的 Bold 字体文件（理想方案）

如果能获取到 HYKaiTiKW 的 Bold 版本：
```latex
\newCJKfontfamily\JOUCoverKai{HYKaiTiKW}[
    BoldFont=HYKaiTiKW-Bold  % 使用真实的加粗字体
]
```

---

## 📊 对齐度预期

### 当前状态
- **字体模式**: system-licensed（macOS）
- **对齐度**: 95-98%
- **主要差异**: 字体加粗、字距、字体 metrics

### 优化后预期
| 优化项 | 对齐度提升 |
|--------|-----------|
| 移除双重加粗 | +1-2% |
| 修正字体选择 | +0.5-1% |
| 微调字距 | +0.5-1% |
| **总计** | **97-99%** |

### 达到 99%+ 对齐的必要条件
1. ✅ 安装 WPS 实际字体（HYKaiTiKW, HYShuSongErKW, HYZhongHeiKW）
2. ✅ 移除双重加粗
3. ✅ 精确匹配字距和列宽
4. ⚠️ 使用完全相同的 PDF 渲染器（XeLaTeX vs WPS）

---

## 🔧 验证流程

实施优化后，运行以下命令验证：

```bash
# 1. 重新编译
make clean
make

# 2. 生成对比图
python3 scripts/generate_cover_diff.py

# 3. 运行视觉测试
python3 tests/test_cover_alignment.py

# 4. 查看对比图
open docs/assets/thesis-cover-overlay-focus.png
open docs/assets/thesis-cover-diff-focus.png
```

**期望结果**：
- `mean_abs_diff < 5.0`（当前 7.268）
- `rms_diff < 30.0`（当前 39.168）
- 视觉上无明显重影

---

## 📝 总结

**根本原因**：
1. 双重加粗（`AutoFakeBold` + `\bfseries`）导致字体粗细不匹配
2. 字体选择不完全一致（需要 WPS 字体）
3. 字距和列宽微调差异

**优先级优化**：
1. 🔴 **HIGH**: 移除冗余的 `\bfseries` 指令（立即见效）
2. 🟡 **MEDIUM**: 明确指定 Times New Roman Bold
3. 🟢 **LOW**: 微调字距和列宽（需要反复迭代）

**最终对齐策略**：
- 短期：通过代码优化达到 97-98% 对齐度
- 长期：鼓励用户安装 WPS 字体达到 99%+ 对齐度
