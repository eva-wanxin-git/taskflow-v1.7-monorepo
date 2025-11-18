@echo off
chcp 65001 >nul
echo.
echo 🧪 Token同步功能演示
echo ================================
echo.

cd /d "%~dp0"

echo 【1】查看当前状态
echo --------------------------------
python packages\shared-utils\token_sync.py status
echo.

echo 【2】记录Token使用
echo --------------------------------
python packages\shared-utils\token_sync.py record 100000 "演示测试"
echo.

echo 【3】再次查看状态
echo --------------------------------
python packages\shared-utils\token_sync.py status
echo.

echo ================================
echo ✅ 演示完成！
echo.
echo 提示：
echo - 使用 🔄快速同步Token.bat 从剪贴板同步
echo - 使用 🔢手动录入Token.bat 交互式录入
echo - 使用 📊查看Token状态.bat 查看当前状态
echo.
pause

