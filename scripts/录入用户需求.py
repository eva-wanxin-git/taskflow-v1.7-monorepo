#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
录入用户提出的5个需求
"""
import sqlite3
import json
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = "database/data/tasks.db"

# 用户提出的5个需求
USER_REQUIREMENTS = [
    {
        "id": "REQ-001",
        "title": "端口冲突彻底解决方案",
        "description": "现在每次更新都必须换新端口非常麻烦。需要实现：1)添加版本号到URL 2)设置no-cache HTTP头 3)Service Worker版本控制 4)提供清除缓存按钮。彻底解决浏览器缓存问题，不再需要换端口。",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 4.0,
        "complexity": "MEDIUM",
        "assigned_to": "fullstack-engineer",
        "metadata": json.dumps({
            "source": "user",
            "type": "enhancement",
            "tags": "infrastructure,cache,user-experience",
            "impact": "避免每次更新换端口",
            "solutions": ["URL版本号", "HTTP头no-cache", "Service Worker控制", "清除缓存按钮"]
        }, ensure_ascii=False),
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "REQ-002",
        "title": "项目记忆空间创立",
        "description": "利用当前使用的2个记忆插件(ultra-memory-cloud和session-memory)，为每个接入任务所的项目建立独立的记忆空间。实现：1)项目隔离存储 2)自动记录架构决策 3)自动记录问题解决方案 4)跨会话知识继承。",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 6.0,
        "complexity": "HIGH",
        "assigned_to": "fullstack-engineer",
        "metadata": json.dumps({
            "source": "user",
            "type": "feature",
            "tags": "memory,knowledge-base,ai-integration",
            "impact": "AI能记住项目历史，提高效率",
            "components": ["ultra-memory-cloud-mcp", "session-memory-mcp"],
            "requirements": ["项目隔离", "自动记录决策", "记录解决方案", "跨会话继承"]
        }, ensure_ascii=False),
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "REQ-003",
        "title": "对话历史库功能",
        "description": "架构师面板上，将'对话交流'改为'对话历史库'，显示过去的多次对话（会话列表），点击可以查看某一次单独对话的完整内容。实现：1)会话列表展示 2)单次会话详情 3)时间/Token/主题标注 4)搜索过滤功能。",
        "status": "pending",
        "priority": "P2",
        "estimated_hours": 5.0,
        "complexity": "MEDIUM",
        "assigned_to": "frontend-engineer",
        "metadata": json.dumps({
            "source": "user",
            "type": "feature",
            "tags": "dashboard,ui,conversation-history",
            "impact": "用户能查看历史对话，追溯决策过程",
            "components": ["ARCHITECT MONITOR", "对话交流Tab"],
            "features": ["会话列表", "会话详情", "时间标注", "搜索过滤"]
        }, ensure_ascii=False),
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "REQ-004",
        "title": "架构师即插即用强制流程",
        "description": "确保架构师接手新项目时，明确知道要做的所有事情，并强制性完成Dashboard更新。实现：1)自动检查清单 2)强制流程提醒 3)未完成项警告 4)一键执行脚本。让架构师Dashboard更新标准流程.md中的8个阶段自动落地。",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 8.0,
        "complexity": "HIGH",
        "assigned_to": "fullstack-engineer",
        "metadata": json.dumps({
            "source": "user",
            "type": "feature",
            "tags": "architect-workflow,automation,quality-assurance",
            "impact": "确保每个项目Dashboard都能正确更新",
            "requirements": ["自动检查清单", "强制流程", "未完成警告", "一键脚本"],
            "ref_doc": "docs/ai/架构师Dashboard更新标准流程.md"
        }, ensure_ascii=False),
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "REQ-005",
        "title": "用户任务所Dashboard重构升级",
        "description": "重构和升级Dashboard的功能和展示，完整实现v1.7的多个功能，让用户感知到系统的运作逻辑。包括：1)细粒度功能展示优化 2)2Tab任务分类优化 3)实时更新机制优化 4)交互体验提升 5)数据可视化增强 6)响应式设计。",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 16.0,
        "complexity": "HIGH",
        "assigned_to": "fullstack-engineer",
        "metadata": json.dumps({
            "source": "user",
            "type": "refactor",
            "tags": "dashboard,ui-ux,visualization,refactor",
            "impact": "用户体验大幅提升，系统价值更可见",
            "scope": ["功能展示", "任务分类", "实时更新", "交互体验", "数据可视化", "响应式"],
            "estimated_impact": "用户满意度+50%"
        }, ensure_ascii=False),
        "created_at": datetime.now().isoformat()
    }
]

def insert_user_requirements():
    """插入用户需求到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        for req in USER_REQUIREMENTS:
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
        
        print("\n✅ 用户需求已录入数据库\n")
        print("录入的5个需求:")
        for req in USER_REQUIREMENTS:
            print(f"  [{req['priority']}] {req['id']}: {req['title']} ({req['estimated_hours']}h)")
        
        print(f"\n总计: 5个用户需求")
        print(f"优先级: P0(1个) + P1(2个) + P2(2个)")
        print(f"总工时: {sum(r['estimated_hours'] for r in USER_REQUIREMENTS)}h")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    insert_user_requirements()

