#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成v1.7完整功能清单（细粒度）
包含从v1.0到v1.7累积的所有功能
"""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# v1.7完整功能清单（细粒度）
FEATURES = {
    "implemented": [
        # ========== 基础设施层 (v1.0-v1.7) ==========
        {"id": "INFRA-001", "name": "SQLite数据库持久化", "type": "基础设施", "file": "database/data/tasks.db", "version": "v1.0", "completion": 1.0},
        {"id": "INFRA-002", "name": "StateManager状态管理", "type": "基础设施", "file": "automation/state_manager.py", "version": "v1.0", "completion": 1.0},
        {"id": "INFRA-003", "name": "3表任务数据库", "type": "基础设施", "file": "database/schemas/v1_tasks_schema.sql", "version": "v1.0", "completion": 1.0},
        {"id": "INFRA-004", "name": "任务CRUD操作", "type": "基础设施", "file": "automation/state_manager.py", "version": "v1.0", "completion": 1.0},
        {"id": "INFRA-005", "name": "配置系统(YAML)", "type": "基础设施", "file": "automation/config.py", "version": "v1.0", "completion": 1.0},
        {"id": "INFRA-006", "name": "知识库数据库扩展(12表)", "type": "基础设施", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "INFRA-007", "name": "数据库迁移工具", "type": "基础设施", "file": "database/migrations/migrate.py", "version": "v1.7", "completion": 1.0},
        {"id": "INFRA-008", "name": "端口管理器(PortManager)", "type": "基础设施", "file": "packages/shared-utils/port_manager.py", "version": "v1.7", "completion": 1.0},
        {"id": "INFRA-009", "name": "Monorepo目录结构", "type": "基础设施", "file": "docs/adr/0001-monorepo-structure.md", "version": "v1.7", "completion": 1.0},
        
        # ========== 任务管理核心 (v1.0-v1.5) ==========
        {"id": "TASK-001", "name": "任务创建和编辑", "type": "任务管理", "file": "automation/state_manager.py", "version": "v1.0", "completion": 1.0},
        {"id": "TASK-002", "name": "任务状态流转(5状态)", "type": "任务管理", "file": "automation/models.py", "version": "v1.0", "completion": 1.0},
        {"id": "TASK-003", "name": "任务优先级管理(P0-P3)", "type": "任务管理", "file": "automation/models.py", "version": "v1.0", "completion": 1.0},
        {"id": "TASK-004", "name": "任务依赖关系", "type": "任务管理", "file": "database/schemas/v1_tasks_schema.sql", "version": "v1.0", "completion": 1.0},
        {"id": "TASK-005", "name": "任务完成详情记录", "type": "任务管理", "file": "database/schemas/v1_tasks_schema.sql", "version": "v1.0", "completion": 1.0},
        {"id": "TASK-006", "name": "任务分配给Worker", "type": "任务管理", "file": "automation/task_scheduler.py", "version": "v1.0", "completion": 1.0},
        
        # ========== 依赖分析引擎 (v1.5) ==========
        {"id": "DEP-001", "name": "循环依赖检测(DFS算法)", "type": "算法", "file": "automation/dependency_analyzer.py", "version": "v1.5", "completion": 1.0},
        {"id": "DEP-002", "name": "拓扑排序(Kahn算法)", "type": "算法", "file": "automation/dependency_analyzer.py", "version": "v1.5", "completion": 1.0},
        {"id": "DEP-003", "name": "关键路径分析(CPM)", "type": "算法", "file": "automation/dependency_analyzer.py", "version": "v1.5", "completion": 1.0},
        {"id": "DEP-004", "name": "并行任务分组", "type": "算法", "file": "automation/dependency_analyzer.py", "version": "v1.5", "completion": 1.0},
        
        # ========== 任务调度系统 (v1.5) ==========
        {"id": "SCHED-001", "name": "Worker注册管理", "type": "调度", "file": "automation/task_scheduler.py", "version": "v1.5", "completion": 1.0},
        {"id": "SCHED-002", "name": "任务负载均衡", "type": "调度", "file": "automation/task_scheduler.py", "version": "v1.5", "completion": 1.0},
        {"id": "SCHED-003", "name": "能力匹配分配", "type": "调度", "file": "automation/task_scheduler.py", "version": "v1.5", "completion": 1.0},
        {"id": "SCHED-004", "name": "Worker健康检查", "type": "调度", "file": "automation/task_scheduler.py", "version": "v1.5", "completion": 1.0},
        
        # ========== Dashboard界面 (v1.0-v1.6) ==========
        {"id": "UI-001", "name": "实时任务列表", "type": "前端", "file": "industrial_dashboard/dashboard.py", "version": "v1.0", "completion": 1.0},
        {"id": "UI-002", "name": "统计卡片(4个指标)", "type": "前端", "file": "industrial_dashboard/templates.py", "version": "v1.0", "completion": 1.0},
        {"id": "UI-003", "name": "进度条可视化", "type": "前端", "file": "industrial_dashboard/templates.py", "version": "v1.0", "completion": 1.0},
        {"id": "UI-004", "name": "自动刷新(10秒)", "type": "前端", "file": "industrial_dashboard/templates.py", "version": "v1.0", "completion": 1.0},
        {"id": "UI-005", "name": "工业美学设计", "type": "前端", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        {"id": "UI-006", "name": "浅色主题+等宽字体", "type": "前端", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        {"id": "UI-007", "name": "Tab切换功能", "type": "前端", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        {"id": "UI-008", "name": "多模块Dashboard", "type": "前端", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        
        # ========== API服务 (v1.0-v1.5) ==========
        {"id": "API-001", "name": "RESTful API框架(FastAPI)", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.0", "completion": 1.0},
        {"id": "API-002", "name": "GET /api/tasks", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.0", "completion": 1.0},
        {"id": "API-003", "name": "GET /api/stats", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.0", "completion": 1.0},
        {"id": "API-004", "name": "GET /health健康检查", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.0", "completion": 1.0},
        {"id": "API-005", "name": "CORS跨域配置", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.0", "completion": 1.0},
        {"id": "API-006", "name": "GET /api/dependencies/*", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.5", "completion": 1.0},
        
        # ========== v1.7 新增API (架构师相关) ==========
        {"id": "API-007", "name": "GET /api/project_scan", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.7", "completion": 1.0},
        {"id": "API-008", "name": "GET /api/architect_monitor", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.7", "completion": 1.0},
        {"id": "API-009", "name": "GET /api/architect_events", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.7", "completion": 1.0},
        {"id": "API-010", "name": "GET /api/developer_knowledge/*", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.7", "completion": 1.0},
        {"id": "API-011", "name": "GET /api/tester_knowledge/*", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.7", "completion": 1.0},
        {"id": "API-012", "name": "GET /api/ops_knowledge/*", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.7", "completion": 1.0},
        {"id": "API-013", "name": "GET /api/delivery_docs/*", "type": "后端API", "file": "industrial_dashboard/dashboard.py", "version": "v1.7", "completion": 1.0},
        {"id": "API-014", "name": "Architect API路由(6个端点)", "type": "后端API", "file": "apps/api/src/routes/architect.py", "version": "v1.7", "completion": 1.0},
        
        # ========== AI体系 (v1.7核心创新) ==========
        {"id": "AI-001", "name": "架构师AI Prompt(8000字)", "type": "AI文档", "file": "docs/ai/architect-system-prompt-expert.md", "version": "v1.7", "completion": 1.0},
        {"id": "AI-002", "name": "全栈工程师AI Prompt(7000字)", "type": "AI文档", "file": "docs/ai/fullstack-engineer-system-prompt.md", "version": "v1.7", "completion": 1.0},
        {"id": "AI-003", "name": "代码管家AI Prompt(5000字)", "type": "AI文档", "file": "docs/ai/code-steward-system-prompt.md", "version": "v1.7", "completion": 1.0},
        {"id": "AI-004", "name": "SRE AI Prompt(4500字)", "type": "AI文档", "file": "docs/ai/sre-system-prompt.md", "version": "v1.7", "completion": 1.0},
        {"id": "AI-005", "name": "AI团队协作指南", "type": "AI文档", "file": "docs/ai/AI-TEAM-GUIDE.md", "version": "v1.7", "completion": 1.0},
        {"id": "AI-006", "name": "Cursor使用指南", "type": "AI文档", "file": "docs/ai/how-to-use-architect-with-cursor.md", "version": "v1.7", "completion": 1.0},
        {"id": "AI-007", "name": "架构师入职清单", "type": "AI文档", "file": "docs/ai/architect-onboarding-checklist.md", "version": "v1.7", "completion": 1.0},
        {"id": "AI-008", "name": "任务提示词模板", "type": "AI文档", "file": "docs/ai/task-prompt-template.md", "version": "v1.7", "completion": 1.0},
        {"id": "AI-009", "name": "ArchitectOrchestrator服务", "type": "AI服务", "file": "apps/api/src/services/architect_orchestrator.py", "version": "v1.7", "completion": 0.9},
        {"id": "AI-010", "name": "架构分析JSON模型(Pydantic)", "type": "AI服务", "file": "apps/api/src/services/architect_orchestrator.py", "version": "v1.7", "completion": 1.0},
        {"id": "AI-011", "name": "任务看板Markdown生成", "type": "AI服务", "file": "apps/api/src/services/architect_orchestrator.py", "version": "v1.7", "completion": 1.0},
        {"id": "AI-012", "name": "交接快照保存", "type": "AI服务", "file": "apps/api/src/services/architect_orchestrator.py", "version": "v1.7", "completion": 1.0},
        
        # ========== 知识库系统 (v1.7) ==========
        {"id": "KB-001", "name": "projects项目表", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-002", "name": "components组件表", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-003", "name": "issues问题记录表", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-004", "name": "solutions解决方案表", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-005", "name": "decisions技术决策表", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-006", "name": "knowledge_articles知识文章表", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-007", "name": "tools工具表", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-008", "name": "component_tools组件工具关联", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-009", "name": "deployments部署记录表", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        {"id": "KB-010", "name": "知识图谱查询能力", "type": "知识库", "file": "database/schemas/v2_knowledge_schema.sql", "version": "v1.7", "completion": 1.0},
        
        # ========== Dashboard数据层 (v1.7今天完成) ==========
        {"id": "DATA-001", "name": "开发者知识库(4文档)", "type": "Dashboard数据", "file": "automation-data/developer-knowledge/", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-002", "name": "测试知识库(2文档)", "type": "Dashboard数据", "file": "automation-data/tester-knowledge/", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-003", "name": "运维知识库(4文档)", "type": "Dashboard数据", "file": "automation-data/ops/", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-004", "name": "交付文档(2文档)", "type": "Dashboard数据", "file": "automation-data/delivery-docs/", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-005", "name": "项目背景(2文档)", "type": "Dashboard数据", "file": "automation-data/01-background/", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-006", "name": "模块数据库(2JSON)", "type": "Dashboard数据", "file": "automation-data/02-modules-db/", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-007", "name": "标准规范文档", "type": "Dashboard数据", "file": "automation-data/08-standards/", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-008", "name": "架构师监控数据", "type": "Dashboard数据", "file": "automation-data/architect_monitor.json", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-009", "name": "架构师事件流(12事件)", "type": "Dashboard数据", "file": "automation-data/architect_events.json", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-010", "name": "架构师对话记录", "type": "Dashboard数据", "file": "automation-data/architect-conversations.json", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-011", "name": "架构师重要信息(4文档)", "type": "Dashboard数据", "file": "automation-data/architect-notes/", "version": "v1.7", "completion": 1.0},
        {"id": "DATA-012", "name": "AI提示词加载(172KB)", "type": "Dashboard数据", "file": "automation-data/09-role-prompts/", "version": "v1.7", "completion": 1.0},
        
        # ========== 文档体系 (v1.7) ==========
        {"id": "DOC-001", "name": "架构审查报告(9000字)", "type": "文档", "file": "docs/arch/architecture-review.md", "version": "v1.7", "completion": 1.0},
        {"id": "DOC-002", "name": "任务看板文档", "type": "文档", "file": "docs/tasks/task-board.md", "version": "v1.7", "completion": 1.0},
        {"id": "DOC-003", "name": "ADR架构决策记录", "type": "文档", "file": "docs/adr/0001-monorepo-structure.md", "version": "v1.7", "completion": 1.0},
        {"id": "DOC-004", "name": "架构师工作流程文档", "type": "文档", "file": "docs/arch/architect-workflow.md", "version": "v1.7", "completion": 1.0},
        {"id": "DOC-005", "name": "Phase完成报告(6份)", "type": "文档", "file": "docs/reports/", "version": "v1.7", "completion": 1.0},
        {"id": "DOC-006", "name": "快速使用指南", "type": "文档", "file": "📖快速使用指南.md", "version": "v1.7", "completion": 1.0},
        {"id": "DOC-007", "name": "AI文档完整索引", "type": "文档", "file": "📚AI文档完整索引.md", "version": "v1.7", "completion": 1.0},
        {"id": "DOC-008", "name": "START_HERE入口文档", "type": "文档", "file": "📍START_HERE.md", "version": "v1.7", "completion": 1.0},
        
        # ========== 工具脚本 (v1.7) ==========
        {"id": "TOOL-001", "name": "任务录入脚本", "type": "工具", "file": "scripts/create_v17_tasks.py", "version": "v1.7", "completion": 1.0},
        {"id": "TOOL-002", "name": "Schema修复脚本", "type": "工具", "file": "scripts/fix_schema_for_dashboard.py", "version": "v1.7", "completion": 1.0},
        {"id": "TOOL-003", "name": "Dashboard数据更新脚本", "type": "工具", "file": "scripts/update_dashboard_data_v17.py", "version": "v1.7", "completion": 1.0},
        {"id": "TOOL-004", "name": "数据库测试脚本", "type": "工具", "file": "scripts/test_knowledge_db.py", "version": "v1.7", "completion": 1.0},
        {"id": "TOOL-005", "name": "一键启动脚本", "type": "工具", "file": "🚀启动任务所.bat", "version": "v1.7", "completion": 1.0},
        
        # ========== Dashboard功能模块 (v1.6-v1.7) ==========
        {"id": "MOD-001", "name": "功能清单模块(3 Tab)", "type": "Dashboard模块", "file": "industrial_dashboard/templates.py", "version": "v1.7", "completion": 1.0},
        {"id": "MOD-002", "name": "待完成任务列表", "type": "Dashboard模块", "file": "industrial_dashboard/templates.py", "version": "v1.7", "completion": 1.0},
        {"id": "MOD-003", "name": "ARCHITECT MONITOR(4 Tab)", "type": "Dashboard模块", "file": "industrial_dashboard/templates.py", "version": "v1.7", "completion": 1.0},
        {"id": "MOD-004", "name": "AI代码管家模块", "type": "Dashboard模块", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        {"id": "MOD-005", "name": "测试工程师模块", "type": "Dashboard模块", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        {"id": "MOD-006", "name": "交付工程师模块", "type": "Dashboard模块", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        {"id": "MOD-007", "name": "运维SRE模块", "type": "Dashboard模块", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        {"id": "MOD-008", "name": "UX/UI确认模块", "type": "Dashboard模块", "file": "industrial_dashboard/templates.py", "version": "v1.6", "completion": 1.0},
        
        # ========== 架构审查功能 (v1.7今天完成) ==========
        {"id": "ARCH-001", "name": "代码扫描能力", "type": "架构审查", "file": "docs/arch/architecture-review.md", "version": "v1.7", "completion": 1.0},
        {"id": "ARCH-002", "name": "功能识别(已实现/半成品)", "type": "架构审查", "file": "docs/arch/architecture-review.md", "version": "v1.7", "completion": 1.0},
        {"id": "ARCH-003", "name": "问题识别(Critical/High/Medium)", "type": "架构审查", "file": "docs/arch/architecture-review.md", "version": "v1.7", "completion": 1.0},
        {"id": "ARCH-004", "name": "代码质量评分(7维度)", "type": "架构审查", "file": "docs/arch/architecture-review.md", "version": "v1.7", "completion": 1.0},
        {"id": "ARCH-005", "name": "任务自动拆解", "type": "架构审查", "file": "docs/tasks/task-board.md", "version": "v1.7", "completion": 1.0},
        {"id": "ARCH-006", "name": "依赖关系识别", "type": "架构审查", "file": "database/data/tasks.db", "version": "v1.7", "completion": 1.0},
        {"id": "ARCH-007", "name": "优先级自动标注", "type": "架构审查", "file": "docs/tasks/task-board.md", "version": "v1.7", "completion": 1.0},
        {"id": "ARCH-008", "name": "工时自动预估", "type": "架构审查", "file": "docs/tasks/task-board.md", "version": "v1.7", "completion": 1.0},
    ],
    "partial": [
        # ========== Phase C: API集成（待完成） ==========
        {"id": "PART-001", "name": "FastAPI主应用入口(main.py)", "type": "后端", "completion": 0, "missing": ["apps/api/src/main.py文件不存在", "无法启动API服务"], "priority": "P0", "estimated_hours": 2.0, "task_id": "TASK-C-1"},
        {"id": "PART-002", "name": "ArchitectOrchestrator数据库集成", "type": "后端", "completion": 0.1, "missing": ["_ensure_project_exists()未实现", "_create_tasks_from_suggestions()未实现", "_create_issues_from_problems()未实现"], "priority": "P0", "estimated_hours": 3.0, "task_id": "TASK-C-2"},
        {"id": "PART-003", "name": "架构师API端到端测试", "type": "测试", "completion": 0, "missing": ["tests/integration/test_architect_api.py不存在", "无E2E测试脚本"], "priority": "P0", "estimated_hours": 1.5, "task_id": "TASK-C-3"},
        
        # ========== Phase D: 代码迁移（可选） ==========
        {"id": "PART-004", "name": "领域模型层(core-domain)", "type": "重构", "completion": 0, "missing": ["packages/core-domain/entities/目录为空", "models.py未迁移"], "priority": "P2", "estimated_hours": 2.0, "task_id": "TASK-D-1"},
        {"id": "PART-005", "name": "基础设施层(infra)", "type": "重构", "completion": 0, "missing": ["packages/infra/database/目录为空", "state_manager.py未迁移"], "priority": "P2", "estimated_hours": 3.0, "task_id": "TASK-D-2"},
        {"id": "PART-006", "name": "算法库(algorithms)", "type": "重构", "completion": 0, "missing": ["packages/algorithms/目录为空", "dependency_analyzer.py未迁移"], "priority": "P3", "estimated_hours": 1.5},
        
        # ========== 测试覆盖（待完善） ==========
        {"id": "PART-007", "name": "单元测试覆盖", "type": "测试", "completion": 0.05, "missing": ["覆盖率<5%", "核心模块无测试"], "priority": "P1", "estimated_hours": 8.0},
        {"id": "PART-008", "name": "集成测试", "type": "测试", "completion": 0, "missing": ["无API集成测试", "无数据库集成测试"], "priority": "P1", "estimated_hours": 4.0},
        
        # ========== 安全与性能（待完善） ==========
        {"id": "PART-009", "name": "API认证授权", "type": "安全", "completion": 0, "missing": ["无JWT认证", "无权限控制"], "priority": "P1", "estimated_hours": 6.0},
        {"id": "PART-010", "name": "性能优化", "type": "性能", "completion": 0.3, "missing": ["无缓存机制", "无连接池", "无并发优化"], "priority": "P2", "estimated_hours": 8.0},
        {"id": "PART-011", "name": "错误处理统一化", "type": "质量", "completion": 0.5, "missing": ["部分模块错误处理不完整", "无统一异常处理中间件"], "priority": "P2", "estimated_hours": 4.0},
        
        # ========== 文档完善（待完善） ==========
        {"id": "PART-012", "name": "API文档(OpenAPI)", "type": "文档", "completion": 0.3, "missing": ["仅有/docs自动文档", "缺少使用示例"], "priority": "P2", "estimated_hours": 3.0},
    ],
    "conflicts": [
        # ========== Critical级别（必须立即解决） ==========
        {"id": "CONF-001", "name": "FastAPI主入口缺失", "severity": "Critical", "impact": "架构师API完全无法启动，核心功能不可用", "affected_features": ["AI-009", "API-014"], "suggestion": "立即创建apps/api/src/main.py，参考dashboard.py结构", "blocking_tasks": ["TASK-C-2", "TASK-C-3"], "estimated_fix_hours": 2.0},
        {"id": "CONF-002", "name": "ArchitectOrchestrator数据库未集成", "severity": "Critical", "impact": "架构分析无法持久化，数据库写入全是TODO", "affected_features": ["AI-009"], "suggestion": "临时从v1.6引用StateManager或快速迁移到packages/infra/", "blocking_tasks": ["TASK-C-3"], "estimated_fix_hours": 3.0},
        
        # ========== High级别（建议本周解决） ==========
        {"id": "CONF-003", "name": "缺少单元测试", "severity": "High", "impact": "代码质量无法保证，重构风险高", "affected_features": ["所有代码模块"], "suggestion": "优先为核心模块添加测试，目标覆盖率50%+", "blocking_tasks": [], "estimated_fix_hours": 8.0},
        {"id": "CONF-004", "name": "无API认证授权", "severity": "High", "impact": "API完全开放，生产环境安全风险", "affected_features": ["API-002", "API-003", "API-007~014"], "suggestion": "添加JWT认证+RBAC权限控制", "blocking_tasks": [], "estimated_fix_hours": 6.0},
        
        # ========== Medium级别（可以延后） ==========
        {"id": "CONF-005", "name": "Dashboard代码位置不合理", "severity": "Medium", "impact": "automation模块在dashboard/src/下，架构不清晰", "affected_features": ["INFRA-002", "DEP-001~004"], "suggestion": "保持现状，v1.6独立运行，v1.7专注AI体系", "blocking_tasks": [], "estimated_fix_hours": 0},
        {"id": "CONF-006", "name": "SQLite并发写入限制", "severity": "Medium", "impact": "QPS>100时可能出现database locked错误", "affected_features": ["INFRA-001"], "suggestion": "添加连接池+重试机制，或切换PostgreSQL", "blocking_tasks": [], "estimated_fix_hours": 4.0},
        {"id": "CONF-007", "name": "缺少性能测试", "severity": "Medium", "impact": "不知道系统性能瓶颈在哪", "affected_features": ["所有API"], "suggestion": "使用locust/ab进行压测，建立性能基线", "blocking_tasks": [], "estimated_fix_hours": 3.0},
        
        # ========== Low级别（技术债） ==========
        {"id": "CONF-008", "name": "代码重复(Service层)", "severity": "Low", "impact": "可维护性下降", "affected_features": [], "suggestion": "抽取装饰器统一错误处理", "blocking_tasks": [], "estimated_fix_hours": 4.0},
        {"id": "CONF-009", "name": "配置管理分散", "severity": "Low", "impact": "配置难以统一管理", "affected_features": ["INFRA-005"], "suggestion": "集中到config/目录，使用配置类", "blocking_tasks": [], "estimated_fix_hours": 2.0},
    ],
    "summary": {
        "total": 0,  # 将计算
        "by_version": {},
        "by_type": {},
        "partial_total": 0,
        "conflicts_total": 0,
        "conflicts_by_severity": {}
    }
}

# 计算统计
features = FEATURES["implemented"]
partial = FEATURES["partial"]
conflicts = FEATURES["conflicts"]

FEATURES["summary"]["total"] = len(features)
FEATURES["summary"]["partial_total"] = len(partial)
FEATURES["summary"]["conflicts_total"] = len(conflicts)

# 计算统计
features = FEATURES["implemented"]
FEATURES["summary"]["total"] = len(features)

# 按版本分组
by_version = {}
for f in features:
    v = f["version"]
    by_version[v] = by_version.get(v, 0) + 1
FEATURES["summary"]["by_version"] = by_version

# 按类型分组
by_type = {}
for f in features:
    t = f["type"]
    by_type[t] = by_type.get(t, 0) + 1
FEATURES["summary"]["by_type"] = by_type

# 输出
print("\n" + "="*70)
print("v1.7完整功能清单（细粒度）")
print("="*70)
print(f"\n总功能数: {len(features)}")
print(f"\n按版本分组:")
for v, count in sorted(by_version.items()):
    print(f"  {v}: {count}个")
print(f"\n按类型分组:")
for t, count in sorted(by_type.items()):
    print(f"  {t}: {count}个")
print()

# 保存JSON
output_file = "apps/dashboard/automation-data/v17-complete-features.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(FEATURES, f, ensure_ascii=False, indent=2)

print(f"✅ 已保存到: {output_file}")
print(f"\n总计: {len(features)}个已实现功能")
print("="*70 + "\n")

