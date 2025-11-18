"""
Token同步工具 - REQ-006实现

提供多种Token同步方式：
1. 快捷记录 - 从剪贴板读取Cursor状态栏Token值
2. 智能估算 - 根据文本长度估算Token消耗
3. 批量同步 - 批量更新多个会话的Token
4. 实时监控 - 自动同步到Dashboard

Author: Fullstack Engineer
Date: 2025-11-18
Task: REQ-006
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import tiktoken  # OpenAI的Token计数库


class TokenSyncManager:
    """Token同步管理器"""
    
    def __init__(self, monitor_file: str = None):
        """
        初始化Token同步管理器
        
        Args:
            monitor_file: 监控数据文件路径，默认为automation-data/architect_monitor.json
        """
        if monitor_file is None:
            # 尝试找到正确的路径
            possible_paths = [
                Path("automation-data/architect_monitor.json"),
                Path("apps/dashboard/automation-data/architect_monitor.json"),
                Path("../../apps/dashboard/automation-data/architect_monitor.json"),
            ]
            for p in possible_paths:
                if p.exists():
                    self.monitor_file = p
                    break
            else:
                # 使用第一个作为默认
                self.monitor_file = possible_paths[0]
        else:
            self.monitor_file = Path(monitor_file)
        
        # 确保文件存在
        self._ensure_file_exists()
        
        # 初始化tiktoken编码器（使用cl100k_base，适用于GPT-4和Claude）
        try:
            self.encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.encoder = None
            print("⚠️  tiktoken未安装，将使用简单估算（字符数/4）")
    
    def _ensure_file_exists(self):
        """确保监控文件存在"""
        if not self.monitor_file.exists():
            self.monitor_file.parent.mkdir(parents=True, exist_ok=True)
            default_data = {
                "token_usage": {
                    "used": 0,
                    "total": 1000000,
                    "sessions": []
                },
                "status": {
                    "text": "工作中",
                    "reviewed_count": 0
                },
                "last_updated": datetime.now().isoformat()
            }
            with open(self.monitor_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    def _load_data(self) -> Dict:
        """加载监控数据"""
        with open(self.monitor_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data: Dict):
        """保存监控数据"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.monitor_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def quick_record(self, token_value: int, event: str = "手动记录", 
                     conversation_id: str = "") -> Dict:
        """
        快捷记录Token使用量
        
        Args:
            token_value: Token值（从Cursor状态栏复制的数字）
            event: 事件描述
            conversation_id: 对话ID（可选）
        
        Returns:
            更新后的Token统计
        
        Example:
            >>> manager = TokenSyncManager()
            >>> result = manager.quick_record(350000, "完成架构设计")
            >>> print(result['total_used'])
        """
        data = self._load_data()
        
        # 计算增量（与上次记录的差值）
        current_total = data["token_usage"]["used"]
        increment = token_value - current_total
        
        # 如果增量为负数或为0，直接使用输入值作为当前总量
        if increment <= 0:
            increment = token_value
            data["token_usage"]["used"] = token_value
        else:
            data["token_usage"]["used"] = token_value
        
        # 记录会话
        session_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tokens": increment,
            "event": event,
            "conversation_id": conversation_id,
            "method": "manual"  # 标记为手动记录
        }
        
        if "sessions" not in data["token_usage"]:
            data["token_usage"]["sessions"] = []
        
        data["token_usage"]["sessions"].insert(0, session_record)
        
        # 只保留最近100条
        if len(data["token_usage"]["sessions"]) > 100:
            data["token_usage"]["sessions"] = data["token_usage"]["sessions"][:100]
        
        self._save_data(data)
        
        percent = (data["token_usage"]["used"] / data["token_usage"]["total"]) * 100
        
        print(f"✅ Token已更新: {token_value:,} / {data['token_usage']['total']:,} ({percent:.1f}%)")
        print(f"   本次增量: {increment:,} tokens")
        
        return {
            "success": True,
            "total_used": data["token_usage"]["used"],
            "increment": increment,
            "percent": percent
        }
    
    def estimate_tokens(self, text: str) -> int:
        """
        估算文本的Token数量
        
        Args:
            text: 要估算的文本
        
        Returns:
            估算的Token数量
        """
        if self.encoder:
            # 使用tiktoken精确计算
            return len(self.encoder.encode(text))
        else:
            # 简单估算：中文约1字=1.5token，英文约1词=1.3token
            # 综合估算：总字符数/4
            chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
            english_chars = len([c for c in text if c.isalpha() and ord(c) < 128])
            other_chars = len(text) - chinese_chars - english_chars
            
            estimated = int(chinese_chars * 1.5 + english_chars * 0.3 + other_chars * 0.5)
            return estimated
    
    def auto_record_conversation(self, user_message: str, assistant_message: str,
                                 event: str = "对话", conversation_id: str = "") -> Dict:
        """
        自动记录一次对话的Token消耗（估算）
        
        Args:
            user_message: 用户消息
            assistant_message: AI回复消息
            event: 事件描述
            conversation_id: 对话ID
        
        Returns:
            更新后的Token统计
        """
        # 估算Token
        user_tokens = self.estimate_tokens(user_message)
        assistant_tokens = self.estimate_tokens(assistant_message)
        total_tokens = user_tokens + assistant_tokens
        
        # 记录
        data = self._load_data()
        data["token_usage"]["used"] += total_tokens
        
        session_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tokens": total_tokens,
            "event": event,
            "conversation_id": conversation_id,
            "method": "auto_estimate",  # 标记为自动估算
            "details": {
                "user_tokens": user_tokens,
                "assistant_tokens": assistant_tokens
            }
        }
        
        if "sessions" not in data["token_usage"]:
            data["token_usage"]["sessions"] = []
        
        data["token_usage"]["sessions"].insert(0, session_record)
        
        if len(data["token_usage"]["sessions"]) > 100:
            data["token_usage"]["sessions"] = data["token_usage"]["sessions"][:100]
        
        self._save_data(data)
        
        percent = (data["token_usage"]["used"] / data["token_usage"]["total"]) * 100
        
        print(f"✅ 自动记录Token: +{total_tokens:,} (用户:{user_tokens:,} + AI:{assistant_tokens:,})")
        print(f"   总计: {data['token_usage']['used']:,} / {data['token_usage']['total']:,} ({percent:.1f}%)")
        
        return {
            "success": True,
            "total_used": data["token_usage"]["used"],
            "session_tokens": total_tokens,
            "percent": percent
        }
    
    def parse_cursor_clipboard(self, clipboard_text: str) -> Optional[int]:
        """
        从剪贴板文本中解析Cursor状态栏的Token值
        
        支持格式：
        - "350,000 tokens used"
        - "350000"
        - "350K"
        - "35万"
        
        Args:
            clipboard_text: 剪贴板文本
        
        Returns:
            解析出的Token数值，失败返回None
        """
        # 移除换行
        text = clipboard_text.strip()
        
        # 模式1: "350,000" 或 "350000" 或 "350 000"
        # 先尝试匹配带逗号的格式
        match = re.search(r'(\d{1,3}(?:,\d{3})+)', text)
        if match:
            number_str = match.group(1).replace(",", "")
            return int(number_str)
        
        # 尝试匹配带空格的格式 "350 000"
        match = re.search(r'(\d{1,3}(?:\s\d{3})+)', text)
        if match:
            number_str = match.group(1).replace(" ", "")
            return int(number_str)
        
        # 再尝试匹配纯数字（5位以上，避免误匹配年份等）
        match = re.search(r'(\d{5,})', text)
        if match:
            return int(match.group(1))
        
        # 模式2: "350K"
        match = re.search(r'(\d+(?:\.\d+)?)K', text, re.IGNORECASE)
        if match:
            return int(float(match.group(1)) * 1000)
        
        # 模式3: "35万"
        match = re.search(r'(\d+(?:\.\d+)?)万', text)
        if match:
            return int(float(match.group(1)) * 10000)
        
        return None
    
    def get_current_usage(self) -> Dict:
        """
        获取当前Token使用情况
        
        Returns:
            Token使用统计
        """
        data = self._load_data()
        token_usage = data.get("token_usage", {})
        
        used = token_usage.get("used", 0)
        total = token_usage.get("total", 1000000)
        percent = (used / total) * 100 if total > 0 else 0
        remaining = total - used
        
        return {
            "used": used,
            "total": total,
            "percent": round(percent, 2),
            "remaining": remaining,
            "sessions_count": len(token_usage.get("sessions", [])),
            "last_updated": data.get("last_updated", "")
        }
    
    def batch_import_sessions(self, sessions: List[Dict]) -> Dict:
        """
        批量导入会话Token记录
        
        Args:
            sessions: 会话列表，每个会话包含 {tokens, event, timestamp?, conversation_id?}
        
        Returns:
            导入结果统计
        """
        data = self._load_data()
        
        if "sessions" not in data["token_usage"]:
            data["token_usage"]["sessions"] = []
        
        imported_count = 0
        total_tokens = 0
        
        for session in sessions:
            tokens = session.get("tokens", 0)
            if tokens <= 0:
                continue
            
            session_record = {
                "timestamp": session.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "tokens": tokens,
                "event": session.get("event", "批量导入"),
                "conversation_id": session.get("conversation_id", ""),
                "method": "batch_import"
            }
            
            data["token_usage"]["sessions"].insert(0, session_record)
            data["token_usage"]["used"] += tokens
            total_tokens += tokens
            imported_count += 1
        
        # 保留最近100条
        if len(data["token_usage"]["sessions"]) > 100:
            data["token_usage"]["sessions"] = data["token_usage"]["sessions"][:100]
        
        self._save_data(data)
        
        print(f"✅ 批量导入完成: {imported_count}个会话, 共{total_tokens:,} tokens")
        
        return {
            "success": True,
            "imported_count": imported_count,
            "total_tokens": total_tokens,
            "current_usage": self.get_current_usage()
        }


