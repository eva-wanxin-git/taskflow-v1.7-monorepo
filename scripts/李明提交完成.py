#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
李明提交完成 - 将任务状态从in_progress改为completed

使用方法:
    python scripts/李明提交完成.py TASK-ID
    python scripts/李明提交完成.py REQ-001 --hours 2.5 --summary "功能已完成"

功能:
    1. 调用API: POST /api/tasks/{task_id}/complete
    2. 更新任务状态: in_progress → completed
    3. 记录完成信息（工时、文件、摘要）
"""
import sys
import requests
import argparse
from pathlib import Path

def complete_task(task_id: str, actor: str = "fullstack-engineer", 
                 actual_hours: float = None, files_modified: list = None,
                 completion_summary: str = None):
    """
    李明提交任务完成
    
    Args:
        task_id: 任务ID（如 REQ-001）
        actor: 执行者（默认fullstack-engineer）
        actual_hours: 实际工时
        files_modified: 修改的文件列表
        completion_summary: 完成摘要
    """
    # Dashboard API地址
    api_url = "http://127.0.0.1:8877"
    
    # 构建请求
    url = f"{api_url}/api/tasks/{task_id}/complete"
    payload = {
        "actor": actor,
        "actual_hours": actual_hours,
        "files_modified": files_modified or [],
        "completion_summary": completion_summary or f"任务 {task_id} 已完成"
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("=" * 70)
                print("🎉 任务完成提交成功！")
                print("=" * 70)
                print(f"任务ID: {data['task_id']}")
                print(f"新状态: {data['status']} (已完成)")
                print(f"执行人: {actor}")
                if actual_hours:
                    print(f"实际工时: {actual_hours} 小时")
                if files_modified:
                    print(f"修改文件: {len(files_modified)} 个")
                print("=" * 70)
                print()
                print("💡 下一步:")
                print("   1. 在Dashboard查看完成报告")
                print("   2. 等待架构师审查")
                print("   3. 或继续下一个任务")
                print()
                return True
            else:
                print(f"❌ 提交失败: {data.get('message')}")
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
    parser = argparse.ArgumentParser(
        description="李明提交任务完成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python scripts/李明提交完成.py REQ-001
    python scripts/李明提交完成.py REQ-001 --hours 2.5
    python scripts/李明提交完成.py REQ-001 --hours 3 --summary "功能已完成并测试"
    python scripts/李明提交完成.py REQ-001 --files "file1.py,file2.py"
        """
    )
    
    parser.add_argument("task_id", help="任务ID (如 REQ-001)")
    parser.add_argument("--hours", type=float, help="实际工时（小时）")
    parser.add_argument("--summary", help="完成摘要")
    parser.add_argument("--files", help="修改的文件（逗号分隔）")
    parser.add_argument("--actor", default="fullstack-engineer", help="执行人")
    
    args = parser.parse_args()
    
    # 解析文件列表
    files_modified = None
    if args.files:
        files_modified = [f.strip() for f in args.files.split(",")]
    
    print()
    print("=" * 70)
    print(f"正在提交任务完成: {args.task_id}")
    print("=" * 70)
    print()
    
    success = complete_task(
        task_id=args.task_id,
        actor=args.actor,
        actual_hours=args.hours,
        files_modified=files_modified,
        completion_summary=args.summary
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

