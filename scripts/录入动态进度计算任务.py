#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入动态进度计算任务
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

TASK = {
    "id": "REQ-011",
    "title": "Dashboard动态进度计算",
    "description": """实现Dashboard进度的动态计算，基于数据库实际任务统计。

【用户需求】:
"以后这个进度，就是统计目前所有任务的数量和已完成数量的办理，比如所有35个，完成了多少个，那么统计就是完成多少百分比"

【当前问题】:
Dashboard显示14% DONE，但这是固定值，不是基于实际任务统计

【应该实现】:
进度 = (已完成任务数 / 总任务数) * 100%
实时从数据库查询，动态计算

【具体功能】:
1. 后端API: GET /api/stats/progress
   - 查询总任务数（SELECT COUNT(*) FROM tasks）
   - 查询已完成数（WHERE status='completed'）
   - 计算完成率
   - 返回JSON

2. 前端显示:
   - 大数字显示完成率（如：14%）
   - 显示任务统计（5/35 tasks）
   - 每5秒自动刷新
   
3. 进度条可视化:
   - 彩色进度条（绿色填充）
   - 动态宽度（width: XX%）

【验收标准】:
- [ ] API返回真实统计数据
- [ ] Dashboard显示动态计算的进度
- [ ] 完成任务后，进度自动更新
- [ ] 进度条反映实际完成度
""",
    "status": "pending",
    "priority": "P1",
    "estimated_hours": 2.0,
    "complexity": "low",
    "assigned_to": "fullstack-engineer",
    "created_at": datetime.now().isoformat(),
    "metadata": json.dumps({
        "project_id": "TASKFLOW",
        "tags": "dashboard,stats,dynamic,p1",
        "created_by": "architect",
        "reason": "用户要求进度动态计算"
    }, ensure_ascii=False)
}

def insert_task():
    """插入动态进度任务"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO tasks (
                id, title, description, status, priority,
                estimated_hours, complexity, assigned_to, 
                created_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            TASK['id'], TASK['title'], TASK['description'],
            TASK['status'], TASK['priority'], TASK['estimated_hours'],
            TASK['complexity'], TASK['assigned_to'],
            TASK['created_at'], TASK['metadata']
        ))
        print(f"[OK] Created: {TASK['id']}")
        inserted = 1
    except sqlite3.IntegrityError:
        print(f"[SKIP] Already exists: {TASK['id']}")
        inserted = 0
    
    conn.commit()
    conn.close()
    
    return inserted

def main():
    print("=" * 60)
    print("[REQ-011] Dynamic Progress Calculation")
    print("=" * 60)
    print()
    
    inserted = insert_task()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Task created")
    print("=" * 60)
    print(f"[Task] REQ-011 - Dashboard动态进度计算 (2h)")
    print(f"[Assigned] fullstack-engineer")
    print(f"[Reason] User wants real-time progress based on DB")
    print()
    print("[Current Progress Calculation]")
    print("  Formula: (completed_count / total_count) * 100%")
    print("  Data Source: SQLite tasks table")
    print("  Update Frequency: Every 5 seconds")

if __name__ == "__main__":
    main()

