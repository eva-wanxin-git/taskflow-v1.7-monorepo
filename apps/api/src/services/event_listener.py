# -*- coding: utf-8 -*-
"""
事件监听器（Event Listener）

功能：
1. 轮询事件流，监听新事件
2. 根据规则引擎处理事件
3. 触发通知机制

设计：
- 采用轮询方式（简单可靠）
- 可扩展为WebSocket（Phase 2）
- 支持多规则并发执行
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 添加packages路径
packages_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "core-domain" / "src"
sys.path.insert(0, str(packages_path))

from services.event_service import EventStore, create_event_store, EventCategory, EventSeverity


# ============================================================================
# 事件监听器
# ============================================================================

class EventListener:
    """
    事件监听器
    
    采用轮询方式监听事件，并根据规则引擎处理
    """
    
    def __init__(
        self, 
        event_store: Optional[EventStore] = None,
        poll_interval: int = 5,
        project_id: str = "TASKFLOW"
    ):
        """
        初始化事件监听器
        
        Args:
            event_store: 事件存储实例，如果为None则创建新实例
            poll_interval: 轮询间隔（秒）
            project_id: 监听的项目ID
        """
        self.event_store = event_store or create_event_store()
        self.poll_interval = poll_interval
        self.project_id = project_id
        self.logger = logging.getLogger(__name__)
        
        # 监听状态
        self.is_running = False
        self.last_poll_time: Optional[datetime] = None
        self.processed_event_ids: set = set()
        
        # 规则引擎和通知服务（延迟注入）
        self.rule_engine: Optional['RuleEngine'] = None
        self.notification_service: Optional['NotificationService'] = None
        
        # 统计信息
        self.stats = {
            "total_polled": 0,
            "total_processed": 0,
            "total_errors": 0,
            "started_at": None,
            "last_poll_at": None
        }
    
    def set_rule_engine(self, rule_engine: 'RuleEngine') -> None:
        """设置规则引擎"""
        self.rule_engine = rule_engine
        self.logger.info("Rule engine set for EventListener")
    
    def set_notification_service(self, notification_service: 'NotificationService') -> None:
        """设置通知服务"""
        self.notification_service = notification_service
        self.logger.info("Notification service set for EventListener")
    
    async def start(self) -> None:
        """启动监听器"""
        if self.is_running:
            self.logger.warning("EventListener is already running")
            return
        
        self.is_running = True
        self.stats["started_at"] = datetime.now().isoformat()
        self.last_poll_time = datetime.now() - timedelta(seconds=self.poll_interval)
        
        self.logger.info(f"EventListener started for project: {self.project_id}")
        self.logger.info(f"Poll interval: {self.poll_interval}s")
        
        # 开始轮询循环
        try:
            while self.is_running:
                await self._poll_and_process()
                await asyncio.sleep(self.poll_interval)
        except Exception as e:
            self.logger.error(f"EventListener error: {e}", exc_info=True)
            self.is_running = False
    
    async def stop(self) -> None:
        """停止监听器"""
        self.logger.info("Stopping EventListener...")
        self.is_running = False
    
    async def _poll_and_process(self) -> None:
        """轮询并处理新事件"""
        try:
            # 查询从上次轮询以来的新事件
            now = datetime.now()
            start_time = self.last_poll_time.isoformat() if self.last_poll_time else None
            
            # 查询新事件
            events = self.event_store.query(
                project_id=self.project_id,
                start_time=start_time,
                limit=100
            )
            
            # 更新轮询时间
            self.last_poll_time = now
            self.stats["last_poll_at"] = now.isoformat()
            self.stats["total_polled"] += len(events)
            
            # 过滤未处理的事件
            new_events = [
                event for event in events 
                if event["id"] not in self.processed_event_ids
            ]
            
            if new_events:
                self.logger.info(f"Found {len(new_events)} new events to process")
                
                # 处理每个新事件
                for event in new_events:
                    await self._process_event(event)
            
        except Exception as e:
            self.logger.error(f"Error in poll_and_process: {e}", exc_info=True)
            self.stats["total_errors"] += 1
    
    async def _process_event(self, event: Dict[str, Any]) -> None:
        """
        处理单个事件
        
        Args:
            event: 事件对象
        """
        try:
            event_id = event["id"]
            event_type = event["event_type"]
            
            self.logger.debug(f"Processing event: {event_id} ({event_type})")
            
            # 标记为已处理
            self.processed_event_ids.add(event_id)
            self.stats["total_processed"] += 1
            
            # 如果有规则引擎，执行规则匹配
            if self.rule_engine:
                await self.rule_engine.process_event(event)
            else:
                self.logger.warning("No rule engine configured, event not processed")
            
        except Exception as e:
            self.logger.error(f"Error processing event {event.get('id', 'unknown')}: {e}", exc_info=True)
            self.stats["total_errors"] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取监听器统计信息"""
        return {
            **self.stats,
            "is_running": self.is_running,
            "project_id": self.project_id,
            "poll_interval": self.poll_interval,
            "processed_event_count": len(self.processed_event_ids)
        }
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        self.stats = {
            "total_polled": 0,
            "total_processed": 0,
            "total_errors": 0,
            "started_at": self.stats.get("started_at"),
            "last_poll_at": None
        }
        self.processed_event_ids.clear()
        self.logger.info("EventListener stats reset")


# ============================================================================
# 便捷函数
# ============================================================================

def create_event_listener(
    project_id: str = "TASKFLOW",
    poll_interval: int = 5
) -> EventListener:
    """
    创建事件监听器实例
    
    Args:
        project_id: 项目ID
        poll_interval: 轮询间隔（秒）
    
    Returns:
        EventListener实例
    """
    return EventListener(
        project_id=project_id,
        poll_interval=poll_interval
    )

