# -*- coding: utf-8 -*-
"""
通知服务（Notification Service）

功能：
1. 发送Dashboard弹窗通知
2. 管理通知队列
3. 支持不同通知类型：info/success/warning/error
4. （可选）系统托盘通知

设计：
- 通知存储在内存队列中
- Dashboard通过API轮询获取通知
- 未来可扩展WebSocket推送
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import deque
from enum import Enum
import uuid


# ============================================================================
# 通知类型枚举
# ============================================================================

class NotificationType(str, Enum):
    """通知类型"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


# ============================================================================
# 通知服务
# ============================================================================

class NotificationService:
    """
    通知服务
    
    管理通知的创建、存储和获取
    """
    
    def __init__(self, max_notifications: int = 1000):
        """
        初始化通知服务
        
        Args:
            max_notifications: 最大通知数量（超过时删除旧通知）
        """
        self.notifications: deque = deque(maxlen=max_notifications)
        self.logger = logging.getLogger(__name__)
        
        # 统计信息
        self.stats = {
            "total_sent": 0,
            "info_count": 0,
            "success_count": 0,
            "warning_count": 0,
            "error_count": 0,
            "started_at": datetime.now().isoformat()
        }
    
    def send_notification(
        self,
        title: str,
        message: str,
        type: str = NotificationType.INFO,
        data: Optional[Dict[str, Any]] = None,
        duration: int = 5000,
        priority: int = 0
    ) -> Dict[str, Any]:
        """
        发送通知
        
        Args:
            title: 通知标题
            message: 通知内容
            type: 通知类型 (info/success/warning/error)
            data: 附加数据
            duration: 显示时长（毫秒），0表示不自动关闭
            priority: 优先级（数值越大优先级越高）
        
        Returns:
            创建的通知对象
        """
        notification_id = f"NOTIF-{uuid.uuid4().hex[:8]}"
        
        notification = {
            "id": notification_id,
            "title": title,
            "message": message,
            "type": type,
            "data": data or {},
            "duration": duration,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "read": False
        }
        
        # 添加到队列
        self.notifications.append(notification)
        
        # 更新统计
        self.stats["total_sent"] += 1
        if type == NotificationType.INFO:
            self.stats["info_count"] += 1
        elif type == NotificationType.SUCCESS:
            self.stats["success_count"] += 1
        elif type == NotificationType.WARNING:
            self.stats["warning_count"] += 1
        elif type == NotificationType.ERROR:
            self.stats["error_count"] += 1
        
        self.logger.info(f"Notification sent: [{type}] {title}")
        
        return notification
    
    def get_notifications(
        self,
        limit: int = 50,
        unread_only: bool = False,
        type_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取通知列表
        
        Args:
            limit: 返回数量限制
            unread_only: 是否只返回未读通知
            type_filter: 类型过滤
        
        Returns:
            通知列表（最新的在前）
        """
        # 转换为列表（最新的在前）
        notifications = list(reversed(self.notifications))
        
        # 过滤
        if unread_only:
            notifications = [n for n in notifications if not n["read"]]
        
        if type_filter:
            notifications = [n for n in notifications if n["type"] == type_filter]
        
        # 限制数量
        return notifications[:limit]
    
    def mark_as_read(self, notification_id: str) -> bool:
        """
        标记通知为已读
        
        Args:
            notification_id: 通知ID
        
        Returns:
            是否成功
        """
        for notification in self.notifications:
            if notification["id"] == notification_id:
                notification["read"] = True
                self.logger.debug(f"Notification marked as read: {notification_id}")
                return True
        return False
    
    def mark_all_as_read(self) -> int:
        """
        标记所有通知为已读
        
        Returns:
            标记数量
        """
        count = 0
        for notification in self.notifications:
            if not notification["read"]:
                notification["read"] = True
                count += 1
        
        self.logger.info(f"Marked {count} notifications as read")
        return count
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        删除通知
        
        Args:
            notification_id: 通知ID
        
        Returns:
            是否成功
        """
        for i, notification in enumerate(self.notifications):
            if notification["id"] == notification_id:
                del self.notifications[i]
                self.logger.debug(f"Notification deleted: {notification_id}")
                return True
        return False
    
    def clear_all(self, type_filter: Optional[str] = None) -> int:
        """
        清空通知
        
        Args:
            type_filter: 类型过滤（可选）
        
        Returns:
            清除数量
        """
        if type_filter:
            # 只清除指定类型
            before_count = len(self.notifications)
            self.notifications = deque(
                [n for n in self.notifications if n["type"] != type_filter],
                maxlen=self.notifications.maxlen
            )
            count = before_count - len(self.notifications)
        else:
            # 清空全部
            count = len(self.notifications)
            self.notifications.clear()
        
        self.logger.info(f"Cleared {count} notifications")
        return count
    
    def get_unread_count(self) -> int:
        """获取未读通知数量"""
        return sum(1 for n in self.notifications if not n["read"])
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "current_count": len(self.notifications),
            "unread_count": self.get_unread_count(),
            "max_notifications": self.notifications.maxlen
        }


