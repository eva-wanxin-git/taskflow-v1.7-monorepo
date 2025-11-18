#!/bin/bash
# 任务所·Flow v1.7 - Dashboard全自动启动脚本
#
# 功能：
# 1. 自动检查并安装Python依赖
# 2. 检查数据库文件
# 3. 启动Dashboard服务
# 4. 自动打开浏览器

echo "======================================================================="
echo "任务所·Flow v1.7 - Dashboard 全自动启动"
echo "======================================================================="
echo ""

# 进入项目根目录
cd "$(dirname "$0")"
PROJECT_ROOT=$(pwd)

echo "[步骤 1/5] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $PYTHON_VERSION"
echo ""

# 检查并安装依赖
echo "[步骤 2/5] 检查Python依赖..."

check_and_install() {
    PACKAGE=$1
    if python3 -c "import $PACKAGE" 2>/dev/null; then
        echo "✅ $PACKAGE 已安装"
    else
        echo "⚠️  $PACKAGE 未安装，正在安装..."
        pip3 install "$PACKAGE" -q
        if [ $? -eq 0 ]; then
            echo "✅ $PACKAGE 安装成功"
        else
            echo "❌ $PACKAGE 安装失败"
            return 1
        fi
    fi
}

# 检查核心依赖
check_and_install "fastapi" || exit 1
check_and_install "uvicorn" || exit 1
check_and_install "requests" || exit 1

echo ""

# 检查数据库
echo "[步骤 3/5] 检查数据库..."
DB_PATH="$PROJECT_ROOT/database/data/tasks.db"
if [ -f "$DB_PATH" ]; then
    DB_SIZE=$(du -h "$DB_PATH" | cut -f1)
    echo "✅ 数据库存在: $DB_PATH ($DB_SIZE)"
else
    echo "⚠️  数据库不存在，将使用默认配置"
fi
echo ""

# 检查端口
echo "[步骤 4/5] 检查端口占用..."
PORT=8877
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  端口 $PORT 已被占用"
    read -p "是否终止旧进程并重启？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
        echo "终止进程 PID=$PID..."
        kill -9 $PID 2>/dev/null
        sleep 2
        echo "✅ 旧进程已终止"
    else
        echo "❌ 取消启动"
        exit 1
    fi
else
    echo "✅ 端口 $PORT 可用"
fi
echo ""

# 启动Dashboard
echo "[步骤 5/5] 启动Dashboard..."
cd "$PROJECT_ROOT/apps/dashboard"

echo "----------------------------------------------------------------------"
echo "📍 工作目录: $(pwd)"
echo "🌐 访问地址: http://127.0.0.1:$PORT"
echo "📊 功能模块: 架构师监控 | 全栈工程师 | 功能清单 | Token管理"
echo "----------------------------------------------------------------------"
echo ""
echo "💡 提示："
echo "   - 按 Ctrl+C 停止服务"
echo "   - Dashboard会自动在浏览器中打开"
echo "   - 数据每5-20秒自动刷新"
echo ""
echo "======================================================================="
echo ""

# 在后台启动Dashboard（方便用户继续使用终端）
echo "正在启动Dashboard服务..."
python3 start_dashboard.py --port $PORT > /dev/null 2>&1 &
DASHBOARD_PID=$!

# 等待服务启动
sleep 3

# 检查服务是否成功启动
if ps -p $DASHBOARD_PID > /dev/null; then
    echo "✅ Dashboard启动成功！(PID: $DASHBOARD_PID)"
    echo ""
    echo "🌐 请访问: http://127.0.0.1:$PORT"
    echo ""

    # 自动打开浏览器
    echo "正在打开浏览器..."
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://127.0.0.1:$PORT" 2>/dev/null
    elif command -v open &> /dev/null; then
        open "http://127.0.0.1:$PORT" 2>/dev/null
    elif command -v start &> /dev/null; then
        start "http://127.0.0.1:$PORT" 2>/dev/null
    else
        echo "⚠️  无法自动打开浏览器，请手动访问上述地址"
    fi

    echo ""
    echo "======================================================================="
    echo "✅ Dashboard 运行中"
    echo "======================================================================="
    echo ""
    echo "📝 查看日志: tail -f ~/taskflow-dashboard.log"
    echo "🛑 停止服务: kill $DASHBOARD_PID"
    echo ""

    # 保存PID到文件
    echo $DASHBOARD_PID > "$PROJECT_ROOT/.dashboard.pid"

else
    echo "❌ Dashboard启动失败"
    echo ""
    echo "请检查错误信息或手动启动："
    echo "  cd $PROJECT_ROOT/apps/dashboard"
    echo "  python3 start_dashboard.py --port $PORT"
    exit 1
fi
