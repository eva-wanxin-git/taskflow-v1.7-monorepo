#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移工具

用法:
    python migrate.py init      # 初始化数据库
    python migrate.py upgrade   # 升级到最新版本
    python migrate.py rollback  # 回滚上一个版本
"""

import sqlite3
import sys
import io
from pathlib import Path
from datetime import datetime

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "database" / "data" / "tasks.db"
SCHEMAS_DIR = PROJECT_ROOT / "database" / "schemas"
MIGRATIONS_DIR = PROJECT_ROOT / "database" / "migrations"
SEEDS_DIR = PROJECT_ROOT / "database" / "seeds"


class DatabaseMigrator:
    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(str(self.db_path))
    
    def init_database(self):
        """初始化数据库"""
        print("=" * 70)
        print("初始化数据库")
        print("=" * 70)
        print()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 1. 执行v1任务Schema
            print("[1/3] 创建任务表...")
            with open(SCHEMAS_DIR / "v1_tasks_schema.sql", 'r', encoding='utf-8') as f:
                schema_sql = f.read()
                cursor.executescript(schema_sql)
            print("✓ 任务表创建完成")
            
            # 2. 执行v2知识库Schema  
            print("[2/3] 创建知识库表...")
            with open(SCHEMAS_DIR / "v2_knowledge_schema.sql", 'r', encoding='utf-8') as f:
                schema_sql = f.read()
                cursor.executescript(schema_sql)
            print("✓ 知识库表创建完成")
            
            # 3. 添加project_id和component_id到tasks表
            print("[3/3] 扩展tasks表...")
            try:
                cursor.execute("ALTER TABLE tasks ADD COLUMN project_id TEXT REFERENCES projects(id)")
            except sqlite3.OperationalError as e:
                if "duplicate column" in str(e).lower():
                    print("  ⚠️  project_id列已存在，跳过")
                else:
                    raise
            
            try:
                cursor.execute("ALTER TABLE tasks ADD COLUMN component_id TEXT REFERENCES components(id)")
            except sqlite3.OperationalError as e:
                if "duplicate column" in str(e).lower():
                    print("  ⚠️  component_id列已存在，跳过")
                else:
                    raise
            
            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_component ON tasks(component_id)")
            print("✓ tasks表扩展完成")
            
            conn.commit()
            print()
            print("=" * 70)
            print("✅ 数据库初始化成功！")
            print(f"📍 数据库位置: {self.db_path}")
            print("=" * 70)
            
        except Exception as e:
            conn.rollback()
            print(f"\n❌ 初始化失败: {e}")
            raise
        finally:
            conn.close()
    
    def seed_data(self):
        """插入初始数据"""
        print("\n插入初始数据...")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            with open(SEEDS_DIR / "001_default_project.sql", 'r', encoding='utf-8') as f:
                seed_sql = f.read()
                cursor.executescript(seed_sql)
            
            conn.commit()
            print("✓ 初始数据插入完成")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ 数据插入失败: {e}")
            raise
        finally:
            conn.close()
    
    def backup_database(self):
        """备份数据库"""
        if not self.db_path.exists():
            print("⚠️  数据库不存在，无需备份")
            return None
        
        backup_dir = self.db_path.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"tasks_backup_{timestamp}.db"
        
        import shutil
        shutil.copy2(self.db_path, backup_path)
        
        print(f"✓ 数据库已备份到: {backup_path}")
        return backup_path
    
    def get_table_count(self):
        """获取表数量"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def list_tables(self):
        """列出所有表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return tables


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python migrate.py init      # 初始化数据库")
        print("  python migrate.py seed      # 插入初始数据")
        print("  python migrate.py backup    # 备份数据库")
        print("  python migrate.py status    # 查看数据库状态")
        sys.exit(1)
    
    command = sys.argv[1]
    migrator = DatabaseMigrator()
    
    if command == "init":
        # 初始化数据库
        backup = migrator.backup_database()
        migrator.init_database()
        migrator.seed_data()
        
    elif command == "seed":
        # 只插入数据
        migrator.seed_data()
        
    elif command == "backup":
        # 备份数据库
        migrator.backup_database()
        
    elif command == "status":
        # 查看状态
        if not migrator.db_path.exists():
            print("❌ 数据库不存在")
            sys.exit(1)
        
        table_count = migrator.get_table_count()
        tables = migrator.list_tables()
        
        print("=" * 70)
        print("数据库状态")
        print("=" * 70)
        print(f"📍 位置: {migrator.db_path}")
        print(f"📊 表数量: {table_count}")
        print(f"📋 表列表:")
        for table in tables:
            print(f"   - {table}")
        print("=" * 70)
        
    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

