# 对话历史库API完整指南

**版本**: 1.0  
**更新时间**: 2025-11-18  
**作者**: 全栈开发工程师

---

## 📋 目录

1. [概述](#概述)
2. [API端点清单](#api端点清单)
3. [身份验证](#身份验证)
4. [数据模型](#数据模型)
5. [使用示例](#使用示例)
6. [错误处理](#错误处理)
7. [Session Memory MCP集成](#session-memory-mcp集成)
8. [性能优化](#性能优化)
9. [常见问题](#常见问题)

---

## 概述

对话历史库API提供完整的会话管理功能，支持：

- ✅ **会话管理**: CRUD操作
- ✅ **消息管理**: 添加和查询消息
- ✅ **标签管理**: 会话标签分类
- ✅ **统计分析**: 会话和消息统计
- ✅ **搜索查询**: 按日期和Token范围查询
- ✅ **Session Memory集成**: 与Session Memory MCP双向同步

---

## API端点清单

### 核心会话管理 (6个端点)

| 方法 | 路径 | 功能 | 状态码 |
|------|------|------|--------|
| GET | `/api/conversations` | 获取所有会话 | 200 |
| GET | `/api/conversations/{session_id}` | 获取单个会话 | 200/404 |
| POST | `/api/conversations` | 创建新会话 | 200 |
| PUT | `/api/conversations/{session_id}` | 更新会话 | 200/404 |
| DELETE | `/api/conversations/{session_id}` | 删除会话 | 200/404 |
| POST | `/api/conversations/{session_id}/messages` | 添加消息 | 200/404 |

### 消息和查询 (2个端点)

| 方法 | 路径 | 功能 | 状态码 |
|------|------|------|--------|
| GET | `/api/conversations/{session_id}/messages` | 获取会话消息 | 200/404 |
| GET | `/api/conversations/search/by-date` | 按日期查询 | 200/400 |

### 统计和标签 (2个端点)

| 方法 | 路径 | 功能 | 状态码 |
|------|------|------|--------|
| GET | `/api/conversations/stats/overview` | 获取统计信息 | 200 |
| GET | `/api/conversations/tags/list` | 获取标签列表 | 200 |

### Session Memory MCP集成 (5个端点)

| 方法 | 路径 | 功能 | 状态码 |
|------|------|------|--------|
| POST | `/api/conversations/session-memory/{session_id}/sync-to-session-memory` | 同步单个会话 | 200/404 |
| POST | `/api/conversations/session-memory/sync-all-to-session-memory` | 同步所有会话 | 200 |
| GET | `/api/conversations/session-memory/retrieve-from-session-memory` | 从Session Memory检索 | 200 |
| POST | `/api/conversations/session-memory/{session_id}/map-to-session-memory` | 创建映射 | 200/404 |
| GET | `/api/conversations/session-memory/session-memory/health` | 检查Session Memory健康状态 | 200 |

### 其他 (1个端点)

| 方法 | 路径 | 功能 | 状态码 |
|------|------|------|--------|
| GET | `/api/conversations/health` | 健康检查 | 200 |

---

## 身份验证

当前版本不需要身份验证（开发阶段）。生产环境建议添加：

```python
# 未来改进
- Bearer Token认证
- API Key验证
- 基于角色的访问控制 (RBAC)
```

---

## 数据模型

### 会话模型 (Session)

```json
{
  "session_id": "session-001",
  "title": "会话标题",
  "created_at": "2025-11-18 23:20:00",
  "updated_at": "2025-11-18 23:30:00",
  "status": "active|completed|archived",
  "total_tokens": 8500,
  "messages_count": 6,
  "participants": ["用户", "架构师AI"],
  "tags": ["标签1", "标签2"],
  "summary": "会话摘要",
  "messages": [...]
}
```

### 消息模型 (Message)

```json
{
  "id": "msg-001",
  "timestamp": "2025-11-18 23:20:00",
  "from": "用户|架构师AI",
  "content": "消息内容",
  "type": "request|response",
  "tokens": 500
}
```

### 统计模型 (Stats)

```json
{
  "total_sessions": 5,
  "active_sessions": 2,
  "completed_sessions": 3,
  "archived_sessions": 0,
  "total_messages": 50,
  "total_tokens": 100000,
  "average_tokens_per_session": 20000,
  "average_messages_per_session": 10
}
```

---

## 使用示例

### 1. 获取所有会话

```bash
curl http://localhost:8800/api/conversations
```

**响应**:
```json
{
  "success": true,
  "sessions": [...],
  "count": 3,
  "timestamp": "2025-11-18T23:45:00"
}
```

### 2. 创建新会话

```bash
curl -X POST http://localhost:8800/api/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "新项目讨论",
    "participants": ["用户", "架构师AI"],
    "tags": ["项目", "讨论"],
    "summary": "关于新项目的初步讨论"
  }'
```

### 3. 向会话添加消息

```bash
curl -X POST http://localhost:8800/api/conversations/session-001/messages \
  -H "Content-Type: application/json" \
  -d '{
    "from": "用户",
    "content": "请分析一下这个需求",
    "type": "request",
    "tokens": 500
  }'
```

### 4. 获取会话详情

```bash
curl http://localhost:8800/api/conversations/session-001
```

### 5. 更新会话

```bash
curl -X PUT http://localhost:8800/api/conversations/session-001 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "更新的标题",
    "status": "completed",
    "tags": ["完成", "存档"]
  }'
```

### 6. 按日期查询会话

```bash
curl "http://localhost:8800/api/conversations/search/by-date?start_date=2025-11-18&end_date=2025-11-19"
```

### 7. 按Token范围查询

```bash
curl "http://localhost:8800/api/conversations/search/by-tokens?min_tokens=5000&max_tokens=50000"
```

### 8. 获取统计信息

```bash
curl http://localhost:8800/api/conversations/stats/overview
```

### 9. 同步到Session Memory MCP

```bash
curl -X POST http://localhost:8800/api/conversations/session-memory/session-001/sync-to-session-memory
```

### 10. 从Session Memory检索

```bash
curl "http://localhost:8800/api/conversations/session-memory/retrieve-from-session-memory?query=关键词"
```

---

## 错误处理

### 错误响应格式

```json
{
  "detail": "错误信息描述"
}
```

### 常见错误码

| 错误码 | 含义 | 示例 |
|--------|------|------|
| 200 | 成功 | 一切正常 |
| 400 | 请求错误 | 日期格式不正确 |
| 404 | 未找到 | 会话不存在 |
| 500 | 服务器错误 | 数据库操作失败 |

### 错误处理最佳实践

```python
import httpx

try:
    response = httpx.get("http://localhost:8800/api/conversations/invalid-id")
    response.raise_for_status()
    data = response.json()
except httpx.HTTPStatusError as e:
    print(f"HTTP错误: {e.response.status_code}")
    print(f"错误详情: {e.response.text}")
except Exception as e:
    print(f"错误: {str(e)}")
```

---

## Session Memory MCP集成

### 工作流

```
对话历史库 ←→ Session Memory MCP
    ↓            ↓
  JSON文件    向量数据库
    ↓            ↓
  本地存储      语义搜索
```

### 同步流程

1. **创建会话**: 自动同步到Session Memory
2. **更新会话**: 自动同步更新
3. **删除会话**: 标记为已删除（不实际删除）
4. **查询**: 可从Session Memory进行语义搜索

### 配置

```python
# apps/api/src/routes/conversations_session_memory.py

# 修改Session Memory URL
SESSION_MEMORY_URL = "http://localhost:5173"  # 默认值

# 修改超时时间
TIMEOUT = 10  # 秒
```

### 高可用性配置

```python
# 重试机制
async def sync_with_retry(session_id: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return await sync_to_session_memory(session_id)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

---

## 性能优化

### 1. 批量操作

```python
# 不推荐: 逐个创建
for i in range(100):
    client.post("/api/conversations", json={...})

# 推荐: 批量操作
# 使用异步任务或批量API
```

### 2. 分页查询

```bash
# 获取第一页 (可以扩展API支持)
curl "http://localhost:8800/api/conversations?limit=20&offset=0"
```

### 3. 缓存策略

```python
# 客户端缓存
cache = {}

def get_conversation(session_id: str):
    if session_id in cache:
        return cache[session_id]
    
    response = client.get(f"/api/conversations/{session_id}")
    data = response.json()
    cache[session_id] = data
    return data
```

### 4. 异步调用

```python
import asyncio
import httpx

async def sync_all_sessions():
    async with httpx.AsyncClient() as client:
        tasks = [
            client.post(f"/api/conversations/session-memory/{sid}/sync-to-session-memory")
            for sid in session_ids
        ]
        results = await asyncio.gather(*tasks)
        return results
```

---

## 常见问题

### Q1: 如何快速开始?

**A**: 
```bash
# 1. 启动API服务
python apps/api/start_api.py

# 2. 打开API文档
http://localhost:8800/api/docs

# 3. 使用Swagger UI测试API
```

### Q2: 数据存储在哪里?

**A**: 
- 本地: `automation-data/architect-conversations.json`
- Session Memory: 向量数据库（可选）

### Q3: 如何与Session Memory MCP集成?

**A**:
```bash
# 1. 启动Session Memory MCP服务
python session-memory-mcp/start.py

# 2. 同步会话
curl -X POST http://localhost:8800/api/conversations/session-memory/sync-all-to-session-memory

# 3. 检查状态
curl http://localhost:8800/api/conversations/session-memory/session-memory/health
```

### Q4: 如何处理大量消息?

**A**:
- 使用分页查询
- 考虑数据库分片
- 实现消息归档机制
- 使用异步处理

### Q5: 如何扩展新功能?

**A**:
1. 在 `conversations.py` 中添加新的API端点
2. 编写单元测试
3. 更新API文档
4. 注册到 `main.py`

---

## 最佳实践

### 1. 命名约定

```python
# 会话ID
session_id = "session-001"  # 格式: session-XXX

# 消息ID
message_id = "msg-001"  # 格式: msg-XXX

# 标签
tags = ["数据更新", "Dashboard", "需求分析"]  # 使用中文，避免特殊字符
```

### 2. 错误处理

```python
from fastapi import HTTPException

try:
    session = find_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
except HTTPException:
    raise
except Exception as e:
    raise HTTPException(status_code=500, detail=f"内部错误: {str(e)}")
```

### 3. 日志记录

```python
import logging

logger = logging.getLogger(__name__)

logger.info(f"创建会话: {session_id}")
logger.error(f"删除会话失败: {session_id}, 错误: {error}")
```

### 4. 验证输入

```python
from pydantic import BaseModel, Field

class CreateMessageRequest(BaseModel):
    from_user: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=10000)
    tokens: int = Field(0, ge=0, le=1000000)
```

---

## 部署检查清单

- [ ] API服务正常运行
- [ ] 数据文件存在且可读写
- [ ] 所有11个端点都能访问
- [ ] 错误响应格式正确
- [ ] Session Memory MCP已配置（可选）
- [ ] 日志记录正常
- [ ] 性能测试通过
- [ ] 文档已更新

---

## 相关资源

- [REQ-003对话历史库功能文档](../../../docs/features/conversation-history-library.md)
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Session Memory MCP文档](../../../session-memory-mcp/README.md)

---

**文档版本**: v1.0  
**最后更新**: 2025-11-18  
**维护者**: 全栈开发工程师

