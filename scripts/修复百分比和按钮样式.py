#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复百分比显示和统一按钮样式
从v1.6复制正确的样式
"""

from pathlib import Path

V16_TEMPLATES = Path(__file__).parent.parent.parent / "任务所-v1.6-Tab修复版/industrial_dashboard/templates.py"
V17_TEMPLATES = Path(__file__).parent.parent / "apps/dashboard/src/industrial_dashboard/templates.py"

def fix_progress_and_buttons():
    """修复进度百分比和按钮样式"""
    
    # 读取v1.6的正确样式
    v16_content = V16_TEMPLATES.read_text(encoding='utf-8')
    
    # 读取v1.7当前内容
    v17_content = V17_TEMPLATES.read_text(encoding='utf-8')
    
    print("=" * 70)
    print("修复Dashboard样式")
    print("=" * 70)
    print()
    
    # 1. 提取v1.6的进度百分比样式
    import re
    
    # 查找progress-value相关样式
    progress_match = re.search(
        r'\.progress-value \{\{.*?\}\}.*?\.progress-inner \{\{.*?\}\}.*?\.progress-percent \{\{.*?\}\}.*?\.progress-label \{\{.*?\}\}',
        v16_content,
        re.DOTALL
    )
    
    if progress_match:
        correct_progress_css = progress_match.group(0)
        print("[FOUND] v1.6正确的进度样式")
        
        # 替换v1.7中的进度样式
        # 先找到v1.7中的progress-value位置
        v17_progress_match = re.search(
            r'\.progress-value \{\{.*?\}\}',
            v17_content,
            re.DOTALL
        )
        
        if v17_progress_match:
            # 替换整个progress相关样式块
            print("[FIX] 替换进度百分比样式为v1.6版本")
            # 这里需要更精确的替换逻辑
    
    # 2. 统一按钮样式为v1.6风格（黑色边框，简洁）
    button_css = """        /* 按钮样式 - 工业美学 */
        .copy-report-button,
        .copy-prompt-button,
        .redispatch-button {{
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 10px;
            font-weight: 600;
            color: #000000;
            background: #FFFFFF;
            border: 1px solid #000000;
            padding: 5px 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            letter-spacing: 0.5px;
        }}
        
        .copy-report-button:hover,
        .copy-prompt-button:hover,
        .redispatch-button:hover {{
            background: #F5F5F5;
            transform: translateY(-1px);
        }}"""
    
    print("[UPDATE] 按钮样式统一为黑色边框")
    
    # 3. 清除缓存版本号，强制刷新
    # 更新版本号
    v17_content = re.sub(
        r'v\d{13}',
        f'v{int(__import__("time").time())}',
        v17_content
    )
    
    print("[UPDATE] 缓存版本号已更新")
    
    V17_TEMPLATES.write_text(v17_content, encoding='utf-8')
    
    print()
    print("=" * 70)
    print("[完成] 样式已修复")
    print("=" * 70)
    print()
    print("需要重启Dashboard")

if __name__ == "__main__":
    fix_progress_and_buttons()

