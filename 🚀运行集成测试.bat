@echo off
REM -*- coding: utf-8 -*-
REM 🚀 运行集成测试脚本 - INTEGRATE-007
REM 
REM 用途: 快速运行任务所·Flow v1.7的E2E集成测试
REM 
REM 使用:
REM   运行所有测试: 🚀运行集成测试.bat
REM   运行E2E测试: 🚀运行集成测试.bat e2e
REM   运行集成测试: 🚀运行集成测试.bat integration

cd /d %~dp0

echo.
echo ===============================================================================
echo 🎯 任务所·Flow v1.7 - E2E集成测试运行器
echo 任务ID: INTEGRATE-007
echo ===============================================================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python或检查PATH配置
    pause
    exit /b 1
)

REM 检查依赖
echo ✓ 检查依赖...

python -m pip show pytest >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pytest未安装，正在安装...
    python -m pip install pytest fastapi httpx requests -q
)

REM 初始化数据库（如果需要）
if not exist "database\data\tasks.db" (
    echo ⚠️  数据库不存在，正在初始化...
    python database/migrations/migrate.py init
)

echo.
echo ===============================================================================
echo 运行测试...
echo ===============================================================================
echo.

REM 根据参数选择运行的测试
if "%1"=="" (
    echo 运行所有测试...
    python tests/run_integration_tests.py
) else if "%1"=="e2e" (
    echo 运行E2E测试...
    python tests/run_integration_tests.py --suite e2e
) else if "%1"=="integration" (
    echo 运行集成测试...
    python tests/run_integration_tests.py --suite integration
) else (
    echo 未知参数: %1
    echo 用法: 🚀运行集成测试.bat [all^|e2e^|integration]
    pause
    exit /b 1
)

echo.
echo ===============================================================================
echo ✅ 测试完成
echo ===============================================================================
echo.
echo 查看测试报告: tests/reports/integration_test_report_*.json
echo.

pause
