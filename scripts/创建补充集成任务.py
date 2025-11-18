#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建补充集成任务 - 10个未集成的功能
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
EVENTS_FILE = Path(__file__).parent.parent / "apps/dashboard/automation-data/architect_events.json"

# 补充集成任务
ADDITIONAL_TASKS = [
    {
        "id": "INTEGRATE-009",
        "title": "集成REQ-002项目记忆空间核心功能",
        "description": """将REQ-002的项目记忆空间完整集成到v1.7系统。

【已完成功能】:
- ✅ 12表知识库数据库设计
- ✅ 项目记忆API设计（11个端点）
- ✅ 自动记录ADR和解决方案
- ⚠️ 数据库查询逻辑待完善（REQ-002-B）

【集成任务】:
1. 确保数据库表已创建（project_memories等4表）
2. 部署记忆空间API端点到主API服务
3. 在Dashboard添加"记忆空间"入口
4. 测试记忆创建、查询、统计功能
5. 集成Session Memory和Ultra Memory MCP
6. 验证跨会话知识继承

【验收标准】:
- [ ] 4个数据库表存在且可用
- [ ] 11个API端点可访问
- [ ] Dashboard有记忆空间入口
- [ ] 可以创建和查询记忆
- [ ] MCP连接正常

【依赖】:
- REQ-002-B完成（数据库查询实现）

【参考】:
- docs/features/PROJECT_MEMORY_SPACE.md
- ✅REQ-002-项目记忆空间-完成报告.md
""",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 3,
        "complexity": "high",
        "assigned_to": "fullstack-engineer",
        "tags": "integration,p0,memory"
    },
    {
        "id": "INTEGRATE-010",
        "title": "验证REQ-009子任务集成",
        "description": """验证REQ-009的3个子任务是否正确集成到Dashboard。

【子任务】:
- ✅ REQ-009-A: 一键复制按钮 (2h)
- ✅ REQ-009-B: 状态管理脚本和API (1.5h)
- ✅ REQ-009-C: 自动刷新 (0.5h)

【验证内容】:
1. Dashboard有"📋 一键复制提示词"按钮
2. 点击按钮可以复制完整提示词
3. 李明收到任务.py脚本可用
4. 李明提交完成.py脚本可用
5. API端点 /received 和 /complete 可用
6. 自动刷新每15秒执行一次

【验收标准】:
- [ ] 3个子功能全部在Dashboard上可见
- [ ] 一键复制功能正常
- [ ] 脚本工具测试通过
- [ ] API端点响应正常
- [ ] 自动刷新机制正常

【参考】:
- ✅REQ-009-任务三态流转系统-完成报告.md
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 1,
        "complexity": "low",
        "assigned_to": "architect",
        "tags": "integration,p1,verification"
    },
    {
        "id": "INTEGRATE-011",
        "title": "验证REQ-010子任务集成",
        "description": """验证REQ-010的4个子任务是否正确集成。

【子任务】:
- ✅ REQ-010-A: 事件类型设计 (1h)
- ✅ REQ-010-B: 事件存储系统 (3h)
- ✅ REQ-010-C: 事件触发集成 (2h)
- ✅ REQ-010-E: 事件流UI升级 (2h)

【验证内容】:
1. architect_events.json包含150+事件
2. 事件结构完整（id/timestamp/type/content）
3. Dashboard"事件流"Tab可见
4. 事件流可以筛选和搜索
5. 所有脚本都会记录事件

【验收标准】:
- [ ] 事件数据文件存在且完整
- [ ] 事件流UI正常显示
- [ ] 事件筛选功能可用
- [ ] 事件实时记录正常

【参考】:
- ✅REQ-010-E-完成报告.md
- docs/features/event-system-quick-guide.md
""",
        "status": "pending",
        "priority": "P1",
        "estimated_hours": 1,
        "complexity": "low",
        "assigned_to": "architect",
        "tags": "integration,p1,verification"
    },
    {
        "id": "INTEGRATE-012",
        "title": "集成TASK-004-A1企业级目录结构模板",
        "description": """将TASK-004-A1的企业级模板文档集成到知识库。

【已完成】:
- ✅ monorepo-structure-template.md (600行)
- ✅ 完整的企业级目录结构
- ✅ 详细的说明和注释

【集成任务】:
1. 验证文档位置正确（docs/arch/）
2. 添加到知识库索引
3. 在Dashboard添加快速访问入口
4. 生成PDF版本（可选）
5. 添加到新项目模板库

【验收标准】:
- [ ] 文档在docs/arch/目录
- [ ] 可以通过Dashboard访问
- [ ] 添加到知识库文章表
- [ ] 有使用示例

【参考】:
- ✅TASK-004-A1-完成报告.md
- docs/arch/monorepo-structure-template.md
""",
        "status": "pending",
        "priority": "P2",
        "estimated_hours": 1,
        "complexity": "low",
        "assigned_to": "architect",
        "tags": "integration,p2,docs"
    },
    {
        "id": "INTEGRATE-013",
        "title": "验证TASK-C-3架构师API测试集成",
        "description": """验证TASK-C-3的E2E测试是否集成到测试套件。

【已完成】:
- ✅ 架构师API端到端测试
- ✅ 测试脚本编写
- ✅ 测试通过

【验证任务】:
1. 测试文件是否在tests/目录
2. 测试是否可以运行
3. 测试覆盖率是否足够
4. 集成到CI/CD（如有）

【验收标准】:
- [ ] 测试文件存在
- [ ] 测试可以独立运行
- [ ] 测试通过率100%
- [ ] 集成到测试套件

【参考】:
- ✅TASK-C-3-完成报告.md
- tests/integration/
""",
        "status": "pending",
        "priority": "P2",
        "estimated_hours": 0.5,
        "complexity": "low",
        "assigned_to": "architect",
        "tags": "integration,p2,test"
    },
    {
        "id": "INTEGRATE-014",
        "title": "集成BUG-001任务列表修复",
        "description": """验证BUG-001的修复是否已部署到生产环境。

【已完成】:
- ✅ 修复state_manager.py兼容性
- ✅ 7分钟快速修复
- ✅ 验证测试通过

【验证任务】:
1. 确认修复代码已合并到主分支
2. Dashboard任务列表加载正常
3. 无schema兼容性错误
4. 记录修复到知识库

【验收标准】:
- [ ] 任务列表加载正常
- [ ] 无控制台错误
- [ ] 修复已文档化

【参考】:
- ✅BUG-001修复完成.md
""",
        "status": "pending",
        "priority": "P2",
        "estimated_hours": 0.5,
        "complexity": "low",
        "assigned_to": "architect",
        "tags": "integration,p2,bugfix"
    }
]

def insert_tasks():
    """插入补充集成任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    inserted = 0
    skipped = 0
    
    for task in ADDITIONAL_TASKS:
        # 检查是否已存在
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task["id"],))
        if cursor.fetchone():
            print(f"  [SKIP] {task['id']} (已存在)")
            skipped += 1
            continue
        
        # 插入
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

