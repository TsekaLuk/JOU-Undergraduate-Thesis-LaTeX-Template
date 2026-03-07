# 截图指南 (Screenshot Guide)

本文档说明 README 中需要添加的截图，以及如何生成这些图片。

---

## 📸 需要的截图列表

### 1. 论文封面 (Thesis Cover Page)

**位置**: README.md "Preview" 部分

**文件名**: `docs/images/cover-preview.png`

**生成方法**:
```bash
# 编译论文
xelatex main.tex

# 使用 ImageMagick 或 Ghostscript 转换 PDF 第一页为 PNG
pdftoppm -png -f 1 -l 1 -r 150 main.pdf docs/images/cover-preview

# 或使用 macOS Preview.app
# 打开 main.pdf，导出第一页为 PNG
```

**推荐尺寸**: 800px 宽度

---

### 2. 表单模板画廊 (Form Templates Gallery)

**位置**: README.md "Preview" 部分

**文件名**: `docs/images/forms-gallery.png`

**内容**: 3-4个代表性表单的缩略图拼接

**推荐表单**:
- 选题审题表 (`topic-selection.tex`)
- 开题报告 (`proposal-science.tex`)
- 中期检查表 (`midterm-check.tex`)
- 答辩记录 (`defense-record.tex`)

**生成方法**:
```bash
# 1. 编译各个表单
cd templates/forms
xelatex topic-selection.tex
xelatex midterm-check.tex
xelatex defense-record.tex

cd ../reports
xelatex proposal-science.tex

# 2. 转换为图片
pdftoppm -png -r 100 topic-selection.pdf topic-selection
pdftoppm -png -r 100 midterm-check.pdf midterm-check
pdftoppm -png -r 100 defense-record.pdf defense-record
pdftoppm -png -r 100 proposal-science.pdf proposal-science

# 3. 使用图片编辑工具（Photoshop/GIMP/Figma）拼接为画廊
# 推荐布局: 2×2 网格，每个缩略图 400×500px
```

**推荐尺寸**: 1000px × 1200px

---

### 3. 编译流程图 (Compilation Workflow)

**位置**: README.md "Preview" 部分

**文件名**: `docs/images/workflow.png`

**内容**: 可视化编译流程

**建议工具**:
- [Excalidraw](https://excalidraw.com/)
- [draw.io](https://draw.io/)
- Figma

**流程图内容**:
```
┌─────────────────┐
│   main.tex      │
│  + chapters/    │
│  + figures/     │
│  + refs.bib     │
└────────┬────────┘
         │
         v
┌─────────────────┐
│    XeLaTeX      │
│   Compilation   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│     BibTeX      │
│  (references)   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  XeLaTeX (×2)   │
│  Final build    │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   main.pdf      │
│  (Final thesis) │
└─────────────────┘
```

**推荐尺寸**: 600px × 800px

---

### 4. 像素级对齐演示 (Pixel-Perfect Alignment Demo)

**位置**: 可选，用于突出技术亮点

**文件名**: `docs/images/alignment-demo.png`

**内容**: Word 表格 vs LaTeX 表格对比

**生成方法**:
1. 从 Word 模板导出一个表格截图
2. 从对应的 LaTeX 模板编译并截图相同表格
3. 使用对比工具（如 Photoshop 的叠加模式）显示完美对齐

**推荐尺寸**: 1200px × 600px

---

### 5. Paper2Slide 功能演示 (Paper-to-Slide Demo)

**位置**: README.md "Advanced Features" 部分或 slides/README.md

**文件名**: `docs/images/paper2slide-demo.png`

**内容**: 从论文到 PPT 的转换过程

**建议**:
- 左侧：LaTeX 论文截图
- 中间：箭头 + "banana-slides"
- 右侧：生成的 PPT 截图

**推荐尺寸**: 1200px × 400px

---

## 🎨 图片规范

### 文件格式
- **主要格式**: PNG（透明背景优先）
- **备用格式**: JPG（如果文件过大）

### 命名规范
- 使用小写字母和连字符
- 描述性命名: `cover-preview.png`, `forms-gallery.png`
- 避免中文文件名

### 尺寸建议
- **最大宽度**: 1200px
- **最小宽度**: 600px
- **DPI**: 150-300（用于 README 显示）

### 文件大小
- 单个图片 < 500KB
- 使用工具压缩（如 TinyPNG, ImageOptim）

---

## 📂 目录结构

```
docs/
├── SCREENSHOTS.md           # 本文件
└── images/
    ├── cover-preview.png    # 封面预览
    ├── forms-gallery.png    # 表单画廊
    ├── workflow.png         # 编译流程
    ├── alignment-demo.png   # 对齐演示（可选）
    └── paper2slide-demo.png # Paper2Slide 演示（可选）
```

---

## 🛠️ 推荐工具

### PDF 转图片
- **ImageMagick**: `convert -density 150 input.pdf output.png`
- **Poppler**: `pdftoppm -png -r 150 input.pdf output`
- **macOS Preview**: 打开 PDF → 文件 → 导出 → PNG

### 图片编辑
- **Figma**: 专业级，支持在线协作
- **GIMP**: 开源，功能强大
- **Photoshop**: 商业标准

### 流程图绘制
- **Excalidraw**: 手绘风格，简单易用
- **draw.io**: 专业流程图
- **Mermaid**: 代码生成流程图（可嵌入 Markdown）

### 图片压缩
- **TinyPNG**: https://tinypng.com/
- **ImageOptim** (macOS): https://imageoptim.com/
- **Squoosh**: https://squoosh.app/

---

## ✅ 检查清单

生成图片后，请确保：

- [ ] 所有图片分辨率适中（600-1200px 宽度）
- [ ] 文件大小合理（< 500KB）
- [ ] PNG 格式且无背景杂色
- [ ] 图片清晰，文字可读
- [ ] 更新 README.md 中的图片路径
- [ ] 提交到 Git 仓库

---

## 📝 更新 README

生成图片后，在 README.md 中替换占位符：

```markdown
### Thesis Cover Page
<img src="docs/images/cover-preview.png" alt="Thesis Cover" width="600"/>

### Form Templates
<img src="docs/images/forms-gallery.png" alt="Form Templates Gallery" width="800"/>

### Compilation Workflow
<img src="docs/images/workflow.png" alt="Compilation Workflow" width="600"/>
```

---

## 🎯 优先级

如果时间有限，建议按以下优先级生成：

1. **必须**: 论文封面 (`cover-preview.png`)
2. **推荐**: 表单画廊 (`forms-gallery.png`)
3. **可选**: 编译流程图 (`workflow.png`)
4. **可选**: 对齐演示 (`alignment-demo.png`)
5. **可选**: Paper2Slide 演示 (`paper2slide-demo.png`)

---

**提示**: 可以先提交 README 文本版本，之后再逐步添加图片。Overleaf 和 CTAN 都接受纯文本 README。
