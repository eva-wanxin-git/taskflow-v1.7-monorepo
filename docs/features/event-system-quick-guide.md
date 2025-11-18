# 事件系统快速使用指南

## 📖 概述

任务所·Flow v1.7 事件系统提供完整的事件发射、存储和查询功能，用于追踪项目中发生的所有关键操作。

## 🚀 快速开始

### 1. 在脚本中使用

```python
from shared_utils.event_helper import create_event_helper

# 创建EventHelper实例
helper = create_event_helper(
    project_id="TASKFLOW",
    actor="your_name",
    source="ai"  # 或 "system", "user", "external"
)

# 触发事件
event = helper.task_created(
    task_id="TASK-001",
    title="实现XXX功能",
    priority="P0",
    assigned_to="engineer",
    estimated_hours=4.0
)

print(f"事件已触发: {event['id']}")
```

### 2. 通过API触发

**开始任务**:
```bash
curl -X PUT http://127.0.0.1:8877/api/tasks/TASK-001/start \
  -H "Content-Type: application/json" \
  -d '{"actor": "engineer", "work_plan": "实施计划"}'
```

**完成任务**:
```bash
curl -X POST http://127.0.0.1:8877/api/tasks/TASK-001/complete \
  -H "Content-Type: application/json" \
  -d '{"actor": "engineer", "actual_hours": 2.5}'
```

**批准任务**:
```bash
curl -X POST http://127.0.0.1:8877/api/tasks/TASK-001/approve \
  -H "Content-Type: application/json" \
  -d '{"reviewer": "architect", "score": 95}'
```

### 3. 查询事件

```bash
# 查询任务相关的所有事件
curl http://127.0.0.1:8877/api/events?related_entity_type=task&related_entity_id=TASK-001

# 查询特定类型的事件
curl http://127.0.0.1:8877/api/events?event_type=task.completed

# 查询特定分类的事件
curl http://127.0.0.1:8877/api/events?category=task

# 分页查询
curl http://127.0.0.1:8877/api/events?page=1&page_size=20
```

## 📋 事件类型

### 任务生命周期事件

| 事件类型 | 方法 | 说明 |
|---------|------|------|
| task.created | `helper.task_created()` | 任务创建 |
| task.dispatched | `helper.task_dispatched()` | 任务派发 |
| task.started | `helper.task_started()` | 任务开始 |
| task.completed | `helper.task_completed()` | 任务完成 |
| task.approved | `helper.task_approved()` | 任务批准 |
| task.rejected | `helper.task_rejected()` | 任务拒绝 |

### 功能事件

| 事件类型 | 方法 | 说明 |
|---------|------|------|
| feature.integrated | `helper.feature_integrated()` | 功能集成 |
| feature.deployed | `helper.feature_deployed()` | 功能部署 |

### 问题事件

| 事件类型 | 方法 | 说明 |
|---------|------|------|
| issue.discovered | `helper.issue_discovered()` | 问题发现 |
| issue.resolved | `helper.issue_resolved()` | 问题解决 |

### 决策事件

| 事件类型 | 方法 | 说明 |
|---------|------|------|
| decision.recorded | `helper.decision_recorded()` | 决策记录 |

### 系统事件

| 事件类型 | 方法 | 说明 |
|---------|------|------|
| milestone.reached | `helper.milestone_reached()` | 里程碑达成 |
| risk.identified | `helper.risk_identified()` | 风险识别 |
| architect.handover | `helper.architect_handover()` | 架构师交接 |

## 🔍 使用场景

### 场景1: 录入新任务

```python
# 1. 创建任务到数据库
# ... (数据库操作)

# 2. 触发task_created事件
helper.task_created(
    task_id="REQ-001",
    title="实现Token同步功能",
    priority="P0",
    assigned_to="fullstack-engineer",
    estimated_hours=4.0
)

# 3. 触发task_dispatched事件
helper.task_dispatched(
    task_id="REQ-001",
    assigned_to="fullstack-engineer",
    reason="根据技能和负载自动分配"
)
```

