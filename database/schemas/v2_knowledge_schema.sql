-- ============================================================================
-- 任务所·Flow v1.7 - 知识库Schema（新增）
-- ============================================================================
-- 创建时间: 2025-11-18
-- 说明: 项目知识库数据库，实现任务与知识的关联
-- 参考: 企业级项目知识图谱设计
-- ============================================================================

-- ============================================================================
-- 1. 项目主表
-- ============================================================================
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,                      -- 使用TEXT而非UUID（SQLite兼容）
    name TEXT NOT NULL,                        -- 项目名称
    code TEXT UNIQUE NOT NULL,                 -- 项目代码 "TASKFLOW"
    description TEXT,
    repo_url TEXT,                             -- 仓库地址
    status TEXT NOT NULL DEFAULT 'active',     -- active/archived/deprecated
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================================
-- 2. 组件/模块表
-- ============================================================================
CREATE TABLE IF NOT EXISTS components (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,                        -- "api", "dashboard", "algorithms"
    type TEXT NOT NULL,                        -- "backend", "frontend", "package", "tool"
    description TEXT,
    repo_path TEXT,                            -- "apps/api" 或 "packages/core-domain"
    owner TEXT,                                -- 负责人
    tech_stack TEXT,                           -- JSON数组: ["Python", "FastAPI"]
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- ============================================================================
-- 3. 问题记录表
-- ============================================================================
CREATE TABLE IF NOT EXISTS issues (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    component_id TEXT,
    task_id TEXT,                              -- 关联到具体任务
    title TEXT NOT NULL,
    description TEXT,
    severity TEXT DEFAULT 'medium',            -- critical/high/medium/low
    status TEXT DEFAULT 'open',                -- open/in_progress/resolved/closed
    discovered_at TEXT DEFAULT (datetime('now')),
    resolved_at TEXT,
    resolution TEXT,                           -- 解决描述
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (component_id) REFERENCES components(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- ============================================================================
-- 4. 解决方案表
-- ============================================================================
CREATE TABLE IF NOT EXISTS solutions (
    id TEXT PRIMARY KEY,
    issue_id TEXT,                             -- 关联到问题（可选）
    title TEXT NOT NULL,
    description TEXT,
    steps TEXT,                                -- JSON数组: 解决步骤
    tools_used TEXT,                           -- JSON数组: 使用的工具
    success_rate REAL DEFAULT 1.0,             -- 0.0-1.0
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (issue_id) REFERENCES issues(id)
);

-- ============================================================================
-- 5. 技术决策表（ADR的数据库版本）
-- ============================================================================
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    component_id TEXT,
    title TEXT NOT NULL,
    context TEXT,                              -- 决策背景
    decision TEXT NOT NULL,                    -- 决策内容
    consequences TEXT,                         -- 影响和后果
    alternatives TEXT,                         -- 备选方案
    status TEXT DEFAULT 'proposed',            -- proposed/accepted/rejected/deprecated
    decided_at TEXT DEFAULT (datetime('now')),
    decided_by TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (component_id) REFERENCES components(id)
);

-- ============================================================================
-- 6. 知识文章表
-- ============================================================================
CREATE TABLE IF NOT EXISTS knowledge_articles (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    component_id TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,                             -- "architecture", "pattern", "guide"
    tags TEXT,                                 -- JSON数组
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (component_id) REFERENCES components(id)
);

-- ============================================================================
-- 7. 工具表
-- ============================================================================
CREATE TABLE IF NOT EXISTS tools (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,                        -- "framework", "library", "cli", "service"
    description TEXT,
    documentation_url TEXT,
    version TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- ============================================================================
-- 8. 组件工具关联表
-- ============================================================================
CREATE TABLE IF NOT EXISTS component_tools (
    component_id TEXT NOT NULL,
    tool_id TEXT NOT NULL,
    purpose TEXT,                              -- 使用目的
    PRIMARY KEY (component_id, tool_id),
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
    FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE CASCADE
);

-- ============================================================================
-- 9. 部署记录表
-- ============================================================================
CREATE TABLE IF NOT EXISTS deployments (
    id TEXT PRIMARY KEY,
    component_id TEXT NOT NULL,
    environment TEXT NOT NULL,                 -- "dev", "staging", "prod"
    version TEXT NOT NULL,
    deployed_at TEXT NOT NULL DEFAULT (datetime('now')),
    deployed_by TEXT,
    status TEXT DEFAULT 'success',             -- success/failed/rollback
    notes TEXT,
    FOREIGN KEY (component_id) REFERENCES components(id)
);

-- ============================================================================
-- 索引优化
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_components_project ON components(project_id);
CREATE INDEX IF NOT EXISTS idx_issues_project ON issues(project_id);
CREATE INDEX IF NOT EXISTS idx_issues_component ON issues(component_id);
CREATE INDEX IF NOT EXISTS idx_issues_task ON issues(task_id);
CREATE INDEX IF NOT EXISTS idx_issues_status ON issues(status);
CREATE INDEX IF NOT EXISTS idx_solutions_issue ON solutions(issue_id);
CREATE INDEX IF NOT EXISTS idx_decisions_project ON decisions(project_id);
CREATE INDEX IF NOT EXISTS idx_articles_project ON knowledge_articles(project_id);
CREATE INDEX IF NOT EXISTS idx_deployments_component ON deployments(component_id);
CREATE INDEX IF NOT EXISTS idx_deployments_env ON deployments(environment);

-- ============================================================================
-- 说明
-- ============================================================================
-- 1. 使用TEXT类型替代UUID（SQLite兼容）
-- 2. 使用TEXT存储datetime（SQLite标准）
-- 3. 使用TEXT存储JSON（SQLite 3.38+支持JSON函数）
-- 4. 所有外键使用ON DELETE CASCADE确保数据一致性
-- ============================================================================

