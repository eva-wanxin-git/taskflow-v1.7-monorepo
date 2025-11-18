# 开发问题解决库

## v1.7常见问题

### 1. Dashboard端口冲突和浏览器缓存
**问题**: 更新Dashboard后浏览器显示旧内容，即使Ctrl+F5也无效
**根因**: 
- 浏览器对localhost缓存激进
- Service Worker可能缓存整个应用
- 同一端口重启服务，浏览器认为是同一应用

**解决**: 
- 短期：换新端口（8870→8871→8872→8873）
- 长期：添加版本号到URL + 设置no-cache HTTP头

**命令**:
```python
# 修改start_dashboard.py中的端口
port = 8873  # 换新端口

# 添加no-cache头（建议）
response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
```

**运维日志**: 2025-11-19记录在ops/incidents.md

---

### 2. 数据库Schema不兼容
**问题**: StateManager期望的字段和v1.7数据库不一致
**解决**: 运行fix_schema_for_dashboard.py添加必需字段
**位置**: scripts/fix_schema_for_dashboard.py

---

### 3. 状态值格式错误
**问题**: 大写'PENDING'导致Pydantic验证失败
**解决**: 统一使用小写'pending'
**命令**: UPDATE tasks SET status = LOWER(status)

---

### 4. API端点重复定义
**问题**: 同一个路由定义两次，后者覆盖前者
**解决**: 搜索重复的@app.get装饰器并删除
**位置**: dashboard.py第228行和567行（已修复）

---

### 5. 功能清单JSON未正确返回
**问题**: /api/project_scan硬编码数据，没有读取JSON文件
**解决**: 修改dashboard.py读取v17-complete-features.json
**位置**: dashboard.py第228行

---

### 6. 待完成任务不显示
**问题**: 前端缺少loadTodoFeatures()渲染函数
**解决**: 添加函数并在window.onload中调用
**位置**: templates.py第4655行

---

## v1.6历史问题

### Tab切换失效
**根因**: JavaScript模板字符串中反引号未转义
**修复**: 在Python f-string中的JS反引号前加反斜杠
**参考**: ../任务所-v1.6-Tab修复版/🐛Tab切换不工作-Bug修复提示词.md
