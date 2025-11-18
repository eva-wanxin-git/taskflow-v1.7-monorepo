# -*- coding: utf-8 -*-
"""
事件监听器系统测试

测试内容：
1. EventListener - 事件监听器
2. RuleEngine - 规则引擎
3. NotificationService - 通知服务
4. 5个核心规则的触发
"""

import pytest
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# 添加src路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# 添加packages路径
packages_path = Path(__file__).parent.parent.parent.parent / "packages" / "core-domain" / "src"
sys.path.insert(0, str(packages_path))

from services.event_listener import EventListener
from services.rule_engine import RuleEngine, Rule, create_default_rule_engine
from services.notification_service import NotificationService, NotificationType, create_notification_service
from services.event_service import create_event_emitter, create_event_store


# ============================================================================
# Fixture - 测试服务实例
# ============================================================================

@pytest.fixture
def event_store():
    """事件存储实例"""
    return create_event_store()


@pytest.fixture
def event_emitter(event_store):
    """事件发射器实例"""
    return create_event_emitter()


@pytest.fixture
def notification_service():
    """通知服务实例"""
    return create_notification_service(max_notifications=100)


@pytest.fixture
def rule_engine(notification_service, event_emitter):
    """规则引擎实例"""
    engine = create_default_rule_engine()
    engine.set_notification_service(notification_service)
    engine.set_event_emitter(event_emitter)
    return engine


@pytest.fixture
def event_listener(event_store, rule_engine, notification_service):
    """事件监听器实例"""
    listener = EventListener(
        event_store=event_store,
        poll_interval=1,  # 1秒轮询间隔（测试用）
        project_id="TEST_PROJECT"
    )
    listener.set_rule_engine(rule_engine)
    listener.set_notification_service(notification_service)
    return listener


# ============================================================================
# 测试：NotificationService
# ============================================================================

def test_notification_service_send(notification_service):
    """测试发送通知"""
    notification = notification_service.send_notification(
        title="测试通知",
        message="这是一条测试通知",
        type=NotificationType.INFO
    )
    
    assert notification["title"] == "测试通知"
    assert notification["message"] == "这是一条测试通知"
    assert notification["type"] == NotificationType.INFO
    assert notification["read"] is False
    assert "id" in notification
    
    # 检查统计
    stats = notification_service.get_stats()
    assert stats["total_sent"] == 1
    assert stats["info_count"] == 1


def test_notification_service_get_notifications(notification_service):
    """测试获取通知列表"""
    # 发送多条通知
    notification_service.send_notification("通知1", "内容1", type=NotificationType.INFO)
    notification_service.send_notification("通知2", "内容2", type=NotificationType.SUCCESS)
    notification_service.send_notification("通知3", "内容3", type=NotificationType.WARNING)
    
    # 获取所有通知
    notifications = notification_service.get_notifications(limit=10)
    assert len(notifications) == 3
    
    # 获取未读通知
    unread = notification_service.get_notifications(unread_only=True)
    assert len(unread) == 3
    
    # 标记一条为已读
    notification_service.mark_as_read(notifications[0]["id"])
    
    # 再次获取未读通知
    unread = notification_service.get_notifications(unread_only=True)
    assert len(unread) == 2


def test_notification_service_type_filter(notification_service):
    """测试类型过滤"""
    notification_service.send_notification("Info", "内容", type=NotificationType.INFO)
    notification_service.send_notification("Warning", "内容", type=NotificationType.WARNING)
    notification_service.send_notification("Error", "内容", type=NotificationType.ERROR)
    
    # 只获取警告类型
    warnings = notification_service.get_notifications(type_filter=NotificationType.WARNING)
    assert len(warnings) == 1
    assert warnings[0]["type"] == NotificationType.WARNING


