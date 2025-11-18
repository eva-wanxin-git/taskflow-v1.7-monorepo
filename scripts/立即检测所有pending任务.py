#!/usr/bin/env python3
"""
立即检测所有pending集成任务，自动更新为in_progress
适用于：派发文档已发出，执行者已开始工作
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
EVENTS_FILE = Path(__file__).parent.parent / "apps/dashboard/automation-data/architect_events.json"

def auto_start_pending_integrations():
    """自动启动所有pending的集成任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 查询所有pending的集成任务
    cursor.execute("""
        SELECT id, title FROM tasks 
        WHERE status = 'pending' 
        AND id LIKE 'INTEGRATE-%'
        ORDER BY id
    """)
    
    tasks = cursor.fetchall()
    
    print("Found", len(tasks), "pending INTEGRATE tasks")
    print()
    
    updated = 0
    
    for task_id, title in tasks:
        print(f"Update {task_id} to in_progress")
        
        cursor.execute("""
            UPDATE tasks 
            SET status = 'in_progress', updated_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), task_id))
        
        updated += 1
    
    conn.commit()
    conn.close()
    
    # 记录事件
    if updated > 0:
        try:
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {"events": []}
        
        event = {
            "id": f"event-{len(data.get('events', [])) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "auto_batch_start",
            "icon": "🤖",
            "content": f"Auto-started {updated} pending INTEGRATE tasks"
        }
        
        data.setdefault("events", []).append(event)
        
        with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"Updated {updated} tasks to in_progress")
    print("Dashboard: http://localhost:8877")
    
    return updated

if __name__ == "__main__":
    auto_start_pending_integrations()

