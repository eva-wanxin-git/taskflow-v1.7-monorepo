# -*- coding: utf-8 -*-
"""
事件流数据提供器

为Dashboard提供事件流数据
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

# 添加event_service路径
packages_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "core-domain" / "src"
sys.path.insert(0, str(packages_path))

from services.event_service import EventStore, create_event_store


class EventStreamProvider:
    """事件流数据提供器"""
    
    def __init__(self, project_id: str = "TASKFLOW"):
        """
        初始化事件流提供器
        
        Args:
            project_id: 项目ID
        """
        self.project_id = project_id
        self.event_store = create_event_store()
    
    def get_events(
        self,
        event_type: Optional[str] = None,
        category: Optional[str] = None,
        actor: Optional[str] = None,
        severity: Optional[str] = None,
        hours: int = 24,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        获取事件列表
        
        Args:
            event_type: 事件类型过滤
            category: 分类过滤 (task/issue/decision/deployment/system/general)
            actor: 操作者过滤
            severity: 严重性过滤 (info/warning/error/critical)
            hours: 最近N小时的事件
            limit: 返回数量限制
        
        Returns:
            事件列表
        """
        # 计算时间范围
        start_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        # 查询事件
        events = self.event_store.query(
            project_id=self.project_id,
            event_type=event_type,
            category=category,
            actor=actor,
            severity=severity,
            start_time=start_time,
            limit=limit
        )
        
        # 按时间倒序排序
        events.sort(key=lambda e: e.get("occurred_at", ""), reverse=True)
        
        return events
    
    def get_event_stats(self) -> Dict[str, Any]:
        """
        获取事件统计
        
        Returns:
            统计数据字典
        """
        stats = self.event_store.get_stats(self.project_id)
        
        # 如果没有统计数据，返回默认值
        if not stats or stats.get("total_events", 0) == 0:
            stats = {
                "project_id": self.project_id,
                "total_events": 0,
                "task_events": 0,
                "issue_events": 0,
                "decision_events": 0,
                "deployment_events": 0,
                "system_events": 0,
                "info_events": 0,
                "warning_events": 0,
                "error_events": 0,
                "critical_events": 0,
                "last_event_at": None,
                "last_updated": datetime.now().isoformat()
            }
        
        return stats
    
    def get_recent_events(self, hours: int = 1, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取最近的事件（用于实时刷新）
        
        Args:
            hours: 最近N小时
            limit: 数量限制
        
        Returns:
            事件列表
        """
        return self.get_events(hours=hours, limit=limit)
    
    def get_categories_summary(self) -> Dict[str, int]:
        """
        获取各分类事件数量汇总
        
        Returns:
            {category: count}字典
        """
        stats = self.get_event_stats()
        
        return {
            "task": stats.get("task_events", 0),
            "issue": stats.get("issue_events", 0),
            "decision": stats.get("decision_events", 0),
            "deployment": stats.get("deployment_events", 0),
            "system": stats.get("system_events", 0)
        }
    
    def get_severities_summary(self) -> Dict[str, int]:
        """
        获取各严重性事件数量汇总
        
        Returns:
            {severity: count}字典
        """
        stats = self.get_event_stats()
        
        return {
            "info": stats.get("info_events", 0),
            "warning": stats.get("warning_events", 0),
            "error": stats.get("error_events", 0),
            "critical": stats.get("critical_events", 0)
        }
    
    def get_actors_summary(self, hours: int = 24) -> Dict[str, int]:
        """
        获取各操作者的事件数量
        
        Args:
            hours: 统计最近N小时
        
        Returns:
            {actor: count}字典
        """
        events = self.get_events(hours=hours, limit=1000)
        
        actors = {}
        for event in events:
            actor = event.get("actor", "unknown")
            if actor:
                actors[actor] = actors.get(actor, 0) + 1
        
        # 按数量排序
        sorted_actors = dict(sorted(actors.items(), key=lambda item: item[1], reverse=True))
        
        return sorted_actors
    
    def search_events(self, keyword: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        搜索事件（标题或描述包含关键词）
        
        Args:
            keyword: 搜索关键词
            limit: 返回数量限制
        
        Returns:
            匹配的事件列表
        """
        # 获取所有最近事件
        all_events = self.get_events(hours=168, limit=1000)  # 最近7天
        
        # 搜索匹配
        keyword_lower = keyword.lower()
        matched = []
        
        for event in all_events:
            title = (event.get("title") or "").lower()
            description = (event.get("description") or "").lower()
            
            if keyword_lower in title or keyword_lower in description:
                matched.append(event)
                
                if len(matched) >= limit:
                    break
        
        return matched


if __name__ == "__main__":
    # 测试代码
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("===== EventStreamProvider Test =====\n")
    
    provider = EventStreamProvider()
    
    # 测试获取事件
    events = provider.get_recent_events(hours=24, limit=10)
    print(f"Recent events (24h): {len(events)}")
    
    if events:
        print("\nFirst event:")
        first = events[0]
        print(f"  - Type: {first.get('event_type')}")
        print(f"  - Title: {first.get('title')}")
        print(f"  - Time: {first.get('occurred_at')}")
    
    # 测试统计
    stats = provider.get_event_stats()
    print(f"\nTotal events: {stats.get('total_events', 0)}")
    
    # 测试分类汇总
    categories = provider.get_categories_summary()
    print(f"\nCategories:")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}")
    
    print("\n✅ Test completed!")

