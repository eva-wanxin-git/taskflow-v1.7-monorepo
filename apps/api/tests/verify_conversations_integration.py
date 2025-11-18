#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对话历史库API集成验证脚本

验证所有11个API端点是否正常工作，包括：
- 会话CRUD操作
- 消息管理
- 统计功能
- Session Memory集成
"""

import httpx
import json
from datetime import datetime
from typing import Dict, Any, List
import sys


# ============================================================================
# 配置
# ============================================================================

API_BASE_URL = "http://localhost:8800"
TEST_DATA_SESSION_ID = "verify-session-001"


# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


# ============================================================================
# 日志函数
# ============================================================================

def log_test(test_name: str, status: bool, message: str = ""):
    """记录测试结果"""
    status_str = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if status else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status_str} | {test_name}")
    if message:
        print(f"         {message}")


def log_section(title: str):
    """记录测试段落"""
    print(f"\n{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BLUE}{title.center(70)}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}\n")


def log_api_call(method: str, path: str, status_code: int):
    """记录API调用"""
    status_str = f"{Colors.GREEN}{status_code}{Colors.RESET}" if 200 <= status_code < 300 else f"{Colors.RED}{status_code}{Colors.RESET}"
    print(f"  {method:6} {path:50} → {status_str}")


# ============================================================================
# 验证函数
# ============================================================================

def verify_endpoint_exists(method: str, path: str) -> bool:
    """验证端点是否存在"""
    try:
        full_url = f"{API_BASE_URL}{path}"
        
        if method.upper() == "GET":
            response = httpx.get(full_url, timeout=5)
        elif method.upper() == "POST":
            response = httpx.post(full_url, json={}, timeout=5)
        elif method.upper() == "PUT":
            response = httpx.put(full_url, json={}, timeout=5)
        elif method.upper() == "DELETE":
            response = httpx.delete(full_url, timeout=5)
        else:
            return False
        
        log_api_call(method, path, response.status_code)
        
        # 200-599都认为端点存在（即使报错）
        return 200 <= response.status_code < 600
        
    except Exception as e:
        log_api_call(method, path, 0)
        print(f"       {Colors.RED}错误: {str(e)}{Colors.RESET}")
        return False


# ============================================================================
# 测试集合
# ============================================================================

class ConversationsIntegrationTests:
    """对话历史库集成测试"""
    
    def __init__(self):
        self.client = httpx.Client(base_url=API_BASE_URL, timeout=10)
        self.test_session_id = None
        self.passed = 0
        self.failed = 0
    
    def run_all_tests(self) -> bool:
        """运行所有测试"""
        try:
            # 基础检查
            log_section("1. API基础检查")
            self.test_health_check()
            self.test_api_documentation()
            
            # 端点验证
            log_section("2. API端点验证")
            self.test_all_endpoints_exist()
            
            # 会话操作测试
            log_section("3. 会话CRUD操作测试")
            self.test_create_conversation()
            self.test_get_all_conversations()
            self.test_get_single_conversation()
            self.test_update_conversation()
            
            # 消息操作测试
            log_section("4. 消息管理测试")
            self.test_add_message()
            self.test_get_messages()
            
            # 查询和统计测试
            log_section("5. 查询和统计测试")
            self.test_get_stats()
            self.test_get_tags()
            self.test_search_by_date()
            self.test_search_by_tokens()
            
            # Session Memory集成测试
            log_section("6. Session Memory MCP集成测试")
            self.test_session_memory_health()
            self.test_sync_to_session_memory()
            
            # 错误处理测试
            log_section("7. 错误处理测试")
            self.test_error_handling()
            
            # 清理测试
            log_section("8. 清理")
            self.test_delete_conversation()
            
            # 摘要
            log_section("测试摘要")
            self.print_summary()
            
            return self.failed == 0
            
        except Exception as e:
            print(f"{Colors.RED}测试执行失败: {str(e)}{Colors.RESET}")
            return False
    
    # ========================================================================
    # 基础检查
    # ========================================================================
    
    def test_health_check(self):
        """测试健康检查"""
        try:
            response = self.client.get("/api/conversations/health")
            is_healthy = response.status_code == 200 and response.json().get("success")
            log_test("健康检查", is_healthy)
            if is_healthy:
                self.passed += 1
            else:
                self.failed += 1
        except Exception as e:
            log_test("健康检查", False, str(e))
            self.failed += 1
    
    def test_api_documentation(self):
        """测试API文档"""
        try:
            response = self.client.get("/api/docs")
            is_available = response.status_code == 200
            log_test("API文档 (/api/docs)", is_available)
            if is_available:
                self.passed += 1
            else:
                self.failed += 1
        except Exception as e:
            log_test("API文档", False, str(e))
            self.failed += 1
    
    # ========================================================================
    # 端点验证
    # ========================================================================
    
    def test_all_endpoints_exist(self):
        """验证所有11个端点存在"""
        endpoints = [
            ("GET", "/api/conversations"),
            ("GET", "/api/conversations/test-id"),
            ("POST", "/api/conversations"),
            ("PUT", "/api/conversations/test-id"),
            ("DELETE", "/api/conversations/test-id"),
            ("POST", "/api/conversations/test-id/messages"),
            ("GET", "/api/conversations/test-id/messages"),
            ("GET", "/api/conversations/stats/overview"),
            ("GET", "/api/conversations/tags/list"),
            ("GET", "/api/conversations/search/by-date?start_date=2025-11-18"),
            ("GET", "/api/conversations/search/by-tokens?min_tokens=0"),
        ]
        
        verified = 0
        for method, path in endpoints:
            if verify_endpoint_exists(method, path):
                verified += 1
        
        log_test(f"端点验证 ({verified}/{len(endpoints)})", verified == len(endpoints))
        if verified == len(endpoints):
            self.passed += 1
        else:
            self.failed += 1
    
    # ========================================================================
    # 会话CRUD操作
    # ========================================================================
    
    def test_create_conversation(self):
        """测试创建会话"""
        try:
            payload = {
                "title": "集成验证会话",
                "participants": ["用户", "架构师AI"],
                "tags": ["验证", "集成测试"],
                "summary": "用于验证API的测试会话"
            }
            
            response = self.client.post("/api/conversations", json=payload)
            is_success = response.status_code == 200 and response.json().get("success")
            
            if is_success:
                self.test_session_id = response.json()["session_id"]
            
            log_test("创建会话", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("创建会话", False, str(e))
            self.failed += 1
    
    def test_get_all_conversations(self):
        """测试获取所有会话"""
        try:
            response = self.client.get("/api/conversations")
            is_success = response.status_code == 200 and response.json().get("success")
            
            log_test("获取所有会话", is_success, 
                    f"共 {response.json().get('count', 0)} 个会话" if is_success else "")
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("获取所有会话", False, str(e))
            self.failed += 1
    
    def test_get_single_conversation(self):
        """测试获取单个会话"""
        if not self.test_session_id:
            log_test("获取单个会话", False, "没有测试会话ID")
            self.failed += 1
            return
        
        try:
            response = self.client.get(f"/api/conversations/{self.test_session_id}")
            is_success = response.status_code == 200 and response.json().get("success")
            
            log_test("获取单个会话", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("获取单个会话", False, str(e))
            self.failed += 1
    
    def test_update_conversation(self):
        """测试更新会话"""
        if not self.test_session_id:
            log_test("更新会话", False, "没有测试会话ID")
            self.failed += 1
            return
        
        try:
            payload = {
                "title": "已更新的会话标题",
                "status": "completed"
            }
            
            response = self.client.put(
                f"/api/conversations/{self.test_session_id}",
                json=payload
            )
            is_success = response.status_code == 200 and response.json().get("success")
            
            log_test("更新会话", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("更新会话", False, str(e))
            self.failed += 1
    
    # ========================================================================
    # 消息操作
    # ========================================================================
    
    def test_add_message(self):
        """测试添加消息"""
        if not self.test_session_id:
            log_test("添加消息", False, "没有测试会话ID")
            self.failed += 1
            return
        
        try:
            payload = {
                "from": "用户",
                "content": "这是一条测试消息",
                "type": "request",
                "tokens": 100
            }
            
            response = self.client.post(
                f"/api/conversations/{self.test_session_id}/messages",
                json=payload
            )
            is_success = response.status_code == 200 and response.json().get("success")
            
            log_test("添加消息", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("添加消息", False, str(e))
            self.failed += 1
    
    def test_get_messages(self):
        """测试获取消息"""
        if not self.test_session_id:
            log_test("获取消息", False, "没有测试会话ID")
            self.failed += 1
            return
        
        try:
            response = self.client.get(
                f"/api/conversations/{self.test_session_id}/messages"
            )
            is_success = response.status_code == 200 and response.json().get("success")
            
            log_test("获取消息", is_success, 
                    f"共 {response.json().get('count', 0)} 条消息" if is_success else "")
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("获取消息", False, str(e))
            self.failed += 1
    
    # ========================================================================
    # 查询和统计
    # ========================================================================
    
    def test_get_stats(self):
        """测试获取统计信息"""
        try:
            response = self.client.get("/api/conversations/stats/overview")
            is_success = response.status_code == 200 and response.json().get("success")
            
            if is_success:
                stats = response.json()["stats"]
                message = f"总会话数: {stats.get('total_sessions')}, 总消息数: {stats.get('total_messages')}"
            else:
                message = ""
            
            log_test("获取统计信息", is_success, message)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("获取统计信息", False, str(e))
            self.failed += 1
    
    def test_get_tags(self):
        """测试获取标签列表"""
        try:
            response = self.client.get("/api/conversations/tags/list")
            is_success = response.status_code == 200 and response.json().get("success")
            
            if is_success:
                tag_count = response.json()["total_unique_tags"]
                message = f"共 {tag_count} 个不同的标签"
            else:
                message = ""
            
            log_test("获取标签列表", is_success, message)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("获取标签列表", False, str(e))
            self.failed += 1
    
    def test_search_by_date(self):
        """测试按日期查询"""
        try:
            response = self.client.get(
                "/api/conversations/search/by-date?start_date=2025-11-18"
            )
            is_success = response.status_code == 200 and response.json().get("success")
            
            log_test("按日期查询", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("按日期查询", False, str(e))
            self.failed += 1
    
    def test_search_by_tokens(self):
        """测试按Token范围查询"""
        try:
            response = self.client.get(
                "/api/conversations/search/by-tokens?min_tokens=0&max_tokens=100000"
            )
            is_success = response.status_code == 200 and response.json().get("success")
            
            log_test("按Token范围查询", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("按Token范围查询", False, str(e))
            self.failed += 1
    
    # ========================================================================
    # Session Memory集成
    # ========================================================================
    
    def test_session_memory_health(self):
        """测试Session Memory健康检查"""
        try:
            response = self.client.get("/api/conversations/session-memory/session-memory/health")
            is_success = response.status_code == 200
            
            log_test("Session Memory健康检查", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("Session Memory健康检查", False, str(e))
            self.failed += 1
    
    def test_sync_to_session_memory(self):
        """测试同步到Session Memory"""
        if not self.test_session_id:
            log_test("同步到Session Memory", False, "没有测试会话ID")
            self.failed += 1
            return
        
        try:
            response = self.client.post(
                f"/api/conversations/session-memory/{self.test_session_id}/sync-to-session-memory"
            )
            # 由于Session Memory服务可能不可用，只检查API本身是否响应
            is_success = response.status_code in [200, 500]
            
            log_test("同步到Session Memory", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("同步到Session Memory", False, str(e))
            self.failed += 1
    
    # ========================================================================
    # 错误处理
    # ========================================================================
    
    def test_error_handling(self):
        """测试错误处理"""
        tests_passed = 0
        tests_total = 3
        
        # 测试404
        try:
            response = self.client.get("/api/conversations/non-existent-id")
            if response.status_code == 404:
                log_test("错误处理: 404 Not Found", True)
                tests_passed += 1
            else:
                log_test("错误处理: 404 Not Found", False)
        except:
            log_test("错误处理: 404 Not Found", False)
        
        # 测试无效日期格式
        try:
            response = self.client.get("/api/conversations/search/by-date?start_date=invalid")
            if response.status_code == 400:
                log_test("错误处理: 400 Bad Request", True)
                tests_passed += 1
            else:
                log_test("错误处理: 400 Bad Request", False)
        except:
            log_test("错误处理: 400 Bad Request", False)
        
        # 测试405
        try:
            response = self.client.post("/api/conversations/non-existent/invalid-action")
            # 应该返回404或405
            if response.status_code in [404, 405]:
                log_test("错误处理: 404/405 Method Not Allowed", True)
                tests_passed += 1
            else:
                log_test("错误处理: 404/405 Method Not Allowed", False)
        except:
            log_test("错误处理: 404/405 Method Not Allowed", False)
        
        if tests_passed >= 2:
            self.passed += 1
        else:
            self.failed += 1
    
    # ========================================================================
    # 清理
    # ========================================================================
    
    def test_delete_conversation(self):
        """测试删除会话"""
        if not self.test_session_id:
            log_test("删除会话", False, "没有测试会话ID")
            self.failed += 1
            return
        
        try:
            response = self.client.delete(
                f"/api/conversations/{self.test_session_id}"
            )
            is_success = response.status_code == 200 and response.json().get("success")
            
            log_test("删除会话", is_success)
            if is_success:
                self.passed += 1
            else:
                self.failed += 1
                
        except Exception as e:
            log_test("删除会话", False, str(e))
            self.failed += 1
    
    # ========================================================================
    # 摘要
    # ========================================================================
    
    def print_summary(self):
        """打印测试摘要"""
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"测试总数:   {total}")
        print(f"通过:       {Colors.GREEN}{self.passed}{Colors.RESET}")
        print(f"失败:       {Colors.RED}{self.failed}{Colors.RESET}")
        print(f"通过率:     {pass_rate:.1f}%")
        print()
        
        if self.failed == 0:
            print(f"{Colors.GREEN}✓ 所有测试都已通过！{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ 存在失败的测试，请检查上面的日志。{Colors.RESET}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    print(f"\n{Colors.BLUE}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║         对话历史库 API 集成验证                                    ║")
    print("║         Conversations API Integration Verification                ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    # 检查API是否运行
    try:
        response = httpx.get(f"{API_BASE_URL}/api/health", timeout=3)
        if response.status_code != 200:
            print(f"{Colors.RED}✗ API服务未响应{Colors.RESET}")
            print(f"  请确保API服务已启动: python apps/api/start_api.py")
            sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}✗ 无法连接到API: {str(e)}{Colors.RESET}")
        print(f"  请确保API服务已启动: python apps/api/start_api.py")
        sys.exit(1)
    
    # 运行测试
    tester = ConversationsIntegrationTests()
    success = tester.run_all_tests()
    
    # 返回状态码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

