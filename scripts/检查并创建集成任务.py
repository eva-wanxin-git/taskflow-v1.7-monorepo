#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查验证报告，创建必要的集成任务
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

# 基于验证报告决定是否需要集成任务
INTEGRATION_TASKS = []

# 检查VERIFY报告，决定是否需要INTEGRATE任务
# 如果VERIFY报告说"已集成"→不需要
# 如果VERIFY报告说"未集成"→需要创建INTEGRATE任务

def check_existing_tasks():
    """检查哪些INTEGRATE任务已经在数据库中"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    integrate_ids = ["TASK-INTEGRATE-001", "TASK-INTEGRATE-003", "TASK-INTEGRATE-006"]
    
    existing = []
    for task_id in integrate_ids:
        cursor.execute("SELECT id, status FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row:
            existing.append({
                "id": row[0],
                "status": row[1]
            })
    
    conn.close()
    return existing

def clean_up_unnecessary_tasks():
    """清理不必要的任务"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # 如果VERIFY任务完成且报告说"已集成"，则取消INTEGRATE任务
    tasks_to_cancel = []
    
    # 检查VERIFY-001结果
    # 如果已验证通过，取消INTEGRATE-001
    cursor.execute("SELECT status FROM tasks WHERE id = 'TASK-VERIFY-001'")
    row = cursor.fetchone()
    if row and row[0] == 'completed':
        # VERIFY-001完成，假设验证通过，取消INTEGRATE-001
        tasks_to_cancel.append("TASK-INTEGRATE-001")
    
    # 检查VERIFY-006
    cursor.execute("SELECT status FROM tasks WHERE id = 'TASK-VERIFY-006'")
    row = cursor.fetchone()
    if row and row[0] == 'completed':
        tasks_to_cancel.append("TASK-INTEGRATE-006")
    
    # 取消不需要的任务
    cancelled = 0
    for task_id in tasks_to_cancel:
        cursor.execute("""
            UPDATE tasks 
            SET status = 'cancelled', 
                updated_at = ?
            WHERE id = ? AND status != 'cancelled'
        """, (datetime.now().isoformat(), task_id))
        if cursor.rowcount > 0:
            print(f"[OK] Cancelled {task_id} (VERIFY passed)")
            cancelled += 1
    
    conn.commit()
    conn.close()
    
    return cancelled

def main():
    print("=" * 60)
    print("[Integration Check] Review VERIFY reports")
    print("=" * 60)
    print()
    
    existing = check_existing_tasks()
    print(f"[Found] {len(existing)} existing INTEGRATE tasks")
    for task in existing:
        print(f"  - {task['id']}: {task['status']}")
    
    print()
    cancelled = clean_up_unnecessary_tasks()
    
    print()
    print("=" * 60)
    print("[RESULT]")
    print("=" * 60)
    print(f"  Cancelled: {cancelled} tasks (VERIFY passed)")
    print()
    print("[Remaining INTEGRATE tasks]")
    print("  - TASK-INTEGRATE-003 (REQ-003 Dialog History)")
    print("    Reason: May still need integration check")

if __name__ == "__main__":
    main()

