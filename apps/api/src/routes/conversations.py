# -*- coding: utf-8 -*-
"""
对话历史库 API 路由

提供会话管理的RESTful API接口，支持：
- 会话CRUD操作
- 消息管理
- 会话标签管理
- 会话统计功能
- Session Memory MCP集成
"""

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json

# ============================================================================
# Pydantic 模型定义
# ============================================================================

class MessageModel(BaseModel):
    """消息模型"""
    id: Optional[str] = Field(None, description="消息ID")
    timestamp: str = Field(..., description="时间戳")
    from_user: str = Field(..., alias="from", description="发送者")
    content: str = Field(..., description="消息内容")
    type: str = Field("request", description="消息类型: request/response")
    tokens: int = Field(0, description="Token消耗")

    class Config:
        allow_population_by_field_name = True


class ConversationModel(BaseModel):
    """会话模型"""
    session_id: Optional[str] = Field(None, description="会话ID")
    title: str = Field(..., description="会话标题")
    created_at: Optional[str] = Field(None, description="创建时间")
    updated_at: Optional[str] = Field(None, description="更新时间")
    status: str = Field("active", description="会话状态: active/completed/archived")
    total_tokens: int = Field(0, description="总Token消耗")
    messages_count: int = Field(0, description="消息总数")
    participants: List[str] = Field(["用户", "架构师AI"], description="参与者列表")
    tags: List[str] = Field([], description="标签列表")
    summary: str = Field("", description="会话摘要")
    messages: Optional[List[Dict[str, Any]]] = Field([], description="消息列表")


class CreateMessageRequest(BaseModel):
    """创建消息请求"""
    from_user: str = Field(..., alias="from", description="发送者")
    content: str = Field(..., description="消息内容")
    type: str = Field("request", description="消息类型")
    tokens: int = Field(0, description="Token消耗")

    class Config:
        allow_population_by_field_name = True


class UpdateConversationRequest(BaseModel):
    """更新会话请求"""
    title: Optional[str] = Field(None, description="会话标题")
    status: Optional[str] = Field(None, description="会话状态")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    summary: Optional[str] = Field(None, description="会话摘要")


# ============================================================================
# API 路由器
# ============================================================================

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

# 数据文件路径
DATA_FILE = Path("automation-data/architect-conversations.json")


# ============================================================================
# 辅助函数
# ============================================================================

def load_conversations() -> Dict[str, Any]:
    """加载会话数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"sessions": []}


def save_conversations(data: Dict[str, Any]) -> None:
    """保存会话数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_session(session_id: str) -> Optional[Dict[str, Any]]:
    """查找会话"""
    data = load_conversations()
    sessions = data.get("sessions", [])
    return next((s for s in sessions if s["session_id"] == session_id), None)


def generate_session_id() -> str:
    """生成唯一的会话ID"""
    data = load_conversations()
    sessions = data.get("sessions", [])
    count = len(sessions)
    return f"session-{str(count + 1).zfill(3)}"


def generate_message_id(session_id: str) -> str:
    """生成唯一的消息ID"""
    session = find_session(session_id)
    if not session:
        return "msg-001"
    messages = session.get("messages", [])
    count = len(messages)
    return f"msg-{str(count + 1).zfill(3)}"


# ============================================================================
# 1. 获取所有会话 (GET /api/conversations)
# ============================================================================

