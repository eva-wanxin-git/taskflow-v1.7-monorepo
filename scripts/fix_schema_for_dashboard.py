#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复v1.7数据库schema，使其兼容Dashboard
"""
import sqlite3
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = "database/data/tasks.db"

def fix_schema():
    """修复schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n=== 修复数据库Schema ===\n")
    
    try:
        # 1. 检查是否已有depends_on字段
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # 2. 添加depends_on和blocked_by字段
        if 'depends_on' not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN depends_on TEXT DEFAULT '[]'")
            print("✓ 已添加 depends_on 字段")
        
        if 'blocked_by' not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN blocked_by TEXT DEFAULT '[]'")
            print("✓ 已添加 blocked_by 字段")
        
        if 'revision_count' not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN revision_count INTEGER DEFAULT 0")
            print("✓ 已添加 revision_count 字段")
        
        if 'max_revision_attempts' not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN max_revision_attempts INTEGER DEFAULT 3")
            print("✓ 已添加 max_revision_attempts 字段")
        
        if 'assigned_at' not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN assigned_at TEXT")
            print("✓ 已添加 assigned_at 字段")
        
        if 'completed_at' not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN completed_at TEXT")
            print("✓ 已添加 completed_at 字段")
        
        # 3. 从task_dependencies表读取依赖关系，转换为JSON填充depends_on
        cursor.execute("""
            SELECT task_id, GROUP_CONCAT(dependency_id) as deps
            FROM task_dependencies
            GROUP BY task_id
        """)
        dependencies = cursor.fetchall()
        
        for task_id, deps in dependencies:
            if deps:
                dep_list = deps.split(',')
                cursor.execute("""
                    UPDATE tasks 
                    SET depends_on = ?
                    WHERE id = ?
                """, (json.dumps(dep_list), task_id))
        
        print(f"✓ 已同步 {len(dependencies)} 个任务的依赖关系")
        
        # 4. 初始化所有任务的空JSON字段
        cursor.execute("""
            UPDATE tasks 
            SET depends_on = '[]'
            WHERE depends_on IS NULL OR depends_on = ''
        """)
        
        cursor.execute("""
            UPDATE tasks 
            SET blocked_by = '[]'
            WHERE blocked_by IS NULL OR blocked_by = ''
        """)
        
        conn.commit()
        
        print("\n✅ Schema修复完成！")
        print("\n现在Dashboard应该可以正常显示数据了。")
        print("请刷新浏览器: http://localhost:8871")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_schema()

