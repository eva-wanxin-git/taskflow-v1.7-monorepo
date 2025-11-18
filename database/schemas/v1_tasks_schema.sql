-- ============================================================================
-- 任务所·Flow v1.7 - 任务表Schema（继承自v1.6）
-- ============================================================================
-- 创建时间: 2025-11-18
-- 说明: 现有的任务管理表结构，保持向后兼容
-- ============================================================================

-- 任务主表
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending/in_progress/review/completed/blocked
    priority TEXT DEFAULT 'P2',               -- P0/P1/P2/P3
    estimated_hours REAL DEFAULT 0,
    actual_hours REAL DEFAULT 0,
    complexity TEXT DEFAULT 'medium',         -- low/medium/high
    assigned_to TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    metadata TEXT DEFAULT '{}'                -- JSON格式
);

-- 任务依赖关系表
CREATE TABLE IF NOT EXISTS task_dependencies (
    task_id TEXT NOT NULL,
    dependency_id TEXT NOT NULL,
    PRIMARY KEY (task_id, dependency_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (dependency_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- 任务完成详情表
CREATE TABLE IF NOT EXISTS task_completions (
    task_id TEXT PRIMARY KEY,
    features_implemented TEXT,  -- JSON数组: ["功能1", "功能2"]
    files_created TEXT,          -- JSON数组: ["file1.py", "file2.py"]
    files_modified TEXT,         -- JSON数组: ["file3.py"]
    code_lines INTEGER DEFAULT 0,
    actual_hours REAL DEFAULT 0,
    notes TEXT,
    completed_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned ON tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at);

-- ============================================================================
-- 说明
-- ============================================================================
-- 1. 此Schema保持与v1.6的兼容性
-- 2. 后续会扩展 project_id 和 component_id 字段（v2_knowledge_schema.sql）
-- 3. metadata字段用于存储扩展信息，保持灵活性
-- ============================================================================

