# 📤 派发给全栈工程师·李明 - TASK-C系列

**派发时间**: 2025-11-19 00:55  
**派发人**: AI Architect (Expert Level)  
**接收人**: 全栈工程师·李明  
**优先级**: 🔴 P0 Critical

---

## 🚀 开始前必读

李明，在执行任务前，请先加载以下文档：

```markdown
@taskflow-v1.7-monorepo/docs/ai/fullstack-engineer-system-prompt.md
@taskflow-v1.7-monorepo/docs/tasks/task-board.md
@taskflow-v1.7-monorepo/📤派发给李明-TASK-C系列.md
```

**这三个文档会告诉你**：
1. 全栈工程师的工作规范和流程
2. 任务的完整上下文
3. 具体的执行要求

---

## 🚀 第一步：接收任务（必做！）

⚠️ **重要**: 看到此任务后，**立即执行**以下命令之一：

```bash
cd taskflow-v1.7-monorepo

# 开始TASK-C-1
python scripts/李明收到任务.py TASK-C-1

# 或开始TASK-C-2
python scripts/李明收到任务.py TASK-C-2

# 或开始TASK-C-3
python scripts/李明收到任务.py TASK-C-3
```

**这会做什么**:
- ✅ 更新任务状态: pending → in_progress
- ✅ Dashboard实时显示"⚙️ 进行中"
- ✅ 架构师可以看到你的进度

**⚠️ 不运行此脚本，Dashboard状态不会更新！**

---

## 🎯 任务概述

我现在派发**Phase C: API集成**的3个任务给你，这是让v1.7架构师API可用的关键任务。

**总工时**: 6.5小时  
**预期完成**: 今天（Day 2）

---

## 📋 任务清单

### TASK-C-1: 创建FastAPI主应用入口 🔴 P0

**工时**: 2小时  
**复杂度**: LOW  
**依赖**: 无  
**状态**: 🟡 待处理

#### 任务目标
创建`apps/api/src/main.py`，整合所有路由和中间件，启动FastAPI服务。

#### 技术要点
1. **FastAPI应用初始化**
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   
   app = FastAPI(
       title="任务所·Flow API",
       version="1.7.0",
       description="企业级AI任务协作中枢"
   )
   ```

2. **CORS配置**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # 生产环境需限制
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"]
   )
   ```

3. **路由注册**
   ```python
   from .routes import architect
   app.include_router(architect.router)
   ```

4. **健康检查端点**
   ```python
   @app.get("/health")
   async def health_check():
       return {
           "status": "healthy",
           "version": "1.7.0",
           "timestamp": datetime.now().isoformat()
       }
   ```

5. **Uvicorn启动配置**
   ```python
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(
           app,
           host="0.0.0.0",
           port=8870,
           log_level="info"
       )
   ```

#### 验收标准
- [ ] 运行`python apps/api/src/main.py`能启动
- [ ] 访问`http://localhost:8870/health`返回200
- [ ] 访问`http://localhost:8870/docs`显示API文档
- [ ] CORS配置正确（允许Dashboard访问）
- [ ] 日志输出清晰（显示启动信息和端口）
- [ ] 无启动错误

#### 参考资料
- v1.6: `任务所-v1.6-Tab修复版/industrial_dashboard/dashboard.py`
- 路由: `apps/api/src/routes/architect.py`
- 详细说明: `docs/tasks/task-board.md` TASK-C.1部分

---

### TASK-C-2: 集成ArchitectOrchestrator与数据库 🔴 P0

**工时**: 3小时  
**复杂度**: MEDIUM  
**依赖**: ✅ TASK-C-1（需要main.py）  
**状态**: ⏸️ 等待C-1完成

#### 任务目标
将ArchitectOrchestrator与StateManager集成，实现真正的数据库读写。

#### 当前问题
```python
# apps/api/src/services/architect_orchestrator.py

def _ensure_project_exists(self, project_code: str) -> None:
    """确保项目存在，不存在则创建"""
    # TODO: 调用state_manager检查/创建项目  ← 需要实现!
    pass

def _create_tasks_from_suggestions(...) -> int:
    """将建议任务转换为实际任务记录"""
    # TODO: 调用state_manager.create_task(task_data)  ← 需要实现!
    pass
```

#### 实现方案（推荐临时方案）

