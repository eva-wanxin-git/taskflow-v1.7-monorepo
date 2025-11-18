#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提交INTEGRATE-004任务完成
"""

import requests
import sys

def submit_task_completion():
    """提交INTEGRATE-004任务完成"""
    
    task_id = "INTEGRATE-004"
    api_url = "http://127.0.0.1:8877"
    
    # 构建完成请求
    url = f"{api_url}/api/tasks/{task_id}/complete"
    payload = {
        "actor": "fullstack-engineer",
        "actual_hours": 2.0,
        "files_modified": [
            "✅INTEGRATE-004-完成报告.md",
            "scripts/test_req009_integration.py",
            "scripts/提交INTEGRATE-004.py"
        ],
        "completion_summary": "REQ-009任务三态流转系统集成验证完成。已验证：1)API端点(PUT /received, POST /complete) 2)Dashboard UI(copyTaskPrompt/Report函数) 3)Python脚本(李明收到任务.py/提交完成.py) 4)状态流转逻辑。测试通过率100%，核心功能全部可用。"
    }
    
    try:
        print("=" * 70)
        print("正在提交INTEGRATE-004任务完成...")
        print("=" * 70)
        
        # 发送POST请求
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("\n✅ 任务完成提交成功！\n")
                print("=" * 70)
                print(f"任务ID: {data.get('task_id', task_id)}")
                print(f"新状态: {data.get('status', 'completed')} (已完成)")
                print(f"事件ID: {data.get('event_id', 'N/A')}")
                print(f"实际工时: 2.0 小时")
                print(f"修改文件: 3 个")
                print("=" * 70)
                print("\n💡 下一步:")
                print("   1. 在Dashboard查看完成报告")
                print("   2. 等待架构师审查")
                print("   3. 或继续下一个任务")
                print("\n完成报告: ✅INTEGRATE-004-完成报告.md")
                return True
        
        print(f"\n❌ 提交失败 (HTTP {response.status_code})")
        print(f"响应: {response.text}")
        return False
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到Dashboard")
        print("请确认Dashboard正在运行: http://127.0.0.1:8877")
        print("\n启动命令:")
        print("   cd taskflow-v1.7-monorepo/apps/dashboard")
        print("   python start_dashboard.py")
        return False
        
    except Exception as e:
        print(f"\n❌ 提交失败: {e}")
        return False

if __name__ == "__main__":
    success = submit_task_completion()
    sys.exit(0 if success else 1)

