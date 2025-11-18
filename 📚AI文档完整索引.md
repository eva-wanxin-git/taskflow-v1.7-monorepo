# 📚 AI文档完整索引 - 任务所·Flow v1.7

**更新时间**: 2025-11-18 23:35  
**文档总数**: 9个 (200KB)  
**AI提示词**: 4套 (127KB, 24500字)

---

## 🎯 AI文档全览

### 核心System Prompts (4套，24500字)

| 角色 | 文件名 | 大小 | 字数 | 经验等级 | 核心特点 |
|------|--------|------|------|---------|---------|
| 🏛️ **架构师** | architect-system-prompt-expert.md | 47KB | 8000字 | Staff Engineer (10-15年) | 深度理解/质疑盲从/3方案对比 |
| 👨‍💻 **全栈工程师** | fullstack-engineer-system-prompt.md | 30KB | 7000字 | 满级工程师 (10年) | 前置自查/完成报告/7部分标准 |
| 🧰 **代码管家** | code-steward-system-prompt.md | 24KB | 5000字 | 实现专家 (8年) | 最小改动/测试≥80%/质量保证 |
| 🛡️ **SRE** | sre-system-prompt.md | 26KB | 4500字 | 运维专家 | 5大职责/监控告警/事故处理 |

**总计**: 127KB, 24500字完整AI团队体系

---

### 协作指南 (3份)

#### 1. AI-TEAM-GUIDE.md (14KB)
**AI团队协作指南**

**内容**:
- 🚀 快速开始: 3步启动AI团队
- 📋 详细使用流程: 阶段1-4完整流程
- 🔄 标准工作流: 架构师→工程师→SRE闭环
- 📊 场景示例: 新项目/重构/Bug修复/功能开发
- 🎯 最佳实践: Token管理/质量标准/交接机制

**适用场景**: 
- ✅ 新项目快速接入任务所
- ✅ 多AI角色协作
- ✅ 标准化工作流程

**使用方式**:
```markdown
@docs/ai/AI-TEAM-GUIDE.md

请按照AI团队协作指南的流程，
启动【项目名称】的完整AI团队。
```

---

#### 2. how-to-use-architect-with-cursor.md (20KB)
**如何在Cursor中使用架构师AI**

**内容**:
- ⚡ 3步快速开始
- 📋 详细使用流程(初次分析/日常迭代/交接)
- 🎯 架构师会产出什么(4份文档)
- 💡 使用技巧(Token优化/分阶段审查)
- 🔗 与任务所Flow集成(API调用)
- 🚀 场景示例(5个实战场景)

**适用场景**:
- ✅ 任何项目即插即用
- ✅ 无需预先配置
- ✅ 10分钟快速分析

**使用方式**:
```markdown
@docs/ai/how-to-use-architect-with-cursor.md

请按照Cursor使用指南，帮我分析【项目名称】
```

---

#### 3. architect-onboarding-checklist.md (5KB)
**架构师接手项目检查清单**

**内容**:
- 📍 Step 0: 端口分配(PortManager)
- ✅ Step 1-4: 标准接手流程
- 📋 必须产出清单(4份文档)
- 🔗 任务所Flow集成

**适用场景**:
- ✅ 架构师接手新项目
- ✅ 标准化流程checklist
- ✅ 确保不遗漏关键步骤

---

### 工具模板 (2份)

#### 4. task-prompt-template.md (6KB)
**单次任务提示词模板**

**内容**:
- 📝 完整的任务提示词模板
- 填空即用
- 包含前置提醒/任务内容/验收标准/参考资料

**使用方式**:
1. 复制模板
2. 填写【】占位符
3. 发送给全栈工程师·李明

**示例任务**:
```markdown
# 【任务所·Flow】全栈开发任务说明

**任务接收人**：全栈工程师·李明  
**任务ID**：TASK-C-1  
**任务标题**：创建FastAPI主应用入口

...
```

---

#### 5. architect-system-prompt.md (26KB)
**标准版架构师Prompt**

**说明**: 这是简化版，建议使用expert版本

**对比**:
- architect-system-prompt.md: 标准版(26KB)
- architect-system-prompt-expert.md: 专家版(47KB) ⭐ 推荐

---

## 📍 文档位置

