#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速批量更新REQ-009和REQ-010系列任务状态
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

# 根据文件发现，这些任务已完成
COMPLETED = [
    "REQ-009",
    "REQ-009-A",
    "REQ-009-B", 
    "REQ-009-C",
    "REQ-010-A",
    "REQ-010-B",
    "REQ-010-C",
    "REQ-010-E",
]

def batch_update():
    """批量更新"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    updated = 0
    for task_id in COMPLETED:
        cursor.execute("""
            UPDATE tasks 
            SET status = 'completed', 
                updated_at = ?
            WHERE id = ? AND status != 'completed'
        """, (datetime.now().isoformat(), task_id))
        
        if cursor.rowcount > 0:
            print(f"[OK] {task_id} -> COMPLETED")
            updated += 1
    
    conn.commit()
    
    # 计算进度
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status != 'cancelled'")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
    completed = cursor.fetchone()[0]
    
    conn.close()
    
    rate = round(completed / total * 100, 1)
    
    print()
    print(f"[Progress] {completed}/{total} = {rate}%")
    
    return updated, completed, total, rate

def main():
    print("=" * 60)
    print("[Batch Update] REQ-009 and REQ-010 series")
    print("=" * 60)
    print()
    
    updated, completed, total, rate = batch_update()
    
    print()
    print("=" * 60)
    print("[SUCCESS]")
    print("=" * 60)
    print(f"  Updated: {updated} tasks")
    print(f"  Progress: {rate}% DONE")

if __name__ == "__main__":
    main()