**步骤1**: 在main.py中添加v1.6路径
```python
import sys
from pathlib import Path

# 临时添加v1.6路径
v16_path = Path(__file__).parent.parent.parent.parent / "任务所-v1.6-Tab修复版"
sys.path.insert(0, str(v16_path))

from automation.state_manager import StateManager
```

**步骤2**: 创建StateManager实例
```python
# 创建state_manager
state_manager = StateManager(db_path="database/data/tasks.db")
```

**步骤3**: 注入到ArchitectOrchestrator
```python
from .services.architect_orchestrator import ArchitectOrchestrator

orchestrator = ArchitectOrchestrator(
    state_manager=state_manager,
    docs_root="docs"
)
```

**步骤4**: 实现TODO的5个方法
1. `_ensure_project_exists()` - 检查/创建项目
2. `_ensure_components_exist()` - 检查/创建组件
3. `_create_tasks_from_suggestions()` - 创建任务记录
4. `_create_issues_from_problems()` - 创建问题记录
5. `_create_feature_articles()` - 创建知识文章

#### 验收标准
- [ ] 提交架构分析JSON，数据库中出现记录
- [ ] `SELECT * FROM tasks` 可以看到新任务
- [ ] `SELECT * FROM issues` 可以看到问题
- [ ] Markdown文档（task-board.md）正确生成
- [ ] 错误处理完整（数据验证失败、数据库错误）

#### 测试方法
```bash
# 1. 准备测试数据
cat > test_analysis.json << EOF
{
  "project_code": "TEST_PROJECT",
  "completed_features": [...],
  "suggested_tasks": [...]
}
EOF

# 2. 调用API
curl -X POST http://localhost:8870/api/architect/analysis \
  -H "Content-Type: application/json" \
  -d @test_analysis.json

# 3. 验证数据库
# （需要sqlite3工具，或用Python脚本查询）

# 4. 检查文档
cat docs/tasks/task-board.md
```

#### 参考资料
- StateManager: `任务所-v1.6-Tab修复版/automation/state_manager.py`
- Orchestrator: `apps/api/src/services/architect_orchestrator.py`
- 详细说明: `docs/tasks/task-board.md` TASK-C.2部分

---

### TASK-C-3: 端到端测试架构师API 🔴 P0

**工时**: 1.5小时  
**复杂度**: LOW  
**依赖**: ✅ TASK-C-1, C-2（需要API可用）  
**状态**: ⏸️ 等待C-1和C-2完成

#### 任务目标
编写完整的E2E测试，验证架构师工作流。

#### 测试场景
1. **提交架构分析JSON** → 验证数据库写入
2. **查询项目摘要** → 验证数据返回
3. **提交交接快照** → 验证JSON文件生成
4. **查询最新快照** → 验证返回正确
5. **错误处理** → 验证异常情况

#### 测试脚本模板
```python
# tests/integration/test_architect_api.py

import pytest
import requests

BASE_URL = "http://localhost:8870"

def test_submit_analysis():
    """测试：提交架构分析"""
    analysis = {
        "project_code": "TEST_PROJECT",
        "completed_features": [
            {"id": "FEAT-001", "name": "功能1", ...}
        ],
        "problems": [...],
        "suggested_tasks": [...]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/architect/analysis",
        json=analysis
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    assert result["tasks_created"] > 0

def test_get_project_summary():
    """测试：查询项目摘要"""
    response = requests.get(
        f"{BASE_URL}/api/architect/summary/TEST_PROJECT"
    )
    
    assert response.status_code == 200
    summary = response.json()
    assert "project" in summary
    assert "stats" in summary

# ... 更多测试 ...
```

#### 验收标准
- [ ] 创建测试脚本`tests/integration/test_architect_api.py`
- [ ] 至少5个测试场景
- [ ] 所有测试通过
- [ ] 测试覆盖率>70%
- [ ] 生成测试报告

#### 测试数据
创建`tests/fixtures/sample_analysis.json`作为测试数据

#### 参考资料
- 路由定义: `apps/api/src/routes/architect.py`
- 详细说明: `docs/tasks/task-board.md` TASK-C.3部分

---

## 🔄 执行顺序

