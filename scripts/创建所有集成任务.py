#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建所有集成任务 - 确保完成的功能真正可用
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

TASKS = [
    {
        "id": "TASK-INTEGRATE-003",
        "title": "集成REQ-003对话历史库到Dashboard",
        "description": """将REQ-003的代码真正替换Dashboard上的"对话交流"Tab。

【用户反馈】:
Dashboard上Tab还叫"对话交流"，不是"对话历史库"
说明REQ-003的代码没有集成

【任务目标】:
替换templates.py中"对话交流"Tab的代码，使用REQ-003的新实现

【具体操作】:
1. 定位templates.py中"对话交流"Tab代码段
2. 完全替换为REQ-003的新代码：
   - Tab标题：对话交流 → 对话历史库
   - HTML结构：旧列表 → 新的左右分栏布局
   - CSS样式：添加254行新样式
   - JavaScript：添加193行会话管理逻辑
3. 重启Dashboard测试

【参考】:
- REQ-003完成报告：完整的实现说明
- REQ-003代码：已经写好的代码片段

【验收标准】:
- [ ] Tab标题显示"对话历史库"
- [ ] 左侧显示会话列表+搜索框
- [ ] 右侧显示会话详情
- [ ] 点击会话可切换
- [ ] 搜索功能正常
- [ ] 用户/AI消息配色区分
- [ ] 用户能在Dashboard上看到并使用
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 1.0,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-003",
            "tags": "integration,frontend,p0",
            "reason": "用户看不到功能，需要集成"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-INTEGRATE-001",
        "title": "集成REQ-001缓存清除功能到Dashboard",
        "description": """验证并集成REQ-001的缓存清除功能。

【用户反馈】:
"没感觉到"REQ-001的功能

【任务目标】:
确认"清除缓存"按钮和"缓存版本"显示是否在Dashboard上

【具体操作】:
1. 检查Dashboard页面：
   - 是否有"缓存版本: vXXXXX"显示？
   - 是否有"🔄 清除缓存"按钮？
   - 在哪个位置？
   
2. 如果没有：
   - 找到templates.py中应该添加的位置
   - 添加UI代码（按钮+JavaScript）
   - 确认API端点可用
   - 重启Dashboard测试
   
3. 如果有但不明显：
   - 调整位置（放到更显著的位置）
   - 增加视觉强调

【验收标准】:
- [ ] 用户能看到"清除缓存"按钮
- [ ] 点击按钮可用
- [ ] 缓存版本号显示
- [ ] 用户实际能使用这个功能
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 1.0,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-001",
            "tags": "integration,verification,p0",
            "reason": "用户看不到功能"
        }, ensure_ascii=False)
    },
    {
        "id": "TASK-INTEGRATE-006",
        "title": "集成REQ-006 Token同步功能到Dashboard",
        "description": """验证并集成REQ-006的Token同步功能。

【用户反馈】:
"没感觉到"REQ-006的功能

【任务目标】:
确认"Token同步"按钮是否在Dashboard上

【具体操作】:
1. 检查Dashboard Token显示区域：
   - 是否有"🔄 同步"按钮？
   - 在哪个位置？
   - 是否明显？
   
2. 如果没有：
   - 在Token显示区域添加同步按钮
   - 添加JavaScript逻辑
   - 测试功能
   
3. 验证快捷脚本：
   - 🔄快速同步Token.bat 是否存在？
   - 是否可运行？

【验收标准】:
- [ ] 用户能看到"Token同步"按钮
- [ ] 点击按钮弹出对话框
- [ ] 可以输入Token值并同步
- [ ] 快捷脚本存在并可用
- [ ] 用户实际能使用这个功能
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 1.0,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat(),
        "metadata": json.dumps({
            "project_id": "TASKFLOW",
            "parent_task": "REQ-006",
            "tags": "integration,verification,p0",
            "reason": "用户看不到功能"
        }, ensure_ascii=False)
    }
]

def insert_tasks():
    """插入集成任务"""
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
            print(f"[OK] Created: {task['id']}")
            inserted += 1
        except sqlite3.IntegrityError:
            print(f"[SKIP] Already exists: {task['id']}")
    
    conn.commit()
    conn.close()
    
    return inserted

def main():
    print("=" * 60)
    print("[Integration Tasks] Create tasks to integrate features")
    print("=" * 60)
    print()
    
    inserted = insert_tasks()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Integration tasks created")
    print("=" * 60)
    print(f"[Created] {inserted} integration tasks")
    print()
    print("[Tasks]")
    print("  - INTEGRATE-003: REQ-003 Dialog History (1h)")
    print("  - INTEGRATE-001: REQ-001 Cache Clear (1h)")
    print("  - INTEGRATE-006: REQ-006 Token Sync (1h)")
    print()
    print("[Reason] User can't see/feel the features")
    print("[Priority] P0 - User explicitly requested")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

