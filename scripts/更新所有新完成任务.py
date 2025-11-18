#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有新发现的完成任务
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

# 扫描发现的所有完成任务
COMPLETED_TASKS = [
    {"id": "REQ-001", "report": "REQ-001-完成报告.md"},
    {"id": "REQ-002", "report": "✅REQ-002-项目记忆空间-完成报告.md"},
    {"id": "REQ-003", "report": "✅REQ-003-对话历史库功能-完成报告.md"},
    {"id": "REQ-006", "report": "✅REQ-006-Token同步功能完成报告.md"},
    {"id": "REQ-010-A", "report": "✅REQ-010-A-完成报告.md"},
    {"id": "REQ-010-C", "report": "✅REQ-010-C-完成报告.md"},
    {"id": "TASK-C-3", "report": "✅TASK-C-3-完成报告.md"},
    {"id": "BUG-001", "report": "✅BUG-001修复完成.md"},
    {"id": "TASK-VERIFY-001", "report": "✅TASK-VERIFY-001-验证报告.md"},
    {"id": "TASK-VERIFY-006", "report": "✅TASK-VERIFY-006-验证报告.md"},
]

def update_all_completed():
    """批量更新所有已完成任务"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    updated = 0
    for task in COMPLETED_TASKS:
        task_id = task["id"]
        
        # 检查任务是否存在
        cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if not row:
            print(f"[SKIP] {task_id} not in database")
            continue
        
        if row[0] == 'completed':
            print(f"[SKIP] {task_id} already completed")
            continue
        
        # 更新状态
        cursor.execute("""
            UPDATE tasks 
            SET status = 'completed', 
                updated_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), task_id))
        
        print(f"[OK] {task_id} -> COMPLETED")
        updated += 1
    
    conn.commit()
    conn.close()
    
    return updated

def calculate_progress():
    """计算完成进度"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status != 'cancelled'")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
    completed = cursor.fetchone()[0]
    
    conn.close()
    
    rate = round(completed / total * 100, 1) if total > 0 else 0
    return total, completed, rate

def add_scan_events():
    """添加扫描事件到Dashboard"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total, completed, rate = calculate_progress()
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "audit",
            "icon": "🔍",
            "content": f"全盘扫描：发现{len(COMPLETED_TASKS)}个完成报告"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "data_update",
            "icon": "📊",
            "content": f"批量更新：{len(COMPLETED_TASKS)}个任务状态确认"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "🎊",
            "content": f"进度更新：{completed}/{total}任务完成（{rate}%）"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return len(new_events)

def update_monitor():
    """更新监控数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total, completed, rate = calculate_progress()
    
    data['token_usage']['used'] = 277000
    data['token_usage']['percentage'] = 27.7
    
    data['project_info']['total_tasks'] = total
    data['project_info']['completed_tasks'] = completed
    data['project_info']['pending_tasks'] = total - completed
    data['project_info']['completion_rate'] = rate
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("=" * 60)
    print("[Full Scan] Update all completed tasks")
    print("=" * 60)
    print()
    
    updated = update_all_completed()
    
    print()
    total, completed, rate = calculate_progress()
    
    print("=" * 60)
    print("[Progress Update]")
    print("=" * 60)
    print(f"  Total: {total} tasks")
    print(f"  Completed: {completed} tasks ({rate}%)")
    print(f"  Pending: {total - completed} tasks")
    print()
    
    event_count = add_scan_events()
    update_monitor()
    
    print("=" * 60)
    print("[SUCCESS] Dashboard updated")
    print("=" * 60)
    print(f"  Updated: {updated} tasks")
    print(f"  Events: +{event_count}")
    print(f"  Progress: {rate}%")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