def main():
    print("=" * 70)
    print("[Additional Integration] Create 补充集成任务")
    print("=" * 70)
    print()
    
    inserted, skipped = insert_tasks()
    
    print()
    print("=" * 70)
    print("[SUCCESS] 补充任务创建完成")
    print("=" * 70)
    print(f"[新增] {inserted} 个任务")
    print(f"[跳过] {skipped} 个任务")
    print()
    print("[补充集成任务]:")
    print("  P0 Critical:")
    print("    - INTEGRATE-009: REQ-002项目记忆空间 (3h)")
    print()
    print("  P1 Important:")
    print("    - INTEGRATE-010: 验证REQ-009子任务 (1h)")
    print("    - INTEGRATE-011: 验证REQ-010子任务 (1h)")
    print()
    print("  P2 Normal:")
    print("    - INTEGRATE-012: 集成企业级模板 (1h)")
    print("    - INTEGRATE-013: 验证TASK-C-3测试 (0.5h)")
    print("    - INTEGRATE-014: 验证BUG-001修复 (0.5h)")
    print()
    print("[总计] 原有8个 + 新增6个 = 14个集成任务")
    print("[总工时] 原22.5h + 新7h = 29.5小时")
    print()
    print("[Dashboard] http://localhost:8877")

if __name__ == "__main__":
    main()

