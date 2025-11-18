# 🚀 如何在Cursor中使用架构师AI

**版本**: v2.0  
**更新时间**: 2025-11-18  
**适用**: 任何项目（无需预先接入任务所·Flow）

---

## 🎯 概述

这份文档说明如何在**任何项目**中启动架构师AI，让它帮你：
1. 快速理解项目结构
2. 识别问题和风险
3. 规划重构路线
4. 拆解可执行任务

**核心优势**: 即插即用，无需预先配置

---

## ⚡ 快速开始（3步）

### Step 1：加载System Prompt

在Cursor中打开你的项目，然后：

**方式A：通过@引用**（推荐）
```
@docs/ai/architect-system-prompt.md 

认命你为这个项目的架构师
```

**方式B：复制System Prompt**
1. 打开 `docs/ai/architect-system-prompt.md`
2. 复制全部内容
3. 在Cursor对话中粘贴
4. 然后说：「认命你为这个项目的架构师」

**方式C：使用Rules for AI（永久生效）**
1. 打开Cursor设置 → Rules for AI
2. 添加新规则：「当用户说"架构师模式"时，加载architect-system-prompt」

### Step 2：架构师开始工作

**架构师会自动**：
1. 扫描项目目录结构
2. 读取README和配置文件
3. 选择性深入核心文件
4. 生成4份文档（inventory/review/refactor-plan/task-board）

**你只需要等待和回答问题**！

### Step 3：获取分析结果

**架构师会产出**：
- `docs/arch/architecture-inventory.md` - 项目概览
- `docs/arch/architecture-review.md` - 审查报告
- `docs/arch/refactor-plan.md` - 重构计划
- `docs/tasks/task-board.md` - 任务看板

**预计时间**: 5-15分钟（取决于项目规模）

---

## 📋 详细使用流程

### 阶段1：初次分析

#### 1.1 准备工作（可选）

**如果项目有目标结构**：
创建 `docs/arch/monorepo-structure.md` 说明理想目录结构

**如果有特殊要求**：
告诉架构师：
```
认命你为架构师。

特别关注：
- 我们计划从单体重构到微服务
- 重点审查认证和支付模块
- 需要评估数据库性能
```

#### 1.2 启动架构师

**标准启动**：
```
@docs/ai/architect-system-prompt.md

认命你为这个项目的架构师，请开始分析。
```

**带上下文启动**：
```
@docs/ai/architect-system-prompt.md
@README.md
@package.json

认命你为架构师。这是一个React + FastAPI的全栈项目，
当前单体部署，计划重构为Monorepo。
```

#### 1.3 等待分析

**架构师会**：
1. 扫描目录（1-2分钟）
2. 读取关键文件（3-5分钟）
3. 生成文档（2-5分钟）

**你可以做的**：
- 回答架构师的澄清问题
- 提供额外上下文
- 指定重点关注的模块

#### 1.4 review分析结果

**检查产出**：
```bash
# 查看生成的文档
ls docs/arch/
ls docs/tasks/

# 阅读关键文档
cat docs/arch/architecture-review.md
cat docs/tasks/task-board.md
```

**如果满意**：进入阶段2（执行任务）  
**如果不满意**：要求架构师深入特定模块

---

### 阶段2：执行任务

#### 2.1 选择任务

**从task-board.md中选择**：
```markdown
看任务看板，我想先完成：
- ARCH-001: 修复LLM错误处理
- ARCH-002: 补充API文档

请给我详细的实现提示词。
```

#### 2.2 切换到代码管家AI

**启动代码管家**：
```
@docs/ai/code-steward-system-prompt.md
@docs/tasks/task-board.md

请实现任务 ARCH-001: 修复LLM错误处理

（代码管家会自动读取任务详情并开始实现）
```

**或者直接说**：
```
现在切换到代码管家模式，实现任务ARCH-001
```

#### 2.3 任务完成后

**回到架构师更新状态**：
```
@docs/ai/architect-system-prompt.md

任务ARCH-001已完成，请更新架构分析和任务板。
```

---

### 阶段3：日常迭代

#### 3.1 定期更新（建议每周）

