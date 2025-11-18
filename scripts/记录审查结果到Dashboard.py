#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录REQ-002审查结果到Dashboard
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_review_events():
    """添加审查事件到事件流"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 添加审查事件
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "code_review",
            "icon": "🏛️",
            "content": "收到李明完成报告：REQ-002项目记忆空间（6.5h，2575行代码）"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "code_review",
            "icon": "🔍",
            "content": "深度审查：架构优秀⭐⭐⭐⭐⭐，但核心查询未实现（TODO）"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "code_review",
            "icon": "⚠️",
            "content": "审查结果：有条件通过✅ - 架构完成100%，实现完成30%"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "document",
            "icon": "📋",
            "content": "生成审查报告：🏛️架构师审查-REQ-002完成报告.md"
        },
        {
            "id": f"event-{len(data['events']) + 5:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_dispatch",
            "icon": "🔧",
            "content": "创建修复任务：REQ-002-B（实现数据库查询，4h，P0）→ 李明"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} review events")
    return len(new_events)

def main():
    print("=" * 60)
    print("[Dashboard] Record review results")
    print("=" * 60)
    print()
    
    count = add_review_events()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Dashboard updated")
    print("=" * 60)
    print(f"[Events] +{count} events")
    print(f"[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

