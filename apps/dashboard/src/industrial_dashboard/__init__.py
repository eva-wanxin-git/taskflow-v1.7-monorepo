"""
Industrial Dashboard - 工业美学监控面板

一个符合工业美学规范的任务监控 Dashboard，可集成到任何 AI 自动化项目中。

特性:
- 高对比度工业级配色
- 实时数据更新
- 响应式设计
- RESTful API
- 易于集成

用法:
    from industrial_dashboard import IndustrialDashboard
    
    dashboard = IndustrialDashboard(
        data_provider=your_data_provider,
        port=8888
    )
    dashboard.run()
"""

__version__ = "1.0.0"
__author__ = "AI Task Automation Team"
__license__ = "MIT"

from .dashboard import IndustrialDashboard
from .data_provider import DataProvider, TaskData, StatsData

__all__ = [
    'IndustrialDashboard',
    'DataProvider',
    'TaskData',
    'StatsData',
]