**唤醒架构师**：
```
@docs/ai/architect-system-prompt.md
@docs/arch/architecture-review.md
@docs/tasks/task-board.md

作为架构师，请查看最近的代码变更（git log --since="7 days ago"），
更新架构分析和任务板。
```

#### 3.2 重点审查

**针对特定模块**：
```
@docs/ai/architect-system-prompt.md

作为架构师，请深入审查 apps/api/src/auth/ 模块，
评估安全性和代码质量，更新architecture-review.md。
```

#### 3.3 调整计划

**根据实际进度**：
```
@docs/ai/architect-system-prompt.md
@docs/arch/refactor-plan.md

Phase A已完成80%，但发现新的性能问题，
请更新refactor-plan，调整优先级。
```

---

## 🔗 与任务所·Flow集成（可选但推荐）

### 为什么要集成？

**不集成** → 只有本地Markdown文档  
**集成后** → 文档 + 数据库 + Dashboard + API查询

**好处**：
- ✅ 任务可以在Dashboard中可视化
- ✅ 多人协作时任务状态同步
- ✅ 知识库可以被AI检索
- ✅ 历史问题和解决方案可追溯

### 集成步骤

#### Step 1：确保任务所·Flow运行中

```bash
# 检查任务所·Flow是否可访问
curl http://localhost:8870/health

# 或访问Dashboard
open http://localhost:8870
```

**如果没有任务所·Flow**：
```bash
# 克隆任务所·Flow
git clone https://github.com/eva-wanxin-git/taskflow-v1.5.git
cd taskflow-v1.5

# 启动
python start_dashboard.py
```

#### Step 2：配置项目连接

**创建配置文件**：`.taskflow.yaml`（项目根目录）

```yaml
# 任务所·Flow配置
taskflow:
  api_url: "http://localhost:8870"
  project_code: "MY_PROJECT"  # 你的项目代码
  auto_sync: true  # 自动同步任务到任务所

# 项目信息
project:
  name: "我的项目"
  description: "项目描述"
  repo_url: "https://github.com/xxx/my-project"
```

#### Step 3：告诉架构师使用任务所

**启动时说明**：
```
@docs/ai/architect-system-prompt.md
@.taskflow.yaml

认命你为架构师。

本项目已接入任务所·Flow（配置见.taskflow.yaml），
请在分析完成后，将结果同步到任务所系统。
```

**架构师会自动**：
1. 读取.taskflow.yaml配置
2. 调用任务所·Flow API
3. 创建项目和组件
4. 提交任务和问题
5. 记录到知识库

#### Step 4：在Dashboard查看

**访问Dashboard**：
```
http://localhost:8870
```

**可以看到**：
- 你的项目卡片
- 任务进度统计
- 组件状态
- 问题追踪

---

## 📊 架构师分析JSON格式

**当架构师完成分析后，会生成这样的JSON**：

