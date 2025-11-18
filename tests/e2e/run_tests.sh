#!/bin/bash
# 运行架构师API端到端测试
# 用法: chmod +x run_tests.sh && ./run_tests.sh

echo "================================================================"
echo "架构师API - 端到端测试套件"
echo "================================================================"
echo ""

# 切换到项目根目录
cd "$(dirname "$0")/../.." || exit 1

echo "当前目录: $(pwd)"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] Python3未安装"
    exit 1
fi

echo "[1/3] 检查依赖..."

# 检查pytest
if ! python3 -c "import pytest" &> /dev/null; then
    echo "[警告] pytest未安装，正在安装..."
    pip3 install pytest fastapi httpx pydantic
fi

# 检查fastapi
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "[警告] fastapi未安装，正在安装..."
    pip3 install fastapi httpx
fi

echo "[2/3] 运行测试..."
echo ""

# 运行测试
python3 -m pytest tests/e2e/test_architect_api_e2e.py -v --tb=short

# 保存退出码
TEST_EXIT_CODE=$?

echo ""
echo "================================================================"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "[成功] 所有测试通过！"
    echo ""
    echo "生成的测试报告位于: tests/e2e/"
else
    echo "[失败] 部分测试未通过，请查看上方错误信息"
fi

echo "================================================================"
echo ""

exit $TEST_EXIT_CODE

