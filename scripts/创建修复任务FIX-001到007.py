#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建修复任务 FIX-001 到 FIX-007
一键录入到数据库
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "任务所-v1.6-Tab修复版"))

from automation.state_manager import StateManager

# 数据库路径
db_path = project_root / "database/data/tasks.db"

# 任务定义
tasks = [
    {
        "id": "FIX-001",
        "title": "同步task-board.md与数据库",
        "description": """将数据库中的54个任务完整同步到task-board.md，确保文档与数据一致。

技术要点:
- 读取数据库所有任务(54个)
- 按状态分组(completed/in_progress/pending/cancelled)
- 按优先级排序
- 生成标准Markdown格式
- 更新docs/tasks/task-board.md

验收标准:
- task-board.md显示54个任务
- 包含所有INTEGRATE-001到INTEGRATE-014
- 按优先级和状态正确分组
- Markdown格式规范""",
        "status": "PENDING",
        "priority": "P0",
        "estimated_hours": 2.0,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "project_id": "TASKFLOW",
        "component_id": "docs"
    },
    {
        "id": "FIX-002",
        "title": "修复Dashboard数据读取",
        "description": """确保Dashboard直接从数据库读取任务，不依赖过期的文件缓存。

技术要点:
- 检查/api/tasks端点
- 确认StateManager.list_all_tasks()正确读取数据库
- 验证返回54个任务
- 检查Dashboard前端正确显示

验收标准:
- /api/tasks返回54个任务
- Dashboard显示任务数量: 54
- 进度计算正确: 25/54 = 46.3%
- 所有INTEGRATE任务可见

依赖: FIX-001""",
        "status": "PENDING",
        "priority": "P0",
        "estimated_hours": 1.5,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "project_id": "TASKFLOW",
        "component_id": "dashboard",
        "depends_on": "FIX-001"
    },
    {
        "id": "FIX-003",
        "title": "创建完整任务清单展示页",
        "description": """在Dashboard添加"完整任务清单"Tab，展示所有54个任务的详细信息。

技术要点:
- 新增Tab: 完整任务清单
- 按状态分4个section展示
- 每个任务卡片显示: ID/标题/优先级/工时
- 支持复制任务ID

验收标准:
- Dashboard新增"任务清单"Tab
- 显示4个section(已完成/进行中/待处理/已取消)
- 每个任务卡片信息完整
- 点击任务ID可复制

依赖: FIX-002""",
        "status": "PENDING",
        "priority": "P1",
        "estimated_hours": 2.0,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "project_id": "TASKFLOW",
        "component_id": "dashboard",
        "depends_on": "FIX-002"
    },
    {
        "id": "FIX-004",
        "title": "验证已完成任务的文件存在性",
        "description": """检查数据库标记为completed的25个任务，是否都有对应的完成报告文件。

技术要点:
- 查询数据库completed任务(25个)
- 扫描项目目录查找完成报告文件
- 匹配文件名模式: *任务ID*完成报告*.md
- 生成缺失文件清单

验收标准:
- 扫描所有已完成任务(25个)
- 列出缺少完成报告的任务
- 生成Markdown报告
- 标记待补充任务""",
        "status": "PENDING",
        "priority": "P1",
        "estimated_hours": 1.0,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "project_id": "TASKFLOW",
        "component_id": "docs"
    },
    {
        "id": "FIX-005",
        "title": "修复事件流完整性",
        "description": """验证154个事件记录是否完整，是否所有任务状态变更都有对应事件。

技术要点:
- 读取architect_events.json
- 统计事件类型分布
- 对比数据库: 25个completed vs 事件流task_completed数量
- 检查时间戳连续性

验收标准:
- 事件流JSON可正常读取
- 154个事件数量正确
- 25个task_completed对应25个completed任务
- 事件时间戳无断层
- 生成事件流健康报告""",
        "status": "PENDING",
        "priority": "P1",
        "estimated_hours": 1.0,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "project_id": "TASKFLOW",
        "component_id": "api"
    },
    {
        "id": "FIX-006",
        "title": "生成功能实现总览文档",
        "description": """基于已完成的25个任务和完成报告，生成一份功能实现总览文档。

技术要点:
- 读取数据库completed任务
- 读取对应的完成报告文件
- 提取功能描述/代码位置
- 按类别分组(基础/集成/子任务/修复)
- 生成Markdown总览文档

验收标准:
- 文档包含所有25个已完成任务
- 每个任务有: 功能描述/代码位置/完成报告链接
- 按类别分组清晰
- 保存为功能实现总览.md

依赖: FIX-004""",
        "status": "PENDING",
        "priority": "P2",
        "estimated_hours": 2.0,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "project_id": "TASKFLOW",
        "component_id": "docs",
        "depends_on": "FIX-004"
    },
    {
        "id": "FIX-007",
        "title": "Dashboard添加任务筛选功能",
        "description": """在Dashboard顶部添加筛选器,支持按状态/优先级/类型筛选任务。

技术要点:
- 添加3个下拉框: 状态/优先级/类型
- 实现筛选逻辑
- 显示筛选结果数量
- 保持工业美学样式

验收标准:
- Dashboard顶部显示3个筛选下拉框
- 按状态筛选正常(all/completed/in_progress/pending)
- 按优先级筛选正常(all/P0/P1/P2)
- 按类型筛选正常(all/REQ/INTEGRATE/TASK)
- 显示筛选结果数量
- 样式符合工业美学

依赖: FIX-003""",
        "status": "PENDING",
        "priority": "P2",
        "estimated_hours": 1.5,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "project_id": "TASKFLOW",
        "component_id": "dashboard",
        "depends_on": "FIX-003"
    }
]


