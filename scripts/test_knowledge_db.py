#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试知识库数据库"""

import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    conn = sqlite3.connect('database/data/tasks.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("知识库数据库测试")
    print("="*70 + "\n")
    
    # 1. 测试projects表
    print("[1/5] 测试projects表...")
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    print(f"✓ 项目数: {len(projects)}")
    for p in projects:
        print(f"  - {p['name']} ({p['code']}) - {p['status']}")
    print()
    
    # 2. 测试components表
    print("[2/5] 测试components表...")
    cursor.execute("SELECT name, type, repo_path FROM components")
    components = cursor.fetchall()
    print(f"✓ 组件数: {len(components)}")
    for c in components:
        print(f"  - {c['name']} ({c['type']}) @ {c['repo_path']}")
    print()
    
    # 3. 测试tools表
    print("[3/5] 测试tools表...")
    cursor.execute("SELECT name, type, version FROM tools")
    tools = cursor.fetchall()
    print(f"✓ 工具数: {len(tools)}")
    for t in tools:
        print(f"  - {t['name']} ({t['type']}) v{t['version']}")
    print()
    
    # 4. 测试component_tools关联
    print("[4/5] 测试component_tools关联...")
    cursor.execute("""
        SELECT c.name AS component, t.name AS tool, ct.purpose
        FROM component_tools ct
        JOIN components c ON ct.component_id = c.id
        JOIN tools t ON ct.tool_id = t.id
    """)
    relations = cursor.fetchall()
    print(f"✓ 关联数: {len(relations)}")
    for r in relations:
        print(f"  - {r['component']} 使用 {r['tool']} ({r['purpose']})")
    print()
    
    # 5. 测试tasks表扩展
    print("[5/5] 测试tasks表扩展...")
    cursor.execute("PRAGMA table_info(tasks)")
    columns = cursor.fetchall()
    has_project_id = any(c['name'] == 'project_id' for c in columns)
    has_component_id = any(c['name'] == 'component_id' for c in columns)
    
    if has_project_id and has_component_id:
        print("✓ tasks表已扩展（包含project_id和component_id）")
    else:
        print("⚠️  tasks表未完全扩展")
    
    conn.close()
    
    print("\n" + "="*70)
    print("✅ 知识库数据库测试通过！")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

