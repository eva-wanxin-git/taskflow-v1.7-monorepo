# 问题解决库

## Dashboard相关

### 问题: Dashboard启动后空白
**症状**: 浏览器打开显示空白或"等待架构师..."
**排查步骤**:
1. 检查端口是否监听: `netstat -ano | findstr 8871`
2. 检查数据库数据: `python check_db.py`
3. 检查StateManager: `python test_dashboard_data.py`
4. 检查浏览器控制台错误

**常见原因**:
- 数据库Schema不兼容
- 状态值格式错误
- API端点返回空数据

### 问题: 端口被占用
**症状**: 启动失败，提示端口已被使用
**解决**:
1. 查找占用进程: `netstat -ano | findstr 8871`
2. 停止进程: `Stop-Process -Id {PID}`
3. 或换端口: 编辑start_dashboard.py

### 问题: 功能清单不显示
**症状**: Tab可切换但内容为"等待架构师..."
**排查**:
1. curl http://localhost:8871/api/project_scan
2. 检查返回的JSON格式
3. 检查features.implemented/partial/conflicts字段

**常见原因**:
- /api/project_scan返回空对象
- JSON格式错误
- 文件路径不对

## 数据库相关

### 问题: 任务读取失败
**症状**: StateManager.list_all_tasks()抛出异常
**排查**:
1. 检查tasks表结构: PRAGMA table_info(tasks)
2. 检查必需字段是否存在
3. 运行fix_schema_for_dashboard.py

### 问题: 依赖关系不显示
**症状**: Dashboard上看不到任务依赖
**原因**: depends_on字段为空或格式错误
**解决**: 从task_dependencies表同步数据

## API相关

### 问题: API 404
**排查**: 访问/docs查看所有端点
**常见原因**:
- 路由未注册
- 路径拼写错误
- 方法不对(GET/POST)
