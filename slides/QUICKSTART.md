# Paper2Slide 快速入门

**5分钟从论文生成专业答辩PPT**

---

## 📋 前置条件

- ✅ 已完成的 LaTeX 论文（`.tex` 文件已编译通过）
- ✅ Python 3.10+ 和 pandoc
- ✅ （推荐）Docker 和 Docker Compose

---

## 🚀 三步生成 PPT

### Step 1: 安装 banana-slides

```bash
cd slides/
./setup_banana_slides.sh
```

脚本会自动：
1. 克隆 banana-slides 仓库
2. 配置环境变量
3. 启动服务（Docker 或手动）

**重要**：编辑 `banana-slides/.env`，填写 LLM API 密钥（Gemini/OpenAI/...）

---

### Step 2: 生成 PPT Markdown

#### 方式 A: 一键生成全部

```bash
make all
```

生成三个 Markdown 文件：
- `outputs/proposal.md` - 开题报告 PPT
- `outputs/midterm.md` - 中期汇报 PPT
- `outputs/defense.md` - 答辩 PPT

#### 方式 B: 单独生成

```bash
# 开题报告
make proposal

# 中期汇报
make midterm

# 答辩 PPT
make defense
```

---

### Step 3: 上传到 banana-slides 生成 PPT

1. 访问 http://localhost:3000
2. 点击「新建项目」
3. 选择「上传文件」→ 选择 `outputs/*.md`
4. 选择风格模板（推荐：学术汇报）
5. 点击「生成」，等待 AI 生成 PPT
6. 下载 PPTX 文件

---

## 🎨 优化 PPT 效果

### 使用自然语言编辑

banana-slides 支持自然语言修改：

- "把这个图换成饼图"
- "调整标题字体大小"
- "改成蓝色主题"

### 自定义模板

1. 编辑 `templates/*_template.md` 修改结构
2. 重新运行 `make` 生成
3. 上传到 banana-slides

### 提取规则自定义

编辑 `extractors/*.py` 中的提取逻辑：

```python
# extractors/extract_defense.py
STANDARD_STRUCTURE = [
    ('研究背景与意义', ['背景', '意义', '引言']),
    ('文献综述', ['综述', '相关工作']),
    # 添加更多章节...
]
```

---

## 📝 手动调整内容

生成的 Markdown 文件是**起点**，建议手动补充：

### 开题报告 (`outputs/proposal.md`)

- ✏️ 补充具体的研究内容描述
- ✏️ 完善参考文献列表
- ✏️ 调整工作计划时间表

### 中期汇报 (`outputs/midterm.md`)

- ✏️ 填写已完成的实际内容
- ✏️ 描述遇到的具体问题
- ✏️ 更新下一步详细计划

### 答辩 PPT (`outputs/defense.md`)

- ✏️ 添加实验结果图表
- ✏️ 补充创新点详细描述
- ✏️ 准备常见问题回答

---

## 🛠️ 常用命令

```bash
# 查看帮助
make help

# 清理生成文件
make clean

# 检查依赖
make check-deps

# 停止 banana-slides
cd banana-slides
docker-compose down  # Docker方式
# 或
kill $(cat backend.pid frontend.pid)  # 手动方式
```

---

## 🐛 故障排除

### 问题 1: pandoc 转换失败

**解决**：安装 pandoc
```bash
# macOS
brew install pandoc

# Ubuntu
sudo apt-get install pandoc
```

### 问题 2: banana-slides 无法访问

**检查**：
```bash
# 检查端口占用
lsof -i :3000  # 前端
lsof -i :5000  # 后端

# 查看日志
cd banana-slides
tail -f backend.log
tail -f frontend.log
```

### 问题 3: LLM API 调用失败

**检查 `.env` 配置**：
```bash
cd banana-slides
cat .env | grep API_KEY
```

确保 API 密钥正确且有余额。

### 问题 4: 生成的 Markdown 内容不完整

**解决**：
1. 检查 `.tex` 文件是否已编译通过
2. 手动编辑 `outputs/*.md` 补充内容
3. 调整 `extractors/*.py` 中的提取规则

---

## 💡 最佳实践

1. **分阶段生成**：先生成框架，再逐步完善内容
2. **保留原始文件**：修改前备份 `outputs/*.md`
3. **迭代优化**：在 banana-slides 中使用自然语言多轮调整
4. **复用模板**：将满意的 PPT 导出为模板，供后续使用

---

## 📚 更多资源

- [完整文档](README.md)
- [banana-slides 官方仓库](https://github.com/Anionex/banana-slides)
- [LaTeX 模板主 README](../README.md)

---

**祝您答辩顺利！🎓**
