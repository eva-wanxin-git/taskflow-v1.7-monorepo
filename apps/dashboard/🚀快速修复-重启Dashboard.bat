@echo off
REM ============================================
REM Dashboard 快速修复脚本
REM 
REM 功能: 以正确的工作目录重启 Dashboard
REM ============================================

echo.
echo ====================================================================
echo 任务所·Flow v1.7 - Dashboard 快速修复
echo ====================================================================
echo.

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
echo [OK] 脚本目录: %SCRIPT_DIR%

REM 切换到 apps/dashboard 目录
cd /d "%SCRIPT_DIR%"
echo [OK] 工作目录已切换到: %cd%

REM 检查 automation-data 目录
if exist "automation-data" (
    echo [OK] automation-data 目录存在
) else (
    echo [ERROR] automation-data 目录不存在!
    echo [ERROR] 请确保在 apps/dashboard 目录下运行此脚本
    pause
    exit /b 1
)

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 未安装或不在 PATH 中
    pause
    exit /b 1
)
echo [OK] Python 已找到

REM 显示启动信息
echo.
echo ====================================================================
echo 启动 Dashboard...
echo ====================================================================
echo.
echo 访问地址: http://127.0.0.1:8877
echo 按 Ctrl+C 停止服务
echo.

REM 启动 Dashboard
python start_dashboard.py --port 8877

pause