def test_notification_service_mark_all_read(notification_service):
    """测试标记所有为已读"""
    notification_service.send_notification("通知1", "内容1")
    notification_service.send_notification("通知2", "内容2")
    notification_service.send_notification("通知3", "内容3")
    
    assert notification_service.get_unread_count() == 3
    
    count = notification_service.mark_all_as_read()
    assert count == 3
    assert notification_service.get_unread_count() == 0


# ============================================================================
# 测试：RuleEngine
# ============================================================================

def test_rule_engine_register_rule(rule_engine):
    """测试注册规则"""
    initial_count = len(rule_engine.rules)
    
    # 注册新规则
    new_rule = Rule(
        rule_id="TEST-RULE",
        name="测试规则",
        description="这是测试规则",
        event_type_pattern="test.event",
        action=lambda event, engine: None
    )
    rule_engine.register_rule(new_rule)
    
    assert len(rule_engine.rules) == initial_count + 1
    
    # 获取规则
    rule = rule_engine.get_rule("TEST-RULE")
    assert rule is not None
    assert rule.name == "测试规则"


def test_rule_engine_enable_disable(rule_engine):
    """测试启用/禁用规则"""
    # 禁用规则
    success = rule_engine.disable_rule("RULE-001")
    assert success is True
    
    rule = rule_engine.get_rule("RULE-001")
    assert rule.is_enabled is False
    
    # 启用规则
    success = rule_engine.enable_rule("RULE-001")
    assert success is True
    
    rule = rule_engine.get_rule("RULE-001")
    assert rule.is_enabled is True


@pytest.mark.asyncio
async def test_rule_engine_process_event(rule_engine, notification_service):
    """测试处理事件"""
    # 创建匹配规则的事件
    event = {
        "id": "EVT-test1",
        "project_id": "TEST_PROJECT",
        "event_type": "task.completed",
        "title": "任务完成测试",
        "related_entity_id": "TASK-001"
    }
    
    # 处理事件
    await rule_engine.process_event(event)
    
    # 检查通知是否被发送
    notifications = notification_service.get_notifications()
    assert len(notifications) > 0
    
    # 检查统计
    stats = rule_engine.get_stats()
    assert stats["total_events_processed"] == 1


def test_rule_matches_pattern():
    """测试规则模式匹配"""
    rule = Rule(
        rule_id="TEST",
        name="测试",
        description="测试",
        event_type_pattern="task.*",
        action=None
    )
    
    # 应该匹配
    event1 = {"event_type": "task.completed"}
    assert rule.matches(event1) is True
    
    event2 = {"event_type": "task.created"}
    assert rule.matches(event2) is True
    
    # 不应该匹配
    event3 = {"event_type": "issue.created"}
    assert rule.matches(event3) is False


# ============================================================================
# 测试：5个核心规则
# ============================================================================

@pytest.mark.asyncio
async def test_rule_task_completed(rule_engine, notification_service):
    """测试规则1: 任务完成"""
    event = {
        "id": "EVT-test1",
        "project_id": "TEST_PROJECT",
        "event_type": "task.completed",
        "title": "任务TASK-001完成",
        "related_entity_id": "TASK-001"
    }
    
    await rule_engine.process_event(event)
    
    # 检查通知
    notifications = notification_service.get_notifications()
    assert len(notifications) > 0
    assert "审查" in notifications[0]["message"]


@pytest.mark.asyncio
async def test_rule_feature_developed(rule_engine, notification_service):
    """测试规则2: 功能开发完成"""
    event = {
        "id": "EVT-test2",
        "project_id": "TEST_PROJECT",
        "event_type": "feature.developed",
        "title": "功能FEAT-001开发完成",
        "related_entity_id": "FEAT-001"
    }
    
    await rule_engine.process_event(event)
    
    # 检查通知
    notifications = notification_service.get_notifications()
    assert len(notifications) > 0
    assert "集成验证" in notifications[0]["message"]


