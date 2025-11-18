#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库任务状态
"""

import sqlite3
import json
from pathlib import Path

# 数据库路径
db_path = Path("database/data/tasks.db")

if not db_path.exists():
    print(f"Error: Database not found at {db_path}")
    exit(1)

# 连接数据库
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("Task Database Status Report")
print("=" * 70)

# 1. 总任务数
cursor.execute("SELECT COUNT(*) FROM tasks")
total = cursor.fetchone()[0]
print(f"\nTotal Tasks: {total}")

# 2. 按状态统计
print("\nBy Status:")
cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status ORDER BY COUNT(*) DESC")
for status, count in cursor.fetchall():
    print(f"  {status}: {count}")

# 3. 按优先级统计
print("\nBy Priority:")
cursor.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority ORDER BY COUNT(*) DESC")
for priority, count in cursor.fetchall():
    print(f"  {priority}: {count}")

# 4. 已完成任务列表
print("\nCompleted Tasks:")
cursor.execute("SELECT task_id, title FROM tasks WHERE status='COMPLETED' ORDER BY task_id")
completed_tasks = cursor.fetchall()
for task_id, title in completed_tasks:
    print(f"  [{task_id}] {title[:60]}")

# 5. 进行中任务
print("\nIn Progress Tasks:")
cursor.execute("SELECT task_id, title FROM tasks WHERE status='IN_PROGRESS' ORDER BY task_id")
inprogress_tasks = cursor.fetchall()
if inprogress_tasks:
    for task_id, title in inprogress_tasks:
        print(f"  [{task_id}] {title[:60]}")
else:
    print("  None")

# 6. 待处理任务（前5个）
print("\nPending Tasks (first 5):")
cursor.execute("SELECT task_id, title, priority FROM tasks WHERE status='PENDING' ORDER BY priority, task_id LIMIT 5")
for task_id, title, priority in cursor.fetchall():
    print(f"  [{task_id}] ({priority}) {title[:50]}")

# 7. 计算进度
cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='COMPLETED'")
completed = cursor.fetchone()[0]
progress = (completed / total * 100) if total > 0 else 0
print(f"\nProgress: {completed}/{total} = {progress:.1f}%")

print("=" * 70)

conn.close()

