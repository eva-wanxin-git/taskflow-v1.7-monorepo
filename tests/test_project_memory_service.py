# -*- coding: utf-8 -*-
"""
项目记忆服务单元测试
"""

import unittest
from datetime import datetime
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core-domain" / "src"))

from services.project_memory_service import (
    ProjectMemoryService,
    MemoryType,
    MemoryCategory,
    RelationType,
    create_project_memory_service
)


class TestProjectMemoryService(unittest.TestCase):
    """测试项目记忆服务"""
    
    def setUp(self):
        """测试前准备"""
        # 创建服务实例（不连接真实数据库和外部服务）
        self.service = create_project_memory_service(
            state_manager=None,
            session_memory_enabled=False,
            ultra_memory_enabled=False
        )
        self.project_id = "TEST_PROJECT"
    
    def test_create_memory_basic(self):
        """测试基础记忆创建"""
        memory = self.service.create_memory(
            project_id=self.project_id,
            memory_type=MemoryType.KNOWLEDGE,
            category=MemoryCategory.KNOWLEDGE,
            title="测试记忆",
            content="这是一个测试记忆",
            importance=5
        )
        
        self.assertIsNotNone(memory)
        self.assertEqual(memory["project_id"], self.project_id)
        self.assertEqual(memory["title"], "测试记忆")
        self.assertIn("id", memory)
        self.assertTrue(memory["id"].startswith("MEM-"))
    
    def test_create_memory_with_tags(self):
        """测试带标签的记忆创建"""
        memory = self.service.create_memory(
            project_id=self.project_id,
            memory_type=MemoryType.ULTRA,
            category=MemoryCategory.KNOWLEDGE,
            title="Python最佳实践",
            content="使用类型提示提高代码质量",
            tags=["python", "best-practice", "typing"],
            importance=7
        )
        
        self.assertIsNotNone(memory)
        self.assertIn("tags", memory)
    
    def test_create_memory_with_relations(self):
        """测试带关联的记忆创建"""
        memory = self.service.create_memory(
            project_id=self.project_id,
            memory_type=MemoryType.SOLUTION,
            category=MemoryCategory.SOLUTION,
            title="解决方案",
            content="使用缓存优化性能",
            related_tasks=["TASK-001", "TASK-002"],
            related_issues=["ISS-001"],
            importance=8
        )
        
        self.assertIsNotNone(memory)
        self.assertIn("related_tasks", memory)
        self.assertIn("related_issues", memory)
    
    def test_auto_record_architecture_decision(self):
        """测试自动记录架构决策"""
        memory = self.service.auto_record_architecture_decision(
            project_id=self.project_id,
            title="采用微服务架构",
            context="系统规模扩大，单体架构难以维护",
            decision="拆分为多个微服务，使用API网关",
            consequences="提高可扩展性，增加运维复杂度",
            alternatives=["保持单体", "服务化但不完全分离"],
            decided_by="架构师AI"
        )
        
        self.assertIsNotNone(memory)
        self.assertEqual(memory["category"], MemoryCategory.DECISION)
        self.assertIn("ADR:", memory["title"])
        self.assertIn("context", memory)
    
    def test_auto_record_problem_solution(self):
        """测试自动记录问题解决方案"""
        result = self.service.auto_record_problem_solution(
            project_id=self.project_id,
            problem_title="内存泄漏",
            problem_description="长时间运行后内存持续增长",
            solution_title="修复事件监听器泄漏",
            solution_description="在组件卸载时移除事件监听",
            solution_steps=["定位泄漏代码", "添加清理逻辑", "验证修复"],
            tools_used=["Chrome DevTools", "memory-profiler"],
            severity="high"
        )
        
        self.assertIsNotNone(result)
        self.assertIn("problem_memory", result)
        self.assertIn("solution_memory", result)
        self.assertTrue(result["relation_created"])
    
    def test_create_memory_relation(self):
        """测试创建记忆关系"""
        # 创建两个记忆
        mem1 = self.service.create_memory(
            project_id=self.project_id,
            memory_type=MemoryType.KNOWLEDGE,
            category=MemoryCategory.PROBLEM,
            title="问题A",
            content="问题描述"
        )
        
        mem2 = self.service.create_memory(
            project_id=self.project_id,
            memory_type=MemoryType.KNOWLEDGE,
            category=MemoryCategory.SOLUTION,
            title="解决方案A",
            content="解决方案描述"
        )
        
        # 创建关系
        relation = self.service.create_memory_relation(
            source_memory_id=mem2["id"],
            target_memory_id=mem1["id"],
            relation_type=RelationType.SOLVED_BY,
            strength=1.0
        )
        
        self.assertIsNotNone(relation)
        self.assertEqual(relation["source_memory_id"], mem2["id"])
        self.assertEqual(relation["target_memory_id"], mem1["id"])
        self.assertEqual(relation["relation_type"], RelationType.SOLVED_BY)
    
    def test_inherit_knowledge(self):
        """测试知识继承"""
        # 先创建一些记忆
        self.service.create_memory(
            project_id=self.project_id,
            memory_type=MemoryType.ULTRA,
            category=MemoryCategory.DECISION,
            title="决策1",
            content="决策内容",
            importance=8
        )
        
        self.service.create_memory(
            project_id=self.project_id,
            memory_type=MemoryType.ULTRA,
            category=MemoryCategory.SOLUTION,
            title="解决方案1",
            content="方案内容",
            importance=7
        )
        
        # 测试知识继承
        knowledge_package = self.service.inherit_knowledge(
            project_id=self.project_id,
            context="开始新任务",
            limit=20
        )
        
        self.assertIsNotNone(knowledge_package)
        self.assertEqual(knowledge_package["project_id"], self.project_id)
        self.assertIn("decisions", knowledge_package)
        self.assertIn("solutions", knowledge_package)
        self.assertIn("important_knowledge", knowledge_package)
        self.assertIn("recent_memories", knowledge_package)
    
    def test_memory_type_constants(self):
        """测试记忆类型常量"""
        self.assertEqual(MemoryType.SESSION, "session")
        self.assertEqual(MemoryType.ULTRA, "ultra")
        self.assertEqual(MemoryType.DECISION, "decision")
        self.assertEqual(MemoryType.SOLUTION, "solution")
    
    def test_memory_category_constants(self):
        """测试记忆分类常量"""
        self.assertEqual(MemoryCategory.ARCHITECTURE, "architecture")
        self.assertEqual(MemoryCategory.PROBLEM, "problem")
        self.assertEqual(MemoryCategory.SOLUTION, "solution")
        self.assertEqual(MemoryCategory.DECISION, "decision")
    
    def test_relation_type_constants(self):
        """测试关系类型常量"""
        self.assertEqual(RelationType.RELATED, "related")
        self.assertEqual(RelationType.SOLVED_BY, "solved-by")
        self.assertEqual(RelationType.CAUSED_BY, "caused-by")
        self.assertEqual(RelationType.EVOLVED_FROM, "evolved-from")