@pytest.mark.asyncio
async def test_rule_task_approved(rule_engine, notification_service):
    """测试规则3: 任务审批通过"""
    event = {
        "id": "EVT-test3",
        "project_id": "TEST_PROJECT",
        "event_type": "task.approved",
        "title": "任务TASK-002审批通过",
        "related_entity_id": "TASK-002"
    }
    
    await rule_engine.process_event(event)
    
    # 检查通知
    notifications = notification_service.get_notifications()
    assert len(notifications) > 0
    assert "批准" in notifications[0]["message"]


@pytest.mark.asyncio
async def test_rule_issue_discovered(rule_engine, notification_service):
    """测试规则4: 问题发现"""
    event = {
        "id": "EVT-test4",
        "project_id": "TEST_PROJECT",
        "event_type": "issue.discovered",
        "title": "发现问题ISS-001",
        "related_entity_id": "ISS-001"
    }
    
    await rule_engine.process_event(event)
    
    # 检查通知
    notifications = notification_service.get_notifications()
    assert len(notifications) > 0
    assert "问题" in notifications[0]["message"]


@pytest.mark.asyncio
async def test_rule_task_rejected(rule_engine, notification_service):
    """测试规则5: 任务被拒绝"""
    event = {
        "id": "EVT-test5",
        "project_id": "TEST_PROJECT",
        "event_type": "task.rejected",
        "title": "任务TASK-003被拒绝",
        "description": "代码质量不符合标准",
        "related_entity_id": "TASK-003"
    }
    
    await rule_engine.process_event(event)
    
    # 检查通知
    notifications = notification_service.get_notifications()
    assert len(notifications) > 0
    assert "拒绝" in notifications[0]["message"] or "修改" in notifications[0]["message"]


# ============================================================================
# 测试：EventListener
# ============================================================================

def test_event_listener_initialization(event_listener):
    """测试监听器初始化"""
    assert event_listener.is_running is False
    assert event_listener.project_id == "TEST_PROJECT"
    assert event_listener.poll_interval == 1
    assert event_listener.rule_engine is not None
    assert event_listener.notification_service is not None


def test_event_listener_stats(event_listener):
    """测试获取统计信息"""
    stats = event_listener.get_stats()
    
    assert "total_polled" in stats
    assert "total_processed" in stats
    assert "total_errors" in stats
    assert "is_running" in stats
    assert "project_id" in stats
    assert stats["is_running"] is False


@pytest.mark.asyncio
async def test_event_listener_start_stop(event_listener):
    """测试启动和停止监听器"""
    # 启动监听器（后台任务）
    task = asyncio.create_task(event_listener.start())
    
    # 等待一小段时间
    await asyncio.sleep(0.5)
    
    # 检查是否运行
    assert event_listener.is_running is True
    
    # 停止监听器
    await event_listener.stop()
    
    # 等待任务完成
    await asyncio.sleep(0.5)
    
    # 检查是否停止
    assert event_listener.is_running is False
    
    # 取消任务
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


# ============================================================================
# 集成测试
# ============================================================================

@pytest.mark.asyncio
async def test_full_integration(event_store, event_emitter, event_listener, notification_service):
    """完整集成测试：发射事件 → 监听器处理 → 规则触发 → 通知发送"""
    # 1. 发射事件
    event = event_emitter.emit(
        project_id="TEST_PROJECT",
        event_type="task.completed",
        title="集成测试：任务完成",
        description="这是一个集成测试",
        category="task",
        source="system",
        related_entity_id="TASK-INTEGRATION"
    )
    
    assert event is not None
    
    # 2. 手动触发一次轮询和处理
    await event_listener._poll_and_process()
    
    # 3. 检查通知是否被创建
    notifications = notification_service.get_notifications()
    
    # 由于规则被触发，应该有通知
    assert len(notifications) > 0
    
    # 4. 检查监听器统计
    stats = event_listener.get_stats()
    assert stats["total_processed"] > 0


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

