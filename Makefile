# LaTeX Makefile for JOU Undergraduate Thesis

MAIN = main
TEX = xelatex
BIB = bibtex

# 编译选项
TEXFLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all clean cleanall view help wordcount

# 默认目标：完整编译
all: $(MAIN).pdf

# 编译PDF（完整流程）
$(MAIN).pdf: $(MAIN).tex
	@echo "==> 第1次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 处理参考文献..."
	-$(BIB) $(MAIN)
	@echo "==> 第2次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 第3次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 编译完成! 生成文件: $(MAIN).pdf"

# 清理临时文件
clean:
	@echo "==> 清理临时文件..."
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
	rm -f *.fls *.fdb_latexmk *.synctex.gz *.xdv *.nav *.snm *.vrb
	rm -f contents/*.aux contents/chapters/*.aux contents/appendices/*.aux
	@echo "==> 清理完成!"

# 完全清理（包括PDF）
cleanall: clean
	@echo "==> 删除PDF文件..."
	rm -f $(MAIN).pdf
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

# 帮助信息
help:
	@echo "江苏海洋大学毕业论文 LaTeX 模板 - Makefile 使用说明"
	@echo ""
	@echo "可用命令:"
	@echo "  make          - 完整编译论文（默认）"
	@echo "  make all      - 完整编译论文"
	@echo "  make clean    - 清理临时文件"
	@echo "  make cleanall - 完全清理（包括PDF）"
	@echo "  make view     - 编译并预览PDF"
	@echo "  make wordcount- 统计论文字数"
	@echo "  make help     - 显示此帮助信息"
	@echo ""
	@echo "编译流程:"
	@echo "  1. xelatex main.tex  (第1次编译)"
	@echo "  2. bibtex main       (处理参考文献)"
	@echo "  3. xelatex main.tex  (第2次编译)"
	@echo "  4. xelatex main.tex  (第3次编译，确保引用正确)"
