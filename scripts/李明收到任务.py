#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
李明收到任务 - 将任务状态从pending改为in_progress

使用方法:
    python scripts/李明收到任务.py TASK-ID
    python scripts/李明收到任务.py REQ-001

功能:
    1. 调用API: PUT /api/tasks/{task_id}/received
    2. 更新任务状态: pending → in_progress
    3. 记录事件到事件流
"""
import sys
import requests
from pathlib import Path

def receive_task(task_id: str, actor: str = "fullstack-engineer", notes: str = None):
    """
    李明接收任务
    
    Args:
        task_id: 任务ID（如 REQ-001）
        actor: 执行者（默认fullstack-engineer）
        notes: 备注信息
    """
    # Dashboard API地址
    api_url = "http://127.0.0.1:8877"
    
    # 构建请求
    url = f"{api_url}/api/tasks/{task_id}/received"
    payload = {
        "actor": actor,
        "notes": notes or f"李明开始处理任务 {task_id}"
    }
    
    try:
        # 发送PUT请求
        response = requests.put(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("=" * 70)
                print("✅ 任务接收成功！")
                print("=" * 70)
                print(f"任务ID: {data['task_id']}")
                print(f"新状态: {data['status']} (进行中)")
                print(f"执行人: {data['actor']}")
                print(f"时间: {data.get('timestamp', '刚刚')}")
                print("=" * 70)
                print()
                print("💡 下一步:")
                print("   1. 查看任务详情: 打开 Dashboard")
                print("   2. 开始开发")
                print("   3. 完成后运行: python scripts/李明提交完成.py " + task_id)
                print()
                return True
            else:
                print(f"❌ 接收任务失败: {data.get('message')}")
                return False
        else:
            print(f"❌ API请求失败 (HTTP {response.status_code})")
            print(f"响应: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Dashboard")
        print(f"   请确保Dashboard正在运行: {api_url}")
        print("   启动命令: cd apps/dashboard && python start_dashboard.py")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("=" * 70)
        print("李明收到任务 - 使用说明")
        print("=" * 70)
        print()
        print("使用方法:")
        print("    python scripts/李明收到任务.py TASK-ID")
        print()
        print("示例:")
        print("    python scripts/李明收到任务.py REQ-001")
        print("    python scripts/李明收到任务.py TASK-C1")
        print()
        print("功能:")
        print("    - 将任务状态从 pending 改为 in_progress")
        print("    - 记录任务接收事件")
        print("    - 显示下一步操作提示")
        print()
        print("=" * 70)
        sys.exit(1)
    
    task_id = sys.argv[1]
    notes = sys.argv[2] if len(sys.argv) > 2 else None
    
    print()
    print("=" * 70)
    print(f"正在接收任务: {task_id}")
    print("=" * 70)
    print()
    
    success = receive_task(task_id, notes=notes)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

