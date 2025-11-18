# -*- coding: utf-8 -*-
"""
事件服务单元测试

测试EventEmitter和EventStore的核心功能
"""

import pytest
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
import tempfile
import os

# 添加packages路径到sys.path
packages_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "core-domain" / "src"
sys.path.insert(0, str(packages_path))

from services.event_service import (
    EventEmitter,
    EventStore,
    EventSeverity,
    EventCategory,
    EventSource,
    create_event_emitter,
    create_event_store
)


@pytest.fixture
def temp_db():
    """创建临时数据库用于测试"""
    # 创建临时数据库文件
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_events.db")
    
    # 创建数据库并初始化schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建project_events表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_events (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_category TEXT NOT NULL DEFAULT 'general',
            source TEXT NOT NULL DEFAULT 'system',
            actor TEXT,
            title TEXT NOT NULL,
            description TEXT,
            data TEXT,
            related_entity_type TEXT,
            related_entity_id TEXT,
            severity TEXT DEFAULT 'info',
            status TEXT DEFAULT 'processed',
            tags TEXT,
            occurred_at TEXT NOT NULL DEFAULT (datetime('now')),
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    
    # 创建event_types表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_types (
            id TEXT PRIMARY KEY,
            type_code TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            display_name TEXT NOT NULL,
            description TEXT,
            severity_default TEXT DEFAULT 'info',
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    
    # 创建event_stats表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_stats (
            project_id TEXT PRIMARY KEY,
            total_events INTEGER DEFAULT 0,
            events_today INTEGER DEFAULT 0,
            events_this_week INTEGER DEFAULT 0,
            events_this_month INTEGER DEFAULT 0,
            task_events INTEGER DEFAULT 0,
            issue_events INTEGER DEFAULT 0,
            decision_events INTEGER DEFAULT 0,
            deployment_events INTEGER DEFAULT 0,
            system_events INTEGER DEFAULT 0,
            info_events INTEGER DEFAULT 0,
            warning_events INTEGER DEFAULT 0,
            error_events INTEGER DEFAULT 0,
            critical_events INTEGER DEFAULT 0,
            last_event_at TEXT,
            last_updated TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    
    # 插入测试事件类型
    cursor.execute("""
        INSERT INTO event_types (id, type_code, category, display_name, description, severity_default)
        VALUES ('ET-01', 'task.created', 'task', '任务创建', '新任务被创建', 'info')
    """)
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    # 清理
    try:
        os.remove(db_path)
        os.rmdir(temp_dir)
    except:
        pass


@pytest.fixture
def event_store(temp_db):
    """创建EventStore实例"""
    return EventStore(db_path=temp_db)


@pytest.fixture
def event_emitter(event_store):
    """创建EventEmitter实例"""
    return EventEmitter(event_store=event_store)


# ============================================================================
# EventStore 测试
# ============================================================================

