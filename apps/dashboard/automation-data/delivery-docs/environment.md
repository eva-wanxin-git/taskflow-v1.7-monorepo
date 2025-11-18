# 环境说明

## 开发环境

### 必需软件
- Python 3.11+
- Git
- VS Code / Cursor

### Python依赖
```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pyyaml==6.0
```

安装: `pip install -r requirements.txt`

## 端口分配

### v1.7端口(8870-8899)
- **8870**: API服务(架构师API) - 待实现
- **8871**: Dashboard(任务看板) - ✅ 运行中
- **8872-8899**: 保留

### 其他项目端口
- **8888**: librechat-desktop
- **8889**: ai-task-automation-board
- **8890**: dify-workflow-api

## 目录结构

```
taskflow-v1.7-monorepo/
├── apps/api/          # API服务(待实现main.py)
├── apps/dashboard/    # Dashboard(✅运行中)
├── packages/          # 共享代码
├── database/          # 数据库(✅12表)
├── docs/              # 文档(✅完整)
└── config/            # 配置
```

## 数据库

### 位置
`database/data/tasks.db`

### 表数量
12个表: tasks, projects, components, issues等

### 备份
```bash
python database/migrations/migrate.py backup
```
