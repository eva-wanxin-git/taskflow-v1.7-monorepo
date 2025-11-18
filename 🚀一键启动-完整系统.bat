@echo off
chcp 65001 >nul
title 任务所·Flow v1.7 - 完整系统启动

cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                  任务所·Flow v1.7 - 系统启动                     ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo [信息] 启动时间: %DATE% %TIME%
echo [信息] 工作目录: %CD%
echo.
echo ══════════════════════════════════════════════════════════════════
echo                           系统检查
echo ══════════════════════════════════════════════════════════════════
echo.

REM 检查Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Python
    echo [提示] 请先安装Python 3.9+
    pause
    exit /b 1
)
echo [OK] Python: 已安装

REM 检查必要文件
if not exist "apps\dashboard\start_dashboard.py" (
    echo [错误] 找不到Dashboard启动文件
    pause
    exit /b 1
)
echo [OK] Dashboard文件: 存在

if not exist "database\data\tasks.db" (
    echo [警告] 数据库文件不存在，将自动创建
)
echo [OK] 数据库: 就绪

echo.
echo ══════════════════════════════════════════════════════════════════
echo                         安装依赖
echo ══════════════════════════════════════════════════════════════════
echo.
echo [提示] 正在检查依赖...

pip show requests >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [安装] requests库...
    pip install requests -q
)
echo [OK] requests: 已安装

pip show fastapi >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [安装] fastapi库...
    pip install fastapi uvicorn -q
)
echo [OK] fastapi: 已安装

echo.
echo ══════════════════════════════════════════════════════════════════
echo                         启动服务
echo ══════════════════════════════════════════════════════════════════
echo.
echo [启动] 任务所·Flow Dashboard
echo [端口] 8877
echo [地址] http://127.0.0.1:8877
echo.
echo ══════════════════════════════════════════════════════════════════
echo.
echo [提示] 按 Ctrl+C 停止服务
echo.
echo ══════════════════════════════════════════════════════════════════
echo.

cd apps\dashboard
python start_dashboard.py

pause

