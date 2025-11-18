#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import sqlite3
from pathlib import Path

print("=" * 60)
print("  检查Dashboard (8877) 显示状态")
print("=" * 60)

# 1. 检查API返回
try:
    resp = requests.get("http://localhost:8877/api/tasks", timeout=3)
    if resp.status_code == 200:
        tasks = resp.json()
        print(f"\n✅ Dashboard API返回: {len(tasks)} 个任务")
        print(f"\n前5个任务:")
        for i, t in enumerate(tasks[:5], 1):
            print(f"  {i}. {t.get('id')}: {t.get('title', '')[:35]}")
    else:
        print(f"\n⚠️ API返回状态码: {resp.status_code}")
except Exception as e:
    print(f"\n❌ 无法访问Dashboard API: {e}")

# 2. 检查数据库
db_path = Path("database/data/tasks.db")
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    status_dist = dict(cursor.fetchall())
    
    print(f"\n✅ 数据库实际有: {total} 个任务")
    print(f"\n状态分布:")
    for status, count in status_dist.items():
        print(f"  {status}: {count}")
    
    conn.close()
else:
    print(f"\n❌ 数据库不存在: {db_path}")

print("\n" + "=" * 60)
print("请在浏览器打开: http://localhost:8877")
print("然后告诉我你看到了多少个任务")
print("=" * 60)

