#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新功能清单 - 添加架构师工作成果
"""
import json
from pathlib import Path

# 功能清单文件路径
features_file = Path(__file__).parent / "apps" / "dashboard" / "automation-data" / "v17-complete-features.json"

# 读取现有功能
with open(features_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"当前已实现功能数: {len(data['implemented'])}")

# 添加架构师新完成的功能
new_features = [
    {
        "id": "ARCH-DOC-001",
        "name": "架构清单文档(architecture-inventory.md)",
        "type": "架构文档",
        "file": "docs/arch/architecture-inventory.md",
        "version": "v1.7",
        "completion": 1.0,
        "details": "完整的项目架构清单,5000+字,包含技术栈/目录结构/核心模块/技术债务"
    },
    {
        "id": "ARCH-DOC-002",
        "name": "重构计划文档(refactor-plan.md)",
        "type": "架构文档",
        "file": "docs/arch/refactor-plan.md",
        "version": "v1.7",
        "completion": 1.0,
        "details": "Phase C/D/E完整重构计划,8000+字,包含详细实现要点和价值分析"
    },
    {
        "id": "ARCH-DOC-003",
        "name": "架构审查报告更新",
        "type": "架构文档",
        "file": "docs/arch/architecture-review.md",
        "version": "v1.7",
        "completion": 1.0,
        "details": "修正进度数据(60%→46.3%),更新审查时间"
    },
    {
        "id": "ARCH-DOC-004",
        "name": "任务看板更新",
        "type": "架构文档",
        "file": "docs/tasks/task-board.md",
        "version": "v1.7",
        "completion": 1.0,
        "details": "更新项目状态(54个任务统计),修正端口信息"
    },
    {
        "id": "ARCH-WORK-001",
        "name": "架构师工作总结文档",
        "type": "架构文档",
        "file": "📍架构师工作总结-2025-11-19-06-00.md",
        "version": "v1.7",
        "completion": 1.0,
        "details": "Phase 0-4完整工作记录,核心发现与建议,15000字"
    },
    {
        "id": "ARCH-ANALYSIS-001",
        "name": "架构师Phase 0-4工作流程",
        "type": "架构师能力",
        "file": "docs/ai/architect-system-prompt-expert.md",
        "version": "v1.7",
        "completion": 1.0,
        "details": "完成启动/扫描/映射/审查/任务板5个阶段,30分钟产出5份文档"
    }
]

# 检查是否已存在这些功能（避免重复添加）
existing_ids = {feature['id'] for feature in data['implemented']}
new_to_add = [f for f in new_features if f['id'] not in existing_ids]

if new_to_add:
    data['implemented'].extend(new_to_add)
    print(f"\n[OK] Added {len(new_to_add)} new features:")
    for feature in new_to_add:
        print(f"  - {feature['id']}: {feature['name']}")
    
    # 写回文件
    with open(features_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal features: {len(data['implemented'])}")
else:
    print("\n[INFO] All features already exist")

print(f"\nFeature summary:")
print(f"  Implemented: {len(data['implemented'])}")
print(f"  Partial: {len(data.get('partial', []))}")

