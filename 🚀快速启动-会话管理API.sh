#!/bin/bash
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 会话管理API

启动v1.7 API服务并运行集成验证
"""

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║         快速启动 - 会话管理API (INTEGRATE-002)                    ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# 检查Python环境
echo "[*] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "[✗] 错误: 未找到Python3"
    exit 1
fi
echo "[✓] Python版本: $(python3 --version)"
echo ""

# 进入API目录
cd "$(dirname "$0")/apps/api" || exit 1
echo "[✓] 已切换到API目录: $(pwd)"
echo ""

# 安装依赖
if [ ! -d "venv" ]; then
    echo "[*] 创建虚拟环境..."
    python3 -m venv venv
fi

echo "[*] 激活虚拟环境..."
source venv/bin/activate || . venv/Scripts/activate

echo "[*] 安装依赖..."
pip install -q fastapi uvicorn httpx pydantic pytest pytest-cov 2>/dev/null || true
echo "[✓] 依赖已安装"
echo ""

# 启动API服务
echo "[*] 启动API服务..."
echo "    运行: python start_api.py"
echo "    文档: http://localhost:8800/api/docs"
echo ""

python start_api.py --port 8800 &
API_PID=$!

echo "[✓] API已启动 (PID: $API_PID)"
echo "[*] 等待服务启动..."
sleep 3

# 运行集成验证
echo ""
echo "[*] 运行集成验证..."
python tests/verify_conversations_integration.py

VERIFY_STATUS=$?

# 清理
echo ""
echo "[*] 清理..."
kill $API_PID 2>/dev/null || true

# 输出结果
echo ""
if [ $VERIFY_STATUS -eq 0 ]; then
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║  ✓ 所有验证已通过！API集成成功！                                 ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║  ✗ 验证失败，请查看上面的日志                                     ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    exit 1
fi

