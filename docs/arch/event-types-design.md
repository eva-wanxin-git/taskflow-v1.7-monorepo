# 📊 任务所·Flow 项目事件类型体系设计

> **文档版本**: v1.0  
> **创建时间**: 2025-11-18  
> **设计者**: AI架构师  
> **状态**: ✅ 设计完成

---

## 📋 目录

1. [概述](#概述)
2. [事件类型定义](#事件类型定义)
3. [事件数据结构](#事件数据结构)
4. [事件优先级体系](#事件优先级体系)
5. [事件聚合规则](#事件聚合规则)
6. [事件过滤规则](#事件过滤规则)
7. [实现建议](#实现建议)

---

## 概述

### 设计目标

为任务所·Flow建立统一的项目事件体系，实现：

1. **全流程追踪** - 记录项目从启动到交付的所有关键事件
2. **智能分析** - 基于事件流分析项目健康度和风险
3. **决策支持** - 为AI架构师提供数据驱动的决策依据
4. **知识沉淀** - 事件作为项目记忆的时间轴

### 设计原则

| 原则 | 说明 |
|------|------|
| **完备性** | 覆盖任务、功能、问题、协作全生命周期 |
| **可扩展性** | 支持新增事件类型，不影响现有系统 |
| **标准化** | 统一数据结构，便于分析和展示 |
| **轻量级** | 避免过度设计，保持简洁高效 |

### 应用场景

1. **架构师Dashboard** - 实时监控项目动态
2. **项目记忆空间** - 自动记录和回溯
3. **风险预警** - 基于事件模式识别风险
4. **团队协作** - 同步项目状态变化

---

## 事件类型定义

### 总览

共定义 **28种核心事件类型**，分为4大类：

| 类别 | 事件数 | 说明 |
|------|--------|------|
| 任务生命周期 | 9种 | 任务从创建到完成的全流程 |
| 功能生命周期 | 5种 | 功能从设计到上线的过程 |
| 问题生命周期 | 6种 | 问题从发现到解决的闭环 |
| 协作事件 | 8种 | 团队协作和外部交互 |

---

### 1️⃣ 任务生命周期事件 (9种)

#### 1.1 TASK_CREATED - 任务创建

**触发时机**: 新任务被添加到任务看板

**关键数据**:
- 任务ID、标题、优先级
- 创建者（架构师/PM AI/全栈工程师）
- 预估工时、依赖关系

**示例**:
```json
{
  "event_type": "TASK_CREATED",
  "task_id": "TASK-C.1",
  "title": "创建FastAPI主应用入口",
  "priority": "P0",
  "estimated_hours": 2.0,
  "created_by": "architect",
  "dependencies": []
}
```

**优先级**: Medium

---

#### 1.2 TASK_ASSIGNED - 任务分配

**触发时机**: 任务被分配给执行者

**关键数据**:
- 任务ID、被分配者
- 分配原因（能力匹配/负载均衡）

**示例**:
```json
{
  "event_type": "TASK_ASSIGNED",
  "task_id": "TASK-C.1",
  "assigned_to": "fullstack-engineer",
  "reason": "capability_match",
  "assigned_by": "architect"
}
```

**优先级**: Medium

---

#### 1.3 TASK_STARTED - 任务开始

**触发时机**: 执行者开始实现任务（状态: PENDING → IN_PROGRESS）

**关键数据**:
- 任务ID、实际开始时间
- 工程师确认的工作计划

**示例**:
```json
{
  "event_type": "TASK_STARTED",
  "task_id": "TASK-C.1",
  "started_by": "fullstack-engineer",
  "planned_completion": "2025-11-18T12:00:00",
  "work_plan": "1. 创建main.py 2. 配置CORS 3. 注册路由"
}
```

**优先级**: Medium

---

#### 1.4 TASK_BLOCKED - 任务阻塞

**触发时机**: 任务因外部依赖或技术问题无法继续（状态: IN_PROGRESS → BLOCKED）

**关键数据**:
- 任务ID、阻塞原因
- 需要的支持、预计恢复时间

**示例**:
```json
{
  "event_type": "TASK_BLOCKED",
  "task_id": "TASK-C.2",
  "blocked_reason": "dependency_not_ready",
  "blocking_task": "TASK-C.1",
  "estimated_unblock": "2025-11-18T14:00:00"
}
```

**优先级**: High（P0任务）/ Medium（其他）

---

#### 1.5 TASK_UNBLOCKED - 任务解除阻塞

**触发时机**: 阻塞条件解除（状态: BLOCKED → IN_PROGRESS）

**关键数据**:
- 任务ID、解除原因

**示例**:
```json
{
  "event_type": "TASK_UNBLOCKED",
  "task_id": "TASK-C.2",
  "unblock_reason": "dependency_completed",
  "unblocked_by": "system"
}
```

**优先级**: Medium

---

#### 1.6 TASK_SUBMITTED - 任务提交审查

**触发时机**: 执行者完成实现，提交给架构师审查（状态: IN_PROGRESS → REVIEW）

**关键数据**:
- 任务ID、实际完成时间
- 完成报告摘要、修改文件清单

**示例**:
```json
{
  "event_type": "TASK_SUBMITTED",
  "task_id": "TASK-C.1",
  "submitted_by": "fullstack-engineer",
  "actual_hours": 2.5,
  "files_modified": ["apps/api/src/main.py"],
  "completion_summary": "已实现FastAPI主应用，通过健康检查"
}
```

**优先级**: Medium

---

#### 1.7 TASK_REVIEWED - 任务审查完成

**触发时机**: 架构师完成代码审查

**关键数据**:
- 任务ID、审查结果（通过/需修改）
- 审查评分、反馈意见

**示例**:
```json
{
  "event_type": "TASK_REVIEWED",
  "task_id": "TASK-C.1",
  "reviewed_by": "architect",
  "result": "approved",
  "score": 95,
  "feedback": "代码质量优秀，日志输出清晰"
}
```

**优先级**: Medium

---

#### 1.8 TASK_COMPLETED - 任务完成

**触发时机**: 任务通过审查，正式完成（状态: REVIEW → COMPLETED）

**关键数据**:
- 任务ID、完成时间
- 最终工时、质量评分

**示例**:
```json
{
  "event_type": "TASK_COMPLETED",
  "task_id": "TASK-C.1",
  "completed_at": "2025-11-18T11:30:00",
  "total_hours": 2.5,
  "quality_score": 95
}
```

**优先级**: Medium

---

#### 1.9 TASK_CANCELLED - 任务取消

**触发时机**: 任务因需求变更或优先级调整被取消

**关键数据**:
- 任务ID、取消原因
- 取消决策者

**示例**:
```json
{
  "event_type": "TASK_CANCELLED",
  "task_id": "TASK-D.3",
  "cancelled_by": "architect",
  "reason": "requirement_changed",
  "explanation": "决定延后迁移，聚焦核心功能"
}
```

**优先级**: Low

---

### 2️⃣ 功能生命周期事件 (5种)

#### 2.1 FEATURE_PROPOSED - 功能提案

**触发时机**: 新功能需求被提出

**关键数据**:
- 功能ID、标题、描述
- 提案者、业务价值

**示例**:
```json
{
  "event_type": "FEATURE_PROPOSED",
  "feature_id": "FEAT-001",
  "title": "项目事件流系统",
  "proposed_by": "product_manager",
  "business_value": "实时监控项目进展，提升决策效率",
  "estimated_effort": "8 hours"
}
```

**优先级**: Low

---

#### 2.2 FEATURE_APPROVED - 功能批准

**触发时机**: 功能提案通过评审，进入开发计划

**关键数据**:
- 功能ID、批准者
- 目标版本、预计完成时间

**示例**:
```json
{
  "event_type": "FEATURE_APPROVED",
  "feature_id": "FEAT-001",
  "approved_by": "architect",
  "target_version": "v1.8",
  "planned_completion": "2025-11-25"
}
```

**优先级**: Medium

---

#### 2.3 FEATURE_IN_PROGRESS - 功能开发中

**触发时机**: 功能的首个任务开始执行

**关键数据**:
- 功能ID、关联任务列表
- 当前进度

**示例**:
```json
{
  "event_type": "FEATURE_IN_PROGRESS",
  "feature_id": "FEAT-001",
  "tasks": ["TASK-E.1", "TASK-E.2"],
  "progress": "20%"
}
```

**优先级**: Medium

---

#### 2.4 FEATURE_COMPLETED - 功能完成

**触发时机**: 功能的所有任务完成，功能测试通过

**关键数据**:
- 功能ID、完成时间
- 质量指标（测试覆盖率、性能指标）

**示例**:
```json
{
  "event_type": "FEATURE_COMPLETED",
  "feature_id": "FEAT-001",
  "completed_at": "2025-11-25T18:00:00",
  "test_coverage": "85%",
  "performance_ok": true
}
```

**优先级**: High

---

#### 2.5 FEATURE_DEPLOYED - 功能部署

**触发时机**: 功能部署到生产环境

**关键数据**:
- 功能ID、部署环境
- 部署版本、健康检查结果

**示例**:
```json
{
  "event_type": "FEATURE_DEPLOYED",
  "feature_id": "FEAT-001",
  "environment": "production",
  "version": "v1.8.0",
  "health_check": "passed"
}
```

**优先级**: Critical

---

### 3️⃣ 问题生命周期事件 (6种)

#### 3.1 ISSUE_DISCOVERED - 问题发现

**触发时机**: 新问题被识别和记录

**关键数据**:
- 问题ID、严重程度（critical/high/medium/low）
- 发现者、影响范围

**示例**:
```json
{
  "event_type": "ISSUE_DISCOVERED",
  "issue_id": "ISS-001",
  "severity": "high",
  "title": "Dashboard Tab切换失败",
  "discovered_by": "tester",
  "impact": "所有Tab模块不可用"
}
```

**优先级**: Critical（严重程度high+）/ High（medium）/ Low（low）

---

#### 3.2 ISSUE_ASSIGNED - 问题分配

**触发时机**: 问题被分配给工程师解决

**关键数据**:
- 问题ID、被分配者

**示例**:
```json
{
  "event_type": "ISSUE_ASSIGNED",
  "issue_id": "ISS-001",
  "assigned_to": "fullstack-engineer"
}
```

**优先级**: 继承问题优先级

---

#### 3.3 ISSUE_IN_PROGRESS - 问题处理中

**触发时机**: 工程师开始排查和修复问题

**关键数据**:
- 问题ID、初步诊断

**示例**:
```json
{
  "event_type": "ISSUE_IN_PROGRESS",
  "issue_id": "ISS-001",
  "diagnosis": "JavaScript模板字符串内反引号未转义"
}
```

**优先级**: 继承问题优先级

---

#### 3.4 ISSUE_SOLVED - 问题解决

**触发时机**: 问题根因修复，等待验证

**关键数据**:
- 问题ID、解决方案描述
- 修改文件、修复工时

**示例**:
```json
{
  "event_type": "ISSUE_SOLVED",
  "issue_id": "ISS-001",
  "solution": "在templates.py第4361行添加反斜杠转义",
  "files_modified": ["apps/dashboard/templates.py"],
  "time_spent": 1.5
}
```

**优先级**: 继承问题优先级

---

#### 3.5 ISSUE_VERIFIED - 问题验证

**触发时机**: 修复通过测试验证

**关键数据**:
- 问题ID、验证结果

**示例**:
```json
{
  "event_type": "ISSUE_VERIFIED",
  "issue_id": "ISS-001",
  "verified_by": "architect",
  "verification_method": "手动测试所有Tab切换"
}
```

**优先级**: Medium

---

#### 3.6 ISSUE_CLOSED - 问题关闭

**触发时机**: 问题完全解决并归档

**关键数据**:
- 问题ID、关闭时间
- 总耗时、经验教训

**示例**:
```json
{
  "event_type": "ISSUE_CLOSED",
  "issue_id": "ISS-001",
  "closed_at": "2025-11-18T15:00:00",
  "total_time": 2.0,
  "lessons_learned": "Python f-string中嵌套JavaScript模板字符串需转义"
}
```

**优先级**: Low

---

### 4️⃣ 协作事件 (8种)

#### 4.1 ARCHITECT_HANDOVER - 架构师交接

**触发时机**: 架构师Token用尽，生成交接快照

**关键数据**:
- 项目ID、交接快照ID
- 当前进度、未完成任务、重要提醒

**示例**:
```json
{
  "event_type": "ARCHITECT_HANDOVER",
  "project_id": "TASKFLOW",
  "snapshot_id": "handover_20251118_220000",
  "progress": "60%",
  "pending_tasks": ["TASK-C.1", "TASK-C.2"],
  "critical_notes": "Phase C需优先完成"
}
```

**优先级**: High

---

#### 4.2 ARCHITECT_RESUME - 新架构师接管

**触发时机**: 新架构师从快照恢复工作上下文

**关键数据**:
- 项目ID、快照ID
- 新架构师ID

**示例**:
```json
{
  "event_type": "ARCHITECT_RESUME",
  "project_id": "TASKFLOW",
  "snapshot_id": "handover_20251118_220000",
  "resumed_by": "architect_v2"
}
```

**优先级**: Medium

---

#### 4.3 CODE_REVIEW_REQUESTED - 代码审查请求

**触发时机**: 工程师请求架构师审查代码

**关键数据**:
- 任务ID、请求者
- 代码diff摘要

**示例**:
```json
{
  "event_type": "CODE_REVIEW_REQUESTED",
  "task_id": "TASK-C.1",
  "requested_by": "fullstack-engineer",
  "files_changed": 3,
  "lines_added": 150,
  "lines_removed": 20
}
```

**优先级**: Medium

---

#### 4.4 DECISION_RECORDED - 技术决策记录

**触发时机**: 重要技术决策被记录为ADR

**关键数据**:
- 决策ID、标题
- 决策内容、影响范围

**示例**:
```json
{
  "event_type": "DECISION_RECORDED",
  "decision_id": "ADR-0001",
  "title": "采用Monorepo架构",
  "decision": "使用单仓库管理所有包",
  "impact": "project_structure"
}
```

**优先级**: High

---

#### 4.5 KNOWLEDGE_CAPTURED - 知识捕获

**触发时机**: 问题解决方案或经验被记录到知识库

**关键数据**:
- 知识ID、类别（architecture/pattern/guide）
- 关联问题/任务

**示例**:
```json
{
  "event_type": "KNOWLEDGE_CAPTURED",
  "knowledge_id": "KB-001",
  "category": "guide",
  "title": "Python f-string嵌套JavaScript模板字符串转义规则",
  "related_issue": "ISS-001"
}
```

**优先级**: Low

---

#### 4.6 DEPENDENCY_ADDED - 依赖添加

**触发时机**: 任务之间建立新的依赖关系

**关键数据**:
- 任务ID、被依赖任务ID

**示例**:
```json
{
  "event_type": "DEPENDENCY_ADDED",
  "task_id": "TASK-C.2",
  "depends_on": "TASK-C.1",
  "reason": "需要FastAPI服务运行"
}
```

**优先级**: Medium

---

#### 4.7 MILESTONE_REACHED - 里程碑达成

**触发时机**: 项目阶段性目标完成

**关键数据**:
- 里程碑ID、完成时间
- 完成任务数、质量指标

**示例**:
```json
{
  "event_type": "MILESTONE_REACHED",
  "milestone_id": "Phase C",
  "milestone_name": "API集成完成",
  "completed_at": "2025-11-19T18:00:00",
  "tasks_completed": 3,
  "overall_quality": "excellent"
}
```

**优先级**: Critical

---

#### 4.8 RISK_IDENTIFIED - 风险识别

**触发时机**: 系统或人工识别到项目风险

**关键数据**:
- 风险ID、风险类型（delay/quality/technical）
- 影响程度、缓解措施

**示例**:
```json
{
  "event_type": "RISK_IDENTIFIED",
  "risk_id": "RISK-001",
  "risk_type": "delay",
  "description": "3个P0任务连续阻塞",
  "impact": "high",
  "mitigation": "调整任务优先级，增加资源"
}
```

**优先级**: Critical

---

## 事件数据结构

### 统一事件基类

所有事件都继承以下基础结构：

```python
@dataclass
class BaseEvent:
    """事件基类"""
    # ===== 必填字段 =====
    event_id: str                    # 事件唯一ID (UUID)
    event_type: str                  # 事件类型 (28种之一)
    project_id: str                  # 项目ID
    timestamp: datetime              # 事件发生时间
    
    # ===== 上下文字段 =====
    actor: str                       # 触发者 (architect/engineer/system)
    actor_type: str                  # 触发者类型 (human/ai/system)
    
    # ===== 优先级字段 =====
    priority: str                    # 事件优先级 (critical/high/medium/low)
    
    # ===== 关联字段 =====
    related_entities: Dict[str, str] # 关联实体 {"task_id": "TASK-C.1", ...}
    
    # ===== 元数据字段 =====
    metadata: Dict[str, Any]         # 扩展元数据 (具体事件的特有字段)
    tags: List[str]                  # 标签 (用于分类和检索)
    
    # ===== 追溯字段 =====
    parent_event_id: Optional[str]   # 父事件ID (用于事件链)
    correlation_id: Optional[str]    # 关联ID (同一流程的事件)
```

### 事件JSON示例

```json
{
  "event_id": "evt_20251118_120001",
  "event_type": "TASK_STARTED",
  "project_id": "TASKFLOW",
  "timestamp": "2025-11-18T12:00:01Z",
  
  "actor": "fullstack-engineer",
  "actor_type": "ai",
  
  "priority": "medium",
  
  "related_entities": {
    "task_id": "TASK-C.1",
    "component_id": "api"
  },
  
  "metadata": {
    "planned_completion": "2025-11-18T14:00:00Z",
    "work_plan": "1. 创建main.py 2. 配置CORS 3. 注册路由"
  },
  
  "tags": ["backend", "api", "phase-c"],
  
  "parent_event_id": "evt_20251118_100001",
  "correlation_id": "flow_task_c1"
}
```

---

## 事件优先级体系

### 优先级定义

| 优先级 | 说明 | 响应时间 | 通知方式 |
|--------|------|---------|---------|
| **Critical** | 项目级关键事件 | 立即 | 实时推送 + 邮件 |
| **High** | 重要事件，需快速响应 | 30分钟内 | 实时推送 |
| **Medium** | 正常事件 | 2小时内 | Dashboard显示 |
| **Low** | 一般信息 | 无要求 | 日志记录 |

### 优先级矩阵

| 事件类型 | 默认优先级 | 动态调整规则 |
|---------|-----------|-------------|
| TASK_BLOCKED | High | 若为P0任务 → Critical |
| ISSUE_DISCOVERED | 继承严重程度 | Critical问题 → Critical事件 |
| MILESTONE_REACHED | Critical | - |
| RISK_IDENTIFIED | Critical | - |
| FEATURE_DEPLOYED | Critical | - |
| ARCHITECT_HANDOVER | High | - |
| TASK_CREATED | Medium | - |
| TASK_COMPLETED | Medium | 若为关键路径任务 → High |
| KNOWLEDGE_CAPTURED | Low | - |

### 优先级计算算法

```python
def calculate_event_priority(
    event_type: str,
    related_task: Optional[Task] = None,
    related_issue: Optional[Issue] = None
) -> str:
    """动态计算事件优先级"""
    
    # 1. 固定Critical事件
    if event_type in ["MILESTONE_REACHED", "RISK_IDENTIFIED", "FEATURE_DEPLOYED"]:
        return "critical"
    
    # 2. 任务相关事件
    if related_task:
        if event_type == "TASK_BLOCKED" and related_task.priority == "P0":
            return "critical"
        if event_type == "TASK_COMPLETED" and related_task.is_critical_path:
            return "high"
    
    # 3. 问题相关事件
    if related_issue:
        severity_map = {
            "critical": "critical",
            "high": "high",
            "medium": "medium",
            "low": "low"
        }
        return severity_map.get(related_issue.severity, "medium")
    
    # 4. 使用默认优先级
    default_priorities = {
        "ARCHITECT_HANDOVER": "high",
        "DECISION_RECORDED": "high",
        "FEATURE_APPROVED": "medium",
        "TASK_CREATED": "medium",
        # ... 更多映射
    }
    return default_priorities.get(event_type, "medium")
```

---

## 事件聚合规则

### 聚合场景

#### 场景1: 同任务连续事件聚合

**规则**: 同一任务在10分钟内的连续状态变更，聚合为单个事件流

**示例**:
```
原始事件:
- 12:00 TASK_CREATED (TASK-C.1)
- 12:01 TASK_ASSIGNED (TASK-C.1)
- 12:05 TASK_STARTED (TASK-C.1)

聚合后:
- 12:05 TASK_FLOW (TASK-C.1: created → assigned → started)
```

**适用**: Dashboard实时监控，避免信息过载

---

#### 场景2: 批量完成聚合

**规则**: 1小时内完成≥3个任务，聚合为"批量完成"事件

**示例**:
```
原始事件:
- 14:00 TASK_COMPLETED (TASK-C.1)
- 14:30 TASK_COMPLETED (TASK-C.2)
- 14:50 TASK_COMPLETED (TASK-C.3)

聚合后:
- 14:50 BATCH_TASKS_COMPLETED (3 tasks in Phase C)
```

**适用**: 项目进度报告

---

#### 场景3: 问题聚合

**规则**: 相同组件在24小时内发现≥3个问题，聚合为"质量风险"

**示例**:
```
原始事件:
- 09:00 ISSUE_DISCOVERED (Dashboard模块)
- 15:00 ISSUE_DISCOVERED (Dashboard模块)
- 21:00 ISSUE_DISCOVERED (Dashboard模块)

聚合后:
- 21:00 QUALITY_RISK_DETECTED (Dashboard模块: 24h内3个问题)
```

**适用**: 风险预警

---

#### 场景4: 功能里程碑聚合

**规则**: 功能的所有子事件聚合为进度视图

**示例**:
```
原始事件:
- Day 1: FEATURE_APPROVED (FEAT-001)
- Day 2: FEATURE_IN_PROGRESS (FEAT-001, 20%)
- Day 3: FEATURE_IN_PROGRESS (FEAT-001, 60%)
- Day 4: FEATURE_COMPLETED (FEAT-001)

聚合后:
- Day 4: FEATURE_LIFECYCLE (FEAT-001: 4天完成，进度符合预期)
```

**适用**: 功能交付分析

---

### 聚合算法

```python
class EventAggregator:
    """事件聚合器"""
    
    def aggregate_task_flow(
        self,
        events: List[BaseEvent],
        time_window_minutes: int = 10
    ) -> Optional[BaseEvent]:
        """聚合任务流事件"""
        
        # 1. 按task_id分组
        task_events = {}
        for event in events:
            task_id = event.related_entities.get("task_id")
            if task_id:
                task_events.setdefault(task_id, []).append(event)
        
        # 2. 对每个任务检查时间窗口
        aggregated = []
        for task_id, task_event_list in task_events.items():
            # 排序
            sorted_events = sorted(task_event_list, key=lambda e: e.timestamp)
            
            # 检查时间差
            if len(sorted_events) >= 2:
                time_diff = (sorted_events[-1].timestamp - sorted_events[0].timestamp).total_seconds()
                if time_diff <= time_window_minutes * 60:
                    # 满足聚合条件
                    aggregated.append(self._create_flow_event(sorted_events))
        
        return aggregated
    
    def _create_flow_event(self, events: List[BaseEvent]) -> BaseEvent:
        """创建聚合事件"""
        return BaseEvent(
            event_id=f"flow_{events[-1].event_id}",
            event_type="TASK_FLOW",
            project_id=events[0].project_id,
            timestamp=events[-1].timestamp,
            actor=events[-1].actor,
            actor_type=events[-1].actor_type,
            priority="medium",
            related_entities=events[-1].related_entities,
            metadata={
                "flow": [e.event_type for e in events],
                "duration_seconds": (events[-1].timestamp - events[0].timestamp).total_seconds(),
                "original_event_count": len(events)
            },
            tags=["aggregated", "task_flow"]
        )
```

---

## 事件过滤规则

### 过滤维度

#### 1. 按优先级过滤

```python
# Dashboard实时监控：只显示High+
filter_events(min_priority="high")

# 日志审计：显示全部
filter_events(min_priority="low")
```

---

#### 2. 按时间过滤

```python
# 最近24小时
filter_events(time_range="24h")

# 指定日期范围
filter_events(start_date="2025-11-18", end_date="2025-11-19")
```

---

#### 3. 按事件类型过滤

```python
# 只看任务事件
filter_events(event_types=["TASK_*"])

# 只看问题和风险
filter_events(event_types=["ISSUE_*", "RISK_*"])
```

---

#### 4. 按项目/组件过滤

```python
# 特定项目
filter_events(project_id="TASKFLOW")

# 特定组件
filter_events(component_id="api")
```

---

#### 5. 按触发者过滤

```python
# 架构师的操作
filter_events(actor="architect")

# AI触发的事件
filter_events(actor_type="ai")
```

---

#### 6. 按标签过滤

```python
# 后端相关
filter_events(tags=["backend"])

# Phase C相关
filter_events(tags=["phase-c"])
```

---

### 过滤器实现

```python
class EventFilter:
    """事件过滤器"""
    
    def __init__(self, events: List[BaseEvent]):
        self.events = events
    
    def filter(
        self,
        min_priority: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        time_range: Optional[str] = None,
        project_id: Optional[str] = None,
        component_id: Optional[str] = None,
        actor: Optional[str] = None,
        actor_type: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[BaseEvent]:
        """多条件过滤"""
        
        result = self.events
        
        # 优先级过滤
        if min_priority:
            priority_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
            min_level = priority_order[min_priority]
            result = [e for e in result if priority_order[e.priority] >= min_level]
        
        # 事件类型过滤（支持通配符）
        if event_types:
            import fnmatch
            result = [
                e for e in result
                if any(fnmatch.fnmatch(e.event_type, pattern) for pattern in event_types)
            ]
        
        # 时间范围过滤
        if time_range:
            cutoff = self._parse_time_range(time_range)
            result = [e for e in result if e.timestamp >= cutoff]
        
        # 项目过滤
        if project_id:
            result = [e for e in result if e.project_id == project_id]
        
        # 组件过滤
        if component_id:
            result = [
                e for e in result
                if e.related_entities.get("component_id") == component_id
            ]
        
        # 触发者过滤
        if actor:
            result = [e for e in result if e.actor == actor]
        if actor_type:
            result = [e for e in result if e.actor_type == actor_type]
        
        # 标签过滤（ANY匹配）
        if tags:
            result = [
                e for e in result
                if any(tag in e.tags for tag in tags)
            ]
        
        return result
    
    def _parse_time_range(self, time_range: str) -> datetime:
        """解析时间范围"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        
        if time_range.endswith("h"):
            hours = int(time_range[:-1])
            return now - timedelta(hours=hours)
        elif time_range.endswith("d"):
            days = int(time_range[:-1])
            return now - timedelta(days=days)
        else:
            raise ValueError(f"Invalid time_range: {time_range}")
```

---

### 预设过滤模板

| 模板名称 | 说明 | 过滤条件 |
|---------|------|---------|
| **critical_alerts** | 紧急告警 | priority=critical |
| **architect_actions** | 架构师操作 | actor=architect |
| **task_lifecycle** | 任务全流程 | event_types=TASK_* |
| **quality_events** | 质量相关 | event_types=ISSUE_*, RISK_* |
| **today** | 今日事件 | time_range=24h |
| **phase_c** | Phase C事件 | tags=phase-c |

**使用示例**:
```python
# 获取今日紧急告警
events = event_filter.apply_template("critical_alerts").apply_template("today")
```

---

## 实现建议

### Phase 1: 核心基础设施 (2小时)

**任务**:
1. 创建事件数据模型 (`packages/core-domain/entities/event.py`)
2. 创建事件枚举 (`packages/core-domain/enums/event_types.py`)
3. 创建数据库表 (`database/migrations/004_add_events.sql`)

**产出**:
- `events`表（8个字段）
- `BaseEvent`类定义
- 28种事件类型枚举

---

### Phase 2: 事件服务层 (3小时)

**任务**:
1. 实现EventService (`packages/core-domain/services/event_service.py`)
   - 记录事件 `record_event()`
   - 查询事件 `get_events()`
   - 优先级计算 `calculate_priority()`
2. 实现EventAggregator (`packages/core-domain/services/event_aggregator.py`)
3. 实现EventFilter (`packages/core-domain/services/event_filter.py`)

**产出**:
- 3个服务类（共~600行）

---

### Phase 3: API端点 (2小时)

**任务**:
1. 创建事件API路由 (`apps/api/src/routes/events.py`)
   - POST /api/events - 记录事件
   - GET /api/events - 查询事件（支持过滤）
   - GET /api/events/aggregate - 聚合事件
   - GET /api/events/stats - 事件统计

**产出**:
- 4个API端点

---

### Phase 4: Dashboard集成 (3小时)

**任务**:
1. 在Dashboard添加"事件流"Tab
2. 实现实时事件推送（WebSocket或轮询）
3. 实现过滤UI（优先级、类型、时间范围）

**产出**:
- Dashboard新模块（~300行前端代码）

---

### Phase 5: 测试和文档 (2小时)

**任务**:
1. 编写单元测试（事件记录、过滤、聚合）
2. 编写集成测试（端到端流程）
3. 编写使用文档

**产出**:
- 测试用例（~200行）
- 使用指南文档

---

### 总计工时：12小时

---

## 附录

### A. 事件类型速查表

| 序号 | 事件类型 | 分类 | 默认优先级 |
|-----|---------|------|-----------|
| 1 | TASK_CREATED | 任务 | Medium |
| 2 | TASK_ASSIGNED | 任务 | Medium |
| 3 | TASK_STARTED | 任务 | Medium |
| 4 | TASK_BLOCKED | 任务 | High |
| 5 | TASK_UNBLOCKED | 任务 | Medium |
| 6 | TASK_SUBMITTED | 任务 | Medium |
| 7 | TASK_REVIEWED | 任务 | Medium |
| 8 | TASK_COMPLETED | 任务 | Medium |
| 9 | TASK_CANCELLED | 任务 | Low |
| 10 | FEATURE_PROPOSED | 功能 | Low |
| 11 | FEATURE_APPROVED | 功能 | Medium |
| 12 | FEATURE_IN_PROGRESS | 功能 | Medium |
| 13 | FEATURE_COMPLETED | 功能 | High |
| 14 | FEATURE_DEPLOYED | 功能 | Critical |
| 15 | ISSUE_DISCOVERED | 问题 | 继承严重程度 |
| 16 | ISSUE_ASSIGNED | 问题 | 继承 |
| 17 | ISSUE_IN_PROGRESS | 问题 | 继承 |
| 18 | ISSUE_SOLVED | 问题 | 继承 |
| 19 | ISSUE_VERIFIED | 问题 | Medium |
| 20 | ISSUE_CLOSED | 问题 | Low |
| 21 | ARCHITECT_HANDOVER | 协作 | High |
| 22 | ARCHITECT_RESUME | 协作 | Medium |
| 23 | CODE_REVIEW_REQUESTED | 协作 | Medium |
| 24 | DECISION_RECORDED | 协作 | High |
| 25 | KNOWLEDGE_CAPTURED | 协作 | Low |
| 26 | DEPENDENCY_ADDED | 协作 | Medium |
| 27 | MILESTONE_REACHED | 协作 | Critical |
| 28 | RISK_IDENTIFIED | 协作 | Critical |

---

### B. 事件枚举Python实现

```python
# packages/core-domain/enums/event_types.py

from enum import Enum

class EventType(str, Enum):
    """事件类型枚举"""
    
    # 任务生命周期 (9种)
    TASK_CREATED = "TASK_CREATED"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    TASK_STARTED = "TASK_STARTED"
    TASK_BLOCKED = "TASK_BLOCKED"
    TASK_UNBLOCKED = "TASK_UNBLOCKED"
    TASK_SUBMITTED = "TASK_SUBMITTED"
    TASK_REVIEWED = "TASK_REVIEWED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_CANCELLED = "TASK_CANCELLED"
    
    # 功能生命周期 (5种)
    FEATURE_PROPOSED = "FEATURE_PROPOSED"
    FEATURE_APPROVED = "FEATURE_APPROVED"
    FEATURE_IN_PROGRESS = "FEATURE_IN_PROGRESS"
    FEATURE_COMPLETED = "FEATURE_COMPLETED"
    FEATURE_DEPLOYED = "FEATURE_DEPLOYED"
    
    # 问题生命周期 (6种)
    ISSUE_DISCOVERED = "ISSUE_DISCOVERED"
    ISSUE_ASSIGNED = "ISSUE_ASSIGNED"
    ISSUE_IN_PROGRESS = "ISSUE_IN_PROGRESS"
    ISSUE_SOLVED = "ISSUE_SOLVED"
    ISSUE_VERIFIED = "ISSUE_VERIFIED"
    ISSUE_CLOSED = "ISSUE_CLOSED"
    
    # 协作事件 (8种)
    ARCHITECT_HANDOVER = "ARCHITECT_HANDOVER"
    ARCHITECT_RESUME = "ARCHITECT_RESUME"
    CODE_REVIEW_REQUESTED = "CODE_REVIEW_REQUESTED"
    DECISION_RECORDED = "DECISION_RECORDED"
    KNOWLEDGE_CAPTURED = "KNOWLEDGE_CAPTURED"
    DEPENDENCY_ADDED = "DEPENDENCY_ADDED"
    MILESTONE_REACHED = "MILESTONE_REACHED"
    RISK_IDENTIFIED = "RISK_IDENTIFIED"


class EventPriority(str, Enum):
    """事件优先级枚举"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EventCategory(str, Enum):
    """事件类别枚举"""
    TASK = "task"
    FEATURE = "feature"
    ISSUE = "issue"
    COLLABORATION = "collaboration"
```

---

### C. 数据库Schema

```sql
-- database/migrations/004_add_events.sql

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,                          -- 事件ID (UUID)
    event_type TEXT NOT NULL,                     -- 事件类型 (28种)
    project_id TEXT NOT NULL,                     -- 项目ID
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    
    actor TEXT,                                   -- 触发者
    actor_type TEXT,                              -- 触发者类型
    
    priority TEXT NOT NULL DEFAULT 'medium',      -- 优先级
    
    related_entities TEXT,                        -- 关联实体 (JSON)
    metadata TEXT,                                -- 扩展元数据 (JSON)
    tags TEXT,                                    -- 标签 (JSON数组)
    
    parent_event_id TEXT,                         -- 父事件ID
    correlation_id TEXT,                          -- 关联ID
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 索引优化
CREATE INDEX IF NOT EXISTS idx_events_project ON events(project_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_priority ON events(priority);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_actor ON events(actor);
CREATE INDEX IF NOT EXISTS idx_events_correlation ON events(correlation_id);
```

---

## 总结

### 设计亮点

1. ✅ **完备性** - 28种事件类型覆盖项目全生命周期
2. ✅ **可扩展性** - 统一基类，易于新增事件类型
3. ✅ **智能化** - 动态优先级计算、智能聚合
4. ✅ **易用性** - 预设过滤模板，开箱即用

### 与现有系统集成

| 现有模块 | 集成点 |
|---------|-------|
| 任务管理 | 任务状态变更自动触发事件 |
| 项目记忆 | 事件作为记忆的时间轴 |
| Dashboard | 事件流实时展示 |
| 架构师AI | 基于事件流做决策 |

### 下一步

1. ✅ 本文档已完成 → 提交审查
2. ⏳ 实现Phase 1-2 → 核心功能
3. ⏳ 实现Phase 3-4 → API和Dashboard
4. ⏳ 编写测试和文档

---

**文档维护者**: AI架构师  
**最后更新**: 2025-11-18  
**版本**: v1.0

📋 **项目事件类型体系设计完成！**