```json
{
  "project_code": "MY_APP",
  "repo_root": "/Users/eva/workspace/my-app",
  
  "completed_features": [
    {
      "title": "用户登录系统",
      "description": "后端API + 前端登录页已完成，含基本验证",
      "related_paths": [
        "apps/api/src/auth/login.py",
        "apps/web/src/pages/Login.tsx"
      ],
      "completion": 0.95,
      "notes": "缺少密码重置功能"
    },
    {
      "title": "任务管理",
      "description": "完整的任务CRUD、状态流转、依赖关系",
      "related_paths": [
        "apps/api/src/tasks/",
        "database/schemas/tasks.sql"
      ],
      "completion": 1.0
    }
  ],
  
  "partial_features": [
    {
      "title": "审计日志",
      "description": "DB schema已有，API未实现，前端无页面",
      "related_paths": [
        "apps/api/src/audit/",
        "database/schemas/audit.sql"
      ],
      "completion": 0.5,
      "missing": ["API实现", "前端页面", "日志查询功能"],
      "risk": "合规要求可能受阻",
      "priority": "high"
    }
  ],
  
  "problems": [
    {
      "title": "LLM认证错误处理缺失",
      "description": "调用LLM失败时未捕获401/429，会中断整个流程",
      "severity": "high",
      "related_paths": ["packages/infra/llm/claude_client.py:45"],
      "impact": "用户体验差，服务不稳定",
      "suggested_solution": "添加重试机制和降级策略"
    },
    {
      "title": "前端状态管理混乱",
      "description": "多个store互相依赖，难以维护",
      "severity": "medium",
      "related_paths": ["apps/web/src/store/"],
      "impact": "新功能开发困难",
      "suggested_solution": "重构为模块化store"
    }
  ],
  
  "suggested_tasks": [
    {
      "id": "ARCH-001",
      "title": "为LLM调用补上错误处理与重试机制",
      "type": "backend",
      "priority": "high",
      "component": "infra-llm",
      "description": "在claude_client中补上对401/429的重试与降级策略",
      "related_paths": [
        "packages/infra/llm/claude_client.py"
      ],
      "acceptance_criteria": [
        "401/403/429情况下不会直接抛出未捕获异常",
        "有至少3次退避重试",
        "错误被记录到日志中"
      ],
      "estimated_hours": 4.0,
      "executor_type": "code-steward",
      "dependencies": []
    },
    {
      "id": "ARCH-002",
      "title": "完成审计日志功能",
      "type": "feature",
      "priority": "high",
      "component": "api-audit",
      "description": "基于现有schema，实现完整的审计日志API和前端展示",
      "acceptance_criteria": [
        "API端点：POST /api/audit/log, GET /api/audit/logs",
        "前端审计日志页面",
        "支持筛选和导出"
      ],
      "estimated_hours": 16.0,
      "executor_type": "code-steward",
      "dependencies": []
    }
  ],
  
  "metadata": {
    "analyzed_at": "2025-11-18T15:00:00Z",
    "analyzer": "AI Architect v2",
    "files_scanned": 45,
    "files_deep_read": 12,
    "token_used": 65000
  }
}
```

---

## 🔌 提交分析到任务所·Flow

### 方式1：通过API（Python示例）

**创建脚本**：`submit_to_taskflow.py`

```python
#!/usr/bin/env python3
import requests
import json

# 从架构师生成的JSON文件读取
with open('architect_analysis.json', 'r') as f:
    analysis = json.load(f)

# 提交到任务所·Flow
response = requests.post(
    "http://localhost:8870/api/architect/analysis",
    json=analysis
)

if response.status_code == 200:
    result = response.json()
    print(f"✓ 已同步到任务所·Flow")
    print(f"  - 创建任务：{result['tasks_created']}个")
    print(f"  - 记录问题：{result['issues_created']}个")
    print(f"  - 创建组件：{result['components_created']}个")
    print(f"\n访问Dashboard查看：http://localhost:8870")
else:
    print(f"✗ 提交失败：{response.text}")
```

**运行**：
```bash
python submit_to_taskflow.py
```

### 方式2：让架构师自动提交

**在Cursor中说**：
```
@docs/ai/architect-system-prompt.md
@.taskflow.yaml

架构师，分析完成后，请将结果提交到任务所·Flow系统
（配置在.taskflow.yaml中）
```

**架构师会**：
1. 读取配置获取API地址
2. 构造分析JSON
3. 调用POST /api/architect/analysis
4. 报告提交结果

### 方式3：手动提交（如果API调用失败）

**保存JSON**：
架构师会在回复中给出完整JSON，复制到文件：
```bash
# 保存
cat > architect_analysis.json
[粘贴JSON]
Ctrl+D

# 手动提交
curl -X POST http://localhost:8870/api/architect/analysis \
  -H "Content-Type: application/json" \
  -d @architect_analysis.json
```

---

## 🎭 多AI角色协作

### 场景：完整的开发流程

#### Step 1：架构师规划
```
@docs/ai/architect-system-prompt.md

认命你为架构师，请分析这个项目。
```
**产出**：4份文档 + 任务列表

---

#### Step 2：代码管家实现
```
@docs/ai/code-steward-system-prompt.md
@docs/tasks/task-board.md

请实现任务ARCH-001
```
**产出**：代码 + 测试 + 文档更新

---

#### Step 3：架构师审查
```
@docs/ai/architect-system-prompt.md

任务ARCH-001已完成，请审查代码质量，
判断是否符合验收标准。
```
**产出**：审查意见 + 是否通过

