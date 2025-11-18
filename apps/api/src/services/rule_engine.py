# -*- coding: utf-8 -*-
"""
规则引擎（Rule Engine）

功能：
1. 定义事件处理规则
2. 匹配事件类型并执行对应动作
3. 支持5个核心规则：
   - task_completed → 提醒架构师审查
   - feature_developed → 触发集成验证
   - task_approved → 自动更新状态
   - issue_discovered → 查找历史方案
   - task_rejected → 通知开发者修改
"""

import logging
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from pathlib import Path
import sys

# 添加packages路径
packages_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "core-domain" / "src"
sys.path.insert(0, str(packages_path))

from services.event_service import EventEmitter, create_event_emitter


# ============================================================================
# 规则定义
# ============================================================================

class Rule:
    """
    规则类
    
    定义单个规则：条件匹配 + 动作执行
    """
    
    def __init__(
        self,
        rule_id: str,
        name: str,
        description: str,
        event_type_pattern: str,
        condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
        action: Callable[[Dict[str, Any], 'RuleEngine'], None] = None
    ):
        """
        初始化规则
        
        Args:
            rule_id: 规则ID
            name: 规则名称
            description: 规则描述
            event_type_pattern: 事件类型模式（支持通配符*）
            condition: 条件函数（可选），返回True表示匹配
            action: 动作函数，接收事件和规则引擎作为参数
        """
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.event_type_pattern = event_type_pattern
        self.condition = condition
        self.action = action
        self.is_enabled = True
        
        # 统计信息
        self.stats = {
            "triggered_count": 0,
            "success_count": 0,
            "error_count": 0,
            "last_triggered": None
        }
    
    def matches(self, event: Dict[str, Any]) -> bool:
        """
        检查事件是否匹配此规则
        
        Args:
            event: 事件对象
        
        Returns:
            是否匹配
        """
        if not self.is_enabled:
            return False
        
        # 匹配事件类型
        event_type = event.get("event_type", "")
        if not self._match_pattern(event_type, self.event_type_pattern):
            return False
        
        # 如果有条件函数，执行条件检查
        if self.condition:
            try:
                return self.condition(event)
            except Exception:
                return False
        
        return True
    
    def _match_pattern(self, text: str, pattern: str) -> bool:
        """
        简单的模式匹配（支持*通配符）
        
        Args:
            text: 待匹配文本
            pattern: 模式（支持*）
        
        Returns:
            是否匹配
        """
        # 完全匹配
        if pattern == text:
            return True
        
        # 通配符匹配
        if "*" in pattern:
            parts = pattern.split("*")
            if len(parts) == 2:
                prefix, suffix = parts
                return text.startswith(prefix) and text.endswith(suffix)
        
        return False
    
    def execute(self, event: Dict[str, Any], engine: 'RuleEngine') -> bool:
        """
        执行规则动作
        
        Args:
            event: 事件对象
            engine: 规则引擎实例
        
        Returns:
            是否执行成功
        """
        try:
            self.stats["triggered_count"] += 1
            self.stats["last_triggered"] = datetime.now().isoformat()
            
            if self.action:
                self.action(event, engine)
            
            self.stats["success_count"] += 1
            return True
            
        except Exception as e:
            logging.error(f"Error executing rule {self.rule_id}: {e}", exc_info=True)
            self.stats["error_count"] += 1
            return False


# ============================================================================
# 规则引擎
# ============================================================================

