# 常用工具库

## Python工具

### FastAPI (0.104+)
- **用途**: Web API框架
- **位置**: apps/api/
- **文档**: https://fastapi.tiangolo.com

### Pydantic (2.5+)
- **用途**: 数据验证和序列化
- **位置**: 所有模型定义
- **文档**: https://docs.pydantic.dev

### SQLite (3.x)
- **用途**: 数据库
- **位置**: database/data/tasks.db
- **工具**: DB Browser for SQLite

## 开发工具

### PortManager
- **位置**: packages/shared-utils/port_manager.py
- **用途**: 自动分配端口(8870-8899)
- **使用**: from port_manager import allocate_project_port

### 迁移工具
- **位置**: database/migrations/migrate.py
- **命令**: python migrate.py init/status/backup/seed

## 调试工具

### 数据库检查
```bash
python check_db.py
python test_dashboard_data.py
```

### 端口检查
```bash
netstat -ano | findstr 8871
```
