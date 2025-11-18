@echo off
chcp 65001 >nul
echo.
echo 📊 Token使用状态
echo ================================
echo.

cd /d "%~dp0"
python packages\shared-utils\token_sync.py status

echo.
echo ================================
echo.
pause

