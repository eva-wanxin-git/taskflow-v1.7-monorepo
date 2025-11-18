#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录紧急Bug到Dashboard
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_bug_events():
    """添加Bug事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "bug_report",
            "icon": "🚨",
            "content": "紧急Bug：全栈工程师任务列表显示Loading...，无法加载"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_create",
            "icon": "🔧",
            "content": "创建紧急任务：BUG-001（任务列表加载失败，1h，P0）→ 李明"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "diagnosis",
            "icon": "🔍",
            "content": "可能原因：任务metadata格式错误/数据量大/API错误/JavaScript错误"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} bug events")

def main():
    print("=" * 60)
    print("[CRITICAL] Record bug to Dashboard")
    print("=" * 60)
    print()
    
    add_bug_events()
    
    print()
    print("=" * 60)
    print("[URGENT] Bug recorded and task created")
    print("=" * 60)
    print("[Bug] Task list loading failure")
    print("[Task] BUG-001 created and dispatched")
    print("[Dashboard] Will update when restarted")

if __name__ == "__main__":
    main()

