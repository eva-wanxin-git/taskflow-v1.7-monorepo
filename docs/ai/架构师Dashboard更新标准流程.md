# 📋 架构师Dashboard更新标准流程

**版本**: v1.0  
**适用**: 任何接入任务所·Flow的项目  
**目标**: 让Dashboard显示项目的真实状态

---

## 🎯 核心理念

**Dashboard = 产品 = 用户看到的全部**

用户看不到代码、数据库、文档，  
用户只能看到浏览器里的Dashboard界面。

所以架构师接手项目后，**必须立即更新Dashboard数据**，  
让用户在界面上看到项目的完整真实状态。

---

## 📊 Dashboard内容分类

### 🔒 通用内容（不需要更新，所有项目通用）

| 内容 | 位置 | 说明 |
|------|------|------|
| AI System Prompts | 09-role-prompts/ | 4套提示词(架构师/工程师/代码管家/SRE) |
| 协作指南 | 09-role-prompts/ | AI-TEAM-GUIDE等 |
| 标准规范 | 08-standards/ | 编码规范/Git规范 |
| 模板文件 | 15-templates/ | 任务模板/Bug模板 |
| UX/UI库 | 04-ux-library, 05-ui-library | 设计规范 |

**这些内容一次配置，所有项目通用，不需要每个项目都更新。**

---

### 🔄 项目特定内容（必须更新，每个项目不同）

| 内容 | 位置 | Dashboard显示位置 | 更新频率 |
|------|------|------------------|---------|
| **功能清单(已实现)** | v17-complete-features.json | 功能清单→已实现功能 | 每次架构师分析 |
| **功能清单(部分实现)** | v17-complete-features.json | 功能清单→部分实现功能 | 每次架构师分析 |
| **问题清单(冲突建议)** | v17-complete-features.json | 功能清单→冲突/建议取舍 | 每次架构师分析 |
| **待完成任务** | database/data/tasks.db | 待完成的功能清单 | 任务创建/更新时 |
| **架构师事件流** | architect_events.json | ARCHITECT MONITOR→事件流 | 实时记录 |
| **架构师对话** | architect-conversations.json | ARCHITECT MONITOR→对话交流 | 实时记录 |
| **Token使用** | architect_monitor.json | ARCHITECT MONITOR顶部 | 实时更新 |
| **重要信息** | architect-notes/ | ARCHITECT MONITOR→重要信息 | 按需更新 |
| **项目背景** | 01-background/ | （内部数据，不直接展示） | 一次性 |
| **开发问题库** | developer-knowledge/problems.md | 开发者知识库 | 遇到问题时 |
| **测试用例库** | tester-knowledge/cases.md | 测试工程师知识库 | 有测试时 |
| **故障记录** | ops/incidents.md | 运维SRE知识库 | 有故障时 |
| **交付文档** | delivery-docs/ | 交付工程师 | 项目交付时 |

---

## 🚀 标准操作流程（架构师接手新项目）

### 阶段1: 接受任命（1分钟）

**用户操作**:
```markdown
@docs/ai/architect-system-prompt-expert.md

认命你为【项目名称】的总架构师
```

**架构师确认**:
```
✅ 已接受【项目名称】总架构师任命
开始工作...
```

---

### 阶段2: 代码审查（10-20分钟）

**扫描项目代码**:
- 目录结构（1-2层）
- 关键文件（10-20个）
- 配置文件
- README等文档

**识别功能状态**:
- 已实现功能：列出所有已完成的功能（**细粒度**）
- 部分实现功能：列出半成品（带完成度%）
- 问题清单：识别Critical/High/Medium/Low问题

**示例（细粒度）**:
```
❌ 错误示例（粗粒度）:
- ✅ 后端API
- ✅ 前端界面
- ✅ 数据库

✅ 正确示例（细粒度）:
- ✅ SQLite数据库持久化
- ✅ StateManager状态管理
- ✅ 3表任务数据库
- ✅ 任务CRUD操作
- ✅ GET /api/tasks端点
- ✅ GET /api/stats端点
- ✅ 实时任务列表UI
- ✅ 统计卡片(4个指标)
- ✅ 进度条可视化
... (列出所有具体功能)
```

