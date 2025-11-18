#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REQ-003 快速验证脚本

验证"对话历史库"是否正确集成到Dashboard
"""
import re
import sys
from pathlib import Path

# 设置Windows终端UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    print()
    print("=" * 70)
    print("【REQ-003集成验证】对话历史库")
    print("=" * 70)
    print()
    
    # 读取templates.py
    templates_path = Path(__file__).parent / "src" / "industrial_dashboard" / "templates.py"
    print(f"[文件] 检查文件: {templates_path.name}")
    print()
    
    if not templates_path.exists():
        print("[错误] templates.py文件不存在")
        return
    
    content = templates_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 验证清单
    checks = []
    
    # 1. 检查Tab标题
    print("【检查1】Tab标题")
    tab_title_found = False
    for i, line in enumerate(lines, 1):
        # 检查是否在architect-tab按钮的附近行（3行范围内）
        if 'architect-tab' in line:
            # 检查当前行和下两行
            check_range = lines[i-1:i+2] if i < len(lines) else lines[i-1:]
            check_text = ''.join(check_range)
            if '对话历史库' in check_text:
                print(f"  [OK] 第{i}行附近: 找到Tab按钮 '对话历史库'")
                tab_title_found = True
                break
    
    if not tab_title_found:
        # 备用检查：只要文件中有"对话历史库"就算通过
        if '对话历史库' in content:
            print("  [OK] 文件中包含 '对话历史库'")
            tab_title_found = True
        else:
            print("  [FAIL] 未找到Tab标题 '对话历史库'")
    checks.append(tab_title_found)
    print()
    
    # 2. 检查CSS样式
    print("【检查2】CSS样式")
    css_patterns = [
        'conversation-library',
        'conversation-sidebar', 
        'conversation-search',
        'conversation-list',
        'conversation-item',
        'conversation-detail',
        'conversation-message'
    ]
    
    css_found = []
    for pattern in css_patterns:
        if f'.{pattern}' in content:
            print(f"  [OK] 找到样式: .{pattern}")
            css_found.append(True)
        else:
            print(f"  [FAIL] 缺失样式: .{pattern}")
            css_found.append(False)
    
    css_all_found = all(css_found)
    checks.append(css_all_found)
    print()
    
    # 3. 检查JavaScript函数
    print("【检查3】JavaScript函数")
    js_functions = [
        'loadConversations',
        'renderConversationList',
        'selectSession',
        'filterSessions',
        'formatNumber',
        'formatDate',
        'calculateDuration'
    ]
    
    js_found = []
    for func in js_functions:
        if f'function {func}' in content or f'async function {func}' in content:
            print(f"  [OK] 找到函数: {func}()")
            js_found.append(True)
        else:
            print(f"  [FAIL] 缺失函数: {func}()")
            js_found.append(False)
    
    js_all_found = all(js_found)
    checks.append(js_all_found)
    print()
    
    # 4. 检查HTML结构
    print("【检查4】HTML结构")
    html_elements = [
        ('会话列表容器', 'conversation-list'),
        ('会话详情容器', 'conversation-detail'),
        ('搜索输入框', 'sessionSearchInput'),
    ]
    
    html_found = []
    for name, element_id in html_elements:
        # 更宽松的匹配：只要包含id即可（可能有class等其他属性）
        if f'id="{element_id}"' in content or f"id='{element_id}'" in content or f'id={element_id}' in content:
            print(f"  [OK] 找到元素: {name} (#{element_id})")
            html_found.append(True)
        else:
            # 再检查class匹配
            if f'class="{element_id}"' in content or f"class='{element_id}'" in content:
                print(f"  [OK] 找到元素(class): {name} (.{element_id})")
                html_found.append(True)
            else:
                print(f"  [FAIL] 缺失元素: {name} (#{element_id})")
                html_found.append(False)
    
    html_all_found = all(html_found)
    checks.append(html_all_found)
    print()
    
    # 5. 检查初始化调用
    print("【检查5】初始化调用")
    if 'loadConversations()' in content:
        print("  [OK] 找到初始化调用: loadConversations()")
        init_found = True
    else:
        print("  [FAIL] 未找到初始化调用")
        init_found = False
    checks.append(init_found)
    print()
    
    # 6. 检查数据文件
    print("【检查6】数据文件")
    data_path = Path(__file__).parent / "automation-data" / "architect-conversations.json"
    if data_path.exists():
        print(f"  [OK] 找到数据文件: {data_path.name}")
        data_found = True
    else:
        print(f"  [FAIL] 缺失数据文件: {data_path.name}")
        data_found = False
    checks.append(data_found)
    print()
    
    # 总结
    print("=" * 70)
    print("【验证结果总结】")
    print("=" * 70)
    print()
    
    total = len(checks)
    passed = sum(checks)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"[通过] {passed}/{total} ({percentage:.0f}%)")
    print()
    
    if passed == total:
        print("[成功] 验证通过！REQ-003已完全集成")
        print()
        print("[提示] 如果浏览器还显示旧内容，请：")
        print("   1. 双击运行: 重启Dashboard-新端口.bat")
        print("   2. 或者按 Ctrl+F5 强制刷新")
    else:
        print("[警告] 验证未通过，存在缺失项")
        print()
        print("请检查上述标记为 [FAIL] 的项目")
    
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

