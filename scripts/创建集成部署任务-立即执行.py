#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建集成部署任务 - 立即执行
将所有已完成的功能集成到v1.7主线
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

# 集成部署任务清单
INTEGRATION_TASKS = [
    {
        "id": "INTEGRATE-001",
        "title": "集成REQ-001端口冲突解决功能",
        "description": """将REQ-001的端口管理和缓存清除功能集成到v1.7 Dashboard。

【已完成功能】:
- ✅ PortManager端口自动分配 (8870-8899)
- ✅ 缓存版本管理 (dashboard_version.json)
- ✅ 清除缓存功能

【集成任务】:
1. 验证Dashboard显示"清除缓存"按钮
2. 测试端口自动分配功能
3. 验证缓存版本控制
4. 集成到启动脚本

【验收标准】:
- [ ] Dashboard有清除缓存按钮且可用
- [ ] 端口自动分配正常工作
- [ ] 缓存版本显示正确
- [ ] 文档更新完整

【参考文档】:
- REQ-001-完成报告.md
- packages/shared-utils/port_manager.py
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 2,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "tags": "integration,p0,dashboard"
    },
    {
        "id": "INTEGRATE-002",
        "title": "集成REQ-003对话历史库功能",
        "description": """将REQ-003的对话历史库功能集成到v1.7 API和Dashboard。

【已完成功能】:
- ✅ 会话管理UI (4个Tab)
- ✅ 会话CRUD API
- ✅ 会话统计功能
- ✅ 会话标签管理

【集成任务】:
1. 部署会话管理API端点 (11个)
2. 集成会话管理UI到Dashboard
3. 测试会话创建、查询、更新、删除
4. 验证会话统计功能
5. 集成Session Memory MCP

【验收标准】:
- [ ] 11个API端点全部可用
- [ ] 会话管理UI集成到Dashboard
- [ ] 创建/查询/更新/删除功能正常
- [ ] 统计数据准确
- [ ] Session Memory MCP连接正常

【参考文档】:
- ✅REQ-003-对话历史库功能-完成报告.md
- docs/features/conversation-history-library.md
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 3,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "tags": "integration,p0,api,dashboard"
    },
    {
        "id": "INTEGRATE-003",
        "title": "集成REQ-006 Token实时同步功能",
        "description": """将REQ-006的Token同步功能集成到Dashboard。

【已完成功能】:
- ✅ 4种同步方式 (Cursor状态栏/手动输入/历史推算/窗口检测)
- ✅ Token显示组件
- ✅ 对话历史库集成
- ✅ 一键同步按钮

【集成任务】:
1. 验证Dashboard显示Token同步按钮
2. 测试4种同步方式
3. 验证Token历史记录
4. 集成对话历史库联动
5. 测试自动更新机制

【验收标准】:
- [ ] Dashboard显示Token实时数据
- [ ] 4种同步方式全部可用
- [ ] Token历史记录正确
- [ ] 与对话历史库联动正常
- [ ] 文档齐全

【参考文档】:
- ✅REQ-006-Token同步与对话历史库-完成报告.md
- docs/REQ-006-Token同步使用指南.md
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 2,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "tags": "integration,p0,dashboard"
    },
    {
        "id": "INTEGRATE-004",
        "title": "集成REQ-009任务三态流转系统",
        "description": """将REQ-009的任务自动化流转功能集成到API和Dashboard。

【已完成功能】:
- ✅ 三态流转逻辑 (待处理→进行中→已完成)
- ✅ 状态转换API
- ✅ 工时记录功能
- ✅ Dashboard状态展示

【集成任务】:
1. 部署状态流转API端点
2. 集成状态更新UI到Dashboard
3. 测试状态转换逻辑
4. 验证工时记录功能
5. 测试状态历史追踪

【验收标准】:
- [ ] 状态流转API全部可用
- [ ] Dashboard状态更新正常
- [ ] 三态转换逻辑正确
- [ ] 工时记录准确
- [ ] 状态历史可查询

【参考文档】:
- ✅REQ-009-任务三态流转系统-完成报告.md
- REQ-009-C-使用指南.md
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 3,
        "complexity": "medium",
        "assigned_to": "fullstack-engineer",
        "tags": "integration,p1,api"
    },
    {
        "id": "INTEGRATE-005",
        "title": "集成REQ-010全局事件流系统",
        "description": """将REQ-010的事件流系统集成到Dashboard。

【已完成功能】:
- ✅ 事件类型定义 (6大类15+小类)
- ✅ 事件存储 (JSON文件)
- ✅ 事件流UI (5个Tab)
- ✅ 事件筛选功能
- ✅ 事件统计功能

【集成任务】:
1. 验证事件流UI显示
2. 测试事件添加功能
3. 验证事件筛选
4. 测试事件统计
5. 优化事件展示性能

【验收标准】:
- [ ] 事件流UI正常显示
- [ ] 事件添加功能可用
- [ ] 筛选功能正常
- [ ] 统计数据准确
- [ ] 100+事件流畅展示

【参考文档】:
- ✅REQ-010-E-完成报告.md
- docs/features/event-system-quick-guide.md
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 2,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "tags": "integration,p1,dashboard"
    },
    {
        "id": "INTEGRATE-006",
        "title": "集成REQ-011动态进度计算功能",
        "description": """将REQ-011的动态进度计算集成到Dashboard。

【已完成功能】:
- ✅ 实时进度计算 (基于数据库)
- ✅ 进度条自动更新
- ✅ 统计数据实时刷新

【集成任务】:
1. 验证进度计算逻辑
2. 测试进度条更新
3. 验证统计数据准确性
4. 测试自动刷新机制

【验收标准】:
- [ ] 进度计算准确
- [ ] 进度条自动更新
- [ ] 统计数据实时刷新
- [ ] 性能良好(无卡顿)

【参考文档】:
- ✅REQ-011-完成报告.md
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 1.5,
        "complexity": "low",
        "assigned_to": "fullstack-engineer",
        "tags": "integration,p1,dashboard"
    },
    {
        "id": "INTEGRATE-007",
        "title": "E2E集成测试",
        "description": """端到端集成测试，验证所有功能协同工作。

【测试范围】:
1. 完整工作流测试
   - 架构师创建任务
   - 全栈工程师领取任务
   - 状态流转
   - 代码审查
   - 知识记录

2. 数据一致性测试
   - Dashboard显示与数据库一致
   - 统计数据准确
   - 进度计算正确

3. 性能测试
   - 100+任务加载时间 <2秒
   - 事件流100+条流畅
   - 自动刷新无卡顿

4. 跨功能测试
   - Token同步 + 对话历史库
   - 任务流转 + 事件流
   - 进度计算 + 统计展示

【验收标准】:
- [ ] 所有工作流测试通过
- [ ] 数据一致性100%
- [ ] 性能指标达标
- [ ] 跨功能集成正常
- [ ] 生成测试报告

【参考文档】:
- tests/integration/
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 4,
        "complexity": "high",
        "assigned_to": "architect",
        "tags": "integration,p0,test"
    },
    {
        "id": "INTEGRATE-008",
        "title": "更新所有文档和使用指南",
        "description": """更新文档以反映集成后的功能。

【更新内容】:
1. 主README.md
   - 添加v1.7新功能说明
   - 更新快速开始指南
   - 更新架构图

2. API文档
   - 更新端点列表
   - 添加使用示例
   - 更新参数说明

3. 用户指南
   - 更新Dashboard使用指南
   - 添加新功能教程
   - 更新常见问题

4. 开发者文档
   - 更新开发指南
   - 更新部署文档
   - 添加故障排查

【验收标准】:
- [ ] README.md更新
- [ ] API文档完整
- [ ] 用户指南清晰
- [ ] 开发者文档完善
- [ ] 无过时信息

【参考文档】:
- docs/
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 3,
        "complexity": "low",
        "assigned_to": "architect",
        "tags": "integration,p1,docs"
    }
]