class TestEventStore:
    """EventStore测试类"""
    
    def test_save_event(self, event_store):
        """测试保存事件"""
        event = {
            "id": "EVT-test001",
            "project_id": "TASKFLOW",
            "event_type": "task.created",
            "event_category": EventCategory.TASK,
            "source": EventSource.SYSTEM,
            "actor": "test",
            "title": "测试事件",
            "description": "这是一个测试事件",
            "data": json.dumps({"key": "value"}),
            "related_entity_type": "task",
            "related_entity_id": "TASK-001",
            "severity": EventSeverity.INFO,
            "status": "processed",
            "tags": json.dumps(["test"]),
            "occurred_at": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        
        # 保存事件
        event_store.save(event)
        
        # 验证事件已保存
        saved_event = event_store.get_by_id("EVT-test001")
        assert saved_event is not None
        assert saved_event["title"] == "测试事件"
        assert saved_event["project_id"] == "TASKFLOW"
    
    def test_query_events_all(self, event_store, event_emitter):
        """测试查询所有事件"""
        # 创建多个测试事件
        for i in range(5):
            event_emitter.emit(
                project_id="TASKFLOW",
                event_type="task.created",
                title=f"测试事件{i}",
                category=EventCategory.TASK
            )
        
        # 查询所有事件
        events = event_store.query(project_id="TASKFLOW")
        assert len(events) == 5
    
    def test_query_events_by_type(self, event_store, event_emitter):
        """测试按类型查询事件"""
        # 创建不同类型的事件
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="task.created",
            title="任务事件",
            category=EventCategory.TASK
        )
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="issue.discovered",
            title="问题事件",
            category=EventCategory.ISSUE
        )
        
        # 查询task类型事件
        events = event_store.query(
            project_id="TASKFLOW",
            event_type="task.created"
        )
        assert len(events) == 1
        assert events[0]["event_type"] == "task.created"
    
    def test_query_events_by_category(self, event_store, event_emitter):
        """测试按分类查询事件"""
        # 创建不同分类的事件
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="task.created",
            title="任务事件",
            category=EventCategory.TASK
        )
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="issue.discovered",
            title="问题事件",
            category=EventCategory.ISSUE
        )
        
        # 查询task分类事件
        events = event_store.query(
            project_id="TASKFLOW",
            category=EventCategory.TASK
        )
        assert len(events) == 1
        assert events[0]["event_category"] == EventCategory.TASK
    
    def test_query_events_by_severity(self, event_store, event_emitter):
        """测试按严重性查询事件"""
        # 创建不同严重性的事件
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="task.created",
            title="普通事件",
            severity=EventSeverity.INFO
        )
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="system.error",
            title="错误事件",
            severity=EventSeverity.ERROR
        )
        
        # 查询error严重性事件
        events = event_store.query(
            project_id="TASKFLOW",
            severity=EventSeverity.ERROR
        )
        assert len(events) == 1
        assert events[0]["severity"] == EventSeverity.ERROR
    
    def test_query_events_pagination(self, event_store, event_emitter):
        """测试分页查询"""
        # 创建10个事件
        for i in range(10):
            event_emitter.emit(
                project_id="TASKFLOW",
                event_type="task.created",
                title=f"事件{i}"
            )
        
        # 第一页
        events_page1 = event_store.query(
            project_id="TASKFLOW",
            limit=5,
            offset=0
        )
        assert len(events_page1) == 5
        
        # 第二页
        events_page2 = event_store.query(
            project_id="TASKFLOW",
            limit=5,
            offset=5
        )
        assert len(events_page2) == 5
        
        # 验证不重复
        ids_page1 = set([e["id"] for e in events_page1])
        ids_page2 = set([e["id"] for e in events_page2])
        assert len(ids_page1.intersection(ids_page2)) == 0
    
    def test_get_stats(self, event_store, event_emitter):
        """测试获取统计"""
        # 创建不同类型和严重性的事件
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="task.created",
            title="任务1",
            category=EventCategory.TASK,
            severity=EventSeverity.INFO
        )
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="task.created",
            title="任务2",
            category=EventCategory.TASK,
            severity=EventSeverity.INFO
        )
        event_emitter.emit(
            project_id="TASKFLOW",
            event_type="issue.discovered",
            title="问题1",
            category=EventCategory.ISSUE,
            severity=EventSeverity.WARNING
        )
        
        # 获取统计
        stats = event_store.get_stats("TASKFLOW")
        assert stats["total_events"] == 3
        assert stats["task_events"] == 2
        assert stats["issue_events"] == 1
        assert stats["info_events"] == 2
        assert stats["warning_events"] == 1
    
    def test_get_event_types(self, event_store):
        """测试获取事件类型"""
        event_types = event_store.get_event_types()
        assert len(event_types) > 0
        assert event_types[0]["type_code"] == "task.created"


# ============================================================================
# EventEmitter 测试
# ============================================================================