def main():
    print("=" * 70)
    print("  创建修复任务 FIX-001 到 FIX-007")
    print("=" * 70)
    
    if not db_path.exists():
        print(f"\n❌ 数据库不存在: {db_path}")
        return
    
    # 初始化StateManager
    state_manager = StateManager(db_path=str(db_path))
    
    print(f"\n📋 准备创建 {len(tasks)} 个修复任务")
    print()
    
    created_count = 0
    skipped_count = 0
    
    for task_data in tasks:
        task_id = task_data["id"]
        
        # 检查任务是否已存在
        existing = state_manager.get_task(task_id)
        if existing:
            print(f"⚠️  {task_id}: 已存在，跳过")
            skipped_count += 1
            continue
        
        # 创建任务
        try:
            # 转换为Task对象并保存
            from automation.models import Task, TaskStatus, TaskPriority, TaskComplexity
            
            task = Task(
                id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                status=TaskStatus(task_data["status"]),
                priority=TaskPriority(task_data["priority"]),
                estimated_hours=task_data["estimated_hours"],
                complexity=TaskComplexity(task_data["complexity"]),
                assigned_to=task_data["assigned_to"],
                project_id=task_data.get("project_id"),
                component_id=task_data.get("component_id"),
                dependencies=[task_data.get("depends_on")] if task_data.get("depends_on") else []
            )
            
            state_manager.create_task(task)
            print(f"✅ {task_id}: {task_data['title']}")
            print(f"   优先级: {task_data['priority']}, 工时: {task_data['estimated_hours']}h")
            created_count += 1
            
        except Exception as e:
            print(f"❌ {task_id}: 创建失败 - {e}")
    
    print()
    print("=" * 70)
    print(f"✅ 成功创建: {created_count} 个任务")
    print(f"⚠️  已存在跳过: {skipped_count} 个任务")
    print(f"📊 总计: {created_count + skipped_count} 个任务")
    print("=" * 70)
    
    if created_count > 0:
        print()
        print("🎯 下一步:")
        print("  1. 查看Dashboard: http://localhost:8877")
        print("  2. 派发任务给李明:")
        print("     - 创建派发文档: 📤派发给李明-修复任务.md")
        print("  3. 或架构师直接执行FIX-001和FIX-002")
        print()


if __name__ == "__main__":
    main()

