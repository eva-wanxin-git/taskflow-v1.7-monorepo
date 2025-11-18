#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新当前正在执行的任务状态
用于监控服务启动前已经在执行的任务
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
EVENTS_FILE = Path(__file__).parent.parent / "apps/dashboard/automation-data/architect_events.json"

# 当前正在执行的任务（需要手动确认）
ACTIVE_TASKS = [
    {"id": "INTEGRATE-003", "executor": "fullstack-engineer"},
    {"id": "INTEGRATE-006", "executor": "fullstack-engineer"},  
    {"id": "INTEGRATE-007", "executor": "fullstack-engineer"},
    {"id": "INTEGRATE-012", "executor": "architect"},
]

def batch_update():
    """批量更新状态"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updated = 0
    
    for task in ACTIVE_TASKS:
        task_id = task["id"]
        executor = task["executor"]
        
        # 检查当前状态
        cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
        result = cursor.fetchone()
        
        if result:
            current_status = result[0]
            if current_status != "in_progress":
                # 更新为进行中
                cursor.execute("""
                    UPDATE tasks 
                    SET status = 'in_progress', 
                        assigned_to = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (executor, datetime.now().isoformat(), task_id))
                
                print(f"[UPDATE] {task_id}: {current_status} -> in_progress")
                updated += 1
            else:
                print(f"[SKIP] {task_id}: 已经是 in_progress")
        else:
            print(f"[ERROR] {task_id}: 任务不存在")
    
    conn.commit()
    conn.close()
    
    # 记录事件
    if updated > 0:
        add_batch_event(updated)
    
    return updated

def add_batch_event(count):
    """记录批量更新事件"""
    try:
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {"events": []}
    
    event = {
        "id": f"event-{len(data.get('events', [])) + 1:03d}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "batch_update",
        "icon": "🔄",
        "content": f"[批量] 更新{count}个正在执行任务的状态为进行中"
    }
    
    data.setdefault("events", []).append(event)
    
    with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("=" * 70)
    print("批量更新进行中任务状态")
    print("=" * 70)
    print()
    
    updated = batch_update()
    
    print()
    print("=" * 70)
    print(f"[完成] 已更新 {updated} 个任务")
    print("=" * 70)
    print()
    print("Dashboard: http://localhost:8877")

