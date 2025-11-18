"""
Cursor Worker 模块

负责获取任务、执行开发、运行测试、提交审查
"""

import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

from .models import Task, TaskStatus, ExecutionPlan
from .state_manager import StateManager
from .utils.markdown_parser import parse_task_markdown
from .utils.git_helper import (
    create_git_branch, commit_code, get_current_branch, 
    get_git_status, is_git_repo
)
from .config import config


class CursorWorker:
    """Cursor Worker Agent - 负责任务执行
    
    工作流:
    1. 轮询待执行任务
    2. 认领任务
    3. 生成执行计划
    4. 执行任务代码生成
    5. 运行测试
    6. 提交代码
    7. 提交审查
    """
    
    def __init__(self, worker_id: str, state_manager: StateManager):
        """初始化 Worker
        
        Args:
            worker_id: Worker标识ID (如 cursor-1)
            state_manager: 状态管理器实例
        """
        self.worker_id = worker_id
        self.state_manager = state_manager
        self.poll_interval = config.get('worker.poll_interval', 30)
        self.tasks_completed = 0
        self.tasks_failed = 0
    
    def poll_tasks(self) -> Optional[Task]:
        """轮询获取待执行任务
        
        Returns:
            可执行的任务，如果没有则返回 None
        """
        # 获取所有待分配任务
        pending_tasks = self.state_manager.list_tasks_by_status(TaskStatus.PENDING)
        
        # 遍历任务，检查依赖是否满足
        for task in pending_tasks:
            # 检查依赖任务是否都已完成
            all_deps_done = True
            for dep_id in task.depends_on:
                dep_task = self.state_manager.get_task(dep_id)
                if dep_task is None or dep_task.status != TaskStatus.COMPLETED:
                    all_deps_done = False
                    break
            
            if all_deps_done:
                return task
        
        return None
    
    def claim_task(self, task: Task) -> bool:
        """认领任务
        
        Args:
            task: 待认领的任务
            
        Returns:
            是否认领成功
        """
        # 更新任务状态为 in_progress
        success = self.state_manager.update_task_status(
            task.id, TaskStatus.IN_PROGRESS
        )
        
        if success:
            # 更新任务的分配信息
            task.assigned_to = self.worker_id
            task.assigned_at = datetime.now()
            
            # 创建 Git 分支
            if is_git_repo():
                create_git_branch(task.id)
        
        return success
    
    def generate_execution_plan(self, task: Task) -> ExecutionPlan:
        """生成执行计划
        
        Args:
            task: 任务对象
            
        Returns:
            ExecutionPlan 对象
        """
        # 解析任务 Markdown 文件
        task_file = f"tasks/{task.id}.md"
        
        parsed_task = {}
        if Path(task_file).exists():
            parsed_task = parse_task_markdown(task_file)
        
        # 生成执行计划
        steps = [
            "阅读任务需求",
            "分析验收标准",
            "设计解决方案",
            "编写代码",
            "运行测试",
            "代码审查准备"
        ]
        
        deliverables = [
            task.title,
            "单元测试代码",
            "执行日志"
        ]
        
        plan = ExecutionPlan(
            task_id=task.id,
            worker_id=self.worker_id,
            steps=steps,
            deliverables=deliverables,
            testing_strategy="单元测试 + 集成测试",
            estimated_time=task.estimated_hours * 60,
        )
        
        return plan
    
    def execute_task(self, task: Task, plan: ExecutionPlan) -> bool:
        """执行任务
        
        Args:
            task: 任务对象
            plan: 执行计划
            
        Returns:
            是否执行成功
        """
        try:
            # 记录执行开始
            task.assigned_at = datetime.now()
            
            # 读取任务 Markdown 文件
            task_file = f"tasks/{task.id}.md"
            if not Path(task_file).exists():
                return False
            
            parsed_task = parse_task_markdown(task_file)
            
            # 执行步骤
            for i, step in enumerate(plan.steps, 1):
                # 这里在实际场景中，会根据具体任务调用 Claude API 生成代码
                # 为了演示，我们只记录日志
                pass
            
            return True
        except Exception as e:
            return False
    
    def run_tests(self, task: Task) -> Dict[str, Any]:
        """运行单元测试
        
        Args:
            task: 任务对象
            
        Returns:
            测试结果字典
        """
        try:
            # 运行 pytest
            result = subprocess.run(
                ["pytest", "automation-tests/", "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # 解析结果
            output = result.stdout + result.stderr
            
            # 简单的通过/失败判断
            passed = result.returncode == 0
            
            # 统计
            import re
            passed_match = re.search(r'(\d+) passed', output)
            failed_match = re.search(r'(\d+) failed', output)
            
            passed_count = int(passed_match.group(1)) if passed_match else 0
            failed_count = int(failed_match.group(1)) if failed_match else 0
            
            return {
                "passed": passed,
                "total": passed_count + failed_count,
                "failed_count": failed_count,
                "test_output": output[-1000:],  # 最后1000字符
            }
        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "total": 0,
                "failed_count": 1,
                "test_output": "Test timeout",
            }
        except Exception as e:
            return {
                "passed": False,
                "total": 0,
                "failed_count": 1,
                "test_output": str(e),
            }
    
    def commit_code(self, task: Task, test_results: Dict) -> bool:
        """提交代码
        
        Args:
            task: 任务对象
            test_results: 测试结果
            
        Returns:
            是否提交成功
        """
        try:
            # 创建 execution_plan.md
            plan_file = Path(f"execution-plan-{task.id}.md")
            plan_content = f"""# 执行计划 - {task.id}

## 任务: {task.title}

**Worker**: {self.worker_id}  
**时间**: {datetime.now().isoformat()}

## 执行结果

测试通过: {test_results['passed']}  
总测试数: {test_results['total']}  
失败数: {test_results['failed_count']}

## 输出摘要

{test_results['test_output'][:500]}
"""
            plan_file.write_text(plan_content, encoding='utf-8')
            
            # 提交代码
            commit_message = f"[{task.id}] 完成任务执行 - {self.worker_id}"
            success = commit_code(task.id, commit_message)
            
            return success
        except Exception as e:
            return False
    
    def submit_for_review(self, task: Task, test_results: Dict[str, Any] = None) -> bool:
        """提交审查
        
        Args:
            task: 任务对象
            test_results: 测试结果（可选）
            
        Returns:
            是否提交成功
        """
        try:
            # 生成完整的任务执行报告
            report = self._generate_task_report(task, test_results)
            
            # 发送报告给架构师审查
            from .architect_reviewer import ArchitectReviewer
            architect = ArchitectReviewer(self.state_manager)
            architect.receive_task_report(task.id, report)
            
            # 更新任务状态为 review
            success = self.state_manager.update_task_status(
                task.id, TaskStatus.REVIEW
            )
            
            return success
        except Exception as e:
            print(f"[CursorWorker] ✗ 提交审查失败: {str(e)}")
            return False
    
    def _generate_task_report(self, task: Task, test_results: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成完整的任务执行报告
        
        Args:
            task: 任务对象
            test_results: 测试结果（可选）
            
        Returns:
            执行报告字典
        """
        try:
            # 读取执行计划文件（如果存在）
            plan_file = Path(f"execution-plan-{task.id}.md")
            plan_content = ""
            if plan_file.exists():
                plan_content = plan_file.read_text(encoding='utf-8')
            
            # 获取Git提交信息
            git_commit = None
            try:
                from .utils.git_helper import get_current_branch, get_git_status
                branch = get_current_branch()
                status = get_git_status()
                git_commit = {
                    'branch': branch,
                    'status': status
                }
            except Exception:
                pass
            
            # 统计代码文件
            code_lines = 0
            files_created = 0
            files_modified = 0
            
            # 尝试从执行计划中提取信息
            if plan_content:
                # 提取代码行数
                lines_match = re.search(r'代码行数[：:]\s*(\d+)', plan_content)
                if lines_match:
                    code_lines = int(lines_match.group(1))
                
                # 提取文件数
                files_match = re.search(r'文件数[：:]\s*(\d+)', plan_content)
                if files_match:
                    files_created = int(files_match.group(1))
            
            # 从任务描述中提取实现的功能
            features_implemented = []
            if task.description:
                # 尝试解析JSON格式的完成详情
                try:
                    completion_data = json.loads(task.description)
                    if isinstance(completion_data, dict):
                        features_implemented = completion_data.get('features_implemented', [])
                except:
                    # 如果不是JSON，尝试从文本中提取
                    if '功能' in task.description or '实现' in task.description:
                        # 简单提取，实际应该更智能
                        features_implemented = [task.title]
            
            # 如果没有提取到功能，使用任务标题
            if not features_implemented:
                features_implemented = [task.title]
            
            # 计算实际工时（估算）
            actual_hours = task.estimated_hours or 0.0
            
            # 生成报告
            report = {
                'task_id': task.id,
                'task_title': task.title,
                'worker_id': self.worker_id,
                'completed_at': datetime.now().isoformat(),
                'features_implemented': features_implemented,
                'code_lines': code_lines,
                'files_created': files_created,
                'files_modified': files_modified,
                'actual_hours': actual_hours,
                'key_achievements': [
                    f"完成 {task.title}",
                    f"代码行数: {code_lines}",
                    f"实现功能: {len(features_implemented)} 个"
                ],
                'tech_stack': [],  # 可以从任务描述中提取
                'notes': plan_content[:500] if plan_content else f"任务 {task.id} 执行完成",
                'test_results': test_results or {
                    'passed': True,
                    'total': 0,
                    'failed_count': 0
                },
                'git_commit': git_commit,
                'execution_plan': plan_content
            }
            
            return report
            
        except Exception as e:
            print(f"[CursorWorker] ✗ 生成报告失败: {str(e)}")
            # 返回最小报告
            return {
                'task_id': task.id,
                'task_title': task.title,
                'worker_id': self.worker_id,
                'completed_at': datetime.now().isoformat(),
                'features_implemented': [task.title],
                'code_lines': 0,
                'files_created': 0,
                'files_modified': 0,
                'actual_hours': 0.0,
                'key_achievements': [],
                'tech_stack': [],
                'notes': f"任务 {task.id} 执行完成",
                'test_results': {'passed': False, 'total': 0, 'failed_count': 0},
                'git_commit': None,
                'execution_plan': ''
            }
    
    def handle_revision_needed(self, task: Task, feedback: str) -> bool:
        """处理需要修订的任务
        
        Args:
            task: 任务对象
            feedback: 审查反馈
            
        Returns:
            是否处理成功
        """
        try:
            # 检查修订次数是否超过限制
            if task.revision_count >= task.max_revision_attempts:
                # 标记为失败
                return self.state_manager.update_task_status(
                    task.id, TaskStatus.FAILED
                )
            
            # 增加修订次数
            task.revision_count += 1
            
            # 返回 in_progress 状态继续修改
            return self.state_manager.update_task_status(
                task.id, TaskStatus.IN_PROGRESS
            )
        except Exception as e:
            return False
    
    def mark_task_completed(self, task: Task) -> bool:
        """标记任务完成
        
        Args:
            task: 任务对象
            
        Returns:
            是否标记成功
        """
        try:
            task.completed_at = datetime.now()
            self.tasks_completed += 1
            return self.state_manager.update_task_status(
                task.id, TaskStatus.COMPLETED
            )
        except Exception as e:
            return False
    
    def work_cycle(self) -> Optional[Task]:
        """执行一个工作周期
        
        Returns:
            成功执行的任务，如果没有可执行的任务返回 None
        """
        # 轮询获取任务
        task = self.poll_tasks()
        
        if task is None:
            return None
        
        # 认领任务
        if not self.claim_task(task):
            return None
        
        # 生成执行计划
        plan = self.generate_execution_plan(task)
        
        # 执行任务
        if not self.execute_task(task, plan):
            self.tasks_failed += 1
            self.state_manager.update_task_status(task.id, TaskStatus.FAILED)
            return None
        
        # 运行测试
        test_results = self.run_tests(task)
        
        if not test_results["passed"]:
            # 测试失败，标记为失败
            self.tasks_failed += 1
            self.state_manager.update_task_status(task.id, TaskStatus.FAILED)
            return None
        
        # 提交代码
        if not self.commit_code(task, test_results):
            self.tasks_failed += 1
            self.state_manager.update_task_status(task.id, TaskStatus.FAILED)
            return None
        
        # 提交审查（包含测试结果）
        if not self.submit_for_review(task, test_results):
            self.tasks_failed += 1
            self.state_manager.update_task_status(task.id, TaskStatus.FAILED)
            return None
        
        return task
    
    def get_stats(self) -> Dict[str, int]:
        """获取 Worker 统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "worker_id": self.worker_id,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "total_tasks": self.tasks_completed + self.tasks_failed,
        }
