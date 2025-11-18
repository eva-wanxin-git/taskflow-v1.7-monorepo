#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例脚本: 李明提交完成

展示如何在提交任务完成时触发事件
"""
import sqlite3
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

def complete_task(
    task_id: str,
    actor: str = "fullstack-engineer",
    actual_hours: float = None,
    files_modified: list = None,
    completion_summary: str = None
):
    """
    完成任务并触发事件
    
    Args:
        task_id: 任务ID
        actor: 执行者
        actual_hours: 实际工时
        files_modified: 修改的文件列表
        completion_summary: 完成摘要
    """
    # 1. 创建EventHelper实例
    event_helper = create_event_helper(
        project_id="TASKFLOW",
        actor=actor,
        source="ai"
    )
    
    try:
        # 2. 更新任务状态到数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查任务是否存在
        cursor.execute('SELECT title, status, started_at FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        
        if not row:
            print(f"✗ 任务不存在: {task_id}")
            return False
        
        title, current_status, started_at = row
        print(f"任务: {title}")
        print(f"当前状态: {current_status}")
        
        # 计算实际工时（如果未提供）
        if actual_hours is None and started_at:
            started_dt = datetime.fromisoformat(started_at)
            hours_diff = (datetime.now() - started_dt).total_seconds() / 3600
            actual_hours = round(hours_diff, 1)
        
        # 更新状态为 completed
        cursor.execute('''
            UPDATE tasks
            SET status = 'completed',
                completed_at = ?,
                actual_hours = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), actual_hours, task_id))
        
        conn.commit()
        print(f"✓ 状态已更新: completed")
        print(f"✓ 实际工时: {actual_hours} 小时")
        
        # 3. 触发 task_completed 事件
        event = event_helper.task_completed(
            task_id=task_id,
            actor=actor,
            actual_hours=actual_hours,
            files_modified=files_modified or [],
            completion_summary=completion_summary or f"任务 {task_id} 已完成"
        )
        print(f"✓ 事件已触发: task.completed (ID: {event['id'][:8]}...)")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("===== 示例: 李明提交完成 =====\n")
    
    # 要完成的任务ID（可以通过命令行参数传入）
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
    else:
        task_id = "REQ-999-DEMO"  # 默认使用演示任务
    
    print(f"完成任务: {task_id}\n")
    
    success = complete_task(
        task_id=task_id,
        actor="李明（全栈工程师）",
        actual_hours=2.5,
        files_modified=[
            "apps/api/src/main.py",
            "packages/core-domain/entities/event.py",
            "tests/test_events.py"
        ],
        completion_summary="已完成事件系统集成，所有测试通过"
    )
    
    if success:
        print("\n✅ 任务已完成，事件已触发！")
        print("\n可以通过以下API查询事件:")
        print(f"  GET /api/events?related_entity_type=task&related_entity_id={task_id}")
        print(f"  GET /api/events?event_type=task.completed")
    else:
        print("\n✗ 任务完成失败")


if __name__ == "__main__":
    main()