def insert_tasks():
    """插入集成部署任务到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    inserted = 0
    skipped = 0
    
    for task in INTEGRATION_TASKS:
        # 检查任务是否已存在
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task["id"],))
        if cursor.fetchone():
            print(f"  [SKIP] {task['id']} (已存在)")
            skipped += 1
            continue
        
        # 插入任务
        cursor.execute("""
            INSERT INTO tasks (
                id, title, description, status, priority,
                estimated_hours, complexity, assigned_to,
                created_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task["id"],
            task["title"],
            task["description"],
            task["status"],
            task["priority"],
            task["estimated_hours"],
            task["complexity"],
            task["assigned_to"],
            datetime.now().isoformat(),
            json.dumps({
                "project_id": "TASKFLOW",
                "tags": task["tags"],
                "integration": True
            }, ensure_ascii=False)
        ))
        
        print(f"  [INSERT] {task['id']}: {task['title']}")
        inserted += 1
    
    conn.commit()
    conn.close()
    
    return inserted, skipped

def add_integration_event():
    """添加集成任务创建事件到Dashboard"""
    events_file = Path(__file__).parent.parent / "apps/dashboard/automation-data/architect_events.json"
    
    try:
        with open(events_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {"events": []}
    
    # 添加事件
    new_event = {
        "id": f"event-{len(data['events']) + 1:03d}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "task_create",
        "icon": "🚀",
        "content": "创建8个集成部署任务 (INTEGRATE-001~008, 共20.5h)"
    }
    
    data["events"].append(new_event)
    
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return True

def main():
    print("=" * 60)
    print("[Integration Deploy] Create integration tasks")
    print("=" * 60)
    print()
    
    print("[Phase] Create 8 integration tasks...")
    inserted, skipped = insert_tasks()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Integration tasks created")
    print("=" * 60)
    print(f"[Inserted] {inserted} tasks")
    print(f"[Skipped] {skipped} tasks")
    print()
    print("[Tasks Overview]")
    print("  P0 Critical (3 tasks, 9h):")
    print("    - INTEGRATE-001: REQ-001端口冲突 (2h)")
    print("    - INTEGRATE-002: REQ-003对话历史库 (3h)")
    print("    - INTEGRATE-003: REQ-006 Token同步 (2h)")
    print("    - INTEGRATE-007: E2E集成测试 (4h)")
    print()
    print("  P1 Important (4 tasks, 11.5h):")
    print("    - INTEGRATE-004: REQ-009任务流转 (3h)")
    print("    - INTEGRATE-005: REQ-010事件流 (2h)")
    print("    - INTEGRATE-006: REQ-011进度计算 (1.5h)")
    print("    - INTEGRATE-008: 文档更新 (3h)")
    print()
    print("[Next Step]")
    print("  1. 派发P0任务给全栈工程师·李明")
    print("  2. 架构师负责E2E测试和文档更新")
    print("  3. 完成后生成集成报告")
    print()
    print("[Dashboard] http://localhost:8877")
    
    # 添加事件
    if add_integration_event():
        print("[Event] Integration task creation recorded")

if __name__ == "__main__":
    main()

