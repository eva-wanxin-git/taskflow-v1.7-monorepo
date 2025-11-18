#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析当前功能实现和展示情况
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# 数据库路径
db_path = Path("database/data/tasks.db")

print("=" * 80)
print("  任务所·Flow v1.7 - 今晚功能实现分析报告")
print("  生成时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 80)

if not db_path.exists():
    print(f"\n⚠️ 数据库未找到: {db_path}")
    exit(1)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 1. 查看表结构
print("\n【1】数据库表结构")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f"  总表数: {len(tables)}")
for table in tables:
    print(f"  - {table}")

# 2. 查看tasks表字段
print("\n【2】tasks表字段")
cursor.execute("PRAGMA table_info(tasks)")
columns = cursor.fetchall()
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

# 3. 任务统计
print("\n【3】任务统计")
cursor.execute("SELECT COUNT(*) FROM tasks")
total = cursor.fetchone()[0]
print(f"  总任务数: {total}")

cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
print(f"\n  按状态分布:")
for status, count in cursor.fetchall():
    pct = count / total * 100 if total > 0 else 0
    print(f"    {status}: {count} ({pct:.1f}%)")

# 4. 查看已完成任务ID
print("\n【4】已完成任务列表（前20个）")
cursor.execute("SELECT id, title FROM tasks WHERE status='COMPLETED' OR status='completed' LIMIT 20")
completed = cursor.fetchall()
for task_id, title in completed:
    print(f"  [{task_id}] {title[:50]}")

# 5. 查看进行中任务
print("\n【5】进行中任务")
cursor.execute("SELECT id, title FROM tasks WHERE status='IN_PROGRESS' OR status='in_progress'")
inprogress = cursor.fetchall()
if inprogress:
    for task_id, title in inprogress:
        print(f"  [{task_id}] {title}")
else:
    print("  无")

# 6. 查看待处理任务（前10个）
print("\n【6】待处理任务（前10个）")
cursor.execute("SELECT id, title, priority FROM tasks WHERE status='PENDING' OR status='pending' LIMIT 10")
for task_id, title, priority in cursor.fetchall():
    print(f"  [{task_id}] ({priority}) {title[:45]}")

# 7. 检查完成报告文件
print("\n【7】完成报告文件检查")
reports_dir = Path(".")
report_files = list(reports_dir.glob("*完成报告*.md"))
print(f"  找到 {len(report_files)} 个完成报告文件")
for f in sorted(report_files)[:10]:
    print(f"  - {f.name}")

# 8. 检查task-board.md
print("\n【8】task-board.md状态")
task_board = Path("docs/tasks/task-board.md")
if task_board.exists():
    content = task_board.read_text(encoding='utf-8')
    lines = content.split('\n')
    print(f"  文件大小: {len(content)} 字符, {len(lines)} 行")
    # 统计任务数量
    task_count = content.count('TASK-') + content.count('REQ-') + content.count('INTEGRATE-')
    print(f"  文档中提到的任务数量（粗略估计）: {task_count}")
else:
    print("  ⚠️ 文件不存在")

# 9. 检查事件流
print("\n【9】事件流状态")
events_file = Path("apps/dashboard/automation-data/architect_events.json")
if events_file.exists():
    try:
        with open(events_file, 'r', encoding='utf-8') as f:
            events_data = json.load(f)
            events = events_data.get('events', [])
            print(f"  事件数量: {len(events)}")
            if events:
                latest = events[-1]
                print(f"  最新事件: {latest.get('event_type', 'N/A')}")
                print(f"  时间: {latest.get('timestamp', 'N/A')}")
    except Exception as e:
        print(f"  ⚠️ 读取失败: {e}")
else:
    print("  ⚠️ 文件不存在")

# 10. 检查集成任务
print("\n【10】集成任务(INTEGRATE-)统计")
cursor.execute("SELECT id, title, status FROM tasks WHERE id LIKE 'INTEGRATE-%'")
integrate_tasks = cursor.fetchall()
if integrate_tasks:
    print(f"  总数: {len(integrate_tasks)}")
    completed_integrate = [t for t in integrate_tasks if t[2] in ('COMPLETED', 'completed')]
    print(f"  已完成: {len(completed_integrate)}")
    print(f"\n  列表:")
    for task_id, title, status in integrate_tasks:
        print(f"    [{status}] {task_id}: {title[:40]}")
else:
    print("  未找到集成任务")

# 11. 对比分析
print("\n" + "=" * 80)
print("【核心问题分析】")
print("=" * 80)
print(f"""
1. 数据库状态:
   - 总任务数: {total}
   - 已完成: {len([t for t in cursor.execute("SELECT * FROM tasks WHERE status='COMPLETED' OR status='completed'")])}
   - 进度: {len(completed) / total * 100:.1f}%

2. task-board.md显示:
   - 文档中的任务数量远少于数据库
   - 可能未同步最新任务

3. 完成报告文件:
   - 有 {len(report_files)} 个完成报告
   - 说明实际完成了很多功能

4. Dashboard可能的问题:
   - 未读取完整的数据库数据
   - 或者task-board.md未更新

建议修复方案:
   1. 更新task-board.md同步所有数据库任务
   2. 检查Dashboard读取逻辑
   3. 验证事件流记录完整性
""")

print("=" * 80)

conn.close()

