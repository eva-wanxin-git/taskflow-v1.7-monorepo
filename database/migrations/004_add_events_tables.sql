-- ============================================================================
-- Migration 004: 添加事件系统表
-- ============================================================================
-- 创建时间: 2025-11-18
-- 说明: 为任务所·Flow v1.7添加事件发射和存储功能
-- ============================================================================

-- 执行v3事件schema
-- 注意: SQLite不支持在migration中使用.read命令，需要手动复制SQL

-- 1. 创建project_events表
CREATE TABLE IF NOT EXISTS project_events (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_category TEXT NOT NULL DEFAULT 'general',
    source TEXT NOT NULL DEFAULT 'system',
    actor TEXT,
    title TEXT NOT NULL,
    description TEXT,
    data TEXT,
    related_entity_type TEXT,
    related_entity_id TEXT,
    severity TEXT DEFAULT 'info',
    status TEXT DEFAULT 'processed',
    tags TEXT,
    occurred_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 2. 创建event_types表
CREATE TABLE IF NOT EXISTS event_types (
    id TEXT PRIMARY KEY,
    type_code TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    display_name TEXT NOT NULL,
    description TEXT,
    severity_default TEXT DEFAULT 'info',
    is_active INTEGER DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 3. 创建event_stats表
CREATE TABLE IF NOT EXISTS event_stats (
    project_id TEXT PRIMARY KEY,
    total_events INTEGER DEFAULT 0,
    events_today INTEGER DEFAULT 0,
    events_this_week INTEGER DEFAULT 0,
    events_this_month INTEGER DEFAULT 0,
    task_events INTEGER DEFAULT 0,
    issue_events INTEGER DEFAULT 0,
    decision_events INTEGER DEFAULT 0,
    deployment_events INTEGER DEFAULT 0,
    system_events INTEGER DEFAULT 0,
    info_events INTEGER DEFAULT 0,
    warning_events INTEGER DEFAULT 0,
    error_events INTEGER DEFAULT 0,
    critical_events INTEGER DEFAULT 0,
    last_event_at TEXT,
    last_updated TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 4. 创建索引
CREATE INDEX IF NOT EXISTS idx_events_project ON project_events(project_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON project_events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_category ON project_events(event_category);
CREATE INDEX IF NOT EXISTS idx_events_occurred ON project_events(occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_severity ON project_events(severity);
CREATE INDEX IF NOT EXISTS idx_events_entity ON project_events(related_entity_type, related_entity_id);
CREATE INDEX IF NOT EXISTS idx_events_actor ON project_events(actor);
CREATE INDEX IF NOT EXISTS idx_event_types_category ON event_types(category);

-- 5. 插入预定义事件类型
INSERT OR IGNORE INTO event_types (id, type_code, category, display_name, description, severity_default) VALUES
    ('ET-01', 'task.created', 'task', '任务创建', '新任务被创建', 'info'),
    ('ET-02', 'task.updated', 'task', '任务更新', '任务信息被更新', 'info'),
    ('ET-03', 'task.completed', 'task', '任务完成', '任务被标记为完成', 'info'),
    ('ET-04', 'task.blocked', 'task', '任务阻塞', '任务被阻塞', 'warning'),
    ('ET-05', 'task.assigned', 'task', '任务分配', '任务被分配给工程师', 'info'),
    ('ET-11', 'issue.discovered', 'issue', '问题发现', '发现新问题', 'warning'),
    ('ET-12', 'issue.resolved', 'issue', '问题解决', '问题被解决', 'info'),
    ('ET-13', 'issue.escalated', 'issue', '问题升级', '问题严重性升级', 'error'),
    ('ET-21', 'decision.made', 'decision', '决策制定', '架构决策被制定', 'info'),
    ('ET-22', 'decision.changed', 'decision', '决策变更', '架构决策被修改', 'warning'),
    ('ET-23', 'decision.deprecated', 'decision', '决策废弃', '架构决策被废弃', 'warning'),
    ('ET-31', 'deployment.started', 'deployment', '部署开始', '开始部署到环境', 'info'),
    ('ET-32', 'deployment.completed', 'deployment', '部署完成', '部署成功完成', 'info'),
    ('ET-33', 'deployment.failed', 'deployment', '部署失败', '部署失败', 'error'),
    ('ET-34', 'deployment.rollback', 'deployment', '部署回滚', '回滚到之前版本', 'warning'),
    ('ET-91', 'system.startup', 'system', '系统启动', '系统启动', 'info'),
    ('ET-92', 'system.shutdown', 'system', '系统关闭', '系统关闭', 'info'),
    ('ET-93', 'system.error', 'system', '系统错误', '系统发生错误', 'error'),
    ('ET-94', 'system.backup', 'system', '系统备份', '数据备份完成', 'info');

-- Migration完成