class TestEventEmitter:
    """EventEmitter测试类"""
    
    def test_emit_event(self, event_emitter, event_store):
        """测试发射事件"""
        event = event_emitter.emit(
            project_id="TASKFLOW",
            event_type="task.created",
            title="测试任务创建",
            description="这是一个测试",
            category=EventCategory.TASK,
            source=EventSource.AI,
            actor="AI Architect",
            severity=EventSeverity.INFO
        )
        
        assert event["id"].startswith("EVT-")
        assert event["title"] == "测试任务创建"
        assert event["project_id"] == "TASKFLOW"
        
        # 验证已保存到数据库
        saved_event = event_store.get_by_id(event["id"])
        assert saved_event is not None
    
    def test_emit_batch_events(self, event_emitter, event_store):
        """测试批量发射事件"""
        events_data = [
            {
                "event_type": "task.created",
                "title": "任务1",
                "category": EventCategory.TASK
            },
            {
                "event_type": "task.created",
                "title": "任务2",
                "category": EventCategory.TASK
            },
            {
                "event_type": "task.created",
                "title": "任务3",
                "category": EventCategory.TASK
            }
        ]
        
        events = event_emitter.emit_batch(
            project_id="TASKFLOW",
            events=events_data
        )
        
        assert len(events) == 3
        
        # 验证所有事件都已保存
        for event in events:
            saved_event = event_store.get_by_id(event["id"])
            assert saved_event is not None
    
    def test_emit_task_created_convenience(self, event_emitter, event_store):
        """测试便捷方法：任务创建"""
        event = event_emitter.emit_task_created(
            project_id="TASKFLOW",
            task_id="TASK-001",
            task_title="实现事件系统",
            actor="AI Architect"
        )
        
        assert event["event_type"] == "task.created"
        assert event["related_entity_id"] == "TASK-001"
        assert event["actor"] == "AI Architect"
    
    def test_emit_task_completed_convenience(self, event_emitter, event_store):
        """测试便捷方法：任务完成"""
        event = event_emitter.emit_task_completed(
            project_id="TASKFLOW",
            task_id="TASK-001",
            task_title="实现事件系统",
            actor="fullstack-engineer"
        )
        
        assert event["event_type"] == "task.completed"
        assert event["related_entity_id"] == "TASK-001"
        assert event["actor"] == "fullstack-engineer"
    
    def test_emit_issue_discovered_convenience(self, event_emitter, event_store):
        """测试便捷方法：问题发现"""
        event = event_emitter.emit_issue_discovered(
            project_id="TASKFLOW",
            issue_id="ISS-001",
            issue_title="API响应慢",
            severity=EventSeverity.ERROR
        )
        
        assert event["event_type"] == "issue.discovered"
        assert event["related_entity_id"] == "ISS-001"
        assert event["severity"] == EventSeverity.ERROR
    
    def test_emit_decision_made_convenience(self, event_emitter, event_store):
        """测试便捷方法：决策制定"""
        event = event_emitter.emit_decision_made(
            project_id="TASKFLOW",
            decision_id="DEC-001",
            decision_title="采用Monorepo架构",
            actor="AI Architect"
        )
        
        assert event["event_type"] == "decision.made"
        assert event["related_entity_id"] == "DEC-001"
        assert event["actor"] == "AI Architect"


# ============================================================================
# 集成测试
# ============================================================================

class TestEventSystemIntegration:
    """事件系统集成测试"""
    
    def test_full_workflow(self, event_emitter, event_store):
        """测试完整工作流"""
        # 1. 发射多个事件
        event_emitter.emit_task_created(
            project_id="TASKFLOW",
            task_id="TASK-001",
            task_title="任务1"
        )
        event_emitter.emit_task_created(
            project_id="TASKFLOW",
            task_id="TASK-002",
            task_title="任务2"
        )
        event_emitter.emit_issue_discovered(
            project_id="TASKFLOW",
            issue_id="ISS-001",
            issue_title="问题1",
            severity=EventSeverity.ERROR
        )
        
        # 2. 查询所有事件
        all_events = event_store.query(project_id="TASKFLOW")
        assert len(all_events) == 3
        
        # 3. 查询任务事件
        task_events = event_store.query(
            project_id="TASKFLOW",
            category=EventCategory.TASK
        )
        assert len(task_events) == 2
        
        # 4. 查询错误事件
        error_events = event_store.query(
            project_id="TASKFLOW",
            severity=EventSeverity.ERROR
        )
        assert len(error_events) == 1
        
        # 5. 获取统计
        stats = event_store.get_stats("TASKFLOW")
        assert stats["total_events"] == 3
        assert stats["task_events"] == 2
        assert stats["issue_events"] == 1
        assert stats["error_events"] == 1
    
    def test_event_with_data_and_tags(self, event_emitter, event_store):
        """测试带数据和标签的事件"""
        event = event_emitter.emit(
            project_id="TASKFLOW",
            event_type="deployment.completed",
            title="部署完成",
            description="v1.7部署成功",
            data={
                "version": "v1.7",
                "environment": "production",
                "duration": "120s"
            },
            category=EventCategory.DEPLOYMENT,
            tags=["deployment", "production", "success"]
        )
        
        # 验证数据和标签
        saved_event = event_store.get_by_id(event["id"])
        assert saved_event["data"]["version"] == "v1.7"
        assert "deployment" in saved_event["tags"]


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

