#!/bin/bash
# 打包脚本 - 准备 Overleaf 和 CTAN 发布包

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION=$(grep "ProvidesClass{jouthesis}" "$PROJECT_ROOT/styles/jouthesis.cls" | sed -n 's/.*\[\([0-9]\{4\}\/[0-9]\{2\}\/[0-9]\{2\}\).*/\1/p' | tr '/' '-')
DIST_DIR="$PROJECT_ROOT/dist"
TEMP_DIR="$PROJECT_ROOT/tmp/packaging"
REPO_URL="$(git -C "$PROJECT_ROOT" remote get-url origin 2>/dev/null || echo "https://github.com/TsekaLuk/JOU-Undergraduate-Thesis-LaTeX-Template.git")"
MAINTAINER_NAME="${CTAN_MAINTAINER_NAME:-$(git -C "$PROJECT_ROOT" config user.name 2>/dev/null || echo '[Your Name]')}"
MAINTAINER_EMAIL="${CTAN_MAINTAINER_EMAIL:-$(git -C "$PROJECT_ROOT" config user.email 2>/dev/null || echo 'your.email@example.com')}"

echo "=========================================="
echo "JOU 本科论文模板打包脚本"
echo "版本: $VERSION"
echo "=========================================="

# 清理旧的打包目录
rm -rf "$DIST_DIR" "$TEMP_DIR"
mkdir -p "$DIST_DIR" "$TEMP_DIR"

# ==========================================
# 1. Overleaf 上传包
# ==========================================
echo ""
echo "==> 准备 Overleaf 上传包..."

OVERLEAF_DIR="$TEMP_DIR/jouthesis-overleaf"
mkdir -p "$OVERLEAF_DIR"

# 复制核心文件
cp "$PROJECT_ROOT"/main.tex "$OVERLEAF_DIR/"
cp "$PROJECT_ROOT"/LICENSE "$OVERLEAF_DIR/"
cp "$PROJECT_ROOT"/README.md "$OVERLEAF_DIR/"
cp "$PROJECT_ROOT"/README_EN.md "$OVERLEAF_DIR/"
cp "$PROJECT_ROOT"/docs/guides/usage.md "$OVERLEAF_DIR/USAGE.md"

# 复制目录
cp -r "$PROJECT_ROOT"/styles "$OVERLEAF_DIR/"
cp -r "$PROJECT_ROOT"/contents "$OVERLEAF_DIR/"
cp -r "$PROJECT_ROOT"/figures "$OVERLEAF_DIR/"
cp -r "$PROJECT_ROOT"/fonts "$OVERLEAF_DIR/"
mkdir -p "$OVERLEAF_DIR"/references
cp "$PROJECT_ROOT"/references/refs.bib "$OVERLEAF_DIR"/references/

# 只保留 opensource 字体（Overleaf 不能使用 proprietary）
rm -rf "$OVERLEAF_DIR"/fonts/proprietary
mkdir -p "$OVERLEAF_DIR"/fonts/proprietary
echo "# 说明：Overleaf 环境请使用 fonts/opensource/ 中的字体" > "$OVERLEAF_DIR"/fonts/proprietary/README.md

# 清理编译残留，避免上传无关中间文件
find "$OVERLEAF_DIR"/contents -type f \( -name '*.aux' -o -name '*.log' -o -name '*.bbl' -o -name '*.blg' \) -delete

# 创建 latexmkrc（Overleaf 专用配置）
cat > "$OVERLEAF_DIR/.latexmkrc" <<'EOF'
# Overleaf latexmkrc 配置
$pdf_mode = 5;  # xelatex
$postscript_mode = $dvi_mode = 0;
$xelatex = 'xelatex -interaction=nonstopmode -file-line-error %O %S';
$clean_ext = 'aux bbl blg fdb_latexmk fls log out synctex.gz toc lof lot';
EOF

# 打包 Overleaf zip
cd "$TEMP_DIR"
zip -r "$DIST_DIR/jouthesis-overleaf-${VERSION}.zip" jouthesis-overleaf/ -x "*.DS_Store" "*.git*"
echo "✓ Overleaf 包已生成: $DIST_DIR/jouthesis-overleaf-${VERSION}.zip"

# ==========================================
# 2. CTAN 提交包
# ==========================================
echo ""
echo "==> 准备 CTAN 提交包..."

CTAN_DIR="$TEMP_DIR/jouthesis"
mkdir -p "$CTAN_DIR"

# CTAN 标准目录结构
mkdir -p "$CTAN_DIR"/{tex,doc,source}

