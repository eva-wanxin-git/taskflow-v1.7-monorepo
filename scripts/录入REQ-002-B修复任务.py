#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入REQ-002-B修复任务（数据库查询实现）
基于架构师审查发现的问题
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

TASK = {
    "id": "REQ-002-B",
    "title": "实现项目记忆空间数据库查询逻辑",
    "description": """基于架构师审查REQ-002发现的问题，实现核心数据库查询逻辑。

【审查发现】:
REQ-002架构优秀（10/10），但核心查询方法全部为TODO，导致功能不可用：
- _query_memories() - 返回空列表
- _query_memory_by_id() - 返回空
- _query_related_memories() - 返回空
- _query_memory_stats() - 返回空数据

【任务目标】:
实现所有数据库查询方法，让项目记忆空间真正可用。

【需要实现的方法】（7个）:
1. _query_memories() - 核心检索（支持筛选）
2. _query_memory_by_id() - 按ID查询
3. _query_related_memories() - 相关记忆查询
4. _query_memory_stats() - 统计查询
5. _insert_memory() - 插入记忆
6. _insert_memory_relation() - 插入关系
7. _record_retrieval() - 记录检索历史

【验收标准】:
- [ ] 所有查询方法实现（不能有TODO）
- [ ] API调用返回真实数据（不是空列表）
- [ ] 测试数据库读写正常
- [ ] 编写集成测试验证
- [ ] 自测API可用性

【参考代码】:
- 服务类: apps/api/src/services/project_memory_service.py
- 数据库Schema: database/schemas/v2_knowledge_schema.sql
- StateManager参考: 任务所-v1.6-Tab修复版/automation/state_manager.py

【关联任务】:
- 父任务: REQ-002（项目记忆空间）
- 审查报告: 🏛️架构师审查-REQ-002完成报告.md
""",
    "status": "pending",
    "priority": "P0",
    "estimated_hours": 4.0,
    "complexity": "medium",
    "assigned_to": "fullstack-engineer",
    "created_at": datetime.now().isoformat(),
    "metadata": json.dumps({
        "project_id": "TASKFLOW",
        "component_id": "api",
        "tags": "bugfix,database,req-002,p0",
        "parent_task": "REQ-002",
        "created_by": "architect",
        "reason": "审查发现核心功能未实现"
    }, ensure_ascii=False)
}

def insert_task():
    """插入修复任务到数据库"""
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
        print(f"[OK] Task inserted: {TASK['id']}")
    except sqlite3.IntegrityError:
        print(f"[SKIP] Task already exists: {TASK['id']}")
    
    conn.commit()
    conn.close()

def main():
    print("=" * 60)
    print("[REQ-002-B] Create fix task based on review")
    print("=" * 60)
    print()
    
    insert_task()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Fix task created")
    print("=" * 60)
    print(f"[Task] {TASK['id']} - {TASK['title']}")
    print(f"[Priority] {TASK['priority']} ({TASK['estimated_hours']}h)")
    print(f"[Assigned] {TASK['assigned_to']}")

if __name__ == "__main__":
    main()