class TestMemoryFormatting(unittest.TestCase):
    """测试记忆格式化功能"""
    
    def setUp(self):
        """测试前准备"""
        self.service = create_project_memory_service(
            state_manager=None,
            session_memory_enabled=False,
            ultra_memory_enabled=False
        )
    
    def test_format_adr(self):
        """测试ADR格式化"""
        adr_content = self.service._format_adr(
            title="采用TypeScript",
            context="JavaScript项目类型安全问题频发",
            decision="全面采用TypeScript替代JavaScript",
            consequences="提高代码质量，增加学习成本",
            alternatives=["Flow", "JSDoc"]
        )
        
        self.assertIsNotNone(adr_content)
        self.assertIn("# ADR:", adr_content)
        self.assertIn("## 背景", adr_content)
        self.assertIn("## 决策", adr_content)
        self.assertIn("## 影响", adr_content)
        self.assertIn("## 备选方案", adr_content)
    
    def test_severity_to_importance(self):
        """测试严重性到重要性的转换"""
        self.assertEqual(self.service._severity_to_importance("critical"), 10)
        self.assertEqual(self.service._severity_to_importance("high"), 8)
        self.assertEqual(self.service._severity_to_importance("medium"), 5)
        self.assertEqual(self.service._severity_to_importance("low"), 3)
        self.assertEqual(self.service._severity_to_importance("unknown"), 5)


class TestFactoryFunction(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_service_with_defaults(self):
        """测试默认参数创建服务"""
        service = create_project_memory_service()
        
        self.assertIsNotNone(service)
        self.assertIsInstance(service, ProjectMemoryService)
        self.assertTrue(service.session_memory_enabled)
        self.assertTrue(service.ultra_memory_enabled)
    
    def test_create_service_with_custom_settings(self):
        """测试自定义参数创建服务"""
        service = create_project_memory_service(
            state_manager=None,
            session_memory_enabled=False,
            ultra_memory_enabled=True
        )
        
        self.assertIsNotNone(service)
        self.assertFalse(service.session_memory_enabled)
        self.assertTrue(service.ultra_memory_enabled)


if __name__ == "__main__":
    unittest.main(verbosity=2)

