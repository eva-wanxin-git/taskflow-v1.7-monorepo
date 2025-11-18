"""
并行任务调度器

支持多Worker并行执行、智能任务分配、负载均衡、Worker健康检查
"""

import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from .models import Task, TaskStatus, Worker
from .state_manager import StateManager
from .dependency_analyzer import DependencyAnalyzer


class TaskScheduler:
    """并行任务调度器
    
    职责:
    - 管理多个Worker
    - 智能分配任务
    - 负载均衡
    - 健康检查
    """
    
    def __init__(self, state_manager: StateManager):
        """初始化调度器
        
        Args:
            state_manager: 状态管理器实例
        """
        self.state_manager = state_manager
        self.analyzer = DependencyAnalyzer()
        self.workers = {}
        self.worker_health = {}
    
    def register_worker(self, worker_id: str) -> bool:
        """注册Worker
        
        Args:
            worker_id: Worker标识ID
            
        Returns:
            是否注册成功
        """
        if worker_id not in self.workers:
            self.workers[worker_id] = {
                'id': worker_id,
                'status': 'idle',
                'current_task': None,
                'completed_tasks': 0,
                'failed_tasks': 0,
            }
            self.worker_health[worker_id] = {
                'last_heartbeat': datetime.now(),
                'is_alive': True,
            }
            return self.state_manager.register_worker(worker_id)
        return False
    
    def unregister_worker(self, worker_id: str) -> bool:
        """注销Worker
        
        Args:
            worker_id: Worker标识ID
            
        Returns:
            是否注销成功
        """
        if worker_id in self.workers:
            # 如果有任务在执行，标记为待分配
            if self.workers[worker_id]['current_task']:
                task_id = self.workers[worker_id]['current_task']
                self.state_manager.update_task_status(task_id, TaskStatus.PENDING)
            
            del self.workers[worker_id]
            del self.worker_health[worker_id]
            return True
        return False
    
    def get_worker_load(self, worker_id: str) -> int:
        """获取Worker的负载（当前执行的任务数）
        
        Args:
            worker_id: Worker标识ID
            
        Returns:
            负载值
        """
        if worker_id in self.workers:
            return 1 if self.workers[worker_id]['current_task'] else 0
        return 0
    
    def find_best_worker(self) -> Optional[str]:
        """找出负载最低的可用Worker
        
        Args:
            
        Returns:
            Worker ID，如果没有可用Worker返回None
        """
        best_worker = None
        min_load = float('inf')
        
        for worker_id in self.workers:
            if self.is_worker_healthy(worker_id):
                load = self.get_worker_load(worker_id)
                if load < min_load:
                    min_load = load
                    best_worker = worker_id
        
        return best_worker
    
    def assign_task(self, task: Task, worker_id: str) -> bool:
        """为Worker分配任务
        
        Args:
            task: 任务对象
            worker_id: Worker标识ID
            
        Returns:
            是否分配成功
        """
        if worker_id not in self.workers:
            return False
        
        # 更新任务状态
        task.assigned_to = worker_id
        task.assigned_at = datetime.now()
        
        success = self.state_manager.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        
        if success:
            self.workers[worker_id]['current_task'] = task.id
            return True
        
        return False
    
    def complete_task(self, task_id: str, worker_id: str, success: bool) -> bool:
        """标记任务完成
        
        Args:
            task_id: 任务ID
            worker_id: Worker ID
            success: 是否成功
            
        Returns:
            是否更新成功
        """
        if worker_id not in self.workers:
            return False
        
        # 更新Worker状态
        self.workers[worker_id]['current_task'] = None
        
        if success:
            self.workers[worker_id]['completed_tasks'] += 1
            return self.state_manager.update_task_status(task_id, TaskStatus.REVIEW)
        else:
            self.workers[worker_id]['failed_tasks'] += 1
            return self.state_manager.update_task_status(task_id, TaskStatus.FAILED)
    
    def heartbeat(self, worker_id: str) -> bool:
        """接收Worker的心跳信号
        
        Args:
            worker_id: Worker标识ID
            
        Returns:
            是否成功
        """
        if worker_id not in self.worker_health:
            return False
        
        self.worker_health[worker_id]['last_heartbeat'] = datetime.now()
        self.worker_health[worker_id]['is_alive'] = True
        return True
    
    def is_worker_healthy(self, worker_id: str, timeout: int = 300) -> bool:
        """检查Worker是否健康
        
        Args:
            worker_id: Worker标识ID
            timeout: 超时时间（秒）
            
        Returns:
            是否健康
        """
        if worker_id not in self.worker_health:
            return False
        
        health = self.worker_health[worker_id]
        elapsed = (datetime.now() - health['last_heartbeat']).total_seconds()
        
        return elapsed < timeout
    
    def check_worker_health(self) -> Dict[str, bool]:
        """检查所有Worker的健康状态
        
        Returns:
            Worker健康状态字典
        """
        health_status = {}
        
        for worker_id in self.workers:
            is_healthy = self.is_worker_healthy(worker_id)
            health_status[worker_id] = is_healthy
            
            if not is_healthy and self.workers[worker_id]['current_task']:
                # Worker不健康且有任务在执行，释放任务
                task_id = self.workers[worker_id]['current_task']
                self.state_manager.update_task_status(task_id, TaskStatus.PENDING)
                self.workers[worker_id]['current_task'] = None
        
        return health_status
    
    def schedule_tasks(self) -> Dict[str, List[str]]:
        """执行一轮任务调度
        
        Returns:
            调度结果 {worker_id: [task_ids]}
        """
        # 检查Worker健康状态
        self.check_worker_health()
        
        # 获取所有任务
        all_tasks = self.state_manager.list_all_tasks()
        
        # 获取已完成的任务ID集合
        completed_ids = set(
            t.id for t in all_tasks if t.status == TaskStatus.COMPLETED
        )
        
        # 获取可执行的任务
        executable_tasks = self.analyzer.get_executable_tasks(all_tasks, completed_ids)
        
        # 过滤未分配的任务
        unassigned_tasks = [
            t for t in all_tasks
            if t.id in executable_tasks and t.status == TaskStatus.PENDING
        ]
        
        # 按优先级排序
        unassigned_tasks.sort(
            key=lambda t: (
                0 if (t.priority.value if hasattr(t.priority, 'value') else t.priority) == 'P0' else
                1 if (t.priority.value if hasattr(t.priority, 'value') else t.priority) == 'P1' else
                2,
                -t.estimated_hours  # 优先分配工时长的任务
            )
        )
        
        # 调度任务
        assignments = {}
        
        for task in unassigned_tasks:
            worker_id = self.find_best_worker()
            
            if worker_id is None:
                break  # 没有可用Worker
            
            if self.assign_task(task, worker_id):
                if worker_id not in assignments:
                    assignments[worker_id] = []
                assignments[worker_id].append(task.id)
        
        return assignments
    
    def get_system_stats(self) -> Dict:
        """获取系统统计信息
        
        Returns:
            系统统计字典
        """
        all_tasks = self.state_manager.list_all_tasks()
        
        stats = {
            'total_workers': len(self.workers),
            'healthy_workers': sum(1 for w in self.workers if self.is_worker_healthy(w)),
            'idle_workers': sum(1 for w in self.workers if not self.workers[w]['current_task']),
            'total_tasks': len(all_tasks),
            'pending_tasks': len([t for t in all_tasks if t.status == TaskStatus.PENDING]),
            'in_progress_tasks': len([t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS]),
            'completed_tasks': len([t for t in all_tasks if t.status == TaskStatus.COMPLETED]),
            'failed_tasks': len([t for t in all_tasks if t.status == TaskStatus.FAILED]),
            'worker_stats': {}
        }
        
        for worker_id, worker in self.workers.items():
            stats['worker_stats'][worker_id] = {
                'status': worker['status'],
                'current_task': worker['current_task'],
                'completed_tasks': worker['completed_tasks'],
                'failed_tasks': worker['failed_tasks'],
                'is_healthy': self.is_worker_healthy(worker_id),
            }
        
        return stats
    
    def start_scheduling_loop(self, interval: int = 10) -> None:
        """启动调度循环
        
        Args:
            interval: 调度间隔（秒）
        """
        print(f"[Scheduler] 🚀 启动任务调度循环 (间隔 {interval}秒)...")
        
        try:
            while True:
                # 执行一轮调度
                assignments = self.schedule_tasks()
                
                if assignments:
                    print(f"[Scheduler] 📍 本轮分配:")
                    for worker_id, task_ids in assignments.items():
                        print(f"  - {worker_id}: {', '.join(task_ids)}")
                
                # 打印系统状态
                stats = self.get_system_stats()
                print(f"[Scheduler] 📊 系统状态: {stats['completed_tasks']}/{stats['total_tasks']} 任务完成")
                
                # 等待下一轮
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print(f"[Scheduler] ⏹️  停止调度循环")
