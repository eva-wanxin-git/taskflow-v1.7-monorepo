#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REQ-010-C 测试脚本: 事件触发集成测试

验证所有脚本和API端点的事件触发功能
"""
import sys
import io
import sqlite3
import json
from pathlib import Path
from datetime import datetime

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加packages路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "packages" / "shared-utils"))
sys.path.insert(0, str(project_root / "packages" / "core-domain" / "src"))

from event_helper import create_event_helper
from services.event_service import EventStore

DB_PATH = project_root / "database" / "data" / "tasks.db"

class EventIntegrationTest:
    """事件集成测试类"""
    
    def __init__(self):
        self.event_helper = create_event_helper(
            project_id="TASKFLOW",
            actor="test_system",
            source="system"
        )
        self.event_store = EventStore(db_path=str(DB_PATH))
        self.test_task_id = f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
    def setup_test_task(self):
        """创建测试任务"""
        print("=" * 70)
        print("1. 创建测试任务")
        print("=" * 70)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO tasks (id, title, description, status, priority, estimated_hours, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.test_task_id,
                "测试任务 - 事件集成",
                "用于验证事件触发功能的测试任务",
                "pending",
                "P0",
                2.0,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✓ 测试任务已创建: {self.test_task_id}")
            return True
            
        except Exception as e:
            print(f"✗ 创建测试任务失败: {e}")
            return False
    
    def test_task_created_event(self):
        """测试 task_created 事件"""
        print("\n" + "=" * 70)
        print("2. 测试 task_created 事件")
        print("=" * 70)
        
        try:
            event = self.event_helper.task_created(
                task_id=self.test_task_id,
                title="测试任务 - 事件集成",
                priority="P0",
                assigned_to="test_engineer",
                estimated_hours=2.0
            )
            
            print(f"✓ task_created 事件已触发")
            print(f"  - 事件ID: {event['id']}")
            print(f"  - 事件类型: {event['event_type']}")
            print(f"  - 事件标题: {event['title']}")
            
            return True
            
        except Exception as e:
            print(f"✗ task_created 事件触发失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_task_dispatched_event(self):
        """测试 task_dispatched 事件"""
        print("\n" + "=" * 70)
        print("3. 测试 task_dispatched 事件")
        print("=" * 70)
        
        try:
            event = self.event_helper.task_dispatched(
                task_id=self.test_task_id,
                assigned_to="fullstack-engineer",
                reason="自动分配测试"
            )
            
            print(f"✓ task_dispatched 事件已触发")
            print(f"  - 事件ID: {event['id']}")
            print(f"  - 事件类型: {event['event_type']}")
            print(f"  - 派发给: fullstack-engineer")
            
            return True
            
        except Exception as e:
            print(f"✗ task_dispatched 事件触发失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_task_started_event(self):
        """测试 task_started 事件"""
        print("\n" + "=" * 70)
        print("4. 测试 task_started 事件")
        print("=" * 70)
        
        try:
            event = self.event_helper.task_started(
                task_id=self.test_task_id,
                actor="test_engineer",
                work_plan="1. 准备环境 2. 执行测试 3. 验证结果"
            )
            
            print(f"✓ task_started 事件已触发")
            print(f"  - 事件ID: {event['id']}")
            print(f"  - 事件类型: {event['event_type']}")
            print(f"  - 执行者: test_engineer")
            
            return True
            
        except Exception as e:
            print(f"✗ task_started 事件触发失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_task_completed_event(self):
        """测试 task_completed 事件"""
        print("\n" + "=" * 70)
        print("5. 测试 task_completed 事件")
        print("=" * 70)
        
        try:
            event = self.event_helper.task_completed(
                task_id=self.test_task_id,
                actor="test_engineer",
                actual_hours=1.5,
                files_modified=["test_file1.py", "test_file2.py"],
                completion_summary="测试完成，所有验证通过"
            )
            
            print(f"✓ task_completed 事件已触发")
            print(f"  - 事件ID: {event['id']}")
            print(f"  - 事件类型: {event['event_type']}")
            print(f"  - 实际工时: 1.5小时")
            
            return True
            
        except Exception as e:
            print(f"✗ task_completed 事件触发失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_task_approved_event(self):
        """测试 task_approved 事件"""
        print("\n" + "=" * 70)
        print("6. 测试 task_approved 事件")
        print("=" * 70)
        
        try:
            event = self.event_helper.task_approved(
                task_id=self.test_task_id,
                reviewer="test_architect",
                score=95,
                feedback="测试完成度高，质量优秀"
            )
            
            print(f"✓ task_approved 事件已触发")
            print(f"  - 事件ID: {event['id']}")
            print(f"  - 事件类型: {event['event_type']}")
            print(f"  - 审查评分: 95/100")
            
            return True
            
        except Exception as e:
            print(f"✗ task_approved 事件触发失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_feature_integrated_event(self):
        """测试 feature_integrated 事件"""
        print("\n" + "=" * 70)
        print("7. 测试 feature_integrated 事件")
        print("=" * 70)
        
        try:
            event = self.event_helper.feature_integrated(
                feature_id=self.test_task_id,
                component="api",
                description="测试功能已集成到API模块",
                version="v1.7.0"
            )
            
            print(f"✓ feature_integrated 事件已触发")
            print(f"  - 事件ID: {event['id']}")
            print(f"  - 事件类型: {event['event_type']}")
            print(f"  - 集成组件: api")
            
            return True
            
        except Exception as e:
            print(f"✗ feature_integrated 事件触发失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def verify_events_in_database(self):
        """验证事件已保存到数据库"""
        print("\n" + "=" * 70)
        print("8. 验证事件数据库记录")
        print("=" * 70)
        
        try:
            # 查询所有与测试任务相关的事件
            events = self.event_store.query(
                project_id="TASKFLOW",
                related_entity_type="task",
                related_entity_id=self.test_task_id
            )
            
            print(f"✓ 找到 {len(events)} 条相关事件记录")
            
            # 按事件类型统计
            event_types = {}
            for event in events:
                event_type = event['event_type']
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            print("\n事件类型统计:")
            for event_type, count in sorted(event_types.items()):
                print(f"  - {event_type}: {count} 条")
            
            # 验证必需的事件类型
            required_events = [
                "task.created",
                "task.dispatched", 
                "task.started",
                "task.completed",
                "task.approved"
            ]
            
            missing_events = []
            for required in required_events:
                if required not in event_types:
                    missing_events.append(required)
            
            if missing_events:
                print(f"\n⚠ 缺少以下事件类型: {', '.join(missing_events)}")
                return False
            else:
                print(f"\n✓ 所有必需事件类型都已记录")
                return True
            
        except Exception as e:
            print(f"✗ 验证事件失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def cleanup_test_task(self):
        """清理测试任务"""
        print("\n" + "=" * 70)
        print("9. 清理测试数据")
        print("=" * 70)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # 删除测试任务
            cursor.execute("DELETE FROM tasks WHERE id = ?", (self.test_task_id,))
            
            # 删除测试事件（如果需要）
            # 注意: 实际生产中可能不想删除事件历史
            cursor.execute("""
                DELETE FROM project_events 
                WHERE related_entity_type = 'task' 
                AND related_entity_id = ?
            """, (self.test_task_id,))
            
            conn.commit()
            conn.close()
            
            print(f"✓ 测试任务已删除: {self.test_task_id}")
            print(f"✓ 相关事件已删除")
            return True
            
        except Exception as e:
            print(f"⚠ 清理测试数据失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n")
        print("=" * 70)
        print("REQ-010-C 事件触发集成测试")
        print("=" * 70)
        print()
        
        results = []
        
        # 创建测试任务
        if not self.setup_test_task():
            print("\n✗ 测试失败: 无法创建测试任务")
            return False
        
        # 运行所有事件测试
        results.append(("task_created", self.test_task_created_event()))
        results.append(("task_dispatched", self.test_task_dispatched_event()))
        results.append(("task_started", self.test_task_started_event()))
        results.append(("task_completed", self.test_task_completed_event()))
        results.append(("task_approved", self.test_task_approved_event()))
        results.append(("feature_integrated", self.test_feature_integrated_event()))
        
        # 验证数据库
        results.append(("database_verification", self.verify_events_in_database()))
        
        # 清理测试数据
        self.cleanup_test_task()
        
        # 汇总结果
        print("\n" + "=" * 70)
        print("测试结果汇总")
        print("=" * 70)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status} - {test_name}")
        
        print()
        print(f"通过率: {passed}/{total} ({passed*100//total}%)")
        
        if passed == total:
            print("\n✅ 所有测试通过！事件触发功能正常！")
            return True
        else:
            print(f"\n⚠ {total - passed} 个测试失败")
            return False


def main():
    """主函数"""
    tester = EventIntegrationTest()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

