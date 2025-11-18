@echo off
chcp 65001 >nul
title 智能任务检测器
echo ============================================================
echo 启动智能任务检测器 v2.0
echo ============================================================
echo.

cd /d "%~dp0"

echo [检测] 检查依赖...
python -c "import watchdog" 2>nul
if %errorlevel% neq 0 (
    echo [安装] 安装watchdog...
    pip install watchdog -q
)
echo [OK] 依赖就绪
echo.

echo ============================================================
echo 智能检测规则:
echo   1. 派发文档创建 ^-^> 记录最近任务
echo   2. 代码频繁修改 ^-^> 检测编码活动  
echo   3. 自动关联推断 ^-^> 更新任务状态
echo   4. 完成报告创建 ^-^> 自动标记完成
echo.
echo 触发条件:
echo   - 5秒内3次修改 = 正在编码
echo   - 10分钟内派发 = 相关任务
echo ============================================================
echo.

python services/smart_task_detector.py

pause

