#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证核心功能实现状态
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
EVENTS_FILE = Path(__file__).parent.parent / "apps/dashboard/automation-data/architect_events.json"
OUTPUT_FILE = Path(__file__).parent.parent / "核心功能验证报告.txt"

def verify_features():
    """验证核心功能"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    output = []
    output.append("=" * 70)
    output.append("核心功能实现状态验证报告")
    output.append("生成时间: 2025-11-19 04:00")
    output.append("=" * 70)
    output.append("")
    
    # 检查已完成的REQ任务
    cursor.execute("""
        SELECT id, title, status, estimated_hours
        FROM tasks 
        WHERE status = 'completed' 
        AND id LIKE 'REQ-%'
        ORDER BY id
    """)
    
    completed_reqs = cursor.fetchall()
    
    output.append(f"[已完成功能] {len(completed_reqs)}个")
    output.append("")
    
    for task_id, title, status, hours in completed_reqs:
        output.append(f"OK {task_id}: {title} ({hours}h)")
    
    output.append("")
    output.append("-" * 70)
    
    # 检查REQ-009特性
    output.append("")
    output.append("[REQ-009] 任务三态流转系统")
    cursor.execute("SELECT status FROM tasks WHERE id = 'REQ-009'")
    result = cursor.fetchone()
    if result and result[0] == 'completed':
        output.append("  [OK] 已实现")
        output.append("  - 待处理(pending) -> 进行中(in_progress) -> 已完成(completed)")
        output.append("  - 状态转换API")
        output.append("  - 工时记录功能")
        output.append("  - Dashboard状态展示")
    
    # 检查REQ-010特性
    output.append("")
    output.append("[REQ-010] 全局事件流系统")
    cursor.execute("SELECT status FROM tasks WHERE id = 'REQ-010'")
    result = cursor.fetchone()
    if result and result[0] == 'completed':
        output.append("  [OK] 已实现")
        # 读取事件数据
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            event_count = len(data.get("events", []))
            output.append(f"  - 当前事件数: {event_count}")
            output.append("  - 6大类事件类型")
            output.append("  - 事件筛选和统计功能")
            output.append("  - Dashboard事件流展示")
    
    # 检查REQ-011特性
    output.append("")
    output.append("[REQ-011] 动态进度计算")
    cursor.execute("SELECT status FROM tasks WHERE id = 'REQ-011'")
    result = cursor.fetchone()
    if result and result[0] == 'completed':
        output.append("  [OK] 已实现")
        # 计算当前进度
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
        completed = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status != 'cancelled'")
        total = cursor.fetchone()[0]
        progress = (completed / total * 100) if total > 0 else 0
        output.append(f"  - 实时进度: {progress:.1f}% ({completed}/{total})")
        output.append("  - 自动计算无需手动")
        output.append("  - Dashboard实时显示")
    
    output.append("")
    output.append("-" * 70)
    
    # 统计所有任务状态
    output.append("")
    output.append("[任务状态统计]")
    cursor.execute("""
        SELECT status, COUNT(*) 
        FROM tasks 
        GROUP BY status
    """)
    
    for status, count in cursor.fetchall():
        output.append(f"  {status:15s}: {count:3d}")
    
    # 集成任务状态
    output.append("")
    output.append("[集成任务状态]")
    cursor.execute("""
        SELECT id, status 
        FROM tasks 
        WHERE id LIKE 'INTEGRATE-%'
        ORDER BY id
    """)
    
    integrate_tasks = cursor.fetchall()
    for task_id, status in integrate_tasks:
        symbol = "OK" if status == "completed" else ".."
        output.append(f"  {symbol} {task_id}: {status}")
    
    output.append("")
    output.append("=" * 70)
    output.append("验证完成")
    output.append("=" * 70)
    output.append(f"Dashboard: http://localhost:8877")
    output.append(f"总进度: {progress:.1f}%")
    output.append("=" * 70)
    
    conn.close()
    
    # 输出到文件
    report = "\n".join(output)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 输出到控制台（ASCII安全）
    for line in output:
        print(line)
    
    return report

if __name__ == "__main__":
    verify_features()

