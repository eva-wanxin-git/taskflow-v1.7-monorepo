# 📚 架构师事件监听器 - 使用指南

## 🎯 功能概述

架构师事件监听器是一个自动化监听和响应系统，能够：

1. **自动监听项目事件** - 轮询事件流，实时获取新事件
2. **智能规则引擎** - 根据5个核心规则自动处理事件
3. **Dashboard通知** - 实时推送通知到Dashboard

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    事件监听器系统                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │ EventListener│─────►│  RuleEngine  │─────►│Notification│ │
│  │   (轮询器)    │      │  (规则引擎)   │      │  Service  │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                      │                     │       │
│         ▼                      ▼                     ▼       │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │  EventStore  │      │  5个核心规则  │      │ Dashboard │ │
│  │  (事件存储)   │      │              │      │  (前端)    │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 核心组件

### 1. EventListener（事件监听器）

**功能**：
- 定时轮询事件存储
- 识别新事件
- 调用规则引擎处理事件

**配置参数**：
- `project_id`: 监听的项目ID（默认：TASKFLOW）
- `poll_interval`: 轮询间隔（默认：5秒）

### 2. RuleEngine（规则引擎）

**功能**：
- 管理多个规则
- 匹配事件类型
- 执行对应动作

**5个核心规则**：

| 规则ID | 事件类型 | 触发条件 | 执行动作 |
|--------|---------|---------|---------|
| RULE-001 | `task.completed` | 任务完成 | 提醒架构师审查 |
| RULE-002 | `feature.developed` | 功能开发完成 | 触发集成验证 |
| RULE-003 | `task.approved` | 任务审批通过 | 自动更新状态 |
| RULE-004 | `issue.discovered` | 发现问题 | 查找历史方案 |
| RULE-005 | `task.rejected` | 任务被拒绝 | 通知开发者修改 |

### 3. NotificationService（通知服务）

**功能**：
- 创建和存储通知
- 管理已读/未读状态
- 提供通知查询接口

**通知类型**：
- `info`: 信息通知 ℹ️
- `success`: 成功通知 ✅
- `warning`: 警告通知 ⚠️
- `error`: 错误通知 ❌

## 🚀 快速开始

### 1. 启动API服务

```bash
cd taskflow-v1.7-monorepo/apps/api
python start_api.py
```

API服务将在 `http://localhost:8800` 启动

### 2. 启动事件监听器

#### 方法A: 通过API启动

```bash
curl -X POST http://localhost:8800/api/listener/start \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "TASKFLOW",
    "poll_interval": 5,
    "max_notifications": 1000
  }'
```

#### 方法B: 使用Python代码

```python
import requests

response = requests.post("http://localhost:8800/api/listener/start", json={
    "project_id": "TASKFLOW",
    "poll_interval": 5,
    "max_notifications": 1000
})

print(response.json())
```

### 3. 发射测试事件

```bash
curl -X POST http://localhost:8800/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "TASKFLOW",
    "event_type": "task.completed",
    "title": "任务REQ-010-D完成",
    "description": "架构师事件监听器实现完成",
    "category": "task",
    "source": "system",
    "related_entity_type": "task",
    "related_entity_id": "REQ-010-D"
  }'
```

### 4. 查看通知

```bash
curl http://localhost:8800/api/listener/notifications?limit=10
```

## 📖 API接口文档

### 监听器管理

#### 启动监听器
```http
POST /api/listener/start
Content-Type: application/json

{
  "project_id": "TASKFLOW",
  "poll_interval": 5,
  "max_notifications": 1000
}
```

#### 停止监听器
```http
POST /api/listener/stop
```

#### 获取监听器状态
```http
GET /api/listener/status
```

### 规则管理

#### 获取规则列表
```http
GET /api/listener/rules
```

#### 启用/禁用规则
```http
POST /api/listener/rules/configure
Content-Type: application/json

{
  "rule_id": "RULE-001",
  "is_enabled": true
}
```

### 通知管理

#### 获取通知列表
```http
GET /api/listener/notifications?limit=50&unread_only=false
```

#### 标记通知为已读
```http
POST /api/listener/notifications/{notification_id}/read
```

#### 标记所有通知为已读
```http
POST /api/listener/notifications/read-all
```

#### 删除通知
```http
DELETE /api/listener/notifications/{notification_id}
```

#### 获取通知统计
```http
GET /api/listener/notifications/stats
```

### 健康检查

```http
GET /api/listener/health
```

## 🧪 测试验证

### 运行单元测试

```bash
cd taskflow-v1.7-monorepo/apps/api
pytest tests/test_listener_system.py -v
```

### 测试覆盖项

- ✅ NotificationService - 通知发送、查询、标记
- ✅ RuleEngine - 规则注册、启用/禁用、事件处理
- ✅ 5个核心规则 - 规则触发和通知
- ✅ EventListener - 初始化、启动/停止、轮询
- ✅ 完整集成测试 - 端到端流程

### 测试场景示例

```python
# 测试1: 任务完成 → 架构师审查提醒
event = {
    "event_type": "task.completed",
    "related_entity_id": "TASK-001"
}
# 预期: 收到"📋 任务完成待审查"通知

# 测试2: 功能开发 → 集成验证
event = {
    "event_type": "feature.developed",
    "related_entity_id": "FEAT-001"
}
# 预期: 收到"🔧 需要集成验证"通知

# 测试3: 任务审批 → 状态更新
event = {
    "event_type": "task.approved",
    "related_entity_id": "TASK-002"
}
# 预期: 收到"✅ 任务已批准"通知

# 测试4: 问题发现 → 历史方案搜索
event = {
    "event_type": "issue.discovered",
    "related_entity_id": "ISS-001"
}
# 预期: 收到"⚠️ 问题发现"通知

# 测试5: 任务拒绝 → 开发者修改通知
event = {
    "event_type": "task.rejected",
    "related_entity_id": "TASK-003"
}
# 预期: 收到"❌ 任务需要修改"通知
```

