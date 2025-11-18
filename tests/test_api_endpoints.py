# -*- coding: utf-8 -*-
"""
API端点快速测试

测试事件系统API是否正常工作
"""

import requests
import sys
import time

API_BASE = "http://localhost:8800"

def test_health():
    """测试健康检查端点"""
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
        if response.status_code == 200:
            print("   [OK] Health check passed")
            return True
        else:
            print(f"   [FAIL] Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   [FAIL] Cannot connect to API server")
        print("   Please start the API server first: python apps/api/start_api.py")
        return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False


def test_emit_event():
    """测试发射事件"""
    print("\n2. Testing emit event endpoint...")
    try:
        response = requests.post(f"{API_BASE}/api/events", json={
            "project_id": "TASKFLOW",
            "event_type": "test.api",
            "title": "API Test Event",
            "description": "This is a test event from API endpoint test",
            "category": "system",
            "source": "system",
            "severity": "info",
            "tags": ["test", "api"]
        }, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                event_id = data["event"]["id"]
                print(f"   [OK] Event emitted: {event_id}")
                return True, event_id
            else:
                print("   [FAIL] Event emit failed")
                return False, None
        else:
            print(f"   [FAIL] HTTP {response.status_code}")
            return False, None
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False, None


def test_query_events():
    """测试查询事件"""
    print("\n3. Testing query events endpoint...")
    try:
        response = requests.get(
            f"{API_BASE}/api/events",
            params={"project_id": "TASKFLOW", "limit": 5},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                count = data.get("count", 0)
                print(f"   [OK] Found {count} events")
                return True
            else:
                print("   [FAIL] Query failed")
                return False
        else:
            print(f"   [FAIL] HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False


def test_get_event(event_id):
    """测试获取单个事件"""
    print("\n4. Testing get event endpoint...")
    if not event_id:
        print("   [SKIP] No event ID to test")
        return True
    
    try:
        response = requests.get(f"{API_BASE}/api/events/{event_id}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"   [OK] Retrieved event: {event_id}")
                return True
            else:
                print("   [FAIL] Get event failed")
                return False
        else:
            print(f"   [FAIL] HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False


def test_get_event_types():
    """测试获取事件类型"""
    print("\n5. Testing get event types endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/events/types", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                count = len(data.get("event_types", []))
                print(f"   [OK] Found {count} event types")
                return True
            else:
                print("   [FAIL] Get types failed")
                return False
        else:
            print(f"   [FAIL] HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False


def test_get_stats():
    """测试获取统计"""
    print("\n6. Testing get stats endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/events/stats/TASKFLOW", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("stats", {})
                total = stats.get("total_events", 0)
                print(f"   [OK] Total events: {total}")
                return True
            else:
                print("   [FAIL] Get stats failed")
                return False
        else:
            print(f"   [FAIL] HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 70)
    print("[TEST] API Endpoints Test")
    print("=" * 70)
    print()
    print("Testing API server at:", API_BASE)
    print()
    
    results = []
    
    # 1. 健康检查
    if not test_health():
        print("\n" + "=" * 70)
        print("[FAIL] API server is not running")
        print("=" * 70)
        print("\nPlease start the API server first:")
        print("  cd apps/api")
        print("  python start_api.py")
        print()
        sys.exit(1)
    
    # 2. 发射事件
    success, event_id = test_emit_event()
    results.append(success)
    
    # 3. 查询事件
    results.append(test_query_events())
    
    # 4. 获取单个事件
    results.append(test_get_event(event_id))
    
    # 5. 获取事件类型
    results.append(test_get_event_types())
    
    # 6. 获取统计
    results.append(test_get_stats())
    
    # 总结
    print("\n" + "=" * 70)
    total = len(results)
    passed = sum(results)
    
    if passed == total:
        print("[PASS] All API tests passed!")
        print("=" * 70)
        print()
        print("API Endpoints Verified:")
        print("   [OK] POST /api/events - Emit event")
        print("   [OK] GET /api/events - Query events")
        print("   [OK] GET /api/events/{id} - Get event")
        print("   [OK] GET /api/events/types - Get event types")
        print("   [OK] GET /api/events/stats/{project_id} - Get statistics")
        print("   [OK] GET /api/health - Health check")
        print()
        sys.exit(0)
    else:
        print(f"[FAIL] {passed}/{total} tests passed")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()

