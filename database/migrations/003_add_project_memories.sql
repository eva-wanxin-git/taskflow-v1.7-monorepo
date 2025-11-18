-- ============================================================================
-- 任务所·Flow v1.7 - 项目记忆空间 Schema
-- ============================================================================
-- 创建时间: 2025-11-18
-- 说明: 为每个项目建立独立的记忆空间，集成 Session Memory 和 Ultra Memory Cloud
-- ============================================================================

-- ============================================================================
-- 1. 项目记忆表
-- ============================================================================
CREATE TABLE IF NOT EXISTS project_memories (
    id TEXT PRIMARY KEY,                          -- 记忆ID
    project_id TEXT NOT NULL,                     -- 项目ID（关联projects表）
    memory_type TEXT NOT NULL,                    -- 记忆类型: session/ultra/decision/solution
    external_memory_id TEXT,                      -- 外部记忆系统的ID（Session Memory或Ultra Memory的ID）
    category TEXT NOT NULL,                       -- 分类: architecture/problem/solution/decision/knowledge
    title TEXT NOT NULL,                          -- 标题
    content TEXT NOT NULL,                        -- 内容
    context TEXT,                                 -- 上下文信息（JSON格式）
    tags TEXT,                                    -- 标签（JSON数组）
    related_tasks TEXT,                           -- 关联任务ID（JSON数组）
    related_issues TEXT,                          -- 关联问题ID（JSON数组）
    importance INTEGER DEFAULT 5,                 -- 重要性 1-10
    created_by TEXT DEFAULT 'system',             -- 创建者
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- ============================================================================
-- 2. 记忆关系表（记忆之间的关联）
-- ============================================================================
CREATE TABLE IF NOT EXISTS memory_relations (
    id TEXT PRIMARY KEY,
    source_memory_id TEXT NOT NULL,               -- 源记忆ID
    target_memory_id TEXT NOT NULL,               -- 目标记忆ID
    relation_type TEXT NOT NULL,                  -- 关系类型: related/caused-by/solved-by/evolved-from
    strength REAL DEFAULT 1.0,                    -- 关系强度 0.0-1.0
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (source_memory_id) REFERENCES project_memories(id) ON DELETE CASCADE,
    FOREIGN KEY (target_memory_id) REFERENCES project_memories(id) ON DELETE CASCADE
);

-- ============================================================================
-- 3. 记忆检索历史（用于优化检索）
-- ============================================================================
CREATE TABLE IF NOT EXISTS memory_retrievals (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    query TEXT NOT NULL,                          -- 检索查询
    memory_ids TEXT NOT NULL,                     -- 检索到的记忆ID列表（JSON数组）
    relevance_scores TEXT,                        -- 相关性分数（JSON数组）
    retrieved_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- ============================================================================
-- 4. 记忆统计表（项目级别）
-- ============================================================================
CREATE TABLE IF NOT EXISTS memory_stats (
    project_id TEXT PRIMARY KEY,
    total_memories INTEGER DEFAULT 0,
    session_memories INTEGER DEFAULT 0,
    ultra_memories INTEGER DEFAULT 0,
    decision_memories INTEGER DEFAULT 0,
    solution_memories INTEGER DEFAULT 0,
    last_updated TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- ============================================================================
-- 索引优化
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_project_memories_project ON project_memories(project_id);
CREATE INDEX IF NOT EXISTS idx_project_memories_type ON project_memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_project_memories_category ON project_memories(category);
CREATE INDEX IF NOT EXISTS idx_project_memories_created ON project_memories(created_at);
CREATE INDEX IF NOT EXISTS idx_memory_relations_source ON memory_relations(source_memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_relations_target ON memory_relations(target_memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_retrievals_project ON memory_retrievals(project_id);

-- ============================================================================
-- 说明
-- ============================================================================
-- 1. project_memories: 核心表，存储项目的所有记忆（本地+外部引用）
-- 2. memory_relations: 记忆之间的关系图谱
-- 3. memory_retrievals: 检索历史，用于优化推荐
-- 4. memory_stats: 项目记忆统计，Dashboard展示用
-- ============================================================================

