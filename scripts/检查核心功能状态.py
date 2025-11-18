#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查核心功能实现状态
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
EVENTS_FILE = Path(__file__).parent.parent / "apps/dashboard/automation-data/architect_events.json"

def check_core_features():
    """检查核心功能"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("核心功能实现状态检查")
    print("=" * 70)
    print()
    
    # 检查REQ-009: 任务三态流转
    print("[1] REQ-009: 任务三态流转系统")
    cursor.execute("SELECT status, description FROM tasks WHERE id = 'REQ-009'")
    result = cursor.fetchone()
    if result:
        status = result[0]
        print(f"   状态: {status}")
        if status == "completed":
            print("   ✓ 任务三态流转已实现")
            print("   - 待处理 → 进行中 → 已完成")
            print("   - 状态转换API")
            print("   - 工时记录功能")
        else:
            print(f"   ✗ 尚未完成 (当前: {status})")
    print()
    
    # 检查REQ-010: 全局事件流
    print("[2] REQ-010: 全局事件流系统")
    cursor.execute("SELECT status FROM tasks WHERE id = 'REQ-010'")
    result = cursor.fetchone()
    if result:
        status = result[0]
        print(f"   状态: {status}")
        if status == "completed":
            print("   ✓ 全局事件流已实现")
            # 读取事件数据
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                event_count = len(data.get("events", []))
                print(f"   - 当前事件数: {event_count}")
                print("   - 6大类事件类型")
                print("   - 事件筛选和统计")
        else:
            print(f"   ✗ 尚未完成 (当前: {status})")
    print()
    
    # 检查REQ-011: 动态进度计算
    print("[3] REQ-011: 动态进度计算")
    cursor.execute("SELECT status FROM tasks WHERE id = 'REQ-011'")
    result = cursor.fetchone()
    if result:
        status = result[0]
        print(f"   状态: {status}")
        if status == "completed":
            print("   ✓ 动态进度计算已实现")
            # 计算实时进度
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
            completed = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status != 'cancelled'")
            total = cursor.fetchone()[0]
            progress = (completed / total * 100) if total > 0 else 0
            print(f"   - 实时进度: {progress:.1f}% ({completed}/{total})")
        else:
            print(f"   ✗ 尚未完成 (当前: {status})")
    print()
    
    # 检查其他完成的功能
    print("[4] 其他已完成功能")
    cursor.execute("""
        SELECT id, title, status 
        FROM tasks 
        WHERE status = 'completed' 
        AND id LIKE 'REQ-%'
        ORDER BY id
    """)
    
    completed_reqs = cursor.fetchall()
    for task_id, title, status in completed_reqs:
        print(f"   ✓ {task_id}: {title}")
    
    print()
    print("=" * 70)
    print("检查完成")
    print("=" * 70)
    print(f"已完成REQ任务: {len(completed_reqs)}个")
    print(f"总进度: {progress:.1f}%")
    print()
    print("Dashboard: http://localhost:8877")
    print("=" * 70)
    
    conn.close()

if __name__ == "__main__":
    check_core_features()

