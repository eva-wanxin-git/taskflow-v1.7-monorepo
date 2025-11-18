#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入REQ-010项目全局事件流系统任务
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

TASKS = [
    {
        "id": "REQ-010",
        "title": "项目全局事件流系统",
        "description": """升级事件流：从架构师视角→项目全局视角，实现事件驱动的自动化协作。

【核心理念】:
事件流 = 项目神经系统
所有角色的动作都触发事件→其他角色监听→自动响应

【核心功能】:
1. 完整的事件类型体系（task/feature/issue生命周期）
2. 事件发射和存储系统
3. 所有触发点集成（脚本/API）
4. 事件监听器（架构师自动化）
5. Dashboard可视化升级

【革命性价值】:
- 项目状态完全透明
- 架构师工作自动化
- 协作效率指数级提升
- 形成项目知识图谱

【总工时】: 16小时（分3个Phase）
【优先级】: P0（Phase 1）+ P1（Phase 2）+ P2（Phase 3）
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 16.0,
        "complexity": "high",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "tags": "event-driven,automation,innovation,p0",
            "created_by": "architect",
            "phases": 3
        }, ensure_ascii=False)
    },
    {
        "id": "REQ-010-A",
        "title": "设计项目事件类型体系",
        "description": """设计完整的项目事件类型、数据结构、生命周期。

【内容】:
1. 定义事件类型（20-30种）
   - 任务生命周期（9种）
   - 功能生命周期（5种）
   - 问题生命周期（4种）
   - 协作事件（4种）
   
2. 每种事件的数据结构
3. 事件优先级（Critical/High/Medium/Low）
4. 事件聚合规则
5. 事件过滤规则

【产出】:
- docs/arch/event-types-design.md（完整设计文档）
- 事件类型枚举定义
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 1.0,
        "complexity": "medium",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-010",
            "phase": 1,
            "tags": "design,p0"
        }, ensure_ascii=False)
    },
    {
        "id": "REQ-010-B",
        "title": "实现事件发射和存储系统",
        "description": """实现完整的事件系统后端。

【内容】:
1. 创建project_events表（SQL Schema）
2. 实现EventEmitter类（发射事件）
   - emit(event_type, data)
   - emit_batch(events)
3. 实现EventStore类（存储事件）
   - save(event)
   - query(filters)
4. 实现API端点（4个）
   - POST /api/events（发射事件）
   - GET /api/events（查询事件）
   - GET /api/events/types（获取事件类型）
   - GET /api/events/stats（统计）

【技术栈】:
- 数据库: SQLite + project_events表
- 后端: FastAPI
- 模型: Pydantic

【验收标准】:
- [ ] project_events表创建成功
- [ ] EventEmitter/Store类实现
- [ ] 4个API端点可用
- [ ] 单元测试通过
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 3.0,
        "complexity": "high",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-010",
            "dependencies": "REQ-010-A",
            "phase": 1,
            "tags": "backend,database,api,p0"
        }, ensure_ascii=False)
    },
    {
        "id": "REQ-010-C",
        "title": "集成事件触发点到所有脚本和API",
        "description": """在所有关键操作点添加事件触发。

【触发点清单】:

1. 脚本触发点（5个脚本）:
   - 录入任务.py → emit(task_created + task_dispatched)
   - 李明开始任务.py → emit(task_started)
   - 李明提交完成.py → emit(task_completed)
   - 李明集成功能.py → emit(feature_integrated)
   - 架构师审查.py → emit(task_reviewed + task_approved/rejected)

2. API触发点（3个端点）:
   - PUT /api/tasks/{id}/start → emit(task_started)
   - POST /api/tasks/{id}/complete → emit(task_completed)
   - POST /api/tasks/{id}/approve → emit(task_approved)

【验收标准】:
- [ ] 所有脚本集成事件发射
- [ ] 所有API集成事件发射
- [ ] 事件数据结构正确
- [ ] 测试验证事件被记录
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 2.0,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-010",
            "dependencies": "REQ-010-B",
            "phase": 1,
            "tags": "integration,p0"
        }, ensure_ascii=False)
    },
    {
        "id": "REQ-010-D",
        "title": "实现架构师事件监听器",
        "description": """实现自动化监听和响应机制。

【内容】:
1. EventListener类（轮询或WebSocket）
2. 规则引擎（5个核心规则）:
   - task_completed → 提醒架构师审查
   - feature_developed → 触发集成验证
   - task_approved → 自动更新状态
   - issue_discovered → 查找历史方案
   - task_rejected → 通知开发者修改

3. 通知机制:
   - Dashboard弹窗通知
   - 系统托盘通知（可选）

【验收标准】:
- [ ] EventListener实现
- [ ] 5个规则可用
- [ ] 测试规则触发
- [ ] 通知正常工作
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 2.0,
        "complexity": "high",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-010",
            "dependencies": "REQ-010-C",
            "phase": 2,
            "tags": "automation,listener,p1"
        }, ensure_ascii=False)
    },
    {
        "id": "REQ-010-E",
        "title": "Dashboard事件流可视化升级",
        "description": """升级事件流UI，支持分类、筛选、实时更新。

【UI功能】:
1. 事件类型筛选（任务/功能/问题/协作）
2. 角色筛选（架构师/李明/用户/系统）
3. 时间轴视图（按时间排序）
4. 实时刷新（轮询5秒或WebSocket）
5. 事件详情展开

【设计要求】:
- 延续工业美学风格
- 不同事件类型不同配色
- 支持搜索和过滤
- 性能优化（虚拟滚动）

【验收标准】:
- [ ] UI升级完成
- [ ] 筛选功能可用
- [ ] 实时刷新正常
- [ ] 性能良好（1000+事件）
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 2.0,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-010",
            "dependencies": "REQ-010-B",
            "phase": 2,
            "tags": "frontend,ui,p1"
        }, ensure_ascii=False)
    }
]

def insert_tasks():
    """插入所有REQ-010任务"""
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

def insert_dependencies():
    """插入依赖关系"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    deps = [
        ("REQ-010-B", "REQ-010-A"),
        ("REQ-010-C", "REQ-010-B"),
        ("REQ-010-D", "REQ-010-C"),
        ("REQ-010-E", "REQ-010-B"),
    ]
    
    inserted = 0
    for task_id, dep_id in deps:
        try:
            cursor.execute("""
                INSERT INTO task_dependencies (task_id, dependency_id)
                VALUES (?, ?)
            """, (task_id, dep_id))
            inserted += 1
        except:
            pass
    
    conn.commit()
    conn.close()
    
    return inserted

def main():
    print("=" * 60)
    print("[REQ-010] Event-Driven System - Insert tasks")
    print("=" * 60)
    print()
    
    inserted = insert_tasks()
    deps = insert_dependencies()
    
    print()
    print("=" * 60)
    print("[SUCCESS] REQ-010 tasks ready")
    print("=" * 60)
    print(f"[Tasks] {inserted} inserted")
    print(f"[Dependencies] {deps} inserted")
    print(f"[Total Hours] 16h (Phase 1: 6h P0, Phase 2: 4h P1, Phase 3: 6h P2)")
    print(f"[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

