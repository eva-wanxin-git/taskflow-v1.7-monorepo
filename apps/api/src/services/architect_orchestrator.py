# -*- coding: utf-8 -*-
"""
架构师编排器（Architect Orchestrator）

负责接收架构师AI的分析结果，将其转换为：
- 数据库记录（tasks, issues, decisions, knowledge_articles）
- Markdown文档（task-board.md等）
- API响应

这是架构师AI与任务所·Flow系统的桥梁
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json

from pydantic import BaseModel, Field


# ============================================================================
# Pydantic模型定义
# ============================================================================

class FeatureSummary(BaseModel):
    """功能摘要"""
    title: str = Field(..., description="功能标题")
    description: str = Field(..., description="功能描述")
    related_paths: List[str] = Field(default_factory=list, description="相关文件路径")
    completion: float = Field(default=1.0, ge=0, le=1, description="完成度0-1")
    notes: Optional[str] = Field(None, description="备注")


class PartialFeatureSummary(FeatureSummary):
    """部分实现功能摘要"""
    missing: List[str] = Field(..., description="缺少的部分")
    risk: Optional[str] = Field(None, description="风险描述")
    priority: str = Field(default="medium", description="优先级")


class ProblemSummary(BaseModel):
    """问题摘要"""
    title: str
    description: str
    severity: str = Field(..., description="严重程度: critical/high/medium/low")
    related_paths: List[str] = Field(default_factory=list)
    impact: str = Field(..., description="影响描述")
    suggested_solution: Optional[str] = None


class ArchitectTaskSuggestion(BaseModel):
    """架构师建议的任务"""
    id: str = Field(..., description="任务ID，如ARCH-001")
    title: str
    type: str = Field(..., description="类型: backend/frontend/refactor/bugfix/test/docs")
    priority: str = Field(..., description="优先级: critical/high/medium/low")
    component: str = Field(..., description="所属组件")
    description: str
    related_paths: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(default_factory=list, description="验收标准")
    estimated_hours: float = Field(default=0, description="预估工时")
    executor_type: str = Field(default="code-steward", description="建议执行者")
    dependencies: List[str] = Field(default_factory=list, description="依赖的任务ID")


class ArchitectAnalysis(BaseModel):
    """架构师完整分析结果"""
    project_code: str = Field(..., description="项目代码，如MY_PROJECT")
    repo_root: Optional[str] = Field(None, description="仓库根目录路径")
    completed_features: List[FeatureSummary] = Field(default_factory=list)
    partial_features: List[PartialFeatureSummary] = Field(default_factory=list)
    problems: List[ProblemSummary] = Field(default_factory=list)
    suggested_tasks: List[ArchitectTaskSuggestion] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="元数据")


class HandoverSnapshot(BaseModel):
    """交接快照"""
    snapshot_id: str
    project_code: str
    architect: str = Field(default="AI Architect v2")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    completed_phases: List[Dict[str, Any]] = Field(default_factory=list)
    current_focus: Dict[str, Any] = Field(default_factory=dict)
    key_files_analyzed: List[Dict[str, str]] = Field(default_factory=list)
    unanalyzed_areas: List[str] = Field(default_factory=list)
    recommendations_for_next: List[str] = Field(default_factory=list)
    token_usage: Optional[Dict[str, Any]] = None


# ============================================================================
# 架构师编排器
# ============================================================================

class ArchitectOrchestrator:
    """架构师编排器
    
    负责将架构师AI的分析结果转换为系统可用的格式：
    - 写入数据库（通过Repository）
    - 生成Markdown文档
    - 记录到知识库
    """
    
    def __init__(
        self,
        state_manager=None,
        docs_root: str = "docs"
    ):
        """
        初始化
        
        Args:
            state_manager: 状态管理器（访问数据库）
            docs_root: 文档根目录路径
        """
        self.state_manager = state_manager
        self.docs_root = Path(docs_root)
        
    def process_analysis(
        self,
        analysis: ArchitectAnalysis
    ) -> Dict[str, Any]:
        """
        处理架构师分析结果
        
        Args:
            analysis: 架构师分析结果
            
        Returns:
            处理结果统计：{
                "tasks_created": 12,
                "issues_created": 3,
                "components_created": 2,
                "task_board_updated": True
            }
        """
        result = {
            "tasks_created": 0,
            "issues_created": 0,
            "decisions_created": 0,
            "articles_created": 0,
            "components_created": 0,
            "task_board_updated": False
        }
        
        # 1. 确保项目和组件存在
        self._ensure_project_exists(analysis.project_code)
        result["components_created"] = self._ensure_components_exist(
            analysis.project_code,
            analysis.suggested_tasks
        )
        
        # 2. 创建任务
        result["tasks_created"] = self._create_tasks_from_suggestions(
            analysis.project_code,
            analysis.suggested_tasks
        )
        
        # 3. 记录问题
        result["issues_created"] = self._create_issues_from_problems(
            analysis.project_code,
            analysis.problems
        )
        
        # 4. 记录功能清单（作为知识文章）
        result["articles_created"] = self._create_feature_articles(
            analysis.project_code,
            analysis.completed_features,
            analysis.partial_features
        )
        
        # 5. 更新任务看板文档
        result["task_board_updated"] = self._update_task_board_md(analysis)
        
        return result
    
    def _ensure_project_exists(self, project_code: str) -> None:
        """确保项目存在，不存在则创建"""
        # TODO: 调用state_manager检查/创建项目
        pass
    
    def _ensure_components_exist(
        self,
        project_code: str,
        tasks: List[ArchitectTaskSuggestion]
    ) -> int:
        """根据任务中的component字段，确保组件存在"""
        components = set(task.component for task in tasks)
        created = 0
        
        for component_name in components:
            # TODO: 检查组件是否存在，不存在则创建
            # 组件ID格式：{project_code}-{component_name}
            # 例如：MY_PROJECT-infra-llm
            created += 1
        
        return created
    
    def _create_tasks_from_suggestions(
        self,
        project_code: str,
        suggestions: List[ArchitectTaskSuggestion]
    ) -> int:
        """将建议任务转换为实际任务记录"""
        created = 0
        
        for suggestion in suggestions:
            # 构造Task对象
            task_data = {
                "id": suggestion.id,
                "title": suggestion.title,
                "description": suggestion.description,
                "status": "pending",
                "priority": self._map_priority(suggestion.priority),
                "estimated_hours": suggestion.estimated_hours,
                "complexity": self._infer_complexity(suggestion.estimated_hours),
                "project_id": project_code,
                "component_id": f"{project_code}-{suggestion.component}",
                "metadata": {
                    "type": suggestion.type,
                    "executor_type": suggestion.executor_type,
                    "related_paths": suggestion.related_paths,
                    "acceptance_criteria": suggestion.acceptance_criteria,
                    "source": "architect_analysis"
                }
            }
            
            # TODO: 调用state_manager.create_task(task_data)
            created += 1
        
        return created
    
    def _create_issues_from_problems(
        self,
        project_code: str,
        problems: List[ProblemSummary]
    ) -> int:
        """将问题转换为issue记录"""
        created = 0
        
        for problem in problems:
            issue_data = {
                "id": f"ISS-{datetime.now().strftime('%Y%m%d')}-{created+1:03d}",
                "project_id": project_code,
                "title": problem.title,
                "description": problem.description,
                "severity": problem.severity,
                "status": "open",
                "discovered_at": datetime.now().isoformat(),
                # TODO: 从related_paths推断component_id
            }
            
            # TODO: 调用state_manager创建issue
            created += 1
        
        return created
    
    def _create_feature_articles(
        self,
        project_code: str,
        completed: List[FeatureSummary],
        partial: List[PartialFeatureSummary]
    ) -> int:
        """将功能清单记录为知识文章"""
        created = 0
        
        # 1. 已完成功能文章
        if completed:
            article = {
                "id": f"ART-{project_code}-completed-features",
                "project_id": project_code,
                "title": f"{project_code} - 已实现功能清单",
                "content": self._format_features_as_markdown(completed),
                "category": "feature-list",
                "tags": json.dumps(["completed", "features"]),
                "created_at": datetime.now().isoformat()
            }
            # TODO: 保存到knowledge_articles表
            created += 1
        
        # 2. 部分实现功能文章
        if partial:
            article = {
                "id": f"ART-{project_code}-partial-features",
                "project_id": project_code,
                "title": f"{project_code} - 部分实现功能清单",
                "content": self._format_partial_features_as_markdown(partial),
                "category": "feature-list",
                "tags": json.dumps(["partial", "features", "wip"]),
                "created_at": datetime.now().isoformat()
            }
            # TODO: 保存到knowledge_articles表
            created += 1
        
        return created
    
    def _update_task_board_md(self, analysis: ArchitectAnalysis) -> bool:
        """更新任务看板Markdown文档"""
        task_board_path = self.docs_root / "tasks" / "task-board.md"
        task_board_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成Markdown内容
        content = self._generate_task_board_markdown(analysis)
        
        # 写入文件
        task_board_path.write_text(content, encoding='utf-8')
        
        return True
    
    def _generate_task_board_markdown(self, analysis: ArchitectAnalysis) -> str:
        """生成任务看板Markdown"""
        lines = []
        
        # 标题
        lines.append(f"# 任务看板\n")
        lines.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        lines.append(f"**项目**: {analysis.project_code}\n")
        lines.append(f"**架构师**: AI Architect\n\n")
        
        # 统计
        total = len(analysis.suggested_tasks)
        by_priority = self._group_by_priority(analysis.suggested_tasks)
        
        lines.append("## 📊 统计\n")
        lines.append(f"- 总任务: {total}\n")
        lines.append(f"- P0: {len(by_priority.get('critical', []))}\n")
        lines.append(f"- P1: {len(by_priority.get('high', []))}\n")
        lines.append(f"- P2: {len(by_priority.get('medium', []))}\n")
        lines.append(f"- P3: {len(by_priority.get('low', []))}\n\n")
        
        lines.append("---\n\n")
        
        # 任务列表（按优先级分组）
        lines.append("## 📋 任务列表\n\n")
        
        for priority_label, priority_key in [
            ("🔴 高优先级（P0/P1）", ["critical", "high"]),
            ("🟡 普通优先级（P2）", ["medium"]),
            ("🟢 低优先级（P3）", ["low"])
        ]:
            tasks_in_group = []
            for key in priority_key:
                tasks_in_group.extend(by_priority.get(key, []))
            
            if not tasks_in_group:
                continue
            
            lines.append(f"### {priority_label}\n\n")
            
            for task in tasks_in_group:
                lines.append(f"#### {task.id}: {task.title}\n")
                lines.append(f"- **类型**: {task.type}\n")
                lines.append(f"- **范围**: {task.component}\n")
                lines.append(f"- **状态**: 待处理\n")
                lines.append(f"- **优先级**: {task.priority}\n")
                lines.append(f"- **预估工时**: {task.estimated_hours}小时\n")
                lines.append(f"- **建议执行者**: {task.executor_type}\n\n")
                
                lines.append(f"**任务描述**:\n{task.description}\n\n")
                
                if task.acceptance_criteria:
                    lines.append("**验收标准**:\n")
                    for criterion in task.acceptance_criteria:
                        lines.append(f"- [ ] {criterion}\n")
                    lines.append("\n")
                
                if task.related_paths:
                    lines.append("**相关文件**:\n")
                    for path in task.related_paths:
                        lines.append(f"- `{path}`\n")
                    lines.append("\n")
                
                lines.append("---\n\n")
        
        # 问题清单
        if analysis.problems:
            lines.append("## 🔴 发现的问题\n\n")
            for i, problem in enumerate(analysis.problems, 1):
                severity_emoji = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢"
                }.get(problem.severity, "⚪")
                
                lines.append(f"### {i}. {problem.title} {severity_emoji} {problem.severity}\n")
                lines.append(f"{problem.description}\n\n")
                lines.append(f"**影响**: {problem.impact}\n\n")
                if problem.suggested_solution:
                    lines.append(f"**建议解决方案**: {problem.suggested_solution}\n\n")
                if problem.related_paths:
                    lines.append(f"**相关文件**: {', '.join(f'`{p}`' for p in problem.related_paths)}\n\n")
                lines.append("---\n\n")
        
        # 功能清单摘要
        if analysis.completed_features or analysis.partial_features:
            lines.append("## 📊 功能清单摘要\n\n")
            lines.append(f"- ✅ 已完成: {len(analysis.completed_features)}个功能\n")
            lines.append(f"- 🟡 部分完成: {len(analysis.partial_features)}个功能\n")
            lines.append(f"\n详见: `docs/arch/architecture-review.md`\n\n")
        
        # 关联链接
        lines.append("---\n\n")
        lines.append("## 🔗 相关文档\n\n")
        lines.append("- [架构清单](../arch/architecture-inventory.md)\n")
        lines.append("- [架构审查](../arch/architecture-review.md)\n")
        lines.append("- [重构计划](../arch/refactor-plan.md)\n")
        
        if analysis.metadata and analysis.metadata.get("taskflow_api"):
            api_url = analysis.metadata["taskflow_api"]
            lines.append(f"\n**任务所·Flow Dashboard**: {api_url}\n")
        
        return "".join(lines)
    
    def process_handover(self, snapshot: HandoverSnapshot) -> Dict[str, Any]:
        """处理交接快照"""
        # 1. 保存快照到文件
        handover_dir = self.docs_root / "arch" / "handovers"
        handover_dir.mkdir(parents=True, exist_ok=True)
        
        snapshot_path = handover_dir / f"{snapshot.snapshot_id}.json"
        snapshot_path.write_text(
            snapshot.json(indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        # 2. 更新HANDOVER.md
        self._update_handover_md(snapshot)
        
        # 3. TODO: 保存到数据库 handover_snapshots表
        
        return {
            "snapshot_saved": True,
            "snapshot_path": str(snapshot_path),
            "handover_md_updated": True
        }
    
    def _update_handover_md(self, snapshot: HandoverSnapshot) -> None:
        """更新HANDOVER.md交接说明"""
        handover_md_path = self.docs_root / "arch" / "HANDOVER.md"
        
        content = f"""# 最新交接说明