@router.get("")
async def get_all_conversations() -> Dict[str, Any]:
    """
    获取所有对话会话
    
    **用途**: 获取系统中的所有对话会话列表
    
    **返回**: 
    ```json
    {
        "success": true,
        "sessions": [
            {
                "session_id": "session-001",
                "title": "会话标题",
                ...
            }
        ],
        "count": 3
    }
    ```
    """
    try:
        data = load_conversations()
        sessions = data.get("sessions", [])
        
        return {
            "success": True,
            "sessions": sessions,
            "count": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话失败: {str(e)}")


# ============================================================================
# 2. 获取单个会话 (GET /api/conversations/{session_id})
# ============================================================================

@router.get("/{session_id}")
async def get_conversation(session_id: str) -> Dict[str, Any]:
    """
    获取单个对话会话详情
    
    **用途**: 获取指定会话的完整信息，包括所有消息
    
    **参数**:
    - session_id: 会话ID (如 session-001)
    
    **返回**:
    ```json
    {
        "success": true,
        "session": {
            "session_id": "session-001",
            "title": "会话标题",
            "messages": [...]
        }
    }
    ```
    """
    try:
        session = find_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        return {
            "success": True,
            "session": session,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话失败: {str(e)}")


# ============================================================================
# 3. 创建新会话 (POST /api/conversations)
# ============================================================================

@router.post("")
async def create_conversation(conversation: ConversationModel) -> Dict[str, Any]:
    """
    创建新的对话会话
    
    **用途**: 开启一个新的对话会话
    
    **请求体**:
    ```json
    {
        "title": "新会话标题",
        "participants": ["用户", "架构师AI"],
        "tags": ["标签1", "标签2"],
        "summary": "会话摘要"
    }
    ```
    
    **返回**:
    ```json
    {
        "success": true,
        "session": {...},
        "session_id": "session-001"
    }
    ```
    """
    try:
        data = load_conversations()
        
        # 生成新会话ID
        session_id = generate_session_id()
        
        # 创建新会话
        new_session = {
            "session_id": session_id,
            "title": conversation.title,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active",
            "total_tokens": 0,
            "messages_count": 0,
            "participants": conversation.participants,
            "tags": conversation.tags,
            "summary": conversation.summary,
            "messages": []
        }
        
        # 添加到列表（最新的在前）
        sessions = data.get("sessions", [])
        sessions.insert(0, new_session)
        data["sessions"] = sessions
        
        # 保存
        save_conversations(data)
        
        return {
            "success": True,
            "session": new_session,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建会话失败: {str(e)}")


# ============================================================================
# 4. 更新会话 (PUT /api/conversations/{session_id})
# ============================================================================

@router.put("/{session_id}")
async def update_conversation(
    session_id: str,
    update_req: UpdateConversationRequest
) -> Dict[str, Any]:
    """
    更新对话会话信息
    
    **用途**: 更新会话的标题、状态、标签等信息
    
    **参数**:
    - session_id: 会话ID
    
    **请求体**:
    ```json
    {
        "title": "新标题",
        "status": "completed",
        "tags": ["新标签"],
        "summary": "新摘要"
    }
    ```
    
    **返回**:
    ```json
    {
        "success": true,
        "session": {...}
    }
    ```
    """
    try:
        data = load_conversations()
        sessions = data.get("sessions", [])
        session = next((s for s in sessions if s["session_id"] == session_id), None)
        
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 更新字段
        if update_req.title:
            session["title"] = update_req.title
        if update_req.status:
            session["status"] = update_req.status
        if update_req.tags is not None:
            session["tags"] = update_req.tags
        if update_req.summary:
            session["summary"] = update_req.summary
        
        session["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存
        save_conversations(data)
        
        return {
            "success": True,
            "session": session,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新会话失败: {str(e)}")


# ============================================================================
# 5. 删除会话 (DELETE /api/conversations/{session_id})
# ============================================================================

@router.delete("/{session_id}")
async def delete_conversation(session_id: str) -> Dict[str, Any]:
    """
    删除对话会话
    
    **用途**: 删除指定的对话会话（不可恢复）
    
    **参数**:
    - session_id: 会话ID
    
    **返回**:
    ```json
    {
        "success": true,
        "message": "会话已删除",
        "deleted_session_id": "session-001"
    }
    ```
    """
    try:
        data = load_conversations()
        sessions = data.get("sessions", [])
        
        # 查找并删除
        original_count = len(sessions)
        sessions = [s for s in sessions if s["session_id"] != session_id]
        
        if len(sessions) == original_count:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        data["sessions"] = sessions
        save_conversations(data)
        
        return {
            "success": True,
            "message": "会话已删除",
            "deleted_session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除会话失败: {str(e)}")


# ============================================================================
# 6. 添加消息到会话 (POST /api/conversations/{session_id}/messages)
# ============================================================================

@router.post("/{session_id}/messages")
async def add_message(
    session_id: str,
    message: CreateMessageRequest
) -> Dict[str, Any]:
    """
    向会话添加消息
    
    **用途**: 向指定会话添加新消息
    
    **参数**:
    - session_id: 会话ID
    
    **请求体**:
    ```json
    {
        "from": "用户",
        "content": "消息内容",
        "type": "request",
        "tokens": 500
    }
    ```
    
    **返回**:
    ```json
    {
        "success": true,
        "message": {...},
        "updated_session": {...}
    }
    ```
    """
    try:
        data = load_conversations()
        sessions = data.get("sessions", [])
        session = next((s for s in sessions if s["session_id"] == session_id), None)
        
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 生成消息ID
        msg_id = generate_message_id(session_id)
        
        # 创建消息
        new_message = {
            "id": msg_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "from": message.from_user,
            "content": message.content,
            "type": message.type,
            "tokens": message.tokens
        }
        
        # 添加到会话
        if "messages" not in session:
            session["messages"] = []
        
        session["messages"].append(new_message)
        session["messages_count"] = len(session["messages"])
        session["total_tokens"] = sum(m.get("tokens", 0) for m in session["messages"])
        session["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存
        save_conversations(data)
        
        return {
            "success": True,
            "message": new_message,
            "updated_session": session,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加消息失败: {str(e)}")


# ============================================================================
# 7. 获取会话消息列表 (GET /api/conversations/{session_id}/messages)
# ============================================================================

@router.get("/{session_id}/messages")
async def get_messages(session_id: str) -> Dict[str, Any]:
    """
    获取会话的所有消息
    
    **用途**: 获取指定会话的消息列表
    
    **参数**:
    - session_id: 会话ID
    
    **返回**:
    ```json
    {
        "success": true,
        "messages": [...],
        "count": 6
    }
    ```
    """
    try:
        session = find_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        messages = session.get("messages", [])
        
        return {
            "success": True,
            "messages": messages,
            "count": len(messages),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取消息失败: {str(e)}")


# ============================================================================
# 8. 获取会话标签列表 (GET /api/conversations/tags)
# ============================================================================

@router.get("/tags/list")
async def get_conversation_tags() -> Dict[str, Any]:
    """
    获取所有会话标签
    
    **用途**: 获取系统中所有已使用的标签及其统计信息
    
    **返回**:
    ```json
    {
        "success": true,
        "tags": [
            {
                "name": "Dashboard",
                "count": 3,
                "last_used": "2025-11-18 23:30:00"
            }
        ],
        "total_unique_tags": 5
    }
    ```
    """
    try:
        data = load_conversations()
        sessions = data.get("sessions", [])
        
        # 收集所有标签
        tag_stats: Dict[str, Dict[str, Any]] = {}
        
        for session in sessions:
            tags = session.get("tags", [])
            for tag in tags:
                if tag not in tag_stats:
                    tag_stats[tag] = {
                        "name": tag,
                        "count": 0,
                        "last_used": session.get("updated_at", "")
                    }
                tag_stats[tag]["count"] += 1
                tag_stats[tag]["last_used"] = session.get("updated_at", "")
        
        tags_list = list(tag_stats.values())
        tags_list.sort(key=lambda x: x["count"], reverse=True)
        
        return {
            "success": True,
            "tags": tags_list,
            "total_unique_tags": len(tags_list),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取标签失败: {str(e)}")


# ============================================================================
# 9. 获取会话统计 (GET /api/conversations/stats)
# ============================================================================

@router.get("/stats/overview")
async def get_conversation_stats() -> Dict[str, Any]:
    """
    获取会话统计信息
    
    **用途**: 获取系统中的会话统计数据
    
    **返回**:
    ```json
    {
        "success": true,
        "stats": {
            "total_sessions": 5,
            "active_sessions": 2,
            "completed_sessions": 3,
            "total_messages": 50,
            "total_tokens": 100000,
            "average_tokens_per_session": 20000,
            "average_messages_per_session": 10
        }
    }
    ```
    """
    try:
        data = load_conversations()
        sessions = data.get("sessions", [])
        
        total_sessions = len(sessions)
        active_count = sum(1 for s in sessions if s.get("status") == "active")
        completed_count = sum(1 for s in sessions if s.get("status") == "completed")
        archived_count = sum(1 for s in sessions if s.get("status") == "archived")
        
        total_messages = sum(s.get("messages_count", 0) for s in sessions)
        total_tokens = sum(s.get("total_tokens", 0) for s in sessions)
        
        avg_tokens = total_tokens / total_sessions if total_sessions > 0 else 0
        avg_messages = total_messages / total_sessions if total_sessions > 0 else 0
        
        return {
            "success": True,
            "stats": {
                "total_sessions": total_sessions,
                "active_sessions": active_count,
                "completed_sessions": completed_count,
                "archived_sessions": archived_count,
                "total_messages": total_messages,
                "total_tokens": total_tokens,
                "average_tokens_per_session": round(avg_tokens, 2),
                "average_messages_per_session": round(avg_messages, 2)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计失败: {str(e)}")


# ============================================================================
# 10. 按日期查询会话 (GET /api/conversations/search/by-date)
# ============================================================================

@router.get("/search/by-date")
async def search_by_date(
    start_date: str = Query(..., description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)")
) -> Dict[str, Any]:
    """
    按日期范围查询会话
    
    **用途**: 查询指定时间范围内的会话
    
    **参数**:
    - start_date: 开始日期 (YYYY-MM-DD格式)
    - end_date: 结束日期 (YYYY-MM-DD格式，可选，默认为start_date)
    
    **示例**:
    - GET /api/conversations/search/by-date?start_date=2025-11-18
    - GET /api/conversations/search/by-date?start_date=2025-11-18&end_date=2025-11-19
    
    **返回**:
    ```json
    {
        "success": true,
        "query": {...},
        "sessions": [...],
        "count": 3
    }
    ```
    """
    try:
        if not end_date:
            end_date = start_date
        
        # 解析日期
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        data = load_conversations()
        sessions = data.get("sessions", [])
        
        # 按日期过滤
        filtered = []
        for session in sessions:
            created_at_str = session.get("created_at", "")
            try:
                created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
                if start <= created_at < end:
                    filtered.append(session)
            except ValueError:
                continue
        
        return {
            "success": True,
            "query": {
                "start_date": start_date,
                "end_date": end_date
            },
            "sessions": filtered,
            "count": len(filtered),
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期格式错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


# ============================================================================
# 11. 按Token范围查询会话 (GET /api/conversations/search/by-tokens)
# ============================================================================

@router.get("/search/by-tokens")
async def search_by_tokens(
    min_tokens: int = Query(0, description="最小Token数"),
    max_tokens: int = Query(9999999, description="最大Token数")
) -> Dict[str, Any]:
    """
    按Token消耗范围查询会话
    
    **用途**: 查询消耗Token数在指定范围内的会话
    
    **参数**:
    - min_tokens: 最小Token数 (默认0)
    - max_tokens: 最大Token数 (默认999999)
    
    **示例**:
    - GET /api/conversations/search/by-tokens?min_tokens=5000&max_tokens=50000
    
    **返回**:
    ```json
    {
        "success": true,
        "query": {...},
        "sessions": [...],
        "count": 2
    }
    ```
    """
    try:
        data = load_conversations()
        sessions = data.get("sessions", [])
        
        # 按Token范围过滤
        filtered = [
            s for s in sessions
            if min_tokens <= s.get("total_tokens", 0) <= max_tokens
        ]
        
        # 按Token数排序（降序）
        filtered.sort(key=lambda x: x.get("total_tokens", 0), reverse=True)
        
        return {
            "success": True,
            "query": {
                "min_tokens": min_tokens,
                "max_tokens": max_tokens
            },
            "sessions": filtered,
            "count": len(filtered),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


# ============================================================================
# 健康检查
# ============================================================================

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    检查会话系统健康状态
    
    **用途**: 验证会话系统是否正常运行
    
    **返回**:
    ```json
    {
        "success": true,
        "status": "healthy",
        "data_file": "automation-data/architect-conversations.json"
    }
    ```
    """
    try:
        # 尝试加载数据
        data = load_conversations()
        sessions_count = len(data.get("sessions", []))
        
        return {
            "success": True,
            "status": "healthy",
            "data_file": str(DATA_FILE),
            "sessions_count": sessions_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

