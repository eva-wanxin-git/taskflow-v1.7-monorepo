"""
Token同步工具测试
REQ-006: Token显示准确实时同步

测试覆盖：
1. Token解析（多种格式）
2. Token估算（中英文）
3. 快捷记录
4. 自动记录对话
5. 批量导入
6. 增量计算
"""

import pytest
import json
from pathlib import Path
import sys
import tempfile
import shutil

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "shared-utils"))

from token_sync import TokenSyncManager


class TestTokenParsing:
    """测试Token值解析"""
    
    def test_parse_plain_number(self):
        """测试纯数字"""
        manager = TokenSyncManager()
        assert manager.parse_cursor_clipboard("350000") == 350000
        assert manager.parse_cursor_clipboard("50000") == 50000
    
    def test_parse_with_comma(self):
        """测试带逗号的数字"""
        manager = TokenSyncManager()
        assert manager.parse_cursor_clipboard("350,000") == 350000
        assert manager.parse_cursor_clipboard("1,234,567") == 1234567
    
    def test_parse_with_spaces(self):
        """测试带空格的数字"""
        manager = TokenSyncManager()
        assert manager.parse_cursor_clipboard("350 000") == 350000
        assert manager.parse_cursor_clipboard("1 234 567") == 1234567
    
    def test_parse_with_k_suffix(self):
        """测试K后缀"""
        manager = TokenSyncManager()
        assert manager.parse_cursor_clipboard("350K") == 350000
        assert manager.parse_cursor_clipboard("50k") == 50000
        assert manager.parse_cursor_clipboard("1.5K") == 1500
    
    def test_parse_with_chinese_unit(self):
        """测试中文单位"""
        manager = TokenSyncManager()
        assert manager.parse_cursor_clipboard("35万") == 350000
        assert manager.parse_cursor_clipboard("10万") == 100000
        assert manager.parse_cursor_clipboard("1.5万") == 15000
    
    def test_parse_cursor_format(self):
        """测试Cursor状态栏格式"""
        manager = TokenSyncManager()
        assert manager.parse_cursor_clipboard("350,000 tokens used") == 350000
        assert manager.parse_cursor_clipboard("Token: 350000") == 350000
    
    def test_parse_invalid_format(self):
        """测试无效格式"""
        manager = TokenSyncManager()
        assert manager.parse_cursor_clipboard("abc") is None
        assert manager.parse_cursor_clipboard("") is None
        assert manager.parse_cursor_clipboard("no numbers here") is None


class TestTokenEstimation:
    """测试Token估算"""
    
    def test_estimate_english_text(self):
        """测试英文文本"""
        manager = TokenSyncManager()
        text = "Hello world, this is a test message."
        tokens = manager.estimate_tokens(text)
        assert tokens > 0
        assert 5 < tokens < 20  # 应该在合理范围内
    
    def test_estimate_chinese_text(self):
        """测试中文文本"""
        manager = TokenSyncManager()
        text = "你好世界，这是一条测试消息。"
        tokens = manager.estimate_tokens(text)
        assert tokens > 0
        assert 10 < tokens < 30
    
    def test_estimate_mixed_text(self):
        """测试中英文混合"""
        manager = TokenSyncManager()
        text = "Hello 你好, this is 测试 message."
        tokens = manager.estimate_tokens(text)
        assert tokens > 0
    
    def test_estimate_code(self):
        """测试代码"""
        manager = TokenSyncManager()
        code = """
def hello_world():
    print("Hello, World!")
    return True
"""
        tokens = manager.estimate_tokens(code)
        assert tokens > 0
        assert 10 < tokens < 50
    
    def test_estimate_empty_text(self):
        """测试空文本"""
        manager = TokenSyncManager()
        assert manager.estimate_tokens("") == 0