**交接时间**: {snapshot.timestamp}  
**快照ID**: {snapshot.snapshot_id}  
**架构师**: {snapshot.architect}

## 📍 下一任架构师请从这里开始

### 快速上手
1. 阅读快照: `handovers/{snapshot.snapshot_id}.json`
2. 阅读四份核心文档（已更新到最新）:
   - architecture-inventory.md
   - architecture-review.md
   - refactor-plan.md
   - task-board.md

### 当前状态
"""
        
        # 添加完成阶段
        if snapshot.completed_phases:
            content += "\n**已完成阶段**:\n"
            for phase in snapshot.completed_phases:
                content += f"- {phase['phase']}: {phase['progress']}%\n"
        
        # 添加当前焦点
        if snapshot.current_focus:
            focus = snapshot.current_focus
            content += f"\n**当前焦点**: {focus.get('area', 'N/A')}\n"
            content += f"**状态**: {focus.get('status', 'N/A')}\n"
            if focus.get('blockers'):
                content += f"**阻塞**: {', '.join(focus['blockers'])}\n"
        
        # 添加建议
        if snapshot.recommendations_for_next:
            content += "\n### 下一步建议\n"
            for i, rec in enumerate(snapshot.recommendations_for_next, 1):
                content += f"{i}. {rec}\n"
        
        content += f"""
