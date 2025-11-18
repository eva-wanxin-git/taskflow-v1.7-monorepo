#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整更新功能清单 - 添加部分实现和冲突建议
"""
import json
from pathlib import Path

# 功能清单文件路径
features_file = Path(__file__).parent / "apps" / "dashboard" / "automation-data" / "v17-complete-features.json"

# 读取现有功能
with open(features_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Current status:")
print(f"  Implemented: {len(data['implemented'])}")
print(f"  Partial: {len(data.get('partial', []))}")
print(f"  Conflicts: {len(data.get('conflicts', []))}")

# ============================================
# 1. 添加部分实现功能（架构师发现的）
# ============================================
new_partial_features = [
    {
        "id": "ARCH-PARTIAL-001",
        "name": "FastAPI主应用入口",
        "type": "基础设施",
        "file": "apps/api/src/main.py",
        "version": "v1.7",
        "completion": 0.0,
        "missing": [
            "main.py文件不存在",
            "无法启动API服务",
            "无法访问架构师API"
        ],
        "risk": "Critical - 阻塞Phase C所有任务",
        "priority": "P0",
        "estimated_fix_hours": 2.0
    },
    {
        "id": "ARCH-PARTIAL-002",
        "name": "ArchitectOrchestrator数据库集成",
        "type": "架构师服务",
        "file": "apps/api/src/services/architect_orchestrator.py",
        "version": "v1.7",
        "completion": 0.1,
        "missing": [
            "_ensure_project_exists() - TODO",
            "_ensure_components_exist() - TODO",
            "_create_tasks_from_suggestions() - TODO",
            "_create_issues_from_problems() - TODO",
            "_create_feature_articles() - TODO"
        ],
        "risk": "Critical - 提交架构分析后无法写入数据库",
        "priority": "P0",
        "estimated_fix_hours": 3.0
    },
    {
        "id": "ARCH-PARTIAL-003",
        "name": "领域模型层(core-domain)",
        "type": "基础设施",
        "file": "packages/core-domain/entities/",
        "version": "v1.7",
        "completion": 0.0,
        "missing": [
            "entities/目录为空",
            "repositories/目录为空",
            "use-cases/目录为空",
            "需要迁移models.py"
        ],
        "risk": "Medium - 不影响Phase C，但影响长期架构",
        "priority": "P2",
        "estimated_fix_hours": 2.0
    },
    {
        "id": "ARCH-PARTIAL-004",
        "name": "基础设施层(infra)",
        "type": "基础设施",
        "file": "packages/infra/database/",
        "version": "v1.7",
        "completion": 0.0,
        "missing": [
            "database/目录为空（需要StateManager）",
            "llm/目录为空",
            "monitoring/目录为空"
        ],
        "risk": "Medium - 不影响Phase C，代码位置不规范",
        "priority": "P2",
        "estimated_fix_hours": 3.0
    },
    {
        "id": "ARCH-PARTIAL-005",
        "name": "算法库(algorithms)",
        "type": "基础设施",
        "file": "packages/algorithms/",
        "version": "v1.7",
        "completion": 0.0,
        "missing": [
            "目录为空",
            "需要迁移dependency_analyzer.py等"
        ],
        "risk": "Low - v1.6中可用，位置不影响功能",
        "priority": "P3",
        "estimated_fix_hours": 1.5
    }
]

# ============================================
# 2. 添加架构师的冲突/建议
# ============================================
new_conflicts = [
    {
        "id": "ARCH-ADVICE-001",
        "name": "Phase C是唯一的P0任务",
        "severity": "Strategic",
        "impact": "v1.7的核心价值是AI体系，不是Monorepo",
        "affected_features": [
            "ARCH-PARTIAL-001",
            "ARCH-PARTIAL-002"
        ],
        "suggestion": "聚焦Phase C(6.5小时)实现架构师API，Phase D(代码迁移)可延后或跳过",
        "blocking_tasks": [],
        "estimated_fix_hours": 6.5,
        "rationale": [
            "AI Prompts 25000字已完成 ⭐⭐⭐⭐⭐",
            "架构师API 90%完成,6.5小时可用 ⭐⭐⭐⭐⭐",
            "知识库12表已完成 ⭐⭐⭐⭐⭐",
            "代码迁移0%但v1.6可独立运行 ⭐⭐⭐",
            "遵循YAGNI原则"
        ]
    },
    {
        "id": "ARCH-ADVICE-002",
        "name": "进度数据不一致已修正",
        "severity": "Critical",
        "impact": "architecture-review和task-board显示60%，实际是46.3%",
        "affected_features": [],
        "suggestion": "已修正为46.3% (25/54任务)，基于2025-11-19 05:30最新扫描",
        "blocking_tasks": [],
        "estimated_fix_hours": 0,
        "details": "2025-11-18晚发现6个新完成任务+14个集成任务，准确统计后是46.3%"
    },
    {
        "id": "ARCH-ADVICE-003",
        "name": "v1.6应继续独立运行",
        "severity": "Strategic",
        "impact": "代码迁移到Monorepo不是必须的",
        "affected_features": [
            "ARCH-PARTIAL-003",
            "ARCH-PARTIAL-004",
            "ARCH-PARTIAL-005"
        ],
        "suggestion": "v1.6和v1.7并行运行，数据共享(同一数据库)，逐步迁移(如果需要)",
        "blocking_tasks": [],
        "estimated_fix_hours": 0,
        "rationale": [
            "v1.6代码完整稳定(3500行)",
            "Dashboard已复制到v1.7",
            "端口8877独立不冲突",
            "避免过度重构",
            "保持灵活性"
        ]
    },
    {
        "id": "ARCH-ADVICE-004",
        "name": "缺少E2E测试",
        "severity": "High",
        "impact": "架构师API无端到端测试验证",
        "affected_features": [
            "ARCH-PARTIAL-001",
            "ARCH-PARTIAL-002"
        ],
        "suggestion": "TASK-C.3: 编写完整E2E测试(1.5小时)，验证架构师工作流",
        "blocking_tasks": [
            "TASK-C-1",
            "TASK-C-2"
        ],
        "estimated_fix_hours": 1.5
    }
]

# ============================================
# 3. 检查并添加
# ============================================

# 添加部分实现功能
existing_partial_ids = {f['id'] for f in data.get('partial', [])}
new_partial_to_add = [f for f in new_partial_features if f['id'] not in existing_partial_ids]

if 'partial' not in data:
    data['partial'] = []

if new_partial_to_add:
    data['partial'].extend(new_partial_to_add)
    print(f"\n[OK] Added {len(new_partial_to_add)} partial features:")
    for feature in new_partial_to_add:
        print(f"  - {feature['id']}: {feature['name']}")

# 添加冲突/建议
existing_conflict_ids = {c['id'] for c in data.get('conflicts', [])}
new_conflicts_to_add = [c for c in new_conflicts if c['id'] not in existing_conflict_ids]

if 'conflicts' not in data:
    data['conflicts'] = []

if new_conflicts_to_add:
    data['conflicts'].extend(new_conflicts_to_add)
    print(f"\n[OK] Added {len(new_conflicts_to_add)} conflicts/suggestions:")
    for conflict in new_conflicts_to_add:
        print(f"  - {conflict['id']}: {conflict['name']}")

# 更新summary
if 'summary' in data:
    data['summary']['total'] = len(data['implemented'])
    data['summary']['partial'] = len(data['partial'])
    data['summary']['conflicts'] = len(data['conflicts'])

# 写回文件
with open(features_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"Final status:")
print(f"  Implemented: {len(data['implemented'])} (+{len([f for f in data['implemented'] if f['id'].startswith('ARCH-')])})")
print(f"  Partial: {len(data['partial'])} (+{len(new_partial_to_add)})")
print(f"  Conflicts: {len(data['conflicts'])} (+{len(new_conflicts_to_add)})")
print(f"{'='*60}")

