#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库初始化器 - 架构师任命后自动创建标准化知识库结构
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class KnowledgeBaseInitializer:
    """知识库初始化器"""
    
    def __init__(self, base_path: str = "automation-data"):
        self.base_path = Path(base_path)
        self.created_files = []
        self.created_dirs = []
    
    def initialize_all(self, scan_result: Dict = None) -> Dict[str, Any]:
        """完整初始化"""
        print("\n" + "=" * 70)
        print("🚀 架构师初始化知识库体系")
        print("=" * 70)
        
        # 1. 创建文件夹结构
        self.create_structure()
        
        # 2. 生成模板文件
        self.generate_templates(scan_result)
        
        # 3. 填充初始数据
        if scan_result:
            self.populate_from_scan(scan_result)
        
        result = {
            "status": "success",
            "created_dirs": len(self.created_dirs),
            "created_files": len(self.created_files),
            "dirs": self.created_dirs,
            "files": self.created_files,
            "initialized_at": datetime.now().isoformat()
        }
        
        print(f"\n✅ 知识库初始化完成！")
        print(f"   创建目录: {len(self.created_dirs)}个")
        print(f"   创建文件: {len(self.created_files)}个")
        print("=" * 70 + "\n")
        
        return result
    
    def create_structure(self):
        """创建16个标准文件夹"""
        directories = [
            "01-background",
            "02-modules-db",
            "03-problem-solving",
            "04-ux-library/user-flows",
            "04-ux-library/wireframes",
            "05-ui-library/design-system",
            "05-ui-library/mockups",
            "06-code-library/snippets",
            "07-maintenance-logs/incident-reports",
            "08-standards",
            "09-role-prompts",
            "10-role-behaviors",
            "11-decisions",
            "12-meeting-notes",
            "13-milestones",
            "14-resources",
            "15-templates",
            "16-metrics"
        ]
        
        for dir_name in directories:
            dir_path = self.base_path / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                self.created_dirs.append(str(dir_path))
                print(f"[创建] 目录: {dir_name}")
    
    def generate_templates(self, scan_result: Dict = None):
        """生成模板文件"""
        project_name = scan_result.get("project_name", "未命名项目") if scan_result else "未命名项目"
        project_type = scan_result.get("project_type", "未知类型") if scan_result else "未知类型"
        
        templates = {
            # 01-background/
            "01-background/project-overview.md": self._template_project_overview(project_name, project_type, scan_result),
            "01-background/business-context.md": self._template_business_context(),
            "01-background/user-personas.md": self._template_user_personas(),
            "01-background/competitive-analysis.md": self._template_competitive_analysis(),
            "01-background/technical-stack.md": self._template_technical_stack(scan_result),
            
            # 02-modules-db/
            "02-modules-db/features.json": self._template_features_db(scan_result),
            "02-modules-db/apis.json": self._template_apis_db(),
            "02-modules-db/database-schema.json": self._template_database_schema(),
            "02-modules-db/components.json": self._template_components_db(),
            "02-modules-db/dependencies.json": self._template_dependencies_db(),
            
            # 03-problem-solving/
            "03-problem-solving/common-issues.md": self._template_common_issues(),
            "03-problem-solving/bug-patterns.md": self._template_bug_patterns(),
            "03-problem-solving/performance-tips.md": self._template_performance_tips(),
            "03-problem-solving/security-checklist.md": self._template_security_checklist(),
            "03-problem-solving/troubleshooting-guide.md": self._template_troubleshooting(),
            
            # 04-ux-library/
            "04-ux-library/ux-principles.md": self._template_ux_principles(),
            "04-ux-library/interaction-patterns.md": self._template_interaction_patterns(),
            "04-ux-library/user-flows/login-flow.md": self._template_user_flow("登录"),
            "04-ux-library/wireframes/README.md": self._template_wireframes_readme(),
            
            # 05-ui-library/
            "05-ui-library/ui-guidelines.md": self._template_ui_guidelines(),
            "05-ui-library/design-system/colors.md": self._template_colors(),
            "05-ui-library/design-system/typography.md": self._template_typography(),
            "05-ui-library/design-system/spacing.md": self._template_spacing(),
            "05-ui-library/design-system/components.md": self._template_ui_components(),
            "05-ui-library/mockups/README.md": self._template_mockups_readme(),
            
            # 06-code-library/
            "06-code-library/code-index.json": self._template_code_index(scan_result),
            "06-code-library/api-documentation.md": self._template_api_doc(scan_result),
            "06-code-library/module-structure.md": self._template_module_structure(scan_result),
            "06-code-library/class-diagram.md": self._template_class_diagram(),
            "06-code-library/data-flow.md": self._template_data_flow(),
            "06-code-library/snippets/common-patterns.md": self._template_code_snippets(),
            
            # 07-maintenance-logs/
            "07-maintenance-logs/changelog.md": self._template_changelog(),
            "07-maintenance-logs/deployment-history.md": self._template_deployment_history(),
            "07-maintenance-logs/incident-reports/template.md": self._template_incident_report(),
            "07-maintenance-logs/performance-logs.md": self._template_performance_logs(),
            "07-maintenance-logs/review-records.md": self._template_review_records(),
            
            # 08-standards/
            "08-standards/coding-standards.md": self._template_coding_standards(scan_result),
            "08-standards/git-workflow.md": self._template_git_workflow(),
            "08-standards/testing-standards.md": self._template_testing_standards(),
            "08-standards/documentation-standards.md": self._template_doc_standards(),
            "08-standards/review-checklist.md": self._template_review_checklist(),
            "08-standards/deployment-checklist.md": self._template_deployment_checklist(),
            
            # 09-role-prompts/
            "09-role-prompts/architect-prompt.md": self._template_architect_prompt(project_name),
            "09-role-prompts/ux-designer-prompt.md": self._template_ux_prompt(project_name),
            "09-role-prompts/ui-designer-prompt.md": self._template_ui_prompt(project_name),
            "09-role-prompts/developer-prompt.md": self._template_developer_prompt(project_name),
            "09-role-prompts/tester-prompt.md": self._template_tester_prompt(project_name),
            "09-role-prompts/ops-prompt.md": self._template_ops_prompt(project_name),
            "09-role-prompts/pm-prompt.md": self._template_pm_prompt(project_name),
            
            # 10-role-behaviors/
            "10-role-behaviors/architect-behavior.md": self._template_architect_behavior(),
            "10-role-behaviors/developer-behavior.md": self._template_developer_behavior(),
            "10-role-behaviors/tester-behavior.md": self._template_tester_behavior(),
            "10-role-behaviors/ops-behavior.md": self._template_ops_behavior(),
            "10-role-behaviors/collaboration-rules.md": self._template_collaboration_rules(),
            
            # 11-decisions/
            "11-decisions/template.md": self._template_adr(),
            "11-decisions/README.md": self._template_decisions_readme(),
            
            # 12-meeting-notes/
            "12-meeting-notes/template.md": self._template_meeting_notes(),
            "12-meeting-notes/README.md": self._template_meeting_readme(),
            
            # 13-milestones/
            "13-milestones/milestones.json": self._template_milestones(),
            "13-milestones/release-plan.md": self._template_release_plan(),
            
            # 14-resources/
            "14-resources/references.md": self._template_references(),
            "14-resources/tutorials.md": self._template_tutorials(),
            "14-resources/tools.md": self._template_tools(),
            
            # 15-templates/
            "15-templates/task-template.md": self._template_task(),
            "15-templates/bug-report-template.md": self._template_bug_report(),
            "15-templates/feature-request-template.md": self._template_feature_request(),
            
            # 16-metrics/
            "16-metrics/code-metrics.json": self._template_code_metrics(),
            "16-metrics/velocity-tracking.json": self._template_velocity(),
        }
        
        for file_path, content in templates.items():
            full_path = self.base_path / file_path
            if not full_path.exists():
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.created_files.append(str(file_path))
                print(f"[生成] 文件: {file_path}")
    
    def populate_from_scan(self, scan_result: Dict):
        """从扫描结果填充数据"""
        # 更新features.json
        features_file = self.base_path / "02-modules-db/features.json"
        if features_file.exists() and scan_result.get("features"):
            with open(features_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data["features"] = scan_result["features"].get("implemented", [])
            data["last_updated"] = datetime.now().isoformat()
            
            with open(features_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ===== 模板生成函数 =====
    
    def _template_project_overview(self, name, type, scan_result):
        files_count = scan_result.get("files_count", {}) if scan_result else {}
        techs = scan_result.get("technologies", []) if scan_result else []
        
        return f"""# 项目概述

## 项目名称
{name}

## 项目类型
{type}

## 技术栈
{', '.join(techs) if techs else '待补充'}

## 项目规模
- Python文件: {files_count.get('python', 0)}个
- JavaScript文件: {files_count.get('javascript', 0)}个
- TypeScript文件: {files_count.get('typescript', 0)}个
- 文档文件: {files_count.get('markdown', 0)}个
- 总文件数: {files_count.get('total', 0)}个

## 项目目标
[待架构师与用户确认后填充]

## 项目范围
- 功能范围：[待确认]
- 用户范围：[待确认]
- 技术范围：[待确认]

## 成功标准
1. [标准1 - 待定义]
2. [标准2 - 待定义]
3. [标准3 - 待定义]

---
**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**创建者**: 架构师AI  
**状态**: 初始化完成，待完善
"""
    
    def _template_business_context(self):
        return """# 业务背景

## 业务目标
[描述这个项目要解决什么业务问题]

## 商业模式
[描述盈利模式、成本结构]

## 目标用户
[主要用户群体]

## 市场定位
[在市场中的定位和差异化]

## 业务流程
[核心业务流程描述]

---
**创建时间**: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """  
**待完善**: 需要产品经理或业务方提供详细信息
"""
    
    def _template_user_personas(self):
        return """# 用户画像

## 主要用户类型

### 用户类型1: [名称]
- **基本信息**: 年龄、职业、技能水平
- **使用场景**: [何时何地使用]
- **痛点**: [现有问题]
- **期望**: [期望的解决方案]
- **使用频率**: 每日/每周

### 用户类型2: [名称]
- **基本信息**: 
- **使用场景**: 
- **痛点**: 
- **期望**: 
- **使用频率**: 

## 用户旅程地图
[描述用户从接触产品到完成目标的完整旅程]

---
**创建时间**: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """  
**待完善**: UX设计师负责补充
"""
    
    def _template_competitive_analysis(self):
        return """# 竞品分析

## 主要竞品

### 竞品1: [名称]
- **优势**: 
- **劣势**: 
- **目标用户**: 
- **技术栈**: 
- **我们的差异化**: 

### 竞品2: [名称]
- **优势**: 
- **劣势**: 
- **目标用户**: 
- **技术栈**: 
- **我们的差异化**: 

## 差异化策略
[我们的独特价值]

---
**创建时间**: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _template_technical_stack(self, scan_result):
        techs = scan_result.get("technologies", []) if scan_result else []
        return f"""# 技术栈说明

## 识别到的技术栈
{chr(10).join([f'- {t}' for t in techs]) if techs else '- 待识别'}

## 技术选型理由

### 后端技术
- **框架**: [FastAPI/Flask/Django等]
- **选型理由**: [性能/易用性/生态]

### 前端技术  
- **框架**: [React/Vue/Angular等]
- **选型理由**: [组件化/性能/生态]

### 数据库
- **类型**: [SQLite/MySQL/PostgreSQL等]
- **选型理由**: [规模/性能/易用性]

### 其他工具
- **CI/CD**: [工具选择]
- **监控**: [工具选择]
- **日志**: [工具选择]

---
**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**维护者**: 架构师
"""
    
    def _template_features_db(self, scan_result):
        features = scan_result.get("features", {}).get("implemented", []) if scan_result else []
        return json.dumps({
            "features": features,
            "last_updated": datetime.now().isoformat(),
            "total_count": len(features)
        }, ensure_ascii=False, indent=2)
    
    def _template_apis_db(self):
        return json.dumps({
            "apis": [],
            "last_updated": datetime.now().isoformat(),
            "note": "架构师扫描后自动填充"
        }, ensure_ascii=False, indent=2)
    
    def _template_database_schema(self):
        return json.dumps({
            "tables": [],
            "relationships": [],
            "indexes": [],
            "note": "待数据库设计完成后填充"
        }, ensure_ascii=False, indent=2)
    
    def _template_components_db(self):
        return json.dumps({
            "components": [],
            "note": "前端组件清单"
        }, ensure_ascii=False, indent=2)
    
    def _template_dependencies_db(self):
        return json.dumps({
            "dependencies": [],
            "note": "模块依赖关系"
        }, ensure_ascii=False, indent=2)
    
    def _template_common_issues(self):
        return """# 常见问题FAQ

## 环境问题

### Q: 如何配置开发环境？
A: [步骤说明]

### Q: 依赖安装失败怎么办？
A: [解决方案]

## 功能问题

### Q: [常见功能问题]
A: [解决方案]

## 性能问题

### Q: [性能相关问题]
A: [优化建议]

---
**维护者**: 运维工程师  
**更新频率**: 遇到新问题时更新
"""
    
    def _template_bug_patterns(self):
        return """# Bug模式库

## 典型Bug模式

### 模式1: [Bug类型]
- **表现**: [如何表现]
- **原因**: [根本原因]
- **解决**: [解决方法]
- **预防**: [如何预防]

### 模式2: [Bug类型]
- **表现**: 
- **原因**: 
- **解决**: 
- **预防**: 

---
**维护者**: 测试工程师 + 开发工程师  
**用途**: Bug预防和快速定位
"""
    
    def _template_performance_tips(self):
        return """# 性能优化建议

## 前端性能

### 1. 加载优化
- 代码分割
- 懒加载
- 图片优化

### 2. 渲染优化
- 虚拟滚动
- 防抖节流
- Memo优化

## 后端性能

### 1. 数据库优化
- 索引优化
- 查询优化
- 连接池

### 2. API优化
- 缓存策略
- 异步处理
- 批量操作

---
**维护者**: 架构师 + 开发工程师
"""
    
    def _template_security_checklist(self):
        return """# 安全检查清单

## 认证授权
- [ ] 密码加密存储
- [ ] Token安全传输
- [ ] 权限验证完整
- [ ] Session管理安全

## 数据安全
- [ ] SQL注入防护
- [ ] XSS防护
- [ ] CSRF防护
- [ ] 敏感数据加密

## API安全
- [ ] 速率限制
- [ ] 参数验证
- [ ] 错误信息脱敏
- [ ] HTTPS强制

---
**审查者**: 架构师 + 安全专家
"""
    
    def _template_troubleshooting(self):
        return """# 故障排查指南

## 服务无法启动

### 检查步骤
1. 检查端口占用
2. 检查配置文件
3. 检查依赖版本
4. 查看错误日志

## 功能异常

### 检查步骤
1. 复现问题
2. 查看日志
3. 检查数据
4. 调试代码

## 性能问题

### 检查步骤
1. 监控指标
2. 性能分析
3. 定位瓶颈
4. 优化方案

---
**维护者**: 运维工程师
"""
    
    def _template_ux_principles(self):
        return """# UX设计原则

## 核心原则

### 1. 易用性
- 操作简单直观
- 学习成本低
- 容错性好

### 2. 一致性
- 交互一致
- 视觉一致
- 术语一致

### 3. 反馈及时
- 操作有反馈
- 状态可见
- 错误友好

### 4. 效率优先
- 减少步骤
- 快捷操作
- 批量处理

---
**维护者**: UX设计师
"""
    
    def _template_interaction_patterns(self):
        return """# 交互模式库

## 表单交互
- 实时验证
- 错误提示
- 保存草稿

## 列表交互
- 搜索过滤
- 排序
- 分页

## 弹窗交互
- 模态框
- 抽屉
- Toast提示

---
**维护者**: UX设计师
"""
    
    def _template_user_flow(self, flow_name):
        return f"""# {flow_name}流程

## 流程图

```mermaid
graph TD
    A[开始] --> B[步骤1]
    B --> C[步骤2]
    C --> D[结束]
```

## 步骤说明

### 步骤1: [名称]
- **操作**: [用户操作]
- **系统反应**: [系统响应]
- **异常处理**: [错误情况]

### 步骤2: [名称]
- **操作**: 
- **系统反应**: 
- **异常处理**: 

---
**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    def _template_wireframes_readme(self):
        return """# 线框图库

## 说明
此目录存放UX线框图（图片）

## 命名规范
- `页面名-v版本号.png`
- 示例: `login-page-v1.png`

## 图片来源
- 手绘扫描
- 设计工具导出
- AI生成

---
**维护者**: UX设计师
"""
    
    def _template_ui_guidelines(self):
        return """# UI设计指南

## 设计风格
[现代简约/工业美学/扁平化等]

## 配色方案
参考: `design-system/colors.md`

## 字体系统
参考: `design-system/typography.md`

## 组件规范
参考: `design-system/components.md`

---
**维护者**: UI设计师
"""
    
    def _template_colors(self):
        return """# 配色方案

## 主色调
- **主色**: #985239（敦煌赭红）
- **辅色**: #537696（敦煌青蓝）
- **强调色**: #7BA882（敦煌绿）

## 功能色
- **成功**: #7BA882
- **警告**: #E6C866
- **错误**: #985239
- **信息**: #537696

## 中性色
- **黑色**: #000000
- **白色**: #FFFFFF
- **灰色**: #E0E0E0

---
**维护者**: UI设计师
"""
    
    def _template_typography(self):
        return """# 字体系统

## 字体家族
- **中文**: -apple-system, 'Microsoft YaHei'
- **英文**: 'Helvetica Neue', Arial
- **等宽**: 'Consolas', 'Monaco', monospace

## 字号体系
- **标题1**: 24px
- **标题2**: 20px
- **标题3**: 16px
- **正文**: 14px
- **辅助**: 12px
- **小字**: 11px

## 字重
- **粗体**: 700
- **中等**: 600
- **常规**: 400

---
**维护者**: UI设计师
"""
    
    def _template_spacing(self):
        return """# 间距系统

## 间距规范
- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **xxl**: 48px

## 使用场景
- 组件内间距: sm (8px)
- 组件间间距: md (16px)
- 模块间间距: lg (24px)
- 区块间间距: xxl (48px)

---
**维护者**: UI设计师
"""
    
    def _template_ui_components(self):
        return """# 组件规范

## 按钮组件
- **主按钮**: 黑色背景，白色文字
- **次按钮**: 白色背景，黑色边框
- **文字按钮**: 无背景，有下划线

## 输入框组件
- **默认**: 灰色边框
- **聚焦**: 青蓝色边框
- **错误**: 赭红色边框

## 卡片组件
- **白色背景**: #FFFFFF
- **灰色边框**: #E0E0E0
- **顶部黑色**: 2px solid

---
**维护者**: UI设计师
"""
    
    def _template_mockups_readme(self):
        return """# 效果图库

## 说明
此目录存放UI效果图（图片）

## 命名规范
- `页面名-v版本号.png`
- 示例: `dashboard-v1.png`

## 存储方式
- 使用图床（Imgur/SM.MS）
- 记录URL到设计确认模块

---
**维护者**: UI设计师
"""
    
    def _template_code_index(self, scan_result):
        features = scan_result.get("features", {}).get("implemented", []) if scan_result else []
        return json.dumps({
            "modules": [f["file"] for f in features if f.get("file")],
            "classes": [f["name"] for f in features if f.get("type") == "核心模块"],
            "functions": [],
            "last_scanned": datetime.now().isoformat()
        }, ensure_ascii=False, indent=2)
    
    def _template_api_doc(self, scan_result):
        return """# API文档

## 基础信息
- **Base URL**: http://127.0.0.1:8852
- **认证方式**: [Token/Session/等]
- **返回格式**: JSON

## API列表

### 1. [API名称]
```
GET /api/example
```

**请求参数**:
- `param1`: 参数说明

**返回示例**:
```json
{
  "success": true,
  "data": {}
}
```

---
**维护者**: 开发工程师  
**更新频率**: 每次API变更后更新
"""
    
    def _template_module_structure(self, scan_result):
        return f"""# 模块结构

## 项目结构

```
{scan_result.get('project_name', 'project') if scan_result else 'project'}/
├── [待扫描]
```

## 核心模块

### 模块1: [名称]
- **职责**: [功能职责]
- **依赖**: [依赖的其他模块]
- **被依赖**: [哪些模块依赖它]

---
**维护者**: 架构师  
**更新**: 架构变更时更新
"""
    
    def _template_class_diagram(self):
        return """# 类图

## 核心类关系

```mermaid
classDiagram
    class ClassA {
        +method1()
        +method2()
    }
    class ClassB {
        +method3()
    }
    ClassA --> ClassB
```

---
**维护者**: 架构师
"""
    
    def _template_data_flow(self):
        return """# 数据流图

## 主要数据流

```mermaid
graph LR
    A[用户输入] --> B[验证]
    B --> C[处理]
    C --> D[存储]
    D --> E[返回]
```

---
**维护者**: 架构师
"""
    
    def _template_code_snippets(self):
        return """# 常用代码片段

## 错误处理

```python
try:
    # 业务逻辑
    pass
except Exception as e:
    logger.error(f"Error: {e}")
    return {"error": str(e)}
```

## API路由

```python
@app.get("/api/example")
async def example():
    return {"success": True}
```

---
**维护者**: 开发工程师
"""
    
    def _template_changelog(self):
        return f"""# 变更日志

## [Unreleased]

### Added
- 知识库初始化系统

### Changed
- 

### Fixed
- 

## [1.0.0] - {datetime.now().strftime("%Y-%m-%d")}

### Added
- 项目初始化

---
**格式**: 遵循 [Keep a Changelog](https://keepachangelog.com/)
"""
    
    def _template_deployment_history(self):
        return f"""# 部署历史

## 部署记录

### {datetime.now().strftime("%Y-%m-%d")} - v1.0.0
- **环境**: 开发环境
- **部署者**: 架构师
- **变更**: 初始部署
- **状态**: 成功

---
**维护者**: 交付工程师
"""
    
    def _template_incident_report(self):
        return """# 故障报告模板

## 基本信息
- **故障ID**: INC-YYYYMMDD-001
- **发生时间**: YYYY-MM-DD HH:MM:SS
- **发现者**: [姓名]
- **严重程度**: P0/P1/P2/P3

## 故障描述
[详细描述故障现象]

## 影响范围
- **影响用户**: [用户数/百分比]
- **影响功能**: [功能列表]
- **业务影响**: [业务影响]

## 根因分析
[深入分析故障原因]

## 解决方案
[采取的解决措施]

## 预防措施
[如何避免再次发生]

---
**提交者**: 运维工程师  
**审核者**: 架构师
"""
    
    def _template_performance_logs(self):
        return f"""# 性能日志

## 性能基线

| 指标 | 基线值 | 当前值 | 状态 |
|------|--------|--------|------|
| API响应时间 | <100ms | - | 待测 |
| 页面加载时间 | <2s | - | 待测 |
| 数据库查询 | <50ms | - | 待测 |

---
**记录时间**: {datetime.now().strftime("%Y-%m-%d")}  
**维护者**: 运维工程师
"""
    
    def _template_review_records(self):
        return """# 代码审查记录

## 审查记录

### YYYY-MM-DD - [任务ID]
- **审查者**: 架构师AI
- **提交者**: 开发工程师
- **评分**: 85/100
- **主要问题**: [列出问题]
- **改进建议**: [具体建议]
- **状态**: 通过/需修改

---
**维护者**: 架构师
"""
    
    def _template_coding_standards(self, scan_result):
        project_type = scan_result.get("project_type", "") if scan_result else ""
        return f"""# 代码规范

## 项目类型
{project_type}

## 语言规范
- **Python**: PEP 8
- **JavaScript**: Airbnb Style Guide
- **TypeScript**: TSLint规则

## 命名规范
- 文件名: snake_case
- 类名: PascalCase
- 函数名: snake_case
- 变量名: snake_case
- 常量: UPPER_SNAKE_CASE

## 注释规范
- 函数/类必须有文档字符串
- 复杂逻辑添加行内注释
- 使用中文或英文（统一）

## 代码组织
- 每个文件不超过500行
- 每个函数不超过50行
- 职责单一原则

---
**维护者**: 架构师  
**强制执行**: Linter + 代码审查
"""
    
    def _template_git_workflow(self):
        return """# Git工作流

## 分支策略
- **main**: 生产环境
- **develop**: 开发环境
- **feature/**: 功能分支
- **hotfix/**: 紧急修复

## Commit规范
```
[类型] 简短描述

详细说明（可选）
```

**类型**:
- feat: 新功能
- fix: Bug修复
- refactor: 重构
- test: 测试
- docs: 文档
- style: 格式
- chore: 构建/工具

---
**示例**: 
```
[feat] 添加用户登录功能

实现了邮箱+密码登录方式
```
"""
    
    def _template_testing_standards(self):
        return """# 测试规范

## 测试覆盖率要求
- **核心模块**: ≥80%
- **一般模块**: ≥70%
- **工具函数**: ≥90%

## 测试类型
1. **单元测试**: 每个函数/类
2. **集成测试**: 模块间交互
3. **端到端测试**: 完整业务流程

## 测试命名
```python
def test_功能_场景_预期结果():
    pass
```

---
**维护者**: 测试工程师
"""
    
    def _template_doc_standards(self):
        return """# 文档规范

## 文档类型
1. **API文档**: 所有接口必须有文档
2. **模块文档**: 每个模块说明职责
3. **用户文档**: 使用手册
4. **开发文档**: 开发指南

## 文档格式
- 使用Markdown
- 清晰的标题层级
- 代码示例

## 文档维护
- 代码变更同步更新文档
- 定期审查文档准确性

---
**维护者**: 全体成员
"""
    
    def _template_review_checklist(self):
        return """# 代码审查检查清单

## 功能正确性
- [ ] 实现符合需求
- [ ] 边界情况处理
- [ ] 错误处理完善

## 代码质量
- [ ] 遵循编码规范
- [ ] 命名清晰合理
- [ ] 注释充分
- [ ] 无重复代码

## 测试
- [ ] 有单元测试
- [ ] 测试覆盖充分
- [ ] 测试通过

## 文档
- [ ] API文档更新
- [ ] 注释完整
- [ ] README更新

---
**使用者**: 架构师
"""
    
    def _template_deployment_checklist(self):
        return """# 部署检查清单

## 部署前
- [ ] 代码审查通过
- [ ] 测试全部通过
- [ ] 配置文件正确
- [ ] 依赖版本确认
- [ ] 数据库迁移脚本
- [ ] 回滚方案准备

## 部署中
- [ ] 停止旧服务
- [ ] 备份数据
- [ ] 更新代码
- [ ] 安装依赖
- [ ] 数据库迁移
- [ ] 启动新服务

## 部署后
- [ ] 健康检查
- [ ] 功能验证
- [ ] 性能监控
- [ ] 日志检查

---
**使用者**: 交付工程师
"""
    
    def _template_architect_prompt(self, project_name):
        return f"""# 架构师提示词

你是【{project_name}】项目的总架构师，负责技术决策、任务拆解、代码审查。

## 核心职责

### 1. 需求分析
- 理解用户需求
- 识别功能依赖
- 发现潜在冲突
- 提出技术方案

### 2. 任务拆解
- 将功能拆解为任务
- 分析依赖关系
- 估算工时
- 分配优先级

### 3. 代码审查
- 审查代码质量
- 检查是否符合规范
- 提供改进建议
- 决定是否通过

### 4. 技术决策
- 技术选型
- 架构设计
- 性能优化
- 安全加固

## 工作流程

1. **接收需求** → 分析和澄清
2. **生成方案** → 与用户确认
3. **UX/UI设计** → 如需要则委托设计师
4. **拆解任务** → 生成开发任务
5. **监督开发** → 跟踪进度
6. **审查代码** → 5维度评分
7. **批准上线** → 确认可部署

## 输出规范

### 任务提示词
必须包含：任务信息、依赖关系、技术要求、验收标准、开发规范

### 审查报告
必须包含：评分、优点、问题、建议、结论

### 技术决策
必须记录到：`11-decisions/`目录

---
**项目**: {project_name}  
**角色**: 架构师  
**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    def _template_ux_prompt(self, project_name):
        return f"""# UX设计师提示词

你是【{project_name}】项目的UX设计师，负责用户体验设计。

## 核心职责
1. 用户研究和画像
2. 用户流程设计
3. 交互原型设计
4. 可用性测试

## 交付物
1. 用户流程图（Markdown + Mermaid）
2. 线框图（图片）
3. 交互说明文档
4. 可用性测试报告

## 设计原则
参考：`04-ux-library/ux-principles.md`

---
**项目**: {project_name}  
**角色**: UX设计师
"""
    
    def _template_ui_prompt(self, project_name):
        return f"""# UI设计师提示词

你是【{project_name}】项目的UI设计师，负责视觉设计。

## 核心职责
1. 建立设计系统（配色、字体、间距）
2. 设计界面效果图
3. 制作设计规范文档
4. 指导前端实现

## 交付物
1. 设计系统文档
2. 效果图（图片）
3. 组件规范
4. 前端实现指南

## 设计系统
参考：`05-ui-library/design-system/`

---
**项目**: {project_name}  
**角色**: UI设计师
"""
    
    def _template_developer_prompt(self, project_name):
        return f"""# 开发工程师提示词

你是【{project_name}】项目的全栈开发工程师。

## 核心职责
1. 实现功能代码
2. 编写单元测试
3. 编写技术文档
4. 提交代码审查

## 开发规范
参考：`08-standards/coding-standards.md`

## 工作流程
1. 领取任务（复制提示词）
2. 理解需求
3. 编写代码
4. 自测验证
5. 提交审查（复制报告）

---
**项目**: {project_name}  
**角色**: 全栈开发工程师
"""
    
    def _template_tester_prompt(self, project_name):
        return f"""# 测试工程师提示词

你是【{project_name}】项目的测试工程师。

## 核心职责
1. 功能测试
2. 集成测试
3. 性能测试
4. Bug跟踪

## 测试规范
参考：`08-standards/testing-standards.md`

---
**项目**: {project_name}  
**角色**: 测试工程师
"""
    
    def _template_ops_prompt(self, project_name):
        return f"""# 运维工程师提示词

你是【{project_name}】项目的运维工程师。

## 核心职责
1. 系统监控
2. 故障处理
3. 性能优化
4. 经验沉淀

---
**项目**: {project_name}  
**角色**: 运维工程师
"""
    
    def _template_pm_prompt(self, project_name):
        return f"""# 项目经理提示词

你是【{project_name}】项目的项目经理。

## 核心职责
1. 进度管理
2. 风险控制
3. 资源协调
4. 干系人沟通

---
**项目**: {project_name}  
**角色**: 项目经理
"""
    
    def _template_architect_behavior(self):
        return """# 架构师行为规范

## 标准工作流

### 1. 接收需求
- 仔细理解需求
- 识别模糊点
- 及时澄清

### 2. 分析方案
- 检查现有功能
- 识别依赖冲突
- 评估技术可行性
- 估算工作量

### 3. 生成任务
- 拆解为子任务
- 分析依赖关系
- 设置优先级
- 分配负责人

### 4. 监督实施
- 跟踪进度
- 解答疑问
- 审查代码
- 批准上线

---
**遵守者**: 所有担任架构师角色的AI
"""
    
    def _template_developer_behavior(self):
        return """# 开发工程师行为规范

## 标准开发流程

1. **领取任务** - 从Dashboard复制提示词
2. **理解需求** - 仔细阅读提示词
3. **设计方案** - 思考实现思路
4. **编写代码** - 遵循代码规范
5. **自测验证** - 运行测试确保正常
6. **提交审查** - 复制报告提交

## 质量要求
- 代码通过Linter
- 测试覆盖率≥70%
- 有适当注释
- API有文档

---
**遵守者**: 所有开发工程师
"""
    
    def _template_tester_behavior(self):
        return """# 测试工程师行为规范

## 标准测试流程

1. **理解需求** - 了解功能需求
2. **设计用例** - 覆盖正常和异常
3. **执行测试** - 手动+自动化
4. **记录问题** - Bug报告规范
5. **回归测试** - 确保无遗漏

## 测试原则
- 全覆盖
- 可重复
- 独立性
- 快速执行

---
**遵守者**: 所有测试工程师
"""
    
    def _template_ops_behavior(self):
        return """# 运维工程师行为规范

## 标准运维流程

1. **日常监控** - 检查系统健康
2. **故障响应** - 快速定位和修复
3. **性能优化** - 持续改进
4. **经验沉淀** - 记录到知识库

## 应急响应
- P0故障: 15分钟响应
- P1故障: 1小时响应
- P2故障: 1天内处理

---
**遵守者**: 所有运维工程师
"""
    
    def _template_collaboration_rules(self):
        return """# 协作规则

## 跨角色协作

### 架构师 ↔ 开发工程师
- 架构师提供清晰的任务提示词
- 开发工程师有问题及时沟通
- 提交前自测充分

### 架构师 ↔ UX/UI设计师
- 架构师说明功能需求
- 设计师提供设计稿
- 用户确认后进入开发

### 开发工程师 ↔ 测试工程师
- 开发完成后通知测试
- 测试发现问题及时反馈
- 修复后重新测试

---
**遵守者**: 所有角色
"""
    
    def _template_adr(self):
        return f"""# ADR-XXX: [决策标题]

**日期**: {datetime.now().strftime("%Y-%m-%d")}  
**状态**: 提议中/已接受/已弃用  
**决策者**: 架构师

## 背景
[为什么需要做这个决策]

## 决策
[我们决定做什么]

## 理由
[为什么这样决策]

## 后果
[这个决策的影响]

## 备选方案
[考虑过的其他方案]

---
**格式**: ADR (Architecture Decision Records)
"""
    
    def _template_decisions_readme(self):
        return """# 架构决策记录

## 说明
此目录记录所有重大技术决策，使用ADR格式。

## 命名规范
- `adr-001-标题.md`
- 按时间顺序编号

## 索引

| 编号 | 标题 | 日期 | 状态 |
|------|------|------|------|
| 001 | [决策标题] | YYYY-MM-DD | 已接受 |

---
**维护者**: 架构师
"""
    
    def _template_meeting_notes(self):
        return f"""# 会议记录

**会议时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**会议类型**: 需求讨论/技术评审/进度同步  
**参与者**: [姓名列表]

## 会议议题
1. [议题1]
2. [议题2]

## 讨论内容

### 议题1: [标题]
- **讨论**: [讨论内容]
- **决策**: [达成的决策]
- **待办**: [后续行动]

## 行动项

| 行动项 | 负责人 | 截止日期 | 状态 |
|--------|--------|----------|------|
| [行动] | [姓名] | YYYY-MM-DD | 待办 |

---
**记录者**: [姓名]
"""
    
    def _template_meeting_readme(self):
        return """# 会议记录库

## 说明
此目录记录所有项目会议。

## 命名规范
- `YYYY-MM-DD-会议主题.md`
- 示例: `2025-11-18-kickoff-meeting.md`

---
**维护者**: 项目经理/架构师
"""
    
    def _template_milestones(self):
        return json.dumps({
            "milestones": [
                {
                    "id": "m1",
                    "name": "项目初始化",
                    "description": "知识库建立，架构师就位",
                    "target_date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "completed"
                }
            ]
        }, ensure_ascii=False, indent=2)
    
    def _template_release_plan(self):
        return f"""# 发布计划

## 版本规划

### v1.0.0 - MVP版本
- **目标日期**: [YYYY-MM-DD]
- **核心功能**: [功能列表]
- **目标**: 基础功能可用

### v1.1.0 - 增强版本
- **目标日期**: [YYYY-MM-DD]
- **新增功能**: [功能列表]
- **目标**: 用户体验提升

### v2.0.0 - 重大更新
- **目标日期**: [YYYY-MM-DD]
- **重大变更**: [变更列表]
- **目标**: 功能完善

---
**创建时间**: {datetime.now().strftime("%Y-%m-%d")}  
**维护者**: 架构师 + 项目经理
"""
    
    def _template_references(self):
        return """# 参考资料

## 官方文档
- [技术栈官方文档链接]

## 教程文章
- [相关教程链接]

## 最佳实践
- [业界最佳实践]

---
**维护者**: 全体成员
"""
    
    def _template_tutorials(self):
        return """# 教程收藏

## 入门教程
- [新成员快速上手]

## 进阶教程
- [深入学习资料]

## 视频教程
- [视频资源链接]

---
**维护者**: 全体成员
"""
    
    def _template_tools(self):
        return """# 推荐工具

## 开发工具
- **IDE**: VS Code / PyCharm
- **Git**: GitHub Desktop / SourceTree
- **API测试**: Postman / Insomnia

## 设计工具
- **UX**: Figma / Sketch
- **UI**: Figma / Adobe XD
- **原型**: Axure / Balsamiq

## 运维工具
- **监控**: Grafana / Prometheus
- **日志**: ELK Stack
- **部署**: Docker / K8s

---
**维护者**: 架构师
"""
    
    def _template_task(self):
        return """# 任务模板

## 任务信息
- **任务ID**: [auto-generated]
- **任务标题**: [简短标题]
- **优先级**: P0/P1/P2/P3
- **预估工时**: [小时]

## 需求描述
[详细描述要实现的功能]

## 验收标准
1. [标准1]
2. [标准2]

## 技术要求
[技术栈、框架、规范]

---
**创建者**: 架构师
"""
    
    def _template_bug_report(self):
        return """# Bug报告模板

## Bug信息
- **Bug ID**: [auto-generated]
- **严重程度**: P0/P1/P2/P3
- **发现者**: [姓名]
- **发现时间**: [时间]

## Bug描述
[详细描述Bug现象]

## 复现步骤
1. [步骤1]
2. [步骤2]
3. [观察到的错误]

## 预期行为
[应该是什么样的]

## 实际行为
[实际是什么样的]

## 环境信息
- 操作系统: 
- 浏览器: 
- 版本: 

---
**提交者**: [姓名]
"""
    
    def _template_feature_request(self):
        return """# 功能需求模板

## 需求信息
- **需求ID**: [auto-generated]
- **优先级**: P0/P1/P2/P3
- **提出者**: [姓名]

## 需求描述
[详细描述需要的功能]

## 使用场景
[什么场景下使用]

## 期望效果
[用户期望达到什么效果]

## 备注
[其他说明]

---
**提交时间**: [时间]
"""
    
    def _template_code_metrics(self):
        return json.dumps({
            "code_metrics": {
                "lines_of_code": 0,
                "functions_count": 0,
                "classes_count": 0,
                "test_coverage": 0,
                "last_measured": datetime.now().isoformat()
            }
        }, ensure_ascii=False, indent=2)
    
    def _template_velocity(self):
        return json.dumps({
            "velocity": {
                "tasks_completed_per_week": 0,
                "average_task_hours": 0,
                "records": []
            }
        }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    initializer = KnowledgeBaseInitializer()
    result = initializer.initialize_all()
    print(f"\n✅ 完成！创建了{result['created_dirs']}个目录，{result['created_files']}个文件")

