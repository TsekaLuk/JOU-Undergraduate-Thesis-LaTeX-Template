# 资源文件说明

## 📸 从Word文档提取的图片

所有图片均从官方《江苏海洋大学2026届毕业实习与设计（论文）工作手册》无损提取。

### 1. jou-logo-full.png
**用途**: 封面主logo
**尺寸**: 1237 × 873 px
**说明**: 学校校徽+校名组合，最完整的官方logo
**Word中原始宽度**: 5.229英寸 (≈ 13.28cm)

**使用位置**:
- ✅ 封面顶部（已配置）
- 可选：PPT首页

### 2. jou-name-large.png
**用途**: 学校名称横版（大）
**尺寸**: 798 × 160 px
**格式**: 8-bit colormap, interlaced
**Word中原始宽度**: 3.625英寸 (≈ 9.21cm)

**使用位置**:
- 各类表格页眉
- 文档页眉（如需图片）

### 3. jou-name-small.png
**用途**: 学校名称横版（小）
**尺寸**: 433 × 99 px
**格式**: 8-bit colormap, interlaced
**Word中原始宽度**: 1.96875英寸 (≈ 5.00cm)

**使用位置**:
- 小型表格页眉
- 页脚标识

### 4. jou-name-large-rgba.png
**用途**: 学校名称横版（RGBA版本）
**尺寸**: 798 × 160 px
**格式**: 8-bit/color RGBA, non-interlaced
**说明**: 与jou-name-large.png内容相同，但支持透明度

**使用位置**:
- 需要透明背景的场景
- 叠加在图片上

## 🎨 Logo使用规范

### 在LaTeX中使用

#### 封面logo（已自动配置）
```latex
% 在 jouthesis.cls 中已配置
\includegraphics[width=13.28cm]{figures/jou-logo-full.png}
```

#### 自定义使用

```latex
% 大logo - 用于封面或独立页
\includegraphics[width=13cm]{figures/jou-logo-full.png}

% 横版校名 - 用于页眉
\includegraphics[width=9cm]{figures/jou-name-large.png}

% 小版校名 - 用于页脚或小型标识
\includegraphics[width=5cm]{figures/jou-name-small.png}

% 透明版本 - 用于叠加
\includegraphics[width=9cm]{figures/jou-name-large-rgba.png}
```

### 尺寸建议

| 场景 | 推荐图片 | 推荐宽度 |
|------|----------|----------|
| A4封面 | jou-logo-full.png | 12-14cm |
| 页眉 | jou-name-large.png | 8-10cm |
| PPT标题页 | jou-logo-full.png | 10-12cm |
| PPT普通页 | jou-name-small.png | 4-6cm |
| 海报 | jou-logo-full.png | 15-20cm |

## 📐 精确尺寸对照

### Word原始尺寸（从XML提取）

```xml
<!-- jou-logo-full.png -->
<wp:extent cx="3314700" cy="666750"/>
<!-- 转换: 3314700 EMU = 13.28 cm -->

<!-- jou-name-large.png -->
宽度: 3.625 英寸 = 9.21 cm

<!-- jou-name-small.png -->
宽度: 1.96875 英寸 = 5.00 cm
```

### LaTeX中的精确复现

```latex
% 完全匹配Word中的显示尺寸
\includegraphics[width=13.28cm]{figures/jou-logo-full.png}  % 封面logo
\includegraphics[width=9.21cm]{figures/jou-name-large.png}  % 大横版
\includegraphics[width=5.00cm]{figures/jou-name-small.png}  % 小横版
```

## 🔍 图片质量

所有图片均为：
- ✅ **无损提取**: 直接从Word文档的.zip结构中提取
- ✅ **原始格式**: PNG格式，保留完整色彩信息
- ✅ **官方资源**: 来自学校官方工作手册
- ✅ **高清晰度**: 足够用于打印和高分辨率显示

## 📋 文件完整性验证

```bash
# 检查图片文件
ls -lh figures/*.png

# 预期输出:
# -rw-r--r--  67K  jou-logo-full.png
# -rw-r--r--  20K  jou-name-large-rgba.png
# -rw-r--r--  7.0K jou-name-large.png
# -rw-r--r--  3.0K jou-name-small.png
```

## 🎯 使用示例

### 示例1: 自定义封面页
```latex
\begin{titlepage}
    \centering
    \vspace*{2cm}
    \includegraphics[width=13cm]{figures/jou-logo-full.png}\\[2cm]
    {\Huge\bfseries 论文标题}\\[1cm]
    {\Large 学生姓名}\\[5cm]
    {\large \today}
\end{titlepage}
```

### 示例2: 页眉使用logo
```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[C]{\includegraphics[height=0.8cm]{figures/jou-name-small.png}}
```

### 示例3: 在表格中使用
```latex
\begin{table}[htbp]
    \centering
    \includegraphics[width=5cm]{figures/jou-name-small.png}\\[0.5cm]
    \caption{实验结果}
    \begin{tabular}{ccc}
        ...
    \end{tabular}
\end{table}
```

## 📦 导出和分享

如需单独导出logo用于其他用途：

```bash
# 复制到桌面
cp figures/jou-logo-full.png ~/Desktop/

# 转换为其他格式（需要ImageMagick）
convert figures/jou-logo-full.png ~/Desktop/jou-logo.jpg
convert figures/jou-logo-full.png ~/Desktop/jou-logo.pdf
```

## ⚠️ 版权说明

这些图片资源属于江苏海洋大学，仅限用于：
- ✅ 本校学生的毕业设计（论文）
- ✅ 学术交流和展示
- ✅ 课程作业和报告

请勿用于：
- ❌ 商业用途
- ❌ 非学术性宣传
- ❌ 未经授权的对外发布

## 🔧 故障排查

### Q: Logo显示不出来？

**检查路径**:
```latex
% 确保路径正确
\includegraphics[width=13cm]{figures/jou-logo-full.png}
```

**检查文件**:
```bash
ls figures/jou-logo-full.png
# 应该显示文件信息
```

### Q: Logo显示模糊？

**不要过度放大**:
```latex
% ❌ 错误：宽度超过20cm会模糊
\includegraphics[width=25cm]{figures/jou-logo-full.png}

% ✅ 正确：保持在合理范围
\includegraphics[width=13cm]{figures/jou-logo-full.png}
```

### Q: 编译报错找不到图片？

**添加graphicx包**:
```latex
\usepackage{graphicx}
```

**设置图片路径**:
```latex
\graphicspath{{figures/}}
% 然后可以直接使用文件名
\includegraphics[width=13cm]{jou-logo-full.png}
```

## 📚 相关文档

- [README.md](README.md) - 项目总览
- [USAGE.md](USAGE.md) - 使用指南
- [TABLE-EXAMPLES.md](TABLE-EXAMPLES.md) - 表格示例
