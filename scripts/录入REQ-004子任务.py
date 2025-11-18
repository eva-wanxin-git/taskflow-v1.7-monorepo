#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入REQ-004的5个子任务到数据库
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

TASKS = [
    {
        "id": "TASK-004-A1",
        "title": "创建企业级目录结构模板",
        "description": """基于用户提供的完整企业级Monorepo结构，创建标准模板文档。

【任务目标】:
创建docs/arch/monorepo-structure-template.md，详细说明企业级目录结构。

【内容包括】:
- apps/（5个应用：api/web/admin/worker/mobile）
- packages/（9个包：core-domain/infra/ui-kit/ux-flows等）
- docs/（7个子目录：product/ux/arch/adr/api/ops-runbook/onboarding）
- ops/（6个子目录：infra/k8s/docker/ci-cd/monitoring/scripts）
- knowledge/（5个子目录：issues/solutions/patterns/tools/lessons-learned）
- database/（4个子目录：migrations/seeds/schemas/docs）
- tests/（4个子目录：e2e/integration/performance/fixtures）

【每个目录需要说明】:
- 用途
- 推荐技术栈
- 依赖关系
- 最佳实践

【验收标准】:
- [ ] 文档500-800行
- [ ] 覆盖所有目录
- [ ] 每个目录有详细说明
- [ ] 有使用示例
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 2.0,
        "complexity": "low",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-004",
            "tags": "documentation,architecture,p0"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-004-A2",
        "title": "补充企业级知识库Schema",
        "description": """扩展知识库数据库，添加企业级表和记忆系统表。

【当前状态】:
- v1: 3个任务表
- v2: 9个知识库表
- 需要补充: 企业级表 + 记忆系统表

【需要创建】:
database/schemas/v3_enterprise_knowledge_schema.sql

【新增表】（5个）:
1. environments - 环境表（dev/staging/prod）
2. deployments - 部署记录表
3. interaction_events - 交互事件表（记录用户↔AI交互）
4. memory_snapshots - 记忆快照表（记录提炼过程）
5. memory_categories - 21库映射表

【扩展表】（3个）:
- tools表: 添加category/installation字段
- component_tools表: 多对多关系
- knowledge_articles表: 添加layer/category_code字段

【验收标准】:
- [ ] SQL文件完整（300-400行）
- [ ] 所有表有注释
- [ ] 索引合理
- [ ] 外键关系正确
- [ ] 可执行（无语法错误）
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 2.0,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-004",
            "tags": "database,schema,p0"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-004-B1",
        "title": "组装即插即用封装包",
        "description": """创建标准化的封装包目录，复制所有必需文件。

【封装包结构】:
任务所Flow-即插即用封装包-v1.7/
├── README-即插即用.md
├── 一键安装.bat / install.sh
├── docs/ai/（4个AI提示词）
├── docs/arch/（模板和工作流）
├── docs/guides/（使用指南）
├── database/schemas/（3个Schema）
├── database/migrations/（迁移工具）
└── scripts/（初始化脚本）

【验收标准】:
- [ ] 目录结构完整
- [ ] 所有文件复制正确
- [ ] README说明清晰
- [ ] 文件路径相对化（不依赖原项目路径）
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 2.0,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-004",
            "dependencies": "TASK-004-A1,TASK-004-A2",
            "tags": "packaging,p1"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-004-B2",
        "title": "编写一键安装脚本",
        "description": """编写Windows和Linux/Mac的一键安装脚本。

【Windows版本】(一键安装.bat):
1. 检测目标项目
2. 创建标准目录结构
3. 初始化知识库DB
4. 生成初始文档模板
5. 显示激活命令

【Linux/Mac版本】(install.sh):
同上功能

【依赖脚本】（需要创建）:
- scripts/初始化项目结构.py
- scripts/初始化知识库DB.py
- scripts/生成功能清单模板.py
- scripts/生成任务板模板.py

【验收标准】:
- [ ] Windows脚本可运行
- [ ] Linux/Mac脚本可运行
- [ ] 所有依赖脚本实现
- [ ] 错误处理完整
- [ ] 有友好的进度提示
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 1.0,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-004",
            "dependencies": "TASK-004-B1",
            "tags": "scripts,automation,p1"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-004-C",
        "title": "真实项目测试封装包",
        "description": """在真实项目（librechat-desktop）测试即插即用封装包。

【测试步骤】:
1. 复制封装包到librechat-desktop项目
2. 运行一键安装脚本
3. 在Cursor中激活架构师
4. 验证Phase 0-6工作流
5. 记录问题和改进点

【测试项目】:
librechat-desktop（已有项目，合适作为测试对象）

【验收标准】:
- [ ] 安装脚本执行成功
- [ ] 目录结构创建正确
- [ ] 知识库DB初始化成功
- [ ] 架构师工作流完整执行
- [ ] 生成测试报告（问题+改进）
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 1.0,
        "complexity": "medium",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-004",
            "dependencies": "TASK-004-B1,TASK-004-B2",
            "tags": "testing,integration,p1"
        }, ensure_ascii=False)
    }
]

def insert_tasks():
    """插入所有REQ-004子任务"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    inserted = 0
    skipped = 0
    
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
            print(f"[OK] Inserted: {task['id']} - {task['title']}")
            inserted += 1
        except sqlite3.IntegrityError:
            print(f"[SKIP] Already exists: {task['id']}")
            skipped += 1
    
    conn.commit()
    conn.close()
    
    return inserted, skipped

def insert_dependencies():
    """插入任务依赖关系"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    dependencies = [
        ("TASK-004-B1", "TASK-004-A1"),  # B1依赖A1
        ("TASK-004-B1", "TASK-004-A2"),  # B1依赖A2
        ("TASK-004-B2", "TASK-004-B1"),  # B2依赖B1
        ("TASK-004-C", "TASK-004-B1"),   # C依赖B1
        ("TASK-004-C", "TASK-004-B2"),   # C依赖B2
    ]
    
    inserted = 0
    for task_id, dependency_id in dependencies:
        try:
            cursor.execute("""
                INSERT INTO task_dependencies (task_id, dependency_id)
                VALUES (?, ?)
            """, (task_id, dependency_id))
            inserted += 1
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    
    return inserted

def main():
    print("=" * 60)
    print("[REQ-004] Insert 5 sub-tasks into database")
    print("=" * 60)
    print()
    
    inserted, skipped = insert_tasks()
    print()
    
    deps = insert_dependencies()
    print(f"[OK] Inserted {deps} dependencies")
    print()
    
    print("=" * 60)
    print("[SUCCESS] Sub-tasks ready")
    print("=" * 60)
    print(f"[Inserted] {inserted} tasks")
    print(f"[Skipped] {skipped} tasks (already exist)")
    print(f"[Dashboard] http://localhost:8877 - should show {inserted} new tasks")

if __name__ == "__main__":
    main()

