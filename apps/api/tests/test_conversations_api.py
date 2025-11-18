# -*- coding: utf-8 -*-
"""
对话历史库API的单元测试和集成测试

测试覆盖：
- 会话CRUD操作
- 消息管理
- 会话标签统计
- 会话查询和过滤
- 错误处理
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json
import sys
from datetime import datetime

# 添加源路径
root_path = Path(__file__).parent.parent.parent.parent
api_src = root_path / "apps" / "api" / "src"
sys.path.insert(0, str(api_src))

from main import app

client = TestClient(app)

# 测试数据路径
TEST_DATA_DIR = Path(__file__).parent.parent / "test_data"
TEST_DATA_FILE = TEST_DATA_DIR / "architect-conversations.json"


# ============================================================================
# 测试准备和清理
# ============================================================================

@pytest.fixture(autouse=True)
def setup_teardown():
    """测试前后的准备和清理"""
    # 准备测试数据目录
    TEST_DATA_DIR.mkdir(exist_ok=True)
    
    # 创建初始测试数据
    test_data = {
        "sessions": [
            {
                "session_id": "test-session-001",
                "title": "测试会话1",
                "created_at": "2025-11-18 10:00:00",
                "updated_at": "2025-11-18 10:30:00",
                "status": "completed",
                "total_tokens": 5000,
                "messages_count": 3,
                "participants": ["用户", "架构师AI"],
                "tags": ["测试", "API"],
                "summary": "测试会话摘要",
                "messages": [
                    {
                        "id": "msg-001",
                        "timestamp": "2025-11-18 10:00:00",
                        "from": "用户",
                        "content": "测试消息1",
                        "type": "request",
                        "tokens": 100
                    },
                    {
                        "id": "msg-002",
                        "timestamp": "2025-11-18 10:10:00",
                        "from": "架构师AI",
                        "content": "测试回复1",
                        "type": "response",
                        "tokens": 200
                    },
                    {
                        "id": "msg-003",
                        "timestamp": "2025-11-18 10:20:00",
                        "from": "用户",
                        "content": "测试消息2",
                        "type": "request",
                        "tokens": 150
                    }
                ]
            },
            {
                "session_id": "test-session-002",
                "title": "测试会话2",
                "created_at": "2025-11-18 11:00:00",
                "updated_at": "2025-11-18 11:15:00",
                "status": "active",
                "total_tokens": 3000,
                "messages_count": 2,
                "participants": ["用户", "架构师AI"],
                "tags": ["测试"],
                "summary": "另一个测试会话",
                "messages": [
                    {
                        "id": "msg-101",
                        "timestamp": "2025-11-18 11:00:00",
                        "from": "用户",
                        "content": "新会话开始",
                        "type": "request",
                        "tokens": 300
                    },
                    {
                        "id": "msg-102",
                        "timestamp": "2025-11-18 11:15:00",
                        "from": "架构师AI",
                        "content": "收到，开始处理",
                        "type": "response",
                        "tokens": 400
                    }
                ]
            }
        ]
    }
    
    # 保存测试数据到临时位置
    with open(TEST_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    yield
    
    # 清理测试数据
    if TEST_DATA_FILE.exists():
        TEST_DATA_FILE.unlink()


# ============================================================================
# 测试1: 获取所有会话 GET /api/conversations
# ============================================================================

class TestGetAllConversations:
    """测试获取所有会话的API"""
    
    def test_get_all_conversations_success(self):
        """测试成功获取所有会话"""
        response = client.get("/api/conversations")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "sessions" in data
        assert "count" in data
        assert data["count"] >= 0
    
    def test_get_all_conversations_returns_sessions(self):
        """测试返回的会话数据结构正确"""
        response = client.get("/api/conversations")
        data = response.json()
        
        if data["count"] > 0:
            session = data["sessions"][0]
            assert "session_id" in session
            assert "title" in session
            assert "status" in session
            assert "total_tokens" in session
            assert "messages_count" in session
    
    def test_get_all_conversations_timestamp(self):
        """测试返回时间戳"""
        response = client.get("/api/conversations")
        data = response.json()
        
        assert "timestamp" in data
        # 验证时间戳格式
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            pytest.fail("时间戳格式不正确")


# ============================================================================
# 测试2: 获取单个会话 GET /api/conversations/{session_id}
# ============================================================================

class TestGetConversation:
    """测试获取单个会话的API"""
    
    def test_get_conversation_success(self):
        """测试成功获取单个会话"""
        response = client.get("/api/conversations/test-session-001")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "session" in data
        assert data["session"]["session_id"] == "test-session-001"
    
    def test_get_conversation_with_messages(self):
        """测试获取的会话包含消息"""
        response = client.get("/api/conversations/test-session-001")
        data = response.json()
        
        session = data["session"]
        assert "messages" in session
        assert len(session["messages"]) > 0
    
    def test_get_conversation_not_found(self):
        """测试获取不存在的会话"""
        response = client.get("/api/conversations/non-existent-session")
        assert response.status_code == 404


# ============================================================================
# 测试3: 创建新会话 POST /api/conversations
# ============================================================================

class TestCreateConversation:
    """测试创建会话的API"""
    
    def test_create_conversation_success(self):
        """测试成功创建会话"""
        payload = {
            "title": "新测试会话",
            "participants": ["用户", "AI"],
            "tags": ["新", "测试"],
            "summary": "这是一个新会话"
        }
        
        response = client.post("/api/conversations", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "session" in data
        assert "session_id" in data
        assert data["session"]["title"] == "新测试会话"
    
    def test_create_conversation_default_values(self):
        """测试创建会话使用默认值"""
        payload = {
            "title": "最小会话"
        }
        
        response = client.post("/api/conversations", json=payload)
        data = response.json()
        
        session = data["session"]
        assert session["status"] == "active"
        assert session["total_tokens"] == 0
        assert session["messages_count"] == 0
        assert len(session["participants"]) > 0
    
    def test_create_conversation_unique_ids(self):
        """测试创建多个会话具有唯一ID"""
        responses = []
        
        for i in range(3):
            payload = {"title": f"会话{i}"}
            response = client.post("/api/conversations", json=payload)
            responses.append(response.json())
        
        ids = [r["session_id"] for r in responses]
        assert len(ids) == len(set(ids)), "会话ID不唯一"


# ============================================================================
# 测试4: 更新会话 PUT /api/conversations/{session_id}
# ============================================================================

class TestUpdateConversation:
    """测试更新会话的API"""
    
    def test_update_conversation_title(self):
        """测试更新会话标题"""
        payload = {"title": "更新后的标题"}
        
        response = client.put(
            "/api/conversations/test-session-001",
            json=payload
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["session"]["title"] == "更新后的标题"
    
    def test_update_conversation_status(self):
        """测试更新会话状态"""
        payload = {"status": "archived"}
        
        response = client.put(
            "/api/conversations/test-session-001",
            json=payload
        )
        
        data = response.json()
        assert data["session"]["status"] == "archived"
    
    def test_update_conversation_tags(self):
        """测试更新会话标签"""
        payload = {"tags": ["新标签1", "新标签2"]}
        
        response = client.put(
            "/api/conversations/test-session-001",
            json=payload
        )
        
        data = response.json()
        assert data["session"]["tags"] == ["新标签1", "新标签2"]
    
    def test_update_conversation_not_found(self):
        """测试更新不存在的会话"""
        response = client.put(
            "/api/conversations/non-existent",
            json={"title": "新标题"}
        )
        assert response.status_code == 404


# ============================================================================
# 测试5: 删除会话 DELETE /api/conversations/{session_id}
# ============================================================================

class TestDeleteConversation:
    """测试删除会话的API"""
    
    def test_delete_conversation_success(self):
        """测试成功删除会话"""
        response = client.delete("/api/conversations/test-session-001")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["deleted_session_id"] == "test-session-001"
        
        # 验证会话已被删除
        get_response = client.get("/api/conversations/test-session-001")
        assert get_response.status_code == 404
    
    def test_delete_conversation_not_found(self):
        """测试删除不存在的会话"""
        response = client.delete("/api/conversations/non-existent")
        assert response.status_code == 404


# ============================================================================
# 测试6: 添加消息 POST /api/conversations/{session_id}/messages
# ============================================================================

class TestAddMessage:
    """测试添加消息的API"""
    
    def test_add_message_success(self):
        """测试成功添加消息"""
        payload = {
            "from": "用户",
            "content": "新消息内容",
            "type": "request",
            "tokens": 500
        }
        
        response = client.post(
            "/api/conversations/test-session-001/messages",
            json=payload
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "message" in data
        assert data["message"]["content"] == "新消息内容"
    
    def test_add_message_updates_session(self):
        """测试添加消息更新会话统计"""
        original = client.get("/api/conversations/test-session-001").json()
        original_count = original["session"]["messages_count"]
        
        payload = {
            "from": "用户",
            "content": "测试",
            "type": "request",
            "tokens": 100
        }
        
        client.post(
            "/api/conversations/test-session-001/messages",
            json=payload
        )
        
        updated = client.get("/api/conversations/test-session-001").json()
        assert updated["session"]["messages_count"] == original_count + 1
    
    def test_add_message_to_nonexistent_session(self):
        """测试向不存在的会话添加消息"""
        payload = {
            "from": "用户",
            "content": "测试",
            "type": "request",
            "tokens": 100
        }
        
        response = client.post(
            "/api/conversations/non-existent/messages",
            json=payload
        )
        assert response.status_code == 404


# ============================================================================
# 测试7: 获取会话消息 GET /api/conversations/{session_id}/messages
# ============================================================================

class TestGetMessages:
    """测试获取会话消息的API"""
    
    def test_get_messages_success(self):
        """测试成功获取消息列表"""
        response = client.get("/api/conversations/test-session-001/messages")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "messages" in data
        assert "count" in data
    
    def test_get_messages_count_correct(self):
        """测试消息计数正确"""
        response = client.get("/api/conversations/test-session-001/messages")
        data = response.json()
        
        assert data["count"] == len(data["messages"])
    
    def test_get_messages_from_nonexistent_session(self):
        """测试获取不存在会话的消息"""
        response = client.get("/api/conversations/non-existent/messages")
        assert response.status_code == 404


# ============================================================================
# 测试8: 获取标签列表 GET /api/conversations/tags/list
# ============================================================================

class TestGetTags:
    """测试获取标签列表的API"""
    
    def test_get_tags_success(self):
        """测试成功获取标签列表"""
        response = client.get("/api/conversations/tags/list")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "tags" in data
        assert "total_unique_tags" in data
    
    def test_get_tags_structure(self):
        """测试标签数据结构"""
        response = client.get("/api/conversations/tags/list")
        data = response.json()
        
        if data["total_unique_tags"] > 0:
            tag = data["tags"][0]
            assert "name" in tag
            assert "count" in tag
            assert "last_used" in tag


# ============================================================================
# 测试9: 获取统计信息 GET /api/conversations/stats/overview
# ============================================================================

class TestGetStats:
    """测试获取统计信息的API"""
    
    def test_get_stats_success(self):
        """测试成功获取统计信息"""
        response = client.get("/api/conversations/stats/overview")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "stats" in data
    
    def test_get_stats_content(self):
        """测试统计信息内容"""
        response = client.get("/api/conversations/stats/overview")
        data = response.json()
        stats = data["stats"]
        
        assert "total_sessions" in stats
        assert "total_messages" in stats
        assert "total_tokens" in stats
        assert "average_tokens_per_session" in stats


# ============================================================================
# 测试10: 按日期查询 GET /api/conversations/search/by-date
# ============================================================================

class TestSearchByDate:
    """测试按日期查询的API"""
    
    def test_search_by_date_success(self):
        """测试按日期查询成功"""
        response = client.get(
            "/api/conversations/search/by-date?start_date=2025-11-18"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "sessions" in data
    
    def test_search_by_date_range(self):
        """测试日期范围查询"""
        response = client.get(
            "/api/conversations/search/by-date?"
            "start_date=2025-11-18&end_date=2025-11-18"
        )
        assert response.status_code == 200
    
    def test_search_by_date_invalid_format(self):
        """测试无效的日期格式"""
        response = client.get(
            "/api/conversations/search/by-date?start_date=invalid"
        )
        assert response.status_code == 400


# ============================================================================
# 测试11: 按Token范围查询 GET /api/conversations/search/by-tokens
# ============================================================================

class TestSearchByTokens:
    """测试按Token范围查询的API"""
    
    def test_search_by_tokens_success(self):
        """测试按Token范围查询成功"""
        response = client.get(
            "/api/conversations/search/by-tokens?min_tokens=0&max_tokens=10000"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "sessions" in data
    
    def test_search_by_tokens_filters_correctly(self):
        """测试Token范围过滤正确"""
        response = client.get(
            "/api/conversations/search/by-tokens?min_tokens=4000&max_tokens=6000"
        )
        data = response.json()
        
        for session in data["sessions"]:
            tokens = session.get("total_tokens", 0)
            assert 4000 <= tokens <= 6000


# ============================================================================
# 测试12: 健康检查 GET /api/conversations/health
# ============================================================================

class TestHealth:
    """测试健康检查的API"""
    
    def test_health_check_success(self):
        """测试健康检查成功"""
        response = client.get("/api/conversations/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "status" in data


# ============================================================================
# 集成测试场景
# ============================================================================

class TestIntegrationScenarios:
    """测试集成场景"""
    
    def test_create_and_add_messages_workflow(self):
        """测试创建会话并添加消息的工作流"""
        # 1. 创建会话
        create_resp = client.post(
            "/api/conversations",
            json={"title": "集成测试会话"}
        )
        session_id = create_resp.json()["session_id"]
        
        # 2. 添加消息
        for i in range(3):
            client.post(
                f"/api/conversations/{session_id}/messages",
                json={
                    "from": "用户" if i % 2 == 0 else "架构师AI",
                    "content": f"消息{i}",
                    "type": "request" if i % 2 == 0 else "response",
                    "tokens": 100 + i * 50
                }
            )
        
        # 3. 验证
        get_resp = client.get(f"/api/conversations/{session_id}")
        session = get_resp.json()["session"]
        assert session["messages_count"] == 3
    
    def test_query_and_update_workflow(self):
        """测试查询和更新的工作流"""
        # 1. 获取所有会话
        list_resp = client.get("/api/conversations")
        sessions = list_resp.json()["sessions"]
        
        if sessions:
            session_id = sessions[0]["session_id"]
            
            # 2. 更新会话
            client.put(
                f"/api/conversations/{session_id}",
                json={"title": "工作流测试"}
            )
            
            # 3. 验证更新
            get_resp = client.get(f"/api/conversations/{session_id}")
            assert get_resp.json()["session"]["title"] == "工作流测试"


# ============================================================================
# 性能测试
# ============================================================================

class TestPerformance:
    """性能测试"""
    
    def test_get_all_conversations_performance(self):
        """测试获取所有会话的性能"""
        import time
        
        start = time.time()
        response = client.get("/api/conversations")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 1.0, f"获取会话耗时{elapsed:.2f}秒，超过1秒"
    
    def test_add_message_performance(self):
        """测试添加消息的性能"""
        import time
        
        start = time.time()
        response = client.post(
            "/api/conversations/test-session-001/messages",
            json={
                "from": "用户",
                "content": "性能测试消息",
                "type": "request",
                "tokens": 100
            }
        )
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 0.5, f"添加消息耗时{elapsed:.2f}秒，超过0.5秒"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

