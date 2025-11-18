#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示部署状态
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

def show_status():
    """显示部署状态"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 统计任务状态
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM tasks
        GROUP BY status
    """)
    
    print("\n" + "=" * 60)
    print("部署状态总览")
    print("=" * 60)
    
    total = 0
    stats = {}
    for status, count in cursor.fetchall():
        stats[status] = count
        total += count
        print(f"{status:15s}: {count:3d}")
    
    completed = stats.get('completed', 0)
    progress = (completed / total * 100) if total > 0 else 0
    
    print("-" * 60)
    print(f"{'TOTAL':15s}: {total:3d}")
    print(f"{'PROGRESS':15s}: {progress:.1f}%")
    print("=" * 60)
    
    # 检查集成任务
    cursor.execute("""
        SELECT id, status
        FROM tasks
        WHERE id LIKE 'INTEGRATE-%'
        ORDER BY id
    """)
    
    integrate_tasks = cursor.fetchall()
    if integrate_tasks:
        print("\n集成任务状态:")
        for task_id, status in integrate_tasks:
            symbol = "✓" if status == "completed" else "○"
            print(f"  {symbol} {task_id}: {status}")
    
    conn.close()

if __name__ == "__main__":
    show_status()