def quick_sync_from_clipboard():
    """
    快捷同步：从剪贴板读取Token值并同步
    
    使用方法：
    1. 在Cursor中，右键状态栏的Token数字，复制
    2. 运行此函数
    3. Token自动同步到Dashboard
    """
    try:
        # 尝试从剪贴板读取
        import pyperclip
        clipboard_text = pyperclip.paste()
        
        manager = TokenSyncManager()
        token_value = manager.parse_cursor_clipboard(clipboard_text)
        
        if token_value:
            result = manager.quick_record(token_value, "从剪贴板同步")
            print(f"\n✅ 同步成功！")
            print(f"   Token: {result['total_used']:,}")
            print(f"   使用率: {result['percent']:.1f}%")
            return True
        else:
            print(f"❌ 无法解析剪贴板内容: {clipboard_text}")
            print(f"   请确保复制了Cursor状态栏的Token数字")
            return False
            
    except ImportError:
        print("❌ 需要安装pyperclip库:")
        print("   pip install pyperclip")
        return False
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return False


# ============ 命令行工具 ============

def cli():
    """命令行接口"""
    import sys
    
    if len(sys.argv) < 2:
        print("""
Token同步工具 - 使用方法

1. 快捷同步（从剪贴板）:
   python token_sync.py quick
   
2. 手动记录Token:
   python token_sync.py record 350000 "完成架构设计"
   
3. 查看当前使用情况:
   python token_sync.py status
   
4. 自动估算对话Token:
   python token_sync.py estimate <user_message> <assistant_message>
""")
        return
    
    command = sys.argv[1]
    manager = TokenSyncManager()
    
    if command == "quick":
        # 快捷同步
        quick_sync_from_clipboard()
    
    elif command == "record":
        # 手动记录
        if len(sys.argv) < 3:
            print("用法: python token_sync.py record <token_value> [event]")
            return
        
        token_value = int(sys.argv[2])
        event = sys.argv[3] if len(sys.argv) > 3 else "手动记录"
        manager.quick_record(token_value, event)
    
    elif command == "status":
        # 查看状态
        usage = manager.get_current_usage()
        print(f"\n[Token使用情况]")
        print(f"   已使用: {usage['used']:,} tokens")
        print(f"   总额度: {usage['total']:,} tokens")
        print(f"   使用率: {usage['percent']:.1f}%")
        print(f"   剩余: {usage['remaining']:,} tokens")
        print(f"   会话数: {usage['sessions_count']}")
        print(f"   更新时间: {usage['last_updated']}")
    
    elif command == "estimate":
        # 估算Token
        if len(sys.argv) < 4:
            print("用法: python token_sync.py estimate <user_message> <assistant_message>")
            return
        
        user_msg = sys.argv[2]
        assistant_msg = sys.argv[3]
        manager.auto_record_conversation(user_msg, assistant_msg)
    
    else:
        print(f"未知命令: {command}")
        print("运行 'python token_sync.py' 查看帮助")


if __name__ == "__main__":
    cli()

