#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录扫描结果到Dashboard
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_scan_events():
    """添加扫描和更新事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "audit",
            "icon": "🔍",
            "content": "自动扫描：发现5个完成报告（REQ-001/002/003/006 + TASK-C-3）"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "data_update",
            "icon": "✅",
            "content": "数据库更新：5个任务状态确认为COMPLETED（REQ-002和TASK-C-3新更新）"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "🎊",
            "content": "完成统计：5个已完成（4个满分+1个60%），26个待处理，总工时20h已完成"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_complete",
            "icon": "🏆",
            "content": "李明成绩单：4个满分作品（REQ-001/003/006/TASK-C-3），1个优秀作品（REQ-002架构10分）"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} scan result events")
    return len(new_events)

def update_final_stats():
    """最终更新统计数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新Token
    data['token_usage']['used'] = 220000
    data['token_usage']['percentage'] = 22.0
    
    # 更新任务统计
    data['project_info']['pending_tasks'] = 26  # 31 - 5
    data['project_info']['completed_tasks'] = 5
    data['project_info']['completion_rate'] = round(5 / 31 * 100, 1)
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[OK] Stats updated:")
    print(f"     - Completed: 5 tasks (16.1%)")
    print(f"     - Pending: 26 tasks")
    print(f"     - Token: 220K (22.0%)")

def main():
    print("=" * 60)
    print("[Dashboard] Record scan results")
    print("=" * 60)
    print()
    
    count = add_scan_events()
    update_final_stats()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Scan results recorded")
    print("=" * 60)
    print(f"[Events] +{count} events (Total: 61+)")
    print(f"[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