### 在项目中
```
taskflow-v1.7-monorepo/
└── docs/
    └── ai/
        ├── architect-system-prompt-expert.md    ⭐ 架构师(专家级)
        ├── architect-system-prompt.md           标准版
        ├── fullstack-engineer-system-prompt.md  ⭐ 全栈工程师
        ├── code-steward-system-prompt.md        ⭐ 代码管家
        ├── sre-system-prompt.md                 ⭐ SRE
        ├── AI-TEAM-GUIDE.md                     ⭐ 团队协作指南
        ├── how-to-use-architect-with-cursor.md  ⭐ Cursor使用指南
        ├── architect-onboarding-checklist.md    架构师入职清单
        └── task-prompt-template.md              任务模板
```

### 在Dashboard中
```
apps/dashboard/automation-data/
├── 09-role-prompts/
│   ├── architect-prompt.md                    (47KB) ✅
│   ├── developer-prompt.md                    (30KB) ✅
│   ├── code-steward-prompt.md                 (24KB) ✅
│   ├── ops-prompt.md                          (26KB) ✅
│   ├── AI-TEAM-GUIDE.md                       (14KB) ✅
│   ├── how-to-use-architect-with-cursor.md    (20KB) ✅
│   └── architect-onboarding-checklist.md      (5KB) ✅
└── 15-templates/
    └── task-prompt-template.md                (6KB) ✅
```

**总计**: 172KB，全部已加载到Dashboard ✅

---

## 🎯 使用场景指南

### 场景1: 新项目快速分析（10-15分钟）

**使用文档**: 
- `how-to-use-architect-with-cursor.md` - Cursor使用指南
- `architect-system-prompt-expert.md` - 架构师Prompt

**步骤**:
```markdown
@docs/ai/architect-system-prompt-expert.md

认命你为【项目名称】的架构师
```

**架构师会自动**:
1. 扫描项目(10-20文件)
2. 生成4份文档
3. 拆解任务列表

---

### 场景2: 完整AI团队协作（标准流程）

**使用文档**: 
- `AI-TEAM-GUIDE.md` - 完整协作流程

**步骤**:
```markdown
@docs/ai/AI-TEAM-GUIDE.md

请按照AI团队协作指南，
为【项目名称】启动完整AI团队
```

**包含**:
- 架构师分析拆解
- 全栈工程师实现
- 代码管家质量保证
- SRE部署运维

---

### 场景3: 派发单个任务（日常使用）

**使用文档**: 
- `task-prompt-template.md` - 任务模板

**步骤**:
1. 复制task-prompt-template.md
2. 填写任务信息
3. @fullstack-engineer-system-prompt.md发送

**示例**:
```markdown
@docs/ai/fullstack-engineer-system-prompt.md

李明，请实现TASK-C-1：创建FastAPI主入口
(使用task-prompt-template.md格式)
```

---

### 场景4: 架构师接手项目（标准检查）

**使用文档**: 
- `architect-onboarding-checklist.md` - 入职清单

**步骤**:
```markdown
@docs/ai/architect-system-prompt-expert.md
@docs/ai/architect-onboarding-checklist.md

请按照入职清单接手【项目名称】
```

**包含**:
- Step 0: 端口分配
- Step 1-4: 标准流程
- 必须产出清单

---

## 📖 在Dashboard中查看

### 1. 架构师相关文档

#### ARCHITECT MONITOR模块
**位置**: 页面最下方

**Tab: 动态提示词**
- 内容: 8000字完整架构师System Prompt
- 来源: architect-system-prompt-expert.md
- 功能: 可点击复制按钮

**Tab: 重要信息 → 架构师交接提示词**
- 内容: v1.7交接说明
- 来源: architect-notes/handoff.md

---

### 2. 全栈工程师相关文档

#### AI代码管家模块
**查看提示词**:
- 文件位置: automation-data/09-role-prompts/developer-prompt.md
- 大小: 30KB (7000字)

**查看知识库**:
- 问题解决库: v1.7问题+解决方案
- 工具库: PortManager/迁移工具
- 开发规范: Python/Git规范
- 最佳实践: v1.7架构实践

---

### 3. 协作指南文档

#### 查看方式
**文件系统**:
```bash
cd docs/ai
type AI-TEAM-GUIDE.md
type how-to-use-architect-with-cursor.md
```

**Dashboard**:
```
automation-data/09-role-prompts/
├── AI-TEAM-GUIDE.md              (14KB)
├── how-to-use-architect-with-cursor.md  (20KB)
└── architect-onboarding-checklist.md    (5KB)
```

---

## 🎯 快速查找指南

### 我想...

#### "让AI帮我分析项目"
📖 使用: `how-to-use-architect-with-cursor.md`  
📋 步骤: @architect-system-prompt-expert.md + "认命你为架构师"

#### "让AI团队协作开发"
📖 使用: `AI-TEAM-GUIDE.md`  
📋 步骤: 按照指南启动架构师→工程师→SRE流程

