# 性能基线

## v1.7 Dashboard性能

### 启动性能
- **启动时间**: <3秒
- **内存占用**: ~80MB
- **CPU使用**: <5%

### API响应时间(本地)
- `/api/tasks`: ~10ms
- `/api/stats`: ~5ms
- `/api/project_scan`: ~15ms
- `/api/architect_monitor`: ~5ms

### 数据库性能
- **查询延迟**: <10ms (本地SQLite)
- **写入延迟**: <20ms
- **并发支持**: 单写锁，建议QPS<100

## 容量规划

### 当前规模
- 任务数: 5个
- 项目数: 1个
- 组件数: 5个

### 扩展建议
- 任务<1000: SQLite足够
- 任务>1000: 考虑PostgreSQL
- QPS>100: 添加Redis缓存
