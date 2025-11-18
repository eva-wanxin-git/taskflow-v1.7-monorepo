#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录REQ-009需求分析到Dashboard
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "apps" / "dashboard" / "automation-data"

def add_analysis_events():
    """添加需求分析事件"""
    events_file = DATA_DIR / "architect_events.json"
    
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_events = [
        {
            "id": f"event-{len(data['events']) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "user_feedback",
            "icon": "💡",
            "content": "用户需求：任务应该由李明自己更新状态，不是架构师手动维护"
        },
        {
            "id": f"event-{len(data['events']) + 2:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "requirement",
            "icon": "📋",
            "content": "识别新需求：REQ-009任务自动化流程（待处理→进行中→已完成）"
        },
        {
            "id": f"event-{len(data['events']) + 3:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "analysis",
            "icon": "🤔",
            "content": "深度分析：设计3个方案（文件监听8h/API提交4h⭐/UI操作12h）"
        },
        {
            "id": f"event-{len(data['events']) + 4:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "document",
            "icon": "📊",
            "content": "产出分析报告：3方案对比+4个追问问题→等待用户回答"
        }
    ]
    
    data['events'].extend(new_events)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Added {len(new_events)} analysis events")
    return len(new_events)

def main():
    print("=" * 60)
    print("[Dashboard] Record REQ-009 analysis")
    print("=" * 60)
    print()
    
    count = add_analysis_events()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Analysis recorded")
    print("=" * 60)
    print(f"[Events] +{count} events")
    print(f"[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

