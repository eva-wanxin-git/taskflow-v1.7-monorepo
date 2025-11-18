@echo off
chcp 65001 >nul
echo.
echo 📝 手动录入Token工具
echo ================================
echo.

cd /d "%~dp0"

set /p TOKEN_VALUE="请输入当前Token值: "
set /p EVENT="事件描述 (可选，按回车跳过): "

if "%EVENT%"=="" set EVENT=手动录入

python packages\shared-utils\token_sync.py record %TOKEN_VALUE% "%EVENT%"

echo.
echo ================================
echo.
pause

