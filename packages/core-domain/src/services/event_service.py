# -*- coding: utf-8 -*-
"""
事件发射和存储服务（Event Emitter & Store）

功能：
1. EventEmitter: 发射事件
2. EventStore: 存储和查询事件
3. 事件类型管理
4. 事件统计
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import uuid
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from enum import Enum


class EventSeverity(str, Enum):
    """事件严重性枚举"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class EventCategory(str, Enum):
    """事件分类枚举"""
    TASK = "task"
    ISSUE = "issue"
    DECISION = "decision"
    DEPLOYMENT = "deployment"
    SYSTEM = "system"
    GENERAL = "general"


class EventStatus(str, Enum):
    """事件状态枚举"""
    PENDING = "pending"
    PROCESSED = "processed"
    ARCHIVED = "archived"


class EventSource(str, Enum):
    """事件来源枚举"""
    SYSTEM = "system"
    USER = "user"
    AI = "ai"
    EXTERNAL = "external"


# ============================================================================
# EventEmitter - 事件发射器
# ============================================================================

class EventEmitter:
    """
    事件发射器
    
    负责创建和发射事件到EventStore
    """
    
    def __init__(self, event_store: 'EventStore'):
        """
        初始化事件发射器
        
        Args:
            event_store: 事件存储实例
        """
        self.event_store = event_store
    
    def emit(
        self,
        project_id: str,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        category: str = EventCategory.GENERAL,
        source: str = EventSource.SYSTEM,
        actor: Optional[str] = None,
        severity: str = EventSeverity.INFO,
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        occurred_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        发射单个事件
        
        Args:
            project_id: 项目ID
            event_type: 事件类型 (如: "task.created", "issue.resolved")
            title: 事件标题
            description: 事件描述
            data: 事件数据（任意JSON对象）
            category: 事件分类
            source: 事件来源
            actor: 操作者
            severity: 严重性
            related_entity_type: 关联实体类型
            related_entity_id: 关联实体ID
            tags: 标签列表
            occurred_at: 事件发生时间（ISO格式），默认为当前时间
            
        Returns:
            创建的事件对象
        """
        event_id = f"EVT-{uuid.uuid4().hex[:8]}"
        
        event = {
            "id": event_id,
            "project_id": project_id,
            "event_type": event_type,
            "event_category": category,
            "source": source,
            "actor": actor,
            "title": title,
            "description": description,
            "data": json.dumps(data) if data else None,
            "related_entity_type": related_entity_type,
            "related_entity_id": related_entity_id,
            "severity": severity,
            "status": EventStatus.PROCESSED,
            "tags": json.dumps(tags) if tags else None,
            "occurred_at": occurred_at or datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        
        # 保存事件
        self.event_store.save(event)
        
        # 更新统计
        self.event_store.update_stats(project_id, category, severity)
        
        return event
    
    def emit_batch(
        self,
        project_id: str,
        events: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        批量发射事件
        
        Args:
            project_id: 项目ID
            events: 事件列表，每个事件包含emit()方法的参数
            
        Returns:
            创建的事件列表
        """
        created_events = []
        
        for event_data in events:
            # 确保project_id
            event_data["project_id"] = project_id
            
            # 发射事件
            event = self.emit(**event_data)
            created_events.append(event)
        
        return created_events
    
    # ========================================================================
    # 便捷方法 - 常用事件类型
    # ========================================================================
    
    def emit_task_created(
        self,
        project_id: str,
        task_id: str,
        task_title: str,
        actor: str = "AI Architect"
    ) -> Dict[str, Any]:
        """发射任务创建事件"""
        return self.emit(
            project_id=project_id,
            event_type="task.created",
            title=f"任务创建: {task_title}",
            description=f"新任务 {task_id} 被创建",
            category=EventCategory.TASK,
            source=EventSource.AI,
            actor=actor,
            severity=EventSeverity.INFO,
            related_entity_type="task",
            related_entity_id=task_id,
            tags=["task", "created"]
        )
    
    def emit_task_completed(
        self,
        project_id: str,
        task_id: str,
        task_title: str,
        actor: str = "fullstack-engineer"
    ) -> Dict[str, Any]:
        """发射任务完成事件"""
        return self.emit(
            project_id=project_id,
            event_type="task.completed",
            title=f"任务完成: {task_title}",
            description=f"任务 {task_id} 已完成",
            category=EventCategory.TASK,
            source=EventSource.AI,
            actor=actor,
            severity=EventSeverity.INFO,
            related_entity_type="task",
            related_entity_id=task_id,
            tags=["task", "completed"]
        )
    
    def emit_issue_discovered(
        self,
        project_id: str,
        issue_id: str,
        issue_title: str,
        severity: str = EventSeverity.WARNING
    ) -> Dict[str, Any]:
        """发射问题发现事件"""
        return self.emit(
            project_id=project_id,
            event_type="issue.discovered",
            title=f"问题发现: {issue_title}",
            description=f"发现新问题 {issue_id}",
            category=EventCategory.ISSUE,
            source=EventSource.AI,
            severity=severity,
            related_entity_type="issue",
            related_entity_id=issue_id,
            tags=["issue", "discovered"]
        )
    
    def emit_decision_made(
        self,
        project_id: str,
        decision_id: str,
        decision_title: str,
        actor: str = "AI Architect"
    ) -> Dict[str, Any]:
        """发射决策制定事件"""
        return self.emit(
            project_id=project_id,
            event_type="decision.made",
            title=f"决策制定: {decision_title}",
            description=f"架构决策 {decision_id} 已制定",
            category=EventCategory.DECISION,
            source=EventSource.AI,
            actor=actor,
            severity=EventSeverity.INFO,
            related_entity_type="decision",
            related_entity_id=decision_id,
            tags=["decision", "made"]
        )


# ============================================================================
# EventStore - 事件存储器
# ============================================================================

class EventStore:
    """
    事件存储器
    
    负责事件的持久化和查询
    """
    
    def __init__(self, db_path: str = "database/data/tasks.db"):
        """
        初始化事件存储器
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = Path(db_path)
        
        # 确保数据库目录存在
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def _get_connection(self):
        """获取数据库连接（上下文管理器）
        
        Yields:
            sqlite3.Connection: 数据库连接
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    # ========================================================================
    # 核心方法
    # ========================================================================
    
    def save(self, event: Dict[str, Any]) -> None:
        """
        保存事件到数据库
        
        Args:
            event: 事件对象
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO project_events (
                    id, project_id, event_type, event_category, source, actor,
                    title, description, data, related_entity_type, related_entity_id,
                    severity, status, tags, occurred_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event["id"],
                event["project_id"],
                event["event_type"],
                event["event_category"],
                event["source"],
                event.get("actor"),
                event["title"],
                event.get("description"),
                event.get("data"),
                event.get("related_entity_type"),
                event.get("related_entity_id"),
                event["severity"],
                event["status"],
                event.get("tags"),
                event["occurred_at"],
                event["created_at"]
            ))
    
    def query(
        self,
        project_id: Optional[str] = None,
        event_type: Optional[str] = None,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        actor: Optional[str] = None,
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "occurred_at",
        order_direction: str = "DESC"
    ) -> List[Dict[str, Any]]:
        """
        查询事件
        
        Args:
            project_id: 项目ID过滤
            event_type: 事件类型过滤
            category: 分类过滤
            severity: 严重性过滤
            actor: 操作者过滤
            related_entity_type: 关联实体类型过滤
            related_entity_id: 关联实体ID过滤
            start_time: 开始时间过滤（ISO格式）
            end_time: 结束时间过滤（ISO格式）
            limit: 返回数量限制
            offset: 偏移量
            order_by: 排序字段
            order_direction: 排序方向（ASC/DESC）
            
        Returns:
            事件列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 构建查询条件
            conditions = []
            params = []
            
            if project_id:
                conditions.append("project_id = ?")
                params.append(project_id)
            
            if event_type:
                conditions.append("event_type = ?")
                params.append(event_type)
            
            if category:
                conditions.append("event_category = ?")
                params.append(category)
            
            if severity:
                conditions.append("severity = ?")
                params.append(severity)
            
            if actor:
                conditions.append("actor = ?")
                params.append(actor)
            
            if related_entity_type:
                conditions.append("related_entity_type = ?")
                params.append(related_entity_type)
            
            if related_entity_id:
                conditions.append("related_entity_id = ?")
                params.append(related_entity_id)
            
            if start_time:
                conditions.append("occurred_at >= ?")
                params.append(start_time)
            
            if end_time:
                conditions.append("occurred_at <= ?")
                params.append(end_time)
            
            # 构建WHERE子句
            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
            
            # 构建完整查询
            query = f"""
                SELECT * FROM project_events
                {where_clause}
                ORDER BY {order_by} {order_direction}
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为字典列表
            events = []
            for row in rows:
                event = dict(row)
                # 解析JSON字段
                if event.get('data'):
                    try:
                        event['data'] = json.loads(event['data'])
                    except:
                        pass
                if event.get('tags'):
                    try:
                        event['tags'] = json.loads(event['tags'])
                    except:
                        event['tags'] = []
                events.append(event)
            
            return events
    
    def get_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        根据ID获取事件
        
        Args:
            event_id: 事件ID
            
        Returns:
            事件对象或None
        """
        events = self.query(limit=1, offset=0)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM project_events WHERE id = ?", (event_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            event = dict(row)
            # 解析JSON字段
            if event.get('data'):
                try:
                    event['data'] = json.loads(event['data'])
                except:
                    pass
            if event.get('tags'):
                try:
                    event['tags'] = json.loads(event['tags'])
                except:
                    event['tags'] = []
            
            return event
    
    # ========================================================================
    # 统计方法
    # ========================================================================
    
    def get_stats(self, project_id: str) -> Dict[str, Any]:
        """
        获取项目事件统计
        
        Args:
            project_id: 项目ID
            
        Returns:
            统计信息
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 尝试从统计表获取
            cursor.execute("""
                SELECT * FROM event_stats WHERE project_id = ?
            """, (project_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            
            # 如果不存在，实时计算
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_events,
                    SUM(CASE WHEN event_category = 'task' THEN 1 ELSE 0 END) as task_events,
                    SUM(CASE WHEN event_category = 'issue' THEN 1 ELSE 0 END) as issue_events,
                    SUM(CASE WHEN event_category = 'decision' THEN 1 ELSE 0 END) as decision_events,
                    SUM(CASE WHEN event_category = 'deployment' THEN 1 ELSE 0 END) as deployment_events,
                    SUM(CASE WHEN event_category = 'system' THEN 1 ELSE 0 END) as system_events,
                    SUM(CASE WHEN severity = 'info' THEN 1 ELSE 0 END) as info_events,
                    SUM(CASE WHEN severity = 'warning' THEN 1 ELSE 0 END) as warning_events,
                    SUM(CASE WHEN severity = 'error' THEN 1 ELSE 0 END) as error_events,
                    SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) as critical_events,
                    MAX(occurred_at) as last_event_at
                FROM project_events
                WHERE project_id = ?
            """, (project_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    def update_stats(
        self,
        project_id: str,
        category: str,
        severity: str
    ) -> None:
        """
        更新事件统计
        
        Args:
            project_id: 项目ID
            category: 事件分类
            severity: 事件严重性
        """
        # 转换枚举为字符串值
        if hasattr(category, 'value'):
            category = category.value
        if hasattr(severity, 'value'):
            severity = severity.value
        
        # 确保是字符串类型
        category = str(category)
        severity = str(severity)
        
        # 有效的分类列（对应数据库列名）
        valid_categories = ["task", "issue", "decision", "deployment", "system"]
        valid_severities = ["info", "warning", "error", "critical"]
        
        # 如果分类或严重性不在有效列表中，使用默认值
        if category not in valid_categories:
            category = "system"  # general类别归到system
        if severity not in valid_severities:
            severity = "info"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查统计记录是否存在
            cursor.execute("""
                SELECT project_id FROM event_stats WHERE project_id = ?
            """, (project_id,))
            exists = cursor.fetchone() is not None
            
            now = datetime.now().isoformat()
            
            if exists:
                # 更新现有统计
                cursor.execute(f"""
                    UPDATE event_stats
                    SET total_events = total_events + 1,
                        {category}_events = {category}_events + 1,
                        {severity}_events = {severity}_events + 1,
                        last_event_at = ?,
                        last_updated = ?
                    WHERE project_id = ?
                """, (now, now, project_id))
            else:
                # 创建新统计记录
                cursor.execute("""
                    INSERT INTO event_stats (
                        project_id, total_events, task_events, issue_events,
                        decision_events, deployment_events, system_events,
                        info_events, warning_events, error_events, critical_events,
                        last_event_at, last_updated
                    ) VALUES (?, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, ?, ?)
                """, (project_id, now, now))
                
                # 更新对应的分类和严重性计数
                cursor.execute(f"""
                    UPDATE event_stats
                    SET {category}_events = 1, {severity}_events = 1
                    WHERE project_id = ?
                """, (project_id,))
    
    # ========================================================================
    # 事件类型管理
    # ========================================================================
    
    def get_event_types(
        self,
        category: Optional[str] = None,
        is_active: bool = True
    ) -> List[Dict[str, Any]]:
        """
        获取事件类型列表
        
        Args:
            category: 分类过滤
            is_active: 是否仅返回启用的类型
            
        Returns:
            事件类型列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            conditions = []
            params = []
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            if is_active:
                conditions.append("is_active = 1")
            
            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
            
            query = f"""
                SELECT * FROM event_types
                {where_clause}
                ORDER BY category, type_code
            """
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]


# ============================================================================
# 工厂函数
# ============================================================================

def create_event_emitter(db_path: str = "database/data/tasks.db") -> EventEmitter:
    """
    创建事件发射器实例
    
    Args:
        db_path: 数据库文件路径
        
    Returns:
        EventEmitter实例
    """
    event_store = EventStore(db_path=db_path)
    return EventEmitter(event_store=event_store)


def create_event_store(db_path: str = "database/data/tasks.db") -> EventStore:
    """
    创建事件存储器实例
    
    Args:
        db_path: 数据库文件路径
        
    Returns:
        EventStore实例
    """
    return EventStore(db_path=db_path)

