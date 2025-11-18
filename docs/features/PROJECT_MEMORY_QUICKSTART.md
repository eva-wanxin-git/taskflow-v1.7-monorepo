# 🚀 项目记忆空间 - 快速入门（5分钟）

> **快速上手项目记忆空间功能**

---

## ⚡ 3步开始使用

### 步骤 1: 运行数据库迁移（1分钟）

```bash
cd taskflow-v1.7-monorepo
python database/migrations/migrate.py --apply 003_add_project_memories.sql
```

### 步骤 2: 启动API服务（1分钟）

```bash
# 启动FastAPI服务
cd apps/api
uvicorn main:app --reload --port 8870
```

### 步骤 3: 测试功能（3分钟）

```bash
# 1. 健康检查
curl http://localhost:8870/api/projects/TASKFLOW/memories/health

# 2. 创建第一个记忆
curl -X POST http://localhost:8870/api/projects/TASKFLOW/memories \
  -H "Content-Type: application/json" \
  -d '{
    "memory_type": "knowledge",
    "category": "knowledge",
    "title": "我的第一个记忆",
    "content": "这是一个测试记忆",
    "importance": 5
  }'

# 3. 检索记忆
curl "http://localhost:8870/api/projects/TASKFLOW/memories?limit=10"
```

---

## 💡 常见使用场景

### 场景1：自动记录架构决策

```bash
curl -X POST http://localhost:8870/api/projects/TASKFLOW/memories/auto-record/decision \
  -H "Content-Type: application/json" \
  -d '{
    "title": "采用Monorepo架构",
    "context": "项目规模扩大需要统一管理",
    "decision": "使用pnpm workspace实现Monorepo",
    "consequences": "提高代码复用性",
    "alternatives": ["Lerna", "Nx"]
  }'
```

### 场景2：记录问题解决方案

```bash
curl -X POST http://localhost:8870/api/projects/TASKFLOW/memories/auto-record/solution \
  -H "Content-Type: application/json" \
  -d '{
    "problem_title": "性能优化",
    "problem_description": "页面加载慢",
    "solution_title": "添加缓存",
    "solution_description": "使用Redis缓存查询结果",
    "solution_steps": ["安装Redis", "实现缓存逻辑", "测试验证"],
    "tools_used": ["Redis"],
    "severity": "medium"
  }'
```

### 场景3：知识继承

```bash
# 新会话开始时获取历史知识
curl "http://localhost:8870/api/projects/TASKFLOW/knowledge/inherit?context=开始新任务&limit=20"
```

---

## 📊 在Dashboard中查看

访问任务所Dashboard：

```
http://localhost:8870/dashboard
```

在Dashboard中可以：
- ✅ 查看项目记忆统计
- ✅ 浏览所有记忆
- ✅ 搜索相关记忆
- ✅ 查看记忆关系图谱

---

## 🔧 Python代码示例

```python
from services.project_memory_service import create_project_memory_service

# 创建服务
service = create_project_memory_service()

# 创建记忆
memory = service.create_memory(
    project_id="TASKFLOW",
    memory_type="ultra",
    category="knowledge",
    title="Python最佳实践",
    content="使用类型提示提高代码质量",
    tags=["python", "best-practice"],
    importance=7
)

# 检索记忆
memories = service.retrieve_memories(
    project_id="TASKFLOW",
    query="如何优化性能",
    limit=10
)

# 知识继承
knowledge = service.inherit_knowledge(
    project_id="TASKFLOW",
    context="开始新任务",
    limit=20
)
```

---

## 🎯 下一步

1. 阅读[完整文档](./PROJECT_MEMORY_SPACE.md)
2. 查看[API参考](../../apps/api/src/routes/project_memory.py)
3. 运行[单元测试](../../tests/test_project_memory_service.py)
4. 配置Session Memory和Ultra Memory MCP

---

## ❓ 常见问题

### Q: 如何配置外部记忆系统？

A: 参考 `🧠Eva的双记忆系统-完整使用指南.md`

### Q: 记忆会自动删除吗？

A: 本地记忆永久保存。Session Memory 24小时，Ultra Memory 30天（可配置）。

### Q: 如何导出记忆？

A: 使用API导出为JSON：
```bash
curl http://localhost:8870/api/projects/TASKFLOW/memories?limit=1000 > memories.json
```

---

**快速开始完成！** 🎉

现在你可以开始使用项目记忆空间了。

