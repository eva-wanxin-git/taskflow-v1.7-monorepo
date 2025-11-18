#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将v1.7任务录入数据库
"""

import sqlite3
import sys
import io
from pathlib import Path
from datetime import datetime

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 数据库路径
DB_PATH = "database/data/tasks.db"

# v1.7的任务数据
TASKS = [
    # Phase C: API集成 (P0)
    {
        "id": "TASK-C-1",
        "title": "创建FastAPI主应用入口",
        "description": "创建apps/api/src/main.py，整合所有路由和中间件，启动FastAPI服务",
        "status": "PENDING",
        "priority": "P0",
        "estimated_hours": 2.0,
        "complexity": "LOW",
        "project_id": "taskflow-main",
        "component_id": "taskflow-api",
        "assigned_to": "fullstack-engineer",
        "tags": "backend,infrastructure,critical",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "TASK-C-2",
        "title": "集成ArchitectOrchestrator与数据库",
        "description": "将ArchitectOrchestrator与StateManager集成，实现真正的数据库读写",
        "status": "PENDING",
        "priority": "P0",
        "estimated_hours": 3.0,
        "complexity": "MEDIUM",
        "project_id": "taskflow-main",
        "component_id": "taskflow-api",
        "assigned_to": "fullstack-engineer",
        "tags": "backend,integration,critical",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "TASK-C-3",
        "title": "端到端测试架构师API",
        "description": "编写完整的E2E测试，验证架构师工作流",
        "status": "PENDING",
        "priority": "P0",
        "estimated_hours": 1.5,
        "complexity": "LOW",
        "project_id": "taskflow-main",
        "component_id": "taskflow-api",
        "assigned_to": "fullstack-engineer",
        "tags": "test,integration,critical",
        "created_at": datetime.now().isoformat()
    },
    # Phase D: 代码迁移 (P2)
    {
        "id": "TASK-D-1",
        "title": "迁移models.py到core-domain",
        "description": "将v1.6的automation/models.py迁移到packages/core-domain/entities/",
        "status": "PENDING",
        "priority": "P2",
        "estimated_hours": 2.0,
        "complexity": "MEDIUM",
        "project_id": "taskflow-main",
        "component_id": "taskflow-core",
        "assigned_to": "fullstack-engineer",
        "tags": "refactor,migration",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "TASK-D-2",
        "title": "迁移state_manager到infra",
        "description": "将StateManager迁移到packages/infra/database/",
        "status": "PENDING",
        "priority": "P2",
        "estimated_hours": 3.0,
        "complexity": "MEDIUM",
        "project_id": "taskflow-main",
        "component_id": "taskflow-infra",
        "assigned_to": "fullstack-engineer",
        "tags": "refactor,migration",
        "created_at": datetime.now().isoformat()
    },
]

# 依赖关系
DEPENDENCIES = [
    ("TASK-C-2", "TASK-C-1"),  # C2依赖C1
    ("TASK-C-3", "TASK-C-1"),  # C3依赖C1
    ("TASK-C-3", "TASK-C-2"),  # C3依赖C2
    ("TASK-D-2", "TASK-D-1"),  # D2依赖D1
]

def clear_existing_tasks(cursor):
    """清除现有的v1.7任务"""
    cursor.execute("DELETE FROM tasks WHERE id LIKE 'TASK-%'")
    cursor.execute("DELETE FROM task_dependencies WHERE task_id LIKE 'TASK-%'")
    print("✓ 已清除现有任务")

def insert_tasks(cursor, tasks):
    """插入任务"""
    import json
    
    for task in tasks:
        # 将tags和project/component信息放到metadata中
        metadata = {
            "tags": task["tags"],
            "project_id": task["project_id"],
            "component_id": task["component_id"]
        }
        
        cursor.execute("""
            INSERT INTO tasks (
                id, title, description, status, priority, 
                estimated_hours, complexity, assigned_to, 
                metadata, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task["id"],
            task["title"],
            task["description"],
            task["status"],
            task["priority"],
            task["estimated_hours"],
            task["complexity"],
            task["assigned_to"],
            json.dumps(metadata, ensure_ascii=False),
            task["created_at"]
        ))
    print(f"✓ 已插入 {len(tasks)} 个任务")

def insert_dependencies(cursor, dependencies):
    """插入依赖关系"""
    for task_id, depends_on in dependencies:
        cursor.execute("""
            INSERT INTO task_dependencies (task_id, dependency_id)
            VALUES (?, ?)
        """, (task_id, depends_on))
    print(f"✓ 已插入 {len(dependencies)} 个依赖关系")

def show_summary(cursor):
    """显示任务摘要"""
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE id LIKE 'TASK-%'")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT priority, COUNT(*) FROM tasks WHERE id LIKE 'TASK-%' GROUP BY priority")
    by_priority = dict(cursor.fetchall())
    
    print("\n" + "="*70)
    print("任务所·Flow v1.7 - 任务数据已录入")
    print("="*70)
    print(f"总任务数: {total}")
    print(f"  - P0(Critical): {by_priority.get('P0', 0)} 个")
    print(f"  - P2(Medium):   {by_priority.get('P2', 0)} 个")
    print("\n任务列表:")
    
    cursor.execute("""
        SELECT id, title, priority, estimated_hours, status
        FROM tasks WHERE id LIKE 'TASK-%'
        ORDER BY priority, id
    """)
    
    for row in cursor.fetchall():
        task_id, title, priority, hours, status = row
        print(f"  [{priority}] {task_id}: {title} ({hours}h) - {status}")
    
    print("="*70)
    print("\n✅ 数据库已更新！")
    print(f"📊 Dashboard地址: http://localhost:8870")
    print("\n下一步: 启动Dashboard")
    print("  cd apps/dashboard")
    print("  python start_dashboard.py")
    print()

def main():
    """主函数"""
    db_path = Path(DB_PATH)
    if not db_path.exists():
        print(f"❌ 数据库不存在: {DB_PATH}")
        print("请先运行: python database/migrations/migrate.py init")
        sys.exit(1)
    
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 清除现有任务
        clear_existing_tasks(cursor)
        
        # 插入新任务
        insert_tasks(cursor, TASKS)
        
        # 插入依赖关系
        insert_dependencies(cursor, DEPENDENCIES)
        
        # 提交
        conn.commit()
        
        # 显示摘要
        show_summary(cursor)
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 错误: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()

