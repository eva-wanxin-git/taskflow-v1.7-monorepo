#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n=== 检查数据库中的任务 ===\n")

conn = sqlite3.connect("database/data/tasks.db")
cursor = conn.cursor()

# 检查任务
cursor.execute("SELECT id, title, status, priority FROM tasks")
tasks = cursor.fetchall()

print(f"数据库中任务数: {len(tasks)}")
for task in tasks:
    print(f"  {task[0]}: {task[1]} [{task[3]}] - {task[2]}")

print(f"\n任务总数: {len(tasks)}")

# 检查状态分布
cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
status_counts = cursor.fetchall()
print(f"\n按状态分组:")
for status, count in status_counts:
    print(f"  {status}: {count}个")

conn.close()

print("\n=== 测试API ===\n")
print("请运行: curl http://localhost:8871/api/tasks")
print("看看API返回什么数据")

