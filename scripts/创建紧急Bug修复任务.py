#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建紧急Bug修复任务 - 任务列表加载失败
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

TASK = {
    "id": "BUG-001",
    "title": "紧急修复：全栈开发工程师任务列表加载失败",
    "description": """Dashboard"全栈开发工程师"模块显示"Loading..."，任务列表无法加载。

【Bug现象】:
- Dashboard → 全栈开发工程师 → 任务清单 Tab
- 显示"Loading..."
- 任务列表不显示
- 其他Tab（功能清单、架构师监控）正常

【可能原因】:
1. API错误: GET /api/tasks 返回500错误
2. 数据量大: 39个任务，查询慢或超时
3. 数据格式: JSON解析失败
4. JavaScript错误: 控制台有错误
5. 数据库锁: SQLite被其他进程锁定

【诊断步骤】:
1. 检查浏览器Console（F12）是否有JavaScript错误
2. 检查Network（F12）: /api/tasks 返回什么？
3. 检查数据库: sqlite3 tasks.db "SELECT COUNT(*) FROM tasks;"
4. 检查Dashboard日志

【修复方向】:
- 如果是API错误 → 修复API端点
- 如果是数据量大 → 添加分页/缓存
- 如果是JSON错误 → 修复数据格式
- 如果是JS错误 → 修复前端代码
- 如果是数据库锁 → 添加重试机制

【验收标准】:
- [ ] 任务列表正常显示
- [ ] 显示39个任务（或当前实际数量）
- [ ] 加载时间<2秒
- [ ] 无JavaScript错误
- [ ] API返回正常

【紧急程度】: Critical
【影响范围】: 用户无法查看任务，系统核心功能不可用
""",
    "status": "pending",
    "priority": "P0",
    "estimated_hours": 1.0,
    "complexity": "high",
    "assigned_to": "fullstack-engineer",
    "created_at": datetime.now().isoformat(),
    "metadata": json.dumps({
        "project_id": "TASKFLOW",
        "tags": "bug,critical,dashboard,p0",
        "created_by": "architect",
        "severity": "critical",
        "bug_type": "loading_failure"
    }, ensure_ascii=False)
}

def insert_bug_task():
    """插入紧急Bug任务"""
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
        print(f"[OK] BUG-001 created")
        inserted = 1
    except sqlite3.IntegrityError:
        print(f"[SKIP] BUG-001 already exists")
        inserted = 0
    
    conn.commit()
    conn.close()
    
    return inserted

def main():
    print("=" * 60)
    print("[CRITICAL BUG] Task list loading failure")
    print("=" * 60)
    print()
    
    inserted = insert_bug_task()
    
    print()
    print("=" * 60)
    print("[URGENT] Bug task created")
    print("=" * 60)
    print(f"[Bug ID] BUG-001")
    print(f"[Severity] Critical")
    print(f"[Impact] User cannot see task list")
    print(f"[Assigned] fullstack-engineer")
    print(f"[Time] 1 hour")

if __name__ == "__main__":
    main()

