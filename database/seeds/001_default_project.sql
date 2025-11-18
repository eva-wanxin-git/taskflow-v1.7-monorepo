-- ============================================================================
-- Seed 001: 默认项目和组件数据
-- ============================================================================
-- 创建时间: 2025-11-18
-- 说明: 为任务所·Flow自身创建项目和组件记录
-- ============================================================================

-- 插入默认项目
INSERT OR IGNORE INTO projects (id, name, code, description, repo_url, status)
VALUES (
    'taskflow-main',
    '任务所·Flow',
    'TASKFLOW',
    'AI驱动的任务协作与进度监控系统',
    'https://github.com/eva-wanxin-git/taskflow-v1.5',
    'active'
);

-- 插入核心组件
INSERT OR IGNORE INTO components (id, project_id, name, type, description, repo_path, tech_stack)
VALUES
-- API服务
('taskflow-api', 'taskflow-main', 'API Service', 'backend',
 '后端API服务，提供RESTful接口', 'apps/api',
 '["Python", "FastAPI", "Uvicorn"]'),

-- Dashboard
('taskflow-dashboard', 'taskflow-main', 'Dashboard', 'frontend',
 'Web Dashboard监控面板', 'apps/dashboard',
 '["HTML", "CSS", "JavaScript"]'),

-- 核心领域
('taskflow-core-domain', 'taskflow-main', 'Core Domain', 'package',
 '领域模型和业务逻辑', 'packages/core-domain',
 '["Python", "DDD"]'),

-- 基础设施
('taskflow-infra', 'taskflow-main', 'Infrastructure', 'package',
 '基础设施封装（数据库、LLM等）', 'packages/infra',
 '["Python", "SQLite", "Claude API"]'),

-- 算法库
('taskflow-algorithms', 'taskflow-main', 'Algorithms', 'package',
 '依赖分析、关键路径等算法', 'packages/algorithms',
 '["Python", "Graph Theory", "CPM"]');

-- 插入常用工具
INSERT OR IGNORE INTO tools (id, name, type, description, documentation_url, version)
VALUES
('tool-fastapi', 'FastAPI', 'framework',
 '现代、高性能的Python Web框架', 'https://fastapi.tiangolo.com/', '0.104+'),

('tool-uvicorn', 'Uvicorn', 'server',
 'ASGI服务器', 'https://www.uvicorn.org/', '0.24+'),

('tool-sqlite', 'SQLite', 'database',
 '轻量级嵌入式数据库', 'https://www.sqlite.org/', '3.x'),

('tool-claude', 'Claude API', 'service',
 'Anthropic Claude AI服务', 'https://docs.anthropic.com/', '3.5 Sonnet'),

('tool-pyyaml', 'PyYAML', 'library',
 'YAML解析库', 'https://pyyaml.org/', '6.0+');

-- 关联组件和工具
INSERT OR IGNORE INTO component_tools (component_id, tool_id, purpose)
VALUES
('taskflow-api', 'tool-fastapi', 'Web框架'),
('taskflow-api', 'tool-uvicorn', '服务器'),
('taskflow-infra', 'tool-sqlite', '数据存储'),
('taskflow-infra', 'tool-claude', 'AI功能'),
('taskflow-core-domain', 'tool-pyyaml', '配置解析');

-- ============================================================================
-- 更新现有任务关联到默认项目
-- ============================================================================
-- 将所有现有任务（project_id为NULL的）关联到主项目
UPDATE tasks 
SET project_id = 'taskflow-main',
    component_id = 'taskflow-api'  -- 默认关联到API组件
WHERE project_id IS NULL;

-- ============================================================================
-- 说明
-- ============================================================================
-- 1. 使用 INSERT OR IGNORE 确保幂等性
-- 2. 默认创建了5个核心组件
-- 3. 预置了5个常用工具
-- 4. 现有任务自动关联到主项目
-- ============================================================================

