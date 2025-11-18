#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能任务检测器 - 检测实际编码行为
监控代码文件变化，自动推断任务状态
"""

import time
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SmartTaskDetector(FileSystemEventHandler):
    """智能任务检测器"""
    
    def __init__(self, db_path, project_root):
        self.db_path = db_path
        self.project_root = Path(project_root)
        self.events_file = self.project_root / "apps/dashboard/automation-data/architect_events.json"
        self.last_dispatch_task = None  # 记录最近派发的任务
        self.code_changes = {}  # 记录代码变化
        
    def on_created(self, event):
        """文件创建"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # 检测1: 派发文档创建（记录最近派发的任务）
        if file_path.name.startswith("📤"):
            time.sleep(0.5)
            task_id = self.extract_task_id(file_path)
            if task_id:
                self.last_dispatch_task = {
                    "task_id": task_id,
                    "time": datetime.now(),
                    "doc": file_path
                }
                print(f"\n[DETECT] 派发文档创建: {task_id}")
                print(f"[WAIT] 等待检测执行迹象...")
        
        # 检测2: 代码文件创建（说明在开发）
        elif file_path.suffix in ['.py', '.js', '.ts', '.tsx', '.md', '.sql']:
            self.on_code_change(file_path, "创建")
        
        # 检测3: 完成报告创建（任务完成）
        elif file_path.name.startswith("✅") and "完成" in file_path.name:
            time.sleep(1)
            task_id = self.extract_task_id(file_path)
            if task_id:
                print(f"\n[AUTO] 检测到完成报告: {task_id}")
                self.auto_complete_task(task_id)
    
    def on_modified(self, event):
        """文件修改"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # 检测代码文件修改（说明在编码）
        if file_path.suffix in ['.py', '.js', '.ts', '.tsx', '.sql', '.md']:
            # 排除事件文件本身
            if "architect_events.json" not in str(file_path):
                self.on_code_change(file_path, "修改")
    
    def on_code_change(self, file_path, action):
        """代码变化时的处理"""
        now = datetime.now()
        
        # 记录这次变化
        file_key = str(file_path)
        if file_key not in self.code_changes:
            self.code_changes[file_key] = []
        self.code_changes[file_key].append(now)
        
        # 检测：如果5秒内有3次以上代码变化，说明在编码
        recent_changes = [t for t in self.code_changes[file_key] 
                         if (now - t).total_seconds() < 5]
        
        if len(recent_changes) >= 3:
            print(f"\n[DETECT] 检测到编码活动: {file_path.name} ({action})")
            
            # 如果最近有派发任务（10分钟内）
            if self.last_dispatch_task:
                task_info = self.last_dispatch_task
                minutes_ago = (now - task_info["time"]).total_seconds() / 60
                
                if minutes_ago < 10:  # 10分钟内派发的任务
                    task_id = task_info["task_id"]
                    status = self.get_task_status(task_id)
                    
                    if status == "pending":
                        print(f"[AUTO] 推断: {task_id} 正在被执行")
                        print(f"[AUTO] 自动更新为: in_progress")
                        self.auto_start_task(task_id)
                        self.last_dispatch_task = None  # 清除，避免重复
    
    def extract_task_id(self, file_path):
        """提取任务ID"""
        try:
            content = file_path.read_text(encoding='utf-8')
            patterns = [
                r'任务ID[:\s]*([A-Z]+-[A-Z0-9-]+)',
                r'任务[:\s]*([A-Z]+-[A-Z0-9-]+)',
                r'(INTEGRATE-\d+)',
                r'(REQ-\d+-?[A-Z]?)',
                r'(TASK-[A-Z]-\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    return match.group(1) if match.lastindex else match.group(0)
            
        except:
            pass
        
        return None
    
    def get_task_status(self, task_id):
        """获取任务状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except:
            return None
    
    def auto_start_task(self, task_id):
        """自动开始任务"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE tasks 
                SET status = 'in_progress', updated_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), task_id))
            
            conn.commit()
            conn.close()
            
            self.record_event(task_id, "auto_start")
            print(f"[SUCCESS] {task_id} 已自动更新为 in_progress")
            
        except Exception as e:
            print(f"[ERROR] 更新失败: {e}")
    
    def auto_complete_task(self, task_id):
        """自动完成任务"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE tasks 
                SET status = 'completed', updated_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), task_id))
            
            conn.commit()
            conn.close()
            
            self.record_event(task_id, "auto_complete")
            print(f"[SUCCESS] {task_id} 已自动更新为 completed")
            
        except Exception as e:
            print(f"[ERROR] 更新失败: {e}")
    
    def record_event(self, task_id, event_type):
        """记录事件"""
        try:
            with open(self.events_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {"events": []}
        
        content_map = {
            "auto_start": f"[自动检测] 任务{task_id}检测到编码活动，自动标记为进行中",
            "auto_complete": f"[自动检测] 任务{task_id}检测到完成报告，自动标记为已完成"
        }
        
        event = {
            "id": f"event-{len(data.get('events', [])) + 1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "auto_detection",
            "icon": "🤖",
            "content": content_map.get(event_type, f"[自动] {task_id}")
        }
        
        data.setdefault("events", []).append(event)
        
        with open(self.events_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def start_smart_detector():
    """启动智能检测器"""
    project_root = Path(__file__).parent.parent
    db_path = project_root / "database/data/tasks.db"
    
    print("=" * 70)
    print("🤖 智能任务检测器 v2.0")
    print("=" * 70)
    print()
    print("智能检测规则:")
    print("  1. 派发文档创建 → 记录最近派发的任务")
    print("  2. 代码文件频繁修改 → 推断有人在编码")
    print("  3. 自动关联: 最近派发的任务 + 编码活动 = 任务进行中")
    print("  4. 完成报告创建 → 自动标记已完成")
    print()
    print("触发条件:")
    print("  - 5秒内同一文件修改3次 = 编码中")
    print("  - 10分钟内派发的任务 = 相关任务")
    print()
    print("🟢 服务已启动")
    print("=" * 70)
    print()
    
    detector = SmartTaskDetector(db_path, project_root)
    observer = Observer()
    observer.schedule(detector, str(project_root), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🔴 服务已停止")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    start_smart_detector()

