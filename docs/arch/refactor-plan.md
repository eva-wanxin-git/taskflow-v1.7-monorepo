# 任务所·Flow v1.7 - 重构计划

**创建时间**: 2025-11-19 06:00  
**架构师**: AI Architect (Expert Level)  
**项目**: 任务所·Flow v1.7  
**当前进度**: 46.3% (25/54任务)

---

## 📊 执行摘要

### 重构目标

将任务所·Flow从**功能散落**的状态重构为**企业级Monorepo架构**,同时保持v1.6的稳定性。

### 核心原则

1. **渐进式重构** - 不搞"大爆炸"式重写
2. **保持可用** - v1.6继续稳定运行
3. **价值优先** - 先实现核心功能(架构师API)
4. **避免过度** - 遵循YAGNI原则

### 时间规划

- **Phase C** (P0): 6.5小时 → 架构师API可用
- **Phase D** (P2): 6.5小时 → 代码完全在Monorepo中(可选)
- **Phase E** (P3): 4小时 → 测试验证+文档

---

## 🎯 Phase C: API集成 (P0 - 立即执行)

### 目标

让架构师API真正可用,实现"即插即用"的核心价值。

### 当前阻塞

1. **缺少FastAPI主入口** 🔴
   - `apps/api/src/main.py`不存在
   - API服务无法启动

2. **ArchitectOrchestrator未集成数据库** 🔴
   - 所有数据库操作都是TODO
   - 提交架构分析后无法写入

### 任务清单

#### TASK-C.1: 创建FastAPI主入口 (2小时)

**位置**: `apps/api/src/main.py`

**功能需求**:
1. FastAPI应用初始化
2. CORS中间件配置
3. 注册architect路由
4. 健康检查端点
5. Uvicorn启动配置

**实现要点**:

```python
# apps/api/src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import architect

app = FastAPI(
    title="任务所·Flow API",
    version="1.7.0",
    description="企业级AI任务协作中枢"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 路由
app.include_router(architect.router)

# 健康检查
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.7.0",
        "timestamp": datetime.now().isoformat()
    }

# 启动
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8870, log_level="info")
```

**验收标准**:
- [ ] `python apps/api/src/main.py` 能启动
- [ ] `http://localhost:8870/health` 返回200
- [ ] `http://localhost:8870/docs` 显示API文档
- [ ] 日志清晰可读

---

#### TASK-C.2: 集成数据库 (3小时)

**位置**: `apps/api/src/services/architect_orchestrator.py`

**问题**: 所有数据库操作都是TODO注释

**方案A: 临时引用v1.6 (推荐,快速)**

在`main.py`中:

```python
import sys
from pathlib import Path

# 临时添加v1.6路径
v16_dashboard = Path(__file__).parent.parent.parent / "dashboard" / "src"
sys.path.insert(0, str(v16_dashboard))

from automation.state_manager import StateManager

# 创建StateManager
state_manager = StateManager(
    db_path=str(Path(__file__).parent.parent.parent.parent / "database" / "data" / "tasks.db")
)

# 注入到orchestrator
from .services.architect_orchestrator import create_architect_orchestrator

orchestrator = create_architect_orchestrator(
    state_manager=state_manager,
    docs_root=str(Path(__file__).parent.parent.parent.parent / "docs")
)

# 在routes/architect.py的get_orchestrator()中使用这个全局实例
```

**方案B: 快速迁移StateManager (更规范)**

1. 复制`apps/dashboard/src/automation/state_manager.py`到`packages/infra/database/`
2. 修复导入路径
3. 在main.py中导入

**推荐**: 先用方案A快速打通,Phase D再考虑方案B

**需要实现的方法**:

