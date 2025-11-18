#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成Monorepo模板到知识库脚本

将docs/arch/monorepo-structure-template.md集成到知识库数据库
"""

import sqlite3
import sys
import io
from pathlib import Path
from datetime import datetime
import json

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "database" / "data" / "tasks.db"
TEMPLATE_PATH = PROJECT_ROOT / "docs" / "arch" / "monorepo-structure-template.md"


class TemplateIntegrator:
    """模板集成器"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(str(self.db_path))
    
    def read_template_file(self):
        """读取模板文件"""
        if not TEMPLATE_PATH.exists():
            print(f"❌ 模板文件不存在: {TEMPLATE_PATH}")
            return None
        
        try:
            with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"❌ 读取模板文件失败: {e}")
            return None
    
    def extract_template_metadata(self, content):
        """从模板内容中提取元数据"""
        lines = content.split('\n')
        
        title = "企业级Monorepo目录结构模板"
        for line in lines[:20]:
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                break
        
        # 提取描述（从概述部分）
        description = "生产级Monorepo目录结构，适用于企业级项目"
        
        tags = ["monorepo", "architecture", "enterprise", "structure", "template"]
        
        return {
            "title": title,
            "description": description,
            "tags": tags,
            "category": "architecture"
        }
    
    def get_or_create_project(self, conn):
        """获取或创建项目"""
        cursor = conn.cursor()
        
        project_id = "TASKFLOW-v17"
        project_name = "任务所·Flow v1.7"
        project_code = "TASKFLOW"
        
        try:
            cursor.execute(
                "SELECT id FROM projects WHERE code = ?",
                (project_code,)
            )
            result = cursor.fetchone()
            
            if result:
                return result[0]
            
            # 创建新项目
            cursor.execute("""
                INSERT INTO projects (id, name, code, description, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                project_id,
                project_name,
                project_code,
                "企业级AI任务中枢系统",
                "active",
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            conn.commit()
            print(f"✓ 创建项目: {project_name}")
            return project_id
            
        except sqlite3.OperationalError as e:
            if "duplicate" in str(e).lower():
                return project_id
            raise
    
    def get_or_create_component(self, conn, project_id):
        """获取或创建架构组件"""
        cursor = conn.cursor()
        
        component_id = "TASKFLOW-ARCH"
        component_name = "系统架构"
        
        try:
            cursor.execute(
                "SELECT id FROM components WHERE id = ?",
                (component_id,)
            )
            result = cursor.fetchone()
            
            if result:
                return result[0]
            
            # 创建新组件
            cursor.execute("""
                INSERT INTO components (id, project_id, name, type, description, repo_path, tech_stack, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                component_id,
                project_id,
                component_name,
                "backend",
                "系统架构设计和文档",
                "docs/arch",
                json.dumps(["Monorepo", "Architecture"]),
                datetime.now().isoformat()
            ))
            conn.commit()
            print(f"✓ 创建组件: {component_name}")
            return component_id
            
        except sqlite3.OperationalError as e:
            if "duplicate" in str(e).lower():
                return component_id
            raise
    
    def create_article(self, conn, content, metadata, project_id, component_id):
        """创建知识文章"""
        cursor = conn.cursor()
        
        article_id = "ARTICLE-MONOREPO-TEMPLATE"
        
        try:
            # 检查是否已存在
            cursor.execute(
                "SELECT id FROM knowledge_articles WHERE id = ?",
                (article_id,)
            )
            result = cursor.fetchone()
            
            if result:
                print(f"⚠️  文章已存在: {article_id}，更新内容...")
                cursor.execute("""
                    UPDATE knowledge_articles 
                    SET content = ?, title = ?, tags = ?, updated_at = ?
                    WHERE id = ?
                """, (
                    content,
                    metadata["title"],
                    json.dumps(metadata["tags"]),
                    datetime.now().isoformat(),
                    article_id
                ))
                conn.commit()
                return article_id
            
            # 创建新文章
            cursor.execute("""
                INSERT INTO knowledge_articles 
                (id, project_id, component_id, title, content, category, tags, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article_id,
                project_id,
                component_id,
                metadata["title"],
                content,
                metadata["category"],
                json.dumps(metadata["tags"]),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            conn.commit()
            print(f"✓ 创建知识文章: {article_id}")
            return article_id
            
        except Exception as e:
            print(f"❌ 创建文章失败: {e}")
            raise
    
    def integrate(self):
        """执行集成"""
        print("=" * 70)
        print("集成TASK-004-A1企业级模板到知识库")
        print("=" * 70)
        print()
        
        # 步骤1: 读取模板文件
        print("[1/4] 读取模板文件...")
        content = self.read_template_file()
        if not content:
            return False
        print(f"✓ 模板文件大小: {len(content)} 字节, {len(content.split(chr(10)))} 行")
        
        # 步骤2: 提取元数据
        print("[2/4] 提取模板元数据...")
        metadata = self.extract_template_metadata(content)
        print(f"✓ 标题: {metadata['title']}")
        print(f"✓ 分类: {metadata['category']}")
        print(f"✓ 标签: {', '.join(metadata['tags'])}")
        
        # 步骤3: 连接数据库并集成
        print("[3/4] 连接数据库...")
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_articles'"
            )
            if not cursor.fetchone():
                print("❌ 知识库表不存在，请先运行: python database/migrations/migrate.py init")
                return False
            
            print("✓ 数据库连接成功")
            
            # 获取或创建项目
            print("[4/4] 保存到知识库...")
            project_id = self.get_or_create_project(conn)
            component_id = self.get_or_create_component(conn, project_id)
            article_id = self.create_article(conn, content, metadata, project_id, component_id)
            
            conn.close()
            
            print()
            print("=" * 70)
            print("✅ 集成成功！")
            print(f"📍 项目ID: {project_id}")
            print(f"📍 组件ID: {component_id}")
            print(f"📍 文章ID: {article_id}")
            print(f"📍 数据库: {self.db_path}")
            print("=" * 70)
            
            return True
            
        except Exception as e:
            print(f"❌ 集成失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    integrator = TemplateIntegrator()
    success = integrator.integrate()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

