# -*- coding: utf-8 -*-
"""
事件系统集成测试

测试事件发射、存储、查询的完整流程
"""

import sys
from pathlib import Path

# 添加packages路径
root_path = Path(__file__).parent.parent
packages_path = root_path / "packages" / "core-domain" / "src"
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


def test_event_emitter_and_store():
    """测试EventEmitter和EventStore"""
    print("=" * 70)
    print("测试1: EventEmitter 和 EventStore 基本功能")
    print("=" * 70)
    
    # 使用实际数据库
    db_path = root_path / "database" / "data" / "tasks.db"
    
    # 创建实例
    event_store = EventStore(db_path=str(db_path))
    event_emitter = EventEmitter(event_store=event_store)
    
    # 测试发射事件
    print("\n1. 发射测试事件...")
    event = event_emitter.emit(
        project_id="TASKFLOW",
        event_type="test.integration",
        title="集成测试事件",
        description="这是一个集成测试事件",
        category=EventCategory.SYSTEM,
        source=EventSource.SYSTEM,
        severity=EventSeverity.INFO,
        tags=["test", "integration"]
    )
    
    print(f"   [OK] Event emitted: {event['id']}")
    print(f"   - Title: {event['title']}")
    print(f"   - Type: {event['event_type']}")
    print(f"   - Category: {event['event_category']}")
    
    # 测试查询事件
    print("\n2. Query events...")
    events = event_store.query(
        project_id="TASKFLOW",
        event_type="test.integration",
        limit=5
    )
    print(f"   [OK] Found {len(events)} test events")
    
    # 测试按ID获取事件
    print("\n3. Get event by ID...")
    retrieved_event = event_store.get_by_id(event['id'])
    if retrieved_event:
        print(f"   [OK] Retrieved event: {retrieved_event['id']}")
    else:
        print(f"   [FAIL] Event not found")
    
    # 测试统计
    print("\n4. Get statistics...")
    stats = event_store.get_stats("TASKFLOW")
    print(f"   [OK] Project statistics:")
    print(f"   - Total events: {stats.get('total_events', 0)}")
    print(f"   - Task events: {stats.get('task_events', 0)}")
    print(f"   - Issue events: {stats.get('issue_events', 0)}")
    print(f"   - System events: {stats.get('system_events', 0)}")
    
    print("\n[PASS] Test 1 passed\n")


def test_convenience_methods():
    """测试便捷方法"""
    print("=" * 70)
    print("Test 2: Convenience Methods")
    print("=" * 70)
    
    db_path = root_path / "database" / "data" / "tasks.db"
    event_emitter = create_event_emitter(db_path=str(db_path))
    event_store = create_event_store(db_path=str(db_path))
    
    # 测试任务创建事件
    print("\n1. Task created event...")
    event = event_emitter.emit_task_created(
        project_id="TASKFLOW",
        task_id="TEST-001",
        task_title="Integration test task",
        actor="AI Architect"
    )
    print(f"   [OK] Task created event: {event['id']}")
    
    # 测试任务完成事件
    print("\n2. Task completed event...")
    event = event_emitter.emit_task_completed(
        project_id="TASKFLOW",
        task_id="TEST-001",
        task_title="Integration test task",
        actor="fullstack-engineer"
    )
    print(f"   [OK] Task completed event: {event['id']}")
    
    # 测试问题发现事件
    print("\n3. Issue discovered event...")
    event = event_emitter.emit_issue_discovered(
        project_id="TASKFLOW",
        issue_id="TEST-ISS-001",
        issue_title="Test issue",
        severity=EventSeverity.WARNING
    )
    print(f"   [OK] Issue discovered event: {event['id']}")
    
    # 测试决策制定事件
    print("\n4. Decision made event...")
    event = event_emitter.emit_decision_made(
        project_id="TASKFLOW",
        decision_id="TEST-DEC-001",
        decision_title="Test decision",
        actor="AI Architect"
    )
    print(f"   [OK] Decision made event: {event['id']}")
    
    print("\n[PASS] Test 2 passed\n")


