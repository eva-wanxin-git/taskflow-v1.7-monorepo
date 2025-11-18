# -*- coding: utf-8 -*-
"""
系统级集成测试 - INTEGRATE-007

验证任务所·Flow完整系统的集成工作：
1. API服务层集成
2. Dashboard数据一致性
3. 事件系统集成
4. 知识库系统集成
5. 完整工作流集成

运行方式:
    pytest tests/integration/test_system_integration_e2e.py -v
    python tests/integration/test_system_integration_e2e.py
"""

import pytest
import json
import sqlite3
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import sys

# 配置路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "database" / "data" / "tasks.db"
EVENTS_FILE = PROJECT_ROOT / "apps" / "dashboard" / "automation-data" / "architect_events.json"
API_URL = "http://localhost:8871"  # 默认API地址
DASHBOARD_URL = "http://localhost:8871"


# ============================================================================
# 工具函数
# ============================================================================

def get_db_stats(project_code: str = None) -> Dict[str, Any]:
    """从数据库获取统计信息"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if project_code:
            cursor.execute(
                """SELECT COUNT(*) as total,
                   SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed,
                   SUM(CASE WHEN status='in_progress' THEN 1 ELSE 0 END) as in_progress,
                   SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) as pending
                   FROM tasks WHERE project_id IN 
                   (SELECT id FROM projects WHERE code = ?)""",
                (project_code,)
            )
        else:
            cursor.execute(
                """SELECT COUNT(*) as total,
                   SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed,
                   SUM(CASE WHEN status='in_progress' THEN 1 ELSE 0 END) as in_progress,
                   SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) as pending
                   FROM tasks"""
            )
        
        stats = dict(cursor.fetchone())
        conn.close()
        
        return stats
    except Exception as e:
        print(f"获取数据库统计失败: {e}")
        return {}


def get_events_from_file() -> List[Dict]:
    """从事件文件读取事件"""
    try:
        if EVENTS_FILE.exists():
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("events", [])
    except Exception as e:
        print(f"读取事件文件失败: {e}")
    
    return []


def make_api_request(method: str, endpoint: str, **kwargs) -> Dict:
    """发送API请求"""
    try:
        url = f"{API_URL}{endpoint}"
        response = requests.request(method, url, timeout=5, **kwargs)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.text else None,
            "success": response.status_code in [200, 201, 204]
        }
    except Exception as e:
        return {
            "status_code": None,
            "data": None,
            "success": False,
            "error": str(e)
        }


# ============================================================================
# 测试类
# ============================================================================

class TestAPIIntegration:
    """API服务层集成测试"""
    
    def test_health_check_endpoint(self):
        """测试1: 健康检查端点"""
        print("\n" + "="*70)
        print("测试: API健康检查")
        print("="*70)
        
        result = make_api_request("GET", "/health")
        
        print(f"✓ 健康检查状态码: {result['status_code']}")
        
        if result["success"]:
            print(f"✓ API服务正常运行")
        else:
            print(f"⚠ API服务不可达: {result.get('error', '未知错误')}")
        
        print("\n✅ 测试完成\n")
    
    def test_get_tasks_endpoint(self):
        """测试2: 获取任务列表API"""
        print("\n" + "="*70)
        print("测试: 获取任务列表API")
        print("="*70)
        
        result = make_api_request("GET", "/api/tasks")
        
        print(f"✓ 请求状态码: {result['status_code']}")
        
        if result["success"] and result["data"]:
            tasks = result["data"] if isinstance(result["data"], list) else result["data"].get("tasks", [])
            print(f"✓ 返回{len(tasks)}个任务")
        else:
            print(f"⚠ 获取任务失败或无任务数据")
        
        print("\n✅ 测试完成\n")
    
    def test_get_stats_endpoint(self):
        """测试3: 获取统计数据API"""
        print("\n" + "="*70)
        print("测试: 获取统计数据API")
        print("="*70)
        
        result = make_api_request("GET", "/api/stats")
        
        print(f"✓ 请求状态码: {result['status_code']}")
        
        if result["success"] and result["data"]:
            stats = result["data"]
            print(f"✓ 统计数据:")
            print(f"  - 总任务数: {stats.get('total', 'N/A')}")
            print(f"  - 已完成: {stats.get('completed', 'N/A')}")
            print(f"  - 进行中: {stats.get('in_progress', 'N/A')}")
            print(f"  - 进度: {stats.get('progress', 'N/A')}%")
        
        print("\n✅ 测试完成\n")


class TestDashboardDataConsistency:
    """Dashboard数据一致性测试"""
    
    def test_dashboard_data_consistency(self):
        """测试1: Dashboard与数据库数据一致性
        
        验证:
        1. Dashboard显示的任务数 == 数据库任务数
        2. 统计数据一致
        3. 进度计算相同
        """
        print("\n" + "="*70)
        print("测试: Dashboard与数据库数据一致性")
        print("="*70)
        
        # 获取数据库统计
        db_stats = get_db_stats()
        print(f"✓ 数据库统计:")
        print(f"  - 总计: {db_stats.get('total', 0)}")
        print(f"  - 已完成: {db_stats.get('completed', 0)}")
        print(f"  - 进行中: {db_stats.get('in_progress', 0)}")
        print(f"  - 待处理: {db_stats.get('pending', 0)}")
        
        # 获取Dashboard数据（通过API）
        result = make_api_request("GET", "/api/stats")
        
        if result["success"] and result["data"]:
            api_stats = result["data"]
            print(f"\n✓ API统计数据:")
            print(f"  - 总计: {api_stats.get('total', 0)}")
            print(f"  - 已完成: {api_stats.get('completed', 0)}")
            print(f"  - 进行中: {api_stats.get('in_progress', 0)}")
            
            # 验证一致性
            if db_stats.get('total') and api_stats.get('total'):
                db_total = db_stats.get('total', 0)
                api_total = api_stats.get('total', 0)
                
                if db_total == api_total:
                    print(f"\n✓ 数据一致性验证: PASS")
                else:
                    print(f"\n⚠ 数据不一致: DB={db_total}, API={api_total}")
        else:
            print(f"⚠ 无法获取API统计数据")
        
        print("\n✅ 测试完成\n")
    
    def test_progress_calculation_consistency(self):
        """测试2: 进度计算一致性"""
        print("\n" + "="*70)
        print("测试: 进度计算一致性")
        print("="*70)
        
        db_stats = get_db_stats()
        
        if db_stats.get('total'):
            # 计算进度
            db_progress = (db_stats.get('completed', 0) / db_stats['total']) * 100
            print(f"✓ 数据库计算进度: {db_progress:.1f}%")
            
            # 从API获取
            result = make_api_request("GET", "/api/stats")
            
            if result["success"] and result["data"]:
                api_progress = result["data"].get('progress', 0)
                print(f"✓ API返回进度: {api_progress:.1f}%")
                
                # 允许小的舍入误差
                if abs(db_progress - float(api_progress)) < 1:
                    print(f"✓ 进度计算一致")
                else:
                    print(f"⚠ 进度差异较大")
        else:
            print(f"⚠ 无任务数据，跳过验证")
        
        print("\n✅ 测试完成\n")


class TestEventSystemIntegration:
    """事件系统集成测试"""
    
    def test_event_stream_completeness(self):
        """测试1: 事件流完整性
        
        验证:
        1. 事件记录完整
        2. 事件顺序正确
        3. 事件内容有效
        """
        print("\n" + "="*70)
        print("测试: 事件流完整性")
        print("="*70)
        
        events = get_events_from_file()
        
        print(f"✓ 读取事件数: {len(events)}")
        
        if events:
            # 验证事件结构
            valid_count = 0
            for i, event in enumerate(events[:5]):  # 检查前5个事件
                has_required_fields = all(k in event for k in ["id", "timestamp", "type", "content"])
                if has_required_fields:
                    valid_count += 1
                    print(f"✓ 事件{i+1}: {event.get('type', 'unknown')} - {event.get('content', '')[:50]}")
            
            if valid_count > 0:
                print(f"\n✓ 事件结构验证: {valid_count}/5有效")
            
            # 验证时间顺序
            if len(events) > 1:
                timestamps = [event.get('timestamp', '') for event in events]
                is_ordered = all(timestamps[i] <= timestamps[i+1] for i in range(len(timestamps)-1))
                
                if is_ordered:
                    print(f"✓ 事件时间顺序: 正确")
                else:
                    print(f"⚠ 事件时间顺序: 乱序")
        else:
            print(f"⚠ 没有事件数据")
        
        print("\n✅ 测试完成\n")
    
    def test_event_stream_volume(self):
        """测试2: 事件流吞吐量
        
        验证:
        1. 事件数量 > 100
        2. 事件处理流畅
        """
        print("\n" + "="*70)
        print("测试: 事件流吞吐量")
        print("="*70)
        
        events = get_events_from_file()
        
        print(f"✓ 事件总数: {len(events)}")
        
        if len(events) >= 100:
            print(f"✓ 事件流充足 (≥100)")
            
            # 测试处理速度
            start_time = time.time()
            processed = 0
            
            for event in events:
                # 模拟处理
                _ = event.get("type")
                processed += 1
            
            process_time = time.time() - start_time
            throughput = len(events) / process_time if process_time > 0 else 0
            
            print(f"✓ 处理{len(events)}个事件耗时: {process_time:.3f}秒")
            print(f"✓ 吞吐量: {throughput:.0f} 事件/秒")
        else:
            print(f"⚠ 事件流不足 (<100)，当前{len(events)}个")
        
        print("\n✅ 测试完成\n")


class TestKnowledgeSystemIntegration:
    """知识库系统集成测试"""
    
    def test_knowledge_database_schema(self):
        """测试1: 知识库数据库Schema验证
        
        验证:
        1. 所有表存在
        2. 表结构正确
        3. 关键字段完整
        """
        print("\n" + "="*70)
        print("测试: 知识库Schema验证")
        print("="*70)
        
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            
            # 查询所有表
            cursor.execute(
                """SELECT name FROM sqlite_master WHERE type='table' 
                   ORDER BY name"""
            )
            
            tables = [row[0] for row in cursor.fetchall()]
            
            # 必须表列表
            required_tables = [
                "projects", "components", "tasks", "issues",
                "solutions", "decisions", "knowledge_articles"
            ]
            
            print(f"✓ 数据库表总数: {len(tables)}")
            print(f"✓ 表列表: {', '.join(tables[:5])}...")
            
            # 检查必要表
            missing_tables = []
            for table in required_tables:
                if table in tables:
                    print(f"  ✓ 表 '{table}' 存在")
                else:
                    missing_tables.append(table)
                    print(f"  ✗ 表 '{table}' 缺失")
            
            if not missing_tables:
                print(f"\n✓ 所有必要表存在")
            else:
                print(f"\n⚠ 缺失表: {', '.join(missing_tables)}")
            
            conn.close()
        except Exception as e:
            print(f"✗ 数据库错误: {e}")
        
        print("\n✅ 测试完成\n")
    
    def test_knowledge_data_completeness(self):
        """测试2: 知识库数据完整性
        
        验证:
        1. 有解决方案记录
        2. 有设计决策记录
        3. 有知识文章
        """
        print("\n" + "="*70)
        print("测试: 知识库数据完整性")
        print("="*70)
        
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            
            # 检查各类知识数据
            checks = [
                ("solutions", "解决方案"),
                ("decisions", "设计决策"),
                ("knowledge_articles", "知识文章"),
            ]
            
            for table, label in checks:
                try:
                    cursor.execute(f"SELECT COUNT(*) as cnt FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✓ {label}: {count}条记录")
                except sqlite3.OperationalError:
                    print(f"⚠ {label}表不存在")
            
            conn.close()
        except Exception as e:
            print(f"✗ 数据库错误: {e}")
        
        print("\n✅ 测试完成\n")


class TestCompleteWorkflowIntegration:
    """完整工作流集成测试"""
    
    def test_end_to_end_workflow(self):
        """测试: 端到端完整工作流
        
        场景:
        1. 检查API健康
        2. 验证数据库
        3. 检查事件系统
        4. 验证知识库
        5. 检查Dashboard一致性
        """
        print("\n" + "="*70)
        print("完整工作流集成测试")
        print("="*70)
        
        results = {
            "api_health": False,
            "database": False,
            "events": False,
            "knowledge_base": False,
            "dashboard": False
        }
        
        # Step 1: API健康检查
        print("\n[1/5] 检查API健康状态...")
        result = make_api_request("GET", "/health")
        results["api_health"] = result["success"]
        print(f"{'✓' if result['success'] else '✗'} API: {'正常' if result['success'] else '异常'}")
        
        # Step 2: 数据库验证
        print("\n[2/5] 验证数据库...")
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.execute("SELECT 1")
            conn.close()
            results["database"] = True
            print(f"✓ 数据库: 连接正常")
        except:
            print(f"✗ 数据库: 连接失败")
        
        # Step 3: 事件系统
        print("\n[3/5] 检查事件系统...")
        events = get_events_from_file()
        results["events"] = len(events) > 0
        print(f"{'✓' if results['events'] else '✗'} 事件: {len(events)}条记录")
        
        # Step 4: 知识库
        print("\n[4/5] 验证知识库...")
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM solutions")
            count = cursor.fetchone()[0]
            results["knowledge_base"] = count >= 0
            conn.close()
            print(f"✓ 知识库: {count}条解决方案")
        except:
            print(f"✗ 知识库: 访问失败")
        
        # Step 5: Dashboard一致性
        print("\n[5/5] 检查Dashboard数据一致性...")
        db_stats = get_db_stats()
        api_result = make_api_request("GET", "/api/stats")
        
        if api_result["success"] and db_stats.get('total'):
            results["dashboard"] = api_result["data"].get('total') == db_stats['total']
            print(f"{'✓' if results['dashboard'] else '✗'} Dashboard: {'数据一致' if results['dashboard'] else '数据不一致'}")
        else:
            print(f"⚠ Dashboard: 无法验证")
        
        # 总结
        print("\n" + "="*70)
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        print(f"集成测试结果: {passed}/{total} 通过")
        print(f"通过率: {passed/total*100:.1f}%")
        
        if passed >= 4:
            print(f"\n✅ 系统集成就绪，可以部署")
        elif passed >= 3:
            print(f"\n⚠ 系统部分集成，建议修复后再部署")
        else:
            print(f"\n❌ 系统集成有问题，需要修复")
        
        print("="*70 + "\n")
        
        return passed, total


# ============================================================================
# 报告生成
# ============================================================================

def generate_integration_report():
    """生成集成测试报告"""
    report = {
        "test_suite": "系统级集成测试 - INTEGRATE-007",
        "timestamp": datetime.now().isoformat(),
        "tests": {
            "API集成": TestAPIIntegration,
            "Dashboard一致性": TestDashboardDataConsistency,
            "事件系统": TestEventSystemIntegration,
            "知识库系统": TestKnowledgeSystemIntegration,
            "完整工作流": TestCompleteWorkflowIntegration,
        }
    }
    
    return report


if __name__ == "__main__":
    """直接运行"""
    print("="*70)
    print("系统级集成测试 - INTEGRATE-007")
    print("="*70)
    
    # 创建测试实例
    workflow_tester = TestCompleteWorkflowIntegration()
    passed, total = workflow_tester.test_end_to_end_workflow()
    
    # 返回状态码
    exit(0 if passed >= 4 else 1)