```python
# architect_orchestrator.py

def _ensure_project_exists(self, project_code: str) -> None:
    """确保项目存在,不存在则创建"""
    # 当前: TODO注释
    # 需要: 调用state_manager.create_project() 或检查是否存在
    
    # 实现逻辑:
    # 1. 查询projects表是否有project_code
    # 2. 如果没有,INSERT INTO projects
    pass

def _ensure_components_exist(self, project_code: str, components: List[str]) -> None:
    """确保组件存在"""
    # 当前: TODO注释
    # 需要: 批量创建components记录
    
    # 实现逻辑:
    # 1. 遍历components列表
    # 2. 查询是否存在
    # 3. 不存在则INSERT INTO components
    pass

def _create_tasks_from_suggestions(
    self, 
    project_code: str, 
    suggestions: List[ArchitectTaskSuggestion]
) -> int:
    """将建议任务转换为tasks表记录"""
    # 当前: TODO注释
    # 需要: 批量INSERT INTO tasks
    
    # 实现逻辑:
    # for suggestion in suggestions:
    #     task_data = {
    #         "id": suggestion.id,
    #         "title": suggestion.title,
    #         "type": suggestion.type,
    #         "priority": suggestion.priority,
    #         "status": "pending",
    #         "project_id": project_code,
    #         ...
    #     }
    #     state_manager.create_task(task_data)
    #     created += 1
    # return created
    pass

def _create_issues_from_problems(
    self, 
    project_code: str, 
    problems: List[ProblemSummary]
) -> int:
    """创建issues记录"""
    # 当前: TODO注释
    # 需要: INSERT INTO issues
    
    # 实现逻辑:
    # for problem in problems:
    #     issue_data = {
    #         "project_id": project_code,
    #         "title": problem.title,
    #         "severity": problem.severity,
    #         "status": "open",
    #         ...
    #     }
    #     state_manager.create_issue(issue_data)
    #     created += 1
    # return created
    pass

def _create_feature_articles(
    self, 
    project_code: str, 
    features: List[FeatureSummary]
) -> int:
    """创建knowledge_articles记录"""
    # 当前: TODO注释
    # 需要: INSERT INTO knowledge_articles
    
    # 实现逻辑:
    # for feature in features:
    #     article_data = {
    #         "project_id": project_code,
    #         "title": feature.title,
    #         "content": feature.description,
    #         "type": "feature",
    #         ...
    #     }
    #     state_manager.create_article(article_data)
    #     created += 1
    # return created
    pass
```

**验收标准**:
- [ ] 提交架构分析JSON,数据库中出现记录
- [ ] `SELECT * FROM tasks WHERE project_id='TEST_PROJECT'` 有数据
- [ ] `SELECT * FROM issues WHERE project_id='TEST_PROJECT'` 有数据
- [ ] Markdown文档(`task-board.md`)正确生成
- [ ] 错误处理完整(数据验证、数据库错误、文件IO错误)

---

#### TASK-C.3: 端到端测试 (1.5小时)

**位置**: `tests/integration/test_architect_api.py`

**测试场景**:

1. **提交架构分析** → 验证数据库写入
2. **查询项目摘要** → 验证数据返回
3. **提交交接快照** → 验证JSON文件生成
4. **查询最新快照** → 验证返回正确
5. **错误处理** → 验证异常处理

**测试脚本**:

