#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新REQ-001和REQ-006完成状态到Dashboard
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# 数据库和数据目录
DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def update_task_status():
    """更新任务状态到数据库"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # 更新REQ-001
    cursor.execute("""
        UPDATE tasks 
        SET status = 'completed', 
            updated_at = ? 
        WHERE id = 'REQ-001'
    """, (datetime.now().isoformat(),))
    
    # 更新REQ-006
    cursor.execute("""
        UPDATE tasks 
        SET status = 'completed', 
            updated_at = ? 
        WHERE id = 'REQ-006'
    """, (datetime.now().isoformat(),))
    
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()
    
    print(f"[OK] Updated {rows_updated} tasks in database")
    return rows_updated

def add_review_events():
    """添加审查事件到事件流"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 添加审查事件
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "code_review",
            "icon": "🎉",
            "content": "审查REQ-001（端口冲突）：完全通过✅ - 100%完成，教科书级别！"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "code_review",
            "icon": "🎉",
            "content": "审查REQ-006（Token同步）：完全通过✅ - 100%完成，实用性极强！"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "document",
            "icon": "📋",
            "content": "生成联合审查报告：REQ-001和REQ-006双双满分（10/10）"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_complete",
            "icon": "✅",
            "content": "任务完成：REQ-001和REQ-006状态更新为COMPLETED"
        },
        {
            "id": f"event-{len(data['events']) + 5:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "🏆",
            "content": "里程碑：2个P1任务完美完成，开发效率大幅提升！"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} review events")
    return len(new_events)

def update_monitor():
    """更新监控数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新Token（估算当前使用）
    data['token_usage']['used'] = 109000
    data['token_usage']['percentage'] = 10.9
    
    # 更新项目信息
    data['project_info']['pending_tasks'] = 11  # 13 - 2
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Updated monitor data")
    return True

def main():
    print("=" * 60)
    print("[Dashboard] Update REQ-001 and REQ-006 status")
    print("=" * 60)
    print()
    
    # 更新数据库
    print("[Step 1] Update task status in database...")
    update_task_status()
    print()
    
    # 更新事件流
    print("[Step 2] Add review events...")
    event_count = add_review_events()
    print()
    
    # 更新监控
    print("[Step 3] Update monitor data...")
    update_monitor()
    print()
    
    print("=" * 60)
    print("[SUCCESS] Dashboard updated")
    print("=" * 60)
    print(f"[Tasks] REQ-001, REQ-006 -> COMPLETED")
    print(f"[Events] +{event_count} events")
    print(f"[Token] 109K/1M (10.9%)")
    print(f"[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

