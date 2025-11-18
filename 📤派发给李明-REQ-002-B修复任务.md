# 📤 派发给全栈工程师·李明 - REQ-002-B修复任务

**派发时间**: 2025-11-19 01:18  
**派发人**: AI Architect (Expert Level)  
**接收人**: 全栈工程师·李明  
**优先级**: 🔴 P0 Critical  
**任务类型**: 🔧 Bug修复/功能完善

---

## 🚀 开始前必读

李明，在执行任务前，请先加载以下文档：

```markdown
@taskflow-v1.7-monorepo/docs/ai/fullstack-engineer-system-prompt.md
@taskflow-v1.7-monorepo/🏛️架构师审查-REQ-002完成报告.md
@taskflow-v1.7-monorepo/📤派发给李明-REQ-002-B修复任务.md
```

**这些文档会告诉你**：
1. 全栈工程师的工作规范
2. REQ-002审查发现的问题
3. 具体的修复要求

---

## 🚀 第一步：接收任务（必做！）

⚠️ **重要**: 看到此任务后，**立即执行**：

```bash
cd taskflow-v1.7-monorepo
python scripts/李明收到任务.py REQ-002-B
```

**这会做什么**:
- ✅ 更新任务状态: pending → in_progress
- ✅ 记录接收时间和执行人
- ✅ Dashboard实时显示"⚙️ 进行中"

**⚠️ 不运行此脚本，架构师看不到你的进度！**

---

## 📋 审查反馈

### REQ-002审查结果：⚠️ 有条件通过

**李明，你的REQ-002工作**：

✅ **做得极好**：
- 架构设计优秀（10/10分）⭐⭐⭐⭐⭐
- 数据库Schema完整（4表8索引）
- API接口规范（11个端点）
- 测试覆盖优秀（14用例100%通过）
- 文档详尽（2份，880行）

❌ **核心问题**：
- **所有数据库查询方法都是TODO**
- API调用返回空列表/空数据
- 功能实际不可用（架构完美，但无实现）

**类比**：
> 就像建了一栋漂亮的房子（架构），
> 装好了门窗（API接口），
> 但**没装水电**（数据库查询）。
> 
> 你不能说这房子"完成了"。

---

## 🎯 REQ-002-B任务目标

**修复REQ-002的核心问题**：实现所有数据库查询方法

**工时**: 4小时  
**复杂度**: MEDIUM  
**依赖**: REQ-002（架构已完成）

---

## 🔧 需要实现的方法（7个）

### 位置
`packages/core-domain/src/services/project_memory_service.py`

### 1. _query_memories() - 核心检索

**当前代码**：
```python
def _query_memories(
    self, 
    project_id: str,
    memory_type: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict]:
    """查询记忆列表"""
    # TODO: 实现数据库查询逻辑  ← 需要修复！
    return []  # 返回空列表
```

**需要实现**：
```python
def _query_memories(
    self, 
    project_id: str,
    memory_type: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict]:
    """查询记忆列表"""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    # 构造SQL查询
    query = "SELECT * FROM project_memories WHERE project_id = ?"
    params = [project_id]
    
    if memory_type:
        query += " AND memory_type = ?"
        params.append(memory_type)
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    # 转换为字典列表
    memories = []
    for row in rows:
        memories.append({
            "id": row[0],
            "project_id": row[1],
            "memory_type": row[2],
            "category": row[4],
            "title": row[5],
            "content": row[6],
            # ... 其他字段
        })
    
    return memories
```

---

### 2. _query_memory_by_id() - 按ID查询

**当前**: 返回None  
**需要**: 从project_memories表查询单条记录

---

### 3. _query_related_memories() - 相关记忆

**当前**: 返回空列表  
**需要**: 
- 从memory_relations表查询关联
- JOIN获取相关记忆详情

---

### 4. _query_memory_stats() - 统计查询

**当前**: 返回模拟数据  
**需要**: 从memory_stats表查询真实统计

---

### 5. _insert_memory() - 插入记忆

**当前**: 可能有实现，请检查  
**需要**: INSERT INTO project_memories

---

### 6. _insert_memory_relation() - 插入关系

**当前**: 可能有实现，请检查  
**需要**: INSERT INTO memory_relations

---

### 7. _record_retrieval() - 记录检索历史

**当前**: 可能为空  
**需要**: INSERT INTO memory_retrievals

---

## ✅ 验收标准

### 功能验收
- [ ] **所有查询方法实现**（没有TODO）
- [ ] **API返回真实数据**（不是空列表）
- [ ] **自测所有11个API端点**
- [ ] **数据库读写正常**

### 测试验收
- [ ] 编写集成测试（至少5个场景）
- [ ] 测试创建记忆→查询记忆
- [ ] 测试记忆关系→查询相关记忆
- [ ] 测试统计功能
- [ ] 所有测试通过

### 代码质量
- [ ] 无TODO注释
- [ ] 错误处理完整（数据库错误、参数验证）
- [ ] 有docstring
- [ ] 有日志记录

### 完成报告
- [ ] 提交7部分完成报告
- [ ] 诚实说明完成度
- [ ] 提供测试截图/日志

---

## 🧪 测试方法

