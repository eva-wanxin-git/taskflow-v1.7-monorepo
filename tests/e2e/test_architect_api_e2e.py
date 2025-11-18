# -*- coding: utf-8 -*-
"""
架构师API端到端测试

测试架构师API的完整工作流：
1. 提交架构分析 -> 生成任务和文档
2. 查询项目摘要
3. 提交交接快照
4. 查询最新快照
5. 服务状态检查
6. 查询架构任务

依赖: FastAPI, pytest, httpx
运行: pytest tests/e2e/test_architect_api_e2e.py -v
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# 尝试导入FastAPI测试客户端
try:
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    TestClient = None
    FastAPI = None

# 导入架构师路由和服务
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "apps" / "api" / "src"))

try:
    from routes.architect import router, _orchestrator, get_orchestrator
    from services.architect_orchestrator import (
        ArchitectOrchestrator,
        ArchitectAnalysis,
        FeatureSummary,
        PartialFeatureSummary,
        ProblemSummary,
        ArchitectTaskSuggestion,
        HandoverSnapshot
    )
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    print(f"Warning: Cannot import modules: {e}")


# ============================================================================
# 测试配置和Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def check_dependencies():
    """检查测试依赖是否可用"""
    if not FASTAPI_AVAILABLE:
        pytest.skip("FastAPI not installed. Run: pip install fastapi httpx")
    if not MODULES_AVAILABLE:
        pytest.skip("Architect modules not available")


@pytest.fixture(scope="function")
def temp_docs_dir():
    """创建临时文档目录"""
    temp_dir = tempfile.mkdtemp(prefix="taskflow_test_")
    docs_path = Path(temp_dir) / "docs"
    docs_path.mkdir(parents=True)
    
    yield docs_path
    
    # 清理
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def mock_orchestrator(temp_docs_dir):
    """创建Mock编排器（不依赖数据库）"""
    return ArchitectOrchestrator(
        state_manager=None,  # Mock模式，不连接数据库
        docs_root=str(temp_docs_dir)
    )


@pytest.fixture(scope="function")
def test_app(mock_orchestrator):
    """创建测试用FastAPI应用"""
    if not FASTAPI_AVAILABLE:
        pytest.skip("FastAPI not available")
    
    app = FastAPI(title="Taskflow API - Test")
    app.include_router(router)
    
    # 注入Mock编排器
    global _orchestrator
    _orchestrator = mock_orchestrator
    
    return app


@pytest.fixture(scope="function")
def client(test_app):
    """创建测试客户端"""
    return TestClient(test_app)


@pytest.fixture(scope="function")
def sample_analysis():
    """样例架构分析数据"""
    return ArchitectAnalysis(
        project_code="TEST_PROJECT",
        repo_root="/path/to/repo",
        completed_features=[
            FeatureSummary(
                title="用户认证系统",
                description="完整的JWT认证流程",
                related_paths=["src/auth/jwt.py", "src/auth/middleware.py"],
                completion=1.0,
                notes="已包含刷新token和注销功能"
            ),
            FeatureSummary(
                title="任务CRUD API",
                description="任务的增删改查REST API",
                related_paths=["src/api/tasks.py"],
                completion=1.0
            )
        ],
        partial_features=[
            PartialFeatureSummary(
                title="实时通知系统",
                description="WebSocket实时推送",
                related_paths=["src/websocket/notifications.py"],
                completion=0.6,
                missing=["重连机制", "消息持久化", "错误处理"],
                risk="生产环境可能不稳定",
                priority="high"
            )
        ],
        problems=[
            ProblemSummary(
                title="数据库连接池未配置",
                description="当前使用默认连接，高并发下会耗尽连接",
                severity="high",
                related_paths=["src/database/engine.py"],
                impact="高负载下性能下降严重",
                suggested_solution="配置连接池大小和超时参数"
            ),
            ProblemSummary(
                title="缺少API限流",
                description="所有端点都没有速率限制",
                severity="medium",
                related_paths=["src/api/main.py"],
                impact="容易被滥用或DDoS攻击",
                suggested_solution="使用slowapi或自定义中间件"
            )
        ],
        suggested_tasks=[
            ArchitectTaskSuggestion(
                id="ARCH-001",
                title="配置数据库连接池",
                type="backend",
                priority="critical",
                component="infra-database",
                description="为SQLAlchemy配置连接池参数",
                related_paths=["src/database/engine.py"],
                acceptance_criteria=[
                    "pool_size设置为20",
                    "max_overflow设置为10",
                    "pool_timeout设置为30秒",
                    "添加连接池监控日志"
                ],
                estimated_hours=2.0,
                executor_type="code-steward",
                dependencies=[]
            ),
            ArchitectTaskSuggestion(
                id="ARCH-002",
                title="实现API限流中间件",
                type="backend",
                priority="high",
                component="api-middleware",
                description="为所有API端点添加速率限制",
                related_paths=["src/api/middleware.py"],
                acceptance_criteria=[
                    "全局限流：100 req/min",
                    "用户限流：50 req/min",
                    "返回429状态码和Retry-After头"
                ],
                estimated_hours=4.0,
                executor_type="code-steward",
                dependencies=[]
            ),
            ArchitectTaskSuggestion(
                id="ARCH-003",
                title="完善WebSocket重连机制",
                type="frontend",
                priority="high",
                component="frontend-websocket",
                description="实现客户端自动重连和指数退避",
                related_paths=["src/websocket/client.ts"],
                acceptance_criteria=[
                    "断线后自动重连",
                    "指数退避：1s, 2s, 4s, 8s",
                    "最多重试5次",
                    "重连成功后恢复订阅"
                ],
                estimated_hours=3.0,
                executor_type="code-steward",
                dependencies=[]
            )
        ],
        metadata={
            "analysis_duration_minutes": 15,
            "files_analyzed": 42,
            "architect_version": "v2.0"
        }
    )


@pytest.fixture(scope="function")
def sample_handover():
    """样例交接快照"""
    return HandoverSnapshot(
        snapshot_id="handover-20251118-001",
        project_code="TEST_PROJECT",
        architect="AI Architect v2.0",
        completed_phases=[
            {
                "phase": "Phase 1: 代码库扫描",
                "progress": 100,
                "duration_minutes": 15
            },
            {
                "phase": "Phase 2: 架构分析",
                "progress": 100,
                "duration_minutes": 20
            }
        ],
        current_focus={
            "area": "任务拆解与优先级排序",
            "status": "completed",
            "next": "等待代码管家认领任务"
        },
        key_files_analyzed=[
            {"path": "src/auth/jwt.py", "importance": "high", "notes": "认证核心"},
            {"path": "src/api/tasks.py", "importance": "high", "notes": "任务API"},
            {"path": "src/database/engine.py", "importance": "critical", "notes": "需配置连接池"}
        ],
        unanalyzed_areas=[
            "tests/ 目录（测试覆盖率未分析）",
            "scripts/ 目录（运维脚本）"
        ],
        recommendations_for_next=[
            "优先完成ARCH-001（数据库连接池）- P0任务",
            "然后并行处理ARCH-002和ARCH-003",
            "分析测试覆盖率（当前未知）",
            "审查运维脚本的安全性"
        ],
        token_usage={
            "input_tokens": 125000,
            "output_tokens": 8500,
            "total_cost_usd": 0.45
        }
    )


# ============================================================================
# E2E测试用例
# ============================================================================

class TestArchitectAPIEndpoints:
    """测试架构师API的所有端点"""
    
    def test_service_status(self, client, check_dependencies):
        """测试1: 获取服务状态（健康检查）"""
        response = client.get("/api/architect/status")
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证响应结构
        assert data["status"] == "healthy"
        assert "version" in data
        assert "features" in data
        assert "endpoints" in data
        assert "timestamp" in data
        
        # 验证功能标志
        features = data["features"]
        assert features["analysis_submission"] is True
        assert features["handover_snapshot"] is True
        assert features["project_summary"] is True
        assert features["task_board_generation"] is True
        
        print(f"✅ 服务状态正常: {data['version']}")
    
    def test_submit_analysis_success(self, client, sample_analysis, temp_docs_dir, check_dependencies):
        """测试2: 成功提交架构分析"""
        response = client.post(
            "/api/architect/analysis",
            json=sample_analysis.dict()
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证响应
        assert data["success"] is True
        assert "tasks_created" in data
        assert "issues_created" in data
        assert "articles_created" in data
        assert "task_board_url" in data
        assert "timestamp" in data
        
        # 验证创建的资源数量（Mock模式下是模拟的计数）
        # 实际集成后应该从数据库验证
        print(f"✅ 分析提交成功:")
        print(f"   - 任务创建: {data.get('tasks_created', 0)}")
        print(f"   - 问题记录: {data.get('issues_created', 0)}")
        print(f"   - 文章创建: {data.get('articles_created', 0)}")
        
        # 验证task-board.md文件已生成
        task_board_path = temp_docs_dir / "tasks" / "task-board.md"
        assert task_board_path.exists(), "task-board.md应该已生成"
        
        # 验证文件内容
        content = task_board_path.read_text(encoding='utf-8')
        assert "TEST_PROJECT" in content
        assert "ARCH-001" in content
        assert "ARCH-002" in content
        assert "ARCH-003" in content
        assert "数据库连接池" in content
        
        print(f"✅ 任务看板已生成: {task_board_path}")
    
    def test_submit_analysis_invalid_data(self, client, check_dependencies):
        """测试3: 提交无效数据（验证输入校验）"""
        invalid_data = {
            "project_code": "",  # 空项目代码
            "suggested_tasks": []
        }
        
        response = client.post(
            "/api/architect/analysis",
            json=invalid_data
        )
        
        # 应该返回422（验证错误）
        assert response.status_code == 422
        print("✅ 输入校验正常工作")
    
    def test_get_project_summary(self, client, check_dependencies):
        """测试4: 获取项目摘要"""
        project_code = "TEST_PROJECT"
        response = client.get(f"/api/architect/summary/{project_code}")
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证响应结构（目前返回模拟数据）
        assert "project" in data
        assert data["project"]["code"] == project_code
        assert "stats" in data
        assert "components" in data
        assert "recent_issues" in data
        assert "last_updated" in data
        
        print(f"✅ 项目摘要获取成功: {data['stats']}")
    
    def test_submit_handover_snapshot(self, client, sample_handover, temp_docs_dir, check_dependencies):
        """测试5: 提交交接快照"""
        response = client.post(
            "/api/architect/handover",
            json=sample_handover.dict()
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证响应
        assert data["success"] is True
        assert data["snapshot_id"] == sample_handover.snapshot_id
        assert "snapshot_path" in data
        
        # 验证快照文件已保存
        snapshot_path = temp_docs_dir / "arch" / "handovers" / f"{sample_handover.snapshot_id}.json"
        assert snapshot_path.exists(), "快照JSON文件应该已保存"
        
        # 验证快照内容
        saved_snapshot = json.loads(snapshot_path.read_text(encoding='utf-8'))
        assert saved_snapshot["snapshot_id"] == sample_handover.snapshot_id
        assert saved_snapshot["project_code"] == sample_handover.project_code
        
        # 验证HANDOVER.md已更新
        handover_md = temp_docs_dir / "arch" / "HANDOVER.md"
        assert handover_md.exists(), "HANDOVER.md应该已生成"
        
        content = handover_md.read_text(encoding='utf-8')
        assert sample_handover.snapshot_id in content
        assert "下一任架构师" in content
        
        print(f"✅ 交接快照已保存: {snapshot_path}")
        print(f"✅ 交接文档已更新: {handover_md}")
    
    def test_get_latest_handover(self, client, check_dependencies):
        """测试6: 获取最新交接快照"""
        project_code = "TEST_PROJECT"
        response = client.get(
            "/api/architect/handover/latest",
            params={"project_code": project_code}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # 目前返回"未找到"的模拟响应
        # 实际集成后应该能找到之前提交的快照
        assert "found" in data or "message" in data
        
        print(f"✅ 查询最新快照接口工作正常")
    
    def test_get_architect_tasks(self, client, check_dependencies):
        """测试7: 查询架构师任务"""
        project_code = "TEST_PROJECT"
        response = client.get(f"/api/architect/tasks/{project_code}")
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证响应结构
        assert data["project_code"] == project_code
        assert "tasks" in data
        assert "total" in data
        
        print(f"✅ 任务查询接口工作正常")
    
    def test_get_architect_tasks_with_filters(self, client, check_dependencies):
        """测试8: 带过滤条件查询任务"""
        project_code = "TEST_PROJECT"
        response = client.get(
            f"/api/architect/tasks/{project_code}",
            params={"status": "pending", "priority": "high"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["project_code"] == project_code
        print(f"✅ 任务过滤查询工作正常")


class TestArchitectAPIWorkflow:
    """测试完整的架构师工作流"""
    
    def test_complete_workflow(
        self,
        client,
        sample_analysis,
        sample_handover,
        temp_docs_dir,
        check_dependencies
    ):
        """测试9: 完整工作流（端到端）
        
        流程:
        1. 检查服务状态
        2. 提交架构分析
        3. 查询项目摘要
        4. 查询任务列表
        5. 提交交接快照
        6. 查询最新快照
        """
        
        print("\n" + "="*70)
        print("开始端到端工作流测试")
        print("="*70)
        
        # Step 1: 检查服务状态
        print("\n[1/6] 检查服务状态...")
        response = client.get("/api/architect/status")
        assert response.status_code == 200
        print("✅ 服务健康")
        
        # Step 2: 提交架构分析
        print("\n[2/6] 提交架构分析...")
        response = client.post(
            "/api/architect/analysis",
            json=sample_analysis.dict()
        )
        assert response.status_code == 200
        analysis_result = response.json()
        assert analysis_result["success"] is True
        print(f"✅ 分析提交成功: 创建 {len(sample_analysis.suggested_tasks)} 个任务")
        
        # Step 3: 查询项目摘要
        print("\n[3/6] 查询项目摘要...")
        response = client.get(f"/api/architect/summary/{sample_analysis.project_code}")
        assert response.status_code == 200
        summary = response.json()
        print(f"✅ 项目摘要: {summary['stats']['total_tasks']} 个任务")
        
        # Step 4: 查询任务列表
        print("\n[4/6] 查询架构师任务...")
        response = client.get(f"/api/architect/tasks/{sample_analysis.project_code}")
        assert response.status_code == 200
        tasks = response.json()
        print(f"✅ 任务查询: {tasks['total']} 个任务")
        
        # Step 5: 提交交接快照
        print("\n[5/6] 提交交接快照...")
        response = client.post(
            "/api/architect/handover",
            json=sample_handover.dict()
        )
        assert response.status_code == 200
        handover_result = response.json()
        assert handover_result["success"] is True
        print(f"✅ 交接快照已保存: {handover_result['snapshot_id']}")
        
        # Step 6: 查询最新快照
        print("\n[6/6] 查询最新交接快照...")
        response = client.get(
            "/api/architect/handover/latest",
            params={"project_code": sample_analysis.project_code}
        )
        assert response.status_code == 200
        print("✅ 快照查询成功")
        
        # 验证生成的文档
        print("\n验证生成的文档...")
        task_board = temp_docs_dir / "tasks" / "task-board.md"
        assert task_board.exists(), "任务看板应该存在"
        
        handover_md = temp_docs_dir / "arch" / "HANDOVER.md"
        assert handover_md.exists(), "交接文档应该存在"
        
        snapshot_json = temp_docs_dir / "arch" / "handovers" / f"{sample_handover.snapshot_id}.json"
        assert snapshot_json.exists(), "快照JSON应该存在"
        
        print("✅ 所有文档已正确生成")
        
        print("\n" + "="*70)
        print("✅ 端到端工作流测试完成")
        print("="*70)


class TestArchitectOrchestratorUnit:
    """测试ArchitectOrchestrator的单元功能"""
    
    def test_orchestrator_process_analysis(self, sample_analysis, temp_docs_dir):
        """测试10: 编排器处理分析"""
        orchestrator = ArchitectOrchestrator(
            state_manager=None,
            docs_root=str(temp_docs_dir)
        )
        
        result = orchestrator.process_analysis(sample_analysis)
        
        # 验证返回值结构
        assert "tasks_created" in result
        assert "issues_created" in result
        assert "articles_created" in result
        assert "task_board_updated" in result
        
        # 验证task-board.md已生成
        task_board = temp_docs_dir / "tasks" / "task-board.md"
        assert task_board.exists()
        
        content = task_board.read_text(encoding='utf-8')
        assert "TEST_PROJECT" in content
        assert "ARCH-001" in content
        
        print(f"✅ 编排器处理分析成功")
    
    def test_orchestrator_process_handover(self, sample_handover, temp_docs_dir):
        """测试11: 编排器处理交接"""
        orchestrator = ArchitectOrchestrator(
            state_manager=None,
            docs_root=str(temp_docs_dir)
        )
        
        result = orchestrator.process_handover(sample_handover)
        
        # 验证返回值
        assert result["snapshot_saved"] is True
        assert "snapshot_path" in result
        assert result["handover_md_updated"] is True
        
        # 验证文件已生成
        snapshot_path = Path(result["snapshot_path"])
        assert snapshot_path.exists()
        
        handover_md = temp_docs_dir / "arch" / "HANDOVER.md"
        assert handover_md.exists()
        
        print(f"✅ 编排器处理交接成功")
    
    def test_orchestrator_markdown_generation(self, sample_analysis, temp_docs_dir):
        """测试12: Markdown生成质量"""
        orchestrator = ArchitectOrchestrator(
            state_manager=None,
            docs_root=str(temp_docs_dir)
        )
        
        orchestrator.process_analysis(sample_analysis)
        
        task_board = temp_docs_dir / "tasks" / "task-board.md"
        content = task_board.read_text(encoding='utf-8')
        
        # 验证Markdown结构
        assert "# 任务看板" in content
        assert "## 📊 统计" in content
        assert "## 📋 任务列表" in content
        assert "## 🔴 发现的问题" in content
        assert "## 📊 功能清单摘要" in content
        
        # 验证任务详情
        for task in sample_analysis.suggested_tasks:
            assert task.id in content
            assert task.title in content
        
        # 验证问题详情
        for problem in sample_analysis.problems:
            assert problem.title in content
        
        print(f"✅ Markdown生成质量合格")


# ============================================================================
# 性能和边界测试
# ============================================================================

class TestArchitectAPIPerformance:
    """性能和边界测试"""
    
    def test_large_analysis_submission(self, client, temp_docs_dir, check_dependencies):
        """测试13: 提交大型分析（100+任务）"""
        # 生成大量任务
        large_tasks = []
        for i in range(100):
            large_tasks.append(
                ArchitectTaskSuggestion(
                    id=f"ARCH-{i+1:03d}",
                    title=f"任务 {i+1}",
                    type="backend",
                    priority="medium",
                    component="test-component",
                    description=f"测试任务 {i+1}",
                    estimated_hours=2.0
                )
            )
        
        large_analysis = ArchitectAnalysis(
            project_code="LARGE_PROJECT",
            suggested_tasks=large_tasks
        )
        
        response = client.post(
            "/api/architect/analysis",
            json=large_analysis.dict()
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # 验证task-board.md能正确生成
        task_board = temp_docs_dir / "tasks" / "task-board.md"
        assert task_board.exists()
        
        content = task_board.read_text(encoding='utf-8')
        assert "ARCH-001" in content
        assert "ARCH-100" in content
        
        print(f"✅ 大型分析（100任务）处理成功")
    
    def test_concurrent_requests(self, client, sample_analysis, check_dependencies):
        """测试14: 并发请求（模拟多架构师）"""
        import concurrent.futures
        
        def submit_analysis(project_suffix):
            analysis = sample_analysis.copy(deep=True)
            analysis.project_code = f"PROJECT_{project_suffix}"
            
            response = client.post(
                "/api/architect/analysis",
                json=analysis.dict()
            )
            return response.status_code
        
        # 模拟5个并发请求
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(submit_analysis, i) for i in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # 所有请求都应该成功
        assert all(status == 200 for status in results)
        print(f"✅ 并发测试通过: 5个并发请求全部成功")


# ============================================================================
# 主函数（直接运行时）
# ============================================================================

if __name__ == "__main__":
    """
    直接运行此文件进行测试
    
    需要安装: pip install pytest fastapi httpx
    """
    import subprocess
    
    print("="*70)
    print("架构师API - 端到端测试套件")
    print("="*70)
    print()
    
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI未安装")
        print("请运行: pip install fastapi httpx")
        exit(1)
    
    if not MODULES_AVAILABLE:
        print("❌ 架构师模块未找到")
        print("请确保在正确的目录运行测试")
        exit(1)
    
    print("✅ 依赖检查通过")
    print()
    print("运行测试...")
    print()
    
    # 运行pytest
    result = subprocess.run(
        ["pytest", __file__, "-v", "--tb=short"],
        capture_output=False
    )
    
    exit(result.returncode)

