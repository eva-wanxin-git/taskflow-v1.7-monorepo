#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正所有任务状态 - 基于完成报告和实际情况
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
PROJECT_ROOT = Path(__file__).parent.parent

def fix_all_status():
    """修正所有任务状态"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("修正任务状态")
    print("=" * 70)
    print()
    
    # 步骤1: 扫描所有完成报告
    print("[1] 扫描完成报告...")
    completion_reports = list(PROJECT_ROOT.glob("✅*完成报告.md"))
    
    completed_tasks = set()
    for report in completion_reports:
        # 从文件名提取任务ID
        name = report.stem  # 去掉.md
        # 提取任务ID模式
        import re
        matches = re.findall(r'(INTEGRATE-\d+|REQ-\d+-?[A-Z]?|TASK-[A-Z]-\d+|BUG-\d+)', name)
        if matches:
            task_id = matches[0]
            completed_tasks.add(task_id)
            print(f"  Found: {task_id}")
    
    print(f"\n  Total: {len(completed_tasks)} tasks with completion reports")
    
    # 步骤2: 更新已完成任务
    print(f"\n[2] 更新已完成任务状态...")
    for task_id in completed_tasks:
        cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
        result = cursor.fetchone()
        
        if result:
            old_status = result[0]
            if old_status != "completed":
                cursor.execute("""
                    UPDATE tasks SET status = 'completed', updated_at = ?
                    WHERE id = ?
                """, (datetime.now().isoformat(), task_id))
                print(f"  FIX: {task_id} {old_status} -> completed")
    
    # 步骤3: 重置错误的in_progress任务
    print(f"\n[3] 检查in_progress任务...")
    cursor.execute("""
        SELECT id, title FROM tasks 
        WHERE status = 'in_progress'
        AND id LIKE 'INTEGRATE-%'
    """)
    
    in_progress_tasks = cursor.fetchall()
    
    # 真正在执行的任务（需要手动确认）
    really_active = [
        "INTEGRATE-003",  # Token同步
        "INTEGRATE-006",  # 进度计算
        "INTEGRATE-007",  # E2E测试
        "INTEGRATE-012",  # 企业级模板
    ]
    
    for task_id, title in in_progress_tasks:
        if task_id in completed_tasks:
            # 已完成，但状态错了
            print(f"  FIX: {task_id} 已有完成报告，应该是completed")
        elif task_id not in really_active:
            # 不在真正执行列表，改回pending
            cursor.execute("""
                UPDATE tasks SET status = 'pending', updated_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), task_id))
            print(f"  FIX: {task_id} 实际未执行，改回pending")
        else:
            print(f"  OK: {task_id} 确实在执行中")
    
    # 步骤4: 显示最终状态
    print(f"\n[4] 最终状态统计...")
    cursor.execute("""
        SELECT status, COUNT(*) FROM tasks GROUP BY status
    """)
    
    print()
    for status, count in cursor.fetchall():
        print(f"  {status:15s}: {count:3d}")
    
    conn.commit()
    conn.close()
    
    print()
    print("=" * 70)
    print("状态修正完成")
    print("=" * 70)
    print("Dashboard: http://localhost:8877")

if __name__ == "__main__":
    fix_all_status()

