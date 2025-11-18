#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例脚本: 架构师审查

展示如何在审查任务时触发事件
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

def review_task(
    task_id: str,
    reviewer: str = "architect",
    result: str = "approved",  # "approved" or "rejected"
    score: int = None,
    feedback: str = None
):
    """
    审查任务并触发事件
    
    Args:
        task_id: 任务ID
        reviewer: 审查者
        result: 审查结果 (approved/rejected)
        score: 审查评分 (0-100)
        feedback: 反馈意见
    """
    # 1. 创建EventHelper实例
    event_helper = create_event_helper(
        project_id="TASKFLOW",
        actor=reviewer,
        source="ai"
    )
    
    try:
        # 2. 查询任务信息
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT title, status FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        
        if not row:
            print(f"✗ 任务不存在: {task_id}")
            return False
        
        title, current_status = row
        print(f"任务: {title}")
        print(f"当前状态: {current_status}")
        
        # 3. 执行审查（模拟审查过程）
        print(f"\n执行审查...")
        print(f"  - 审查代码质量")
        print(f"  - 检查测试覆盖")
        print(f"  - 验证功能完整性")
        print(f"  - 检查文档完整性")
        
        # 4. 更新任务状态
        new_status = "completed" if result == "approved" else "in_progress"
        cursor.execute('''
            UPDATE tasks
            SET status = ?,
                reviewed_at = ?,
                review_score = ?
            WHERE id = ?
        ''', (new_status, datetime.now().isoformat(), score, task_id))
        
        conn.commit()
        print(f"✓ 状态已更新: {new_status}")
        
        # 5. 触发审查事件
        if result == "approved":
            event = event_helper.task_approved(
                task_id=task_id,
                reviewer=reviewer,
                score=score,
                feedback=feedback
            )
            print(f"✓ 事件已触发: task.approved (ID: {event['id'][:8]}...)")
        else:
            event = event_helper.task_rejected(
                task_id=task_id,
                reviewer=reviewer,
                reason=feedback or "需要修改"
            )
            print(f"✓ 事件已触发: task.rejected (ID: {event['id'][:8]}...)")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("===== 示例: 架构师审查 =====\n")
    
    # 审查参数（可以通过命令行传入）
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
        result = sys.argv[2] if len(sys.argv) > 2 else "approved"
    else:
        task_id = "REQ-999-DEMO"
        result = "approved"
    
    print(f"审查任务: {task_id}")
    print(f"审查结果: {result}\n")
    
    # 根据结果设置评分和反馈
    if result == "approved":
        score = 95
        feedback = "代码质量优秀，文档完整，测试覆盖充分，批准通过！"
    else:
        score = 70
        feedback = "代码实现基本正确，但需要补充单元测试，文档需要更详细"
    
    success = review_task(
        task_id=task_id,
        reviewer="AI架构师",
        result=result,
        score=score,
        feedback=feedback
    )
    
    if success:
        print(f"\n✅ 审查完成（{result}），事件已触发！")
        print(f"✓ 审查评分: {score}/100")
        print(f"✓ 反馈意见: {feedback}")
        print("\n可以通过以下API查询事件:")
        print(f"  GET /api/events?related_entity_type=task&related_entity_id={task_id}")
        print(f"  GET /api/events?event_type=task.{result}")
        print(f"  GET /api/events?actor=AI架构师")
    else:
        print("\n✗ 审查失败")


if __name__ == "__main__":
    main()

