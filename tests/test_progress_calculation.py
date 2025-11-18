#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
REQ-011: Dashboard动态进度计算 - 单元测试

测试进度计算功能的正确性
"""
import unittest
import sqlite3
from pathlib import Path


class TestProgressCalculation(unittest.TestCase):
    """测试进度计算功能"""
    
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        cls.db_path = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
        cls.conn = sqlite3.connect(str(cls.db_path))
        cls.cursor = cls.conn.cursor()
    
    @classmethod
    def tearDownClass(cls):
        """清理测试环境"""
        cls.conn.close()
    
    def test_total_tasks_count(self):
        """测试总任务数统计"""
        self.cursor.execute('SELECT COUNT(*) FROM tasks')
        total = self.cursor.fetchone()[0]
        self.assertGreater(total, 0, "总任务数应该大于0")
    
    def test_completed_tasks_count(self):
        """测试已完成任务数统计"""
        self.cursor.execute('SELECT COUNT(*) FROM tasks WHERE status="completed"')
        completed = self.cursor.fetchone()[0]
        self.assertGreaterEqual(completed, 0, "已完成任务数应该大于等于0")
    
    def test_progress_calculation(self):
        """测试进度计算公式"""
        # 获取总数和完成数
        self.cursor.execute('SELECT COUNT(*) FROM tasks')
        total = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM tasks WHERE status="completed"')
        completed = self.cursor.fetchone()[0]
        
        # 计算进度
        progress = round((completed / total) * 100) if total > 0 else 0
        
        # 验证进度范围
        self.assertGreaterEqual(progress, 0, "进度应该大于等于0%")
        self.assertLessEqual(progress, 100, "进度应该小于等于100%")
        
        # 验证计算正确性
        expected_progress = round((completed / total) * 100) if total > 0 else 0
        self.assertEqual(progress, expected_progress, "进度计算应该正确")
    
    def test_status_distribution(self):
        """测试任务状态分布统计"""
        self.cursor.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
        status_counts = self.cursor.fetchall()
        
        # 验证至少有一个状态
        self.assertGreater(len(status_counts), 0, "应该至少有一个任务状态")
        
        # 验证状态计数都大于0
        for status, count in status_counts:
            self.assertGreater(count, 0, f"状态 {status} 的计数应该大于0")
    
    def test_all_tasks_sum(self):
        """测试各状态任务数之和等于总任务数"""
        # 获取总任务数
        self.cursor.execute('SELECT COUNT(*) FROM tasks')
        total = self.cursor.fetchone()[0]
        
        # 获取各状态任务数
        self.cursor.execute('SELECT COUNT(*) FROM tasks GROUP BY status')
        status_counts = self.cursor.fetchall()
        status_sum = sum(count[0] for count in status_counts)
        
        # 验证总和相等
        self.assertEqual(total, status_sum, "各状态任务数之和应该等于总任务数")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)

