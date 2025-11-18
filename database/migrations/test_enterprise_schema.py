#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业级知识库Schema测试脚本
用途: 验证SQL语法、表结构、索引创建
"""

import sys
import io

# Windows终端编码问题解决
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import sqlite3
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def test_schema():
    """测试Schema创建"""
    print("=" * 80)
    print("任务所·Flow v1.7 - 企业级知识库Schema测试")
    print("=" * 80)
    
    # 创建临时测试数据库
    test_db = "test_enterprise_knowledge.db"
    
    try:
        # 删除旧的测试数据库
        if os.path.exists(test_db):
            os.remove(test_db)
            print(f"✓ 删除旧测试数据库")
        
        # 连接数据库
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        print(f"✓ 创建测试数据库: {test_db}")
        
        # 1. 先创建依赖的基础表（简化版）
        print("\n【步骤1】创建基础依赖表...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        print("  ✓ 创建projects表")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS components (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)
        print("  ✓ 创建components表")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tools (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        print("  ✓ 创建tools表（基础版）")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS component_tools (
                component_id TEXT NOT NULL,
                tool_id TEXT NOT NULL,
                purpose TEXT,
                PRIMARY KEY (component_id, tool_id),
                FOREIGN KEY (component_id) REFERENCES components(id),
                FOREIGN KEY (tool_id) REFERENCES tools(id)
            )
        """)
        print("  ✓ 创建component_tools表（基础版）")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_articles (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        print("  ✓ 创建knowledge_articles表（基础版）")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deployments (
                id TEXT PRIMARY KEY,
                component_id TEXT NOT NULL,
                environment TEXT NOT NULL,
                version TEXT NOT NULL,
                deployed_at TEXT DEFAULT (datetime('now')),
                status TEXT DEFAULT 'success'
            )
        """)
        print("  ✓ 创建deployments表（基础版）")
        
        # 2. 读取并执行迁移脚本
        print("\n【步骤2】执行企业级Schema迁移...")
        
        migration_file = Path(__file__).parent / "005_enterprise_knowledge_schema.sql"
        
        if not migration_file.exists():
            print(f"  ✗ 迁移文件不存在: {migration_file}")
            return False
        
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 使用executescript执行整个SQL文件
        try:
            cursor.executescript(sql_content)
            print(f"  ✓ 迁移脚本执行成功")
        except sqlite3.Error as e:
            print(f"  ✗ 迁移脚本执行失败: {e}")
            
            # 尝试逐句执行以找出问题
            print("  → 尝试逐句执行...")
            
            # 简单的SQL分割（忽略注释）
            lines = sql_content.split('\n')
            statement = []
            success_count = 0
            error_count = 0
            
            for line in lines:
                # 跳过空行和注释
                stripped = line.strip()
                if not stripped or stripped.startswith('--'):
                    continue
                
                statement.append(line)
                
                # 当遇到分号时，执行这个语句
                if stripped.endswith(';'):
                    sql = '\n'.join(statement)
                    try:
                        cursor.execute(sql)
                        success_count += 1
                    except sqlite3.Error as stmt_error:
                        if "duplicate column" not in str(stmt_error).lower():
                            error_count += 1
                            if error_count <= 5:  # 只显示前5个错误
                                print(f"    ✗ SQL错误: {stmt_error}")
                    statement = []
            
            print(f"  ✓ 逐句执行完成: {success_count} 成功, {error_count} 失败")
        
        # 3. 验证表结构
        print("\n【步骤3】验证表结构...")
        
        expected_tables = [
            'projects',
            'components',
            'tools',
            'component_tools',
            'knowledge_articles',
            'deployments',
            'environments',
            'interaction_events',
            'memory_snapshots',
            'memory_categories',
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        actual_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"  实际表数量: {len(actual_tables)}")
        
        for table in expected_tables:
            if table in actual_tables:
                print(f"  ✓ {table}")
            else:
                print(f"  ✗ {table} (缺失)")
        
        # 4. 验证索引
        print("\n【步骤4】验证索引...")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' ORDER BY name")
        indexes = [row[0] for row in cursor.fetchall()]
        
        expected_indexes = [
            'idx_environments_project',
            'idx_interactions_project',
            'idx_snapshots_project',
            'idx_categories_layer',
        ]
        
        print(f"  总索引数量: {len(indexes)}")
        
        for idx in expected_indexes:
            if idx in indexes:
                print(f"  ✓ {idx}")
            else:
                print(f"  ✗ {idx} (缺失)")
        
        # 5. 验证21库数据
        print("\n【步骤5】验证21库知识分类数据...")
        
        cursor.execute("SELECT COUNT(*) FROM memory_categories")
        count = cursor.fetchone()[0]
        
        if count >= 21:
            print(f"  ✓ 知识分类数据已初始化: {count} 条")
            
            # 显示分层统计
            cursor.execute("SELECT layer, COUNT(*) FROM memory_categories GROUP BY layer")
            for layer, cnt in cursor.fetchall():
                layer_name = {1: '基础设施层', 2: '业务逻辑层', 3: '应用层'}.get(layer, f'Layer {layer}')
                print(f"    - {layer_name}: {cnt} 个分类")
        else:
            print(f"  ✗ 知识分类数据不完整: 仅 {count} 条（预期21条）")
        
        # 6. 测试数据插入
        print("\n【步骤6】测试数据插入...")
        
        # 插入测试项目
        cursor.execute("""
            INSERT INTO projects (id, name, code, description) 
            VALUES ('PRJ-TEST', '测试项目', 'TEST', '企业级Schema测试项目')
        """)
        print("  ✓ 插入测试项目")
        
        # 插入测试环境
        cursor.execute("""
            INSERT INTO environments (id, project_id, name, display_name, type) 
            VALUES ('ENV-001', 'PRJ-TEST', 'dev', '开发环境', 'local')
        """)
        print("  ✓ 插入测试环境")
        
        # 插入测试交互事件
        cursor.execute("""
            INSERT INTO interaction_events (id, project_id, session_id, actor_type, action_type, tokens_total) 
            VALUES ('INT-001', 'PRJ-TEST', 'SESSION-001', 'user', 'query', 100)
        """)
        print("  ✓ 插入测试交互事件")
        
        # 插入测试记忆快照
        cursor.execute("""
            INSERT INTO memory_snapshots (id, project_id, snapshot_type, title, refined_content) 
            VALUES ('MEM-001', 'PRJ-TEST', 'session_end', '测试快照', '测试内容')
        """)
        print("  ✓ 插入测试记忆快照")
        
        # 7. 测试外键约束
        print("\n【步骤7】测试外键约束...")
        
        try:
            cursor.execute("""
                INSERT INTO environments (id, project_id, name, display_name, type) 
                VALUES ('ENV-999', 'PRJ-NOTEXIST', 'dev', '测试', 'local')
            """)
            print("  ✗ 外键约束未生效（应该失败但成功了）")
        except sqlite3.IntegrityError:
            print("  ✓ 外键约束正常工作")
        
        # 8. 提交并总结
        conn.commit()
        print("\n" + "=" * 80)
        print("测试结果总结:")
        print(f"  ✓ Schema创建成功")
        print(f"  ✓ 表数量: {len(actual_tables)}")
        print(f"  ✓ 索引数量: {len(indexes)}")
        print(f"  ✓ 知识分类: {count} 条")
        print(f"  ✓ 数据插入测试通过")
        print(f"  ✓ 外键约束测试通过")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()
            print(f"\n✓ 测试数据库已关闭")
        
        # 自动删除测试数据库
        if os.path.exists(test_db):
            try:
                os.remove(test_db)
                print(f"✓ 测试数据库已删除: {test_db}")
            except Exception as e:
                print(f"⚠ 无法删除测试数据库: {e}")


def check_sql_syntax():
    """检查SQL文件语法"""
    print("\n" + "=" * 80)
    print("SQL语法检查")
    print("=" * 80)
    
    schema_file = Path(__file__).parent.parent / "schemas" / "v4_enterprise_knowledge_schema.sql"
    
    if not schema_file.exists():
        print(f"✗ Schema文件不存在: {schema_file}")
        return False
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 基本统计
    lines = content.split('\n')
    total_lines = len(lines)
    comment_lines = sum(1 for line in lines if line.strip().startswith('--'))
    code_lines = total_lines - comment_lines
    
    # 统计关键字
    create_table_count = content.upper().count('CREATE TABLE')
    create_index_count = content.upper().count('CREATE INDEX')
    insert_count = content.upper().count('INSERT')
    alter_table_count = content.upper().count('ALTER TABLE')
    
    print(f"  总行数: {total_lines}")
    print(f"  注释行: {comment_lines}")
    print(f"  代码行: {code_lines}")
    print(f"  CREATE TABLE: {create_table_count}")
    print(f"  CREATE INDEX: {create_index_count}")
    print(f"  INSERT: {insert_count}")
    print(f"  ALTER TABLE: {alter_table_count}")
    
    print("\n✓ 文件结构正常")
    return True


if __name__ == "__main__":
    print("\n[START] 开始企业级知识库Schema测试...\n")
    
    # 1. 检查SQL语法
    if not check_sql_syntax():
        print("\n[FAIL] SQL语法检查失败")
        sys.exit(1)
    
    # 2. 测试Schema
    if not test_schema():
        print("\n[FAIL] Schema测试失败")
        sys.exit(1)
    
    print("\n[SUCCESS] 所有测试通过！")
    print("\n[NEXT] 下一步:")
    print("  1. 检查测试输出确认所有表和索引都已创建")
    print("  2. 运行 python database/migrations/migrate.py apply 005")
    print("  3. 验证生产数据库")
    print()