```python
# tests/integration/test_architect_api.py

import pytest
import requests
from pathlib import Path
import sqlite3

BASE_URL = "http://localhost:8870"
DB_PATH = Path(__file__).parent.parent.parent / "database" / "data" / "tasks.db"

def test_health_check():
    """测试: 健康检查"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_submit_analysis():
    """测试: 提交架构分析"""
    analysis = {
        "project_code": "TEST_PROJECT_001",
        "completed_features": [
            {
                "title": "用户认证",
                "description": "完整的JWT认证系统",
                "related_paths": ["auth/"],
                "completion": 1.0
            }
        ],
        "problems": [
            {
                "title": "缺少测试",
                "description": "单元测试覆盖率<10%",
                "severity": "high",
                "impact": "回归风险高"
            }
        ],
        "suggested_tasks": [
            {
                "id": "TEST-001",
                "title": "补充单元测试",
                "type": "test",
                "priority": "high",
                "component": "backend",
                "description": "为核心模块补充测试",
                "estimated_hours": 8.0
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/architect/analysis",
        json=analysis
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    assert result["tasks_created"] >= 1
    assert result["issues_created"] >= 1
    assert "task_board_url" in result
    
    # 验证数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查tasks表
    cursor.execute(
        "SELECT * FROM tasks WHERE id=?",
        ("TEST-001",)
    )
    task = cursor.fetchone()
    assert task is not None
    
    # 检查issues表
    cursor.execute(
        "SELECT * FROM issues WHERE project_id=? AND title=?",
        ("TEST_PROJECT_001", "缺少测试")
    )
    issue = cursor.fetchone()
    assert issue is not None
    
    conn.close()

def test_get_project_summary():
    """测试: 查询项目摘要"""
    response = requests.get(
        f"{BASE_URL}/api/architect/summary/TEST_PROJECT_001"
    )
    
    assert response.status_code == 200
    summary = response.json()
    assert "project" in summary
    assert "stats" in summary
    assert summary["project"]["code"] == "TEST_PROJECT_001"

def test_submit_handover():
    """测试: 提交交接快照"""
    snapshot = {
        "snapshot_id": "handover-test-001",
        "project_code": "TEST_PROJECT_001",
        "completed_phases": [
            {"name": "Phase 1", "completion": 1.0}
        ],
        "current_focus": {
            "phase": "Phase 2",
            "tasks": ["TEST-001"]
        },
        "recommendations_for_next": [
            "继续完成Phase 2"
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/architect/handover",
        json=snapshot
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    assert "snapshot_path" in result
    
    # 验证JSON文件
    snapshot_path = Path(result["snapshot_path"])
    assert snapshot_path.exists()

def test_get_latest_handover():
    """测试: 查询最新交接快照"""
    response = requests.get(
        f"{BASE_URL}/api/architect/handover/latest?project=TEST_PROJECT_001"
    )
    
    assert response.status_code == 200
    snapshot = response.json()
    assert snapshot["snapshot_id"] == "handover-test-001"
    assert snapshot["project_code"] == "TEST_PROJECT_001"

def test_error_handling():
    """测试: 错误处理"""
    # 1. 提交无效数据
    response = requests.post(
        f"{BASE_URL}/api/architect/analysis",
        json={"invalid": "data"}
    )
    assert response.status_code == 422  # Validation Error
    
    # 2. 查询不存在的项目
    response = requests.get(
        f"{BASE_URL}/api/architect/summary/NONEXISTENT"
    )
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**验收标准**:
- [ ] 所有测试通过
- [ ] 测试覆盖率>70%
- [ ] 生成测试报告

---

### Phase C 总结

**预估时间**: 6.5小时

**完成后**:
- ✅ API服务可以启动
- ✅ 架构师可以提交分析结果
- ✅ 数据库正确写入
- ✅ Markdown文档自动生成
- ✅ 端到端测试通过

**核心价值**: 实现"即插即用"的架构师AI

---

## 🎯 Phase D: 代码迁移 (P2 - 可选)

### 目标

将v1.6的代码迁移到Monorepo的规范位置,提升长期可维护性。

### 优先级评估

**为什么是P2(可选)?**

1. **v1.6已经稳定可用** ✅
   - Dashboard运行正常
   - StateManager功能完整
   - 算法模块测试通过

2. **v1.7的核心价值已实现** ✅
   - AI Prompts完整(25000字)
   - 架构师API可用(Phase C后)
   - 知识库数据库就绪(12表)

3. **代码迁移是"锦上添花"** 💡
   - 不影响功能使用
   - 不影响用户体验
   - 主要提升开发者体验

4. **遵循YAGNI原则** 🎯
   - 如果v1.6够用,就不需要迁移
   - 避免"为了Monorepo而Monorepo"
   - 专注于真正的价值

**结论**: Phase D可以延后,甚至跳过。

### 如果确实需要迁移

#### TASK-D.1: 迁移models.py (2小时)

**从**: `apps/dashboard/src/automation/models.py`  
**到**: `packages/core-domain/entities/`

**策略**:
1. 复制models.py到新位置
2. 拆分为多个文件:
   - `task.py` - Task相关模型
   - `project.py` - Project相关模型
   - `component.py` - Component相关模型
   - `knowledge.py` - 知识库相关模型
3. 在旧位置保留兼容导入:
   ```python
   # apps/dashboard/src/automation/models.py
   # 兼容导入,避免破坏v1.6
   from packages.core_domain.entities.task import *
   from packages.core_domain.entities.project import *
   ```
4. 逐步替换导入路径

**验收**:
- [ ] 所有实体模型在新位置
- [ ] 旧位置有兼容导入
- [ ] v1.6 Dashboard仍可运行
- [ ] 所有单元测试通过

---

#### TASK-D.2: 迁移state_manager (3小时)

**从**: `apps/dashboard/src/automation/state_manager.py`  
**到**: `packages/infra/database/state_manager.py`

**策略**:
1. 复制state_manager.py到新位置
2. 修复数据库路径配置:
   ```python
   # 旧: 硬编码路径
   db_path = "database/data/tasks.db"
   
   # 新: 配置化路径
   from pathlib import Path
   db_path = Path(__file__).parent.parent.parent.parent / "database" / "data" / "tasks.db"
   ```
3. 更新所有导入路径
4. 在旧位置保留兼容导入
5. 测试所有CRUD操作

**验收**:
- [ ] StateManager在新位置
- [ ] 数据库路径配置化
- [ ] 旧位置有兼容导入
- [ ] 所有CRUD测试通过
- [ ] v1.6 Dashboard仍可运行

---

#### TASK-D.3: 迁移algorithms (1.5小时)

**从**: `apps/dashboard/src/automation/dependency_analyzer.py`等  
**到**: `packages/algorithms/`

**策略**:
1. 复制算法文件到新位置
2. 拆分为独立模块:
   - `dependency_analyzer.py` - 依赖分析
   - `scheduler.py` - 任务调度
   - `critical_path.py` - 关键路径
3. 在旧位置保留兼容导入
4. 确保算法逻辑不变

**验收**:
- [ ] 算法模块在新位置
- [ ] 旧位置有兼容导入
- [ ] 算法测试全部通过
- [ ] v1.6 Dashboard仍可运行

---

### Phase D 总结

**预估时间**: 6.5小时

**完成后**:
- ✅ 代码完全在Monorepo规范位置
- ✅ v1.6仍可独立运行(兼容导入)
- ✅ 长期可维护性提升

**是否必须**: ❌ 非必须,可延后或跳过

---

## 🎯 Phase E: 测试验证 (P3 - 可延后)

### 目标

补充完整的测试,提升系统稳定性。

### 任务清单

#### TASK-E.1: 完整功能测试 (2小时)

**范围**: 所有主要功能的E2E测试

**测试场景**:
1. 架构师分析 → API提交 → 数据库验证
2. 任务CRUD → 状态流转 → 依赖检查
3. 知识库 → issues/solutions/decisions
4. Dashboard → 数据展示 → 实时刷新

**验收**:
- [ ] E2E测试脚本完整
- [ ] 所有场景通过
- [ ] 测试覆盖率>70%
- [ ] 测试报告生成

---

#### TASK-E.2: 性能测试 (2小时)

**目标**: 识别性能瓶颈并优化

**测试指标**:
- QPS目标: 100+ (架构师API)
- P95延迟: <200ms
- 错误率: <0.1%
- 内存占用: <500MB

**工具**: 
- Apache Bench (ab)
- Locust
- Python cProfile

**验收**:
- [ ] 压测脚本完整
- [ ] 性能报告生成
- [ ] 瓶颈识别
- [ ] 优化建议

---

### Phase E 总结

**预估时间**: 4小时

**完成后**:
- ✅ 测试覆盖率>70%
- ✅ 性能瓶颈识别
- ✅ 系统稳定性提升

---

## 🗺️ 完整实施路线图

### Week 1

**Day 1 上午 (3h)**: Phase C-1 + C-2开始
- TASK-C.1: 创建main.py (2h)
- TASK-C.2: 集成数据库开始 (1h)

**Day 1 下午 (4h)**: Phase C-2完成 + C-3
- TASK-C.2: 集成数据库完成 (2h)
- TASK-C.3: E2E测试 (1.5h)
- ✅ **里程碑**: 架构师API完全可用

**Day 2-3 (可选)**: Phase D
- TASK-D.1: 迁移models (2h)
- TASK-D.2: 迁移state_manager (3h)
- TASK-D.3: 迁移algorithms (1.5h)
- ✅ **里程碑**: 代码完全在Monorepo中

**Day 4 (可选)**: Phase E
- TASK-E.1: 完整功能测试 (2h)
- TASK-E.2: 性能测试 (2h)
- ✅ **里程碑**: v1.7正式发布

---

## 💡 架构师的核心建议

### 建议1: 聚焦核心价值

**v1.7的核心价值是什么?**

不是Monorepo本身,而是:
1. **AI体系** (25000字Prompts) ⭐⭐⭐⭐⭐
2. **架构师API** (即插即用) ⭐⭐⭐⭐⭐
3. **知识库** (12表数据库) ⭐⭐⭐⭐

**结论**: Phase C(API集成)完成后,核心价值已实现,可以交付。

---

### 建议2: 遵循YAGNI原则

**YAGNI**: You Aren't Gonna Need It

**问题**: 
- 我们真的需要把代码迁移到Monorepo吗?
- v1.6的代码位置真的有问题吗?
- 迁移能带来多少实际价值?

**答案**:
- 如果v1.6够用 → 不需要迁移
- 如果用户没抱怨 → 不需要迁移
- 如果没有扩展需求 → 不需要迁移

**结论**: Phase D(代码迁移)可以延后或跳过。

---

### 建议3: 保持灵活性

**并行运行策略**:

```
v1.6 (稳定)              v1.7 (增强)
    ↓                        ↓