**粒度要求**:
- 一个功能 = 一个具体的类/函数/API端点/UI组件
- 不要：一个功能 = 一个大模块
- 目标：用户能清楚知道具体实现了什么

---

### 阶段3: 生成功能清单JSON（5分钟）

**创建脚本**: `scripts/生成_{项目代码}_功能清单.py`

**模板**:
```python
FEATURES = {
    "implemented": [
        {"id": "FEAT-001", "name": "具体功能名", "type": "类型", "file": "文件路径", "version": "v1.0", "completion": 1.0},
        {"id": "FEAT-002", "name": "...", ...},
        ... (列出所有已实现功能)
    ],
    "partial": [
        {"id": "PART-001", "name": "半成品名", "type": "类型", "completion": 0.5, "missing": ["缺少什么"], "priority": "P0", "estimated_hours": 2.0, "task_id": "TASK-001"},
        ... (列出所有半成品)
    ],
    "conflicts": [
        {"id": "CONF-001", "name": "问题名", "severity": "Critical", "impact": "影响", "suggestion": "建议", "estimated_fix_hours": 2.0},
        ... (列出所有问题)
    ]
}
```

**运行脚本**:
```bash
python scripts/生成_{项目代码}_功能清单.py
# 生成: apps/dashboard/automation-data/{项目代码}-features.json
```

---

### 阶段4: 更新Dashboard API（5分钟）

**修改**: `apps/dashboard/src/industrial_dashboard/dashboard.py`

**找到`/api/project_scan`端点**，修改为：
```python
@self.app.get("/api/project_scan")
async def get_project_scan():
    """获取项目扫描结果"""
    try:
        # 读取项目功能清单JSON
        features_file = Path("automation-data/{项目代码}-features.json")
        if features_file.exists():
            with open(features_file, 'r', encoding='utf-8') as f:
                complete_data = json.load(f)
            
            implemented = complete_data.get("implemented", [])
            partial = complete_data.get("partial", [])
            conflicts = complete_data.get("conflicts", [])
            
            return JSONResponse(content={
                "features": {
                    "implemented": implemented,
                    "partial": partial,
                    "conflicts": conflicts
                },
                "summary": {
                    "total_features": len(implemented) + len(partial),
                    "implemented": len(implemented),
                    "partial": len(partial),
                    "conflicts": len(conflicts)
                }
            })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
```

---

### 阶段5: 任务拆解并录入数据库（10分钟）

**拆解任务**:
- 根据架构审查发现的问题
- 拆解成可执行任务（有验收标准）
- 识别依赖关系
- 标注优先级和工时

**创建录入脚本**: `scripts/录入_{项目代码}_任务.py`

**模板**:
```python
TASKS = [
    {
        "id": "TASK-001",
        "title": "任务标题",
        "description": "详细描述",
        "status": "pending",
        "priority": "P0",
        "estimated_hours": 2.0,
        "complexity": "LOW",
        "project_id": "{项目代码}",
        "assigned_to": "fullstack-engineer",
        "created_at": datetime.now().isoformat()
    },
    ...
]

DEPENDENCIES = [
    ("TASK-002", "TASK-001"),  # TASK-002依赖TASK-001
    ...
]
```

**运行脚本**:
```bash
python scripts/录入_{项目代码}_任务.py
# 将任务录入database/data/tasks.db
```

---

### 阶段6: 更新事件流（5分钟）

**创建**: `automation-data/architect_events.json`

**记录所有工作事件**（每次与用户沟通/每个重要操作）:
```json
{
  "events": [
    {
      "id": "event-001",
      "timestamp": "2025-11-18 22:00:00",
      "type": "role_assignment",
      "icon": "🏛️",
      "content": "用户任命：担任【项目名称】总架构师"
    },
    {
      "id": "event-002",
      "timestamp": "2025-11-18 22:05:00",
      "type": "code_review",
      "icon": "🔍",
      "content": "代码扫描：审查10个核心文件"
    },
    ... (记录每个工作步骤和用户反馈)
  ]
}
```