### 场景2: 工程师开始任务

```python
# 1. 更新任务状态
# ... (数据库操作)

# 2. 触发task_started事件
helper.task_started(
    task_id="REQ-001",
    actor="李明（全栈工程师）",
    work_plan="1. 理解需求 2. 设计方案 3. 编码实现 4. 自测",
    planned_completion="2025-11-19T18:00:00"
)
```

### 场景3: 工程师完成任务

```python
# 1. 更新任务状态
# ... (数据库操作)

# 2. 触发task_completed事件
helper.task_completed(
    task_id="REQ-001",
    actor="李明（全栈工程师）",
    actual_hours=3.5,
    files_modified=[
        "apps/api/src/routes/token_sync.py",
        "packages/shared-utils/token_manager.py"
    ],
    completion_summary="Token同步功能已完成，测试通过"
)
```

### 场景4: 架构师审查任务

```python
# 审查通过
helper.task_approved(
    task_id="REQ-001",
    reviewer="AI架构师",
    score=95,
    feedback="代码质量优秀，文档完整，测试覆盖充分，批准通过！"
)

# 或审查不通过
helper.task_rejected(
    task_id="REQ-001",
    reviewer="AI架构师",
    reason="需要补充单元测试，文档需要更详细"
)
```

### 场景5: 集成功能到组件

```python
helper.feature_integrated(
    feature_id="REQ-001",
    component="api",
    description="Token同步功能已成功集成到API模块",
    version="v1.7.0"
)
```

### 场景6: 发现问题

```python
helper.issue_discovered(
    issue_id="ISS-001",
    title="Token同步延迟过高",
    severity="high",  # low/medium/high/critical
    component="api",
    impact="影响用户体验，需要优化"
)
```

### 场景7: 解决问题

```python
helper.issue_resolved(
    issue_id="ISS-001",
    solution="优化数据库查询，添加索引",
    resolved_by="李明（全栈工程师）",
    time_spent=1.5
)
```

## 📊 事件数据结构

每个事件包含以下字段：

```json
{
  "id": "EVT-f0130f81",
  "project_id": "TASKFLOW",
  "event_type": "task.created",
  "event_category": "task",
  "source": "ai",
  "actor": "architect",
  "title": "任务创建: 实现Token同步功能",
  "description": "新任务 REQ-001 已创建",
  "data": {
    "task_id": "REQ-001",
    "priority": "P0",
    "assigned_to": "fullstack-engineer",
    "estimated_hours": 4.0
  },
  "related_entity_type": "task",
  "related_entity_id": "REQ-001",
  "severity": "info",
  "status": "processed",
  "tags": ["task", "created", "P0"],
  "occurred_at": "2025-11-18T21:00:00",
  "created_at": "2025-11-18T21:00:01"
}
```

## 🛠️ 高级用法

### 批量发射事件

```python
from shared_utils.event_helper import create_event_helper

helper = create_event_helper(project_id="TASKFLOW")

# 批量发射
events = []

events.append({
    "event_type": "task.created",
    "title": "任务1创建",
    "description": "...",
    "data": {"task_id": "TASK-001"}
})

events.append({
    "event_type": "task.created",
    "title": "任务2创建",
    "description": "...",
    "data": {"task_id": "TASK-002"}
})

# 使用底层EventEmitter批量发射
results = helper.emitter.emit_batch("TASKFLOW", events)
```

### 自定义事件

```python
# 使用底层emit方法发射自定义事件
event = helper.emitter.emit(
    project_id="TASKFLOW",
    event_type="custom.action",
    title="自定义操作",
    description="执行了某个自定义操作",
    data={"key": "value"},
    category="general",
    source="system",
    actor="custom_actor",
    severity="info",
    related_entity_type="custom",
    related_entity_id="CUSTOM-001",
    tags=["custom", "action"]
)
```

### 事件查询（编程方式）

