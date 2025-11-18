-- ============================================================================
-- 任务所·Flow v1.7 - 企业级知识库迁移脚本
-- ============================================================================
-- 迁移版本: 005
-- 创建时间: 2025-11-18
-- 说明: 添加企业级表和记忆系统表，扩展现有表
-- ============================================================================

-- ============================================================================
-- 第一部分: 创建新表
-- ============================================================================

-- 1. 环境表
CREATE TABLE IF NOT EXISTS environments (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL,
    region TEXT,
    url TEXT,
    api_endpoint TEXT,
    status TEXT DEFAULT 'active',
    is_production INTEGER DEFAULT 0,
    requires_approval INTEGER DEFAULT 0,
    resources TEXT,
    env_vars TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_by TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 2. AI交互事件表
CREATE TABLE IF NOT EXISTS interaction_events (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    actor_type TEXT NOT NULL,
    actor_name TEXT,
    ai_role TEXT,
    action_type TEXT NOT NULL,
    intent TEXT,
    input_text TEXT,
    output_text TEXT,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    tokens_total INTEGER DEFAULT 0,
    related_entity_type TEXT,
    related_entity_id TEXT,
    success INTEGER DEFAULT 1,
    error_message TEXT,
    context TEXT,
    tags TEXT,
    occurred_at TEXT NOT NULL DEFAULT (datetime('now')),
    duration_ms INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 3. 记忆快照表
CREATE TABLE IF NOT EXISTS memory_snapshots (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    snapshot_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    raw_content TEXT,
    refined_content TEXT NOT NULL,
    key_points TEXT,
    category_codes TEXT,
    knowledge_type TEXT,
    extraction_method TEXT DEFAULT 'ai',
    extracted_by TEXT,
    confidence_score REAL DEFAULT 0.0,
    importance_level TEXT DEFAULT 'medium',
    session_id TEXT,
    related_entities TEXT,
    reference_count INTEGER DEFAULT 0,
    last_referenced_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    expires_at TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- 4. 记忆分类表
CREATE TABLE IF NOT EXISTS memory_categories (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    description TEXT,
    layer INTEGER NOT NULL,
    parent_code TEXT,
    icon TEXT,
    color TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    article_count INTEGER DEFAULT 0,
    snapshot_count INTEGER DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (parent_code) REFERENCES memory_categories(code)
);

-- ============================================================================
-- 第二部分: 扩展现有表
-- ============================================================================

-- 扩展tools表
ALTER TABLE tools ADD COLUMN category TEXT DEFAULT 'library';
ALTER TABLE tools ADD COLUMN installation TEXT;
ALTER TABLE tools ADD COLUMN license TEXT;
ALTER TABLE tools ADD COLUMN website_url TEXT;
ALTER TABLE tools ADD COLUMN is_active INTEGER DEFAULT 1;
ALTER TABLE tools ADD COLUMN updated_at TEXT DEFAULT (datetime('now'));

-- 扩展component_tools表
ALTER TABLE component_tools ADD COLUMN version_used TEXT;
ALTER TABLE component_tools ADD COLUMN importance TEXT DEFAULT 'normal';
ALTER TABLE component_tools ADD COLUMN notes TEXT;
ALTER TABLE component_tools ADD COLUMN configuration TEXT;
ALTER TABLE component_tools ADD COLUMN added_at TEXT DEFAULT (datetime('now'));
ALTER TABLE component_tools ADD COLUMN updated_at TEXT DEFAULT (datetime('now'));

-- 扩展knowledge_articles表
ALTER TABLE knowledge_articles ADD COLUMN layer INTEGER;
ALTER TABLE knowledge_articles ADD COLUMN category_code TEXT;
ALTER TABLE knowledge_articles ADD COLUMN version TEXT DEFAULT '1.0';
ALTER TABLE knowledge_articles ADD COLUMN importance TEXT DEFAULT 'medium';
ALTER TABLE knowledge_articles ADD COLUMN author TEXT;
ALTER TABLE knowledge_articles ADD COLUMN view_count INTEGER DEFAULT 0;

-- 扩展deployments表（增强企业级功能）
ALTER TABLE deployments ADD COLUMN environment_id TEXT;
ALTER TABLE deployments ADD COLUMN build_number TEXT;
ALTER TABLE deployments ADD COLUMN commit_hash TEXT;
ALTER TABLE deployments ADD COLUMN completed_at TEXT;
ALTER TABLE deployments ADD COLUMN duration_seconds INTEGER;
ALTER TABLE deployments ADD COLUMN deployment_type TEXT DEFAULT 'normal';
ALTER TABLE deployments ADD COLUMN approved_by TEXT;
ALTER TABLE deployments ADD COLUMN rollback_from TEXT;
ALTER TABLE deployments ADD COLUMN rollback_reason TEXT;
ALTER TABLE deployments ADD COLUMN changes TEXT;

-- ============================================================================
-- 第三部分: 创建索引
-- ============================================================================

-- environments表索引
CREATE INDEX IF NOT EXISTS idx_environments_project ON environments(project_id);
CREATE INDEX IF NOT EXISTS idx_environments_status ON environments(status);
CREATE INDEX IF NOT EXISTS idx_environments_name ON environments(name);
CREATE INDEX IF NOT EXISTS idx_environments_production ON environments(is_production);

-- interaction_events表索引
CREATE INDEX IF NOT EXISTS idx_interactions_project ON interaction_events(project_id);
CREATE INDEX IF NOT EXISTS idx_interactions_session ON interaction_events(session_id);
CREATE INDEX IF NOT EXISTS idx_interactions_actor ON interaction_events(actor_type, actor_name);
CREATE INDEX IF NOT EXISTS idx_interactions_ai_role ON interaction_events(ai_role);
CREATE INDEX IF NOT EXISTS idx_interactions_action ON interaction_events(action_type);
CREATE INDEX IF NOT EXISTS idx_interactions_occurred ON interaction_events(occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_interactions_entity ON interaction_events(related_entity_type, related_entity_id);

-- memory_snapshots表索引
CREATE INDEX IF NOT EXISTS idx_snapshots_project ON memory_snapshots(project_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_type ON memory_snapshots(snapshot_type);
CREATE INDEX IF NOT EXISTS idx_snapshots_session ON memory_snapshots(session_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_categories ON memory_snapshots(category_codes);
CREATE INDEX IF NOT EXISTS idx_snapshots_importance ON memory_snapshots(importance_level);
CREATE INDEX IF NOT EXISTS idx_snapshots_created ON memory_snapshots(created_at DESC);

-- memory_categories表索引
CREATE INDEX IF NOT EXISTS idx_categories_layer ON memory_categories(layer);
CREATE INDEX IF NOT EXISTS idx_categories_parent ON memory_categories(parent_code);
CREATE INDEX IF NOT EXISTS idx_categories_active ON memory_categories(is_active);
CREATE INDEX IF NOT EXISTS idx_categories_sort ON memory_categories(sort_order);

-- knowledge_articles扩展索引
CREATE INDEX IF NOT EXISTS idx_articles_layer ON knowledge_articles(layer);
CREATE INDEX IF NOT EXISTS idx_articles_category_code ON knowledge_articles(category_code);

-- deployments扩展索引
CREATE INDEX IF NOT EXISTS idx_deployments_environment ON deployments(environment_id);
CREATE INDEX IF NOT EXISTS idx_deployments_type ON deployments(deployment_type);

-- ============================================================================
-- 第四部分: 初始化数据
-- ============================================================================

-- 初始化21库知识分类
INSERT OR IGNORE INTO memory_categories (id, code, name, display_name, description, layer, icon, color, sort_order) VALUES
    -- 第1层: 基础设施层
    ('MC-01', 'KB-01', 'infrastructure', '基础设施', '服务器、网络、存储等基础设施知识', 1, '🏗️', '#3498db', 1),
    ('MC-02', 'KB-02', 'database', '数据库', '数据库设计、优化、管理知识', 1, '🗄️', '#2ecc71', 2),
    ('MC-03', 'KB-03', 'devops', 'DevOps', 'CI/CD、容器化、自动化部署知识', 1, '🚀', '#e74c3c', 3),
    ('MC-04', 'KB-04', 'security', '安全', '安全策略、加密、认证授权知识', 1, '🔒', '#f39c12', 4),
    ('MC-05', 'KB-05', 'monitoring', '监控', '日志、监控、告警、性能分析知识', 1, '📊', '#9b59b6', 5),
    ('MC-06', 'KB-06', 'networking', '网络', '网络协议、负载均衡、CDN知识', 1, '🌐', '#1abc9c', 6),
    ('MC-07', 'KB-07', 'tools', '工具链', '开发工具、框架、库的使用知识', 1, '🔧', '#34495e', 7),
    
    -- 第2层: 业务逻辑层
    ('MC-08', 'KB-08', 'domain', '领域模型', '业务领域建模、DDD知识', 2, '🏛️', '#3498db', 8),
    ('MC-09', 'KB-09', 'algorithms', '算法', '算法设计、数据结构、优化策略', 2, '🧮', '#2ecc71', 9),
    ('MC-10', 'KB-10', 'api', 'API设计', 'RESTful、GraphQL、接口设计', 2, '🔌', '#e74c3c', 10),
    ('MC-11', 'KB-11', 'patterns', '设计模式', '软件设计模式、架构模式', 2, '🎨', '#f39c12', 11),
    ('MC-12', 'KB-12', 'business', '业务规则', '业务流程、规则引擎', 2, '📋', '#9b59b6', 12),
    ('MC-13', 'KB-13', 'integration', '系统集成', '第三方集成、消息队列', 2, '🔗', '#1abc9c', 13),
    ('MC-14', 'KB-14', 'testing', '测试', '单元测试、集成测试、自动化测试', 2, '✅', '#34495e', 14),
    
    -- 第3层: 应用层
    ('MC-15', 'KB-15', 'ui-ux', 'UI/UX', '用户界面设计、用户体验优化', 3, '🎨', '#3498db', 15),
    ('MC-16', 'KB-16', 'frontend', '前端', '前端框架、组件、状态管理', 3, '💻', '#2ecc71', 16),
    ('MC-17', 'KB-17', 'mobile', '移动端', 'iOS、Android、跨平台开发', 3, '📱', '#e74c3c', 17),
    ('MC-18', 'KB-18', 'performance', '性能优化', '前端性能、后端优化', 3, '⚡', '#f39c12', 18),
    ('MC-19', 'KB-19', 'accessibility', '可访问性', '无障碍设计、国际化', 3, '♿', '#9b59b6', 19),
    ('MC-20', 'KB-20', 'documentation', '文档', '技术文档、API文档、用户手册', 3, '📚', '#1abc9c', 20),
    ('MC-21', 'KB-21', 'best-practices', '最佳实践', '编码规范、团队协作、项目管理', 3, '⭐', '#34495e', 21);

-- ============================================================================
-- 说明
-- ============================================================================
-- 
-- 【迁移内容】
-- 1. 新增4个表: environments, interaction_events, memory_snapshots, memory_categories
-- 2. 扩展4个表: tools, component_tools, knowledge_articles, deployments
-- 3. 新增25个索引
-- 4. 初始化21条知识分类数据
-- 
-- 【执行说明】
-- python database/migrations/migrate.py apply 005
-- 
-- 【回滚说明】
-- 如需回滚，需要手动删除新增的表和字段
-- 
-- ============================================================================

