#!/bin/bash
# 自动安装和配置 banana-slides
# 用法: ./setup_banana_slides.sh

set -e  # 遇到错误立即退出

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  banana-slides 自动安装脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查依赖
echo -e "${YELLOW}[1/6] 检查依赖...${NC}"

# 检查 git
if ! command -v git &> /dev/null; then
    echo -e "${RED}错误: 未找到 git，请先安装 git${NC}"
    exit 1
fi

# 检查 Docker (可选)
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    DOCKER_AVAILABLE=true
    echo -e "${GREEN}✓ 检测到 Docker 和 Docker Compose${NC}"
else
    DOCKER_AVAILABLE=false
    echo -e "${YELLOW}⚠ 未检测到 Docker，将使用手动安装方式${NC}"
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 python3，请先安装 Python 3.10+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 版本: $(python3 --version)${NC}"

# 检查 Node.js (用于前端)
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠ 未检测到 Node.js，前端无法启动${NC}"
    echo -e "${YELLOW}  建议安装 Node.js 16+: https://nodejs.org/${NC}"
    NODE_AVAILABLE=false
else
    NODE_AVAILABLE=true
    echo -e "${GREEN}✓ Node.js 版本: $(node --version)${NC}"
fi

echo ""

# 克隆 banana-slides
echo -e "${YELLOW}[2/6] 克隆 banana-slides 仓库...${NC}"

if [ -d "banana-slides" ]; then
    echo -e "${YELLOW}⚠ banana-slides 目录已存在，跳过克隆${NC}"
else
    git clone https://github.com/Anionex/banana-slides.git
    echo -e "${GREEN}✓ 仓库克隆完成${NC}"
fi

cd banana-slides
echo ""

# 配置环境变量
echo -e "${YELLOW}[3/6] 配置环境变量...${NC}"

if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env 文件已存在，跳过配置${NC}"
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ 已创建 .env 文件（从 .env.example 复制）${NC}"
        echo -e "${RED}重要: 请编辑 .env 文件，填写您的 LLM API 密钥${NC}"
        echo -e "${YELLOW}支持的 LLM 提供商:${NC}"
        echo "  - Google Gemini"
        echo "  - OpenAI"
        echo "  - Vertex AI"
        echo "  - 其他（通过 Lazyllm）"
    else
        echo -e "${RED}错误: 未找到 .env.example 文件${NC}"
        exit 1
    fi
fi

echo ""

# 选择安装方式
if [ "$DOCKER_AVAILABLE" = true ]; then
    echo -e "${YELLOW}[4/6] 选择安装方式${NC}"
    echo "1) Docker Compose（推荐，快速启动）"
    echo "2) 手动安装（需要配置Python环境和Node.js）"
    read -p "请选择 (1/2): " install_choice

    if [ "$install_choice" = "1" ]; then
        # Docker 方式
        echo -e "${YELLOW}[5/6] 使用 Docker Compose 启动...${NC}"
        docker-compose up -d
        echo -e "${GREEN}✓ banana-slides 已通过 Docker 启动${NC}"
    else
        # 手动安装
        ./setup_manual.sh
    fi
else
    # 只能手动安装
    echo -e "${YELLOW}[4/6] 手动安装 banana-slides...${NC}"

    # 后端安装
    echo -e "${YELLOW}[4.1] 安装后端依赖...${NC}"
    if [ -d "backend" ]; then
        cd backend

        # 检查 uv 包管理器
        if ! command -v uv &> /dev/null; then
            echo -e "${YELLOW}安装 uv 包管理器...${NC}"
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
        fi

        # 创建虚拟环境
        if [ ! -d ".venv" ]; then
            uv venv
            echo -e "${GREEN}✓ 虚拟环境创建完成${NC}"
        fi

        # 激活虚拟环境
        source .venv/bin/activate

        # 安装依赖
        uv pip install -r requirements.txt
        echo -e "${GREEN}✓ 后端依赖安装完成${NC}"

        cd ..
    fi

    # 前端安装
    if [ "$NODE_AVAILABLE" = true ]; then
        echo -e "${YELLOW}[4.2] 安装前端依赖...${NC}"
        if [ -d "frontend" ]; then
            cd frontend
            npm install
            echo -e "${GREEN}✓ 前端依赖安装完成${NC}"
            cd ..
        fi
    fi

    echo ""
    echo -e "${YELLOW}[5/6] 启动服务...${NC}"

    # 启动后端
    if [ -d "backend" ]; then
        echo -e "${YELLOW}启动后端服务...${NC}"
        cd backend
        source .venv/bin/activate
        nohup uv run main.py > ../backend.log 2>&1 &
        BACKEND_PID=$!
        echo $BACKEND_PID > ../backend.pid
        cd ..
        echo -e "${GREEN}✓ 后端已启动 (PID: $BACKEND_PID)${NC}"
        echo -e "${GREEN}  日志文件: backend.log${NC}"
    fi

    # 启动前端
    if [ "$NODE_AVAILABLE" = true ] && [ -d "frontend" ]; then
        echo -e "${YELLOW}启动前端服务...${NC}"
        cd frontend
        nohup npm run dev > ../frontend.log 2>&1 &
        FRONTEND_PID=$!
        echo $FRONTEND_PID > ../frontend.pid
        cd ..
        echo -e "${GREEN}✓ 前端已启动 (PID: $FRONTEND_PID)${NC}"
        echo -e "${GREEN}  日志文件: frontend.log${NC}"
    fi
fi

echo ""

# 完成
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  安装完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}下一步:${NC}"
echo "1. 编辑 banana-slides/.env 文件，填写 LLM API 密钥"
echo "2. 访问 http://localhost:3000 查看 banana-slides 界面"
echo "3. 返回 slides/ 目录，运行 'make all' 生成 PPT Markdown"
echo "4. 将生成的 Markdown 文件上传到 banana-slides 生成 PPT"
echo ""
echo -e "${YELLOW}停止服务:${NC}"
if [ "$DOCKER_AVAILABLE" = true ] && [ "$install_choice" = "1" ]; then
    echo "  cd banana-slides && docker-compose down"
else
    echo "  cd banana-slides && kill \$(cat backend.pid frontend.pid)"
fi
echo ""
echo -e "${GREEN}祝使用愉快！${NC}"
