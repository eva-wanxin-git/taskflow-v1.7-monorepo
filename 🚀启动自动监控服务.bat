@echo off
chcp 65001 >nul
echo ============================================================
echo 启动任务自动监控服务
echo ============================================================
echo.

cd /d "%~dp0"

echo [检查] 检查watchdog库是否安装...
python -c "import watchdog" 2>nul
if %errorlevel% neq 0 (
    echo [安装] watchdog库未安装，正在安装...
    pip install watchdog -q
    echo [完成] watchdog库安装完成
) else (
    echo [OK] watchdog库已安装
)
echo.

echo [启动] 启动自动监控服务...
echo.
echo 监控范围:
echo   - 派发文档 (自动检测任务开始)
echo   - 完成报告 (自动检测任务完成)
echo.
echo 自动化功能:
echo   1. 派发文档打开15秒 → 自动标记"进行中"
echo   2. 完成报告创建 → 自动标记"已完成"
echo   3. 每30秒智能检测状态异常
echo.
echo ============================================================
echo 服务启动中...
echo ============================================================
echo.

python services/task_auto_monitor.py

pause

