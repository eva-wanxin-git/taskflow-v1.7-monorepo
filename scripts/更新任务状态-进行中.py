#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新任务状态为进行中
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
EVENTS_FILE = Path(__file__).parent.parent / "apps/dashboard/automation-data/architect_events.json"

def update_task_status(task_id, new_status="in_progress", assigned_to=None):
    """更新任务状态"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取当前任务信息
    cursor.execute("SELECT title, status, assigned_to FROM tasks WHERE id = ?", (task_id,))
    result = cursor.fetchone()
    
    if not result:
        print(f"错误: 任务 {task_id} 不存在")
        return False
    
    title, old_status, old_assigned = result
    
    # 更新状态
    if assigned_to:
        cursor.execute("""
            UPDATE tasks 
            SET status = ?, assigned_to = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, assigned_to, datetime.now().isoformat(), task_id))
    else:
        cursor.execute("""
            UPDATE tasks 
            SET status = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, datetime.now().isoformat(), task_id))
    
    conn.commit()
    conn.close()
    
    print(f"成功: {task_id} 状态已更新")
    print(f"  {old_status} -> {new_status}")
    if assigned_to:
        print(f"  执行人: {assigned_to}")
    
    # 添加事件
    add_status_change_event(task_id, title, old_status, new_status, assigned_to)
    
    return True

def add_status_change_event(task_id, title, old_status, new_status, assigned_to):
    """添加状态变更事件"""
    try:
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {"events": []}
    
    # 构造事件内容
    if assigned_to:
        content = f"任务派发: {task_id} 已派发给{assigned_to}，状态变更为{new_status}"
        icon = "📤"
        event_type = "task_dispatch"
    else:
        content = f"状态变更: {task_id} {old_status} → {new_status}"
        icon = "🔄"
        event_type = "status_change"
    
    new_event = {
        "id": f"event-{len(data['events']) + 1:03d}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": event_type,
        "icon": icon,
        "content": content,
        "metadata": {
            "task_id": task_id,
            "old_status": old_status,
            "new_status": new_status,
            "assigned_to": assigned_to
        }
    }
    
    data["events"].append(new_event)
    
    with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"事件已记录: event-{len(data['events']):03d}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python 更新任务状态-进行中.py <任务ID> [执行人]")
        print("示例: python 更新任务状态-进行中.py INTEGRATE-007 fullstack-engineer")
        sys.exit(1)
    
    task_id = sys.argv[1]
    assigned_to = sys.argv[2] if len(sys.argv) > 2 else None
    
    update_task_status(task_id, "in_progress", assigned_to)

