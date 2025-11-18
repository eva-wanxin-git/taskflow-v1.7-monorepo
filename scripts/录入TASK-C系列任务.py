#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入TASK-C系列任务到数据库
派发给全栈工程师·李明执行
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# 数据库路径
DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

# TASK-C系列任务
TASKS = [
    {
        "id": "TASK-C-1",
        "title": "创建FastAPI主应用入口",
        "description": """创建apps/api/src/main.py，整合所有路由和中间件，启动FastAPI服务。

技术要点:
- FastAPI应用初始化
- CORS中间件配置
- 注册architect路由
- 健康检查端点
- 异常处理中间件
- Uvicorn启动配置

验收标准:
- python main.py能启动
- GET /health返回200
- GET /docs显示API文档
- CORS配置正确（允许Dashboard访问）
- 日志输出清晰

参考:
- v1.6的industrial_dashboard/dashboard.py
- docs/tasks/task-board.md中的详细说明
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 2.0,
        "complexity": "LOW",
        "project_id": "TASKFLOW",
        "component_id": "api",
        "assigned_to": "fullstack-engineer",
        "tags": "phase-c,fastapi,api-entry,p0",
        "dependencies": "",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "TASK-C-2",
        "title": "集成ArchitectOrchestrator与数据库",
        "description": """将ArchitectOrchestrator与StateManager集成，实现真正的数据库读写。

当前问题:
- ArchitectOrchestrator已定义接口
- 所有数据库操作都是TODO注释
- 需要真正实现数据读写

实现方案（推荐临时方案）:
- 在main.py中添加v1.6路径
- 导入StateManager
- 注入到ArchitectOrchestrator
- 实现_ensure_project_exists()
- 实现_create_tasks_from_suggestions()
- 实现_create_issues_from_problems()

验收标准:
- 提交架构分析JSON，数据库出现记录
- SELECT * FROM tasks可以看到新任务
- SELECT * FROM issues可以看到问题
- Markdown文档（task-board.md）正确生成
- 错误处理完整

测试方法:
curl -X POST http://localhost:8870/api/architect/analysis -d @test_analysis.json
sqlite3 database/data/tasks.db "SELECT * FROM tasks;"
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 3.0,
        "complexity": "MEDIUM",
        "project_id": "TASKFLOW",
        "component_id": "api",
        "assigned_to": "fullstack-engineer",
        "tags": "phase-c,database,integration,p0",
        "dependencies": "TASK-C-1",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "TASK-C-3",
        "title": "端到端测试架构师API",
        "description": """编写完整的E2E测试，验证架构师工作流。

测试场景:
1. 提交架构分析JSON → 验证数据库写入
2. 查询项目摘要 → 验证数据返回
3. 提交交接快照 → 验证JSON文件生成
4. 查询最新快照 → 验证返回正确

测试脚本位置: tests/integration/test_architect_api.py
测试数据位置: tests/fixtures/sample_analysis.json

验收标准:
- 编写测试脚本
- 至少5个测试场景
- 所有测试通过
- 测试覆盖率>70%
- 生成测试报告

使用pytest框架
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 1.5,
        "complexity": "LOW",
        "project_id": "TASKFLOW",
        "component_id": "api",
        "assigned_to": "fullstack-engineer",
        "tags": "phase-c,test,e2e,p0",
        "dependencies": "TASK-C-1,TASK-C-2",
        "created_at": datetime.now().isoformat()
    }
]

def insert_tasks():
    """插入任务到数据库"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    for task in TASKS:
        try:
            # 构造metadata JSON（包含project_id等扩展字段）
            metadata = {
                "project_id": task.get('project_id'),
                "component_id": task.get('component_id'),
                "tags": task.get('tags'),
                "dependencies_str": task.get('dependencies')
            }
            
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
                task['created_at'], json.dumps(metadata, ensure_ascii=False)
            ))
            print(f"[OK] Task inserted: {task['id']} - {task['title']}")
        except sqlite3.IntegrityError:
            print(f"[SKIP] Task already exists: {task['id']}")
    
    conn.commit()
    conn.close()
    print(f"\n[SUCCESS] {len(TASKS)} tasks processed")

def insert_dependencies():
    """插入任务依赖关系"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    dependencies = [
        ("TASK-C-2", "TASK-C-1"),  # C-2依赖C-1
        ("TASK-C-3", "TASK-C-1"),  # C-3依赖C-1
        ("TASK-C-3", "TASK-C-2"),  # C-3依赖C-2
    ]
    
    for task_id, dependency_id in dependencies:
        try:
            cursor.execute("""
                INSERT INTO task_dependencies (task_id, dependency_id)
                VALUES (?, ?)
            """, (task_id, dependency_id))
            print(f"[OK] Dependency: {task_id} depends on {dependency_id}")
        except sqlite3.IntegrityError:
            print(f"[SKIP] Dependency already exists: {task_id} -> {dependency_id}")
    
    conn.commit()
    conn.close()
    print(f"\n[SUCCESS] {len(dependencies)} dependencies processed")

def main():
    print("=" * 60)
    print("[TASK-C] Insert tasks into database")
    print("=" * 60)
    print()
    
    insert_tasks()
    print()
    insert_dependencies()
    print()
    
    print("=" * 60)
    print("[DONE] TASK-C series ready for dispatch")
    print("=" * 60)

if __name__ == "__main__":
    main()

