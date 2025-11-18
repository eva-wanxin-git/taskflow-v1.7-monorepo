@echo off
REM -*- coding: utf-8 -*-
REM 一键启动脚本 - 前端 + API + 对话历史库

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  🚀 一键启动 - Dashboard + 会话管理API                            ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM 检查Python
echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 错误: 未找到Python
    echo 请先安装Python 3.9+
    pause
    exit /b 1
)
echo ✓ Python已安装
echo.

REM 启动Dashboard (假设已启动)
echo [2/4] Dashboard应该已在运行...
echo      访问: http://localhost:8877
echo      (如果没启动，请先启动Dashboard)
echo.

REM 启动API服务
echo [3/4] 启动会话管理API服务...
echo      位置: apps/api
cd apps\api
if not exist "venv" (
    echo [*] 创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate.bat

echo [*] 安装依赖...
pip install -q fastapi uvicorn httpx pydantic 2>nul

echo [*] 启动API服务...
start "会话管理API" cmd /k "python start_api.py --port 8800"

echo ✓ API服务启动中...
echo    等待5秒服务就绪...
timeout /t 5 /nobreak

echo.
echo [4/4] 刷新Dashboard...
echo      1. 在浏览器中打开 Dashboard
echo      2. 按 Ctrl+F5 强制刷新
echo      3. 应该看到"对话历史库"中的会话列表
echo.

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  ✓ 启动完成！                                                     ║
echo ║  请在浏览器中刷新Dashboard查看对话历史库                          ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM 验证API
echo [*] 验证API连接...
curl http://localhost:8800/api/health >nul 2>&1
if errorlevel 0 (
    echo ✓ API已就绪！
    echo.
    echo 📊 API文档: http://localhost:8800/api/docs
    echo 📊 Dashboard: http://localhost:8877
    echo.
) else (
    echo ⚠ API可能未启动，请检查终端窗口
)

pause

