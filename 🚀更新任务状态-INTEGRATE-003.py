#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速更新任务状态工具
用于同步INTEGRATE-003的执行状态到Dashboard

功能：
1. 标记任务为"进行中"(IN_PROGRESS)
2. 更新任务完成度百分比
3. 记录执行者信息
4. 添加状态变更事件到事件流
5. 自动刷新Dashboard显示
"""

import json
from pathlib import Path
from datetime import datetime
import sqlite3

def update_task_in_db():
    """在数据库中更新任务状态"""
    db_path = Path("database/data/tasks.db")
    
    if not db_path.exists():
        print(f"❌ 数据库不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 更新INTEGRATE-003任务
        task_id = "INTEGRATE-003"
        status = "IN_PROGRESS"
        progress = 50
        executed_by = "fullstack-engineer"
        updated_at = datetime.now().isoformat()
        
        query = """
        UPDATE tasks 
        SET status = ?, progress = ?, assigned_to = ?, updated_at = ?
        WHERE id = ?
        """
        
        cursor.execute(query, (status, progress, executed_by, updated_at, task_id))
        conn.commit()
        
        affected = cursor.rowcount
        print(f"✅ 数据库更新成功: {affected}条记录")
        
        # 验证更新
        cursor.execute("SELECT id, status, progress FROM tasks WHERE id = ?", (task_id,))
        result = cursor.fetchone()
        if result:
            print(f"✓ 任务ID: {result[0]}")
            print(f"✓ 状态: {result[1]}")
            print(f"✓ 进度: {result[2]}%")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 数据库操作失败: {e}")
        return False

def update_progress_json():
    """更新progress.json进度文件"""
    progress_file = Path("apps/dashboard/automation-data/progress.json")
    
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 更新统计信息
        data["stats"]["in_progress"] = 1
        data["stats"]["pending"] = 4
        data["overall_progress"] = 60 + 5  # 增加5%
        data["updated_at"] = datetime.now().isoformat()
        
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Progress文件已更新: {progress_file}")
        return True
    except Exception as e:
        print(f"❌ Progress文件更新失败: {e}")
        return False

def add_event():
    """添加事件到事件流"""
    events_file = Path("apps/dashboard/automation-data/architect_events.json")
    
    try:
        # 读取现有事件
        if events_file.exists():
            with open(events_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"events": []}
        
        # 创建新事件
        new_event = {
            "id": f"event-{len(data.get('events', [])) + 1}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "task_status_change",
            "content": "✅ INTEGRATE-003任务开始执行 - Token同步与对话历史库集成",
            "metadata": {
                "task_id": "INTEGRATE-003",
                "status": "IN_PROGRESS",
                "assignee": "fullstack-engineer",
                "component": "Dashboard"
            }
        }
        
        data["events"].insert(0, new_event)
        
        # 只保留最近100个事件
        if len(data["events"]) > 100:
            data["events"] = data["events"][:100]
        
        # 保存
        events_file.parent.mkdir(parents=True, exist_ok=True)
        with open(events_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 事件已记录: {new_event['content']}")
        return True
    except Exception as e:
        print(f"❌ 事件记录失败: {e}")
        return False

def generate_summary():
    """生成更新摘要"""
    print("\n" + "="*70)
    print("【任务状态更新摘要】")
    print("="*70)
    print("\n📋 更新内容:")
    print("  ✓ 任务ID: INTEGRATE-003")
    print("  ✓ 任务标题: 集成REQ-006 Token实时同步功能")
    print("  ✓ 新状态: ▶️ 进行中 (IN_PROGRESS)")
    print("  ✓ 执行者: fullstack-engineer (李明)")
    print("  ✓ 预估工时: 2小时")
    print("  ✓ 优先级: P0")
    print("\n📊 进度更新:")
    print("  ✓ 任务进度: 50%")
    print("  ✓ 项目总体进度: 65% (原60%)")
    print("  ✓ 进行中任务: 1个")
    print("  ✓ 待处理任务: 4个")
    print("\n📌 Dashboard显示:")
    print("  ✓ 事件流已更新")
    print("  ✓ 任务看板已更新")
    print("  ✓ 进度统计已更新")
    print("\n💡 后续操作:")
    print("  1. 访问 http://localhost:8877 查看Dashboard")
    print("  2. 检查事件流显示新事件")
    print("  3. 查看任务看板显示INTEGRATE-003为\"进行中\"")
    print("  4. 任务完成后运行 \"🏁完成任务-INTEGRATE-003.py\"")
    print("\n" + "="*70)

def main():
    print("\n" + "🔄 任务状态更新工具 - INTEGRATE-003".center(70, "="))
    print("="*70)
    
    print("\n[1/3] 更新数据库...")
    db_ok = update_task_in_db()
    
    print("\n[2/3] 更新进度文件...")
    progress_ok = update_progress_json()
    
    print("\n[3/3] 记录事件...")
    event_ok = add_event()
    
    if db_ok and progress_ok and event_ok:
        print("\n" + "✅ 所有更新完成！".center(70, "="))
        generate_summary()
        return True
    else:
        print("\n" + "⚠️ 部分更新失败，请查看上面的错误信息".center(70, "="))
        return False

if __name__ == "__main__":
    main()

