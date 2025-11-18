@echo off
REM 运行架构师API端到端测试
REM 用法: 双击运行或在命令行执行

echo ================================================================
echo 架构师API - 端到端测试套件
echo ================================================================
echo.

REM 切换到项目根目录
cd /d "%~dp0\..\..\"

echo 当前目录: %CD%
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    echo 请访问 https://www.python.org/downloads/ 下载安装
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo [警告] pytest未安装，正在安装...
    pip install pytest fastapi httpx pydantic
)

python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [警告] fastapi未安装，正在安装...
    pip install fastapi httpx
)

echo [2/3] 运行测试...
echo.

REM 运行测试
python -m pytest tests\e2e\test_architect_api_e2e.py -v --tb=short

REM 保存退出码
set TEST_EXIT_CODE=%errorlevel%

echo.
echo ================================================================

if %TEST_EXIT_CODE% == 0 (
    echo [成功] 所有测试通过！
    echo.
    echo 生成的测试报告位于: tests\e2e\
) else (
    echo [失败] 部分测试未通过，请查看上方错误信息
)

echo ================================================================
echo.

pause
exit /b %TEST_EXIT_CODE%

