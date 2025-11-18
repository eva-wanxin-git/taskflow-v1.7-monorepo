# -*- coding: utf-8 -*-
"""
对话历史库与Session Memory MCP集成

提供对话数据与Session Memory MCP的双向同步接口
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import httpx


router = APIRouter(prefix="/api/conversations/session-memory", tags=["conversations-session-memory"])

# Session Memory MCP服务地址（配置）
SESSION_MEMORY_URL = "http://localhost:5173"  # 默认端口，可通过环境变量覆盖
TIMEOUT = 10


# ============================================================================
# 会话→Session Memory 同步
# ============================================================================

@router.post("/{session_id}/sync-to-session-memory")
async def sync_to_session_memory(session_id: str) -> Dict[str, Any]:
    """
    同步会话到Session Memory MCP
    
    **用途**: 将对话历史库中的会话数据上传到Session Memory MCP服务
    
    **参数**:
    - session_id: 会话ID
    
    **返回**:
    ```json
    {
        "success": true,
        "session_id": "session-001",
        "memory_id": "MEM-12345678",
        "synced_messages": 6,
        "synced_at": "2025-11-18T23:45:00"
    }
    ```
    """
    try:
        from .conversations import find_session, load_conversations
        
        session = find_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 构建Session Memory格式的数据
        session_memory_data = {
            "user_id": "architect",
            "content": _format_session_for_memory(session),
            "metadata": {
                "source": "conversations",
                "session_id": session_id,
                "title": session.get("title"),
                "created_at": session.get("created_at"),
                "participants": session.get("participants", []),
                "tags": session.get("tags", []),
                "total_messages": session.get("messages_count", 0),
                "total_tokens": session.get("total_tokens", 0)
            }
        }
        
        # 调用Session Memory MCP API
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{SESSION_MEMORY_URL}/api/memory/store",
                json=session_memory_data
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Session Memory MCP返回错误: {response.text}"
            )
        
        memory_response = response.json()
        
        return {
            "success": True,
            "session_id": session_id,
            "memory_id": memory_response.get("memory_id", "unknown"),
            "synced_messages": session.get("messages_count", 0),
            "synced_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"同步失败: {str(e)}")


@router.post("/sync-all-to-session-memory")
async def sync_all_to_session_memory() -> Dict[str, Any]:
    """
    同步所有会话到Session Memory MCP
    
    **用途**: 批量将所有对话历史库中的会话上传到Session Memory MCP
    
    **返回**:
    ```json
    {
        "success": true,
        "total_sessions": 5,
        "synced_sessions": 5,
        "failed_sessions": 0,
        "total_messages": 50,
        "synced_at": "2025-11-18T23:45:00"
    }
    ```
    """
    try:
        from .conversations import load_conversations
        
        data = load_conversations()
        sessions = data.get("sessions", [])
        
        synced_count = 0
        failed_count = 0
        total_messages = 0
        
        for session in sessions:
            try:
                session_memory_data = {
                    "user_id": "architect",
                    "content": _format_session_for_memory(session),
                    "metadata": {
                        "source": "conversations",
                        "session_id": session.get("session_id"),
                        "title": session.get("title"),
                        "created_at": session.get("created_at"),
                        "participants": session.get("participants", []),
                        "tags": session.get("tags", []),
                        "total_messages": session.get("messages_count", 0),
                        "total_tokens": session.get("total_tokens", 0)
                    }
                }
                
                async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                    response = await client.post(
                        f"{SESSION_MEMORY_URL}/api/memory/store",
                        json=session_memory_data
                    )
                
                if response.status_code == 200:
                    synced_count += 1
                    total_messages += session.get("messages_count", 0)
                else:
                    failed_count += 1
                    
            except Exception as e:
                failed_count += 1
                continue
        
        return {
            "success": True,
            "total_sessions": len(sessions),
            "synced_sessions": synced_count,
            "failed_sessions": failed_count,
            "total_messages": total_messages,
            "synced_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量同步失败: {str(e)}")


# ============================================================================
# Session Memory → 会话查询
# ============================================================================

@router.get("/retrieve-from-session-memory")
async def retrieve_from_session_memory(
    query: str,
    limit: int = 10
) -> Dict[str, Any]:
    """
    从Session Memory MCP检索相关会话
    
    **用途**: 从Session Memory MCP中搜索相关的会话记忆
    
    **参数**:
    - query: 搜索查询文本
    - limit: 返回结果数量 (默认10)
    
    **返回**:
    ```json
    {
        "success": true,
        "query": "关键词",
        "memories": [
            {
                "memory_id": "MEM-12345678",
                "relevance": 0.95,
                "session_id": "session-001",
                "content": "摘录..."
            }
        ],
        "count": 3
    }
    ```
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(
                f"{SESSION_MEMORY_URL}/api/memory/retrieve",
                params={
                    "query": query,
                    "limit": limit,
                    "user_id": "architect"
                }
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Session Memory MCP返回错误: {response.text}"
            )
        
        memories = response.json()
        
        return {
            "success": True,
            "query": query,
            "memories": memories.get("memories", []),
            "count": len(memories.get("memories", [])),
            "retrieved_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检索失败: {str(e)}")


