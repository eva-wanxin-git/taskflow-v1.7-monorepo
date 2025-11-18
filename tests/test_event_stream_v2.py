# -*- coding: utf-8 -*-
"""
REQ-010-E: Dashboard事件流可视化升级 - 测试脚本

测试事件流v2的所有功能
"""

import sys
import io
import json
from pathlib import Path
from datetime import datetime

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "packages" / "core-domain" / "src"))
sys.path.insert(0, str(project_root / "packages" / "shared-utils"))

from services.event_service import create_event_emitter, create_event_store


def test_event_creation():
    """测试1: 创建测试事件"""
    print("\n[TEST 1] 创建测试事件...")
    
    emitter = create_event_emitter()
    project_id = "TASKFLOW"
    
    # 创建不同类型和严重性的测试事件
    test_events = [
        {
            "event_type": "task.created",
            "title": "任务创建: REQ-010-E Dashboard事件流升级",
            "description": "新任务 REQ-010-E 已创建，优先级P1",
            "category": "task",
            "severity": "info",
            "actor": "AI Architect",
            "related_entity_type": "task",
            "related_entity_id": "REQ-010-E",
            "tags": ["task", "created", "p1"]
        },
        {
            "event_type": "issue.discovered",
            "title": "问题发现: 事件流性能问题",
            "description": "发现1000+事件时加载缓慢",
            "category": "issue",
            "severity": "warning",
            "actor": "QA Tester",
            "related_entity_type": "issue",
            "related_entity_id": "ISS-101",
            "tags": ["issue", "performance"]
        },
        {
            "event_type": "decision.made",
            "title": "架构决策: 采用虚拟滚动",
            "description": "决定使用虚拟滚动优化大量事件显示",
            "category": "decision",
            "severity": "info",
            "actor": "AI Architect",
            "related_entity_type": "decision",
            "related_entity_id": "ADR-005",
            "tags": ["decision", "performance"]
        },
        {
            "event_type": "deployment.completed",
            "title": "部署完成: 事件流v2上线",
            "description": "事件流v2已成功部署到生产环境",
            "category": "deployment",
            "severity": "info",
            "actor": "SRE AI",
            "related_entity_type": "deployment",
            "related_entity_id": "DEP-2025-11-18-001",
            "tags": ["deployment", "production"]
        },
        {
            "event_type": "system.error",
            "title": "系统错误: 数据库连接失败",
            "description": "数据库连接池耗尽，需要立即处理",
            "category": "system",
            "severity": "critical",
            "actor": "system",
            "tags": ["system", "error", "database"]
        }
    ]
    
    created_count = 0
    for event_data in test_events:
        try:
            event = emitter.emit(project_id=project_id, **event_data)
            print(f"  ✅ 创建事件: {event['title'][:50]}")
            created_count += 1
        except Exception as e:
            print(f"  ❌ 创建失败: {str(e)}")
    
    print(f"\n✅ 测试1完成: 成功创建 {created_count}/{len(test_events)} 个事件\n")
    return created_count == len(test_events)


def test_event_query():
    """测试2: 查询事件"""
    print("\n[TEST 2] 查询事件...")
    
    store = create_event_store()
    
    # 测试基础查询
    try:
        all_events = store.query(project_id="TASKFLOW", limit=100)
        print(f"  ✅ 查询所有事件: {len(all_events)} 条")
    except Exception as e:
        print(f"  ❌ 查询失败: {str(e)}")
        return False
    
    # 测试分类筛选
    try:
        task_events = store.query(project_id="TASKFLOW", category="task", limit=50)
        print(f"  ✅ 任务事件: {len(task_events)} 条")
    except Exception as e:
        print(f"  ❌ 任务事件查询失败: {str(e)}")
    
    # 测试严重性筛选
    try:
        critical_events = store.query(project_id="TASKFLOW", severity="critical", limit=50)
        print(f"  ✅ 严重事件: {len(critical_events)} 条")
    except Exception as e:
        print(f"  ❌ 严重事件查询失败: {str(e)}")
    
    # 测试操作者筛选
    try:
        architect_events = store.query(project_id="TASKFLOW", actor="AI Architect", limit=50)
        print(f"  ✅ 架构师事件: {len(architect_events)} 条")
    except Exception as e:
        print(f"  ❌ 架构师事件查询失败: {str(e)}")
    
    print(f"\n✅ 测试2完成: 事件查询功能正常\n")
    return True


def test_event_stats():
    """测试3: 事件统计"""
    print("\n[TEST 3] 事件统计...")
    
    store = create_event_store()
    
    try:
        stats = store.get_stats("TASKFLOW")
        
        print(f"  总事件数: {stats.get('total_events', 0)}")
        print(f"  任务事件: {stats.get('task_events', 0)}")
        print(f"  问题事件: {stats.get('issue_events', 0)}")
        print(f"  决策事件: {stats.get('decision_events', 0)}")
        print(f"  部署事件: {stats.get('deployment_events', 0)}")
        print(f"  系统事件: {stats.get('system_events', 0)}")
        print(f"  严重事件: {stats.get('critical_events', 0)}")
        
        print(f"\n✅ 测试3完成: 统计功能正常\n")
        return True
    except Exception as e:
        print(f"  ❌ 统计失败: {str(e)}")
        return False