---

**快照文件**: `handovers/{snapshot.snapshot_id}.json`  
**查看完整快照**: 打开上述JSON文件
"""
        
        handover_md_path.write_text(content, encoding='utf-8')
    
    # ========================================================================
    # 辅助方法
    # ========================================================================
    
    def _map_priority(self, priority: str) -> str:
        """映射优先级"""
        mapping = {
            "critical": "P0",
            "high": "P1",
            "medium": "P2",
            "low": "P3"
        }
        return mapping.get(priority.lower(), "P2")
    
    def _infer_complexity(self, hours: float) -> str:
        """根据工时推断复杂度"""
        if hours <= 4:
            return "low"
        elif hours <= 16:
            return "medium"
        else:
            return "high"
    
    def _group_by_priority(
        self,
        tasks: List[ArchitectTaskSuggestion]
    ) -> Dict[str, List[ArchitectTaskSuggestion]]:
        """按优先级分组任务"""
        groups = {}
        for task in tasks:
            priority = task.priority.lower()
            if priority not in groups:
                groups[priority] = []
            groups[priority].append(task)
        return groups
    
    def _format_features_as_markdown(self, features: List[FeatureSummary]) -> str:
        """将功能列表格式化为Markdown"""
        lines = ["# 已实现功能清单\n\n"]
        
        for i, feature in enumerate(features, 1):
            lines.append(f"## {i}. {feature.title}\n\n")
            lines.append(f"{feature.description}\n\n")
            lines.append(f"**完成度**: {feature.completion*100:.0f}%\n\n")
            if feature.related_paths:
                lines.append("**相关文件**:\n")
                for path in feature.related_paths:
                    lines.append(f"- `{path}`\n")
                lines.append("\n")
            if feature.notes:
                lines.append(f"**备注**: {feature.notes}\n\n")
            lines.append("---\n\n")
        
        return "".join(lines)
    
    def _format_partial_features_as_markdown(
        self,
        features: List[PartialFeatureSummary]
    ) -> str:
        """将部分实现功能格式化为Markdown"""
        lines = ["# 部分实现功能清单\n\n"]
        
        for i, feature in enumerate(features, 1):
            lines.append(f"## {i}. {feature.title} ⚠️ {feature.completion*100:.0f}%\n\n")
            lines.append(f"{feature.description}\n\n")
            
            lines.append(f"**已完成**: {feature.completion*100:.0f}%\n\n")
            
            lines.append("**缺少部分**:\n")
            for missing in feature.missing:
                lines.append(f"- ❌ {missing}\n")
            lines.append("\n")
            
            if feature.risk:
                lines.append(f"**风险**: {feature.risk}\n\n")
            
            lines.append(f"**优先级**: {feature.priority}\n\n")
            lines.append("---\n\n")
        
        return "".join(lines)


# ============================================================================
# 辅助函数
# ============================================================================

def create_architect_orchestrator(state_manager=None, docs_root="docs"):
    """创建架构师编排器实例（工厂函数）"""
    return ArchitectOrchestrator(
        state_manager=state_manager,
        docs_root=docs_root
    )

