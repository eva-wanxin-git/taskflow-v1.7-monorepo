#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录BUG-001修复到Dashboard
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def update_bug_status():
    """更新BUG-001状态为completed"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE tasks 
        SET status = 'completed', 
            updated_at = ? 
        WHERE id = 'BUG-001'
    """, (datetime.now().isoformat(),))
    
    conn.commit()
    conn.close()
    print("[OK] BUG-001 status updated to COMPLETED")

def add_fix_events():
    """添加修复事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "diagnosis",
            "icon": "🔍",
            "content": "诊断BUG-001：根因=v1.6 StateManager与v1.7 schema不兼容（缺6个字段）"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "bugfix",
            "icon": "🔧",
            "content": "修复BUG-001：修改_task_dict_to_model方法，使用.get()兼容两种schema"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "code_change",
            "icon": "✅",
            "content": "修改文件：state_manager.py（30行），兼容v1.6和v1.7 schema"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "🎉",
            "content": "BUG-001修复完成（7分钟）：等待Dashboard重启验证"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} fix events")

def update_monitor():
    """更新监控数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新Token
    data['token_usage']['used'] = 259000
    data['token_usage']['percentage'] = 25.9
    
    # 更新完成任务数（+1个Bug修复）
    data['project_info']['completed_tasks'] = 6
    data['project_info']['pending_tasks'] = 28
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[OK] Monitor updated: 6 completed, 28 pending")

def main():
    print("=" * 60)
    print("[BUG-001] Record fix completion")
    print("=" * 60)
    print()
    
    update_bug_status()
    add_fix_events()
    update_monitor()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Bug fix recorded")
    print("=" * 60)
    print("[Root Cause] Schema mismatch (v1.6 vs v1.7)")
    print("[Fix] Modified _task_dict_to_model to use .get()")
    print("[Time] 7 minutes")
    print("[Status] Waiting for Dashboard restart to verify")

if __name__ == "__main__":
    main()