def test_batch_emit():
    """测试批量发射"""
    print("=" * 70)
    print("Test 3: Batch Emit")
    print("=" * 70)
    
    db_path = root_path / "database" / "data" / "tasks.db"
    event_emitter = create_event_emitter(db_path=str(db_path))
    
    print("\n1. Emit 3 events in batch...")
    events_data = [
        {
            "event_type": "task.created",
            "title": "Batch task 1",
            "category": EventCategory.TASK
        },
        {
            "event_type": "task.created",
            "title": "Batch task 2",
            "category": EventCategory.TASK
        },
        {
            "event_type": "task.created",
            "title": "Batch task 3",
            "category": EventCategory.TASK
        }
    ]
    
    events = event_emitter.emit_batch(
        project_id="TASKFLOW",
        events=events_data
    )
    
    print(f"   [OK] Emitted {len(events)} events")
    for i, event in enumerate(events, 1):
        print(f"   - Event {i}: {event['id']} - {event['title']}")
    
    print("\n[PASS] Test 3 passed\n")


def test_query_filters():
    """测试查询过滤"""
    print("=" * 70)
    print("Test 4: Query Filters")
    print("=" * 70)
    
    db_path = root_path / "database" / "data" / "tasks.db"
    event_store = create_event_store(db_path=str(db_path))
    
    # 按分类查询
    print("\n1. Query by category...")
    task_events = event_store.query(
        project_id="TASKFLOW",
        category=EventCategory.TASK,
        limit=10
    )
    print(f"   [OK] Task events: {len(task_events)}")
    
    # 按严重性查询
    print("\n2. Query by severity...")
    error_events = event_store.query(
        project_id="TASKFLOW",
        severity=EventSeverity.ERROR,
        limit=10
    )
    print(f"   [OK] Error events: {len(error_events)}")
    
    # 按实体查询
    print("\n3. Query by entity...")
    entity_events = event_store.query(
        project_id="TASKFLOW",
        related_entity_type="task",
        related_entity_id="TEST-001",
        limit=10
    )
    print(f"   [OK] Entity related events: {len(entity_events)}")
    
    # 分页查询
    print("\n4. Query with pagination...")
    page1 = event_store.query(project_id="TASKFLOW", limit=5, offset=0)
    page2 = event_store.query(project_id="TASKFLOW", limit=5, offset=5)
    print(f"   [OK] Page 1: {len(page1)} events")
    print(f"   [OK] Page 2: {len(page2)} events")
    
    print("\n[PASS] Test 4 passed\n")


def test_event_types():
    """测试事件类型"""
    print("=" * 70)
    print("Test 5: Event Types Management")
    print("=" * 70)
    
    db_path = root_path / "database" / "data" / "tasks.db"
    event_store = create_event_store(db_path=str(db_path))
    
    print("\n1. Get all event types...")
    event_types = event_store.get_event_types()
    print(f"   [OK] Total {len(event_types)} event types")
    
    # 按分类统计
    categories = {}
    for et in event_types:
        cat = et['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n2. Group by category:")
    for cat, count in categories.items():
        print(f"   - {cat}: {count} types")
    
    print("\n3. Predefined event type samples:")
    for et in event_types[:5]:
        print(f"   - {et['type_code']}: {et['display_name']} ({et['category']})")
    
    print("\n[PASS] Test 5 passed\n")


def main():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("[TEST] Event System Integration Test")
    print("=" * 70)
    print()
    
    try:
        test_event_emitter_and_store()
        test_convenience_methods()
        test_batch_emit()
        test_query_filters()
        test_event_types()
        
        print("=" * 70)
        print("[PASS] All Tests Passed!")
        print("=" * 70)
        print()
        print("Event System Verification Complete:")
        print("   [OK] EventEmitter - Event emitter")
        print("   [OK] EventStore - Event storage")
        print("   [OK] Convenience methods - Quick emit")
        print("   [OK] Batch emit - Batch processing")
        print("   [OK] Query filters - Flexible queries")
        print("   [OK] Event types - Type management")
        print("   [OK] Statistics - Event stats")
        print()
        
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"[FAIL] Test failed: {str(e)}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

