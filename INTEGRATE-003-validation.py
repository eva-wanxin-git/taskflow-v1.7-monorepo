#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
INTEGRATE-003 集成验证脚本
验证Token同步功能和对话历史库是否完整集成到Dashboard

验证项：
1. Dashboard API是否有4个对话历史库端点
2. Token同步API是否支持sync_type参数
3. 对话历史库数据文件是否存在并有效
4. Dashboard UI是否包含Token同步按钮和对话历史库Tab
5. 前端JavaScript是否正确加载会话数据
6. Token历史记录是否正确存储
"""

import json
from pathlib import Path
import sys
import re

def check_api_endpoints():
    """检查Dashboard API端点是否完整"""
    print("\n" + "="*60)
    print("【检查1】API端点完整性")
    print("="*60)
    
    dashboard_file = Path("apps/dashboard/src/industrial_dashboard/dashboard.py")
    if not dashboard_file.exists():
        print("❌ dashboard.py不存在")
        return False
    
    with open(dashboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_endpoints = {
        "record_token_usage": r"async def record_token_usage",
        "get_conversations": r"async def get_conversations",
        "get_conversation_detail": r"async def get_conversation\(",
        "create_conversation": r"async def create_conversation",
        "add_message": r"async def add_message"
    }
    
    results = {}
    for name, pattern in required_endpoints.items():
        exists = bool(re.search(pattern, content))
        results[name] = exists
        status = "✅" if exists else "❌"
        print(f"{status} {name}")
    
    all_passed = all(results.values())
    print(f"\n汇总: {sum(results.values())}/{len(results)} 端点存在")
    return all_passed

def check_token_sync_features():
    """检查Token同步功能是否完整"""
    print("\n" + "="*60)
    print("【检查2】Token同步功能完整性")
    print("="*60)
    
    dashboard_file = Path("apps/dashboard/src/industrial_dashboard/dashboard.py")
    with open(dashboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    features = {
        "sync_type参数": r'sync_type.*=.*data\.get\("sync_type"',
        "manual模式": r'if sync_type == "manual"',
        "auto模式": r'else:.*monitor_data\["token_usage"\]\["used"\] \+=',
        "增量计算": r'increment = tokens -',
        "事件流记录": r'new_event.*=.*\{.*token_usage',
        "会话历史": r'monitor_data\["token_usage"\]\["sessions"\]'
    }
    
    results = {}
    for name, pattern in features.items():
        exists = bool(re.search(pattern, content, re.DOTALL))
        results[name] = exists
        status = "✅" if exists else "❌"
        print(f"{status} {name}")
    
    all_passed = all(results.values())
    print(f"\n汇总: {sum(results.values())}/{len(results)} 功能存在")
    return all_passed

def check_data_files():
    """检查数据文件是否存在"""
    print("\n" + "="*60)
    print("【检查3】数据文件完整性")
    print("="*60)
    
    required_files = {
        "对话历史库数据": "automation-data/architect-conversations.json",
        "Token监控数据": "automation-data/architect_monitor.json",
        "事件流数据": "automation-data/architect_events.json"
    }
    
    results = {}
    for name, filepath in required_files.items():
        path = Path(filepath)
        exists = path.exists()
        results[name] = exists
        status = "✅" if exists else "❌"
        print(f"{status} {name}: {filepath}")
        
        if exists:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # 基本验证
                if "sessions" in data:
                    print(f"   └─ 包含{len(data.get('sessions', []))}个会话")
                elif "token_usage" in data:
                    print(f"   └─ Token已使用: {data['token_usage'].get('used', 0):,}")
                elif "events" in data:
                    print(f"   └─ 包含{len(data.get('events', []))}个事件")
            except json.JSONDecodeError:
                print(f"   └─ ⚠️ JSON格式错误")
    
    all_passed = all(results.values())
    print(f"\n汇总: {sum(results.values())}/{len(results)} 数据文件存在")
    return all_passed

def check_ui_components():
    """检查Dashboard UI组件"""
    print("\n" + "="*60)
    print("【检查4】Dashboard UI组件")
    print("="*60)
    
    templates_file = Path("apps/dashboard/src/industrial_dashboard/templates.py")
    if not templates_file.exists():
        print("❌ templates.py不存在")
        return False
    
    with open(templates_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    ui_components = {
        "Token同步按钮": r'🔄.*同步|class.*sync.*button',
        "对话历史库Tab": r'对话历史库',
        "会话列表": r'class.*conversation-list',
        "会话详情": r'class.*conversation-detail|conversation-sidebar',
        "搜索框": r'class.*conversation-search',
        "消息样式": r'class.*conversation-message',
        "Token同步对话框": r'showTokenSyncDialog|token.*modal'
    }
    
    results = {}
    for name, pattern in ui_components.items():
        exists = bool(re.search(pattern, content, re.IGNORECASE))
        results[name] = exists
        status = "✅" if exists else "❌"
        print(f"{status} {name}")
    
    all_passed = all(results.values())
    print(f"\n汇总: {sum(results.values())}/{len(results)} UI组件存在")
    return all_passed

def check_javascript_functions():
    """检查前端JavaScript函数"""
    print("\n" + "="*60)
    print("【检查5】JavaScript函数完整性")
    print("="*60)
    
    templates_file = Path("apps/dashboard/src/industrial_dashboard/templates.py")
    with open(templates_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    js_functions = {
        "加载会话": r'function.*loadConversations|loadConversations\s*\(\)',
        "渲染列表": r'function.*renderConversationList|renderConversationList\s*\(\)',
        "选择会话": r'function.*selectSession|selectSession\s*\(',
        "过滤搜索": r'function.*filterSessions|filterSessions\s*\(',
        "Token同步": r'function.*syncToken|showTokenSyncDialog',
        "格式化数字": r'function.*formatNumber|formatNumber\s*\(',
        "格式化日期": r'function.*formatDate|formatDate\s*\('
    }
    
    results = {}
    for name, pattern in js_functions.items():
        exists = bool(re.search(pattern, content, re.IGNORECASE))
        results[name] = exists
        status = "✅" if exists else "❌"
        print(f"{status} {name}")
    
    all_passed = all(results.values())
    print(f"\n汇总: {sum(results.values())}/{len(results)} JS函数存在")
    return all_passed

def check_token_history():
    """检查Token历史记录是否正确存储"""
    print("\n" + "="*60)
    print("【检查6】Token历史记录存储")
    print("="*60)
    
    monitor_file = Path("automation-data/architect_monitor.json")
    if not monitor_file.exists():
        print("❌ architect_monitor.json不存在")
        return False
    
    try:
        with open(monitor_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查结构
        checks = {
            "token_usage字段": "token_usage" in data,
            "sessions字段": "sessions" in data.get("token_usage", {}),
            "used字段": "used" in data.get("token_usage", {}),
            "total字段": "total" in data.get("token_usage", {}),
            "sessions非空": len(data.get("token_usage", {}).get("sessions", [])) > 0
        }
        
        results = {}
        for name, exists in checks.items():
            results[name] = exists
            status = "✅" if exists else "⚠️" if "非空" not in name else "ℹ️"
            print(f"{status} {name}")
            
            if name == "sessions非空" and exists:
                sessions = data["token_usage"]["sessions"]
                print(f"   └─ 最近记录: {sessions[0] if sessions else 'N/A'}")
        
        all_passed = all([v for k, v in results.items() if "非空" not in k]) and results.get("sessions非空", False)
        print(f"\n汇总: {'✅ 数据结构完整' if all_passed else '⚠️ 需检查数据'}")
        return all_passed
    except Exception as e:
        print(f"❌ 数据文件错误: {e}")
        return False

def generate_report():
    """生成完整报告"""
    print("\n" + "="*60)
    print("【综合验证结果】")
    print("="*60)
    
    all_results = {
        "API端点": check_api_endpoints(),
        "Token同步功能": check_token_sync_features(),
        "数据文件": check_data_files(),
        "UI组件": check_ui_components(),
        "JavaScript函数": check_javascript_functions(),
        "Token历史记录": check_token_history()
    }
    
    print("\n" + "="*60)
    print("【最终结论】")
    print("="*60)
    
    passed = sum(1 for v in all_results.values() if v)
    total = len(all_results)
    
    print(f"\n验证通过: {passed}/{total}")
    print("\n详细结果:")
    for name, result in all_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status} {name}")
    
    if passed == total:
        print("\n🎉 恭喜！REQ-006功能已完整集成到Dashboard")
        print("\n后续操作:")
        print("  1. 启动Dashboard: python apps/dashboard/start_dashboard.py")
        print("  2. 访问浏览器: http://localhost:8877")
        print("  3. 测试Token同步按钮和对话历史库Tab")
        return True
    else:
        print("\n⚠️ 有部分功能未完成，请检查上面的详细结果")
        return False

if __name__ == "__main__":
    print("\n" + "🔍 INTEGRATE-003 集成验证 ".center(60, "="))
    print("验证Token同步功能和对话历史库是否完整集成到Dashboard")
    print("="*60)
    
    success = generate_report()
    sys.exit(0 if success else 1)

