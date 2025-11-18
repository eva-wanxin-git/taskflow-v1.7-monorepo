"""
项目经理 AI 模块

负责需求分析、任务拆解、依赖识别、进度监控
"""

import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from anthropic import Anthropic

from .models import Task, TaskStatus, TaskPriority
from .state_manager import StateManager
from .config import config


class ProjectManagerAI:
    """项目经理AI - 负责需求分析和任务拆解
    
    工作流:
    1. 分析用户需求
    2. 拆解为可执行任务
    3. 识别任务依赖
    4. 设置优先级和复杂度
    5. 创建任务到状态管理器
    """
    
    def __init__(self, state_manager: StateManager):
        """初始化PM AI
        
        Args:
            state_manager: 状态管理器实例
        """
        self.state_manager = state_manager
        self.client = Anthropic(api_key=config.get('claude.api_key'))
        self.model = config.get('claude.pm_model')
        self.max_tokens = config.get('claude.max_tokens', 4096)
        
        # 加载提示词
        self.system_prompt = self._load_prompt()
    
    def _load_prompt(self) -> str:
        """加载系统提示词
        
        Returns:
            提示词内容
        """
        try:
            with open('automation-config/pm_prompt.md', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "You are a project manager AI responsible for requirements analysis and task decomposition."
    
    def analyze_requirements(self, user_requirement: str) -> Dict[str, Any]:
        """分析用户需求
        
        Args:
            user_requirement: 用户的需求描述文本
            
        Returns:
            分析结果，包含主要目标、关键功能等
        """
        prompt = f"""
请分析以下用户需求，提取主要目标、关键功能、约束条件和可能的风险。
以JSON格式返回结果。

用户需求:
{user_requirement}

返回格式:
{{
  "main_goals": [...],
  "key_features": [...],
  "constraints": [...],
  "risks": [...]
}}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # 提取 JSON
        try:
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            json_str = result_text[json_start:json_end]
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            return {
                "main_goals": [user_requirement],
                "key_features": [],
                "constraints": [],
                "risks": []
            }
    
    def decompose_into_tasks(self, requirement: str, analysis: Dict) -> List[Task]:
        """将需求拆解为任务
        
        Args:
            requirement: 原始需求
            analysis: 需求分析结果
            
        Returns:
            任务列表
        """
        analysis_str = json.dumps(analysis, ensure_ascii=False, indent=2)
        
        prompt = f"""
基于以下需求和分析结果，拆解为具体的可执行任务。

要求:
- 每个任务 1-3 小时可完成
- 每个任务都有明确的验收标准
- 任务名称清晰简洁
- 包含实现要求

用户需求:
{requirement}

分析结果:
{analysis_str}

返回 JSON 格式的任务列表（不包含"task-"前缀的ID，只有数字如"1.0"）:
{{
  "tasks": [
    {{
      "id": "1.0",
      "title": "任务标题",
      "description": "详细描述",
      "requirements": ["需求1"],
      "acceptance_criteria": ["标准1"],
      "complexity": "low|medium|high",
      "estimated_hours": 2.0,
      "testing_strategy": "测试策略"
    }}
  ]
}}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # 提取任务列表
        tasks = []
        try:
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            json_str = result_text[json_start:json_end]
            data = json.loads(json_str)
            
            for task_data in data.get('tasks', []):
                task = Task(
                    id=f"task-{task_data['id']}",
                    title=task_data['title'],
                    description=task_data['description'],
                    status=TaskStatus.PENDING,
                    priority=TaskPriority.P1,
                    complexity=task_data.get('complexity', 'medium'),
                    estimated_hours=task_data.get('estimated_hours', 2.0),
                )
                tasks.append(task)
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
        
        return tasks
    
    def analyze_dependencies(self, tasks: List[Task]) -> List[Task]:
        """分析任务之间的依赖关系
        
        Args:
            tasks: 任务列表
            
        Returns:
            更新了depends_on的任务列表
        """
        tasks_str = json.dumps([{"id": t.id, "title": t.title} for t in tasks], 
                              ensure_ascii=False, indent=2)
        
        prompt = f"""
分析以下任务之间的依赖关系。
返回一个依赖映射，key为任务ID，value为它依赖的任务ID列表。

任务列表:
{tasks_str}

返回格式:
{{
  "dependencies": {{
    "task-1.0": [],
    "task-2.0": ["task-1.0"],
    "task-3.0": ["task-1.0", "task-2.0"]
  }}
}}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        try:
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            json_str = result_text[json_start:json_end]
            data = json.loads(json_str)
            
            deps = data.get('dependencies', {})
            for task in tasks:
                task.depends_on = deps.get(task.id, [])
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
        
        return tasks
    
    def set_priorities_and_complexity(self, tasks: List[Task]) -> List[Task]:
        """设置优先级和复杂度
        
        Args:
            tasks: 任务列表
            
        Returns:
            更新了优先级的任务列表
        """
        # 简单启发式算法：
        # - 没有依赖的任务 → P0
        # - 有依赖的任务 → P1
        for task in tasks:
            if len(task.depends_on) == 0:
                task.priority = TaskPriority.P0
            elif len(task.depends_on) <= 2:
                task.priority = TaskPriority.P1
            else:
                task.priority = TaskPriority.P2
        
        return tasks
    
    def create_tasks_in_board(self, tasks: List[Task]) -> bool:
        """将任务创建到白板
        
        Args:
            tasks: 任务列表
            
        Returns:
            是否创建成功
        """
        success_count = 0
        for task in tasks:
            if self.state_manager.create_task(task):
                success_count += 1
        
        return success_count == len(tasks)
    
    def execute_workflow(self, user_requirement: str) -> Dict[str, Any]:
        """执行完整的任务拆解工作流
        
        Args:
            user_requirement: 用户需求文本
            
        Returns:
            工作流执行结果
        """
        start_time = time.time()
        
        # 第一步：分析需求
        analysis = self.analyze_requirements(user_requirement)
        
        # 第二步：拆解任务
        tasks = self.decompose_into_tasks(user_requirement, analysis)
        
        if not tasks:
            return {
                "status": "failed",
                "error": "Failed to decompose tasks",
                "analysis": analysis,
            }
        
        # 第三步：分析依赖
        tasks = self.analyze_dependencies(tasks)
        
        # 第四步：设置优先级
        tasks = self.set_priorities_and_complexity(tasks)
        
        # 第五步：创建到白板
        success = self.create_tasks_in_board(tasks)
        
        elapsed = time.time() - start_time
        
        return {
            "status": "success" if success else "failed",
            "analysis": analysis,
            "tasks_created": len(tasks) if success else 0,
            "task_ids": [t.id for t in tasks],
            "dependencies": {t.id: t.depends_on for t in tasks},
            "elapsed_seconds": elapsed,
        }
