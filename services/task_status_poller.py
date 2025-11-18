#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务状态定时检测服务
每30秒检查一次，智能推断状态变化
"""

import sqlite3
import time
import json
from datetime import datetime, timedelta
from pathlib import Path

class TaskStatusPoller:
    """任务状态轮询器"""
    
    def __init__(self, db_path, project_root):
        self.db_path = db_path
        self.project_root = Path(project_root)
        self.events_file = self.project_root / "apps/dashboard/automation-data/architect_events.json"
    
    def check_and_update(self):
        """检查并自动更新状态"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检测1: pending任务是否有完成报告（说明忘记更新了）
        cursor.execute("""
            SELECT id, title FROM tasks WHERE status = 'pending'
        """)
        
        for task_id, title in cursor.fetchall():
            # 检查是否存在完成报告
            report = self.find_completion_report(task_id)
            if report:
                print(f"[SMART] {task_id} 发现完成报告但状态还是pending，自动更新！")
                self.update_status(cursor, task_id, "completed")
        
        # 检测2: pending任务超过派发时间很久（可能在执行但忘记更新）
        cursor.execute("""
            SELECT id, title, created_at FROM tasks 
            WHERE status = 'pending'
            AND assigned_to IN ('fullstack-engineer', 'architect')
        """)
        
        for task_id, title, created_at in cursor.fetchall():
            created = datetime.fromisoformat(created_at)
            hours_ago = (datetime.now() - created).total_seconds() / 3600
            
            # 如果派发超过1小时还是pending，检查是否有工作迹象
            if hours_ago > 1:
                if self.has_work_signs(task_id):
                    print(f"[SMART] {task_id} 检测到工作迹象，自动标记为进行中")
                    self.update_status(cursor, task_id, "in_progress")
        
        # 检测3: in_progress任务是否有完成报告
        cursor.execute("""
            SELECT id, title FROM tasks WHERE status = 'in_progress'
        """)
        
        for task_id, title in cursor.fetchall():
            report = self.find_completion_report(task_id)
            if report:
                print(f"[SMART] {task_id} 发现完成报告，自动标记为已完成！")
                self.update_status(cursor, task_id, "completed")
        
        conn.commit()
        conn.close()
    
    def find_completion_report(self, task_id):
        """查找完成报告"""
        patterns = [
            f"✅{task_id}*完成报告.md",
            f"✅{task_id}*完成.md",
            f"*{task_id}*完成报告.md"
        ]
        
        for pattern in patterns:
            reports = list(self.project_root.glob(pattern))
            if reports:
                return reports[0]
        
        return None
    
    def has_work_signs(self, task_id):
        """检测是否有工作迹象"""
        # 检查最近1小时内是否有Git提交包含此任务ID
        # 或相关代码文件被修改
        # 简化版本：检查是否有相关文件最近被修改
        
        # 这里可以添加更复杂的检测逻辑
        return False  # 当前保守，避免误判
    
    def update_status(self, cursor, task_id, new_status):
        """更新任务状态"""
        cursor.execute("""
            UPDATE tasks 
            SET status = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, datetime.now().isoformat(), task_id))
        
        # 记录自动更新事件
        self.record_event(task_id, new_status)
    
    def record_event(self, task_id, status):
        """记录事件"""
        try:
            if not self.events_file.exists():
                data = {"events": []}
            else:
                with open(self.events_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            event = {
                "id": f"event-{len(data.get('events', [])) + 1:03d}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "auto_status_change",
                "icon": "🤖",
                "content": f"[自动] 任务{task_id}状态已自动更新为{status}",
                "metadata": {
                    "task_id": task_id,
                    "status": status,
                    "auto": True
                }
            }
            
            data.setdefault("events", []).append(event)
            
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] 记录事件失败: {e}")
    
    def run_polling(self):
        """定时轮询检测"""
        print("\n[POLL] 执行定时检测...")
        self.check_and_update()

def start_service():
    """启动监控服务"""
    project_root = Path(__file__).parent.parent
    db_path = project_root / "database/data/tasks.db"
    
    print("=" * 70)
    print("🤖 任务自动监控服务 v1.0")
    print("=" * 70)
    print()
    print(f"项目路径: {project_root}")
    print(f"数据库: {db_path}")
    print()
    print("🔍 监控范围:")
    print("  - 派发文档（📤派发给*.md）")
    print("  - 完成报告（✅*完成报告.md）")
    print()
    print("⚡ 自动化规则:")
    print("  1. 派发文档创建 → 记录派发事件")
    print("  2. 派发文档打开15秒 → 自动更新为'进行中'")
    print("  3. 完成报告创建 → 自动更新为'已完成'")
    print("  4. 每30秒轮询 → 智能检测异常状态")
    print()
    print("🟢 服务已启动，按Ctrl+C停止")
    print("=" * 70)
    print()
    
    # 创建监控器
    monitor = TaskAutoMonitor(db_path, project_root)
    
    # 文件系统监控
    observer = Observer()
    observer.schedule(monitor, str(project_root), recursive=True)
    observer.start()
    
    print("[INFO] 文件系统监控已启动 ✅")
    print("[INFO] 定时轮询已启动 ✅")
    print()
    
    try:
        # 主循环：每30秒轮询一次
        while True:
            time.sleep(30)
            monitor.run_polling()
            
    except KeyboardInterrupt:
        print("\n\n🔴 收到停止信号")
        observer.stop()
        observer.join()
        print("🔴 监控服务已停止")

if __name__ == "__main__":
    start_service()

