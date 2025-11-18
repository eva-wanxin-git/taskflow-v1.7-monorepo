@echo off
chcp 65001 > nul
echo.
echo ═════════════════════════════════════════════
echo   🚀 重启任务所·Flow Dashboard (新端口)
echo ═════════════════════════════════════════════
echo.
echo 📍 当前位置: taskflow-v1.7-monorepo/apps/dashboard
echo 🎯 目标端口: 8878 (新端口，避免缓存)
echo ⏰ 启动时间: %date% %time%
echo.
echo ─────────────────────────────────────────────
echo 🔄 启动中...
echo ─────────────────────────────────────────────
echo.

python start_dashboard.py --port 8878

echo.
echo ─────────────────────────────────────────────
echo ✅ Dashboard已启动
echo ─────────────────────────────────────────────
echo.
echo 📱 访问地址: http://localhost:8878
echo 📋 测试步骤:
echo    1. 点击 "◉ ARCHITECT MONITOR"
echo    2. 查看Tab按钮：应该显示 "对话历史库"
echo    3. 点击 "对话历史库" Tab
echo    4. 测试会话列表、详情、搜索功能
echo.
echo 💡 提示: 如果仍显示旧内容，请按 Ctrl+F5 强制刷新
echo.
pause

