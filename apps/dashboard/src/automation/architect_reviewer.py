"""
架构师审查模块

负责：
1. 接收任务执行报告
2. 审查代码
3. 完成部署预览
4. 更新任务面板已完成清单
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .models import Task, TaskStatus, Review
from .state_manager import StateManager
from .task_completion import TaskCompletion


class ArchitectReviewer:
    """架构师审查者
    
    工作流:
    1. 接收任务执行报告
    2. 审查代码和实现
    3. 进行部署预览检查
    4. 更新任务状态为已完成
    5. 更新任务面板已完成清单
    """
    
    def __init__(self, state_manager: StateManager):
        """初始化架构师审查者
        
        Args:
            state_manager: 状态管理器实例
        """
        self.state_manager = state_manager
        self.task_completion = TaskCompletion()
        self.reports_dir = Path("automation-data/task_reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def receive_task_report(self, task_id: str, report_data: Dict[str, Any]) -> bool:
        """接收任务执行报告
        
        Args:
            task_id: 任务ID
            report_data: 报告数据，包含：
                - features_implemented: 实现的功能列表
                - code_lines: 代码行数
                - files_created: 新建文件数
                - files_modified: 修改文件数
                - actual_hours: 实际工时
                - key_achievements: 关键成就
                - tech_stack: 使用的技术栈
                - notes: 备注
                - test_results: 测试结果
                - git_commit: Git提交信息
                
        Returns:
            是否接收成功
        """
        try:
            # 保存报告到文件
            report_file = self.reports_dir / f"{task_id}_report.json"
            report_data['received_at'] = datetime.now().isoformat()
            report_data['task_id'] = task_id
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            # 更新任务完成详情
            self.task_completion.update_completion(
                task_id=task_id,
                features_implemented=report_data.get('features_implemented', []),
                code_lines=report_data.get('code_lines', 0),
                files_created=report_data.get('files_created', 0),
                files_modified=report_data.get('files_modified', 0),
                actual_hours=report_data.get('actual_hours', 0.0),
                key_achievements=report_data.get('key_achievements', []),
                tech_stack=report_data.get('tech_stack', []),
                notes=report_data.get('notes', '')
            )
            
            # 记录架构师事件
            self._log_architect_event(
                f"📬 收到 {task_id} 任务完成报告",
                f"实现功能: {len(report_data.get('features_implemented', []))} 个"
            )
            
            return True
        except Exception as e:
            print(f"[ArchitectReviewer] ✗ 接收报告失败: {str(e)}")
            return False
    
    def review_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """审查任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            审查结果字典，包含：
                - passed: 是否通过
                - score: 评分
                - feedback: 反馈
                - deployment_ready: 是否可部署
        """
        try:
            # 读取任务
            task = self.state_manager.get_task(task_id)
            if not task:
                return None
            
            # 读取执行报告
            report_file = self.reports_dir / f"{task_id}_report.json"
            if not report_file.exists():
                return None
            
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            # 记录审查开始
            self._log_architect_event(
                f"🔍 开始审查 {task_id}",
                f"任务: {task.title}"
            )
            
            # 执行审查（简化版，实际应该调用AI审查）
            review_result = self._perform_review(task, report_data)
            
            # 记录审查结果
            if review_result['passed']:
                self._log_architect_event(
                    f"✅ 审查通过 {task_id}",
                    f"评分: {review_result['score']}/100"
                )
            else:
                self._log_architect_event(
                    f"⚠️ 审查未通过 {task_id}",
                    f"评分: {review_result['score']}/100，需要修订"
                )
            
            return review_result
            
        except Exception as e:
            print(f"[ArchitectReviewer] ✗ 审查失败: {str(e)}")
            return None
    
    def _perform_review(self, task: Task, report_data: Dict) -> Dict[str, Any]:
        """执行审查逻辑
        
        Args:
            task: 任务对象
            report_data: 报告数据
            
        Returns:
            审查结果
        """
        # 简化版审查逻辑
        # 实际应该调用AI进行详细审查
        
        score = 0
        feedback_items = []
        
        # 检查功能完整性（30分）
        features = report_data.get('features_implemented', [])
        if len(features) > 0:
            score += 25
            feedback_items.append("✓ 功能实现完整")
        else:
            feedback_items.append("✗ 缺少功能实现")
        
        # 检查代码量（10分）
        code_lines = report_data.get('code_lines', 0)
        if code_lines > 100:
            score += 10
            feedback_items.append(f"✓ 代码量充足 ({code_lines} 行)")
        elif code_lines > 50:
            score += 5
            feedback_items.append(f"⚠ 代码量一般 ({code_lines} 行)")
        else:
            feedback_items.append(f"✗ 代码量不足 ({code_lines} 行)")
        
        # 检查测试结果（20分）
        test_results = report_data.get('test_results', {})
        if test_results.get('passed', False):
            score += 20
            feedback_items.append("✓ 测试通过")
        else:
            feedback_items.append("✗ 测试未通过")
        
        # 检查Git提交（10分）
        git_commit = report_data.get('git_commit')
        if git_commit:
            score += 10
            feedback_items.append("✓ 代码已提交")
        else:
            feedback_items.append("✗ 代码未提交")
        
        # 检查文档（10分）
        notes = report_data.get('notes', '')
        if len(notes) > 50:
            score += 10
            feedback_items.append("✓ 文档完整")
        else:
            score += 5
            feedback_items.append("⚠ 文档需要补充")
        
        # 技术栈检查（10分）
        tech_stack = report_data.get('tech_stack', [])
        if len(tech_stack) > 0:
            score += 10
            feedback_items.append(f"✓ 技术栈明确: {', '.join(tech_stack)}")
        
        # 关键成就（10分）
        achievements = report_data.get('key_achievements', [])
        if len(achievements) > 0:
            score += 10
            feedback_items.append(f"✓ 关键成就: {len(achievements)} 项")
        
        passed = score >= 80
        deployment_ready = passed and test_results.get('passed', False)
        
        return {
            'passed': passed,
            'score': score,
            'feedback': '\n'.join(feedback_items),
            'deployment_ready': deployment_ready,
            'reviewed_at': datetime.now().isoformat()
        }
    
    def deploy_preview(self, task_id: str) -> Dict[str, Any]:
        """部署预览检查
        
        Args:
            task_id: 任务ID
            
        Returns:
            部署预览结果
        """
        try:
            # 读取任务和报告
            task = self.state_manager.get_task(task_id)
            if not task:
                return {'ready': False, 'message': '任务不存在'}
            
            report_file = self.reports_dir / f"{task_id}_report.json"
            if not report_file.exists():
                return {'ready': False, 'message': '执行报告不存在'}
            
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            # 检查部署条件
            checks = []
            
            # 检查1: 测试通过
            test_results = report_data.get('test_results', {})
            if test_results.get('passed', False):
                checks.append({'name': '测试通过', 'status': '✓', 'ready': True})
            else:
                checks.append({'name': '测试通过', 'status': '✗', 'ready': False})
            
            # 检查2: 代码已提交
            git_commit = report_data.get('git_commit')
            if git_commit:
                checks.append({'name': '代码已提交', 'status': '✓', 'ready': True})
            else:
                checks.append({'name': '代码已提交', 'status': '✗', 'ready': False})
            
            # 检查3: 功能完整
            features = report_data.get('features_implemented', [])
            if len(features) > 0:
                checks.append({'name': '功能完整', 'status': '✓', 'ready': True})
            else:
                checks.append({'name': '功能完整', 'status': '✗', 'ready': False})
            
            # 检查4: 文档完整
            notes = report_data.get('notes', '')
            if len(notes) > 50:
                checks.append({'name': '文档完整', 'status': '✓', 'ready': True})
            else:
                checks.append({'name': '文档完整', 'status': '⚠', 'ready': True})
            
            all_ready = all(check['ready'] for check in checks)
            
            # 记录部署预览事件
            if all_ready:
                self._log_architect_event(
                    f"🚀 部署预览通过 {task_id}",
                    "所有检查项通过，可以部署"
                )
            else:
                self._log_architect_event(
                    f"⚠️ 部署预览未通过 {task_id}",
                    "部分检查项未通过"
                )
            
            return {
                'ready': all_ready,
                'checks': checks,
                'message': '所有检查通过' if all_ready else '部分检查未通过'
            }
            
        except Exception as e:
            print(f"[ArchitectReviewer] ✗ 部署预览失败: {str(e)}")
            return {'ready': False, 'message': str(e)}
    
    def complete_task_review(self, task_id: str) -> bool:
        """完成任务审查并更新状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功
        """
        try:
            # 执行审查
            review_result = self.review_task(task_id)
            if not review_result:
                return False
            
            # 如果审查通过，执行部署预览
            if review_result['passed']:
                deploy_result = self.deploy_preview(task_id)
                
                # 如果部署预览通过，更新任务状态为已完成
                if deploy_result.get('ready', False):
                    success = self.state_manager.update_task_status(
                        task_id, TaskStatus.COMPLETED
                    )
                    
                    if success:
                        # 更新任务完成时间
                        task = self.state_manager.get_task(task_id)
                        if task:
                            task.completed_at = datetime.now()
                            self.state_manager.update_task(task)
                        
                        # 记录完成事件
                        self._log_architect_event(
                            f"✅ 任务完成 {task_id}",
                            f"审查通过 ({review_result['score']}/100)，已更新任务面板"
                        )
                        
                        return True
            
            return False
            
        except Exception as e:
            print(f"[ArchitectReviewer] ✗ 完成审查失败: {str(e)}")
            return False
    
    def _log_architect_event(self, title: str, content: str = ""):
        """记录架构师事件
        
        Args:
            title: 事件标题
            content: 事件内容
        """
        try:
            events_file = Path("automation-data/architect_events.json")
            
            if events_file.exists():
                with open(events_file, 'r', encoding='utf-8') as f:
                    events = json.load(f)
            else:
                events = []
            
            event = {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'title': title,
                'content': content
            }
            
            events.append(event)
            
            # 只保留最近100条事件
            if len(events) > 100:
                events = events[-100:]
            
            with open(events_file, 'w', encoding='utf-8') as f:
                json.dump(events, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"[ArchitectReviewer] ✗ 记录事件失败: {str(e)}")

