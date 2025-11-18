#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync task-board.md with database
Generate complete task board from database
"""

import sqlite3
from pathlib import Path
from datetime import datetime

# Paths
project_root = Path(__file__).parent.parent
db_path = project_root / "database/data/tasks.db"
board_path = project_root / "docs/tasks/task-board.md"

print("Syncing task-board.md with database...")

# Connect database
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all tasks
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
total = len(all_tasks)
completed = len([t for t in all_tasks if t['status'] == 'completed'])
in_progress = len([t for t in all_tasks if t['status'] == 'in_progress'])
pending = len([t for t in all_tasks if t['status'] == 'pending'])
cancelled = len([t for t in all_tasks if t['status'] == 'cancelled'])
progress_pct = (completed / total * 100) if total > 0 else 0

# Generate markdown
md = f"""# Task Board - TaskFlow v1.7

**Update Time**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Project**: TaskFlow (This System)  
**Project Code**: TASKFLOW  
**Chief Architect**: AI Architect (Expert Level)  
**Port**: 8877  
**URL**: http://localhost:8877

---

## Project Status

### Progress
```
{completed}/{total} tasks completed ({progress_pct:.1f}%)

Status Distribution:
- Completed: {completed} tasks ({completed/total*100:.1f}%)
- In Progress: {in_progress} tasks ({in_progress/total*100:.1f}%)
- Pending: {pending} tasks ({pending/total*100:.1f}%)
- Cancelled: {cancelled} tasks ({cancelled/total*100:.1f}%)
```

---

## Completed Tasks ({completed})

"""

# Completed tasks
completed_tasks = [t for t in all_tasks if t['status'] == 'completed']
for task in completed_tasks:
    md += f"""
### {task['id']}: {task['title']}

**Status**: COMPLETED  
**Priority**: {task['priority'] or 'N/A'}  
**Hours**: Estimated {task['estimated_hours'] or 0}h / Actual {task['actual_hours'] or 0}h  
**Assignee**: {task['assigned_to'] or 'N/A'}  
**Completed**: {task['completed_at'] or 'N/A'}

**Description**:
{task['description'] or 'N/A'}

---
"""

# In Progress tasks
md += f"""
## In Progress Tasks ({in_progress})

"""

inprogress_tasks = [t for t in all_tasks if t['status'] == 'in_progress']
if inprogress_tasks:
    for task in inprogress_tasks:
        md += f"""
### {task['id']}: {task['title']}

**Status**: IN PROGRESS  
**Priority**: {task['priority'] or 'N/A'}  
**Estimated Hours**: {task['estimated_hours'] or 0}h  
**Assignee**: {task['assigned_to'] or 'N/A'}  
**Dependencies**: {task['depends_on'] or 'None'}

**Description**:
{task['description'] or 'N/A'}

---
"""
else:
    md += "\nNo tasks in progress\n\n---\n"

# Pending tasks by priority
p0 = [t for t in all_tasks if t['status'] == 'pending' and t['priority'] == 'P0']
p1 = [t for t in all_tasks if t['status'] == 'pending' and t['priority'] == 'P1']
p2 = [t for t in all_tasks if t['status'] == 'pending' and t['priority'] == 'P2']

md += f"""
## Pending Tasks ({pending})

### P0 - Critical ({len(p0)})

"""
for task in p0:
    md += f"""
#### {task['id']}: {task['title']}

**Priority**: P0 Critical  
**Estimated**: {task['estimated_hours'] or 0}h  
**Complexity**: {task['complexity'] or 'medium'}  
**Assignee**: {task['assigned_to'] or 'N/A'}  
**Dependencies**: {task['depends_on'] or 'None'}

**Description**:
{task['description'] or 'N/A'}

---
"""

md += f"""
### P1 - High ({len(p1)})

"""
for task in p1:
    md += f"""
#### {task['id']}: {task['title']}

**Priority**: P1 High  
**Estimated**: {task['estimated_hours'] or 0}h  
**Complexity**: {task['complexity'] or 'medium'}  
**Assignee**: {task['assigned_to'] or 'N/A'}  
**Dependencies**: {task['depends_on'] or 'None'}

**Description**:
{task['description'] or 'N/A'}

---
"""

md += f"""
### P2 - Medium ({len(p2)})

"""
for task in p2:
    md += f"""
#### {task['id']}: {task['title']}

**Priority**: P2 Medium  
**Estimated**: {task['estimated_hours'] or 0}h  
**Complexity**: {task['complexity'] or 'medium'}  
**Assignee**: {task['assigned_to'] or 'N/A'}  
**Dependencies**: {task['depends_on'] or 'None'}

**Description**:
{task['description'] or 'N/A'}

---
"""

# Cancelled tasks
cancelled_tasks = [t for t in all_tasks if t['status'] == 'cancelled']
md += f"""
## Cancelled Tasks ({cancelled})

"""
if cancelled_tasks:
    for task in cancelled_tasks:
        md += f"- {task['id']}: {task['title']}\n"
    md += "\n---\n"
else:
    md += "\nNo cancelled tasks\n\n---\n"

# Summary
md += f"""
## Task Statistics

| Status | Count | Percentage |
|--------|-------|------------|
| Completed | {completed} | {completed/total*100:.1f}% |
| In Progress | {in_progress} | {in_progress/total*100:.1f}% |
| Pending | {pending} | {pending/total*100:.1f}% |
| Cancelled | {cancelled} | {cancelled/total*100:.1f}% |
| **Total** | **{total}** | **100%** |

---

**Board Version**: v2.0 (Database-Driven)  
**Last Update**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Maintainer**: AI Architect (Expert)  
**Data Source**: database/data/tasks.db  
**Dashboard**: http://localhost:8877
"""

# Backup old file
if board_path.exists():
    backup = board_path.parent / f"task-board-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    board_path.rename(backup)
    print(f"\nOld version backed up: {backup.name}")

# Write new file
board_path.write_text(md, encoding='utf-8')

print(f"\nTask board updated!")
print(f"  File: {board_path}")
print(f"  Tasks: {total}")
print(f"  Progress: {progress_pct:.1f}%")
print(f"  Completed: {completed}/{total}")
print("\n" + "=" * 60)
print(f"Task board sync completed!")
print(f"View at: docs/tasks/task-board.md")
print("=" * 60)

conn.close()

