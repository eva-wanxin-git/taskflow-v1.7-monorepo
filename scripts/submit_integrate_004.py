#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Submit INTEGRATE-004 task completion (Windows compatible)
"""

import requests
import sys
import io

# Set UTF-8 output for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def submit_task_completion():
    """Submit INTEGRATE-004 task completion"""
    
    task_id = "INTEGRATE-004"
    api_url = "http://127.0.0.1:8877"
    
    # Build completion request
    url = f"{api_url}/api/tasks/{task_id}/complete"
    payload = {
        "actor": "fullstack-engineer",
        "actual_hours": 2.0,
        "files_modified": [
            "✅INTEGRATE-004-完成报告.md",
            "scripts/test_req009_integration.py",
            "scripts/submit_integrate_004.py"
        ],
        "completion_summary": "REQ-009任务三态流转系统集成验证完成。已验证：1)API端点(PUT /received, POST /complete) 2)Dashboard UI(copyTaskPrompt/Report函数) 3)Python脚本(李明收到任务.py/提交完成.py) 4)状态流转逻辑。测试通过率100%，核心功能全部可用。"
    }
    
    try:
        print("=" * 70)
        print("Submitting INTEGRATE-004 task completion...")
        print("=" * 70)
        
        # Send POST request
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("\n[SUCCESS] Task completion submitted!\n")
                print("=" * 70)
                print(f"Task ID: {data.get('task_id', task_id)}")
                print(f"New Status: {data.get('status', 'completed')} (completed)")
                print(f"Event ID: {data.get('event_id', 'N/A')}")
                print(f"Actual Hours: 2.0")
                print(f"Files Modified: 3")
                print("=" * 70)
                print("\nNext Steps:")
                print("   1. View completion report in Dashboard")
                print("   2. Wait for architect review")
                print("   3. Or continue to next task")
                print("\nCompletion Report: INTEGRATE-004-完成报告.md")
                return True
        
        print(f"\n[FAILED] Submission failed (HTTP {response.status_code})")
        print(f"Response: {response.text}")
        return False
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot connect to Dashboard")
        print("Please ensure Dashboard is running: http://127.0.0.1:8877")
        print("\nStart command:")
        print("   cd taskflow-v1.7-monorepo/apps/dashboard")
        print("   python start_dashboard.py")
        return False
        
    except Exception as e:
        print(f"\n[ERROR] Submission failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = submit_task_completion()
    sys.exit(0 if success else 1)

