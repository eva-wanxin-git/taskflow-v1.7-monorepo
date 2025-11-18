#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新任务看板 task-board.md
从数据库读取所有54个任务，更新到task-board.md
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# 数据库路径
project_root = Path(__file__).parent.parent
db_path = project_root / "database/data/tasks.db"
task_board_path = project_root / "docs/tasks/task-board.md"

print("=" * 80)
print("  更新任务看板 - task-board.md")
print("=" * 80)

if not db_path.exists():
    print(f"\n❌ 数据库不存在: {db_path}")
    sys.exit(1)

# 连接数据库
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row  # 可以用字段名访问
cursor = conn.cursor()

# 读取所有任务
cursor.execute("""
SELECT id, title, description, status, priority, estimated_hours,
       actual_hours, complexity, assigned_to, depends_on, created_at, completed_at
FROM tasks
ORDER BY 
  CASE status
    WHEN 'completed' THEN 1
    WHEN 'in_progress' THEN 2
    WHEN 'pending' THEN 3
    WHEN 'cancelled' THEN 4
  END,
  CASE priority
    WHEN 'P0' THEN 1
    WHEN 'P1' THEN 2
    WHEN 'P2' THEN 3
  END,
  id
""")

all_tasks = [dict(row) for row in cursor.fetchall()]

# 统计
total = len(all_tasks)
completed = len([t for t in all_tasks if t['status'] == 'completed'])
in_progress = len([t for t in all_tasks if t['status'] == 'in_progress'])
pending = len([t for t in all_tasks if t['status'] == 'pending'])
cancelled = len([t for t in all_tasks if t['status'] == 'cancelled'])
progress_pct = (completed / total * 100) if total > 0 else 0

print(f"\n📊 数据库任务统计:")
print(f"  总任务: {total}")
print(f"  已完成: {completed} ({completed/total*100:.1f}%)")
print(f"  进行中: {in_progress}")
print(f"  待处理: {pending}")
print(f"  已取消: {cancelled}")

# 生成Markdown内容
md_content = f"""# 📋 任务所·Flow v1.7 - 任务看板

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**项目**: 任务所·Flow（本系统）  
**项目代码**: TASKFLOW  
**总架构师**: AI Architect (Expert Level)  
**维护范围**: v1.7版本

**📍 端口信息**:
- **Dashboard端口**: 8877（当前）
- **访问地址**: http://localhost:8877
- **端口范围**: 8870-8899（任务所Flow专用）

---

## 📊 项目状态总览

### 整体进度
```
[████████████████████████░░░░░░░░] {progress_pct:.1f}% 完成

已完成: {completed}/{total} 任务
进行中: {in_progress} 任务
待处理: {pending} 任务
已取消: {cancelled} 任务
```

### 统计数据
- **总任务**: {total}个
- **已完成**: {completed}个 ({progress_pct:.1f}%)
- **进行中**: {in_progress}个
- **待处理**: {pending}个
- **已取消**: {cancelled}个

---

## ✅ 已完成任务 ({completed}个)

"""

# 添加已完成任务
completed_tasks = [t for t in all_tasks if t['status'] == 'completed']
for task in completed_tasks:
    md_content += f"""
### {task['id']}: {task['title']} ✅

**状态**: 已完成  
**优先级**: {task['priority'] or 'N/A'}  
**工时**: 预估{task['estimated_hours'] or 0}h / 实际{task['actual_hours'] or 0}h  
**负责人**: {task['assigned_to'] or 'N/A'}  
**完成时间**: {task['completed_at'] or 'N/A'}

**任务描述**:
{task['description'] or '无'}

---
"""

# 添加进行中任务
md_content += f"""
## 🟡 进行中任务 ({in_progress}个)

"""

inprogress_tasks = [t for t in all_tasks if t['status'] == 'in_progress']
if inprogress_tasks:
    for task in inprogress_tasks:
        md_content += f"""
### {task['id']}: {task['title']} 🟡

**状态**: 进行中  
**优先级**: {task['priority'] or 'N/A'}  
**预估工时**: {task['estimated_hours'] or 0}h  
**负责人**: {task['assigned_to'] or 'N/A'}  
**依赖**: {task['depends_on'] or '无'}

**任务描述**:
{task['description'] or '无'}

---
"""
else:
    md_content += "\n暂无进行中任务\n\n---\n"

