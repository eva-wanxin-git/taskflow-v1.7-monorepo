#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复 - 简化任务加载，避免复杂查询
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

def test_simple_query():
    """测试最简单的查询"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # 最简单查询
        cursor.execute("SELECT id, title, status FROM tasks LIMIT 5")
        rows = cursor.fetchall()
        
        print("[OK] Simple query works:")
        for row in rows:
            print(f"  {row[0]}: {row[1]} ({row[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Even simple query failed: {e}")
        return False

def check_api_endpoint():
    """检查API端点"""
    import requests
    
    try:
        # 测试健康检查
        response = requests.get("http://localhost:8877/health", timeout=2)
        print(f"\n[Health Check] Status: {response.status_code}")
        
        # 测试tasks API
        response = requests.get("http://localhost:8877/api/tasks", timeout=5)
        print(f"[Tasks API] Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"[Tasks API] Returned {len(data)} tasks")
            else:
                print(f"[Tasks API] Returned: {data}")
        else:
            print(f"[Tasks API] Error: {response.text[:200]}")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot connect to Dashboard (not running?)")
        return False
    except Exception as e:
        print(f"\n[ERROR] API check failed: {e}")
        return False

def main():
    print("=" * 60)
    print("[Quick Fix] Diagnose task loading")
    print("=" * 60)
    print()
    
    print("[Step 1] Test database query...")
    db_ok = test_simple_query()
    
    if not db_ok:
        print("\n[FAIL] Database has issues")
        return
    
    print("\n[Step 2] Test API endpoint...")
    api_ok = check_api_endpoint()
    
    print()
    print("=" * 60)
    if api_ok:
        print("[RESULT] API works - issue is frontend JavaScript")
    else:
        print("[RESULT] API broken - need to fix backend")
    print("=" * 60)

if __name__ == "__main__":
    main()

