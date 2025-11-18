#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录派发TASK-C动作到Dashboard
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_dispatch_events():
    """添加派发事件到事件流"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 添加派发事件
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_dispatch",
            "icon": "📤",
            "content": "派发任务：TASK-C-1（创建FastAPI主入口）→ 李明（2h）"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_dispatch",
            "icon": "📤",
            "content": "派发任务：TASK-C-2（集成数据库）→ 李明（3h, depends on C-1）"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_dispatch",
            "icon": "📤",
            "content": "派发任务：TASK-C-3（E2E测试）→ 李明（1.5h, depends on C-1,C-2）"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "document",
            "icon": "📋",
            "content": "生成派发文档：📤派发给李明-TASK-C系列.md（完整提示词+验收标准）"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} dispatch events")
    return len(new_events)

def main():
    print("=" * 60)
    print("[Dashboard] Record dispatch actions")
    print("=" * 60)
    print()
    
    count = add_dispatch_events()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Dashboard updated")
    print("=" * 60)
    print(f"[Events] +{count} events")
    print(f"[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