# 添加待处理任务（按优先级）
md_content += f"""
## ⏳ 待处理任务 ({pending}个)

"""

# 按优先级分组
p0_tasks = [t for t in all_tasks if t['status'] == 'pending' and t['priority'] == 'P0']
p1_tasks = [t for t in all_tasks if t['status'] == 'pending' and t['priority'] == 'P1']
p2_tasks = [t for t in all_tasks if t['status'] == 'pending' and t['priority'] == 'P2']

md_content += f"""
### 🔴 P0 - Critical ({len(p0_tasks)}个)

"""
for task in p0_tasks:
    md_content += f"""
#### {task['id']}: {task['title']}

**优先级**: 🔴 P0  
**预估工时**: {task['estimated_hours'] or 0}h  
**复杂度**: {task['complexity'] or 'medium'}  
**负责人**: {task['assigned_to'] or 'N/A'}  
**依赖**: {task['depends_on'] or '无'}

**任务描述**:
{task['description'] or '无'}

---
"""

md_content += f"""
### 🟡 P1 - High ({len(p1_tasks)}个)

"""
for task in p1_tasks:
    md_content += f"""
#### {task['id']}: {task['title']}

**优先级**: 🟡 P1  
**预估工时**: {task['estimated_hours'] or 0}h  
**复杂度**: {task['complexity'] or 'medium'}  
**负责人**: {task['assigned_to'] or 'N/A'}  
**依赖**: {task['depends_on'] or '无'}

**任务描述**:
{task['description'] or '无'}

---
"""

md_content += f"""
### 🟢 P2 - Medium ({len(p2_tasks)}个)

"""
for task in p2_tasks:
    md_content += f"""
#### {task['id']}: {task['title']}

**优先级**: 🟢 P2  
**预估工时**: {task['estimated_hours'] or 0}h  
**复杂度**: {task['complexity'] or 'medium'}  
**负责人**: {task['assigned_to'] or 'N/A'}  
**依赖**: {task['depends_on'] or '无'}

**任务描述**:
{task['description'] or '无'}

---
"""

# 添加已取消任务
md_content += f"""
## ❌ 已取消任务 ({cancelled}个)

"""
cancelled_tasks = [t for t in all_tasks if t['status'] == 'cancelled']
if cancelled_tasks:
    for task in cancelled_tasks:
        md_content += f"""
### {task['id']}: {task['title']} ❌

**原因**: 不再需要或已被其他任务替代

---
"""
else:
    md_content += "\n暂无已取消任务\n\n---\n"

# 添加页脚
md_content += f"""
## 📊 任务统计

| 状态 | 数量 | 百分比 |
|------|------|--------|
| ✅ 已完成 | {completed} | {completed/total*100:.1f}% |
| 🟡 进行中 | {in_progress} | {in_progress/total*100:.1f}% |
| ⏳ 待处理 | {pending} | {pending/total*100:.1f}% |
| ❌ 已取消 | {cancelled} | {cancelled/total*100:.1f}% |
| **总计** | **{total}** | **100%** |

---

**看板版本**: v2.0 (数据库驱动)  
**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**维护者**: AI Architect (Expert)  
**数据来源**: database/data/tasks.db  
**更新频率**: 每次任务状态变更后自动更新

📋 **任务所·Flow v1.7 任务看板已更新！**
"""

# 备份旧文件
if task_board_path.exists():
    backup_path = task_board_path.parent / f"task-board-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    task_board_path.rename(backup_path)
    print(f"\n📦 旧版本已备份: {backup_path.name}")

# 写入新文件
task_board_path.write_text(md_content, encoding='utf-8')
print(f"\n✅ 任务看板已更新!")
print(f"   文件: {task_board_path}")
print(f"   任务数: {total}")
print(f"   进度: {progress_pct:.1f}%")

print("\n" + "=" * 80)
print(f"✅ 看板更新完成！")
print(f"📊 {completed}/{total} 任务已完成 ({progress_pct:.1f}%)")
print(f"📍 立即查看: docs/tasks/task-board.md")
print("=" * 80)

conn.close()

