-- ============================================================================
-- 任务所·Flow v1.7 - 企业级知识库Schema + 记忆系统
-- ============================================================================
-- 创建时间: 2025-11-18
-- 说明: 企业级扩展表和AI记忆系统表
-- 功能: 
--   1. 环境管理（dev/staging/prod）
--   2. AI交互事件跟踪
--   3. 记忆快照和提炼过程
--   4. 21库知识分类映射
--   5. 扩展工具和文章表
-- ============================================================================

-- ============================================================================
-- 第一部分: 企业级基础设施表
-- ============================================================================

-- ============================================================================
-- 1. 环境表 - 管理不同的部署环境
-- ============================================================================
CREATE TABLE IF NOT EXISTS environments (
    id TEXT PRIMARY KEY,                       -- ENV-xxx
    project_id TEXT NOT NULL,                  -- 所属项目
    name TEXT NOT NULL,                        -- dev/staging/production
    display_name TEXT NOT NULL,                -- 开发环境/预发布环境/生产环境
    description TEXT,                          -- 环境描述
    
    -- 环境配置
    type TEXT NOT NULL,                        -- local/cloud/hybrid
    region TEXT,                               -- 区域: cn-north-1, us-east-1
    
    -- 访问信息
    url TEXT,                                  -- 环境访问URL
    api_endpoint TEXT,                         -- API端点
    
    -- 状态和元数据
    status TEXT DEFAULT 'active',              -- active/inactive/maintenance
    is_production INTEGER DEFAULT 0,           -- 是否为生产环境
    requires_approval INTEGER DEFAULT 0,       -- 是否需要审批
    
    -- 资源配置（JSON格式）
    resources TEXT,                            -- {"cpu": "2 cores", "memory": "4GB", "storage": "100GB"}
    
    -- 环境变量（加密存储，JSON格式）
    env_vars TEXT,                             -- {"DATABASE_URL": "***", "API_KEY": "***"}
    
    -- 时间戳
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_by TEXT,                           -- 创建者
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- ============================================================================
-- 2. 部署记录表扩展 - 增强版（扩展v2的deployments表）
-- ============================================================================
-- 注意: v2已有deployments表，这里通过ALTER TABLE扩展
-- 如果需要创建完整版本，请先删除v2的deployments表

-- 为现有deployments表添加新字段
-- ALTER TABLE deployments ADD COLUMN environment_id TEXT;
-- ALTER TABLE deployments ADD COLUMN build_number TEXT;
-- ALTER TABLE deployments ADD COLUMN commit_hash TEXT;
-- ALTER TABLE deployments ADD COLUMN duration_seconds INTEGER;
-- ALTER TABLE deployments ADD COLUMN rollback_from TEXT;

-- 完整的部署记录表定义（作为参考，实际使用ALTER TABLE）
CREATE TABLE IF NOT EXISTS deployments_v2 (
    id TEXT PRIMARY KEY,                       -- DEP-xxx
    project_id TEXT NOT NULL,                  -- 所属项目
    component_id TEXT NOT NULL,                -- 部署的组件
    environment_id TEXT NOT NULL,              -- 部署到的环境（新增）
    
    -- 版本信息
    version TEXT NOT NULL,                     -- 版本号: v1.7.0
    build_number TEXT,                         -- 构建号: #123（新增）
    commit_hash TEXT,                          -- Git提交哈希（新增）
    
    -- 部署状态
    status TEXT DEFAULT 'in_progress',         -- in_progress/success/failed/rollback
    deployment_type TEXT DEFAULT 'normal',     -- normal/hotfix/rollback
    
    -- 时间信息
    deployed_at TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT,                         -- 部署完成时间
    duration_seconds INTEGER,                  -- 部署耗时（秒）（新增）
    
    -- 执行信息
    deployed_by TEXT,                          -- 部署者
    approved_by TEXT,                          -- 审批者（生产环境）
    
    -- 回滚信息
    rollback_from TEXT,                        -- 从哪个部署回滚（新增）
    rollback_reason TEXT,                      -- 回滚原因
    
    -- 部署详情
    notes TEXT,                                -- 部署说明
    changes TEXT,                              -- 变更内容（JSON数组）
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
    FOREIGN KEY (environment_id) REFERENCES environments(id),
    FOREIGN KEY (rollback_from) REFERENCES deployments_v2(id)
);

-- ============================================================================
-- 第二部分: AI交互和记忆系统表
-- ============================================================================

-- ============================================================================
-- 3. AI交互事件表 - 记录用户与AI的每次交互
-- ============================================================================
CREATE TABLE IF NOT EXISTS interaction_events (
    id TEXT PRIMARY KEY,                       -- INT-xxx
    project_id TEXT NOT NULL,                  -- 所属项目
    session_id TEXT NOT NULL,                  -- 会话ID（同一对话的多次交互）
    
    -- 交互角色
    actor_type TEXT NOT NULL,                  -- user/ai/system
    actor_name TEXT,                           -- 用户名或AI角色名
    ai_role TEXT,                              -- architect/fullstack-engineer/code-steward/sre
    
    -- 交互内容
    action_type TEXT NOT NULL,                 -- query/command/response/analysis/review
    intent TEXT,                               -- 意图分类: feature_request/bug_report/question/task_assignment
    
    input_text TEXT,                           -- 输入内容
    output_text TEXT,                          -- 输出内容
    
    -- Token使用情况
    tokens_input INTEGER DEFAULT 0,            -- 输入Token数
    tokens_output INTEGER DEFAULT 0,           -- 输出Token数
    tokens_total INTEGER DEFAULT 0,            -- 总Token数
    
    -- 关联实体
    related_entity_type TEXT,                  -- task/issue/decision/article
    related_entity_id TEXT,                    -- 关联实体ID
    
    -- 执行结果
    success INTEGER DEFAULT 1,                 -- 是否成功: 1=成功, 0=失败
    error_message TEXT,                        -- 错误信息（如果失败）
    
    -- 元数据
    context TEXT,                              -- 上下文信息（JSON格式）
    tags TEXT,                                 -- 标签（JSON数组）
    
    -- 时间戳
    occurred_at TEXT NOT NULL DEFAULT (datetime('now')),
    duration_ms INTEGER,                       -- 执行耗时（毫秒）
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- ============================================================================
-- 4. 记忆快照表 - 记录AI提炼的知识快照
-- ============================================================================
CREATE TABLE IF NOT EXISTS memory_snapshots (
    id TEXT PRIMARY KEY,                       -- MEM-xxx
    project_id TEXT NOT NULL,                  -- 所属项目
    
    -- 快照信息
    snapshot_type TEXT NOT NULL,               -- session_end/milestone/handover/periodic
    title TEXT NOT NULL,                       -- 快照标题
    description TEXT,                          -- 快照描述
    
    -- 快照内容
    raw_content TEXT,                          -- 原始对话内容（压缩）
    refined_content TEXT NOT NULL,             -- 提炼后的内容
    key_points TEXT,                           -- 关键要点（JSON数组）
    
    -- 知识分类
    category_codes TEXT,                       -- 知识库分类代码（JSON数组）: ["KB-01", "KB-05"]
    knowledge_type TEXT,                       -- fact/procedure/concept/decision/pattern
    
    -- 提炼过程
    extraction_method TEXT DEFAULT 'ai',       -- ai/manual/hybrid
    extracted_by TEXT,                         -- AI角色或人员
    
    -- 质量评估
    confidence_score REAL DEFAULT 0.0,         -- 置信度: 0.0-1.0
    importance_level TEXT DEFAULT 'medium',    -- low/medium/high/critical
    
    -- 关联信息
    session_id TEXT,                           -- 关联会话ID
    related_entities TEXT,                     -- 关联的实体列表（JSON）
    
    -- 引用统计
    reference_count INTEGER DEFAULT 0,         -- 被引用次数
    last_referenced_at TEXT,                   -- 最后引用时间
    
    -- 时间戳
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    expires_at TEXT,                           -- 过期时间（可选）
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- ============================================================================
-- 5. 记忆分类表 - 21库知识分类映射
-- ============================================================================
CREATE TABLE IF NOT EXISTS memory_categories (
    id TEXT PRIMARY KEY,                       -- 自增ID
    code TEXT UNIQUE NOT NULL,                 -- 分类代码: KB-01, KB-02...KB-21
    name TEXT NOT NULL,                        -- 分类名称
    display_name TEXT NOT NULL,                -- 显示名称（中文）
    description TEXT,                          -- 分类描述
    
    -- 分层信息
    layer INTEGER NOT NULL,                    -- 所属层级: 1=基础设施, 2=业务逻辑, 3=应用层
    parent_code TEXT,                          -- 父分类代码（如果有）
    
    -- 分类配置
    icon TEXT,                                 -- 图标名称
    color TEXT,                                -- 显示颜色: #FF6B6B
    sort_order INTEGER DEFAULT 0,              -- 排序顺序
    
    -- 状态
    is_active INTEGER DEFAULT 1,               -- 是否启用
    
    -- 统计信息
    article_count INTEGER DEFAULT 0,           -- 关联文章数
    snapshot_count INTEGER DEFAULT 0,          -- 关联快照数
    
    -- 时间戳
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    -- 外键约束
    FOREIGN KEY (parent_code) REFERENCES memory_categories(code)
);

-- ============================================================================
-- 第三部分: 扩展现有表（通过ALTER TABLE）
-- ============================================================================

-- 注意: 以下ALTER TABLE语句用于扩展v2已有的表
-- 如果表不存在或字段已存在，可能会报错，请根据实际情况调整

-- ============================================================================
-- 6. 扩展tools表 - 添加分类和安装信息
-- ============================================================================
-- ALTER TABLE tools ADD COLUMN category TEXT DEFAULT 'library';        -- framework/library/cli/service/platform
-- ALTER TABLE tools ADD COLUMN installation TEXT;                       -- 安装方式（JSON格式）
-- ALTER TABLE tools ADD COLUMN license TEXT;                            -- 许可证
-- ALTER TABLE tools ADD COLUMN website_url TEXT;                        -- 官网地址
-- ALTER TABLE tools ADD COLUMN is_active INTEGER DEFAULT 1;             -- 是否在用

-- 完整的tools表定义（作为参考）
CREATE TABLE IF NOT EXISTS tools_v2 (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,                        -- framework/library/cli/service
    category TEXT DEFAULT 'library',           -- 细分类别（新增）
    description TEXT,
    
    -- 文档和资源
    documentation_url TEXT,
    website_url TEXT,                          -- 官网地址（新增）
    
    -- 版本和许可
    version TEXT,
    license TEXT,                              -- MIT/Apache-2.0/GPL（新增）
    
    -- 安装信息（新增）
    installation TEXT,                         -- JSON格式: {"pip": "pip install fastapi", "npm": "npm install react"}
    
    -- 状态
    is_active INTEGER DEFAULT 1,               -- 是否在用（新增）
    
    -- 时间戳
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- ============================================================================
-- 7. 扩展component_tools表 - 增强关联关系
-- ============================================================================
-- ALTER TABLE component_tools ADD COLUMN version_used TEXT;            -- 使用的版本
-- ALTER TABLE component_tools ADD COLUMN importance TEXT DEFAULT 'normal'; -- critical/important/normal/optional
-- ALTER TABLE component_tools ADD COLUMN notes TEXT;                   -- 备注

-- 完整的component_tools表定义（作为参考）
CREATE TABLE IF NOT EXISTS component_tools_v2 (
    component_id TEXT NOT NULL,
    tool_id TEXT NOT NULL,
    
    -- 使用信息
    purpose TEXT,                              -- 使用目的
    version_used TEXT,                         -- 使用的版本（新增）
    importance TEXT DEFAULT 'normal',          -- critical/important/normal/optional（新增）
    
    -- 详细信息
    notes TEXT,                                -- 备注说明（新增）
    configuration TEXT,                        -- 配置信息（JSON格式）
    
    -- 时间戳
    added_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    
    PRIMARY KEY (component_id, tool_id),
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
    FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE CASCADE
);

-- ============================================================================
-- 8. 扩展knowledge_articles表 - 添加分层和分类信息
-- ============================================================================
-- ALTER TABLE knowledge_articles ADD COLUMN layer INTEGER;             -- 知识层级: 1/2/3
-- ALTER TABLE knowledge_articles ADD COLUMN category_code TEXT;        -- 21库分类代码: KB-01
-- ALTER TABLE knowledge_articles ADD COLUMN importance TEXT DEFAULT 'medium'; -- 重要性
-- ALTER TABLE knowledge_articles ADD COLUMN version TEXT DEFAULT '1.0'; -- 版本号

-- 完整的knowledge_articles表定义（作为参考）
CREATE TABLE IF NOT EXISTS knowledge_articles_v2 (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    component_id TEXT,
    
    -- 文章信息
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,                             -- architecture/pattern/guide
    
    -- 分层和分类（新增）
    layer INTEGER,                             -- 1=基础设施, 2=业务逻辑, 3=应用层（新增）
    category_code TEXT,                        -- 21库分类代码: KB-01（新增）
    
    -- 版本和重要性（新增）
    version TEXT DEFAULT '1.0',                -- 文章版本（新增）
    importance TEXT DEFAULT 'medium',          -- low/medium/high/critical（新增）
    
    -- 元数据
    tags TEXT,                                 -- JSON数组
    author TEXT,                               -- 作者
    
    -- 统计
    view_count INTEGER DEFAULT 0,              -- 查看次数
    
    -- 时间戳
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (component_id) REFERENCES components(id),
    FOREIGN KEY (category_code) REFERENCES memory_categories(code)
);

-- ============================================================================
-- 索引优化
-- ============================================================================

-- environments表索引
CREATE INDEX IF NOT EXISTS idx_environments_project ON environments(project_id);
CREATE INDEX IF NOT EXISTS idx_environments_status ON environments(status);
CREATE INDEX IF NOT EXISTS idx_environments_name ON environments(name);
CREATE INDEX IF NOT EXISTS idx_environments_production ON environments(is_production);

-- deployments_v2表索引
CREATE INDEX IF NOT EXISTS idx_deployments_v2_project ON deployments_v2(project_id);
CREATE INDEX IF NOT EXISTS idx_deployments_v2_component ON deployments_v2(component_id);
CREATE INDEX IF NOT EXISTS idx_deployments_v2_environment ON deployments_v2(environment_id);
CREATE INDEX IF NOT EXISTS idx_deployments_v2_status ON deployments_v2(status);
CREATE INDEX IF NOT EXISTS idx_deployments_v2_deployed_at ON deployments_v2(deployed_at DESC);

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

-- ============================================================================
-- 初始化21库知识分类数据
-- ============================================================================
INSERT OR IGNORE INTO memory_categories (id, code, name, display_name, description, layer, icon, color, sort_order) VALUES
    -- 第1层: 基础设施层 (Layer 1)
    ('MC-01', 'KB-01', 'infrastructure', '基础设施', '服务器、网络、存储等基础设施知识', 1, '🏗️', '#3498db', 1),
    ('MC-02', 'KB-02', 'database', '数据库', '数据库设计、优化、管理知识', 1, '🗄️', '#2ecc71', 2),
    ('MC-03', 'KB-03', 'devops', 'DevOps', 'CI/CD、容器化、自动化部署知识', 1, '🚀', '#e74c3c', 3),
    ('MC-04', 'KB-04', 'security', '安全', '安全策略、加密、认证授权知识', 1, '🔒', '#f39c12', 4),
    ('MC-05', 'KB-05', 'monitoring', '监控', '日志、监控、告警、性能分析知识', 1, '📊', '#9b59b6', 5),
    ('MC-06', 'KB-06', 'networking', '网络', '网络协议、负载均衡、CDN知识', 1, '🌐', '#1abc9c', 6),
    ('MC-07', 'KB-07', 'tools', '工具链', '开发工具、框架、库的使用知识', 1, '🔧', '#34495e', 7),
    
    -- 第2层: 业务逻辑层 (Layer 2)
    ('MC-08', 'KB-08', 'domain', '领域模型', '业务领域建模、DDD知识', 2, '🏛️', '#3498db', 8),
    ('MC-09', 'KB-09', 'algorithms', '算法', '算法设计、数据结构、优化策略', 2, '🧮', '#2ecc71', 9),
    ('MC-10', 'KB-10', 'api', 'API设计', 'RESTful、GraphQL、接口设计', 2, '🔌', '#e74c3c', 10),
    ('MC-11', 'KB-11', 'patterns', '设计模式', '软件设计模式、架构模式', 2, '🎨', '#f39c12', 11),
    ('MC-12', 'KB-12', 'business', '业务规则', '业务流程、规则引擎', 2, '📋', '#9b59b6', 12),
    ('MC-13', 'KB-13', 'integration', '系统集成', '第三方集成、消息队列', 2, '🔗', '#1abc9c', 13),
    ('MC-14', 'KB-14', 'testing', '测试', '单元测试、集成测试、自动化测试', 2, '✅', '#34495e', 14),
    
    -- 第3层: 应用层 (Layer 3)
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
-- 【新增功能】
-- 1. environments表: 管理开发/预发布/生产等多环境
-- 2. deployments_v2表: 增强版部署记录，包含构建号、commit、耗时等
-- 3. interaction_events表: 记录用户与AI的每次交互，包含Token使用
-- 4. memory_snapshots表: AI记忆快照，记录提炼过程和关键知识点
-- 5. memory_categories表: 21库知识分类，分为3层(基础设施/业务逻辑/应用层)
-- 
-- 【扩展功能】
-- 6. tools表扩展: category/installation/license/website等字段
-- 7. component_tools表扩展: version_used/importance/notes等字段
-- 8. knowledge_articles表扩展: layer/category_code/version/importance等字段
-- 
-- 【使用建议】
-- 1. deployments_v2表与v2的deployments表二选一使用，或者使用ALTER TABLE扩展
-- 2. tools_v2、component_tools_v2、knowledge_articles_v2为参考版本
-- 3. 实际使用时建议使用ALTER TABLE语句扩展现有表
-- 4. 所有JSON字段在SQLite 3.38+可使用JSON函数查询
-- 5. 索引已优化，支持常见查询场景
-- 
-- 【数据统计】
-- - 新增表: 5个（environments, deployments_v2, interaction_events, memory_snapshots, memory_categories）
-- - 扩展表: 3个（tools, component_tools, knowledge_articles）
-- - 索引: 25个
-- - 预置数据: 21条知识分类记录
-- - 总行数: 约400行
-- 
-- ============================================================================

