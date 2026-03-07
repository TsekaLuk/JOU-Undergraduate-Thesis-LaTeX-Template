#!/bin/bash
# 打包脚本 - 准备 Overleaf 社区包、完整版和 CTAN 发布包

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

rm -rf "$DIST_DIR" "$TEMP_DIR"
mkdir -p "$DIST_DIR" "$TEMP_DIR"

create_latexmkrc() {
  local target_dir="$1"
  cat > "$target_dir/latexmkrc" <<'EOF'
# Overleaf latexmkrc 配置
$pdf_mode = 5;  # xelatex
$postscript_mode = $dvi_mode = 0;
$xelatex = 'xelatex -interaction=nonstopmode -file-line-error %O %S';
$clean_ext = 'aux bbl blg fdb_latexmk fls log out synctex.gz toc lof lot';
EOF
  cp "$target_dir/latexmkrc" "$target_dir/.latexmkrc"
}

copy_common_project_files() {
  local target_dir="$1"
  cp "$PROJECT_ROOT"/main.tex "$target_dir/"
  cp "$PROJECT_ROOT"/LICENSE "$target_dir/"
  cp "$PROJECT_ROOT"/README.md "$target_dir/"
  cp "$PROJECT_ROOT"/README_EN.md "$target_dir/"
  cp "$PROJECT_ROOT"/docs/guides/usage.md "$target_dir/USAGE.md"
  cp -r "$PROJECT_ROOT"/styles "$target_dir/"
  cp -r "$PROJECT_ROOT"/contents "$target_dir/"
  cp -r "$PROJECT_ROOT"/figures "$target_dir/"
  mkdir -p "$target_dir"/references
  cp "$PROJECT_ROOT"/references/refs.bib "$target_dir"/references/
  find "$target_dir"/contents -type f \( -name '*.aux' -o -name '*.log' -o -name '*.bbl' -o -name '*.blg' \) -delete
  create_latexmkrc "$target_dir"
}

# ==========================================
# 1. Overleaf Gallery 轻量社区包
# ==========================================
echo ""
echo "==> 准备 Overleaf Gallery 轻量社区包..."

OVERLEAF_GALLERY_DIR="$TEMP_DIR/jouthesis-overleaf-gallery"
mkdir -p "$OVERLEAF_GALLERY_DIR"
copy_common_project_files "$OVERLEAF_GALLERY_DIR"

# 社区包不携带大字体文件，只保留说明目录
mkdir -p "$OVERLEAF_GALLERY_DIR"/fonts/proprietary
cat > "$OVERLEAF_GALLERY_DIR"/fonts/README.md <<EOF
# Overleaf Gallery Community Package

This package is intentionally lightweight for Overleaf Gallery distribution.

- Canonical maintained version: ${REPO_URL}
- Large vendored fonts are intentionally omitted.
- On Overleaf, the template falls back to TeX Live built-in fonts automatically.
- For full assets, E2E tests, local high-fidelity fonts, and issue tracking, use the GitHub repository.
EOF
echo "# Optional local commercial fonts can be added here in a full local clone." > "$OVERLEAF_GALLERY_DIR"/fonts/proprietary/README.md

cat > "$OVERLEAF_GALLERY_DIR"/OVERLEAF_GALLERY.md <<EOF
# Overleaf Gallery Release

This is the lightweight community edition for Overleaf Gallery.

- Best for: quick preview and onboarding
- Canonical maintained version: ${REPO_URL}
- Full assets, packaging scripts, CI, and issue tracking live on GitHub
EOF

cd "$TEMP_DIR"
zip -r "$DIST_DIR/jouthesis-overleaf-gallery-${VERSION}.zip" jouthesis-overleaf-gallery/ -x "*.DS_Store" "*.git*"
echo "✓ Overleaf Gallery 包已生成: $DIST_DIR/jouthesis-overleaf-gallery-${VERSION}.zip"

# ==========================================
# 2. Overleaf 完整上传包（GitHub/本地优先）
# ==========================================
echo ""
echo "==> 准备 Overleaf 完整上传包..."

OVERLEAF_DIR="$TEMP_DIR/jouthesis-overleaf"
mkdir -p "$OVERLEAF_DIR"
copy_common_project_files "$OVERLEAF_DIR"
cp -r "$PROJECT_ROOT"/fonts "$OVERLEAF_DIR/"
rm -rf "$OVERLEAF_DIR"/fonts/proprietary
mkdir -p "$OVERLEAF_DIR"/fonts/proprietary
echo "# 说明：Overleaf 环境请使用 fonts/opensource/ 中的字体" > "$OVERLEAF_DIR"/fonts/proprietary/README.md

cd "$TEMP_DIR"
zip -r "$DIST_DIR/jouthesis-overleaf-${VERSION}.zip" jouthesis-overleaf/ -x "*.DS_Store" "*.git*"
echo "✓ Overleaf 完整包已生成: $DIST_DIR/jouthesis-overleaf-${VERSION}.zip"