# tex/ - 样式文件
cp "$PROJECT_ROOT"/styles/*.cls "$CTAN_DIR/tex/"
cp "$PROJECT_ROOT"/styles/*.sty "$CTAN_DIR/tex/"

# doc/ - 文档和示例
mkdir -p "$CTAN_DIR/doc/examples"
mkdir -p "$CTAN_DIR/doc/figures"
cp "$PROJECT_ROOT"/README.md "$CTAN_DIR/doc/"
cp "$PROJECT_ROOT"/README_EN.md "$CTAN_DIR/doc/"
cp "$PROJECT_ROOT"/LICENSE "$CTAN_DIR/doc/"
cp "$PROJECT_ROOT"/docs/guides/usage.md "$CTAN_DIR/doc/USAGE.md"
cp "$PROJECT_ROOT"/main.tex "$CTAN_DIR/doc/examples/"
mkdir -p "$CTAN_DIR/doc/examples/contents/chapters"
mkdir -p "$CTAN_DIR/doc/examples/contents/appendices"
cp "$PROJECT_ROOT"/contents/acknowledgements.tex "$CTAN_DIR/doc/examples/contents/"
cp "$PROJECT_ROOT"/contents/chapters/*.tex "$CTAN_DIR/doc/examples/contents/chapters/"
cp "$PROJECT_ROOT"/contents/appendices/*.tex "$CTAN_DIR/doc/examples/contents/appendices/"
mkdir -p "$CTAN_DIR/doc/examples/references"
cp "$PROJECT_ROOT"/references/refs.bib "$CTAN_DIR/doc/examples/references/"
cp "$PROJECT_ROOT"/figures/* "$CTAN_DIR/doc/figures/"

# 创建 README（CTAN 特殊格式）
cat > "$CTAN_DIR/README" <<EOF
JOU Undergraduate Thesis LaTeX Template
========================================

Version: $VERSION
License: LPPL 1.3c

This package provides a LaTeX template for undergraduate thesis at Jiangsu Ocean University (JOU).

Features:
- Cross-platform font support (Linux, macOS, Windows)
- Pixel-perfect alignment with official handbook
- 18 supplementary templates included
- Open source font fallback

Installation:
1. Copy files from tex/ to your local TEXMF tree
2. Run 'texhash' to update the filename database

Documentation:
- README.md: Full documentation (Chinese)
- README_EN.md: English documentation
- USAGE.md: User guide

For more information, visit:
${REPO_URL}

Maintainer: ${MAINTAINER_NAME}
EOF

# 打包 CTAN TDS zip
cd "$TEMP_DIR"
zip -r "$DIST_DIR/jouthesis-ctan-${VERSION}.zip" jouthesis/ -x "*.DS_Store" "*.git*"
echo "✓ CTAN 包已生成: $DIST_DIR/jouthesis-ctan-${VERSION}.zip"

# ==========================================
# 3. 环境一致性检查配置
# ==========================================
echo ""
echo "==> 生成环境一致性检查配置..."

cat > "$DIST_DIR/environment-check.yml" <<'EOF'
# 环境一致性检查配置
# 用于 CI/CD 和本地验证

name: JOU Thesis Environment Check

texlive:
  minimum_version: "2020"
  required_packages:
    - xetex
    - ctex
    - fontspec
    - geometry
    - fancyhdr
    - titletoc
    - graphicx
    - amsmath
    - natbib
    - hyperref
    - cleveref
    - caption
    - subcaption
    - booktabs
    - tabularx
    - multirow
    - longtable
    - algorithm
    - algpseudocode
    - listings
    - xcolor

fonts:
  required:
    - "Times New Roman (or Tinos fallback)"
    - "SimSun/STSong (or Noto Serif CJK fallback)"
    - "KaiTi/STKaiti (or LXGW WenKai fallback)"
  optional:
    - "HYKaiTiKW (WPS exact alignment)"
    - "HYShuSongErKW"
    - "HYZhongHeiKW"

tools:
  required:
    - xelatex
    - bibtex
    - makeindex
  optional:
    - latexmk
    - pdfinfo (Poppler)
    - pdftoppm (Poppler)

compilation:
  commands:
    - "xelatex main.tex"
    - "bibtex main"
    - "xelatex main.tex"
    - "xelatex main.tex"
  alternative:
    - "latexmk -xelatex main.tex"

validation:
  checks:
    - "PDF generated successfully"
    - "All fonts embedded"
    - "Page count matches expected (16 pages)"
    - "Cross-references resolved"
    - "Bibliography compiled"
    - "No undefined references"
EOF

echo "✓ 环境检查配置已生成: $DIST_DIR/environment-check.yml"

# ==========================================
# 4. 生成上传清单
# ==========================================
cat > "$DIST_DIR/UPLOAD-CHECKLIST.md" <<EOF
# 上传清单

## Overleaf 上传步骤

### 方法 1: 直接上传 ZIP
1. 登录 Overleaf (https://www.overleaf.com)
2. 点击 "New Project" → "Upload Project"
3. 上传 \`jouthesis-overleaf-${VERSION}.zip\`
4. 等待解压完成
5. 验证编译成功

### 方法 2: 从 GitHub 导入
1. 登录 Overleaf
2. 点击 "New Project" → "Import from GitHub"
3. 授权访问 GitHub 仓库
4. 选择 JOU-Undergraduate-Thesis-LaTeX-Template
5. 等待导入完成

### Overleaf 环境配置
- 编译器: XeLaTeX
- TeX Live 版本: 2024 (推荐最新)
- 主文档: main.tex

### 验证清单
- [ ] 编译成功（无错误）
- [ ] 封面正确显示
- [ ] 中英文字体正确
- [ ] 所有章节都能看到
- [ ] 图表正常显示
- [ ] 参考文献正确生成

---

## CTAN 提交步骤

### 1. 准备提交材料
- [x] 打包文件: \`jouthesis-ctan-${VERSION}.zip\`
- [ ] 确认 LICENSE 文件（LPPL 1.3c）
- [ ] 确认 README 文件
- [ ] 确认文档完整性

### 2. CTAN 上传
访问: https://www.ctan.org/upload

#### 必填字段
- **Package name**: jouthesis
- **Version**: ${VERSION}
- **Author**: ${MAINTAINER_NAME} <${MAINTAINER_EMAIL}>
- **License**: LPPL 1.3c
- **Summary**: LaTeX template for Jiangsu Ocean University undergraduate thesis
- **Announcement**: [发布说明]
- **Note to CTAN team**: This is the official LaTeX template for undergraduate thesis at Jiangsu Ocean University, China.

#### 上传文件
1. 上传 \`jouthesis-ctan-${VERSION}.zip\`
2. 确认 TDS 结构正确
3. 提交审核

### 3. CTAN 审核
- 审核周期: 通常 1-2 周
- 邮件通知: 会收到确认邮件
- 发布后: 包会出现在 https://ctan.org/pkg/jouthesis

### CTAN 包结构验证
\`\`\`
jouthesis/
├── README              # CTAN 格式简介
├── tex/                # 样式文件
│   ├── jouthesis.cls
│   ├── joufonts.sty
│   └── jouhandbook.sty
├── doc/                # 文档
│   ├── README.md
│   ├── README_EN.md
│   ├── USAGE.md
│   ├── LICENSE
│   ├── examples/       # 示例
│   └── figures/        # 图片
└── source/             # 源代码（可选）
\`\`\`

---

## 环境一致性测试

### 本地测试
\`\`\`bash
# 1. 清理环境
make clean

# 2. 下载字体（如果未下载）
make fonts

# 3. 编译测试
make

# 4. 运行测试套件
make test

# 5. 检查字体
python3 scripts/check_fonts.py

# 6. 生成对比图
python3 scripts/generate_cover_diff.py
\`\`\`

### CI/CD 测试
- GitHub Actions 会自动测试跨平台编译
- 检查 .github/workflows/cross-platform-fonts.yml

### 手动验证清单
- [ ] Linux 编译成功
- [ ] macOS 编译成功
- [ ] Windows 编译成功
- [ ] 开源字体 fallback 工作正常
- [ ] 商业字体检测正常
- [ ] 所有测试通过

---

## 发布后任务

### GitHub Release
1. 创建新 tag: \`git tag v${VERSION}\`
2. 推送 tag: \`git push origin v${VERSION}\`
3. 在 GitHub 创建 Release
4. 上传打包文件

### 文档更新
- [ ] 更新 README.md 版本号
- [ ] 更新下载链接
- [ ] 添加发布说明

### 社区通知
- [ ] 在学校论坛发布
- [ ] LaTeX 中文社区通知
- [ ] 更新项目主页

---

## 联系方式

如有问题，请联系：
- GitHub Issues: ${REPO_URL%.git}/issues
- Email: ${MAINTAINER_EMAIL}

EOF

echo "✓ 上传清单已生成: $DIST_DIR/UPLOAD-CHECKLIST.md"

# ==========================================
# 5. 汇总
# ==========================================
echo ""
echo "=========================================="
echo "打包完成！"
echo "=========================================="
echo ""
echo "生成的文件："
ls -lh "$DIST_DIR"
echo ""
echo "下一步："
echo "1. 查看上传清单: $DIST_DIR/UPLOAD-CHECKLIST.md"
echo "2. Overleaf 测试: 使用 jouthesis-overleaf-${VERSION}.zip"
echo "3. CTAN 提交: 使用 jouthesis-ctan-${VERSION}.zip"
echo ""
