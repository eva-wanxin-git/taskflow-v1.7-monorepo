#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正Dashboard按钮样式 - 严格按照工业美学规范
"""

from pathlib import Path

TEMPLATES_FILE = Path(__file__).parent.parent / "apps/dashboard/src/industrial_dashboard/templates.py"

def fix_button_styles():
    """修正按钮样式为统一的工业美学风格"""
    
    content = TEMPLATES_FILE.read_text(encoding='utf-8')
    
    # 1. 修正按钮CSS - 统一为简洁样式
    old_button_css = """        .copy-report-button,
        .copy-prompt-button,
        .redispatch-button {{
            font-family: var(--font-chinese);
            font-size: 11px;
            font-weight: 600;
            color: var(--black);
            background: var(--white);
            border: 1px solid var(--black);
            padding: 6px 16px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .copy-prompt-button {{
            border-color: #537696;
            color: #537696;
        }}
        
        .redispatch-button {{
            border-color: #d97706;
            color: #d97706;
        }}
        
        .copy-report-button:hover,
        .copy-prompt-button:hover,
        .redispatch-button:hover {{
            background: var(--gray-100);
        }}"""
    
    new_button_css = """        .copy-report-button,
        .copy-prompt-button,
        .redispatch-button {{
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 10px;
            font-weight: 600;
            color: #000000;
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            padding: 5px 12px;
            border-radius: 0;
            cursor: pointer;
            transition: all 0.2s ease;
            letter-spacing: 0.5px;
        }}
        
        .copy-prompt-button {{
            color: #000000;
            border-color: #E0E0E0;
        }}
        
        .copy-report-button {{
            color: #000000;
            border-color: #E0E0E0;
        }}
        
        .redispatch-button {{
            color: #985239;
            border-color: #E0E0E0;
        }}
        
        .copy-report-button:hover,
        .copy-prompt-button:hover,
        .redispatch-button:hover {{
            background: #F5F5F5;
            border-color: #000000;
            transform: translateY(-1px);
        }}"""
    
    if old_button_css in content:
        content = content.replace(old_button_css, new_button_css)
        print("[FIX] 按钮CSS样式已修正为工业美学风格")
    else:
        print("[WARN] 未找到旧按钮CSS，可能已被修改")
    
    # 2. 修正按钮文字 - 使用统一符号
    # 待处理按钮
    content = content.replace(
        '▸ 一键复制提示词',
        '▸ 复制提示词'
    )
    
    # 已完成按钮
    content = content.replace(
        '▸ 一键复制完成报告',
        '▸ 复制报告'
    )
    
    # 重新派发按钮
    content = content.replace(
        '🔄 重新派发',
        '↻ 重新派发'
    )
    
    print("[FIX] 按钮文字已统一为简洁风格")
    
    # 3. 保存文件
    TEMPLATES_FILE.write_text(content, encoding='utf-8')
    
    print("[OK] templates.py已更新")
    print()
    print("需要重启Dashboard才能生效")

if __name__ == "__main__":
    fix_button_styles()

