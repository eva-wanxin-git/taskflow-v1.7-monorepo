#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描所有完成报告文件，自动更新任务状态
"""

import json
import sqlite3
import re
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
PROJECT_ROOT = Path(__file__).parent.parent

def scan_completion_reports():
    """扫描所有完成报告文件"""
    patterns = [
        "✅*完成报告*.md",
        "*完成报告*.md",
        "REQ-*完成*.md",
        "TASK-*完成*.md"
    ]
    
    found_reports = {}
    
    for pattern in patterns:
        files = list(PROJECT_ROOT.glob(pattern))
        for file in files:
            # 从文件名提取任务ID
            filename = file.name
            
            # 尝试匹配 REQ-XXX 或 TASK-XXX
            match = re.search(r'(REQ-\d+[A-Z]?|TASK-[A-Z]-\d+)', filename)
            if match:
                task_id = match.group(1)
                found_reports[task_id] = str(file)
    
    return found_reports

def update_task_status(task_id, report_path):
    """更新单个任务状态为completed"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # 检查任务是否存在
    cursor.execute("SELECT id, status FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return False, "任务不存在"
    
    current_status = row[1]
    
    # 如果已经是completed，跳过
    if current_status == 'completed':
        conn.close()
        return False, "已经是completed"
    
    # 更新状态
    metadata = json.dumps({
        "completion_report": report_path,
        "completed_at": datetime.now().isoformat(),
        "auto_detected": True
    }, ensure_ascii=False)
    
    cursor.execute("""
        UPDATE tasks 
        SET status = 'completed', 
            updated_at = ?,
            metadata = json_patch(COALESCE(metadata, '{}'), ?)
        WHERE id = ?
    """, (datetime.now().isoformat(), metadata, task_id))
    
    conn.commit()
    conn.close()
    
    return True, "已更新"

def main():
    print("=" * 60)
    print("[Auto-Detect] Scan all completion reports")
    print("=" * 60)
    print()
    
    # 扫描完成报告
    reports = scan_completion_reports()
    
    print(f"[Found] {len(reports)} completion reports:")
    for task_id, path in reports.items():
        filename = Path(path).name
        # 避免GBK编码问题，只打印task_id
        print(f"  - {task_id}")
    
    print()
    print("[Updating] Task status in database...")
    print()
    
    updated = 0
    skipped = 0
    not_found = 0
    
    for task_id, report_path in reports.items():
        success, message = update_task_status(task_id, report_path)
        if success:
            print(f"  [OK] {task_id} -> COMPLETED")
            updated += 1
        elif "不存在" in message:
            print(f"  [SKIP] {task_id} (not in database)")
            not_found += 1
        else:
            print(f"  [SKIP] {task_id} ({message})")
            skipped += 1
    
    print()
    print("=" * 60)
    print("[SUCCESS] Status update complete")
    print("=" * 60)
    print(f"[Updated] {updated} tasks")
    print(f"[Already Completed] {skipped} tasks")
    print(f"[Not in DB] {not_found} tasks")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

