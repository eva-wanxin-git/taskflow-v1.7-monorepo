#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录REQ-007取消到Dashboard
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_cancel_events():
    """添加任务取消事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "user_feedback",
            "icon": "💬",
            "content": "用户确认：REQ-004和REQ-007重复，保留REQ-004"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_cancel",
            "icon": "🗑️",
            "content": "取消重复任务：REQ-007和TASK-USER-007，理由：与REQ-004（即插即用封装包）功能重复"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "📊",
            "content": "任务清理：36个总任务 → 34个有效任务（5完成+29待处理+2取消）"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} cancel events")
    return len(new_events)

def update_monitor():
    """更新监控数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新任务数（减去取消的2个）
    data['project_info']['pending_tasks'] = 29  # 31 - 2
    data['project_info']['cancelled_tasks'] = 2
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[OK] Monitor updated: Pending 29, Cancelled 2")

def main():
    print("=" * 60)
    print("[Dashboard] Record REQ-007 cancellation")
    print("=" * 60)
    print()
    
    count = add_cancel_events()
    update_monitor()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Cancellation recorded")
    print("=" * 60)
    print(f"[Events] +{count} events")
    print(f"[Total Tasks] 34 active (5 completed + 29 pending)")
    print(f"[Cancelled] 2 tasks (REQ-007, USER-007)")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