Dashboard 8877            API 8870
    ↓                        ↓
automation/               架构师API
state_manager            知识库API
models                   (新功能)
algorithms               
    ↓                        ↓
    都访问同一个数据库
database/data/tasks.db
```

**优点**:
- ✅ v1.6保持稳定(不破坏)
- ✅ v1.7增量增强(新功能)
- ✅ 数据共享(同一数据库)
- ✅ 逐步迁移(如果需要)

---

## 📊 价值评估矩阵

| Phase | 预估时间 | 用户价值 | 开发体验 | 风险 | 优先级 | 建议 |
|-------|---------|---------|---------|------|--------|------|
| Phase C | 6.5h | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 低 | P0 | 立即执行 |
| Phase D | 6.5h | ⭐⭐ | ⭐⭐⭐⭐ | 中 | P2 | 可延后 |
| Phase E | 4h | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 低 | P3 | 可延后 |

**结论**: Phase C是唯一的P0任务。

---

## 🎯 成功标准

### Phase C成功标准

- [ ] API服务可以启动(`python apps/api/src/main.py`)
- [ ] 健康检查通过(`http://localhost:8870/health`)
- [ ] 可以提交架构分析(POST `/api/architect/analysis`)
- [ ] 数据库正确写入(tasks/issues表有记录)
- [ ] Markdown文档自动生成(`docs/tasks/task-board.md`)
- [ ] E2E测试全部通过

### 交付标准

**最小交付**:
- ✅ Phase C完成 → 架构师API可用

**推荐交付**:
- ✅ Phase C + E.1完成 → API可用 + 测试覆盖

**完美交付**:
- ✅ Phase C + D + E全部完成 → 代码规范 + 测试完整

---

## 🔗 相关文档

- [架构清单](architecture-inventory.md)
- [架构审查](architecture-review.md)
- [任务看板](../tasks/task-board.md)
- [ADR-0001](../adr/0001-monorepo-structure.md)

---

**架构师**: AI Architect (Expert Level)  
**版本**: v1.0  
**下次更新**: Phase C完成后

🗺️ **重构计划文档创建完成!**