### 手动测试脚本

```python
# tests/manual_test_memory.py

import requests

BASE_URL = "http://localhost:8870"
PROJECT = "TEST_PROJECT"

# 1. 创建记忆
response = requests.post(
    f"{BASE_URL}/api/projects/{PROJECT}/memories",
    json={
        "category": "architecture",
        "title": "测试记忆",
        "content": "这是一条测试记忆",
        "importance": 8
    }
)
print("创建记忆:", response.json())
memory_id = response.json()["id"]

# 2. 查询记忆（应该返回数据，不是空列表）
response = requests.get(
    f"{BASE_URL}/api/projects/{PROJECT}/memories"
)
print("查询记忆:", response.json())
assert len(response.json()["memories"]) > 0, "❌ 查询返回空！"

# 3. 获取统计（应该返回真实数据）
response = requests.get(
    f"{BASE_URL}/api/projects/{PROJECT}/memories/stats"
)
print("统计信息:", response.json())
assert response.json()["total_memories"] > 0, "❌ 统计为0！"

print("✅ 所有测试通过！")
```

---

## 📚 参考资料

### 必读
1. **审查报告**: `🏛️架构师审查-REQ-002完成报告.md`
   - 了解我发现了什么问题
   - 为什么说是"有条件通过"

2. **REQ-002完成报告**: `✅REQ-002-项目记忆空间-完成报告.md`
   - 你之前的工作成果
   - 架构和接口设计

3. **数据库Schema**: `database/schemas/v2_knowledge_schema.sql`
   - 4个表的结构
   - 字段定义

### 参考实现
- StateManager: `任务所-v1.6-Tab修复版/automation/state_manager.py`
  - 查看CRUD操作的参考实现

---

## 🎯 完成标准（对比REQ-001和REQ-006）

李明，你的REQ-001和REQ-006都是**满分（10/10）**，因为：
- ✅ 承诺的功能100%实现
- ✅ 没有TODO或占位代码
- ✅ 自己测试过功能可用
- ✅ 完成报告准确诚实

**REQ-002-B也要达到这个标准**：
- ✅ 7个方法全部实现（不能有TODO）
- ✅ 自己测试过API返回真实数据
- ✅ 完成报告证明功能可用

---

## ⚠️ 特别提醒

### 1. 核心逻辑不能TODO
```python
# ❌ 这样不算完成
def query_something():
    # TODO: 实现查询
    return []

# ✅ 这样才算完成
def query_something():
    """查询XXX"""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ...")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
```

### 2. 提交前自测
```bash
# 必须自己测试
python tests/manual_test_memory.py

# 期望输出
创建记忆: {"success": true, "id": "mem-001"}
查询记忆: {"memories": [...], "total": 1}  ← 不能是空！
统计信息: {"total_memories": 1, ...}  ← 不能是0！
✅ 所有测试通过！
```

### 3. 完成报告要诚实
- ✅ 功能完成：说"100%完成，已测试可用"
- ❌ 功能半成品：不要说"完成"，要说"架构完成，实现X%"

---

## 📋 工作流程

```
1. 加载必读文档
   ↓
   @fullstack-engineer-system-prompt.md
   @🏛️架构师审查-REQ-002完成报告.md
   @📤派发给李明-REQ-002-B修复任务.md

2. 理解审查反馈
   ↓
   为什么有条件通过？
   需要修复什么？

3. 实现7个查询方法
   ↓
   逐个实现，逐个自测

4. 集成测试
   ↓
   编写测试脚本
   验证所有API可用

5. 提交完成报告
   ↓
   按模板生成7部分报告
   用户一键复制给架构师

6. 等待审查
   ↓
   架构师审查 → 通过/修改
```

---

## 🏆 期望产出

**REQ-002-B完成后（4小时）**：
- ✅ 7个查询方法全部实现
- ✅ API返回真实数据
- ✅ 集成测试通过
- ✅ 项目记忆空间功能100%可用
- ✅ REQ-002真正完成！

---

**李明，这是基于审查反馈的修复任务！**

**请对比REQ-001和REQ-006的标准，让REQ-002-B也达到满分！** 💪

**记住**：
- ✅ 先读审查报告（理解问题）
- ✅ 实现不能有TODO
- ✅ 自测功能可用
- ✅ 提交完成报告

**工作愉快！期待你的完美修复！**

---

## 📝 最后一步：提交完成（必做！）

完成后**立即执行**:

```bash
cd taskflow-v1.7-monorepo
python scripts/李明提交完成.py REQ-002-B --hours <实际工时>
```

**示例**:
```bash
python scripts/李明提交完成.py REQ-002-B --hours 4 --summary "7个查询方法全部实现，测试通过"
```

**这会做什么**:
- ✅ 更新任务状态: in_progress → completed
- ✅ 记录实际工时
- ✅ Dashboard显示"📄 一键复制完成报告"按钮

**然后**: 
1. 刷新Dashboard
2. 点击"📄 一键复制完成报告"按钮
3. 粘贴报告并补充详细信息
4. 提交给架构师审查

---

**架构师**: AI Architect (Expert Level)  
**派发时间**: 2025-11-19 01:18  
**Dashboard**: http://localhost:8877