class RuleEngine:
    """
    规则引擎
    
    管理多个规则，匹配事件并执行对应动作
    """
    
    def __init__(self):
        """初始化规则引擎"""
        self.rules: List[Rule] = []
        self.logger = logging.getLogger(__name__)
        self.notification_service: Optional['NotificationService'] = None
        self.event_emitter: Optional[EventEmitter] = None
        
        # 统计信息
        self.stats = {
            "total_events_processed": 0,
            "total_rules_triggered": 0,
            "total_errors": 0,
            "started_at": datetime.now().isoformat()
        }
    
    def set_notification_service(self, notification_service: 'NotificationService') -> None:
        """设置通知服务"""
        self.notification_service = notification_service
        self.logger.info("Notification service set for RuleEngine")
    
    def set_event_emitter(self, event_emitter: EventEmitter) -> None:
        """设置事件发射器"""
        self.event_emitter = event_emitter
        self.logger.info("Event emitter set for RuleEngine")
    
    def register_rule(self, rule: Rule) -> None:
        """
        注册规则
        
        Args:
            rule: 规则对象
        """
        self.rules.append(rule)
        self.logger.info(f"Rule registered: {rule.rule_id} - {rule.name}")
    
    def unregister_rule(self, rule_id: str) -> bool:
        """
        注销规则
        
        Args:
            rule_id: 规则ID
        
        Returns:
            是否成功
        """
        for i, rule in enumerate(self.rules):
            if rule.rule_id == rule_id:
                self.rules.pop(i)
                self.logger.info(f"Rule unregistered: {rule_id}")
                return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """获取规则"""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def enable_rule(self, rule_id: str) -> bool:
        """启用规则"""
        rule = self.get_rule(rule_id)
        if rule:
            rule.is_enabled = True
            self.logger.info(f"Rule enabled: {rule_id}")
            return True
        return False
    
    def disable_rule(self, rule_id: str) -> bool:
        """禁用规则"""
        rule = self.get_rule(rule_id)
        if rule:
            rule.is_enabled = False
            self.logger.info(f"Rule disabled: {rule_id}")
            return True
        return False
    
    async def process_event(self, event: Dict[str, Any]) -> None:
        """
        处理事件，匹配规则并执行动作
        
        Args:
            event: 事件对象
        """
        try:
            self.stats["total_events_processed"] += 1
            event_type = event.get("event_type", "unknown")
            
            self.logger.debug(f"Processing event in RuleEngine: {event.get('id')} ({event_type})")
            
            # 匹配所有规则
            matched_rules = [rule for rule in self.rules if rule.matches(event)]
            
            if matched_rules:
                self.logger.info(f"Event {event.get('id')} matched {len(matched_rules)} rules")
                
                # 执行所有匹配的规则
                for rule in matched_rules:
                    success = rule.execute(event, self)
                    if success:
                        self.stats["total_rules_triggered"] += 1
            else:
                self.logger.debug(f"No rules matched for event: {event.get('id')}")
            
        except Exception as e:
            self.logger.error(f"Error in process_event: {e}", exc_info=True)
            self.stats["total_errors"] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "total_rules": len(self.rules),
            "enabled_rules": len([r for r in self.rules if r.is_enabled]),
            "rules": [
                {
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "is_enabled": rule.is_enabled,
                    "stats": rule.stats
                }
                for rule in self.rules
            ]
        }


# ============================================================================
# 5个核心规则动作
# ============================================================================

def action_task_completed(event: Dict[str, Any], engine: RuleEngine) -> None:
    """
    规则1: 任务完成 → 提醒架构师审查
    
    Args:
        event: 事件对象
        engine: 规则引擎
    """
    task_id = event.get("related_entity_id", "未知任务")
    task_title = event.get("title", "")
    
    # 发送通知
    if engine.notification_service:
        engine.notification_service.send_notification(
            title="📋 任务完成待审查",
            message=f"任务 {task_id} 已完成，请架构师审查",
            type="info",
            data={
                "task_id": task_id,
                "task_title": task_title,
                "action": "review_required",
                "event_id": event.get("id")
            }
        )
    
    # 记录事件
    if engine.event_emitter:
        engine.event_emitter.emit(
            project_id=event.get("project_id", "TASKFLOW"),
            event_type="architect.review_requested",
            title=f"架构师审查请求: {task_id}",
            description=f"任务 {task_id} 完成，等待架构师审查",
            category="task",
            source="system",
            severity="info",
            related_entity_type="task",
            related_entity_id=task_id
        )
    
    logging.info(f"Rule triggered: task_completed for {task_id}")


def action_feature_developed(event: Dict[str, Any], engine: RuleEngine) -> None:
    """
    规则2: 功能开发完成 → 触发集成验证
    
    Args:
        event: 事件对象
        engine: 规则引擎
    """
    feature_id = event.get("related_entity_id", "未知功能")
    
    # 发送通知
    if engine.notification_service:
        engine.notification_service.send_notification(
            title="🔧 需要集成验证",
            message=f"功能 {feature_id} 开发完成，需要进行集成验证",
            type="warning",
            data={
                "feature_id": feature_id,
                "action": "integration_test",
                "event_id": event.get("id")
            }
        )
    
    # 触发集成验证事件
    if engine.event_emitter:
        engine.event_emitter.emit(
            project_id=event.get("project_id", "TASKFLOW"),
            event_type="test.integration_required",
            title=f"集成验证需求: {feature_id}",
            description=f"功能 {feature_id} 需要集成验证",
            category="system",
            source="system",
            severity="warning",
            related_entity_type="feature",
            related_entity_id=feature_id
        )
    
    logging.info(f"Rule triggered: feature_developed for {feature_id}")


def action_task_approved(event: Dict[str, Any], engine: RuleEngine) -> None:
    """
    规则3: 任务审批通过 → 自动更新状态
    
    Args:
        event: 事件对象
        engine: 规则引擎
    """
    task_id = event.get("related_entity_id", "未知任务")
    
    # 发送通知
    if engine.notification_service:
        engine.notification_service.send_notification(
            title="✅ 任务已批准",
            message=f"任务 {task_id} 审批通过，状态已自动更新",
            type="success",
            data={
                "task_id": task_id,
                "action": "status_updated",
                "new_status": "completed",
                "event_id": event.get("id")
            }
        )
    
    # 记录状态更新事件
    if engine.event_emitter:
        engine.event_emitter.emit(
            project_id=event.get("project_id", "TASKFLOW"),
            event_type="task.status_updated",
            title=f"任务状态更新: {task_id}",
            description=f"任务 {task_id} 审批通过，状态更新为已完成",
            category="task",
            source="system",
            severity="info",
            related_entity_type="task",
            related_entity_id=task_id,
            data={"old_status": "review", "new_status": "completed"}
        )
    
    logging.info(f"Rule triggered: task_approved for {task_id}")