---

#### Step 4：SRE配置运维
```
@docs/ai/sre-system-prompt.md

请为新功能（Token刷新）设计监控和告警。
```
**产出**：监控指标 + 告警规则 + Runbook

---

### 角色切换技巧

**明确指定角色**：
```
# 架构师模式
@docs/ai/architect-system-prompt.md
作为架构师...

# 代码管家模式
@docs/ai/code-steward-system-prompt.md
作为代码管家...

# SRE模式
@docs/ai/sre-system-prompt.md
作为SRE...
```

**角色职责边界**：
```
问题：需要重构某个模块
谁负责？
- 架构师：制定重构计划、定义验收标准
- 代码管家：执行具体重构、写测试
- SRE：确保重构不影响稳定性、准备回滚

做法：
1. 架构师先规划（写refactor-plan）
2. 代码管家实现（改代码+测试）
3. SRE配置监控（告警+回滚）
```

---

## 💡 实用技巧

### 技巧1：增量分析

**不要一次分析所有代码**：
```
# ❌ 不好
认命你为架构师，分析整个项目的所有细节

# ✅ 好
认命你为架构师，先做整体扫描，
然后我会告诉你重点深入哪些模块
```

**分批深入**：
```
# 第一批：核心业务
请深入分析 apps/api/src/core/ 模块

# 第二批：认证授权
请深入分析 apps/api/src/auth/ 模块

# 第三批：前端
请深入分析 apps/web/src/pages/ 主要页面
```

### 技巧2：问题驱动

**带着问题让架构师分析**：
```
@docs/ai/architect-system-prompt.md

认命你为架构师。

我们的问题：
1. 系统响应慢（API延迟>2s）
2. 代码难以维护（新功能开发困难）
3. 测试覆盖率低（<30%）

请重点分析这些问题的根因，并给出解决方案。
```

### 技巧3：对照目标结构

**提供理想状态**：
```
@docs/ai/architect-system-prompt.md
@docs/arch/monorepo-structure.md

认命你为架构师。

我们的目标结构在 monorepo-structure.md 中，
请对比当前实现与目标的差距，制定迁移计划。
```

### 技巧4：利用Git历史

**让架构师看变更**：
```
@docs/ai/architect-system-prompt.md

作为架构师，请查看最近10次提交（git log -10），
评估代码质量趋势，是在改善还是恶化？
```

---

## 🎯 完整示例：从零开始

### 示例项目：一个React + FastAPI的待办事项应用

#### 1. 初次启动

**用户说**：
```
@docs/ai/architect-system-prompt.md

认命你为这个项目的架构师。

这是一个待办事项管理应用：
- 后端：Python + FastAPI
- 前端：React + TypeScript
- 数据库：PostgreSQL

当前问题：
- 代码比较混乱，没有清晰的模块划分
- 测试几乎没有
- 想重构为Monorepo结构

请帮我分析并制定重构计划。
```

#### 2. 架构师工作（10分钟）

**架构师会**：
1. 扫描目录结构
2. 读取主要文件（main.py, App.tsx, schema.sql等）
3. 生成4份文档

**产出示例**：

**architecture-inventory.md**：
```markdown
# 项目架构清单

## 基本信息
- 项目名称：Todo App
- 技术栈：FastAPI + React + PostgreSQL
- 部署：Docker Compose

## 目录结构
```
todo-app/
├── backend/
│   ├── main.py（150行）
│   ├── models.py（80行）
│   └── database.py（100行）
├── frontend/
│   ├── src/
│   │   ├── App.tsx（200行）
│   │   └── components/（5个组件）
│   └── package.json
├── database/
│   └── schema.sql
└── docker-compose.yml
```

## 代码规模
- 总文件数：23
- 总行数：~3000
- 后端：1200行
- 前端：1800行
```

