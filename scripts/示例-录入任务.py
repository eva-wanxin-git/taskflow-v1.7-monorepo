#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例脚本: 录入任务

展示如何在录入任务时触发事件
"""
import sqlite3
import json
import sys
import io
from datetime import datetime
from pathlib import Path

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加packages路径
sys.path.insert(0, str(Path(__file__).parent.parent / "packages"))

from shared_utils.event_helper import create_event_helper

DB_PATH = "database/data/tasks.db"

def create_task(
    task_id: str,
    title: str,
    description: str,
    priority: str = "P1",
    assigned_to: str = "fullstack-engineer",
    estimated_hours: float = 4.0
):
    """
    创建任务并触发事件
    
    Args:
        task_id: 任务ID
        title: 任务标题
        description: 任务描述
        priority: 优先级
        assigned_to: 分配给谁
        estimated_hours: 预估工时
    """
    # 1. 创建EventHelper实例
    event_helper = create_event_helper(
        project_id="TASKFLOW",
        actor="architect",  # 录入任务通常是架构师操作
        source="ai"
    )
    
    try:
        # 2. 插入任务到数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (id, title, description, status, priority, estimated_hours, assigned_to, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task_id,
            title,
            description,
            "pending",
            priority,
            estimated_hours,
            assigned_to,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        print(f"✓ 任务已创建: {task_id}")
        
        # 3. 触发 task_created 事件
        event1 = event_helper.task_created(
            task_id=task_id,
            title=title,
            priority=priority,
            assigned_to=assigned_to,
            estimated_hours=estimated_hours
        )
        print(f"✓ 事件已触发: task.created (ID: {event1['id'][:8]}...)")
        
        # 4. 触发 task_dispatched 事件
        event2 = event_helper.task_dispatched(
            task_id=task_id,
            assigned_to=assigned_to,
            reason="根据能力和负载分配"
        )
        print(f"✓ 事件已触发: task.dispatched (ID: {event2['id'][:8]}...)")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


def main():
    """主函数"""
    print("===== 示例: 录入任务 =====\n")
    
    # 示例任务数据
    task_data = {
        "task_id": "REQ-999-DEMO",
        "title": "演示任务 - 事件集成测试",
        "description": "这是一个演示任务，用于测试事件触发功能",
        "priority": "P2",
        "assigned_to": "fullstack-engineer",
        "estimated_hours": 2.0
    }
    
    print(f"创建任务: {task_data['task_id']}")
    print(f"标题: {task_data['title']}")
    print(f"优先级: {task_data['priority']}\n")
    
    success = create_task(**task_data)
    
    if success:
        print("\n✅ 任务录入完成，事件已触发！")
        print("\n可以通过以下API查询事件:")
        print(f"  GET /api/events?related_entity_type=task&related_entity_id={task_data['task_id']}")
    else:
        print("\n✗ 任务录入失败")


if __name__ == "__main__":
    main()

