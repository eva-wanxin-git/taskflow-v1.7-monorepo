#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入用户提出的3个新需求
"""
import sqlite3
import json
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = "database/data/tasks.db"

NEW_REQUIREMENTS = [
    {
        "id": "REQ-006",
        "title": "Token显示准确实时同步",
        "description": "架构师Token余量显示必须准确实时，同步Cursor状态栏的真实Token使用量。实现：1)自动读取Cursor状态栏Token值 2)实时同步到Dashboard 3)每次操作后自动更新 4)多会话Token累加计算正确。避免手动更新导致的不准确。",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 3.0,
        "complexity": "MEDIUM",
        "assigned_to": "fullstack-engineer",
        "metadata": json.dumps({
            "source": "user",
            "type": "feature",
            "tags": "dashboard,real-time,accuracy",
            "impact": "Token数据准确，避免误判",
            "requirements": ["读取Cursor状态栏", "实时同步", "自动更新", "多会话累加"]
        }, ensure_ascii=False),
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "REQ-007",
        "title": "封装v1.7完整版为独立包",
        "description": "将任务所·Flow v1.7封装成完整的独立版本，可一键部署到新项目。包括：1)完整打包(代码+文档+数据库+工具) 2)一键安装脚本 3)配置向导 4)README使用说明 5)版本管理。类似v1.5的GitHub发布。",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 8.0,
        "complexity": "HIGH",
        "assigned_to": "fullstack-engineer",
        "metadata": json.dumps({
            "source": "user",
            "type": "release",
            "tags": "packaging,deployment,release",
            "impact": "v1.7可独立发布使用",
            "requirements": ["完整打包", "一键安装", "配置向导", "README", "版本管理"],
            "ref": "v1.5封装经验"
        }, ensure_ascii=False),
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "REQ-008",
        "title": "真实项目测试与反向改进",
        "description": "将v1.7部署到一个真实项目(如librechat-desktop)中运行测试，发现问题并反向改进任务所本身。包括：1)选择测试项目 2)完整部署v1.7 3)架构师接手分析 4)记录所有问题 5)反向优化任务所 6)形成最佳实践文档。",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 12.0,
        "complexity": "HIGH",
        "assigned_to": "architect+fullstack-engineer",
        "metadata": json.dumps({
            "source": "user",
            "type": "testing",
            "tags": "real-world-test,improvement,best-practices",
            "impact": "验证v1.7实用性，发现真实问题",
            "test_project": "librechat-desktop或其他",
            "steps": ["选择项目", "部署v1.7", "架构师分析", "记录问题", "反向改进", "文档化"],
            "expected_outcome": "最佳实践文档+v1.7优化清单"
        }, ensure_ascii=False),
        "created_at": datetime.now().isoformat()
    }
]

def insert_requirements():
    """插入需求到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        for req in NEW_REQUIREMENTS:
            cursor.execute("""
                INSERT OR REPLACE INTO tasks (
                    id, title, description, status, priority, 
                    estimated_hours, complexity, assigned_to, 
                    metadata, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                req["id"],
                req["title"],
                req["description"],
                req["status"],
                req["priority"],
                req["estimated_hours"],
                req["complexity"],
                req["assigned_to"],
                req["metadata"],
                req["created_at"]
            ))
        
        conn.commit()
        
        print("\n✅ 3个新需求已录入数据库\n")
        print("录入的需求:")
        for req in NEW_REQUIREMENTS:
            print(f"  [{req['priority']}] {req['id']}: {req['title']} ({req['estimated_hours']}h)")
        
        print(f"\n总计: 3个新需求")
        print(f"总工时: {sum(r['estimated_hours'] for r in NEW_REQUIREMENTS)}h")
        
        # 显示所有用户需求
        cursor.execute("SELECT id, title, priority, estimated_hours FROM tasks WHERE id LIKE 'REQ-%' ORDER BY priority, id")
        all_reqs = cursor.fetchall()
        print(f"\n所有用户需求: {len(all_reqs)}个")
        for req in all_reqs:
            print(f"  [{req[2]}] {req[0]}: {req[1]} ({req[3]}h)")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 错误: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_requirements()