**architecture-review.md**：
```markdown
# 架构审查报告

## ✅ 已实现功能
1. ✅ 用户登录（100%）
2. ✅ 待办CRUD（100%）
3. ✅ 待办标签（90%，缺前端展示）

## 🟡 部分实现
1. ⚠️ 待办分享（50% - 后端有API，前端无UI）
2. ⚠️ 通知系统（30% - DB设计完成，未实现）

## 🔴 发现的问题
1. 🔴 High：认证未加密传输（使用HTTP）
2. 🟡 Medium：数据库连接未使用连接池
3. 🟡 Medium：前端无错误边界

## 💳 技术债务
1. backend/所有代码在3个文件中（混乱）
2. 前端无状态管理（prop drilling严重）
3. 无测试代码
```

**refactor-plan.md**：
```markdown
# 重构计划

## 目标：Monorepo + 清晰分层

## 阶段A：目录重组（1周）
- [ ] 创建monorepo结构（apps/packages）
- [ ] 后端拆分为模块（auth/tasks/...）
- [ ] 前端添加状态管理（Redux Toolkit）

## 阶段B：测试补充（1周）
- [ ] 后端单元测试（覆盖率80%+）
- [ ] 前端组件测试
- [ ] E2E测试（登录+创建待办）

## 阶段C：安全增强（3天）
- [ ] 启用HTTPS
- [ ] 添加CORS配置
- [ ] 输入验证加强
```

**task-board.md**：
```markdown
# 任务看板

## 📊 统计
- 总任务：15
- P0：3
- P1：6
- P2：6

## 任务列表

### ARCH-001: 启用HTTPS（P0）
- 类型：security
- 预估：2小时
- 执行者：SRE AI

### ARCH-002: 后端模块化拆分（P1）
- 类型：refactor
- 预估：8小时
- 执行者：代码管家AI

[...]
```

#### 3. 提交到任务所（1分钟）

**自动提交**：
架构师会调用API提交，或者用户运行：
```bash
python submit_to_taskflow.py
```

#### 4. 开始执行

**在Dashboard查看任务**：
```
http://localhost:8870

看到：
- Todo App项目卡片
- 15个任务
- 3个高优先级任务
```

**开始实现**：
```
@docs/ai/code-steward-system-prompt.md

请实现任务ARCH-001: 启用HTTPS
```

---

## 🔧 故障排查

### Q1：架构师不工作？

**检查**：
```
1. 是否正确加载了System Prompt？
   → 用@引用或复制完整prompt

2. 是否说了启动关键词？
   → 必须说"认命"或"架构师"

3. Token是否充足？
   → 至少需要50k可用token
```

### Q2：文档生成不完整？

**可能原因**：
- Token不足
- 项目太大，架构师选择性跳过

**解决方案**：
```
请继续完成 architecture-review.md，
重点分析后端认证模块。
```

### Q3：任务所·Flow API调用失败？

**检查**：
```bash
# 1. 任务所是否运行？
curl http://localhost:8870/health

# 2. 配置文件是否正确？
cat .taskflow.yaml

# 3. 网络是否可达？
ping localhost
```

**解决**：
```
如果API不可用，架构师会退回到"仅文档模式"，
所有内容只保存在本地Markdown中。

等任务所启动后，可以手动提交：
python submit_to_taskflow.py
```

---

## 📚 参考资源

### System Prompts
- `docs/ai/architect-system-prompt.md` - 架构师
- `docs/ai/code-steward-system-prompt.md` - 代码管家
- `docs/ai/sre-system-prompt.md` - SRE

### 工作流程
- `docs/arch/architect-workflow.md` - 详细工作流程

### API文档
- 任务所·Flow API：http://localhost:8870/docs

---

## 🎊 总结

### 最简单的使用方式

**3步启动**：
```bash
# 1. 在Cursor中加载prompt
@docs/ai/architect-system-prompt.md

# 2. 认命架构师
认命你为这个项目的架构师

# 3. 等待分析完成
（5-15分钟后获得4份文档）
```

### 最完整的使用方式

**集成任务所·Flow**：
1. 启动任务所·Flow服务
2. 创建.taskflow.yaml配置
3. 架构师分析并自动提交
4. 在Dashboard查看和管理任务
5. 多AI角色协作开发

---

**文档版本**：v2.0  
**最后更新**：2025-11-18  
**状态**：✅ 即插即用

🚀 **任何项目都可以立即使用架构师AI！**

