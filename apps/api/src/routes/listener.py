# -*- coding: utf-8 -*-
"""
事件监听器管理 API 路由

提供事件监听器的启动、停止、配置、统计等接口
"""

from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

# 导入服务
from services.event_listener import EventListener, create_event_listener
from services.rule_engine import RuleEngine, create_default_rule_engine
from services.notification_service import NotificationService, create_notification_service


# ============================================================================
# Pydantic 模型定义
# ============================================================================

class StartListenerRequest(BaseModel):
    """启动监听器请求"""
    project_id: str = Field(default="TASKFLOW", description="项目ID")
    poll_interval: int = Field(default=5, ge=1, le=300, description="轮询间隔（秒）")
    max_notifications: int = Field(default=1000, ge=100, le=10000, description="最大通知数量")


class RuleConfigRequest(BaseModel):
    """规则配置请求"""
    rule_id: str = Field(..., description="规则ID")
    is_enabled: bool = Field(..., description="是否启用")


# ============================================================================
# 全局服务实例
# ============================================================================

_event_listener: Optional[EventListener] = None
_rule_engine: Optional[RuleEngine] = None
_notification_service: Optional[NotificationService] = None


def get_or_create_listener() -> EventListener:
    """获取或创建监听器实例"""
    global _event_listener, _rule_engine, _notification_service
    
    if _event_listener is None:
        # 创建通知服务
        _notification_service = create_notification_service()
        
        # 创建规则引擎
        _rule_engine = create_default_rule_engine()
        _rule_engine.set_notification_service(_notification_service)
        
        # 创建事件监听器
        _event_listener = create_event_listener()
        _event_listener.set_rule_engine(_rule_engine)
        _event_listener.set_notification_service(_notification_service)
    
    return _event_listener


def get_rule_engine() -> Optional[RuleEngine]:
    """获取规则引擎"""
    return _rule_engine


def get_notification_service() -> Optional[NotificationService]:
    """获取通知服务"""
    return _notification_service


# ============================================================================
# API 路由器
# ============================================================================

router = APIRouter(prefix="/api/listener", tags=["listener"])


# ============================================================================
# 监听器管理端点
# ============================================================================

@router.post(
    "/start",
    summary="启动事件监听器",
    description="启动事件监听器，开始监听和处理事件"
)
async def start_listener(
    request: StartListenerRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    启动事件监听器
    
    **功能**:
    - 创建或获取监听器实例
    - 配置项目ID和轮询间隔
    - 在后台任务中运行监听器
    
    **示例**:
    ```json
    {
        "project_id": "TASKFLOW",
        "poll_interval": 5,
        "max_notifications": 1000
    }
    ```
    """
    try:
        listener = get_or_create_listener()
        
        # 检查是否已经在运行
        if listener.is_running:
            return {
                "success": False,
                "message": "Listener is already running",
                "stats": listener.get_stats()
            }
        
        # 更新配置
        listener.project_id = request.project_id
        listener.poll_interval = request.poll_interval
        
        # 在后台启动监听器
        background_tasks.add_task(listener.start)
        
        return {
            "success": True,
            "message": "Listener started successfully",
            "config": {
                "project_id": request.project_id,
                "poll_interval": request.poll_interval
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start listener: {str(e)}"
        )


@router.post(
    "/stop",
    summary="停止事件监听器",
    description="停止正在运行的事件监听器"
)
async def stop_listener() -> Dict[str, Any]:
    """
    停止事件监听器
    
    **功能**:
    - 停止监听器轮询
    - 保留统计信息
    
    **示例**:
    - POST /api/listener/stop
    """
    try:
        listener = get_or_create_listener()
        
        if not listener.is_running:
            return {
                "success": False,
                "message": "Listener is not running"
            }
        
        await listener.stop()
        
        return {
            "success": True,
            "message": "Listener stopped successfully",
            "final_stats": listener.get_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop listener: {str(e)}"
        )


@router.get(
    "/status",
    summary="获取监听器状态",
    description="获取事件监听器的运行状态和统计信息"
)
async def get_listener_status() -> Dict[str, Any]:
    """
    获取监听器状态
    
    **返回内容**:
    - 是否运行中
    - 项目ID
    - 轮询间隔
    - 统计信息（处理事件数、错误数等）
    
    **示例**:
    - GET /api/listener/status
    """
    try:
        global _event_listener
        
        if _event_listener is None:
            return {
                "success": True,
                "is_initialized": False,
                "is_running": False,
                "message": "Listener not initialized"
            }
        
        return {
            "success": True,
            "is_initialized": True,
            "status": _event_listener.get_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get listener status: {str(e)}"
        )


# ============================================================================
# 规则管理端点
# ============================================================================

@router.get(
    "/rules",
    summary="获取规则列表",
    description="获取所有已注册的规则及其状态"
)
async def get_rules() -> Dict[str, Any]:
    """
    获取规则列表
    
    **返回内容**:
    - 规则总数
    - 启用的规则数
    - 每个规则的详细信息和统计
    
    **示例**:
    - GET /api/listener/rules
    """
    try:
        engine = get_rule_engine()
        
        if engine is None:
            return {
                "success": False,
                "message": "Rule engine not initialized"
            }
        
        return {
            "success": True,
            "stats": engine.get_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get rules: {str(e)}"
        )


@router.post(
    "/rules/configure",
    summary="配置规则",
    description="启用或禁用指定规则"
)
async def configure_rule(request: RuleConfigRequest) -> Dict[str, Any]:
    """
    配置规则
    
    **功能**:
    - 启用或禁用指定规则
    
    **示例**:
    ```json
    {
        "rule_id": "RULE-001",
        "is_enabled": true
    }
    ```
    """
    try:
        engine = get_rule_engine()
        
        if engine is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rule engine not initialized"
            )
        
        # 启用或禁用规则
        if request.is_enabled:
            success = engine.enable_rule(request.rule_id)
        else:
            success = engine.disable_rule(request.rule_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rule not found: {request.rule_id}"
            )
        
        return {
            "success": True,
            "message": f"Rule {request.rule_id} {'enabled' if request.is_enabled else 'disabled'}",
            "rule_id": request.rule_id,
            "is_enabled": request.is_enabled,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to configure rule: {str(e)}"
        )


# ============================================================================
# 通知管理端点
# ============================================================================

@router.get(
    "/notifications",
    summary="获取通知列表",
    description="获取Dashboard通知列表"
)
async def get_notifications(
    limit: int = 50,
    unread_only: bool = False,
    type_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    获取通知列表
    
    **用途**: Dashboard轮询此接口获取最新通知
    
    **参数**:
    - limit: 返回数量限制（默认50）
    - unread_only: 是否只返回未读通知（默认false）
    - type_filter: 类型过滤（info/success/warning/error）
    
    **示例**:
    - GET /api/listener/notifications?limit=20&unread_only=true
    - GET /api/listener/notifications?type_filter=warning
    """
    try:
        service = get_notification_service()
        
        if service is None:
            return {
                "success": False,
                "message": "Notification service not initialized",
                "notifications": []
            }
        
        notifications = service.get_notifications(
            limit=limit,
            unread_only=unread_only,
            type_filter=type_filter
        )
        
        return {
            "success": True,
            "notifications": notifications,
            "count": len(notifications),
            "unread_count": service.get_unread_count(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notifications: {str(e)}"
        )


@router.post(
    "/notifications/{notification_id}/read",
    summary="标记通知为已读",
    description="标记指定通知为已读状态"
)
async def mark_notification_read(notification_id: str) -> Dict[str, Any]:
    """
    标记通知为已读
    
    **示例**:
    - POST /api/listener/notifications/NOTIF-abc12345/read
    """
    try:
        service = get_notification_service()
        
        if service is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification service not initialized"
            )
        
        success = service.mark_as_read(notification_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification not found: {notification_id}"
            )
        
        return {
            "success": True,
            "message": "Notification marked as read",
            "notification_id": notification_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark notification as read: {str(e)}"
        )


@router.post(
    "/notifications/read-all",
    summary="标记所有通知为已读",
    description="标记所有通知为已读状态"
)
async def mark_all_notifications_read() -> Dict[str, Any]:
    """
    标记所有通知为已读
    
    **示例**:
    - POST /api/listener/notifications/read-all
    """
    try:
        service = get_notification_service()
        
        if service is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification service not initialized"
            )
        
        count = service.mark_all_as_read()
        
        return {
            "success": True,
            "message": f"Marked {count} notifications as read",
            "count": count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark all notifications as read: {str(e)}"
        )


