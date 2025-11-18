# 测试用例库

## v1.7核心功能测试

### 1. 端口管理器测试
**文件**: packages/shared-utils/port_manager.py
**用例**:
- 测试分配新端口
- 测试查询已分配端口
- 测试端口冲突检测
- 测试端口释放

### 2. 数据库迁移测试
**文件**: database/migrations/migrate.py
**用例**:
- 测试init命令
- 测试status命令
- 测试seed命令
- 测试backup命令

### 3. StateManager测试
**文件**: apps/dashboard/src/automation/state_manager.py
**用例**:
- 测试list_all_tasks()
- 测试create_task()
- 测试update_task()
- 测试get_task()

### 4. ArchitectOrchestrator测试
**文件**: apps/api/src/services/architect_orchestrator.py
**用例**:
- 测试process_analysis()
- 测试process_handover()
- 测试任务看板生成

## 测试状态

### 已有测试
- ✅ test_knowledge_db.py - 知识库数据库测试
- ✅ check_db.py - 数据库检查
- ✅ test_dashboard_data.py - Dashboard数据读取测试

### 缺失测试
- ❌ API端点测试
- ❌ 单元测试
- ❌ E2E测试

**优先级**: P0 - 需要TASK-C-3补充