def action_issue_discovered(event: Dict[str, Any], engine: RuleEngine) -> None:
    """
    规则4: 问题发现 → 查找历史方案
    
    Args:
        event: 事件对象
        engine: 规则引擎
    """
    issue_id = event.get("related_entity_id", "未知问题")
    issue_title = event.get("title", "")
    
    # 发送通知（建议查找历史方案）
    if engine.notification_service:
        engine.notification_service.send_notification(
            title="⚠️ 问题发现",
            message=f"发现问题 {issue_id}，建议查找历史解决方案",
            type="warning",
            data={
                "issue_id": issue_id,
                "issue_title": issue_title,
                "action": "search_solutions",
                "event_id": event.get("id")
            }
        )
    
    # 触发历史方案搜索事件
    if engine.event_emitter:
        engine.event_emitter.emit(
            project_id=event.get("project_id", "TASKFLOW"),
            event_type="knowledge.search_requested",
            title=f"历史方案搜索: {issue_id}",
            description=f"问题 {issue_id} 需要搜索历史解决方案",
            category="issue",
            source="system",
            severity="info",
            related_entity_type="issue",
            related_entity_id=issue_id
        )
    
    logging.info(f"Rule triggered: issue_discovered for {issue_id}")


def action_task_rejected(event: Dict[str, Any], engine: RuleEngine) -> None:
    """
    规则5: 任务被拒绝 → 通知开发者修改
    
    Args:
        event: 事件对象
        engine: 规则引擎
    """
    task_id = event.get("related_entity_id", "未知任务")
    reject_reason = event.get("description", "未提供原因")
    
    # 发送通知
    if engine.notification_service:
        engine.notification_service.send_notification(
            title="❌ 任务需要修改",
            message=f"任务 {task_id} 被拒绝，需要修改后重新提交",
            type="error",
            data={
                "task_id": task_id,
                "reject_reason": reject_reason,
                "action": "revision_required",
                "event_id": event.get("id")
            }
        )
    
    # 记录拒绝事件
    if engine.event_emitter:
        engine.event_emitter.emit(
            project_id=event.get("project_id", "TASKFLOW"),
            event_type="task.revision_requested",
            title=f"任务修改请求: {task_id}",
            description=f"任务 {task_id} 需要修改: {reject_reason}",
            category="task",
            source="system",
            severity="warning",
            related_entity_type="task",
            related_entity_id=task_id,
            data={"reject_reason": reject_reason}
        )
    
    logging.info(f"Rule triggered: task_rejected for {task_id}")


# ============================================================================
# 便捷函数 - 创建预配置的规则引擎
# ============================================================================

def create_default_rule_engine() -> RuleEngine:
    """
    创建预配置的规则引擎（包含5个核心规则）
    
    Returns:
        RuleEngine实例
    """
    engine = RuleEngine()
    
    # 规则1: 任务完成 → 提醒架构师审查
    rule1 = Rule(
        rule_id="RULE-001",
        name="任务完成审查提醒",
        description="当任务完成时，提醒架构师进行审查",
        event_type_pattern="task.completed",
        action=action_task_completed
    )
    engine.register_rule(rule1)
    
    # 规则2: 功能开发完成 → 触发集成验证
    rule2 = Rule(
        rule_id="RULE-002",
        name="功能集成验证",
        description="当功能开发完成时，触发集成验证流程",
        event_type_pattern="feature.developed",
        action=action_feature_developed
    )
    engine.register_rule(rule2)
    
    # 规则3: 任务审批通过 → 自动更新状态
    rule3 = Rule(
        rule_id="RULE-003",
        name="任务自动审批",
        description="当任务审批通过时，自动更新任务状态",
        event_type_pattern="task.approved",
        action=action_task_approved
    )
    engine.register_rule(rule3)
    
    # 规则4: 问题发现 → 查找历史方案
    rule4 = Rule(
        rule_id="RULE-004",
        name="历史方案搜索",
        description="当发现问题时，自动搜索历史解决方案",
        event_type_pattern="issue.discovered",
        action=action_issue_discovered
    )
    engine.register_rule(rule4)
    
    # 规则5: 任务被拒绝 → 通知开发者修改
    rule5 = Rule(
        rule_id="RULE-005",
        name="任务拒绝通知",
        description="当任务被拒绝时，通知开发者进行修改",
        event_type_pattern="task.rejected",
        action=action_task_rejected
    )
    engine.register_rule(rule5)
    
    logging.info(f"Default rule engine created with {len(engine.rules)} rules")
    
    return engine

