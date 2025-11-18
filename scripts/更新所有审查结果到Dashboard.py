#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新所有审查结果到Dashboard
包括：REQ-003审查 + REQ-009方案确定
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def update_req003_status():
    """更新REQ-003状态为已完成"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE tasks 
        SET status = 'completed', 
            updated_at = ? 
        WHERE id = 'REQ-003'
    """, (datetime.now().isoformat(),))
    
    conn.commit()
    conn.close()
    print("[OK] REQ-003 status updated to COMPLETED")

def add_all_events():
    """添加所有审查和分析事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "code_review",
            "icon": "🎉",
            "content": "审查REQ-003（对话历史库）：完全通过✅ - 100%完成，满分作品！"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "🏆",
            "content": "里程碑：李明三连满分！REQ-001(10/10) + REQ-006(10/10) + REQ-003(10/10)"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "user_feedback",
            "icon": "💡",
            "content": "用户反馈：李明工作环境=新Cursor对话（独立AI）"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "analysis",
            "icon": "🎯",
            "content": "REQ-009方案确定：半自动化文件流程（API+脚本+一键复制）"
        },
        {
            "id": f"event-{len(data['events']) + 5:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "document",
            "icon": "📋",
            "content": "拆解REQ-009为3个子任务：REQ-009-A(一键复制2h) + B(脚本1h) + C(刷新1h)"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} events")
    return len(new_events)

def update_monitor():
    """更新监控数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新Token
    data['token_usage']['used'] = 147000
    data['token_usage']['percentage'] = 14.7
    
    # 更新项目信息
    data['project_info']['pending_tasks'] = 10  # 13 - 3
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[OK] Monitor data updated: Token 147K (14.7%)")

def main():
    print("=" * 60)
    print("[Dashboard] Batch update - All reviews")
    print("=" * 60)
    print()
    
    # 更新REQ-003状态
    print("[Step 1] Update REQ-003 status...")
    update_req003_status()
    print()
    
    # 添加所有事件
    print("[Step 2] Add review events...")
    event_count = add_all_events()
    print()
    
    # 更新监控
    print("[Step 3] Update monitor...")
    update_monitor()
    print()
    
    print("=" * 60)
    print("[SUCCESS] All reviews recorded")
    print("=" * 60)
    print(f"[Completed] REQ-001, REQ-006, REQ-003 (3x perfect)")
    print(f"[Events] +{event_count} events")
    print(f"[Token] 147K/1M (14.7%)")
    print(f"[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

