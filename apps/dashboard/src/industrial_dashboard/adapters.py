"""
适配器 - 连接现有项目的数据到 Dashboard

提供开箱即用的适配器，支持快速集成
"""
from typing import List
import json
from pathlib import Path
from .data_provider import DataProvider, TaskData, StatsData


class StateManagerAdapter(DataProvider):
    """
    StateManager 适配器
    
    用于 AI Task Automation Board 项目
    
    用法:
        from automation.state_manager import StateManager
        from industrial_dashboard.adapters import StateManagerAdapter
        from industrial_dashboard import IndustrialDashboard
        
        sm = StateManager()
        provider = StateManagerAdapter(sm)
        dashboard = IndustrialDashboard(provider)
        dashboard.run()
    """
    
    def __init__(self, state_manager):
        """
        初始化适配器
        
        Args:
            state_manager: StateManager 实例
        """
        self.sm = state_manager
        self.completions_file = Path("automation-data/task_completions.json")
        self._load_completions()
    
    def _load_completions(self):
        """加载任务完成详情"""
        if self.completions_file.exists():
            with open(self.completions_file, 'r', encoding='utf-8') as f:
                self.completions = json.load(f)
        else:
            self.completions = {}
    
    def get_stats(self) -> StatsData:
        """获取统计数据"""
        all_tasks = self.sm.list_all_tasks()
        
        return StatsData(
            total_tasks=len(all_tasks),
            pending_tasks=len([
                t for t in all_tasks 
                if str(t.status).lower() == 'pending'
            ]),
            in_progress_tasks=len([
                t for t in all_tasks 
                if str(t.status).lower() == 'in_progress'
            ]),
            completed_tasks=len([
                t for t in all_tasks 
                if str(t.status).lower() == 'completed'
            ]),
            review_tasks=len([
                t for t in all_tasks 
                if str(t.status).lower() == 'review'
            ]),
            failed_tasks=len([
                t for t in all_tasks 
                if str(t.status).lower() == 'failed'
            ])
        )
    
    def get_tasks(self) -> List[TaskData]:
        """获取任务列表"""
        all_tasks = self.sm.list_all_tasks()
        
        result = []
        for task in all_tasks:
            # 提取状态
            status = str(task.status).split('.')[-1].lower() if hasattr(task.status, 'name') else str(task.status).lower()
            
            # 提取优先级
            priority = str(task.priority).split('.')[-1] if hasattr(task.priority, 'name') else str(task.priority)
            
            # 获取完成详情
            completion = self.completions.get(task.id, {})
            
            task_data = TaskData(
                id=task.id,
                title=task.title,
                description=task.description or "",
                status=status,
                priority=priority,
                complexity=task.complexity or "medium",
                estimated_hours=task.estimated_hours or 0.0,
                created_at=task.created_at.isoformat() if task.created_at else None,
                assigned_to=task.assigned_to
            )
            
            # 添加完成详情到描述中（JSON格式）
            if completion:
                task_data.description = json.dumps(completion, ensure_ascii=False)
            
            result.append(task_data)
        
        return result


class GenericDictAdapter(DataProvider):
    """
    通用字典适配器
    
    适用于任何提供字典格式数据的项目
    
    用法:
        def get_tasks_func():
            return [
                {"id": "1", "title": "Task 1", "status": "pending"},
                ...
            ]
        
        def get_stats_func():
            return {
                "total_tasks": 10,
                "pending_tasks": 5,
                ...
            }
        
        provider = GenericDictAdapter(get_tasks_func, get_stats_func)
        dashboard = IndustrialDashboard(provider)
        dashboard.run()
    """
    
    def __init__(self, tasks_getter, stats_getter):
        """
        初始化适配器
        
        Args:
            tasks_getter: 返回任务列表的函数
            stats_getter: 返回统计数据的函数
        """
        self.tasks_getter = tasks_getter
        self.stats_getter = stats_getter
    
    def get_stats(self) -> StatsData:
        """获取统计数据"""
        stats_dict = self.stats_getter()
        return StatsData(
            total_tasks=stats_dict.get('total_tasks', 0),
            pending_tasks=stats_dict.get('pending_tasks', 0),
            in_progress_tasks=stats_dict.get('in_progress_tasks', 0),
            completed_tasks=stats_dict.get('completed_tasks', 0),
            review_tasks=stats_dict.get('review_tasks', 0),
            failed_tasks=stats_dict.get('failed_tasks', 0)
        )
    
    def get_tasks(self) -> List[TaskData]:
        """获取任务列表"""
        tasks_list = self.tasks_getter()
        
        result = []
        for task_dict in tasks_list:
            result.append(TaskData(
                id=task_dict.get('id', ''),
                title=task_dict.get('title', ''),
                description=task_dict.get('description', ''),
                status=task_dict.get('status', 'pending'),
                priority=task_dict.get('priority', 'P1'),
                complexity=task_dict.get('complexity', 'medium'),
                estimated_hours=task_dict.get('estimated_hours', 0.0),
                created_at=task_dict.get('created_at'),
                assigned_to=task_dict.get('assigned_to')
            ))
        
        return result