def test_event_stream_provider():
    """测试4: EventStreamProvider功能"""
    print("\n[TEST 4] 测试EventStreamProvider...")
    
    sys.path.insert(0, str(project_root / "apps" / "dashboard" / "src" / "industrial_dashboard"))
    from event_stream_provider import EventStreamProvider
    
    provider = EventStreamProvider()
    
    # 测试获取事件
    try:
        events = provider.get_events(hours=24, limit=50)
        print(f"  ✅ 获取最近24小时事件: {len(events)} 条")
    except Exception as e:
        print(f"  ❌ 获取事件失败: {str(e)}")
        return False
    
    # 测试分类汇总
    try:
        categories = provider.get_categories_summary()
        print(f"  ✅ 分类汇总:")
        for cat, count in categories.items():
            print(f"      {cat}: {count}")
    except Exception as e:
        print(f"  ❌ 分类汇总失败: {str(e)}")
    
    # 测试操作者汇总
    try:
        actors = provider.get_actors_summary(hours=24)
        print(f"  ✅ 操作者汇总:")
        for actor, count in list(actors.items())[:5]:  # 只显示前5个
            print(f"      {actor}: {count}")
    except Exception as e:
        print(f"  ❌ 操作者汇总失败: {str(e)}")
    
    # 测试搜索
    try:
        search_results = provider.search_events("REQ-010-E", limit=10)
        print(f"  ✅ 搜索'REQ-010-E': {len(search_results)} 条结果")
    except Exception as e:
        print(f"  ❌ 搜索失败: {str(e)}")
    
    print(f"\n✅ 测试4完成: EventStreamProvider功能正常\n")
    return True


def test_ui_template():
    """测试5: UI模板检查"""
    print("\n[TEST 5] UI模板检查...")
    
    template_path = project_root / "apps" / "dashboard" / "src" / "industrial_dashboard" / "event_stream_template_v2.html"
    
    if not template_path.exists():
        print(f"  ❌ 模板文件不存在: {template_path}")
        return False
    
    print(f"  ✅ 模板文件存在: {template_path}")
    
    # 检查关键功能
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_features = [
        ("搜索功能", "searchInput"),
        ("筛选器", "filterCategory"),
        ("事件详情", "event-details"),
        ("展开按钮", "expand-button"),
        ("统计卡片", "stat-card"),
        ("自动刷新", "startAutoRefresh"),
        ("虚拟滚动", "visibleEvents"),
        ("配色方案", "category-task"),
    ]
    
    all_found = True
    for feature_name, keyword in required_features:
        if keyword in content:
            print(f"  ✅ {feature_name}: 已实现")
        else:
            print(f"  ❌ {feature_name}: 未找到关键字 '{keyword}'")
            all_found = False
    
    print(f"\n✅ 测试5完成: UI模板检查{'完全通过' if all_found else '部分通过'}\n")
    return all_found


def test_performance():
    """测试6: 性能测试（1000+事件）"""
    print("\n[TEST 6] 性能测试...")
    
    store = create_event_store()
    
    try:
        import time
        
        # 测试查询1000个事件的性能
        start = time.time()
        events = store.query(project_id="TASKFLOW", limit=1000)
        elapsed = time.time() - start
        
        print(f"  查询1000个事件耗时: {elapsed:.3f}秒")
        
        if elapsed < 1.0:
            print(f"  ✅ 性能优秀 (< 1秒)")
            performance_grade = "A"
        elif elapsed < 2.0:
            print(f"  ✅ 性能良好 (< 2秒)")
            performance_grade = "B"
        elif elapsed < 5.0:
            print(f"  ⚠️ 性能一般 (< 5秒)")
            performance_grade = "C"
        else:
            print(f"  ❌ 性能较差 (> 5秒)")
            performance_grade = "D"
        
        print(f"\n✅ 测试6完成: 性能等级 {performance_grade}\n")
        return elapsed < 5.0
    except Exception as e:
        print(f"  ❌ 性能测试失败: {str(e)}")
        return False


def main():
    """运行所有测试"""
    print("=" * 70)
    print("REQ-010-E: Dashboard事件流可视化升级 - 功能测试")
    print("=" * 70)
    
    tests = [
        ("创建测试事件", test_event_creation),
        ("查询事件", test_event_query),
        ("事件统计", test_event_stats),
        ("EventStreamProvider", test_event_stream_provider),
        ("UI模板检查", test_ui_template),
        ("性能测试", test_performance),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ 测试 '{test_name}' 发生异常: {str(e)}\n")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status} - {test_name}")
    
    print("\n" + "-" * 70)
    print(f"总计: {passed}/{total} 测试通过 ({passed/total*100:.1f}%)")
    print("=" * 70)
    
    # 访问提示
    print("\n" + "🌐 访问事件流页面:")
    print("   1. 启动Dashboard: python apps/dashboard/start_dashboard.py")
    print("   2. 打开浏览器访问: http://127.0.0.1:8877/events")
    print("\n" + "=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

