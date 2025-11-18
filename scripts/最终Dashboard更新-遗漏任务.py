#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终Dashboard更新 - 记录遗漏任务的发现和补充
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_missing_task_events():
    """添加遗漏任务发现事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "audit",
            "icon": "🔍",
            "content": "用户指示：检查聊天记录，找出遗漏的任务"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "audit",
            "icon": "❌",
            "content": "审计发现：3个需求未拆解（REQ-005 Dashboard重构16h/REQ-007封装8h/REQ-008测试12h）"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_create",
            "icon": "✅",
            "content": "立即补充：创建3个分析任务（ARCH-005分析1h/USER-007确认0h/ARCH-008设计1h）"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "milestone",
            "icon": "📊",
            "content": "完整任务清单：31个任务（3已完成+28待处理），100%需求已转化为任务"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} audit events")
    return len(new_events)

def update_final_monitor():
    """最终更新监控数据"""
    monitor_file = DATA_DIR / "architect_monitor.json"
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新Token
    data['token_usage']['used'] = 210000
    data['token_usage']['percentage'] = 21.0
    
    # 更新任务数
    data['project_info']['pending_tasks'] = 31  # 28 + 3
    
    with open(monitor_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[OK] Final monitor: Token 210K (21.0%), Tasks 31 total")

def main():
    print("=" * 60)
    print("[Dashboard] Final update - Missing tasks found")
    print("=" * 60)
    print()
    
    count = add_missing_task_events()
    update_final_monitor()
    
    print()
    print("=" * 60)
    print("[COMPLETE] All requirements converted to tasks")
    print("=" * 60)
    print(f"[Events] +{count} events (Total: 57+)")
    print(f"[Tasks] 31 total (3 completed + 28 pending)")
    print(f"[Token] 210K/1M (21.0%)")
    print()
    print("[Missing Found]")
    print("  - REQ-005: Dashboard refactor (needs analysis)")
    print("  - REQ-007: Package v1.7 (needs clarification)")
    print("  - REQ-008: Real test (needs design)")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