# ============================================================================
# 便捷通知方法
# ============================================================================

class NotificationHelper:
    """
    通知助手类
    
    提供便捷的通知发送方法
    """
    
    def __init__(self, service: NotificationService):
        """
        初始化通知助手
        
        Args:
            service: 通知服务实例
        """
        self.service = service
    
    def info(self, title: str, message: str, **kwargs) -> Dict[str, Any]:
        """发送信息通知"""
        return self.service.send_notification(
            title=title,
            message=message,
            type=NotificationType.INFO,
            **kwargs
        )
    
    def success(self, title: str, message: str, **kwargs) -> Dict[str, Any]:
        """发送成功通知"""
        return self.service.send_notification(
            title=title,
            message=message,
            type=NotificationType.SUCCESS,
            **kwargs
        )
    
    def warning(self, title: str, message: str, **kwargs) -> Dict[str, Any]:
        """发送警告通知"""
        return self.service.send_notification(
            title=title,
            message=message,
            type=NotificationType.WARNING,
            **kwargs
        )
    
    def error(self, title: str, message: str, **kwargs) -> Dict[str, Any]:
        """发送错误通知"""
        return self.service.send_notification(
            title=title,
            message=message,
            type=NotificationType.ERROR,
            **kwargs
        )
    
    def task_completed(self, task_id: str, task_title: str) -> Dict[str, Any]:
        """任务完成通知"""
        return self.success(
            title="✅ 任务完成",
            message=f"任务 {task_id} 已完成: {task_title}",
            data={"task_id": task_id}
        )
    
    def task_review_required(self, task_id: str) -> Dict[str, Any]:
        """任务需要审查通知"""
        return self.info(
            title="📋 需要审查",
            message=f"任务 {task_id} 等待架构师审查",
            data={"task_id": task_id, "action": "review"}
        )
    
    def issue_detected(self, issue_id: str, severity: str) -> Dict[str, Any]:
        """问题检测通知"""
        type_map = {
            "critical": NotificationType.ERROR,
            "high": NotificationType.ERROR,
            "medium": NotificationType.WARNING,
            "low": NotificationType.INFO
        }
        return self.service.send_notification(
            title="⚠️ 问题检测",
            message=f"检测到 {severity} 级别问题: {issue_id}",
            type=type_map.get(severity, NotificationType.WARNING),
            data={"issue_id": issue_id, "severity": severity}
        )


# ============================================================================
# 便捷函数
# ============================================================================

def create_notification_service(max_notifications: int = 1000) -> NotificationService:
    """
    创建通知服务实例
    
    Args:
        max_notifications: 最大通知数量
    
    Returns:
        NotificationService实例
    """
    return NotificationService(max_notifications=max_notifications)


def create_notification_helper(service: NotificationService) -> NotificationHelper:
    """
    创建通知助手
    
    Args:
        service: 通知服务实例
    
    Returns:
        NotificationHelper实例
    """
    return NotificationHelper(service)

