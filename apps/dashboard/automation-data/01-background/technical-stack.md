# 技术栈

## 后端

### Python 3.11+
- **FastAPI 0.104+**: Web框架
- **Uvicorn 0.24+**: ASGI服务器
- **Pydantic 2.5+**: 数据验证
- **SQLite 3.x**: 数据库

### 核心模块
- **StateManager**: 数据持久化
- **DependencyAnalyzer**: 依赖分析算法
- **TaskScheduler**: 任务调度
- **ArchitectOrchestrator**: 架构师服务编排

## 前端

### Dashboard
- **HTML/CSS/JS**: 纯原生，无框架
- **设计风格**: 工业美学，浅色主题
- **字体**: Consolas等宽字体
- **自动刷新**: 30秒

## 数据库

### SQLite 3.x
- **位置**: database/data/tasks.db
- **表数量**: 12个
- **Schema版本**: v2 (知识库增强)

### 核心表
1. tasks - 任务主表
2. projects - 项目
3. components - 组件
4. issues - 问题
5. solutions - 解决方案
6. decisions - 技术决策
7. knowledge_articles - 知识文章

## AI技术

### Claude API 3.5 Sonnet
- **用途**: AI角色智能(可选)
- **模型**: claude-3-5-sonnet-20241022
- **Token**: 1M上下文

### AI角色
1. 架构师AI (8000字Prompt)
2. 全栈工程师AI (7000字Prompt)
3. 代码管家AI (5000字Prompt)
4. SRE AI (4500字Prompt)

## 部署

### 开发环境
```bash
python apps/dashboard/start_dashboard.py
# 或
双击: 🚀启动任务所.bat
```

### 端口
- Dashboard: 8871
- API: 8870 (待实现)

## 工具链

### 开发工具
- VS Code / Cursor
- Git
- Python虚拟环境

### 数据库工具
- SQLite命令行
- DB Browser for SQLite
- 自研migrate.py

### 端口工具
- PortManager (自研)
- netstat (系统)
