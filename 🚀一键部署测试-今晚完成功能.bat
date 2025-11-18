@echo off
chcp 65001 >nul
echo ============================================================
echo 一键部署测试 - 今晚完成的所有功能
echo ============================================================
echo.

cd /d "%~dp0"

echo [Step 1/6] 备份数据库...
python scripts/备份数据库.py
echo.

echo [Step 2/6] 启动API服务...
start "TaskFlow API" cmd /k "cd apps/api && python -m uvicorn src.main:app --host 0.0.0.0 --port 8870 --reload"
timeout /t 3 >nul
echo.

echo [Step 3/6] 启动Dashboard...
start "TaskFlow Dashboard" cmd /k "python apps/dashboard/start_dashboard.py"
timeout /t 5 >nul
echo.

echo [Step 4/6] 运行集成测试...
python tests/integration/test_all_features.py
echo.

echo [Step 5/6] 打开Dashboard验证...
start http://localhost:8877
echo.

echo [Step 6/6] 显示部署状态...
python scripts/显示部署状态.py
echo.

echo ============================================================
echo 部署完成！请在浏览器中验证所有功能
echo ============================================================
echo.
echo Dashboard: http://localhost:8877
echo API Docs: http://localhost:8870/docs
echo.
pause

