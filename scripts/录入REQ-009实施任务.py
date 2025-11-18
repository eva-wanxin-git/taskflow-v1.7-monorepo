#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入REQ-009实施任务 - 任务三态流转系统
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

TASKS = [
    {
        "id": "REQ-009",
        "title": "任务三态流转系统",
        "description": """实现任务的三种状态和对应按钮，让李明自己管理任务状态。

【三种状态】:
1. 待处理（pending）
   - Dashboard显示：📋 一键复制提示词
   - 点击：复制派发文档内容
   
2. 进行中（in_progress）
   - 李明触发：python scripts/李明收到任务.py TASK-ID
   - API调用：PUT /api/tasks/{id}/received
   - 状态：待处理 → 进行中
   
3. 已完成（completed）
   - 李明触发：python scripts/李明提交完成.py TASK-ID
   - API调用：POST /api/tasks/{id}/complete
   - Dashboard显示：📄 一键复制完成报告
   - 点击：复制完成报告内容

【核心价值】:
- 李明自己管理状态（不是架构师手动）
- Dashboard按钮化操作（一键复制）
- 状态自动流转（通过API）

【总工时】: 4小时
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 4.0,
        "complexity": "medium",
        "assigned_to": "architect",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "tags": "workflow,automation,ui,p0",
            "created_by": "architect"
        }, ensure_ascii=False)
    },
    {
        "id": "REQ-009-A",
        "title": "实现Dashboard一键复制按钮",
        "description": """在Dashboard任务卡片上添加一键复制按钮。

【待处理任务卡片】:
<button onclick="copyTaskPrompt('TASK-C-1')">
  📋 一键复制提示词
</button>

【已完成任务卡片】:
<button onclick="copyCompletionReport('TASK-C-1')">
  📄 一键复制完成报告
</button>

【JavaScript函数】:
1. copyTaskPrompt(taskId)
   - 调用API: GET /api/tasks/{id}/prompt
   - 复制到剪贴板
   - 显示成功提示

2. copyCompletionReport(taskId)
   - 调用API: GET /api/tasks/{id}/report
   - 复制到剪贴板
   - 显示成功提示

【后端API】（2个）:
- GET /api/tasks/{id}/prompt
- GET /api/tasks/{id}/report

【验收标准】:
- [ ] 待处理任务有"一键复制提示词"按钮
- [ ] 已完成任务有"一键复制完成报告"按钮
- [ ] 点击按钮可复制内容
- [ ] 显示友好提示
- [ ] API返回正确内容
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 2.0,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-009",
            "tags": "frontend,ui,p0"
        }, ensure_ascii=False)
    },
    {
        "id": "REQ-009-B",
        "title": "实现李明状态管理脚本和API",
        "description": """创建李明使用的脚本和对应API端点。

【脚本】（2个）:
1. scripts/李明收到任务.py
   - 用法: python 李明收到任务.py TASK-C-1
   - 功能: 待处理 → 进行中
   - API: PUT /api/tasks/{id}/received

2. scripts/李明提交完成.py
   - 用法: python 李明提交完成.py TASK-C-1
   - 功能: 进行中 → 已完成
   - API: POST /api/tasks/{id}/complete
   - 自动查找完成报告文件

【API端点】（3个）:
1. PUT /api/tasks/{id}/received
   - 更新status为in_progress
   - 记录received_at时间
   
2. PUT /api/tasks/{id}/start（已有，确认）
   - 同上

3. POST /api/tasks/{id}/complete
   - 更新status为completed
   - 保存report_path到metadata
   - 记录completed_at时间

【验收标准】:
- [ ] 2个脚本可运行
- [ ] 3个API端点可用
- [ ] 数据库状态正确更新
- [ ] 有使用文档
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 1.5,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-009",
            "tags": "scripts,api,p0"
        }, ensure_ascii=False)
    },
    {
        "id": "REQ-009-C",
        "title": "Dashboard任务列表自动刷新",
        "description": """实现Dashboard任务列表的自动刷新机制。

【功能】:
1. 轮询机制（每5秒）
2. 检测任务状态变化
3. 自动更新UI
4. 无需手动刷新页面

【实现方式】:
方案A: 轮询（简单）
- setInterval(() => refreshTasks(), 5000)

方案B: WebSocket（实时，可选）
- WebSocket连接
- 服务器推送更新

【验收标准】:
- [ ] Dashboard每5秒自动刷新任务
- [ ] 状态变化立即可见
- [ ] 不影响用户操作
- [ ] 性能良好（CPU<5%）
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 0.5,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-009",
            "dependencies": "REQ-009-A",
            "tags": "frontend,auto-refresh,p1"
        }, ensure_ascii=False)
    }
]

def insert_tasks():
    """插入所有REQ-009任务"""
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
        ("REQ-009-A", "REQ-010-B"),  # 一键复制需要API支持
        ("REQ-009-B", "REQ-010-B"),  # 状态管理需要API支持
        ("REQ-009-C", "REQ-009-A"),  # 自动刷新依赖前端完成
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
    print("[REQ-009] Task Three-State System - Insert tasks")
    print("=" * 60)
    print()
    
    inserted = insert_tasks()
    deps = insert_dependencies()
    
    print()
    print("=" * 60)
    print("[SUCCESS] REQ-009 tasks ready")
    print("=" * 60)
    print(f"[Tasks] {inserted} inserted")
    print(f"[Dependencies] {deps} inserted")
    print(f"[Total Hours] 4h (REQ-009 + 3 sub-tasks)")
    print(f"[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