@router.delete(
    "/notifications/{notification_id}",
    summary="删除通知",
    description="删除指定通知"
)
async def delete_notification(notification_id: str) -> Dict[str, Any]:
    """
    删除通知
    
    **示例**:
    - DELETE /api/listener/notifications/NOTIF-abc12345
    """
    try:
        service = get_notification_service()
        
        if service is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification service not initialized"
            )
        
        success = service.delete_notification(notification_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification not found: {notification_id}"
            )
        
        return {
            "success": True,
            "message": "Notification deleted",
            "notification_id": notification_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete notification: {str(e)}"
        )


@router.get(
    "/notifications/stats",
    summary="获取通知统计",
    description="获取通知服务的统计信息"
)
async def get_notification_stats() -> Dict[str, Any]:
    """
    获取通知统计
    
    **返回内容**:
    - 总发送数
    - 各类型通知数量
    - 当前通知数量
    - 未读通知数量
    
    **示例**:
    - GET /api/listener/notifications/stats
    """
    try:
        service = get_notification_service()
        
        if service is None:
            return {
                "success": False,
                "message": "Notification service not initialized"
            }
        
        return {
            "success": True,
            "stats": service.get_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notification stats: {str(e)}"
        )


# ============================================================================
# 健康检查
# ============================================================================

@router.get(
    "/health",
    summary="事件监听器健康检查",
    description="检查事件监听器系统的运行状态"
)
async def health_check() -> Dict[str, Any]:
    """事件监听器系统健康检查"""
    global _event_listener, _rule_engine, _notification_service
    
    return {
        "success": True,
        "status": "healthy",
        "components": {
            "event_listener": {
                "initialized": _event_listener is not None,
                "running": _event_listener.is_running if _event_listener else False
            },
            "rule_engine": {
                "initialized": _rule_engine is not None,
                "rules_count": len(_rule_engine.rules) if _rule_engine else 0
            },
            "notification_service": {
                "initialized": _notification_service is not None,
                "notifications_count": len(_notification_service.notifications) if _notification_service else 0
            }
        },
        "endpoints": {
            "start": "POST /api/listener/start",
            "stop": "POST /api/listener/stop",
            "status": "GET /api/listener/status",
            "rules": "GET /api/listener/rules",
            "notifications": "GET /api/listener/notifications"
        },
        "timestamp": datetime.now().isoformat()
    }