class TestQuickRecord:
    """测试快捷记录"""
    
    def setup_method(self):
        """每个测试前创建临时目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.monitor_file = Path(self.temp_dir) / "architect_monitor.json"
        self.manager = TokenSyncManager(str(self.monitor_file))
    
    def teardown_method(self):
        """每个测试后清理"""
        shutil.rmtree(self.temp_dir)
    
    def test_first_record(self):
        """测试第一次记录"""
        result = self.manager.quick_record(50000, "首次记录")
        assert result["success"] is True
        assert result["total_used"] == 50000
        assert result["increment"] == 50000
    
    def test_incremental_record(self):
        """测试增量记录"""
        self.manager.quick_record(50000, "第一次")
        result = self.manager.quick_record(80000, "第二次")
        
        assert result["total_used"] == 80000
        assert result["increment"] == 30000
    
    def test_negative_increment(self):
        """测试负增量（修正错误）"""
        self.manager.quick_record(100000, "错误记录")
        result = self.manager.quick_record(50000, "修正")
        
        # 负增量时，应该直接设置为新值
        assert result["total_used"] == 50000
    
    def test_session_history(self):
        """测试会话历史"""
        self.manager.quick_record(50000, "第一次")
        self.manager.quick_record(80000, "第二次")
        
        data = self.manager._load_data()
        sessions = data["token_usage"]["sessions"]
        
        assert len(sessions) == 2
        assert sessions[0]["event"] == "第二次"  # 最新的在前
        assert sessions[1]["event"] == "第一次"


class TestAutoRecordConversation:
    """测试自动记录对话"""
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.monitor_file = Path(self.temp_dir) / "architect_monitor.json"
        self.manager = TokenSyncManager(str(self.monitor_file))
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_record_conversation(self):
        """测试记录对话"""
        user_msg = "请帮我实现Token同步功能"
        assistant_msg = "好的，我会创建一个TokenSyncManager类..."
        
        result = self.manager.auto_record_conversation(
            user_msg, assistant_msg,
            event="开发Token同步"
        )
        
        assert result["success"] is True
        assert result["session_tokens"] > 0
        assert result["total_used"] > 0
    
    def test_multiple_conversations(self):
        """测试多次对话累加"""
        self.manager.auto_record_conversation("Hello", "Hi there")
        result = self.manager.auto_record_conversation("How are you?", "I'm fine")
        
        assert result["total_used"] > 0
        
        data = self.manager._load_data()
        assert len(data["token_usage"]["sessions"]) == 2


class TestBatchImport:
    """测试批量导入"""
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.monitor_file = Path(self.temp_dir) / "architect_monitor.json"
        self.manager = TokenSyncManager(str(self.monitor_file))
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_batch_import_sessions(self):
        """测试批量导入会话"""
        sessions = [
            {"tokens": 5000, "event": "会话1"},
            {"tokens": 8000, "event": "会话2"},
            {"tokens": 12000, "event": "会话3"},
        ]
        
        result = self.manager.batch_import_sessions(sessions)
        
        assert result["success"] is True
        assert result["imported_count"] == 3
        assert result["total_tokens"] == 25000
        assert result["current_usage"]["used"] == 25000
    
    def test_batch_import_with_timestamp(self):
        """测试带时间戳的批量导入"""
        sessions = [
            {
                "tokens": 5000,
                "event": "历史会话",
                "timestamp": "2025-11-01 10:00:00",
                "conversation_id": "hist-001"
            }
        ]
        
        result = self.manager.batch_import_sessions(sessions)
        assert result["success"] is True
        
        data = self.manager._load_data()
        session = data["token_usage"]["sessions"][0]
        assert session["timestamp"] == "2025-11-01 10:00:00"
    
    def test_batch_import_skip_invalid(self):
        """测试跳过无效会话"""
        sessions = [
            {"tokens": 5000, "event": "有效"},
            {"tokens": 0, "event": "无效1"},
            {"tokens": -100, "event": "无效2"},
            {"tokens": 8000, "event": "有效"},
        ]
        
        result = self.manager.batch_import_sessions(sessions)
        
        assert result["imported_count"] == 2  # 只导入2个有效的
        assert result["total_tokens"] == 13000


class TestCurrentUsage:
    """测试当前使用情况查询"""
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.monitor_file = Path(self.temp_dir) / "architect_monitor.json"
        self.manager = TokenSyncManager(str(self.monitor_file))
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_get_current_usage(self):
        """测试获取当前使用情况"""
        self.manager.quick_record(350000, "测试")
        
        usage = self.manager.get_current_usage()
        
        assert usage["used"] == 350000
        assert usage["total"] == 1000000
        assert usage["percent"] == 35.0
        assert usage["remaining"] == 650000
        assert usage["sessions_count"] == 1
        assert "last_updated" in usage
    
    def test_get_usage_empty(self):
        """测试空数据的使用情况"""
        usage = self.manager.get_current_usage()
        
        assert usage["used"] == 0
        assert usage["percent"] == 0
        assert usage["remaining"] == 1000000


class TestEdgeCases:
    """测试边界情况"""
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.monitor_file = Path(self.temp_dir) / "architect_monitor.json"
        self.manager = TokenSyncManager(str(self.monitor_file))
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_exceed_total_tokens(self):
        """测试超过总额度"""
        result = self.manager.quick_record(1500000, "超额")
        
        assert result["total_used"] == 1500000
        assert result["percent"] > 100
    
    def test_session_limit_100(self):
        """测试会话历史限制为100条"""
        for i in range(150):
            self.manager.quick_record(1000 * (i + 1), f"会话{i}")
        
        data = self.manager._load_data()
        sessions = data["token_usage"]["sessions"]
        
        assert len(sessions) == 100  # 只保留最近100条
        assert sessions[0]["event"] == "会话149"  # 最新的在前
    
    def test_zero_token_conversation(self):
        """测试零Token对话"""
        result = self.manager.auto_record_conversation("", "", "空对话")
        
        assert result["session_tokens"] == 0
        assert result["total_used"] == 0


# ========== 集成测试 ==========

class TestIntegration:
    """集成测试"""
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.monitor_file = Path(self.temp_dir) / "architect_monitor.json"
        self.manager = TokenSyncManager(str(self.monitor_file))
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_mixed_record_types(self):
        """测试混合使用不同记录方式"""
        # 手动记录
        self.manager.quick_record(50000, "手动1")
        
        # 自动对话
        self.manager.auto_record_conversation("Hi", "Hello", "对话1")
        
        # 批量导入
        self.manager.batch_import_sessions([
            {"tokens": 5000, "event": "批量1"}
        ])
        
        # 再次手动记录
        result = self.manager.quick_record(80000, "手动2")
        
        usage = self.manager.get_current_usage()
        
        # 验证所有会话都被记录
        assert usage["sessions_count"] == 4
        assert usage["used"] > 0
    
    def test_realistic_workflow(self):
        """测试真实工作流"""
        # 场景：一天的开发工作
        
        # 1. 早上开始，初始Token
        self.manager.quick_record(100000, "工作开始")
        
        # 2. 上午开发，多次对话
        self.manager.auto_record_conversation(
            "实现Token同步功能",
            "好的，我会创建...",
            "开发Token同步"
        )
        
        self.manager.auto_record_conversation(
            "添加测试用例",
            "我会添加完整的测试...",
            "编写测试"
        )
        
        # 3. 中午同步一次
        self.manager.quick_record(150000, "上午完成")
        
        # 4. 下午继续
        self.manager.auto_record_conversation(
            "优化代码",
            "我会进行重构...",
            "代码优化"
        )
        
        # 5. 下班前最后同步
        result = self.manager.quick_record(200000, "今日完成")
        
        # 验证
        usage = self.manager.get_current_usage()
        assert usage["used"] == 200000
        assert usage["sessions_count"] == 6  # 2次手动 + 3次自动对话 + 最终手动 = 6
        assert usage["percent"] == 20.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

