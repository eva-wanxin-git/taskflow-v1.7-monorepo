#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import sqlite3
from pathlib import Path

print("=" * 60)
print("Dashboard Status Check (Port 8877)")
print("=" * 60)

# 1. Check Dashboard API
try:
    resp = requests.get("http://localhost:8877/api/tasks", timeout=3)
    if resp.status_code == 200:
        tasks = resp.json()
        print(f"\nDashboard API returns: {len(tasks)} tasks")
        print(f"\nFirst 5 tasks:")
        for i, t in enumerate(tasks[:5], 1):
            task_id = t.get('id', 'N/A')
            title = t.get('title', '')[:40]
            status = t.get('status', 'N/A')
            print(f"  {i}. [{status}] {task_id}: {title}")
    else:
        print(f"\nAPI returned status: {resp.status_code}")
except Exception as e:
    print(f"\nCannot access Dashboard API: {e}")

# 2. Check Database
db_path = Path("database/data/tasks.db")
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    print(f"\nDatabase has: {total} tasks")
    print(f"\nStatus distribution:")
    for status, count in cursor.fetchall():
        pct = count / total * 100
        print(f"  {status}: {count} ({pct:.1f}%)")
    
    conn.close()

print("\n" + "=" * 60)
print("Please open: http://localhost:8877")
print("And tell me: How many tasks do you see?")
print("=" * 60)

