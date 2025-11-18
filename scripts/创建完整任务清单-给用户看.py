#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建完整任务清单 - 所有待办任务录入Dashboard
包括：架构师任务 + 派发任务 + 用户任务
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

# 所有待办任务（完整清单）
ALL_TASKS = [
    # === 集成验证任务（Critical！用户说"没感觉到"） ===
    {
        "id": "TASK-VERIFY-001",
        "title": "验证REQ-001缓存清除功能是否集成",
        "description": """用户反馈：REQ-001审查通过了，但"没感觉到"功能。

【验证内容】:
1. 打开Dashboard: http://localhost:8877
2. 查找"清除缓存"按钮（应该在页面显著位置）
3. 查找"缓存版本"显示
4. 点击"清除缓存"按钮测试
5. 验证API端点: GET /api/cache/version

【如果没有】:
- 说明功能只写了代码，没集成
- 需要创建集成任务

【验收标准】:
- [ ] Dashboard上有"清除缓存"按钮
- [ ] 点击按钮可用
- [ ] API端点返回正确
- [ ] 生成验证报告
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 0.5,
        "complexity": "low",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "tags": "verification,critical,req-001",
            "created_by": "architect",
            "reason": "用户反馈：没感觉到功能"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-VERIFY-006",
        "title": "验证REQ-006 Token同步功能是否集成",
        "description": """用户反馈：REQ-006审查通过了，但"没感觉到"功能。

【验证内容】:
1. 打开Dashboard: http://localhost:8877
2. 查找"Token同步"按钮
3. 测试Token同步功能
4. 验证快捷脚本是否存在

【如果没有】:
- 说明功能只写了代码，没集成
- 需要创建集成任务

【验收标准】:
- [ ] Dashboard上有Token同步按钮
- [ ] 点击按钮可用
- [ ] 快捷脚本存在并可运行
- [ ] 生成验证报告
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 0.5,
        "complexity": "low",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "tags": "verification,critical,req-006",
            "created_by": "architect",
            "reason": "用户反馈：没感觉到功能"
        }, ensure_ascii=False)
    },
    
    # === REQ-009任务（等待用户决策） ===
    {
        "id": "TASK-USER-009",
        "title": "用户决策：REQ-009任务自动化流程方案选择",
        "description": """请用户选择REQ-009的实施方案。

【背景】:
REQ-009要求：李明自己更新任务状态（待处理→进行中→已完成），Dashboard有一键复制按钮。

【已设计3个方案】:
- 方案A：文件监听自动化（8h，完全自动）
- 方案B：API提交流程（4h，半自动）⭐ 推荐
- 方案C：最简方案（0h，当前方式）

【需要用户回答】:
1. 李明的工作环境？（已回答：新Cursor对话）
2. 完成报告位置？（观察到：项目根目录）
3. 文件命名约定？（观察到：✅{TASK-ID}-完成报告.md）
4. 您更看重什么？（待回答：自动化程度？）

【参考文档】:
- 🏛️REQ-009需求分析-任务自动化流程.md

【验收标准】:
- [ ] 用户明确选择方案
- [ ] 或用户提供补充要求
- [ ] 架构师基于回答拆解任务
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 0.0,
        "complexity": "low",
        "assigned_to": "user",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "tags": "user-decision,req-009,p1",
            "created_by": "architect",
            "waiting_for": "user_feedback"
        }, ensure_ascii=False)
    },
]

def insert_all_tasks():
    """插入所有待办任务"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    inserted = 0
    skipped = 0
    
    for task in ALL_TASKS:
        try:
            cursor.execute("""
                INSERT INTO tasks (
                    id, title, description, status, priority,
                    estimated_hours, complexity, assigned_to, 
                    created_at, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task['id'], task['title'], task['description'],
                task['status'], task['priority'], task['estimated_hours'],
                task['complexity'], task['assigned_to'],
                task['created_at'], task['metadata']
            ))
            print(f"[OK] Inserted: {task['id']} -> {task['assigned_to']}")
            inserted += 1
        except sqlite3.IntegrityError:
            print(f"[SKIP] Already exists: {task['id']}")
            skipped += 1
    
    conn.commit()
    conn.close()
    
    return inserted, skipped

def main():
    print("=" * 60)
    print("[Dashboard] Complete task list for user")
    print("=" * 60)
    print()
    
    inserted, skipped = insert_all_tasks()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Task list updated")
    print("=" * 60)
    print(f"[Inserted] {inserted} new tasks")
    print(f"[Skipped] {skipped} existing tasks")
    print()
    print("[Task Assignment]")
    print("  - architect: 2 tasks (VERIFY-001, VERIFY-006)")
    print("  - user: 1 task (USER-009, waiting for decision)")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

