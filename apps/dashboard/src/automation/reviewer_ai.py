"""
审查者 AI 模块

负责代码审查、评分反馈、决定通过/修订
"""

import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from anthropic import Anthropic

from .models import Task, TaskStatus, Review, ReviewScore
from .state_manager import StateManager
from .config import config


class ReviewerAI:
    """审查者AI - 负责代码审查和评分
    
    工作流:
    1. 监听待审查任务（review状态）
    2. 读取任务代码和要求
    3. 调用Claude进行审查
    4. 解析审查结果
    5. 保存审查记录
    6. 更新任务状态
    7. 如需修订，自动创建修订任务
    """
    
    def __init__(self, state_manager: StateManager):
        """初始化审查者AI
        
        Args:
            state_manager: 状态管理器实例
        """
        self.state_manager = state_manager
        self.client = Anthropic(api_key=config.get('claude.api_key'))
        self.model = config.get('claude.reviewer_model', config.get('claude.pm_model'))
        self.max_tokens = config.get('claude.max_tokens', 4096)
        self.pass_score = config.get('review.pass_score', 80)
        
        # 加载提示词
        self.system_prompt = self._load_prompt()
    
    def _load_prompt(self) -> str:
        """加载系统提示词
        
        Returns:
            提示词内容
        """
        try:
            with open('automation-config/reviewer_prompt.md', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "You are a code reviewer AI responsible for code review and scoring."
    
    def review_task(self, task: Task) -> Optional[Review]:
        """审查任务
        
        Args:
            task: 待审查的任务
            
        Returns:
            审查记录，如果审查失败返回None
        """
        try:
            # 获取任务信息
            task_info = f"""
任务ID: {task.id}
任务标题: {task.title}
任务描述: {task.description}
预估工时: {task.estimated_hours}小时
复杂度: {task.complexity}
            """
            
            # 构建审查提示
            review_prompt = f"""
请对以下任务进行代码审查，并按照审查标准进行评分。

{task_info}

要求：
1. 根据功能完整性、代码质量、规范遵守、文档完整、测试覆盖五个维度评分
2. 总分100分，计算各维度分数和和
3. 80分及以上为通过，低于80分为需修订
4. 返回有效的JSON格式

评分标准：
- 功能完整性 (30分)
- 代码质量 (25分)
- 规范遵守 (20分)
- 文档完整 (15分)
- 测试覆盖 (10分)

返回JSON格式:
{{
  "functionality_score": <数字>,
  "code_quality_score": <数字>,
  "standards_score": <数字>,
  "documentation_score": <数字>,
  "testing_score": <数字>,
  "total_score": <数字>,
  "passed": <true/false>,
  "feedback": "<反馈意见>",
  "revision_instructions": "<修订指令或null>"
}}
"""
            
            # 调用Claude进行审查
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=[{"role": "user", "content": review_prompt}]
            )
            
            result_text = response.content[0].text
            
            # 解析审查结果
            review_result = self._parse_review_result(result_text, task)
            
            if review_result:
                # 保存审查记录
                success = self.state_manager.create_review(review_result)
                
                if success:
                    # 更新任务状态
                    if review_result.score.passed:
                        self.state_manager.update_task_status(task.id, TaskStatus.COMPLETED)
                    else:
                        self.state_manager.update_task_status(task.id, TaskStatus.REVISION)
                        # 创建修订任务
                        self._create_revision_task(task, review_result)
                    
                    return review_result
            
            return None
        
        except Exception as e:
            print(f"[ReviewerAI] ✗ 审查失败: {str(e)}")
            return None
    
    def _parse_review_result(self, result_text: str, task: Task) -> Optional[Review]:
        """解析审查结果
        
        Args:
            result_text: Claude返回的文本
            task: 被审查的任务
            
        Returns:
            审查记录对象
        """
        try:
            # 提取JSON
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            json_str = result_text[json_start:json_end]
            data = json.loads(json_str)
            
            # 创建评分对象
            score = ReviewScore(
                functionality=data.get('functionality_score', 0),
                code_quality=data.get('code_quality_score', 0),
                standards=data.get('standards_score', 0),
                documentation=data.get('documentation_score', 0),
                testing=data.get('testing_score', 0),
            )
            
            # 创建审查记录
            review_id = f"review-{task.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            decision = "approved" if score.passed else "revision_required"
            
            review = Review(
                id=review_id,
                task_id=task.id,
                reviewer_id="reviewer-ai",
                score=score,
                feedback=data.get('feedback', ''),
                decision=decision,
                created_at=datetime.now()
            )
            
            return review
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            return None
    
    def _create_revision_task(self, task: Task, review: Review) -> bool:
        """创建修订任务
        
        Args:
            task: 原任务
            review: 审查结果
            
        Returns:
            是否创建成功
        """
        try:
            # 生成修订任务ID
            parts = task.id.split('.')
            if len(parts) == 2:
                major, minor = parts[0].split('-')[1], parts[1]
                revision_id = f"task-{major}.{int(minor) + 1}"
            else:
                revision_id = f"{task.id}-revision"
            
            # 创建修订任务
            revision_task = Task(
                id=revision_id,
                title=f"{task.title} (修订版)",
                description=f"""原任务：{task.title}

审查反馈：
{review.feedback}

修订要求：
{review.feedback}

修订指令：
请根据上述审查反馈进行修改和改进。
""",
                status=TaskStatus.PENDING,
                priority=task.priority,
                complexity=task.complexity,
                estimated_hours=task.estimated_hours * 0.8,
                depends_on=[task.id],  # 依赖原任务
            )
            
            # 保存修订任务
            return self.state_manager.create_task(revision_task)
        
        except Exception as e:
            return False
    
    def auto_review_loop(self, poll_interval: int = 30) -> None:
        """自动审查循环
        
        Args:
            poll_interval: 轮询间隔（秒）
        """
        print(f"[ReviewerAI] 🚀 启动自动审查循环...")
        
        while True:
            try:
                # 获取所有待审查任务
                review_tasks = self.state_manager.list_tasks_by_status(TaskStatus.REVIEW)
                
                for task in review_tasks:
                    print(f"[ReviewerAI] 📍 审查任务: {task.id}")
                    
                    # 进行审查
                    review = self.review_task(task)
                    
                    if review:
                        if review.score.passed:
                            print(f"[ReviewerAI] ✓ 审查通过 ({review.score.total}分)")
                        else:
                            print(f"[ReviewerAI] 🔧 需要修订 ({review.score.total}分)")
                    else:
                        print(f"[ReviewerAI] ✗ 审查失败")
                
                # 等待下一轮
                time.sleep(poll_interval)
            
            except KeyboardInterrupt:
                print(f"[ReviewerAI] ⏹️  停止审查循环")
                break
            except Exception as e:
                print(f"[ReviewerAI] ✗ 循环错误: {str(e)}")
                time.sleep(poll_interval)
    
    def generate_review_report(self, review: Review) -> str:
        """生成审查报告
        
        Args:
            review: 审查记录
            
        Returns:
            报告文本
        """
        score = review.score
        
        report = f"""# 代码审查报告 - {review.task_id}

**审查者**: {review.reviewer_id}  
**审查时间**: {review.created_at.isoformat()}  
**审查ID**: {review.id}

---

## 📊 评分结果

| 维度 | 得分 | 满分 | 比例 |
|------|------|------|------|
| 功能完整性 | {score.functionality} | 30 | {score.functionality/30*100:.0f}% |
| 代码质量 | {score.code_quality} | 25 | {score.code_quality/25*100:.0f}% |
| 规范遵守 | {score.standards} | 20 | {score.standards/20*100:.0f}% |
| 文档完整 | {score.documentation} | 15 | {score.documentation/15*100:.0f}% |
| 测试覆盖 | {score.testing} | 10 | {score.testing/10*100:.0f}% |
| **总分** | **{score.total}** | **100** | **{score.total}%** |

---

## ✅ 审查结果

**状态**: {'✅ 通过' if score.passed else '🔧 需要修订'}  
**决定**: {review.decision}  
**是否合并**: {'是' if score.passed else '否'}

---

## 💬 审查意见

{review.feedback}

---

## 🔧 修订建议

{review.feedback if not score.passed else '无需修订'}

---

**审查完成**
"""
        
        return report
