#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例脚本: 李明开始任务

展示如何在开始任务时触发事件
"""
import sqlite3
import sys
import io
from datetime import datetime, timedelta
from pathlib import Path

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加packages路径
sys.path.insert(0, str(Path(__file__).parent.parent / "packages"))

from shared_utils.event_helper import create_event_helper

DB_PATH = "database/data/tasks.db"

def start_task(
    task_id: str,
    actor: str = "fullstack-engineer",
    work_plan: str = None
):
    """
    开始任务并触发事件
    
    Args:
        task_id: 任务ID
        actor: 执行者
        work_plan: 工作计划
    """
    # 1. 创建EventHelper实例
    event_helper = create_event_helper(
        project_id="TASKFLOW",
        actor=actor,
        source="ai"  # 李明是AI工程师
    )
    
    try:
        # 2. 更新任务状态到数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查任务是否存在
        cursor.execute('SELECT title, status FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        
        if not row:
            print(f"✗ 任务不存在: {task_id}")
            return False
        
        title, current_status = row
        print(f"任务: {title}")
        print(f"当前状态: {current_status}")
        
        # 更新状态为 in_progress
        cursor.execute('''
            UPDATE tasks
            SET status = 'in_progress',
                started_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), task_id))
        
        conn.commit()
        print(f"✓ 状态已更新: in_progress")
        
        # 3. 触发 task_started 事件
        planned_completion = (datetime.now() + timedelta(hours=4)).isoformat()
        
        event = event_helper.task_started(
            task_id=task_id,
            actor=actor,
            planned_completion=planned_completion,
            work_plan=work_plan or "1. 阅读需求 2. 设计方案 3. 编写代码 4. 自测"
        )
        print(f"✓ 事件已触发: task.started (ID: {event['id'][:8]}...)")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


def main():
    """主函数"""
    print("===== 示例: 李明开始任务 =====\n")
    
    # 要开始的任务ID（可以通过命令行参数传入）
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
    else:
        task_id = "REQ-999-DEMO"  # 默认使用演示任务
    
    print(f"开始执行任务: {task_id}\n")
    
    success = start_task(
        task_id=task_id,
        actor="李明（全栈工程师）",
        work_plan="1. 理解需求 2. 查看现有代码 3. 设计实现方案 4. 编码实现 5. 自测验证"
    )
    
    if success:
        print("\n✅ 任务已开始，事件已触发！")
        print("\n可以通过以下API查询事件:")
        print(f"  GET /api/events?related_entity_type=task&related_entity_id={task_id}")
        print(f"  GET /api/events?event_type=task.started")
    else:
        print("\n✗ 任务开始失败")


if __name__ == "__main__":
    main()