#### "给AI派一个具体任务"
📖 使用: `task-prompt-template.md`  
📋 步骤: 填写模板 + @fullstack-engineer-system-prompt.md

#### "架构师接手新项目"
📖 使用: `architect-onboarding-checklist.md`  
📋 步骤: 按照清单执行Step 0-4

#### "查看AI提示词内容"
📖 位置1: Dashboard → ARCHITECT MONITOR → 动态提示词  
📖 位置2: docs/ai/ 或 automation-data/09-role-prompts/

---

## 📊 AI文档对比表

| 文档 | 用途 | 何时使用 | 在Dashboard中 |
|------|------|---------|--------------|
| architect-system-prompt-expert.md | 架构师工作手册 | 任命架构师时 | ✅ 提示词Tab |
| fullstack-engineer-system-prompt.md | 全栈工程师工作手册 | 派发实现任务 | ✅ 09-role-prompts/ |
| code-steward-system-prompt.md | 代码管家工作手册 | 代码实现和质量保证 | ✅ 09-role-prompts/ |
| sre-system-prompt.md | SRE工作手册 | 部署运维时 | ✅ 09-role-prompts/ |
| AI-TEAM-GUIDE.md | 团队协作流程 | 完整团队协作 | ✅ 09-role-prompts/ |
| how-to-use-architect-with-cursor.md | Cursor使用说明 | 即插即用场景 | ✅ 09-role-prompts/ |
| architect-onboarding-checklist.md | 入职检查清单 | 架构师接手项目 | ✅ 09-role-prompts/ |
| task-prompt-template.md | 任务模板 | 派发任务时 | ✅ 15-templates/ |
| architect-system-prompt.md | 标准版(简化) | 不推荐 | ❌ 未加载 |

---

## 🚀 3个最常用场景

### 场景A: 快速分析项目（推荐）

**文档**: `how-to-use-architect-with-cursor.md`

**操作**:
```markdown
@taskflow-v1.7-monorepo/docs/ai/architect-system-prompt-expert.md

认命你为【项目名称】的架构师
```

**产出**: 
- 4份文档(10-15分钟)
- 架构审查报告
- 任务列表

---

### 场景B: 完整AI团队开发（标准流程）

**文档**: `AI-TEAM-GUIDE.md`

**操作**:
```markdown
第1步: @architect-system-prompt-expert.md
     认命你为架构师，分析并拆解任务

第2步: @fullstack-engineer-system-prompt.md
     李明，实现TASK-XXX

第3步: @architect-system-prompt-expert.md
     审查李明的代码

第4步: @sre-system-prompt.md
     部署和配置监控
```

**特点**: 完整PDCA闭环

---

### 场景C: 派发单个任务（日常）

**文档**: `task-prompt-template.md`

**操作**:
1. 复制task-prompt-template.md
2. 填写任务信息
3. 发送:
```markdown
@fullstack-engineer-system-prompt.md

【填好的任务提示词】
```

**特点**: 标准化、可复制

---

## 💡 核心特点对比

### 架构师Prompt特点

#### expert版 (推荐) ⭐
- **8000字**: 最详细
- **5大原则**: 理解优于执行/质疑优于盲从等
- **3方案对比**: 必须提供保守/平衡/激进方案
- **Token优化**: 抽样而非全量
- **适合**: 复杂项目、重要决策

#### 标准版
- **5000字**: 相对简单
- **适合**: 小项目、快速分析

---

### 工程师Prompt特点

#### 全栈工程师·李明
- **7000字**: 入职手册级
- **前置自查**: 先查文档/代码/记忆
- **完成报告**: 7部分标准化
- **技能树**: 后端⭐⭐⭐⭐⭐ 前端⭐⭐⭐⭐⭐
- **适合**: 完整功能开发(前后端都需要)

#### 代码管家
- **5000字**: 实现专家
- **最小改动**: 只改需要改的
- **测试≥80%**: 强制测试覆盖
- **适合**: 单一模块实现、稳定维护

---

## 📋 推荐阅读顺序

### 新手（第一次使用）

**5分钟快速了解**:
1. 📖 本文件 - AI文档完整索引 (了解全貌)
2. 📖 how-to-use-architect-with-cursor.md (前20行，了解如何启动)
3. 📖 AI-TEAM-GUIDE.md (前50行，了解协作流程)

**立即上手**:
4. 复制"认命架构师"提示词
5. @architect-system-prompt-expert.md
6. 粘贴并执行

---

### 进阶（深度使用）

