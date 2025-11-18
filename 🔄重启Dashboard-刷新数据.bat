@echo off
echo ==========================================
echo   重启Dashboard - 刷新108个功能数据
echo ==========================================
echo.
echo 正在重启Dashboard...
echo 端口: 8877
echo.

cd /d "%~dp0apps\dashboard"

echo 步骤1: 停止旧进程（如果有）
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Dashboard*" 2>nul

timeout /t 2 /nobreak >nul

echo.
echo 步骤2: 启动Dashboard
echo.
python start_dashboard.py

pause