# ==========================================
# 3. CTAN 提交包
# ==========================================
echo ""
echo "==> 准备 CTAN 提交包..."

CTAN_DIR="$TEMP_DIR/jouthesis"
mkdir -p "$CTAN_DIR"/{tex,doc,source}

cp "$PROJECT_ROOT"/styles/*.cls "$CTAN_DIR/tex/"
cp "$PROJECT_ROOT"/styles/*.sty "$CTAN_DIR/tex/"

mkdir -p "$CTAN_DIR/doc/examples/contents/chapters"
mkdir -p "$CTAN_DIR/doc/examples/contents/appendices"
mkdir -p "$CTAN_DIR/doc/examples/references"
mkdir -p "$CTAN_DIR/doc/figures"
cp "$PROJECT_ROOT"/README.md "$CTAN_DIR/doc/"
cp "$PROJECT_ROOT"/README_EN.md "$CTAN_DIR/doc/"
cp "$PROJECT_ROOT"/LICENSE "$CTAN_DIR/doc/"
cp "$PROJECT_ROOT"/docs/guides/usage.md "$CTAN_DIR/doc/USAGE.md"
cp "$PROJECT_ROOT"/main.tex "$CTAN_DIR/doc/examples/"
cp "$PROJECT_ROOT"/contents/acknowledgements.tex "$CTAN_DIR/doc/examples/contents/"
cp "$PROJECT_ROOT"/contents/chapters/*.tex "$CTAN_DIR/doc/examples/contents/chapters/"
cp "$PROJECT_ROOT"/contents/appendices/*.tex "$CTAN_DIR/doc/examples/contents/appendices/"
cp "$PROJECT_ROOT"/references/refs.bib "$CTAN_DIR/doc/examples/references/"
cp "$PROJECT_ROOT"/figures/* "$CTAN_DIR/doc/figures/"

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
- GitHub-maintained canonical distribution

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

cd "$TEMP_DIR"
zip -r "$DIST_DIR/jouthesis-ctan-${VERSION}.zip" jouthesis/ -x "*.DS_Store" "*.git*"
echo "✓ CTAN 包已生成: $DIST_DIR/jouthesis-ctan-${VERSION}.zip"

# ==========================================
# 4. 环境一致性检查配置
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
    - "Times New Roman (or Tinos / TeX Gyre Termes fallback)"
    - "SimSun/STSong (or Noto Serif CJK / Fandol Song fallback)"
    - "KaiTi/STKaiti (or LXGW WenKai / Fandol Kai fallback)"
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
    - "Cross-references resolved"
    - "Bibliography compiled"
    - "No undefined references"
EOF

echo "✓ 环境检查配置已生成: $DIST_DIR/environment-check.yml"

# ==========================================
# 5. 生成上传清单
# ==========================================
cat > "$DIST_DIR/UPLOAD-CHECKLIST.md" <<EOF
# 上传清单

## Overleaf 上传步骤

### 社区版（推荐用于 Overleaf Gallery）
1. 登录 Overleaf (https://www.overleaf.com)
2. 上传 \`jouthesis-overleaf-gallery-${VERSION}.zip\` 或创建空白项目后导入文件
3. 在项目中点击 "Submit" → "Overleaf Gallery"
4. 填写模板信息并提交
5. 强调 GitHub 为 canonical maintained version

### 社区版说明
- 社区包文件: \`jouthesis-overleaf-gallery-${VERSION}.zip\`
- 设计目标: 轻量、可编译、适合社区分发
- 字体策略: Overleaf / TeX Live 内置字体优先
- Canonical GitHub: ${REPO_URL}

### 完整版（适合本地/付费 Overleaf/GitHub）
1. 登录 Overleaf
2. 点击 "New Project" → "Upload Project"
3. 上传 \`jouthesis-overleaf-${VERSION}.zip\`
4. 等待解压完成
5. 验证编译成功

### 从 GitHub 导入
1. 登录 Overleaf
2. 点击 "New Project" → "Import from GitHub"
3. 授权访问 GitHub 仓库
4. 选择 JOU-Undergraduate-Thesis-LaTeX-Template
5. 等待导入完成

### Overleaf 环境配置
- 编译器: XeLaTeX
- TeX Live 版本: 2024 (推荐最新)
- 主文档: main.tex

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
- **Note to CTAN team**: This is the official LaTeX template for undergraduate thesis at Jiangsu Ocean University, China.

---

## 联系方式

- GitHub Issues: ${REPO_URL%.git}/issues
- Email: ${MAINTAINER_EMAIL}
EOF

echo "✓ 上传清单已生成: $DIST_DIR/UPLOAD-CHECKLIST.md"

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
echo "2. Overleaf Gallery: 使用 jouthesis-overleaf-gallery-${VERSION}.zip"
echo "3. Overleaf 完整版: 使用 jouthesis-overleaf-${VERSION}.zip"
echo "4. CTAN 提交: 使用 jouthesis-ctan-${VERSION}.zip"
echo ""