## 📊 监控和统计

### 查看监听器统计

```python
import requests

# 获取监听器状态
status = requests.get("http://localhost:8800/api/listener/status").json()
print("监听器状态:", status)

# 获取规则统计
rules = requests.get("http://localhost:8800/api/listener/rules").json()
print("规则统计:", rules)

# 获取通知统计
notif_stats = requests.get("http://localhost:8800/api/listener/notifications/stats").json()
print("通知统计:", notif_stats)
```

### 统计指标

**监听器统计**：
- `total_polled`: 总轮询次数
- `total_processed`: 已处理事件数
- `total_errors`: 错误次数
- `is_running`: 是否运行中

**规则引擎统计**：
- `total_events_processed`: 处理的事件总数
- `total_rules_triggered`: 触发的规则总数
- 每个规则的触发次数和成功率

**通知统计**：
- `total_sent`: 总发送数
- `info_count/success_count/warning_count/error_count`: 各类型数量
- `current_count`: 当前通知数
- `unread_count`: 未读数

## 🔍 故障排查

### 问题1: 监听器启动失败

**症状**：`POST /api/listener/start` 返回错误

**检查步骤**：
1. 确认API服务已启动：`curl http://localhost:8800/api/health`
2. 检查数据库连接：确认 `database/data/tasks.db` 存在
3. 查看API日志：检查控制台输出

### 问题2: 规则不触发

**症状**：发射事件后没有通知

**检查步骤**：
1. 确认监听器正在运行：`GET /api/listener/status`
2. 确认规则已启用：`GET /api/listener/rules`
3. 检查事件类型是否匹配规则模式
4. 查看规则统计：确认 `total_events_processed` 有增加

### 问题3: 通知未显示

**症状**：规则触发但Dashboard看不到通知

**检查步骤**：
1. 直接调用API查询通知：`GET /api/listener/notifications`
2. 检查通知统计：`GET /api/listener/notifications/stats`
3. 确认Dashboard轮询间隔设置

## 🎨 Dashboard集成

### 前端轮询通知

```javascript
// Dashboard中添加通知轮询
async function pollNotifications() {
    const response = await fetch('http://localhost:8800/api/listener/notifications?limit=20&unread_only=true');
    const data = await response.json();
    
    if (data.success && data.notifications.length > 0) {
        // 显示通知
        data.notifications.forEach(notif => {
            showNotification(notif);
        });
    }
}

// 每5秒轮询一次
setInterval(pollNotifications, 5000);
```

### 通知显示组件

```javascript
function showNotification(notification) {
    const typeIcons = {
        'info': 'ℹ️',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    };
    
    const notifElement = document.createElement('div');
    notifElement.className = `notification notification-${notification.type}`;
    notifElement.innerHTML = `
        <div class="notification-icon">${typeIcons[notification.type]}</div>
        <div class="notification-content">
            <div class="notification-title">${notification.title}</div>
            <div class="notification-message">${notification.message}</div>
        </div>
        <button onclick="markAsRead('${notification.id}')">×</button>
    `;
    
    document.getElementById('notifications-container').appendChild(notifElement);
    
    // 自动消失（如果设置了duration）
    if (notification.duration > 0) {
        setTimeout(() => {
            notifElement.remove();
        }, notification.duration);
    }
}

async function markAsRead(notificationId) {
    await fetch(`http://localhost:8800/api/listener/notifications/${notificationId}/read`, {
        method: 'POST'
    });
}
```

## 📝 最佳实践

### 1. 轮询间隔设置

- **开发环境**: 5秒（快速反馈）
- **生产环境**: 10-30秒（减少负载）
- **高频场景**: 1-3秒（实时性要求高）

### 2. 规则设计

- 规则动作应该轻量级，避免阻塞
- 重操作应该异步执行
- 规则之间避免循环依赖

### 3. 通知管理

- 定期清理旧通知（超过1000条）
- 重要通知设置较长的显示时长
- 为不同类型的通知设置优先级

### 4. 性能优化

- 使用事件索引加速查询
- 批量处理事件而非逐个处理
- 考虑将来升级为WebSocket推送

## 🔮 未来扩展

### Phase 2计划

1. **WebSocket推送** - 替代轮询，实时推送通知
2. **系统托盘通知** - 桌面应用集成
3. **规则脚本化** - 支持用户自定义规则
4. **通知持久化** - 保存到数据库
5. **通知模板** - 可配置的通知模板

### 扩展API

```python
# 自定义规则（未来功能）
POST /api/listener/rules/custom
{
    "name": "自定义规则",
    "event_pattern": "custom.*",
    "condition": "event.data.priority == 'high'",
    "action": "send_email"
}
```

## 📞 支持

如有问题，请联系：

- **架构师**: @AI架构师
- **开发者**: fullstack-engineer
- **文档**: `docs/ai/`

---

✅ **任务状态**: REQ-010-D 已完成
📅 **完成时间**: 2025-11-18
👨‍💻 **实现者**: AI全栈工程师

