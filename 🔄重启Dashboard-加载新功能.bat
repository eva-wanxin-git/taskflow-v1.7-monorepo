@echo off
chcp 65001 >nul
echo ============================================================
echo 重启Dashboard - 加载重新派发按钮
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/3] 停止旧的Dashboard进程...
taskkill /FI "WINDOWTITLE eq TaskFlow Dashboard*" /F 2>nul
timeout /t 2 /nobreak >nul
echo [OK] 已停止
echo.

echo [2/3] 切换到新端口8878（避免缓存）...
echo [OK] 新端口: 8878
echo.

echo [3/3] 启动Dashboard...
start "TaskFlow Dashboard" cmd /k "python apps/dashboard/start_dashboard.py"
timeout /t 3 /nobreak >nul
echo [OK] Dashboard已启动
echo.

echo ============================================================
echo Dashboard已重启！
echo ============================================================
echo.
echo 新地址: http://localhost:8878
echo.
echo 新功能:
echo   - 进行中任务显示 "🔄 重新派发" 按钮
echo   - 点击可复制提示词重新派发
echo   - 可选重置状态为pending
echo.
echo 按任意键打开浏览器...
pause >nul

start http://localhost:8878

echo.
echo ============================================================

