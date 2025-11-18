#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务自动监控服务 - 实现全自动化
监控文件系统变化，自动更新任务状态
"""

import time
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TaskAutoMonitor(FileSystemEventHandler):
    """任务自动监控器"""
    
    def __init__(self, db_path, project_root):
        self.db_path = db_path
        self.project_root = Path(project_root)
        self.events_file = self.project_root / "apps/dashboard/automation-data/architect_events.json"
        self.processed_files = set()  # 避免重复处理
        
    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # 避免重复处理
        if str(file_path) in self.processed_files:
            return
        
        # 检测1: 派发文档被创建
        if file_path.name.startswith("📤派发给"):
            self.processed_files.add(str(file_path))
            time.sleep(0.5)  # 等待文件写完
            task_id = self.extract_task_id_from_file(file_path)
            if task_id:
                print(f"\n[AUTO] 检测到派发文档创建: {file_path.name}")
                print(f"[AUTO] 提取任务ID: {task_id}")
                # 注意：这里不自动更新为in_progress，等执行者打开文档
                self.record_dispatch_event(task_id)
        
        # 检测2: 完成报告被创建
        elif file_path.name.startswith("✅") and "完成报告" in file_path.name:
            self.processed_files.add(str(file_path))
            time.sleep(1)  # 等待文件写完
            task_id = self.extract_task_id_from_file(file_path)
            if task_id:
                print(f"\n[AUTO] 检测到完成报告创建: {file_path.name}")
                print(f"[AUTO] 提取任务ID: {task_id}")
                print(f"[AUTO] 🎉 自动更新状态为: completed")
                self.update_status(task_id, "completed", auto=True)
    
    def on_modified(self, event):
        """文件修改事件"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # 检测3: 派发文档被打开/修改（可能在阅读）
        if file_path.name.startswith("📤派发给") and str(file_path) not in self.processed_files:
            self.processed_files.add(str(file_path))
            task_id = self.extract_task_id_from_file(file_path)
            if task_id:
                status = self.get_task_status(task_id)
                if status == "pending":
                    print(f"\n[AUTO] 检测到派发文档被打开: {file_path.name}")
                    print(f"[AUTO] 任务ID: {task_id}")
                    print(f"[AUTO] 等待15秒确认执行者在阅读...")
                    time.sleep(15)
                    # 15秒后自动更新为in_progress
                    print(f"[AUTO] ✅ 自动更新状态为: in_progress")
                    self.update_status(task_id, "in_progress", auto=True)
    
    def extract_task_id_from_file(self, file_path):
        """从文件内容提取任务ID"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 匹配各种任务ID格式
            patterns = [
                r'任务ID[:\s]*([A-Z]+-[A-Z0-9-]+)',
                r'\*\*任务ID\*\*[:\s]*([A-Z]+-[A-Z0-9-]+)',
                r'(INTEGRATE-\d+)',
                r'(REQ-\d+-?[A-Z]?)',
                r'(TASK-[A-Z]-\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    task_id = match.group(1) if match.lastindex else match.group(0)
                    return task_id
            
            return None
        except Exception as e:
            print(f"[ERROR] 读取文件失败: {e}")
            return None
    
    def get_task_status(self, task_id):
        """获取任务当前状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except Exception as e:
            print(f"[ERROR] 查询状态失败: {e}")
            return None
    
    def update_status(self, task_id, new_status, auto=True):
        """更新任务状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取旧状态
            cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            old_status = result[0] if result else None
            
            if old_status == new_status:
                conn.close()
                return  # 状态相同，不更新
            
            # 更新状态
            cursor.execute("""
                UPDATE tasks 
                SET status = ?, updated_at = ?
                WHERE id = ?
            """, (new_status, datetime.now().isoformat(), task_id))
            
            conn.commit()
            conn.close()
            
            print(f"[AUTO] ✅ {task_id}: {old_status} → {new_status}")
            
            # 记录事件
            if auto:
                self.record_auto_event(task_id, old_status, new_status)
            
        except Exception as e:
            print(f"[ERROR] 更新状态失败: {e}")
    
    def record_dispatch_event(self, task_id):
        """记录派发事件"""
        self.add_event(
            event_type="task_dispatch",
            icon="📤",
            content=f"[自动检测] 任务{task_id}派发文档已创建"
        )
    
    def record_auto_event(self, task_id, old_status, new_status):
        """记录自动更新事件"""
        self.add_event(
            event_type="auto_status_change",
            icon="🤖",
            content=f"[自动更新] 任务{task_id}状态: {old_status} → {new_status}",
            metadata={
                "task_id": task_id,
                "old_status": old_status,
                "new_status": new_status,
                "auto": True
            }
        )
    
    def add_event(self, event_type, icon, content, metadata=None):
        """添加事件到事件流"""
        try:
            if not self.events_file.exists():
                data = {"events": []}
            else:
                with open(self.events_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            event = {
                "id": f"event-{len(data.get('events', [])) + 1:03d}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": event_type,
                "icon": icon,
                "content": content
            }
            
            if metadata:
                event["metadata"] = metadata
            
            data.setdefault("events", []).append(event)
            
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"[ERROR] 记录事件失败: {e}")

def start_monitor():
    """启动监控服务"""
    project_root = Path(__file__).parent.parent
    db_path = project_root / "database/data/tasks.db"
    
    print("=" * 70)
    print("🤖 任务自动监控服务")
    print("=" * 70)
    print()
    print(f"项目: {project_root}")
    print(f"数据库: {db_path}")
    print()
    print("监控规则:")
    print("  1. 派发文档创建 → 记录派发事件")
    print("  2. 派发文档打开15秒 → 自动标记'进行中'")
    print("  3. 完成报告创建 → 自动标记'已完成'")
    print()
    print("🟢 服务已启动，按Ctrl+C停止")
    print("=" * 70)
    print()
    
    event_handler = TaskAutoMonitor(db_path, project_root)
    observer = Observer()
    observer.schedule(event_handler, str(project_root), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🔴 监控服务已停止")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    start_monitor()

