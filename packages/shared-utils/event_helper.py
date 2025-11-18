# -*- coding: utf-8 -*-
"""
事件触发辅助工具 (Event Helper)

提供简化的事件触发接口，用于在脚本和API中快速集成事件发射功能。

使用示例：
    from shared_utils.event_helper import EventHelper
    
    helper = EventHelper(project_id="TASKFLOW")
    
    # 任务相关事件
    helper.task_created(task_id="TASK-001", title="实现XXX功能")
    helper.task_started(task_id="TASK-001", actor="fullstack-engineer")
    helper.task_completed(task_id="TASK-001", actual_hours=2.5)
    
    # 功能相关事件
    helper.feature_integrated(feature_id="FEAT-001", component="api")
    
    # 问题相关事件
    helper.issue_discovered(issue_id="ISS-001", severity="high")
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# 添加event_service路径
packages_path = Path(__file__).parent.parent / "core-domain" / "src"
sys.path.insert(0, str(packages_path))

from services.event_service import (
    EventEmitter,
    EventStore,
    EventSeverity,
    EventCategory,
    EventSource,
    create_event_emitter
)


class EventHelper:
    """
    事件触发辅助类
    
    简化事件发射，提供高层API
    """
    
    def __init__(
        self,
        project_id: str = "TASKFLOW",
        actor: Optional[str] = None,
        source: str = EventSource.SYSTEM
    ):
        """
        初始化事件助手
        
        Args:
            project_id: 项目ID，默认TASKFLOW
            actor: 默认操作者
            source: 事件来源（system/user/ai/external）
        """
        self.project_id = project_id
        self.default_actor = actor
        self.default_source = source
        self.emitter = create_event_emitter()
    
    # ========================================================================
    # 任务生命周期事件 (Task Lifecycle Events)
    # ========================================================================
    
    def task_created(
        self,
        task_id: str,
        title: str,
        priority: Optional[str] = None,
        assigned_to: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        dependencies: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        任务创建事件
        
        Args:
            task_id: 任务ID
            title: 任务标题
            priority: 优先级 (P0/P1/P2)
            assigned_to: 分配给谁
            estimated_hours: 预估工时
            dependencies: 依赖任务列表
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="task.created",
            title=f"任务创建: {title}",
            description=f"新任务 {task_id} 已创建",
            data={
                "task_id": task_id,
                "priority": priority,
                "assigned_to": assigned_to,
                "estimated_hours": estimated_hours,
                "dependencies": dependencies or []
            },
            category=EventCategory.TASK,
            source=kwargs.get("source", self.default_source),
            actor=kwargs.get("actor", self.default_actor),
            severity=EventSeverity.INFO,
            related_entity_type="task",
            related_entity_id=task_id,
            tags=["task", "created", priority] if priority else ["task", "created"]
        )
    
    def task_dispatched(
        self,
        task_id: str,
        assigned_to: str,
        reason: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        任务派发事件
        
        Args:
            task_id: 任务ID
            assigned_to: 派发给谁
            reason: 派发原因
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="task.dispatched",
            title=f"任务派发: {task_id} → {assigned_to}",
            description=f"任务 {task_id} 已派发给 {assigned_to}",
            data={
                "task_id": task_id,
                "assigned_to": assigned_to,
                "reason": reason
            },
            category=EventCategory.TASK,
            source=kwargs.get("source", self.default_source),
            actor=kwargs.get("actor", self.default_actor or "architect"),
            severity=EventSeverity.INFO,
            related_entity_type="task",
            related_entity_id=task_id,
            tags=["task", "dispatched", assigned_to]
        )
    
    def task_started(
        self,
        task_id: str,
        actor: Optional[str] = None,
        planned_completion: Optional[str] = None,
        work_plan: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        任务开始事件
        
        Args:
            task_id: 任务ID
            actor: 谁开始任务
            planned_completion: 计划完成时间
            work_plan: 工作计划
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="task.started",
            title=f"任务开始: {task_id}",
            description=f"{actor or 'Engineer'} 开始执行任务 {task_id}",
            data={
                "task_id": task_id,
                "planned_completion": planned_completion,
                "work_plan": work_plan
            },
            category=EventCategory.TASK,
            source=kwargs.get("source", self.default_source),
            actor=actor or self.default_actor or "engineer",
            severity=EventSeverity.INFO,
            related_entity_type="task",
            related_entity_id=task_id,
            tags=["task", "started"]
        )
    
    def task_completed(
        self,
        task_id: str,
        actor: Optional[str] = None,
        actual_hours: Optional[float] = None,
        files_modified: Optional[List[str]] = None,
        completion_summary: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        任务完成事件
        
        Args:
            task_id: 任务ID
            actor: 谁完成任务
            actual_hours: 实际工时
            files_modified: 修改的文件列表
            completion_summary: 完成摘要
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="task.completed",
            title=f"任务完成: {task_id}",
            description=completion_summary or f"任务 {task_id} 已完成",
            data={
                "task_id": task_id,
                "actual_hours": actual_hours,
                "files_modified": files_modified or [],
                "completion_summary": completion_summary
            },
            category=EventCategory.TASK,
            source=kwargs.get("source", self.default_source),
            actor=actor or self.default_actor or "engineer",
            severity=EventSeverity.INFO,
            related_entity_type="task",
            related_entity_id=task_id,
            tags=["task", "completed"]
        )
    
    def task_reviewed(
        self,
        task_id: str,
        reviewer: str,
        result: str,  # "approved" or "rejected"
        score: Optional[int] = None,
        feedback: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        任务审查事件
        
        Args:
            task_id: 任务ID
            reviewer: 审查者
            result: 审查结果 (approved/rejected)
            score: 审查评分
            feedback: 反馈意见
        """
        severity = EventSeverity.INFO if result == "approved" else EventSeverity.WARNING
        
        return self.emitter.emit(
            project_id=self.project_id,
            event_type=f"task.{result}",
            title=f"任务审查: {task_id} - {result}",
            description=feedback or f"任务 {task_id} 审查{result}",
            data={
                "task_id": task_id,
                "result": result,
                "score": score,
                "feedback": feedback
            },
            category=EventCategory.TASK,
            source=kwargs.get("source", self.default_source),
            actor=reviewer,
            severity=severity,
            related_entity_type="task",
            related_entity_id=task_id,
            tags=["task", "reviewed", result]
        )
    
    def task_approved(
        self,
        task_id: str,
        reviewer: str,
        score: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """任务批准事件（便捷方法）"""
        return self.task_reviewed(
            task_id=task_id,
            reviewer=reviewer,
            result="approved",
            score=score,
            **kwargs
        )
    
    def task_rejected(
        self,
        task_id: str,
        reviewer: str,
        reason: str,
        **kwargs
    ) -> Dict[str, Any]:
        """任务拒绝事件（便捷方法）"""
        return self.task_reviewed(
            task_id=task_id,
            reviewer=reviewer,
            result="rejected",
            feedback=reason,
            **kwargs
        )
    
    # ========================================================================
    # 功能/特性事件 (Feature Events)
    # ========================================================================
    
    def feature_integrated(
        self,
        feature_id: str,
        component: str,
        description: Optional[str] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        功能集成事件
        
        Args:
            feature_id: 功能ID
            component: 集成的组件
            description: 描述
            version: 版本号
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="feature.integrated",
            title=f"功能集成: {feature_id}",
            description=description or f"功能 {feature_id} 已集成到 {component}",
            data={
                "feature_id": feature_id,
                "component": component,
                "version": version
            },
            category=EventCategory.GENERAL,
            source=kwargs.get("source", self.default_source),
            actor=kwargs.get("actor", self.default_actor),
            severity=EventSeverity.INFO,
            related_entity_type="feature",
            related_entity_id=feature_id,
            tags=["feature", "integrated", component]
        )
    
    def feature_deployed(
        self,
        feature_id: str,
        environment: str,
        version: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        功能部署事件
        
        Args:
            feature_id: 功能ID
            environment: 部署环境 (dev/staging/prod)
            version: 版本号
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="feature.deployed",
            title=f"功能部署: {feature_id} v{version}",
            description=f"功能 {feature_id} 已部署到 {environment}",
            data={
                "feature_id": feature_id,
                "environment": environment,
                "version": version
            },
            category=EventCategory.DEPLOYMENT,
            source=kwargs.get("source", self.default_source),
            actor=kwargs.get("actor", self.default_actor),
            severity=EventSeverity.WARNING,  # 部署是重要事件
            related_entity_type="feature",
            related_entity_id=feature_id,
            tags=["feature", "deployed", environment]
        )
    
    # ========================================================================
    # 问题事件 (Issue Events)
    # ========================================================================
    
    def issue_discovered(
        self,
        issue_id: str,
        title: str,
        severity: str = "medium",
        component: Optional[str] = None,
        impact: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        问题发现事件
        
        Args:
            issue_id: 问题ID
            title: 问题标题
            severity: 严重性 (low/medium/high/critical)
            component: 影响的组件
            impact: 影响说明
        """
        # 映射severity到EventSeverity
        severity_map = {
            "low": EventSeverity.INFO,
            "medium": EventSeverity.WARNING,
            "high": EventSeverity.ERROR,
            "critical": EventSeverity.CRITICAL
        }
        event_severity = severity_map.get(severity, EventSeverity.WARNING)
        
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="issue.discovered",
            title=f"问题发现: {title}",
            description=impact or f"发现 {severity} 级别问题: {issue_id}",
            data={
                "issue_id": issue_id,
                "severity": severity,
                "component": component,
                "impact": impact
            },
            category=EventCategory.ISSUE,
            source=kwargs.get("source", self.default_source),
            actor=kwargs.get("actor", self.default_actor),
            severity=event_severity,
            related_entity_type="issue",
            related_entity_id=issue_id,
            tags=["issue", "discovered", severity]
        )
    
    def issue_resolved(
        self,
        issue_id: str,
        solution: str,
        resolved_by: str,
        time_spent: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        问题解决事件
        
        Args:
            issue_id: 问题ID
            solution: 解决方案
            resolved_by: 解决者
            time_spent: 花费时间（小时）
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="issue.resolved",
            title=f"问题解决: {issue_id}",
            description=solution,
            data={
                "issue_id": issue_id,
                "solution": solution,
                "time_spent": time_spent
            },
            category=EventCategory.ISSUE,
            source=kwargs.get("source", self.default_source),
            actor=resolved_by,
            severity=EventSeverity.INFO,
            related_entity_type="issue",
            related_entity_id=issue_id,
            tags=["issue", "resolved"]
        )
    
    # ========================================================================
    # 技术决策事件 (Decision Events)
    # ========================================================================
    
    def decision_recorded(
        self,
        decision_id: str,
        title: str,
        decision: str,
        context: Optional[str] = None,
        impact: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        技术决策记录事件
        
        Args:
            decision_id: 决策ID (如: ADR-0001)
            title: 决策标题
            decision: 决策内容
            context: 决策背景
            impact: 影响范围
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="decision.recorded",
            title=f"技术决策: {title}",
            description=decision,
            data={
                "decision_id": decision_id,
                "context": context,
                "impact": impact
            },
            category=EventCategory.DECISION,
            source=kwargs.get("source", self.default_source),
            actor=kwargs.get("actor", self.default_actor or "architect"),
            severity=EventSeverity.WARNING,  # 决策是重要事件
            related_entity_type="decision",
            related_entity_id=decision_id,
            tags=["decision", "recorded"]
        )
    
    # ========================================================================
    # 系统事件 (System Events)
    # ========================================================================
    
    def milestone_reached(
        self,
        milestone_id: str,
        milestone_name: str,
        tasks_completed: int,
        quality_metrics: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        里程碑达成事件
        
        Args:
            milestone_id: 里程碑ID
            milestone_name: 里程碑名称
            tasks_completed: 完成任务数
            quality_metrics: 质量指标
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="milestone.reached",
            title=f"里程碑达成: {milestone_name}",
            description=f"已完成 {tasks_completed} 个任务",
            data={
                "milestone_id": milestone_id,
                "tasks_completed": tasks_completed,
                "quality_metrics": quality_metrics or {}
            },
            category=EventCategory.SYSTEM,
            source=kwargs.get("source", self.default_source),
            actor=kwargs.get("actor", self.default_actor or "system"),
            severity=EventSeverity.CRITICAL,  # 里程碑是关键事件
            related_entity_type="milestone",
            related_entity_id=milestone_id,
            tags=["milestone", "reached"]
        )
    
    def risk_identified(
        self,
        risk_id: str,
        risk_type: str,
        description: str,
        impact: str,
        mitigation: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        风险识别事件
        
        Args:
            risk_id: 风险ID
            risk_type: 风险类型 (delay/quality/technical)
            description: 风险描述
            impact: 影响程度 (low/medium/high)
            mitigation: 缓解措施
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="risk.identified",
            title=f"风险识别: {risk_type}",
            description=description,
            data={
                "risk_id": risk_id,
                "risk_type": risk_type,
                "impact": impact,
                "mitigation": mitigation
            },
            category=EventCategory.SYSTEM,
            source=kwargs.get("source", self.default_source),
            actor=kwargs.get("actor", self.default_actor or "system"),
            severity=EventSeverity.CRITICAL,
            related_entity_type="risk",
            related_entity_id=risk_id,
            tags=["risk", "identified", risk_type]
        )
    
    # ========================================================================
    # 架构师事件 (Architect Events)
    # ========================================================================
    
    def architect_handover(
        self,
        snapshot_id: str,
        progress: str,
        pending_tasks: List[str],
        critical_notes: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        架构师交接事件
        
        Args:
            snapshot_id: 快照ID
            progress: 当前进度
            pending_tasks: 待处理任务列表
            critical_notes: 关键提醒
        """
        return self.emitter.emit(
            project_id=self.project_id,
            event_type="architect.handover",
            title=f"架构师交接: {snapshot_id}",
            description=critical_notes or f"项目进度 {progress}，待处理 {len(pending_tasks)} 个任务",
            data={
                "snapshot_id": snapshot_id,
                "progress": progress,
                "pending_tasks": pending_tasks,
                "critical_notes": critical_notes
            },
            category=EventCategory.SYSTEM,
            source=kwargs.get("source", EventSource.AI),
            actor=kwargs.get("actor", "architect"),
            severity=EventSeverity.WARNING,
            tags=["architect", "handover"]
        )


# ============================================================================
# 便捷函数
# ============================================================================

def create_event_helper(
    project_id: str = "TASKFLOW",
    actor: Optional[str] = None,
    source: str = EventSource.SYSTEM
) -> EventHelper:
    """
    创建事件助手实例
    
    Args:
        project_id: 项目ID
        actor: 默认操作者
        source: 事件来源
    
    Returns:
        EventHelper实例
    """
    return EventHelper(project_id=project_id, actor=actor, source=source)


# ============================================================================
# 模块测试
# ============================================================================

if __name__ == "__main__":
    import io
    
    # 设置UTF-8编码
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("===== Event Helper Test =====\n")
    
    # 创建EventHelper实例
    helper = create_event_helper(
        project_id="TEST_PROJECT",
        actor="test_user",
        source=EventSource.USER
    )
    
    print("Testing task events...")
    
    # 测试任务事件
    event1 = helper.task_created(
        task_id="TEST-001",
        title="测试任务",
        priority="P0",
        assigned_to="engineer"
    )
    print(f"✓ Task created event: {event1['id']}")
    
    event2 = helper.task_started(
        task_id="TEST-001",
        actor="engineer"
    )
    print(f"✓ Task started event: {event2['id']}")
    
    event3 = helper.task_completed(
        task_id="TEST-001",
        actor="engineer",
        actual_hours=2.0
    )
    print(f"✓ Task completed event: {event3['id']}")
    
    # 测试问题事件
    event4 = helper.issue_discovered(
        issue_id="ISS-001",
        title="测试问题",
        severity="high"
    )
    print(f"✓ Issue discovered event: {event4['id']}")
    
    print("\n✅ All tests passed!")

