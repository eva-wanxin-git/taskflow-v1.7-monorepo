#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有已完成但还没有集成任务的功能
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

def check_unintegrated():
    """检查未集成的功能"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取所有已完成的任务
    cursor.execute("""
        SELECT id, title, estimated_hours
        FROM tasks
        WHERE status = 'completed'
        AND id NOT LIKE 'INTEGRATE-%'
        AND id NOT LIKE 'TASK-VERIFY-%'
        AND id NOT LIKE 'BUG-%'
        ORDER BY id
    """)
    
    completed = cursor.fetchall()
    
    # 获取已有的集成任务
    cursor.execute("""
        SELECT id, description
        FROM tasks
        WHERE id LIKE 'INTEGRATE-%'
    """)
    
    integrations = cursor.fetchall()
    
    # 分析哪些功能已有集成任务
    integrated_features = set()
    for int_id, desc in integrations:
        # 从描述中提取REQ-xxx或TASK-xxx
        if desc:
            import re
            matches = re.findall(r'(REQ-\d+|TASK-[A-Z]-\d+)', desc)
            integrated_features.update(matches)
    
    # 找出未集成的功能
    unintegrated = []
    for task_id, title, hours in completed:
        if task_id not in integrated_features:
            unintegrated.append((task_id, title, hours))
    
    # 输出结果
    print("=" * 70)
    print("未集成功能检查")
    print("=" * 70)
    print()
    print(f"[已完成任务] {len(completed)}个")
    print(f"[已有集成任务] {len(integrations)}个")
    print(f"[已集成功能] {len(integrated_features)}个")
    print(f"[未集成功能] {len(unintegrated)}个")
    print()
    
    if unintegrated:
        print("[需要创建集成任务的功能]:")
        print()
        for task_id, title, hours in unintegrated:
            print(f"  - {task_id}: {title} ({hours}h)")
    else:
        print("[结论] 所有已完成功能都有集成任务！")
    
    print()
    print("=" * 70)
    
    conn.close()
    
    return unintegrated

if __name__ == "__main__":
    check_unintegrated()