**粒度要求**:
- 每次用户沟通 = 1个事件
- 每个重要操作 = 1个事件
- 让用户能追溯完整工作过程

---

### 阶段7: 更新项目特定知识库（10分钟）

**必须更新的文件**:

#### 1. 开发者知识库
**developer-knowledge/problems.md**:
```markdown
# 开发问题解决库

## {项目名}常见问题

### 1. 具体问题
**问题**: ...
**根因**: ...
**解决**: ...
**位置**: ...
```

#### 2. 运维故障记录
**ops/incidents.md**:
```markdown
# 故障记录

## 2025-XX-XX {项目名}具体故障

**问题描述**: ...
**根因分析**: ...
**解决方案**: ...
**预防措施**: ...
```

#### 3. 项目背景
**01-background/project-overview.md**:
```markdown
# 项目概览

## {项目名称}

**Slogan**: ...
**项目定位**: ...
**核心能力**: ...
**技术架构**: ...
**当前状态**: ...
```

**01-background/technical-stack.md**:
```markdown
# 技术栈

## 后端
- Python x.x
- FastAPI x.x
- ...

## 前端
- React/Vue/原生
- ...

(具体技术栈)
```

#### 4. 架构师监控数据
**architect_monitor.json**:
```json
{
  "token_usage": {
    "used": 实际值,
    "total": 1000000,
    "percentage": 实际百分比
  },
  "project_info": {
    "name": "项目名称",
    "code": "PROJECT_CODE",
    "completion": 实际完成度,
    "total_features": 实际功能数
  }
}
```

---

### 阶段8: 重启Dashboard并自动打开浏览器（2分钟）

**操作**:
```bash
# 1. 停止旧进程
Stop-Process -Name python -Force

# 2. 如果需要避免缓存，换新端口
# 修改start_dashboard.py的port值

# 3. 启动Dashboard
cd apps/dashboard
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python start_dashboard.py"

# 4. 等待启动（5-8秒）
Start-Sleep -Seconds 8

# 5. 自动打开浏览器
Start-Process "http://localhost:{端口}"
```

**注意**:
- 每次重大更新建议换新端口（避免浏览器缓存）
- 端口范围：8870-8899
- 让用户看到最新内容

---

## 📊 Dashboard必须显示的项目内容

### 模块1: 功能清单（细粒度）⭐ 核心

**Tab 1: 已实现功能**
- **要求**: 细粒度列举所有已实现功能
- **粒度**: 1个功能 = 1个类/函数/API/UI组件
- **数量**: 通常50-150个（取决于项目规模）
- **格式**: 
  ```
  ✓ 功能名称
    文件: 具体文件路径 | 类型: 功能类型
  ```

**示例（正确）**:
```
✓ SQLite数据库持久化 (文件: database/db.py | 类型: 基础设施)
✓ 用户注册API (文件: routes/auth.py | 类型: 后端API)
✓ 登录表单组件 (文件: components/LoginForm.tsx | 类型: 前端)
```

**示例（错误）**:
```
✓ 后端功能  ❌ (太粗)
✓ 前端界面  ❌ (太粗)
```

---

**Tab 2: 部分实现功能**
- **要求**: 列出所有半成品
- **必须包含**: 
  - 完成度% (0%, 10%, 50%等)
  - 缺少什么（具体列表）
  - 优先级(P0/P1/P2/P3)
  - 预估工时
  - 对应任务ID（如有）

**格式**:
```
⚠️ 功能名 (完成度%)
   缺少: [具体缺失1, 具体缺失2]
   优先级: P0
   工时: 2.0h
   任务: TASK-001
```

---

**Tab 3: 冲突/建议取舍**
- **要求**: 列出所有问题（按严重程度）
- **分类**: Critical → High → Medium → Low
- **必须包含**:
  - 严重程度
  - 影响描述
  - 建议解决方案
  - 预估修复工时
  - 阻塞的任务（如有）

**格式**:
```
🔴 问题名 (Critical)
   影响: 具体影响描述
   建议: 具体解决方案
   修复工时: 2.0h
   阻塞任务: TASK-002, TASK-003
```

