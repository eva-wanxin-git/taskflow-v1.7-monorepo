# 编码规范

## Python规范

### 代码风格
- 遵循PEP 8
- 使用类型标注
- 函数≤50行
- 类≤300行

### 命名规范
```python
# 类名: PascalCase
class TaskManager:
    pass

# 函数/变量: snake_case
def create_task():
    task_id = "TASK-001"

# 常量: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3

# 私有方法: _前缀
def _internal_method():
    pass
```

### 文档字符串
```python
def create_task(task_data: dict) -> Task:
    """创建新任务
    
    Args:
        task_data: 任务数据字典
        
    Returns:
        Task对象
        
    Raises:
        ValidationError: 数据验证失败
    """
    pass
```

## 项目规范

### 目录结构
```
apps/          # 应用层(API/Dashboard/Worker)
packages/      # 共享代码(core-domain/infra/algorithms)
docs/          # 文档(arch/api/adr)
database/      # 数据库(schemas/migrations/data)
ops/           # 运维(docker/ci-cd/monitoring)
```

### 文件命名
- Python: snake_case.py
- Markdown: kebab-case.md或emoji-标题.md
- JSON/YAML: kebab-case.json

## Git规范

### Commit格式
```
[类型] 简短描述

详细说明（可选）

相关任务: TASK-C-1
```

### 类型
- feat: 新功能
- fix: Bug修复
- refactor: 重构
- docs: 文档
- test: 测试
- chore: 构建/工具
