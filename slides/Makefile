# Makefile for Paper2Slide Pipeline
# 自动化论文转PPT流程

# 路径配置
EXTRACTORS_DIR = extractors
TEMPLATES_DIR = ../templates
OUTPUTS_DIR = outputs
CHAPTERS_DIR = ../contents/chapters

# 输入文件
PROPOSAL_TEX = $(TEMPLATES_DIR)/reports/proposal-science.tex
MIDTERM_TEX = $(TEMPLATES_DIR)/forms/midterm-check.tex
THESIS_TEX = ../main.tex

# 输出文件
PROPOSAL_MD = $(OUTPUTS_DIR)/proposal.md
MIDTERM_MD = $(OUTPUTS_DIR)/midterm.md
DEFENSE_MD = $(OUTPUTS_DIR)/defense.md

# Python解释器
PYTHON = python3

# 颜色输出
GREEN = \033[0;32m
YELLOW = \033[0;33m
NC = \033[0m  # No Color

.PHONY: all proposal midterm defense clean help check-deps

# 默认目标：生成全部三个PPT Markdown
all: proposal midterm defense
	@echo "$(GREEN)✓ 全部PPT Markdown已生成$(NC)"
	@echo "$(YELLOW)下一步: 访问 banana-slides (http://localhost:3000) 上传生成PPT$(NC)"

# 检查依赖
check-deps:
	@echo "检查依赖..."
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "错误: 未找到 python3"; exit 1; }
	@command -v pandoc >/dev/null 2>&1 || echo "$(YELLOW)警告: 未找到 pandoc，建议安装以提高转换质量$(NC)"
	@echo "$(GREEN)✓ 依赖检查完成$(NC)"

# 生成开题报告PPT
proposal: check-deps $(OUTPUTS_DIR)
	@echo "$(GREEN)生成开题报告PPT Markdown...$(NC)"
	@$(PYTHON) $(EXTRACTORS_DIR)/extract_proposal.py \
		--input $(PROPOSAL_TEX) \
		--output $(PROPOSAL_MD)
	@echo "$(GREEN)✓ 开题报告PPT Markdown已生成: $(PROPOSAL_MD)$(NC)"

# 生成中期汇报PPT
midterm: check-deps $(OUTPUTS_DIR)
	@echo "$(GREEN)生成中期汇报PPT Markdown...$(NC)"
	@$(PYTHON) $(EXTRACTORS_DIR)/extract_midterm.py \
		--input $(MIDTERM_TEX) \
		--thesis $(THESIS_TEX) \
		--output $(MIDTERM_MD)
	@echo "$(GREEN)✓ 中期汇报PPT Markdown已生成: $(MIDTERM_MD)$(NC)"

# 生成答辩PPT
defense: check-deps $(OUTPUTS_DIR)
	@echo "$(GREEN)生成答辩PPT Markdown...$(NC)"
	@$(PYTHON) $(EXTRACTORS_DIR)/extract_defense.py \
		--input $(THESIS_TEX) \
		--chapters $(CHAPTERS_DIR) \
		--output $(DEFENSE_MD)
	@echo "$(GREEN)✓ 答辩PPT Markdown已生成: $(DEFENSE_MD)$(NC)"

# 创建输出目录
$(OUTPUTS_DIR):
	@mkdir -p $(OUTPUTS_DIR)

# 清理生成的文件
clean:
	@echo "清理输出文件..."
	@rm -f $(OUTPUTS_DIR)/*.md
	@echo "$(GREEN)✓ 清理完成$(NC)"

# 深度清理（包括outputs目录）
clean-all: clean
	@rm -rf $(OUTPUTS_DIR)
	@echo "$(GREEN)✓ 深度清理完成$(NC)"

# 手动转换（使用pandoc）
convert-tex-to-md:
	@echo "$(GREEN)使用pandoc手动转换LaTeX到Markdown...$(NC)"
	@for f in $(TEMPLATES_DIR)/reports/*.tex $(TEMPLATES_DIR)/forms/*.tex; do \
		pandoc -f latex -t markdown --wrap=none "$$f" -o "$(OUTPUTS_DIR)/$$(basename $$f .tex).md"; \
		echo "$(GREEN)✓ 已转换: $$f$(NC)"; \
	done

# 帮助信息
help:
	@echo "$(GREEN)Paper2Slide Makefile 使用指南$(NC)"
	@echo ""
	@echo "$(YELLOW)可用目标:$(NC)"
	@echo "  make all          - 生成全部三个PPT Markdown（开题、中期、答辩）"
	@echo "  make proposal     - 只生成开题报告PPT Markdown"
	@echo "  make midterm      - 只生成中期汇报PPT Markdown"
	@echo "  make defense      - 只生成答辩PPT Markdown"
	@echo "  make clean        - 清理生成的Markdown文件"
	@echo "  make clean-all    - 清理全部输出（包括outputs目录）"
	@echo "  make check-deps   - 检查依赖项"
	@echo "  make help         - 显示此帮助信息"
	@echo ""
	@echo "$(YELLOW)使用流程:$(NC)"
	@echo "  1. make all                          # 生成全部PPT Markdown"
	@echo "  2. 编辑 outputs/*.md 补充详细内容"
	@echo "  3. 访问 http://localhost:3000"
	@echo "  4. 上传 Markdown 文件到 banana-slides"
	@echo "  5. 选择风格模板并生成 PPTX"
	@echo ""
	@echo "$(YELLOW)自定义配置:$(NC)"
	@echo "  - 修改输入文件路径: 编辑 Makefile 中的变量"
	@echo "  - 修改提取规则: 编辑 extractors/*.py"
	@echo "  - 使用自定义模板: 复制 templates/*_template.md 并修改"