---

### 模块2: 待完成的功能清单

**要求**: 显示所有待办任务（从数据库读取）

**任务卡片格式**:
```
[P0] TASK-001: 任务标题
     描述: 任务详细描述
     ⏱️ 2.0h | 👤 fullstack-engineer | 🔧 LOW
     状态: 待处理
```

**排序**: 按优先级（P0→P1→P2→P3）

**来源**: database/data/tasks.db的tasks表

---

### 模块3: ARCHITECT MONITOR ⭐ 核心

**Tab 1: 事件流**
- **要求**: 记录所有工作事件（完整）
- **粒度**: 每次用户沟通 = 1个事件，每个重要操作 = 1个事件
- **格式**:
  ```json
  {
    "id": "event-001",
    "timestamp": "2025-11-18 22:00:00",
    "type": "role_assignment",
    "icon": "🏛️",
    "content": "具体描述",
    "metadata": {}
  }
  ```

**示例事件类型**:
- role_assignment: 任命
- code_review: 代码审查
- document: 文档产出
- bugfix: Bug修复
- user_feedback: 用户反馈
- diagnosis: 问题诊断
- data_update: 数据更新

---

**Tab 2: 对话交流**
- 记录架构师与用户的对话
- 每次请求和响应

---

**Tab 3: 动态提示词**
- 显示架构师的完整System Prompt
- 可滚动查看（600px高度）
- 可复制

**注意**: 这个是通用内容，不需要每个项目都更新

---

**Tab 4: 重要信息**
- 重大需求变更（requirements.md）
- 架构师交接提示词（handoff.md）
- Bug进度清单（bugs.md）
- 技术决策记录（decisions.md）

**这些需要根据项目实际情况填写**

---

### 模块4: 各角色知识库

**开发者知识库**:
- problems.md: 项目特定问题和解决方案
- tools.md: 项目使用的工具（可选更新）
- standards.md: 项目规范（可选更新）
- tips.md: 项目最佳实践（可选更新）

**测试知识库**:
- cases.md: 项目测试用例
- bugs.md: 项目Bug记录

**运维知识库**:
- incidents.md: 项目故障记录
- troubleshooting.md: 项目问题排查
- lessons.md: 项目经验教训
- metrics.md: 项目性能基线

**交付文档**:
- environment.md: 项目环境说明
- tools.md: 项目工具链

---

## 📋 快速检查清单

架构师完成Dashboard更新后，检查：

### 必查项（项目特定）
- [ ] 功能清单→已实现：是否细粒度（50+个）？
- [ ] 功能清单→部分实现：是否有完成度%和缺失列表？
- [ ] 功能清单→冲突建议：是否按严重程度分类？
- [ ] 待完成任务：是否显示所有任务？
- [ ] 事件流：是否记录了所有工作？
- [ ] Token数据：是否是实际值？
- [ ] 项目背景：是否填写了项目信息？

### 可选项（按需更新）
- [ ] 开发问题库：是否记录了项目问题？
- [ ] 测试用例：是否有测试？
- [ ] 故障记录：是否有运维操作？
- [ ] 交付文档：是否有环境说明？

---

## 🎯 即插即用流程总结

```
用户任命架构师
    ↓
架构师扫描项目(10-20分钟)
    ↓
生成功能清单JSON (细粒度：已实现+部分实现+冲突)
    ↓
任务拆解并录入数据库
    ↓
更新事件流（每次沟通/操作）
    ↓
更新项目特定知识库（问题/故障/背景）
    ↓
重启Dashboard + 换新端口
    ↓
自动打开浏览器
    ↓
用户看到完整的项目状态！
```

**总耗时**: 30-50分钟  
**产出**: 用户在Dashboard看到完整的项目状态

---

## ⚠️ 关键注意事项

### 1. 粒度要求
- ❌ 不要：一个功能 = 一个大模块
- ✅ 要：一个功能 = 一个具体实现

