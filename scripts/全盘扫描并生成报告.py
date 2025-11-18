#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全盘扫描所有完成报告并生成完整报告
"""

import sqlite3
import re
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
PROJECT_ROOT = Path(__file__).parent.parent

def scan_all_completion_reports():
    """扫描所有完成报告"""
    patterns = [
        "✅*.md",
        "*完成报告*.md",
        "*完成.md"
    ]
    
    found = {}
    
    for pattern in patterns:
        files = list(PROJECT_ROOT.glob(pattern))
        for file in files:
            # 从文件名提取任务ID
            filename = file.name
            match = re.search(r'(REQ-\d+[A-Z]?|TASK-[A-Z]-\d+|BUG-\d+)', filename)
            if match:
                task_id = match.group(1)
                if task_id not in found:
                    found[task_id] = file
    
    return found

def get_current_status():
    """获取当前数据库状态"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status != 'cancelled'")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
    completed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
    pending = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "rate": round(completed / total * 100, 1) if total > 0 else 0
    }

def main():
    print("=" * 60)
    print("[Full Scan] Scan all completion reports")
    print("=" * 60)
    print()
    
    # 扫描完成报告
    reports = scan_all_completion_reports()
    
    print(f"[Found] {len(reports)} completion reports:")
    for task_id in sorted(reports.keys()):
        print(f"  - {task_id}")
    
    # 获取当前状态
    print("\n[Database Status]")
    status = get_current_status()
    print(f"  Total: {status['total']} tasks")
    print(f"  Completed: {status['completed']} tasks")
    print(f"  Pending: {status['pending']} tasks")
    print(f"  Progress: {status['rate']}%")
    
    print()
    print("=" * 60)
    print("[RESULT]")
    print("=" * 60)
    print(f"  Found reports: {len(reports)}")
    print(f"  DB shows completed: {status['completed']}")
    print(f"  Match: {'YES' if len(reports) == status['completed'] else 'NO - Update needed'}")

if __name__ == "__main__":
    main()

