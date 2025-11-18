# -*- coding: utf-8 -*-
"""
事件系统 API 路由

提供事件发射、查询、统计的RESTful API接口
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

# 导入事件服务
import sys
from pathlib import Path
# 添加packages路径到sys.path
packages_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "core-domain" / "src"
sys.path.insert(0, str(packages_path))

from services.event_service import (
    EventEmitter,
    EventStore,
    EventSeverity,
    EventCategory,
    EventSource,
    create_event_emitter,
    create_event_store
)


# ============================================================================
# Pydantic 模型定义
# ============================================================================

class EmitEventRequest(BaseModel):
    """发射事件请求"""
    project_id: str = Field(..., description="项目ID")
    event_type: str = Field(..., description="事件类型，如: task.created, issue.resolved")
    title: str = Field(..., description="事件标题")
    description: Optional[str] = Field(None, description="事件描述")
    data: Optional[Dict[str, Any]] = Field(None, description="事件数据（任意JSON对象）")
    category: str = Field(EventCategory.GENERAL, description="事件分类: task/issue/decision/deployment/system/general")
    source: str = Field(EventSource.SYSTEM, description="事件来源: system/user/ai/external")
    actor: Optional[str] = Field(None, description="操作者")
    severity: str = Field(EventSeverity.INFO, description="严重性: info/warning/error/critical")
    related_entity_type: Optional[str] = Field(None, description="关联实体类型")
    related_entity_id: Optional[str] = Field(None, description="关联实体ID")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    occurred_at: Optional[str] = Field(None, description="事件发生时间（ISO格式），默认为当前时间")


class EmitBatchEventsRequest(BaseModel):
    """批量发射事件请求"""
    project_id: str = Field(..., description="项目ID")
    events: List[Dict[str, Any]] = Field(..., description="事件列表")


class QueryEventsRequest(BaseModel):
    """查询事件请求（用于POST请求）"""
    project_id: Optional[str] = Field(None, description="项目ID过滤")
    event_type: Optional[str] = Field(None, description="事件类型过滤")
    category: Optional[str] = Field(None, description="分类过滤")
    severity: Optional[str] = Field(None, description="严重性过滤")
    actor: Optional[str] = Field(None, description="操作者过滤")
    related_entity_type: Optional[str] = Field(None, description="关联实体类型过滤")
    related_entity_id: Optional[str] = Field(None, description="关联实体ID过滤")
    start_time: Optional[str] = Field(None, description="开始时间过滤（ISO格式）")
    end_time: Optional[str] = Field(None, description="结束时间过滤（ISO格式）")
    limit: int = Field(100, ge=1, le=1000, description="返回数量限制")
    offset: int = Field(0, ge=0, description="偏移量")


# ============================================================================
# API 路由器
# ============================================================================

router = APIRouter(prefix="/api/events", tags=["events"])

# 全局服务实例
_event_store: Optional[EventStore] = None
_event_emitter: Optional[EventEmitter] = None


def get_event_store() -> EventStore:
    """获取事件存储实例"""
    global _event_store
    if _event_store is None:
        _event_store = create_event_store()
    return _event_store


def get_event_emitter() -> EventEmitter:
    """获取事件发射器实例"""
    global _event_emitter
    if _event_emitter is None:
        _event_emitter = create_event_emitter()
    return _event_emitter


# ============================================================================
# 事件发射端点
# ============================================================================

@router.post(
    "",
    summary="发射事件",
    description="发射单个事件到系统"
)
async def emit_event(request: EmitEventRequest) -> Dict[str, Any]:
    """
    发射单个事件
    
    **用途**: 在项目中发生重要事件时调用此API记录
    
    **示例**:
    ```json
    {
        "project_id": "TASKFLOW",
        "event_type": "task.created",
        "title": "任务创建: 实现事件系统",
        "description": "新任务 REQ-010-B 被创建",
        "category": "task",
        "source": "ai",
        "actor": "AI Architect",
        "severity": "info",
        "related_entity_type": "task",
        "related_entity_id": "REQ-010-B",
        "tags": ["task", "created"]
    }
    ```
    """
    try:
        emitter = get_event_emitter()
        event = emitter.emit(
            project_id=request.project_id,
            event_type=request.event_type,
            title=request.title,
            description=request.description,
            data=request.data,
            category=request.category,
            source=request.source,
            actor=request.actor,
            severity=request.severity,
            related_entity_type=request.related_entity_type,
            related_entity_id=request.related_entity_id,
            tags=request.tags,
            occurred_at=request.occurred_at
        )
        
        return {
            "success": True,
            "event": event,
            "message": "Event emitted successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to emit event: {str(e)}"
        )


@router.post(
    "/batch",
    summary="批量发射事件",
    description="批量发射多个事件"
)
async def emit_batch_events(request: EmitBatchEventsRequest) -> Dict[str, Any]:
    """
    批量发射事件
    
    **用途**: 一次性发射多个事件，提高效率
    
    **示例**:
    ```json
    {
        "project_id": "TASKFLOW",
        "events": [
            {
                "event_type": "task.created",
                "title": "任务1创建",
                "category": "task"
            },
            {
                "event_type": "task.created",
                "title": "任务2创建",
                "category": "task"
            }
        ]
    }
    ```
    """
    try:
        emitter = get_event_emitter()
        events = emitter.emit_batch(
            project_id=request.project_id,
            events=request.events
        )
        
        return {
            "success": True,
            "events": events,
            "count": len(events),
            "message": f"Successfully emitted {len(events)} events"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to emit batch events: {str(e)}"
        )


# ============================================================================
# 事件查询端点
# ============================================================================

@router.get(
    "",
    summary="查询事件",
    description="根据条件查询事件列表"
)
async def query_events(
    project_id: Optional[str] = Query(None, description="项目ID过滤"),
    event_type: Optional[str] = Query(None, description="事件类型过滤"),
    category: Optional[str] = Query(None, description="分类过滤"),
    severity: Optional[str] = Query(None, description="严重性过滤"),
    actor: Optional[str] = Query(None, description="操作者过滤"),
    related_entity_type: Optional[str] = Query(None, description="关联实体类型过滤"),
    related_entity_id: Optional[str] = Query(None, description="关联实体ID过滤"),
    start_time: Optional[str] = Query(None, description="开始时间（ISO格式）"),
    end_time: Optional[str] = Query(None, description="结束时间（ISO格式）"),
    limit: int = Query(100, ge=1, le=1000, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量")
) -> Dict[str, Any]:
    """
    查询事件
    
    **用途**: 查询项目的历史事件
    
    **示例**:
    - GET /api/events?project_id=TASKFLOW
    - GET /api/events?project_id=TASKFLOW&category=task&limit=50
    - GET /api/events?project_id=TASKFLOW&severity=error
    - GET /api/events?actor=AI%20Architect
    """
    try:
        store = get_event_store()
        events = store.query(
            project_id=project_id,
            event_type=event_type,
            category=category,
            severity=severity,
            actor=actor,
            related_entity_type=related_entity_type,
            related_entity_id=related_entity_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "events": events,
            "count": len(events),
            "limit": limit,
            "offset": offset,
            "filters": {
                "project_id": project_id,
                "event_type": event_type,
                "category": category,
                "severity": severity,
                "actor": actor,
                "related_entity_type": related_entity_type,
                "related_entity_id": related_entity_id,
                "start_time": start_time,
                "end_time": end_time
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query events: {str(e)}"
        )


@router.get(
    "/{event_id}",
    summary="获取事件详情",
    description="根据ID获取单个事件的详细信息"
)
async def get_event(event_id: str) -> Dict[str, Any]:
    """
    获取事件详情
    
    **用途**: 查看单个事件的完整信息
    """
    try:
        store = get_event_store()
        event = store.get_by_id(event_id)
        
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event not found: {event_id}"
            )
        
        return {
            "success": True,
            "event": event
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get event: {str(e)}"
        )


# ============================================================================
# 事件类型端点
# ============================================================================

@router.get(
    "/types",
    summary="获取事件类型列表",
    description="获取系统支持的所有事件类型"
)
async def get_event_types(
    category: Optional[str] = Query(None, description="分类过滤"),
    is_active: bool = Query(True, description="是否仅返回启用的类型")
) -> Dict[str, Any]:
    """
    获取事件类型列表
    
    **用途**: 查看系统支持的所有事件类型，用于前端下拉框等
    
    **示例**:
    - GET /api/events/types
    - GET /api/events/types?category=task
    """
    try:
        store = get_event_store()
        event_types = store.get_event_types(
            category=category,
            is_active=is_active
        )
        
        return {
            "success": True,
            "event_types": event_types,
            "count": len(event_types),
            "categories": list(set([et["category"] for et in event_types]))
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get event types: {str(e)}"
        )


# ============================================================================
# 事件统计端点
# ============================================================================

@router.get(
    "/stats/{project_id}",
    summary="获取事件统计",
    description="获取项目的事件统计信息"
)
async def get_event_stats(project_id: str) -> Dict[str, Any]:
    """
    获取事件统计
    
    **用途**: Dashboard展示项目的事件统计
    
    **返回内容**:
    - 总事件数
    - 按分类统计
    - 按严重性统计
    - 最后事件时间
    
    **示例**:
    - GET /api/events/stats/TASKFLOW
    """
    try:
        store = get_event_store()
        stats = store.get_stats(project_id)
        
        if not stats or stats.get("total_events", 0) == 0:
            # 如果没有统计数据，返回空统计
            stats = {
                "project_id": project_id,
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
        
        return {
            "success": True,
            "project_id": project_id,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get event stats: {str(e)}"
        )


# ============================================================================
# 便捷端点 - 按实体查询
# ============================================================================

@router.get(
    "/by-entity/{entity_type}/{entity_id}",
    summary="按实体查询事件",
    description="查询与特定实体相关的所有事件"
)
async def query_events_by_entity(
    entity_type: str,
    entity_id: str,
    limit: int = Query(100, ge=1, le=1000)
) -> Dict[str, Any]:
    """
    按实体查询事件
    
    **用途**: 查询某个任务/问题/决策的所有相关事件
    
    **示例**:
    - GET /api/events/by-entity/task/REQ-010-B
    - GET /api/events/by-entity/issue/ISS-001
    """
    try:
        store = get_event_store()
        events = store.query(
            related_entity_type=entity_type,
            related_entity_id=entity_id,
            limit=limit
        )
        
        return {
            "success": True,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "events": events,
            "count": len(events)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query events by entity: {str(e)}"
        )


# ============================================================================
# 健康检查
# ============================================================================

@router.get(
    "/health",
    summary="事件系统健康检查",
    description="检查事件系统的运行状态"
)
async def health_check() -> Dict[str, Any]:
    """事件系统健康检查"""
    try:
        # 尝试查询一个事件来验证数据库连接
        store = get_event_store()
        store.query(limit=1)
        
        return {
            "success": True,
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "emit": "POST /api/events",
                "emit_batch": "POST /api/events/batch",
                "query": "GET /api/events",
                "get_event": "GET /api/events/{event_id}",
                "get_types": "GET /api/events/types",
                "get_stats": "GET /api/events/stats/{project_id}",
                "query_by_entity": "GET /api/events/by-entity/{entity_type}/{entity_id}"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

