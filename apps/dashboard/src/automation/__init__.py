"""
AI 任务协作白板 - 自动化层
"""

__version__ = "0.1.0"

from .config import config
from .models import TaskStatus, Task, Review

__all__ = ['config', 'TaskStatus', 'Task', 'Review']
