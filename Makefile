# LaTeX Makefile for JOU Undergraduate Thesis

MAIN = main
BODY_SAMPLE_TEX = samples/body-sample.tex
BODY_SAMPLE_PDF = body-sample.pdf
EXCELLENT_ABSTRACT_DIR = templates/reports
EXCELLENT_ABSTRACT_TEX = $(EXCELLENT_ABSTRACT_DIR)/excellent-thesis-abstract.tex
EXCELLENT_ABSTRACT_PDF = $(EXCELLENT_ABSTRACT_DIR)/excellent-thesis-abstract.pdf
TEX = xelatex
BIB = bibtex
INDEX = makeindex
THESIS_DEPS = $(MAIN).tex \
	$(wildcard styles/*.sty) \
	$(wildcard styles/*.cls) \
	$(wildcard contents/*.tex) \
	$(wildcard contents/chapters/*.tex) \
	$(wildcard contents/appendices/*.tex) \
	$(wildcard references/*.bib)
BODY_SAMPLE_DEPS = $(BODY_SAMPLE_TEX) \
	$(wildcard styles/*.sty) \
	$(wildcard fonts/opensource/*) \
	$(wildcard fonts/proprietary/*)
EXCELLENT_ABSTRACT_DEPS = $(EXCELLENT_ABSTRACT_TEX) \
	$(wildcard styles/*.sty) \
	$(wildcard contents/shared/*.tex) \
	$(wildcard contents/excellent-abstract/*.tex) \
	$(wildcard references/*.bib) \
	$(wildcard fonts/opensource/*) \
	$(wildcard fonts/proprietary/*)

# 编译选项
TEXFLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all fonts import-fonts clean cleanall view help wordcount test cover-diff readme-images

# 默认目标：完整编译
all: fonts $(MAIN).pdf $(BODY_SAMPLE_PDF)

# 下载仓库自带的开源字体
fonts:
	@echo "==> 检查仓库字体资源..."
	python3 scripts/download_fonts.py

# 从系统 / 桌面 / WPS 目录导入本机字体到 fonts/proprietary/
import-fonts:
	@echo "==> 导入本机标准字体..."
	python3 scripts/import_fonts.py

# 编译PDF（完整流程）
$(MAIN).pdf: $(THESIS_DEPS)
	@echo "==> 第1次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 处理参考文献..."
	-$(BIB) $(MAIN)
	@echo "==> 处理符号表..."
	-$(INDEX) $(MAIN).nlo -s nomencl.ist -o $(MAIN).nls
	@echo "==> 第2次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 第3次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 编译完成! 生成文件: $(MAIN).pdf"

$(BODY_SAMPLE_PDF): $(BODY_SAMPLE_DEPS)
	@echo "==> 编译正文样页基线..."
	$(TEX) $(TEXFLAGS) samples/body-sample.tex
	@echo "==> 第2次编译正文样页基线..."
	$(TEX) $(TEXFLAGS) samples/body-sample.tex
	@echo "==> 正文样页生成完成: $(BODY_SAMPLE_PDF)"

$(EXCELLENT_ABSTRACT_PDF): $(EXCELLENT_ABSTRACT_DEPS)
	@echo "==> 编译校优摘要模板..."
	cd $(EXCELLENT_ABSTRACT_DIR) && latexmk -xelatex -bibtex $(TEXFLAGS) excellent-thesis-abstract.tex
	@echo "==> 校优摘要生成完成: $(EXCELLENT_ABSTRACT_PDF)"

# 清理临时文件
clean:
	@echo "==> 清理临时文件..."
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.loa *.lol
	rm -f *.fls *.fdb_latexmk *.synctex.gz *.xdv *.nav *.snm *.vrb *.nlo *.nls *.ilg *.ind *.idx
	rm -f body-sample.aux body-sample.log body-sample.out body-sample.fls body-sample.fdb_latexmk body-sample.xdv
	rm -f contents/*.aux contents/chapters/*.aux contents/appendices/*.aux
	@echo "==> 清理完成!"

# 完全清理（包括PDF）
cleanall: clean
	@echo "==> 删除PDF文件..."
	rm -f $(MAIN).pdf $(BODY_SAMPLE_PDF)
	@echo "==> 完全清理完成!"

# 编译并预览
view: $(MAIN).pdf
	@echo "==> 打开PDF..."
	@if [ "$(shell uname)" = "Darwin" ]; then \
		open $(MAIN).pdf; \
	elif [ "$(shell uname)" = "Linux" ]; then \
		xdg-open $(MAIN).pdf; \
	else \
		echo "请手动打开 $(MAIN).pdf"; \
	fi

# 统计字数（仅统计正文章节）
wordcount:
	@echo "==> 统计字数..."
	@find contents/chapters -name "*.tex" -exec cat {} \; | \
		sed 's/\\[a-zA-Z]*{//g' | sed 's/}//g' | \
		sed 's/%.*//g' | sed '/^$$/d' | wc -m
	@echo "注：此为粗略估计，实际字数以Word工具为准"

# 生成封面对比产物（参考页 vs 当前页）
cover-diff: $(MAIN).pdf
	python3 scripts/generate_cover_diff.py

# 生成 README 预览图片（横向对比图 + 表单画廊）
readme-images: $(MAIN).pdf $(BODY_SAMPLE_PDF) $(EXCELLENT_ABSTRACT_PDF)
	python3 scripts/generate_readme_images.py

# 帮助信息
help:
	@echo "江苏海洋大学毕业论文 LaTeX 模板 - Makefile 使用说明"
	@echo ""
	@echo "可用命令:"
	@echo "  make          - 完整编译论文（默认）"
	@echo "  make all      - 完整编译论文"
	@echo "  make body-sample.pdf - 编译正文样页基线页"
	@echo "  make fonts    - 下载/校验仓库内置字体"
	@echo "  make import-fonts - 从系统 / 桌面 / WPS 目录导入本机字体"
	@echo "  make clean    - 清理临时文件"
	@echo "  make cleanall - 完全清理（包括PDF）"
	@echo "  make view     - 编译并预览PDF"
	@echo "  make cover-diff - 生成封面对比 overlay/diff/checker 产物"
	@echo "  make readme-images - 生成 README 用的横向对比图、校优摘要预览图和表单画廊"
	@echo "  make wordcount- 统计论文字数"
	@echo "  make test     - 运行 E2E 测试"
	@echo "  make help     - 显示此帮助信息"
	@echo ""
	@echo "编译流程:"
	@echo "  1. xelatex main.tex  (第1次编译)"
	@echo "  2. bibtex main       (处理参考文献)"
	@echo "  3. makeindex main.nlo -s nomencl.ist -o main.nls  (处理符号表)"
	@echo "  4. xelatex main.tex  (第2次编译)"
	@echo "  5. xelatex main.tex  (第3次编译，确保引用正确)"

test:
	$(MAKE) $(BODY_SAMPLE_PDF)
	python3 -m pytest tests/ -v --tb=short
