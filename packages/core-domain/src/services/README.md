# 核心服务层

## 项目记忆空间服务

### ProjectMemoryService

为每个项目建立独立的记忆空间，集成 Session Memory 和 Ultra Memory Cloud。

**核心功能**:
- 项目隔离存储
- 自动记录架构决策（ADR）
- 自动记录问题解决方案
- 跨会话知识继承
- 记忆关系图谱

**快速使用**:

```python
from services.project_memory_service import create_project_memory_service

# 创建服务
service = create_project_memory_service()

# 创建记忆
memory = service.create_memory(
    project_id="MY_PROJECT",
    memory_type="ultra",
    category="knowledge",
    title="Python最佳实践",
    content="使用类型提示...",
    importance=7
)

# 自动记录架构决策
service.auto_record_architecture_decision(
    project_id="MY_PROJECT",
    title="采用Monorepo",
    context="项目规模扩大",
    decision="使用pnpm workspace"
)

# 知识继承
knowledge = service.inherit_knowledge(
    project_id="MY_PROJECT",
    context="开始新任务"
)
```

**文档**:
- [完整文档](../../../../docs/features/PROJECT_MEMORY_SPACE.md)
- [快速入门](../../../../docs/features/PROJECT_MEMORY_QUICKSTART.md)
- [测试](../../../../tests/test_project_memory_service.py)