### 2. 数据完整性
- 功能清单：必须细粒度（50+个）
- 部分实现：必须有完成度%
- 冲突：必须按严重程度分类
- 事件流：必须记录所有沟通

### 3. 浏览器缓存
- 重大更新建议换端口
- 端口范围：8870-8899
- 自动打开浏览器
- 让用户立即看到新内容

### 4. 实时更新
- Token数据：使用实际值（从Cursor状态栏读取）
- 事件流：每次操作都记录
- 任务状态：及时同步

---

## 📁 标准文件结构

```
apps/dashboard/automation-data/
│
├── 【项目特定，必须更新】
│   ├── {项目代码}-features.json        ⭐ 功能清单(细粒度)
│   ├── architect_events.json           ⭐ 事件流(完整)
│   ├── architect_monitor.json          ⭐ Token+状态
│   ├── architect-conversations.json    ⭐ 对话记录
│   ├── architect-notes/               ⭐ 重要信息(4个)
│   ├── developer-knowledge/problems.md ⭐ 项目问题
│   ├── tester-knowledge/cases.md       项目测试
│   ├── ops/incidents.md                ⭐ 项目故障
│   ├── delivery-docs/environment.md    项目环境
│   └── 01-background/                  项目背景
│
└── 【通用内容，不需要更新】
    ├── 09-role-prompts/                AI提示词(所有项目通用)
    ├── 08-standards/                   标准规范(通用)
    ├── 15-templates/                   模板(通用)
    └── ...其他
```

---

## 🚀 使用示例

### 场景：架构师接手新项目"LibreChat-Desktop"

**Step 1**: 用户任命
```
@architect-system-prompt-expert.md
认命你为LibreChat-Desktop的总架构师
```

**Step 2**: 架构师扫描（15分钟）
- 扫描librechat-desktop目录
- 识别已实现功能（细粒度，假设80个）
- 识别半成品（假设6个）
- 识别问题（假设5个）

**Step 3**: 生成功能清单（5分钟）
```python
# scripts/生成_librechat_功能清单.py
FEATURES = {
    "implemented": [
        {"id": "FEAT-001", "name": "Electron主进程初始化", ...},
        {"id": "FEAT-002", "name": "LibreChat配置加载", ...},
        ... (80个)
    ],
    "partial": [
        {"id": "PART-001", "name": "AWS Bedrock集成", "completion": 0.3, ...},
        ... (6个)
    ],
    "conflicts": [
        {"id": "CONF-001", "name": "MCP服务器连接不稳定", ...},
        ... (5个)
    ]
}
```

**Step 4**: 拆解任务（10分钟）
```python
# scripts/录入_librechat_任务.py
TASKS = [
    {"id": "LC-001", "title": "完成AWS Bedrock集成", ...},
    {"id": "LC-002", "title": "修复MCP连接", ...},
    ... (假设10个任务)
]
```

**Step 5**: 更新事件流（5分钟）
```json
{
  "events": [
    {"id": "event-001", "content": "接受LibreChat-Desktop架构师任命"},
    {"id": "event-002", "content": "扫描16个Electron文件"},
    {"id": "event-003", "content": "识别80个已实现功能"},
    ...
  ]
}
```

**Step 6**: 更新知识库（10分钟）
- 项目背景 → LibreChat Desktop项目介绍
- 开发问题 → Electron打包问题/MCP连接问题
- 故障记录 → （如有）

**Step 7**: 重启Dashboard
```bash
# 换到8876端口（如之前用过8870-8875）
# 启动并自动打开浏览器
```

**完成！用户在Dashboard看到LibreChat-Desktop的完整状态！**

---

## 🎊 标准化成果

通过这个流程，任何项目：
- ✅ 30-50分钟完成Dashboard更新
- ✅ 用户看到完整的项目状态（细粒度）
- ✅ 功能清单、任务、事件流全部最新
- ✅ 即插即用，可复制到任何项目

---

**流程版本**: v1.0  
**创建时间**: 2025-11-19  
**验证项目**: 任务所·Flow v1.7  
**状态**: ✅ 已验证有效

📋 **这就是架构师接手项目更新Dashboard的标准流程！**

