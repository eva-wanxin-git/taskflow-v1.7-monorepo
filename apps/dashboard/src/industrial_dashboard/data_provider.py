"""
数据提供器接口

定义了 Dashboard 需要的数据接口，项目只需实现这个接口即可集成
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class TaskData:
    """任务数据结构"""
    id: str
    title: str
    description: str = ""
    status: str = "pending"  # pending, in_progress, review, completed, failed
    priority: str = "P1"
    complexity: str = "medium"
    estimated_hours: float = 0.0
    created_at: str = None
    assigned_to: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "complexity": self.complexity,
            "estimated_hours": self.estimated_hours,
            "created_at": self.created_at or datetime.now().isoformat(),
            "assigned_to": self.assigned_to
        }


@dataclass
class StatsData:
    """统计数据结构"""
    total_tasks: int = 0
    pending_tasks: int = 0
    in_progress_tasks: int = 0
    completed_tasks: int = 0
    review_tasks: int = 0
    failed_tasks: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "total_tasks": self.total_tasks,
            "pending_tasks": self.pending_tasks,
            "in_progress_tasks": self.in_progress_tasks,
            "completed_tasks": self.completed_tasks,
            "review_tasks": self.review_tasks,
            "failed_tasks": self.failed_tasks,
            "last_updated": datetime.now().isoformat()
        }


class DataProvider(ABC):
    """
    数据提供器抽象类
    
    项目需要实现这个类来提供数据给 Dashboard
    
    示例:
        class MyDataProvider(DataProvider):
            def __init__(self, state_manager):
                self.sm = state_manager
            
            def get_stats(self) -> StatsData:
                tasks = self.sm.list_all_tasks()
                return StatsData(
                    total_tasks=len(tasks),
                    pending_tasks=len([t for t in tasks if t.status == 'pending']),
                    # ...
                )
            
            def get_tasks(self) -> List[TaskData]:
                tasks = self.sm.list_all_tasks()
                return [TaskData(
                    id=t.id,
                    title=t.title,
                    status=str(t.status),
                    # ...
                ) for t in tasks]
    """
    
    @abstractmethod
    def get_stats(self) -> StatsData:
        """
        获取统计数据
        
        Returns:
            StatsData: 统计数据对象
        """
        pass
    
    @abstractmethod
    def get_tasks(self) -> List[TaskData]:
        """
        获取任务列表
        
        Returns:
            List[TaskData]: 任务数据列表
        """
        pass

