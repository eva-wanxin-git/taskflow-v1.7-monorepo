# 最佳实践

## v1.7架构最佳实践

### 1. 使用PortManager自动分配端口
```python
from packages.shared_utils.port_manager import allocate_project_port
port = allocate_project_port("MY_PROJECT")
```

### 2. 数据库迁移规范
```bash
# 创建新表
python database/migrations/migrate.py init

# 检查状态
python database/migrations/migrate.py status
```

### 3. 任务元数据使用JSON
```python
metadata = {
    "tags": "backend,critical",
    "project_id": "taskflow-main",
    "component_id": "taskflow-api"
}
```

### 4. 依赖关系管理
- 使用task_dependencies表
- 或在Task对象中用depends_on字段(JSON数组)

## 性能优化

### SQLite优化
- 使用连接池
- 添加重试机制
- 设置timeout=5.0

### API优化
- 使用async/await
- 合理使用缓存
- 避免N+1查询

## 安全实践

### 数据库
- 使用参数化查询（防SQL注入）
- 定期备份

### API
- 添加CORS配置
- 输入验证（Pydantic）
- 错误不暴露内部信息