```
上午（9:00-12:00）：
├── TASK-C-1: 创建main.py（2h）
└── TASK-C-2开始: 集成数据库（1h）

下午（14:00-18:00）：
├── TASK-C-2完成: 集成数据库（2h）
└── TASK-C-3: E2E测试（1.5h）
```

---

## 📝 完成报告要求 ⭐ 重要

每个任务完成后，**必须**提交**完成总结报告**（7部分）：

### 完成报告模板

```markdown
# 🎉 任务完成总结报告

## 1. 任务概述
- **任务ID**: TASK-C-X
- **任务标题**: XXX
- **完成时间**: YYYY-MM-DD HH:MM
- **实际工时**: X.Xh

## 2. 实现摘要
[简要描述做了什么，怎么做的]

## 3. 涉及文件清单
**新建文件**:
- `path/to/file1.py` - 说明
- `path/to/file2.py` - 说明

**修改文件**:
- `path/to/file3.py` - 修改内容

## 4. 测试验证
[如何验证功能正常]
- [ ] 测试场景1: 结果
- [ ] 测试场景2: 结果

## 5. 风险注意事项
[有没有潜在问题或需要注意的地方]

## 6. 后续建议
[可选：优化方向或改进建议]

## 7. 任务状态更新
- 状态: 待处理 → **已完成** ✅
- Dashboard: 已更新
```

### 提交方式

1. **完成代码后**，按照上面模板生成完成报告
2. **用户会一键复制完成报告**给我（架构师）
3. **我收到后会审查**，并反馈是否通过

⚠️ **没有完成报告 = 任务未完成！**

---

## ⚠️ 注意事项

### 1. 代码质量要求
- **Clean Code**: 函数≤50行，类型标注完整
- **错误处理**: 完整的try-except，清晰的错误信息
- **日志记录**: 关键步骤都要有日志
- **注释**: 复杂逻辑要有注释

### 2. 测试要求
- **自测**: 提交前自己测试所有场景
- **E2E**: TASK-C-3要覆盖主要流程

### 3. 文档要求
- **代码注释**: docstring完整
- **README**: 如有新功能，更新README

### 4. 如遇问题
- **优先自查**: 先查文档、代码、记忆
- **再提问**: 具体描述问题+复现步骤
- **不能阻塞**: 遇到困难立即反馈

---

## 🎯 期望产出

**Phase C完成后（今天晚上）**：
- ✅ FastAPI服务可以启动
- ✅ 架构师API完全可用
- ✅ 数据库集成正常
- ✅ E2E测试通过
- ✅ 任务所·Flow v1.7核心价值实现！

---

---

## 📋 工作流程总结

```
1. 加载提示词
   ↓
   @fullstack-engineer-system-prompt.md
   @task-board.md
   @📤派发给李明-TASK-C系列.md

2. 确认理解
   ↓
   复述任务，确认验收标准

3. 执行任务
   ↓
   编写代码 + 测试 + 文档

4. 提交完成报告
   ↓
   按模板生成7部分报告
   用户一键复制给架构师

5. 等待审查
   ↓
   架构师审查 → 通过/修改
```

---

**李明，任务已派发！期待你的完成报告！** 💪

**记住**：
- ✅ 先读提示词
- ✅ 后执行任务
- ✅ 必须提交完成报告

**工作愉快！**

---

## 📝 最后一步：提交完成（必做！）

每完成一个任务后，**立即执行**:

```bash
cd taskflow-v1.7-monorepo

# TASK-C-1完成后
python scripts/李明提交完成.py TASK-C-1 --hours <实际工时>

# TASK-C-2完成后
python scripts/李明提交完成.py TASK-C-2 --hours <实际工时>

# TASK-C-3完成后
python scripts/李明提交完成.py TASK-C-3 --hours <实际工时>
```

**示例**:
```bash
python scripts/李明提交完成.py TASK-C-1 --hours 2 --summary "FastAPI主入口已创建并测试"
```

**这会做什么**:
- ✅ 更新任务状态: in_progress → completed
- ✅ 记录实际工时
- ✅ Dashboard显示"📄 一键复制完成报告"按钮

**然后**: 在Dashboard点击按钮，复制完成报告，提交给架构师！

---

**架构师**: AI Architect (Expert Level)  
**派发时间**: 2025-11-19 01:02（已修订）  
**Dashboard**: http://localhost:8877（可查看任务详情）

