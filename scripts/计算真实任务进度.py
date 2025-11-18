#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算真实的任务完成进度
基于数据库中的实际任务数量和状态
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

def calculate_progress():
    """计算任务完成进度"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # 统计总任务数
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    
    # 统计已完成任务数
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
    completed_tasks = cursor.fetchone()[0]
    
    # 统计进行中任务数
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'in_progress'")
    in_progress_tasks = cursor.fetchone()[0]
    
    # 统计待处理任务数
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
    pending_tasks = cursor.fetchone()[0]
    
    # 统计各优先级任务
    cursor.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority")
    priority_stats = dict(cursor.fetchall())
    
    conn.close()
    
    # 计算完成率
    completion_rate = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
    
    return {
        "total": total_tasks,
        "completed": completed_tasks,
        "in_progress": in_progress_tasks,
        "pending": pending_tasks,
        "completion_rate": completion_rate,
        "priority_stats": priority_stats
    }

def main():
    print("=" * 60)
    print("[Progress] Calculate real task progress")
    print("=" * 60)
    print()
    
    stats = calculate_progress()
    
    print("[Task Statistics]")
    print(f"  Total Tasks: {stats['total']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  In Progress: {stats['in_progress']}")
    print(f"  Pending: {stats['pending']}")
    print()
    
    print(f"[Completion Rate] {stats['completion_rate']}%")
    print()
    
    print("[Progress Bar]")
    completed_blocks = int(stats['completion_rate'] / 5)  # 每5%一个方块
    pending_blocks = 20 - completed_blocks
    bar = "█" * completed_blocks + "░" * pending_blocks
    print(f"  [{bar}] {stats['completion_rate']}%")
    print()
    
    print("[Priority Breakdown]")
    for priority, count in sorted(stats['priority_stats'].items()):
        print(f"  {priority}: {count} tasks")
    print()
    
    print("=" * 60)
    print("[Dashboard should show]")
    print("=" * 60)
    print(f"  {stats['completion_rate']}% DONE")
    print(f"  {stats['completed']}/{stats['total']} tasks completed")
    print()

if __name__ == "__main__":
    main()

