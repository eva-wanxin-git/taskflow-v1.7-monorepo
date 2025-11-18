#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断任务列表加载问题
"""

import sys
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

def check_database():
    """检查数据库状态"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # 检查任务总数
        cursor.execute("SELECT COUNT(*) FROM tasks")
        total = cursor.fetchone()[0]
        print(f"[OK] Total tasks in DB: {total}")
        
        # 检查是否有超长description
        cursor.execute("""
            SELECT id, title, LENGTH(description) as len 
            FROM tasks 
            ORDER BY len DESC 
            LIMIT 5
        """)
        print("\n[Check] Longest descriptions:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[2]} chars")
        
        # 检查metadata格式
        cursor.execute("SELECT id, metadata FROM tasks WHERE metadata IS NOT NULL")
        invalid_count = 0
        for row in cursor.fetchall():
            task_id, metadata_str = row
            try:
                if metadata_str:
                    json.loads(metadata_str)
            except:
                print(f"  [ERROR] Invalid JSON in {task_id}")
                invalid_count += 1
        
        if invalid_count == 0:
            print("\n[OK] All metadata JSON valid")
        else:
            print(f"\n[ERROR] {invalid_count} tasks with invalid metadata JSON")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Database check failed: {e}")
        return False

def test_data_provider():
    """测试DataProvider"""
    try:
        # 添加路径
        sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "dashboard" / "src"))
        
        from industrial_dashboard.data_provider import DataProvider
        
        provider = DataProvider(db_path=str(DB_PATH))
        
        print("\n[Test] Loading tasks...")
        tasks = provider.get_tasks()
        
        print(f"[OK] Loaded {len(tasks)} tasks")
        
        if len(tasks) > 0:
            print(f"\n[Sample] First task:")
            first_task = tasks[0]
            print(f"  ID: {first_task.id}")
            print(f"  Title: {first_task.title}")
            print(f"  Status: {first_task.status}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] DataProvider failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("[Diagnosis] Task list loading issue")
    print("=" * 60)
    print()
    
    # 检查数据库
    print("[Step 1] Check database...")
    db_ok = check_database()
    
    if not db_ok:
        print("\n[FAIL] Database check failed")
        return
    
    # 测试DataProvider
    print("\n[Step 2] Test DataProvider...")
    provider_ok = test_data_provider()
    
    print()
    print("=" * 60)
    if db_ok and provider_ok:
        print("[SUCCESS] Both checks passed - issue may be frontend")
    else:
        print("[FAILED] Found backend issues")
    print("=" * 60)

if __name__ == "__main__":
    main()

