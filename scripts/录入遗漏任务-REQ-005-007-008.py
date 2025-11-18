#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入遗漏的3个需求分析任务
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

TASKS = [
    {
        "id": "TASK-ARCH-005",
        "title": "深度分析REQ-005：Dashboard重构升级",
        "description": """分析Dashboard重构需求，拆解成可执行任务。

【原始需求】:
- REQ-005: Dashboard重构升级（16h，P1）
- 来源：用户需求清单

【我的任务】:
1. 追问用户：
   - Dashboard哪些模块需要重构？
   - 重构目标是什么？（性能？功能？UI？）
   - 有哪些痛点？
   
2. 分析当前Dashboard问题
3. 设计3个方案（保守/平衡/激进）
4. 拆解成10+个子任务（16h大任务）

【产出】:
- REQ-005分析报告
- 10+个子任务
- 派发文档

【验收标准】:
- [ ] 完成深度分析
- [ ] 拆解成可执行任务
- [ ] 所有子任务录入数据库
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 1.0,
        "complexity": "medium",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-005",
            "tags": "analysis,dashboard,p1"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-USER-007",
        "title": "用户确认：REQ-007需求是否与REQ-004重复",
        "description": """请用户确认REQ-007的具体需求。

【背景】:
交接文档中有两个封装需求：
- REQ-004：即插即用封装包（复制到其他项目使用）
- REQ-007：封装v1.7完整版为独立包（一键部署？）

【疑问】:
这两个需求是否重复？还是：
- REQ-004 = 插件式封装（轻量，给其他项目用）
- REQ-007 = 完整打包（包含Dashboard/API/数据库，独立部署）

【需要用户回答】:
1. REQ-007和REQ-004是同一个需求吗？
2. 如果不是，REQ-007的具体需求是什么？
3. "独立包"是指什么？（Docker镜像？安装包？）

【验收标准】:
- [ ] 用户明确回答
- [ ] 如果不重复，架构师分析REQ-007
- [ ] 如果重复，合并到REQ-004
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 0.0,
        "complexity": "low",
        "assigned_to": "user",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "tags": "user-decision,clarification,p1",
            "waiting_for": "user_feedback"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-ARCH-008",
        "title": "设计REQ-008：真实项目测试计划",
        "description": """设计真实项目测试的完整计划。

【原始需求】:
- REQ-008：真实项目测试与反向改进（12h，P0）
- 建议项目：librechat-desktop

【我的任务】:
1. 确认测试项目（librechat-desktop？）
2. 制定测试范围：
   - 测试哪些功能？（即插即用？事件流？）
   - 测试目标？（验证可用性？发现问题？）
   
3. 拆解测试任务：
   - 准备阶段（复制封装包、安装）
   - 执行阶段（运行架构师工作流）
   - 记录阶段（记录问题）
   - 改进阶段（反向优化）

【依赖】:
- REQ-004完成（封装包做好了再测试）

【产出】:
- REQ-008测试计划
- 4-5个测试子任务
- 派发文档

【验收标准】:
- [ ] 测试计划完整
- [ ] 拆解成可执行任务
- [ ] 所有子任务录入数据库
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 1.0,
        "complexity": "medium",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-008",
            "dependencies": "REQ-004",
            "tags": "testing,analysis,p1"
        }, ensure_ascii=False)
    }
]

def insert_tasks():
    """插入遗漏任务"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    inserted = 0
    for task in TASKS:
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
    
    conn.commit()
    conn.close()
    
    return inserted

def main():
    print("=" * 60)
    print("[Missing Tasks] Insert REQ-005, 007, 008 analysis tasks")
    print("=" * 60)
    print()
    
    inserted = insert_tasks()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Missing tasks recorded")
    print("=" * 60)
    print(f"[Inserted] {inserted} tasks")
    print()
    print("[Missing Requirements]")
    print("  - REQ-005: Dashboard refactor (16h, needs breakdown)")
    print("  - REQ-007: Package v1.7 (8h, needs clarification)")
    print("  - REQ-008: Real project test (12h, depends on REQ-004)")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

