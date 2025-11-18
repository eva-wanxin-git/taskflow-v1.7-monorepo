#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
事件监听器系统演示脚本

演示内容：
1. 启动监听器
2. 发射测试事件
3. 查看通知
4. 查看统计
"""

import requests
import time
import json
from datetime import datetime


API_BASE = "http://localhost:8800"


def print_section(title):
    """打印章节标题"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60 + "\n")


def check_api_health():
    """检查API服务是否运行"""
    print_section("🔍 检查API服务")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API服务正常运行")
            return True
        else:
            print("❌ API服务响应异常")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到API服务: {e}")
        print("\n请先启动API服务:")
        print("  cd taskflow-v1.7-monorepo/apps/api")
        print("  python start_api.py")
        return False


def start_listener():
    """启动事件监听器"""
    print_section("🚀 启动事件监听器")
    
    try:
        response = requests.post(
            f"{API_BASE}/api/listener/start",
            json={
                "project_id": "TASKFLOW",
                "poll_interval": 3,  # 3秒轮询间隔
                "max_notifications": 1000
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ 监听器启动成功")
                print(f"   项目ID: {data['config']['project_id']}")
                print(f"   轮询间隔: {data['config']['poll_interval']}秒")
            else:
                print(f"ℹ️  {data.get('message', '监听器已在运行')}")
        else:
            print(f"❌ 启动失败: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")


def emit_test_events():
    """发射测试事件"""
    print_section("📤 发射测试事件")
    
    test_events = [
        {
            "event_type": "task.completed",
            "title": "任务 DEMO-001 完成",
            "description": "演示任务完成事件",
            "related_entity_id": "DEMO-001"
        },
        {
            "event_type": "feature.developed",
            "title": "功能 FEAT-DEMO 开发完成",
            "description": "演示功能开发事件",
            "related_entity_id": "FEAT-DEMO"
        },
        {
            "event_type": "issue.discovered",
            "title": "发现问题 ISS-DEMO",
            "description": "演示问题发现事件",
            "related_entity_id": "ISS-DEMO"
        }
    ]
    
    for i, event_data in enumerate(test_events, 1):
        try:
            response = requests.post(
                f"{API_BASE}/api/events",
                json={
                    "project_id": "TASKFLOW",
                    "category": "task",
                    "source": "system",
                    "severity": "info",
                    **event_data
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    event = data.get("event", {})
                    print(f"✅ 事件 {i}: {event_data['event_type']}")
                    print(f"   ID: {event.get('id', 'N/A')}")
                    print(f"   标题: {event_data['title']}")
                else:
                    print(f"❌ 事件 {i} 发射失败")
            else:
                print(f"❌ 事件 {i} 请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 事件 {i} 请求异常: {e}")
    
    print("\n⏳ 等待5秒让监听器处理事件...")
    time.sleep(5)


def view_notifications():
    """查看通知"""
    print_section("📬 查看通知")
    
    try:
        response = requests.get(
            f"{API_BASE}/api/listener/notifications",
            params={"limit": 10, "unread_only": False},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            notifications = data.get("notifications", [])
            
            if notifications:
                print(f"✅ 收到 {len(notifications)} 条通知:\n")
                
                for i, notif in enumerate(notifications, 1):
                    type_icons = {
                        'info': 'ℹ️',
                        'success': '✅',
                        'warning': '⚠️',
                        'error': '❌'
                    }
                    icon = type_icons.get(notif.get('type', 'info'), '📌')
                    
                    print(f"{i}. {icon} [{notif.get('type', 'unknown').upper()}] {notif.get('title', 'N/A')}")
                    print(f"   消息: {notif.get('message', 'N/A')}")
                    print(f"   时间: {notif.get('created_at', 'N/A')}")
                    print(f"   已读: {'是' if notif.get('read') else '否'}")
                    print()
            else:
                print("ℹ️  暂无通知")
                
        else:
            print(f"❌ 获取通知失败: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")


def view_statistics():
    """查看统计信息"""
    print_section("📊 统计信息")
    
    # 监听器状态
    try:
        response = requests.get(f"{API_BASE}/api/listener/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                status = data.get("status", {})
                print("【监听器状态】")
                print(f"  运行中: {'是' if status.get('is_running') else '否'}")
                print(f"  项目ID: {status.get('project_id', 'N/A')}")
                print(f"  轮询间隔: {status.get('poll_interval', 'N/A')}秒")
                print(f"  总轮询次数: {status.get('total_polled', 0)}")
                print(f"  已处理事件: {status.get('total_processed', 0)}")
                print(f"  错误次数: {status.get('total_errors', 0)}")
                print()
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取监听器状态失败: {e}")
    
    # 规则统计
    try:
        response = requests.get(f"{API_BASE}/api/listener/rules", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("stats", {})
                print("【规则引擎统计】")
                print(f"  总规则数: {stats.get('total_rules', 0)}")
                print(f"  启用规则: {stats.get('enabled_rules', 0)}")
                print(f"  处理事件: {stats.get('total_events_processed', 0)}")
                print(f"  触发规则: {stats.get('total_rules_triggered', 0)}")
                print()
                
                rules = stats.get('rules', [])
                if rules:
                    print("【规则详情】")
                    for rule in rules:
                        rule_stats = rule.get('stats', {})
                        print(f"  • {rule.get('name', 'N/A')} ({rule.get('rule_id', 'N/A')})")
                        print(f"    启用: {'是' if rule.get('is_enabled') else '否'}")
                        print(f"    触发次数: {rule_stats.get('triggered_count', 0)}")
                        print(f"    成功次数: {rule_stats.get('success_count', 0)}")
                    print()
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取规则统计失败: {e}")
    
    # 通知统计
    try:
        response = requests.get(f"{API_BASE}/api/listener/notifications/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("stats", {})
                print("【通知统计】")
                print(f"  总发送数: {stats.get('total_sent', 0)}")
                print(f"  Info: {stats.get('info_count', 0)}")
                print(f"  Success: {stats.get('success_count', 0)}")
                print(f"  Warning: {stats.get('warning_count', 0)}")
                print(f"  Error: {stats.get('error_count', 0)}")
                print(f"  当前通知数: {stats.get('current_count', 0)}")
                print(f"  未读通知: {stats.get('unread_count', 0)}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取通知统计失败: {e}")


def main():
    """主函数"""
    print("\n" + "="*60)
    print(" 🎯 事件监听器系统演示")
    print("="*60)
    print("\n本演示将展示事件监听器的完整工作流程：")
    print("  1. 检查API服务")
    print("  2. 启动监听器")
    print("  3. 发射测试事件")
    print("  4. 查看自动生成的通知")
    print("  5. 查看统计信息")
    print("\n按 Enter 键开始演示...")
    input()
    
    # 步骤1: 检查API
    if not check_api_health():
        print("\n❌ 演示中止：API服务未运行")
        return
    
    input("\n按 Enter 键继续...")
    
    # 步骤2: 启动监听器
    start_listener()
    
    input("\n按 Enter 键继续...")
    
    # 步骤3: 发射事件
    emit_test_events()
    
    input("\n按 Enter 键查看通知...")
    
    # 步骤4: 查看通知
    view_notifications()
    
    input("\n按 Enter 键查看统计...")
    
    # 步骤5: 查看统计
    view_statistics()
    
    print_section("✅ 演示完成")
    print("事件监听器系统工作正常！")
    print("\n您可以访问以下地址查看更多信息:")
    print(f"  • API文档: {API_BASE}/api/docs")
    print(f"  • 监听器状态: {API_BASE}/api/listener/status")
    print(f"  • 规则列表: {API_BASE}/api/listener/rules")
    print(f"  • 通知列表: {API_BASE}/api/listener/notifications")
    print("\n详细使用说明请参考: REQ-010-D-使用指南.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  演示被用户中断")
    except Exception as e:
        print(f"\n\n❌ 演示出错: {e}")

