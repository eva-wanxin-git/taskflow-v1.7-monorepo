#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动触发状态检测 - 立即检查所有派发文档对应的任务
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
PROJECT_ROOT = Path(__file__).parent.parent
EVENTS_FILE = PROJECT_ROOT / "apps/dashboard/automation-data/architect_events.json"

def scan_dispatch_docs():
    """扫描所有派发文档"""
    dispatch_docs = list(PROJECT_ROOT.glob("📤派发给*.md"))
    
    print("=" * 70)
    print("手动触发状态检测")
    print("=" * 70)
    print()
    print(f"[扫描] 找到{len(dispatch_docs)}个派发文档")
    print()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updated = 0
    
    for doc in dispatch_docs:
        print(f"[检查] {doc.name}")
        
        # 从文件名提取可能的任务ID
        import re
        
        # 读取文件内容
        try:
            content = doc.read_text(encoding='utf-8')
            
            # 提取任务ID
            patterns = [
                r'任务ID[:\s]*([A-Z]+-[A-Z0-9-]+)',
                r'\*\*任务ID\*\*[:\s]*([A-Z]+-[A-Z0-9-]+)',
                r'(INTEGRATE-\d+)',
                r'(REQ-\d+-?[A-Z]?)',
                r'(TASK-[A-Z]-\d+)'
            ]
            
            task_id = None
            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    task_id = match.group(1) if match.lastindex else match.group(0)
                    break
            
            if not task_id:
                print(f"  [SKIP] 无法提取任务ID")
                continue
            
            # 查询任务状态
            cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            
            if not result:
                print(f"  [ERROR] 任务{task_id}不存在于数据库")
                continue
            
            status = result[0]
            
            if status == "pending":
                # 这个任务有派发文档但状态还是pending
                # 可能执行者正在看文档
                print(f"  [ACTION] {task_id} 当前pending，自动更新为in_progress")
                
                cursor.execute("""
                    UPDATE tasks 
                    SET status = 'in_progress', updated_at = ?
                    WHERE id = ?
                """, (datetime.now().isoformat(), task_id))
                
                updated += 1
                
                # 记录事件
                record_event(task_id, "pending", "in_progress")
            else:
                print(f"  [INFO] {task_id} 当前状态: {status}")
        
        except Exception as e:
            print(f"  [ERROR] 处理失败: {e}")
    
    conn.commit()
    conn.close()
    
    print()
    print("=" * 70)
    print(f"[完成] 已自动更新{updated}个任务")
    print("=" * 70)
    print()
    print("Dashboard: http://localhost:8877")
    
    return updated

def record_event(task_id, old_status, new_status):
    """记录事件"""
    try:
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {"events": []}
    
    event = {
        "id": f"event-{len(data.get('events', [])) + 1:03d}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "manual_trigger",
        "icon": "🔄",
        "content": f"[手动触发] {task_id}: {old_status} → {new_status}"
    }
    
    data.setdefault("events", []).append(event)
    
    with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    scan_dispatch_docs()

