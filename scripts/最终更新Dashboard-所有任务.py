#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终更新Dashboard - 记录所有新创建的任务和修复
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_final_events():
    """添加最终事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "user_feedback",
            "icon": "🚨",
            "content": "用户反馈：REQ-009分析了但没创建任务！"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "self_review",
            "icon": "❌",
            "content": "架构师自我检查：又犯错了！分析完必须立即录入任务！"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_create",
            "icon": "✅",
            "content": "立即修复：录入REQ-009和3个子任务（A一键复制2h/B脚本1.5h/C刷新0.5h）"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "📊",
            "content": "当前待办任务总数：28个（验证2+REQ-004五个+REQ-010六个+REQ-009四个+TASK-C三个+其他）"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} final events")
    return len(new_events)

def update_monitor():
    """最终更新监控数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新Token
    data['token_usage']['used'] = 206000
    data['token_usage']['percentage'] = 20.6
    
    # 更新任务数
    data['project_info']['pending_tasks'] = 28
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[OK] Final monitor update: Token 206K (20.6%), Tasks 28")

def main():
    print("=" * 60)
    print("[Dashboard] Final update - All tasks recorded")
    print("=" * 60)
    print()
    
    count = add_final_events()
    update_monitor()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Dashboard fully updated")
    print("=" * 60)
    print(f"[Events] +{count} events (Total: 53+)")
    print(f"[Tasks] 28 pending tasks")
    print(f"[Completed] 3 tasks")
    print(f"[Token] 206K/1M (20.6%)")
    print()
    print("[Dashboard] http://localhost:8877")
    print()
    print("[User should see]")
    print("  - Pending Tasks: 28")
    print("  - Event Stream: 53+ events")
    print("  - Task breakdown clear")

if __name__ == "__main__":
    main()

