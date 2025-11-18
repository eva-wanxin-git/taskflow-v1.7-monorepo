# 工具链说明

## 核心工具

### 1. PortManager (端口管理)
**位置**: packages/shared-utils/port_manager.py
**功能**: 自动分配端口，避免冲突
**使用**:
```python
from port_manager import allocate_project_port
port = allocate_project_port("TASKFLOW")
```

### 2. 数据库迁移工具
**位置**: database/migrations/migrate.py
**命令**:
```bash
python migrate.py init      # 初始化
python migrate.py status    # 检查状态
python migrate.py backup    # 备份
python migrate.py seed      # 插入初始数据
```

### 3. 知识库测试工具
**位置**: test_knowledge_db.py
**功能**: 验证12表数据库
**使用**: `python test_knowledge_db.py`

### 4. Dashboard数据测试
**位置**: test_dashboard_data.py
**功能**: 测试StateManager读取
**使用**: `python test_dashboard_data.py`

## 一键启动脚本

### 🚀启动任务所.bat
**功能**: 一键启动Dashboard
**使用**: 双击运行
**端口**: 8871
**访问**: http://localhost:8871

## 调试工具

### 数据库检查
```bash
python check_db.py
```

### Schema修复
```bash
python fix_schema_for_dashboard.py
python fix_status.py
```

### 任务录入
```bash
python create_v17_tasks.py
```
