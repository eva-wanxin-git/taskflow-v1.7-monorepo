#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
取消重复任务REQ-007 - 与REQ-004重复
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

def cancel_tasks():
    """取消REQ-007和相关任务"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    tasks_to_cancel = ["REQ-007", "TASK-USER-007"]
    
    for task_id in tasks_to_cancel:
        cursor.execute("""
            UPDATE tasks 
            SET status = 'cancelled', 
                updated_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), task_id))
        
        if cursor.rowcount > 0:
            print(f"[OK] Cancelled: {task_id}")
        else:
            print(f"[SKIP] Not found: {task_id}")
    
    conn.commit()
    conn.close()

def main():
    print("=" * 60)
    print("[Cancel] REQ-007 - Duplicate of REQ-004")
    print("=" * 60)
    print()
    
    cancel_tasks()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Duplicate task cancelled")
    print("=" * 60)
    print("[Reason] User confirmed REQ-007 = REQ-004")
    print("[Action] Keep REQ-004 (already broken down)")
    print("[Cancelled] REQ-007 + TASK-USER-007")

if __name__ == "__main__":
    main()

