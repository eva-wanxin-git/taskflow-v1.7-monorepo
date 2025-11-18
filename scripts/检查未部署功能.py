#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有已完成但未部署的功能
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

def check_undeployed():
    """检查未部署的任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 查询所有已完成的任务
    cursor.execute("""
        SELECT id, title, description, metadata
        FROM tasks
        WHERE status = 'completed'
        AND id LIKE 'REQ-%'
        ORDER BY id
    """)
    
    completed_tasks = cursor.fetchall()
    
    print("=" * 70)
    print("[Check] Undeployed completed features")
    print("=" * 70)
    print()
    print(f"[Found] {len(completed_tasks)} completed REQ tasks")
    print()
    
    undeployed = []
    
    for task_id, title, desc, metadata in completed_tasks:
        # 检查是否有对应的INTEGRATE任务
        cursor.execute("""
            SELECT status FROM tasks
            WHERE description LIKE ?
        """, (f"%{task_id}%",))
        
        integrate = cursor.fetchone()
        
        if integrate and integrate[0] == 'completed':
            status = "✅ 已部署"
        elif integrate:
            status = f"⏳ 部署中 ({integrate[0]})"
        else:
            status = "❌ 未部署"
            undeployed.append((task_id, title))
        
        print(f"{status} {task_id}: {title}")
    
    conn.close()
    
    print()
    print("=" * 70)
    print(f"[Result] {len(undeployed)} features need deployment")
    print("=" * 70)
    
    if undeployed:
        print()
        print("[Undeployed Features]:")
        for task_id, title in undeployed:
            print(f"  - {task_id}: {title}")
    
    return undeployed

if __name__ == "__main__":
    check_undeployed()