# ============================================================================
# 会话与Session Memory双向映射
# ============================================================================

@router.post("/{session_id}/map-to-session-memory")
async def map_session_to_memory(
    session_id: str,
    memory_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    创建会话与Session Memory的双向映射
    
    **用途**: 建立对话历史库中的会话与Session Memory中记忆的关联
    
    **参数**:
    - session_id: 会话ID
    - memory_id: Session Memory中的记忆ID (可选)
    
    **返回**:
    ```json
    {
        "success": true,
        "session_id": "session-001",
        "memory_id": "MEM-12345678",
        "mapping_created": true
    }
    ```
    """
    try:
        from .conversations import find_session, load_conversations, save_conversations
        
        session = find_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 添加映射信息到会话元数据
        if "metadata" not in session:
            session["metadata"] = {}
        
        session["metadata"]["memory_id"] = memory_id
        session["metadata"]["mapped_at"] = datetime.now().isoformat()
        
        # 保存
        data = load_conversations()
        save_conversations(data)
        
        return {
            "success": True,
            "session_id": session_id,
            "memory_id": memory_id,
            "mapping_created": True,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"映射失败: {str(e)}")


# ============================================================================
# Session Memory MCP健康检查
# ============================================================================

@router.get("/session-memory/health")
async def check_session_memory_health() -> Dict[str, Any]:
    """
    检查Session Memory MCP服务的健康状态
    
    **用途**: 验证Session Memory MCP服务是否可用
    
    **返回**:
    ```json
    {
        "success": true,
        "session_memory_status": "healthy",
        "url": "http://localhost:5173",
        "checked_at": "2025-11-18T23:45:00"
    }
    ```
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{SESSION_MEMORY_URL}/health")
        
        is_healthy = response.status_code == 200
        
        return {
            "success": True,
            "session_memory_status": "healthy" if is_healthy else "unhealthy",
            "url": SESSION_MEMORY_URL,
            "response_time_ms": response.elapsed.total_seconds() * 1000,
            "checked_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "session_memory_status": "unavailable",
            "url": SESSION_MEMORY_URL,
            "error": str(e),
            "checked_at": datetime.now().isoformat()
        }


# ============================================================================
# 辅助函数
# ============================================================================

def _format_session_for_memory(session: Dict[str, Any]) -> str:
    """
    将会话格式化为Session Memory适用的格式
    
    Args:
        session: 会话数据
        
    Returns:
        格式化的会话内容字符串
    """
    lines = []
    
    # 标题
    lines.append(f"# {session.get('title', '未命名会话')}")
    lines.append("")
    
    # 元数据
    lines.append("## 会话信息")
    lines.append(f"- **创建时间**: {session.get('created_at', '未知')}")
    lines.append(f"- **更新时间**: {session.get('updated_at', '未知')}")
    lines.append(f"- **状态**: {session.get('status', 'unknown')}")
    lines.append(f"- **参与者**: {', '.join(session.get('participants', []))}")
    lines.append(f"- **标签**: {', '.join(session.get('tags', []))}")
    lines.append(f"- **消息总数**: {session.get('messages_count', 0)}")
    lines.append(f"- **Token总消耗**: {session.get('total_tokens', 0)}")
    lines.append("")
    
    # 摘要
    if session.get('summary'):
        lines.append("## 摘要")
        lines.append(session.get('summary'))
        lines.append("")
    
    # 消息列表
    lines.append("## 对话记录")
    messages = session.get('messages', [])
    for msg in messages:
        from_user = msg.get('from', '未知')
        content = msg.get('content', '')
        timestamp = msg.get('timestamp', '')
        tokens = msg.get('tokens', 0)
        
        lines.append(f"### {from_user} ({timestamp}) [{tokens} tokens]")
        lines.append(content)
        lines.append("")
    
    return "\n".join(lines)


# ============================================================================
# 事件驱动的自动同步
# ============================================================================

async def on_conversation_created(session_id: str) -> None:
    """
    会话创建事件处理 - 自动同步到Session Memory
    
    Args:
        session_id: 新创建的会话ID
    """
    try:
        # 延迟1秒确保数据已保存
        import asyncio
        await asyncio.sleep(1)
        
        # 同步到Session Memory
        await sync_to_session_memory(session_id)
        
    except Exception as e:
        print(f"[错误] 自动同步失败: {str(e)}")


async def on_conversation_updated(session_id: str) -> None:
    """
    会话更新事件处理 - 自动同步到Session Memory
    
    Args:
        session_id: 更新的会话ID
    """
    try:
        import asyncio
        await asyncio.sleep(1)
        await sync_to_session_memory(session_id)
        
    except Exception as e:
        print(f"[错误] 自动同步失败: {str(e)}")

