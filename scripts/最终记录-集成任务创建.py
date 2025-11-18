#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终记录 - 集成任务创建和派发
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_integration_task_events():
    """添加集成任务创建事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "issue_found",
            "icon": "🚨",
            "content": "用户指出：Dashboard Tab还叫'对话交流'，应该是'对话历史库'！"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "diagnosis",
            "icon": "🔍",
            "content": "诊断：REQ-003代码写了，但没有替换templates.py中的旧Tab代码"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_create",
            "icon": "🔧",
            "content": "创建集成任务：INTEGRATE-001/003/006（各1h，P0）→ 李明"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_dispatch",
            "icon": "📤",
            "content": "派发紧急任务：3个集成任务派发给李明，确保用户能实际使用功能"
        },
        {
            "id": f"event-{len(data['events']) + 5:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "📊",
            "content": "任务总数更新：34个（5已完成+29待处理），新增3个集成任务"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} integration task events")
    return len(new_events)

def update_final_monitor():
    """最终更新监控数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新Token
    data['token_usage']['used'] = 224000
    data['token_usage']['percentage'] = 22.4
    
    # 更新任务数
    data['project_info']['pending_tasks'] = 29  # 26 + 3
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[OK] Monitor: Token 224K (22.4%), Pending 29")

def main():
    print("=" * 60)
    print("[Dashboard] Final record - Integration tasks")
    print("=" * 60)
    print()
    
    count = add_integration_task_events()
    update_final_monitor()
    
    print()
    print("=" * 60)
    print("[COMPLETE] All work recorded")
    print("=" * 60)
    print(f"[Events] +{count} events (Total: 70+)")
    print(f"[Tasks] 34 total (5 completed + 29 pending)")
    print(f"[Token] 224K/1M (22.4%)")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

