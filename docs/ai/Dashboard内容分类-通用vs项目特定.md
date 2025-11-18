# 📊 Dashboard内容分类：通用 vs 项目特定

**版本**: v1.0  
**目的**: 区分哪些内容所有项目通用，哪些必须每个项目更新

---

## 🔒 通用内容（一次配置，所有项目共享）

### AI System Prompts（09-role-prompts/）
**文件**:
- architect-prompt.md (8000字)
- developer-prompt.md (7000字)
- code-steward-prompt.md (5000字)
- ops-prompt.md (4500字)
- AI-TEAM-GUIDE.md
- how-to-use-architect-with-cursor.md
- architect-onboarding-checklist.md
- task-prompt-template.md

**更新频率**: 永久不变（除非Prompt本身升级）  
**Dashboard位置**: 
- ARCHITECT MONITOR → 动态提示词
- 全栈开发工程师 → 提示词

---

### 标准规范（08-standards/）
**文件**:
- coding-standards.md
- git-workflow.md
- testing-standards.md
- documentation-standards.md
- review-checklist.md
- deployment-checklist.md

**更新频率**: 永久不变  
**Dashboard位置**: （不直接展示，内部参考）

---

### 模板文件（15-templates/）
**文件**:
- task-template.md
- bug-report-template.md
- feature-request-template.md
- task-prompt-template.md

**更新频率**: 永久不变  
**Dashboard位置**: （不直接展示，工具使用）

---

### UX/UI库（04-ux-library/, 05-ui-library/）
**更新频率**: 永久不变  
**Dashboard位置**: UX/UI确认模块（可选）

---

## 🔄 项目特定内容（每个项目必须更新）

### 1. 功能清单 JSON ⭐ 最重要
**文件**: `{项目代码}-features.json`

**包含**:
```json
{
  "implemented": [108个细粒度功能],
  "partial": [12个半成品],
  "conflicts": [9个问题]
}
```

**Dashboard显示**: 
- 功能清单 → 已实现功能 (108个)
- 功能清单 → 部分实现功能 (12个)
- 功能清单 → 冲突/建议取舍 (9个)

**必须**: 每个项目都不同，必须生成

---

### 2. 待完成任务 ⭐ 最重要
**文件**: `database/data/tasks.db` (tasks表)

**Dashboard显示**: 待完成的功能清单模块

**必须**: 任务拆解后录入数据库

---

### 3. 架构师事件流 ⭐ 最重要
**文件**: `architect_events.json`

**Dashboard显示**: ARCHITECT MONITOR → 事件流Tab

**必须**: 记录架构师所有工作（每次沟通/每个操作）

---

### 4. 架构师监控数据 ⭐ 最重要
**文件**: `architect_monitor.json`

**包含**:
```json
{
  "token_usage": {实际Token使用},
  "project_info": {项目名/代码/完成度/功能数},
  "status": {当前状态/任务数}
}
```

**Dashboard显示**: ARCHITECT MONITOR顶部

**必须**: 实时更新Token，填写项目信息

---

### 5. 架构师对话记录
**文件**: `architect-conversations.json`

**Dashboard显示**: ARCHITECT MONITOR → 对话交流Tab

**建议**: 记录关键对话

---

### 6. 架构师重要信息
**文件**: `architect-notes/` (4个文档)
- requirements.md: 项目重大需求变更
- handoff.md: 架构师交接说明
- bugs.md: Bug进度清单
- decisions.md: 技术决策记录(ADR)

**Dashboard显示**: ARCHITECT MONITOR → 重要信息Tab

**建议**: 根据项目实际情况填写

---

### 7. 项目背景
**文件**: `01-background/`
- project-overview.md: 项目概览
- technical-stack.md: 技术栈
- business-context.md: 业务背景
- user-personas.md: 用户画像

**Dashboard显示**: （内部数据，不直接展示）

**建议**: 填写项目基本信息

---

### 8. 开发者知识库（项目问题）⭐ 重要
**文件**: `developer-knowledge/problems.md`

**内容**: 项目特定的常见问题和解决方案

**Dashboard显示**: AI代码管家 → 问题解决库

**必须**: 遇到问题就记录

---

### 9. 测试知识库（项目测试）
**文件**: `tester-knowledge/`
- cases.md: 项目测试用例
- bugs.md: 项目Bug跟踪

**Dashboard显示**: 测试工程师 → 知识库

**建议**: 有测试时记录

---

### 10. 运维知识库（项目故障）⭐ 重要
**文件**: `ops/`
- incidents.md: 项目故障记录
- troubleshooting.md: 项目问题排查
- lessons.md: 项目经验教训
- metrics.md: 项目性能基线

**Dashboard显示**: 运维SRE → 知识库

**必须**: 有运维操作就记录（如端口切换/服务重启/故障修复）

---

### 11. 交付文档（项目环境）
**文件**: `delivery-docs/`
- environment.md: 项目环境说明
- tools.md: 项目工具链

**Dashboard显示**: 交付工程师模块

**建议**: 填写项目部署信息

---

## 📊 更新优先级

### P0（必须立即更新）
1. 功能清单JSON（细粒度）
2. 待完成任务（数据库）
3. 事件流（完整记录）
4. Token数据（实际值）

### P1（建议更新）
5. 架构师重要信息
6. 项目背景
7. 开发问题库
8. 运维故障记录

### P2（可选更新）
9. 测试用例
10. 交付文档
11. 其他知识库

---

## 🎯 快速判断

**这个内容需要更新吗？**

问自己：
- 这个内容在不同项目中一样吗？
  - 一样 → 通用内容，不更新
  - 不一样 → 项目特定，必须更新

**示例**:
- "架构师System Prompt" → 所有项目一样 → 不更新
- "已实现功能清单" → 每个项目不同 → 必须更新
- "编码规范" → 所有项目一样 → 不更新
- "项目故障记录" → 每个项目不同 → 必须更新

---

**文档版本**: v1.0  
**更新时间**: 2025-11-19  
**状态**: ✅ 标准流程已建立

📋 **区分清楚，更新高效！**