**完整理解**:
1. 📖 architect-system-prompt-expert.md (全文8000字)
2. 📖 fullstack-engineer-system-prompt.md (全文7000字)
3. 📖 AI-TEAM-GUIDE.md (全文，理解完整流程)

**掌握技巧**:
4. 📖 how-to-use-architect-with-cursor.md (实战场景)
5. 📖 task-prompt-template.md (任务模板)
6. 📖 architect-onboarding-checklist.md (标准流程)

---

### 老手（高效使用）

**直接使用**:
- Dashboard查看提示词 → 复制
- task-prompt-template填空 → 派任务
- 新对话@对应Prompt → 执行

**工作流**:
```
架构师(10分钟分析) 
  → 工程师(实现) 
  → 架构师(审查) 
  → SRE(部署)
```

---

## 🔗 在Dashboard中的位置

### 查看AI提示词

#### 方式1: ARCHITECT MONITOR → 动态提示词
- 可查看: 架构师8000字Prompt
- 可操作: 点击复制按钮

#### 方式2: 文件系统
```bash
cd apps/dashboard/automation-data/09-role-prompts
dir *.md

# 8个文档，172KB
architect-prompt.md                    (47KB)
developer-prompt.md                    (30KB)
code-steward-prompt.md                 (24KB)
ops-prompt.md                          (26KB)
AI-TEAM-GUIDE.md                       (14KB)
how-to-use-architect-with-cursor.md    (20KB)
architect-onboarding-checklist.md      (5KB)
+ task-prompt-template.md in 15-templates/ (6KB)
```

---

## 🎊 完整AI文档体系

### 核心组成
```
AI文档体系 (200KB)
├── 角色Prompts (127KB)
│   ├── 架构师 (47KB) ⭐
│   ├── 全栈工程师 (30KB) ⭐
│   ├── 代码管家 (24KB) ⭐
│   └── SRE (26KB) ⭐
│
├── 协作指南 (39KB)
│   ├── AI团队协作指南 (14KB) ⭐
│   ├── Cursor使用指南 (20KB) ⭐
│   └── 架构师入职清单 (5KB)
│
└── 工具模板 (6KB)
    └── 任务提示词模板 (6KB) ⭐
```

**特点**:
- ✅ 入职手册级质量
- ✅ 完整工作流程
- ✅ 可复制可执行
- ✅ 职责清晰闭环

---

## 📍 立即开始

### 最简单的方式（3步）

**Step 1**: 打开Dashboard
```
http://localhost:8871
```

**Step 2**: 滚动到ARCHITECT MONITOR
```
点击"动态提示词"Tab
```

**Step 3**: 复制提示词，在Cursor中使用
```
点击"复制"按钮
在新对话中粘贴
添加: "认命你为【项目名称】的架构师"
```

---

## 🌟 推荐文档 Top 5

### 🥇 architect-system-prompt-expert.md (47KB)
**最重要！** 架构师的完整工作手册
- 5大能力维度
- 5大核心原则
- 三阶段工作流
- 专家级思维

### 🥈 AI-TEAM-GUIDE.md (14KB)
**最实用！** 完整的AI团队协作指南
- 4个场景示例
- 标准工作流
- 最佳实践

### 🥉 how-to-use-architect-with-cursor.md (20KB)
**最易上手！** Cursor即插即用指南
- 3步快速开始
- 5个实战场景
- Token优化技巧

### 4️⃣ fullstack-engineer-system-prompt.md (30KB)
**最详细！** 全栈工程师李明的入职手册
- 5步工作流程
- 7部分完成报告
- 前置自查机制

### 5️⃣ task-prompt-template.md (6KB)
**最常用！** 任务提示词模板
- 填空即用
- 标准格式
- 包含验收标准

---

## 📞 获取帮助

### 在Dashboard中
1. 打开 http://localhost:8871
2. ARCHITECT MONITOR → 动态提示词
3. 查看完整8000字内容

### 在项目中
```bash
cd docs/ai
type architect-system-prompt-expert.md
type AI-TEAM-GUIDE.md
type how-to-use-architect-with-cursor.md
```

### 在Cursor中
```markdown
@docs/ai/AI-TEAM-GUIDE.md

我想了解AI团队协作的完整流程
```

---

**索引版本**: v1.0  
**文档总数**: 9个  
**总大小**: 200KB  
**核心提示词**: 24500字  
**状态**: ✅ 全部已加载到Dashboard

---

🎉 **完整的AI文档体系！从入门到精通的全套资料！**

📖 **立即查看Dashboard → ARCHITECT MONITOR → 动态提示词！**

