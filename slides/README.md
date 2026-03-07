# 论文转演示文稿（Paper2Slide）集成

本目录提供基于 [banana-slides](https://github.com/Anionex/banana-slides) 的论文转PPT自动化流程，支持从LaTeX模板快速生成开题、中期、答辩演示文稿。

---

## 📋 功能概览

| 场景 | 输入 | 输出 |
|------|------|------|
| **开题答辩** | `reports/proposal-*.tex` | 开题报告PPT（16:9） |
| **中期检查** | `forms/midterm-check.tex` + 论文进度 | 中期汇报PPT |
| **毕业答辩** | `main.tex` 论文正文 | 答辩PPT（含核心内容提取） |

---

## 🚀 快速开始

### 前置条件

1. **已完成的LaTeX文档**（编译通过的 `.tex` 和 `.pdf` 文件）
2. **banana-slides环境**（见下方安装步骤）
3. **Python 3.10+** 和 **pandoc**

### 安装 banana-slides

```bash
# 克隆 banana-slides 仓库
cd slides/
git clone https://github.com/Anionex/banana-slides.git

# 配置环境变量（复制模板并填写API密钥）
cd banana-slides
cp .env.example .env
# 编辑 .env 文件，填写 Gemini/OpenAI/其他LLM的API密钥

# Docker方式启动（推荐）
docker compose up -d

# 或手动启动
# 后端：
cd backend && uv venv && source .venv/bin/activate && uv pip install -r requirements.txt && uv run main.py
# 前端：
cd frontend && npm install && npm run dev
```

访问 `http://localhost:3000` 验证安装成功。

---

## 🔑 API-KEY 配置（重要！）

### 必需步骤

banana-slides 需要 LLM API 才能生成 PPT。完成安装后，**必须配置 API-KEY**：

```bash
cd slides/banana-slides
nano .env  # 或使用其他编辑器
```

### 配置选项

#### 方案 A: Google Gemini（推荐）

**优点**：免费额度充足，性能好，配置简单

```bash
# 在 .env 文件中添加
GOOGLE_API_KEY=your_gemini_api_key_here
```

**获取 API Key**:
1. 访问 https://makersuite.google.com/app/apikey
2. 登录 Google 账号
3. 点击「Create API key」
4. 复制密钥到 `.env` 文件

---

#### 方案 B: OpenAI

```bash
# 在 .env 文件中添加
OPENAI_API_KEY=sk-your_openai_api_key_here
OPENAI_MODEL=gpt-4  # 可选，默认 gpt-3.5-turbo
```

**获取 API Key**: https://platform.openai.com/api-keys

---

#### 方案 C: 国内 LLM（智谱 AI / 通义千问等）

```bash
# 在 .env 文件中添加
LAZYLLM_API_KEY=your_api_key_here
LAZYLLM_PROVIDER=zhipu  # 或 qwen, wenxin, etc.
```

---

### 配置后重启服务

```bash
# Docker 方式
cd banana-slides
docker-compose restart

# 手动方式
# 重新运行启动脚本或手动重启服务
```

### 验证配置

```bash
# 检查环境变量
cat .env | grep API_KEY

# 测试服务
curl http://localhost:5000/health
```

---

## 📂 目录结构

```
slides/
├── README.md                    # 本文件
├── banana-slides/               # banana-slides子仓库（git clone）
├── extractors/                  # LaTeX内容提取脚本
│   ├── extract_proposal.py      #   开题报告提取器
│   ├── extract_midterm.py       #   中期检查提取器
│   ├── extract_defense.py       #   答辩内容提取器
│   └── tex2markdown.py          #   通用LaTeX→Markdown转换器
├── templates/                   # Markdown模板（喂给banana-slides）
│   ├── proposal_template.md     #   开题报告结构模板
│   ├── midterm_template.md      #   中期汇报结构模板
│   └── defense_template.md      #   答辩PPT结构模板
└── outputs/                     # 生成的中间Markdown和最终PPT
    ├── proposal.md
    ├── midterm.md
    ├── defense.md
    └── *.pptx / *.pdf
```

---

## 🔧 使用流程

### 1. 生成开题报告PPT

```bash
# 从开题报告LaTeX提取内容
python extractors/extract_proposal.py \
  --input ../templates/reports/proposal-science.tex \
  --output outputs/proposal.md

# 方式A: 使用banana-slides Web界面
# 1. 访问 http://localhost:3000
# 2. 上传 outputs/proposal.md
# 3. 选择"学术汇报"风格模板
# 4. 生成并下载PPTX

# 方式B: 使用API（需配置banana-slides API端点）
curl -X POST http://localhost:5000/api/generate \
  -F "file=@outputs/proposal.md" \
  -F "template=academic" \
  -o outputs/proposal.pptx
```

### 2. 生成中期检查PPT

```bash
python extractors/extract_midterm.py \
  --input ../templates/forms/midterm-check.tex \
  --thesis ../main.tex \
  --output outputs/midterm.md

# 上传到banana-slides生成PPT
```

### 3. 生成答辩PPT

```bash
python extractors/extract_defense.py \
  --input ../main.tex \
  --chapters ../contents/chapters/ \
  --output outputs/defense.md

# 上传到banana-slides生成PPT
```

---

## 📝 Markdown模板说明

### 开题报告模板结构

```markdown
# [论文题目]

---

## 研究背景与意义

- 背景介绍
- 研究意义
- 国内外研究现状

---

## 研究内容与目标

1. 主要研究内容
2. 拟解决的关键问题
3. 预期研究目标

---

## 研究方法与技术路线

- 研究方法
- 技术路线图
- 可行性分析

---

## 工作计划与进度安排

| 阶段 | 时间 | 内容 |
|------|------|------|
| 第一阶段 | XX-XX | 文献调研 |
| ...

---

## 参考文献

1. [文献1]
2. [文献2]
```

### 答辩PPT模板结构

```markdown
# [论文题目]

答辩人：XXX
指导教师：XXX

---

## 目录

1. 研究背景与意义
2. 文献综述
3. 研究方法与实现
4. 实验结果与分析
5. 结论与展望

---

## 1. 研究背景与意义

...

---

## 2. 文献综述

...

---

## 3. 研究方法与实现

### 3.1 总体架构
### 3.2 关键技术
### 3.3 实现细节

---

## 4. 实验结果与分析

### 4.1 实验设置
### 4.2 结果对比
### 4.3 性能分析

---

## 5. 结论与展望

### 主要贡献
### 不足与改进
### 未来工作

---

## 谢谢！

欢迎各位老师批评指正
```

---

## 🎨 风格定制

### 预设风格模板

banana-slides 支持多种风格预设，推荐使用：

- **学术汇报**：简洁专业，适合开题/答辩
- **科技蓝**：现代科技感，适合理工类
- **商务灰**：商务风格，适合经管类

### 自定义风格

上传参考图片到banana-slides实现风格迁移：

1. 准备参考PPT截图（16:9比例）
2. 在banana-slides上传为"参考图片"
3. 生成时应用该风格

---

## 🔄 工作流程图

```
LaTeX论文/报告
    |
    v
[extractors/*.py]  ──> Markdown文件
    |
    v
banana-slides
    |
    ├─> 自动生成初稿
    ├─> 自然语言调整（"把这张图换成饼图"）
    └─> 导出PPTX/PDF
    |
    v
最终演示文稿
```

---

## ⚙️ 高级配置

### 自定义提取规则

编辑 `extractors/tex2markdown.py` 中的转换规则：

```python
# 自定义章节标题映射
SECTION_MAPPING = {
    r'\\section{(.+?)}': '## {}',
    r'\\subsection{(.+?)}': '### {}',
    r'\\subsubsection{(.+?)}': '#### {}',
}

# 自定义内容过滤（跳过不需要的部分）
SKIP_PATTERNS = [
    r'\\begin{acknowledgements}',  # 跳过致谢
    r'\\appendix',                  # 跳过附录
]
```

### API批量生成

```python
import requests

files = ['proposal.md', 'midterm.md', 'defense.md']
for f in files:
    with open(f, 'rb') as file:
        response = requests.post(
            'http://localhost:5000/api/generate',
            files={'file': file},
            data={'template': 'academic'}
        )
        with open(f.replace('.md', '.pptx'), 'wb') as out:
            out.write(response.content)
```

---

## 📚 参考资源

- [banana-slides 官方文档](https://github.com/Anionex/banana-slides)
- [LaTeX to Markdown 转换指南](https://pandoc.org/MANUAL.html)
- [学术PPT设计原则](https://www.bilibili.com/video/BV1...)

---

## 🐛 常见问题

### Q: 提取的Markdown格式不正确？

A: 检查LaTeX文件编码（应为UTF-8），并确保pandoc版本 >= 2.0。

### Q: banana-slides生成的PPT样式不满意？

A: 使用自然语言编辑功能："把标题字体改大"、"调整配色为蓝色系"等。

### Q: 如何批量生成多个场景的PPT？

A: 使用 `Makefile` 或编写shell脚本自动化：

```bash
#!/bin/bash
for stage in proposal midterm defense; do
    python extractors/extract_${stage}.py
    # 调用banana-slides API...
done
```

---

## 📄 许可证

本集成脚本采用 [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt)，与主模板保持一致。

banana-slides 项目遵循其自身的开源许可证。

---

**注**: 首次使用建议先用Web界面熟悉流程，再使用脚本自动化。