```python
from core_domain.src.services.event_service import EventStore

store = EventStore(db_path="database/data/tasks.db")

# 查询所有事件
events = store.query(project_id="TASKFLOW")

# 按类型查询
events = store.query(
    project_id="TASKFLOW",
    event_type="task.completed"
)

# 按分类查询
events = store.query(
    project_id="TASKFLOW",
    category="task"
)

# 按严重性查询
events = store.query(
    project_id="TASKFLOW",
    severity="error"
)

# 按关联实体查询
events = store.query(
    project_id="TASKFLOW",
    related_entity_type="task",
    related_entity_id="REQ-001"
)

# 分页查询
events = store.query(
    project_id="TASKFLOW",
    page=1,
    page_size=20
)

# 获取统计
stats = store.get_stats(project_id="TASKFLOW")
print(f"总事件数: {stats['total_events']}")
print(f"今日事件: {stats['events_today']}")
```

## 📈 事件统计

事件系统自动维护统计信息：

```python
from core_domain.src.services.event_service import EventStore

store = EventStore()
stats = store.get_stats(project_id="TASKFLOW")

# 统计信息包括：
# - total_events: 总事件数
# - events_today: 今日事件数
# - events_this_week: 本周事件数
# - events_this_month: 本月事件数
# - task_events: 任务事件数
# - issue_events: 问题事件数
# - decision_events: 决策事件数
# - info_events: info级别事件数
# - warning_events: warning级别事件数
# - error_events: error级别事件数
# - critical_events: critical级别事件数
```

## 🔒 最佳实践

### 1. 始终记录关键操作

任何改变任务状态、创建/解决问题、做出技术决策的操作，都应该触发事件。

### 2. 使用正确的事件类型

选择最合适的事件类型，而不是都用通用的"general"事件。

### 3. 提供完整的事件数据

在data字段中包含足够的信息，以便后续分析和审计。

### 4. 设置正确的actor

明确指出是谁触发的事件（architect, engineer, system等）。

### 5. 关联正确的实体

使用related_entity_type和related_entity_id关联事件与具体的任务、问题等。

### 6. 使用合适的严重性

- `info`: 正常操作
- `warning`: 需要关注的操作（如任务拒绝、问题发现）
- `error`: 错误操作
- `critical`: 关键事件（如里程碑、重大决策）

## 🐛 故障排查

### 问题1: 事件未保存到数据库

**原因**: 数据库文件路径错误或权限问题

**解决**: 检查数据库路径和文件权限

```python
from pathlib import Path

db_path = Path("database/data/tasks.db")
print(f"数据库存在: {db_path.exists()}")
print(f"可写: {os.access(db_path, os.W_OK)}")
```

### 问题2: SQL语法错误

**原因**: 事件分类或严重性参数不正确

**解决**: 确保使用正确的枚举值或字符串

```python
# ✓ 正确
helper.task_created(..., category="task", severity="info")

# ✗ 错误
helper.task_created(..., category="EventCategory.TASK", severity="EventSeverity.INFO")
```

### 问题3: API返回404

**原因**: Dashboard未重启，新API端点未加载

**解决**: 重启Dashboard

```bash
# 停止Dashboard（Ctrl+C）
# 重新启动
cd taskflow-v1.7-monorepo
python apps/dashboard/start_dashboard.py
```

## 📚 相关文档

- [EventHelper API文档](../../packages/shared-utils/event_helper.py)
- [EventService实现](../../packages/core-domain/src/services/event_service.py)
- [数据库Schema](../../database/schemas/v3_events_schema.sql)
- [API文档](../api/events-api.md)
- [完成报告](../../✅REQ-010-C-完成报告.md)

## 🆘 获取帮助

如果遇到问题：

1. 查看测试脚本: `tests/test_event_integration.py`
2. 参考示例脚本: `scripts/示例-*.py`
3. 运行测试验证: `python tests/test_event_integration.py`
4. 查看完成报告: `✅REQ-010-C-完成报告.md`

---

**文档版本**: v1.0  
**最后更新**: 2025-11-18  
**维护者**: 全栈工程师AI

