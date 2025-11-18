-- ============================================================================
-- Migration 002: 添加知识库表
-- ============================================================================
-- 创建时间: 2025-11-18
-- 说明: 新增projects, components, issues, solutions等知识库表
-- ============================================================================

-- 执行 v2_knowledge_schema.sql
-- 此文件包含9个新表: projects, components, issues, solutions, decisions,
--                  knowledge_articles, tools, component_tools, deployments

.read v2_knowledge_schema.sql

-- ============================================================================
-- 扩展现有tasks表，添加项目和组件关联
-- ============================================================================

-- 检查列是否已存在（SQLite不支持IF NOT EXISTS for ALTER TABLE）
-- 如果列已存在，ALTER TABLE会失败但不影响后续操作

-- 添加 project_id 列
ALTER TABLE tasks ADD COLUMN project_id TEXT REFERENCES projects(id);

-- 添加 component_id 列
ALTER TABLE tasks ADD COLUMN component_id TEXT REFERENCES components(id);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_component ON tasks(component_id);

-- ============================================================================
-- 说明
-- ============================================================================
-- 1. 现有任务的 project_id 和 component_id 初始为 NULL
-- 2. 后续通过数据迁移脚本将现有任务关联到默认项目
-- 3. 新创建的任务应该指定 project_id 和 component_id
-- ============================================================================

