@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   任务所·Flow v1.7 - 一键启动
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 启动 Dashboard (任务看板)...
start "任务所-Dashboard" cmd /k "cd apps\dashboard && python start_dashboard.py"
timeout /t 2 >nul

echo [2/2] Dashboard 已启动！
echo.
echo ========================================
echo   ✅ 启动完成
echo ========================================
echo.
echo 📊 Dashboard (任务看板):
echo    http://localhost:8871
echo.
echo 💡 提示: 
echo    - 浏览器打开上述地址即可查看
echo    - 关闭此窗口不会停止服务
echo    - 要停止服务，关闭弹出的命令窗口
echo.
echo ⚠️  注意:
echo    - API服务(8870)暂未实现，需要完成TASK-C-1
echo    - 当前仅Dashboard可用
echo.

start http://localhost:8871

pause

