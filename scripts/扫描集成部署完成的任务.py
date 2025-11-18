#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描集成部署完成的任务
基于文件名和内容识别
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# 需要检查的任务列表
TASKS_TO_CHECK = [
    "REQ-001",  # 缓存解决方案
    "REQ-009",  # 任务三态流转
    "REQ-009-A", "REQ-009-B", "REQ-009-C",
    "REQ-010",  # 事件流系统
    "REQ-010-A", "REQ-010-B", "REQ-010-C", "REQ-010-D", "REQ-010-E",
    "TASK-FIX-001", "TASK-FIX-002"
]

def scan_completion_files():
    """扫描完成文件"""
    patterns = [
        "*2025-11-18*.md",
        "✅REQ-009*.md",
        "✅REQ-010*.md",
        "📖*快速*.md",
        "📝李明*.md",
        "🎊*集成*.md",
        "✅*完成*.md"
    ]
    
    found_files = {}
    
    for pattern in patterns:
        files = list(PROJECT_ROOT.glob(pattern))
        for file in files:
            # 提取任务ID
            match = re.search(r'(REQ-\d+[A-Z]?|TASK-[A-Z]+-\d+|TASK-FIX-\d+)', file.name)
            if match:
                task_id = match.group(1)
                if task_id not in found_files:
                    found_files[task_id] = str(file.name)
    
    return found_files

def main():
    print("=" * 60)
    print("[Scan] Integration deployment completion")
    print("=" * 60)
    print()
    
    found = scan_completion_files()
    
    print(f"[Found] {len(found)} task completion indicators:")
    for task_id, filename in sorted(found.items()):
        status = "[OK]" if task_id in TASKS_TO_CHECK else "[INFO]"
        print(f"  {status} {task_id}")
    
    print()
    print("=" * 60)
    print("[Tasks to update]")
    print("=" * 60)
    
    for task_id in TASKS_TO_CHECK:
        if task_id in found:
            print(f"  [UPDATE] {task_id} -> COMPLETED")
        else:
            print(f"  [SKIP] {task_id} (no completion file)")

if __name__ == "__main__":
    main()

