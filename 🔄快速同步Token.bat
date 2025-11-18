@echo off
chcp 65001 >nul
echo.
echo ⚡ Token快速同步工具
echo ================================
echo.
echo 使用方法：
echo 1. 在Cursor中，查看右下角状态栏的Token数字
echo 2. 选中数字并复制（Ctrl+C）
echo 3. 运行此脚本
echo.
echo 按任意键开始同步...
pause >nul

cd /d "%~dp0"
python packages\shared-utils\token_sync.py quick

echo.
echo ================================
echo.
pause

