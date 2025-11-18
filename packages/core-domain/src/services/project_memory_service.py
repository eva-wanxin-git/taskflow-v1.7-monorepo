# -*- coding: utf-8 -*-
"""
项目记忆空间服务（Project Memory Service）

功能：
1. 项目隔离的记忆存储
2. 自动记录架构决策（ADR）
3. 自动记录问题解决方案
4. 跨会话知识继承
5. 集成 Session Memory 和 Ultra Memory Cloud
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import uuid
import sqlite3
from pathlib import Path
from contextlib import contextmanager


class MemoryType:
    """记忆类型常量"""
    SESSION = "session"              # Session Memory 会话记忆
    ULTRA = "ultra"                  # Ultra Memory Cloud 长期记忆
    DECISION = "decision"            # 架构决策记忆
    SOLUTION = "solution"            # 问题解决方案记忆
    KNOWLEDGE = "knowledge"          # 一般知识记忆


class MemoryCategory:
    """记忆分类常量"""
    ARCHITECTURE = "architecture"    # 架构相关
    PROBLEM = "problem"              # 问题相关
    SOLUTION = "solution"            # 解决方案相关
    DECISION = "decision"            # 决策相关
    KNOWLEDGE = "knowledge"          # 知识相关
    EXPERIENCE = "experience"        # 经验相关


class RelationType:
    """记忆关系类型"""
    RELATED = "related"              # 相关
    CAUSED_BY = "caused-by"          # 由...引起
    SOLVED_BY = "solved-by"          # 由...解决
    EVOLVED_FROM = "evolved-from"    # 由...演化
    DEPENDS_ON = "depends-on"        # 依赖于


class ProjectMemoryService:
    """
    项目记忆空间服务
    
    负责管理项目的记忆空间，集成多个记忆系统：
    - 本地数据库（SQLite）
    - Session Memory MCP（会话记忆）
    - Ultra Memory Cloud MCP（长期记忆）
    """
    
    def __init__(
        self,
        state_manager=None,
        db_path: str = "database/data/tasks.db",
        session_memory_enabled: bool = True,
        ultra_memory_enabled: bool = True
    ):
        """
        初始化项目记忆服务
        
        Args:
            state_manager: 状态管理器（访问数据库）- 弃用，保留兼容性
            db_path: 数据库文件路径
            session_memory_enabled: 是否启用Session Memory
            ultra_memory_enabled: 是否启用Ultra Memory Cloud
        """
        self.state_manager = state_manager  # 保留兼容性
        self.db_path = Path(db_path)
        self.session_memory_enabled = session_memory_enabled
        self.ultra_memory_enabled = ultra_memory_enabled
        
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
    # 核心功能：记忆存储
    # ========================================================================
    
    def create_memory(
        self,
        project_id: str,
        memory_type: str,
        category: str,
        title: str,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        related_tasks: Optional[List[str]] = None,
        related_issues: Optional[List[str]] = None,
        importance: int = 5,
        created_by: str = "system"
    ) -> Dict[str, Any]:
        """
        创建项目记忆
        
        Args:
            project_id: 项目ID
            memory_type: 记忆类型
            category: 记忆分类
            title: 标题
            content: 内容
            context: 上下文信息
            tags: 标签列表
            related_tasks: 关联任务ID列表
            related_issues: 关联问题ID列表
            importance: 重要性(1-10)
            created_by: 创建者
            
        Returns:
            创建的记忆对象
        """
        memory_id = f"MEM-{uuid.uuid4().hex[:8]}"
        
        # 1. 存储到本地数据库
        memory_data = {
            "id": memory_id,
            "project_id": project_id,
            "memory_type": memory_type,
            "external_memory_id": None,
            "category": category,
            "title": title,
            "content": content,
            "context": json.dumps(context) if context else None,
            "tags": json.dumps(tags) if tags else None,
            "related_tasks": json.dumps(related_tasks) if related_tasks else None,
            "related_issues": json.dumps(related_issues) if related_issues else None,
            "importance": importance,
            "created_by": created_by,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 2. 根据记忆类型，同步到外部记忆系统
        external_memory_id = None
        
        if memory_type == MemoryType.ULTRA and self.ultra_memory_enabled:
            # 存储到 Ultra Memory Cloud（长期记忆）
            external_memory_id = self._store_to_ultra_memory(
                project_id=project_id,
                content=content,
                metadata={
                    "title": title,
                    "category": category,
                    "tags": tags,
                    "importance": importance
                }
            )
            memory_data["external_memory_id"] = external_memory_id
        
        elif memory_type == MemoryType.SESSION and self.session_memory_enabled:
            # 存储到 Session Memory（会话记忆）
            external_memory_id = self._store_to_session_memory(
                project_id=project_id,
                title=title,
                content=content,
                context=context
            )
            memory_data["external_memory_id"] = external_memory_id
        
        # 3. 保存到本地数据库
        if self.state_manager:
            self._save_memory_to_db(memory_data)
        
        # 4. 更新统计
        self._update_memory_stats(project_id, memory_type)
        
        return memory_data
    
    def retrieve_memories(
        self,
        project_id: str,
        query: Optional[str] = None,
        category: Optional[str] = None,
        memory_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        检索项目记忆
        
        Args:
            project_id: 项目ID
            query: 查询文本（语义搜索）
            category: 记忆分类过滤
            memory_type: 记忆类型过滤
            tags: 标签过滤
            limit: 返回数量限制
            
        Returns:
            记忆列表
        """
        # 1. 从本地数据库查询
        memories = self._query_memories_from_db(
            project_id=project_id,
            category=category,
            memory_type=memory_type,
            tags=tags,
            limit=limit
        )
        
        # 2. 如果有查询文本，使用Ultra Memory进行语义搜索
        if query and self.ultra_memory_enabled:
            ultra_results = self._query_from_ultra_memory(
                project_id=project_id,
                query=query,
                top_k=limit
            )
            # 合并结果（去重）
            memories = self._merge_memory_results(memories, ultra_results)
        
        # 3. 记录检索历史（用于优化推荐）
        self._record_retrieval(
            project_id=project_id,
            query=query,
            memory_ids=[m["id"] for m in memories]
        )
        
        return memories
    
    # ========================================================================
    # 自动记录功能
    # ========================================================================
    
    def auto_record_architecture_decision(
        self,
        project_id: str,
        title: str,
        context: str,
        decision: str,
        consequences: Optional[str] = None,
        alternatives: Optional[List[str]] = None,
        decided_by: str = "AI Architect"
    ) -> Dict[str, Any]:
        """
        自动记录架构决策（ADR）
        
        Args:
            project_id: 项目ID
            title: 决策标题
            context: 决策背景
            decision: 决策内容
            consequences: 影响和后果
            alternatives: 备选方案列表
            decided_by: 决策者
            
        Returns:
            创建的记忆对象
        """
        # 1. 格式化为ADR格式
        content = self._format_adr(
            title=title,
            context=context,
            decision=decision,
            consequences=consequences,
            alternatives=alternatives
        )
        
        # 2. 存储到数据库的decisions表
        decision_id = self._save_decision_to_db(
            project_id=project_id,
            title=title,
            context=context,
            decision=decision,
            consequences=consequences,
            alternatives=json.dumps(alternatives) if alternatives else None,
            decided_by=decided_by
        )
        
        # 3. 创建记忆（存储到Ultra Memory作为长期知识）
        memory = self.create_memory(
            project_id=project_id,
            memory_type=MemoryType.ULTRA,
            category=MemoryCategory.DECISION,
            title=f"ADR: {title}",
            content=content,
            context={
                "decision_id": decision_id,
                "decided_by": decided_by,
                "alternatives_count": len(alternatives) if alternatives else 0
            },
            tags=["architecture", "decision", "adr"],
            importance=8,  # 架构决策很重要
            created_by=decided_by
        )
        
        return memory
    
    def auto_record_problem_solution(
        self,
        project_id: str,
        problem_title: str,
        problem_description: str,
        solution_title: str,
        solution_description: str,
        solution_steps: Optional[List[str]] = None,
        tools_used: Optional[List[str]] = None,
        severity: str = "medium",
        component_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        自动记录问题解决方案
        
        Args:
            project_id: 项目ID
            problem_title: 问题标题
            problem_description: 问题描述
            solution_title: 解决方案标题
            solution_description: 解决方案描述
            solution_steps: 解决步骤列表
            tools_used: 使用的工具列表
            severity: 问题严重性
            component_id: 组件ID
            
        Returns:
            创建的记忆对象（包含问题和方案）
        """
        # 1. 保存问题到issues表
        issue_id = self._save_issue_to_db(
            project_id=project_id,
            component_id=component_id,
            title=problem_title,
            description=problem_description,
            severity=severity,
            status="resolved"
        )
        
        # 2. 保存解决方案到solutions表
        solution_id = self._save_solution_to_db(
            issue_id=issue_id,
            title=solution_title,
            description=solution_description,
            steps=json.dumps(solution_steps) if solution_steps else None,
            tools_used=json.dumps(tools_used) if tools_used else None
        )
        
        # 3. 创建问题记忆
        problem_memory = self.create_memory(
            project_id=project_id,
            memory_type=MemoryType.ULTRA,
            category=MemoryCategory.PROBLEM,
            title=problem_title,
            content=problem_description,
            context={
                "issue_id": issue_id,
                "severity": severity,
                "component_id": component_id
            },
            tags=["problem", severity, "resolved"],
            importance=self._severity_to_importance(severity),
            created_by="system"
        )
        
        # 4. 创建解决方案记忆
        solution_memory = self.create_memory(
            project_id=project_id,
            memory_type=MemoryType.ULTRA,
            category=MemoryCategory.SOLUTION,
            title=solution_title,
            content=solution_description,
            context={
                "solution_id": solution_id,
                "issue_id": issue_id,
                "steps": solution_steps,
                "tools_used": tools_used
            },
            tags=["solution", "resolved"] + (tools_used or []),
            importance=self._severity_to_importance(severity),
            created_by="system"
        )
        
        # 5. 创建记忆关系：方案解决了问题
        self.create_memory_relation(
            source_memory_id=solution_memory["id"],
            target_memory_id=problem_memory["id"],
            relation_type=RelationType.SOLVED_BY
        )
        
        return {
            "problem_memory": problem_memory,
            "solution_memory": solution_memory,
            "relation_created": True
        }
    
    # ========================================================================
    # 跨会话知识继承
    # ========================================================================
    
    def inherit_knowledge(
        self,
        project_id: str,
        context: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        跨会话知识继承
        
        获取项目的历史记忆，帮助新会话快速获取上下文
        
        Args:
            project_id: 项目ID
            context: 当前上下文（用于相关性过滤）
            limit: 返回记忆数量
            
        Returns:
            知识继承包：{
                "decisions": [...],  # 架构决策
                "solutions": [...],  # 解决方案
                "important_knowledge": [...],  # 重要知识
                "recent_memories": [...]  # 最近记忆
            }
        """
        # 1. 获取架构决策记忆（按重要性排序）
        decisions = self.retrieve_memories(
            project_id=project_id,
            category=MemoryCategory.DECISION,
            limit=5
        )
        
        # 2. 获取解决方案记忆（按重要性排序）
        solutions = self.retrieve_memories(
            project_id=project_id,
            category=MemoryCategory.SOLUTION,
            limit=10
        )
        
        # 3. 获取重要知识（importance >= 7）
        important_knowledge = self._query_important_memories(
            project_id=project_id,
            min_importance=7,
            limit=5
        )
        
        # 4. 获取最近记忆（时间排序）
        recent_memories = self._query_recent_memories(
            project_id=project_id,
            days=7,
            limit=10
        )
        
        # 5. 如果有上下文，使用语义搜索获取相关记忆
        related_memories = []
        if context and self.ultra_memory_enabled:
            related_memories = self.retrieve_memories(
                project_id=project_id,
                query=context,
                limit=10
            )
        
        return {
            "project_id": project_id,
            "decisions": decisions,
            "solutions": solutions,
            "important_knowledge": important_knowledge,
            "recent_memories": recent_memories,
            "related_memories": related_memories,
            "total_inherited": (
                len(decisions) +
                len(solutions) +
                len(important_knowledge) +
                len(recent_memories) +
                len(related_memories)
            ),
            "inherited_at": datetime.now().isoformat()
        }
    
    # ========================================================================
    # 记忆关系管理
    # ========================================================================
    
    def create_memory_relation(
        self,
        source_memory_id: str,
        target_memory_id: str,
        relation_type: str,
        strength: float = 1.0
    ) -> Dict[str, Any]:
        """
        创建记忆关系
        
        Args:
            source_memory_id: 源记忆ID
            target_memory_id: 目标记忆ID
            relation_type: 关系类型
            strength: 关系强度 0.0-1.0
            
        Returns:
            关系对象
        """
        relation_id = f"REL-{uuid.uuid4().hex[:8]}"
        
        relation_data = {
            "id": relation_id,
            "source_memory_id": source_memory_id,
            "target_memory_id": target_memory_id,
            "relation_type": relation_type,
            "strength": strength,
            "created_at": datetime.now().isoformat()
        }
        
        if self.state_manager:
            self._save_relation_to_db(relation_data)
        
        return relation_data
    
    def get_related_memories(
        self,
        memory_id: str,
        relation_types: Optional[List[str]] = None,
        min_strength: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        获取相关记忆
        
        Args:
            memory_id: 记忆ID
            relation_types: 关系类型过滤
            min_strength: 最小关系强度
            
        Returns:
            相关记忆列表
        """
        if not self.state_manager:
            return []
        
        return self._query_related_memories(
            memory_id=memory_id,
            relation_types=relation_types,
            min_strength=min_strength
        )
    
    # ========================================================================
    # 记忆统计
    # ========================================================================
    
    def get_memory_stats(self, project_id: str) -> Dict[str, Any]:
        """
        获取项目记忆统计
        
        Args:
            project_id: 项目ID
            
        Returns:
            统计信息
        """
        if not self.state_manager:
            return {}
        
        return self._query_memory_stats(project_id)
    
    # ========================================================================
    # 内部辅助方法
    # ========================================================================
    
    def _store_to_ultra_memory(
        self,
        project_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> Optional[str]:
        """存储到Ultra Memory Cloud"""
        # TODO: 实际调用Ultra Memory Cloud MCP工具
        # 这里返回模拟的memory_id
        return f"ultra-{uuid.uuid4().hex[:12]}"
    
    def _store_to_session_memory(
        self,
        project_id: str,
        title: str,
        content: str,
        context: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """存储到Session Memory"""
        # TODO: 实际调用Session Memory MCP工具
        # 这里返回模拟的session_id
        return f"session-{uuid.uuid4().hex[:12]}"
    
    def _query_from_ultra_memory(
        self,
        project_id: str,
        query: str,
        top_k: int
    ) -> List[Dict[str, Any]]:
        """从Ultra Memory查询"""
        # TODO: 实际调用Ultra Memory Cloud检索工具
        return []
    
    def _format_adr(
        self,
        title: str,
        context: str,
        decision: str,
        consequences: Optional[str],
        alternatives: Optional[List[str]]
    ) -> str:
        """格式化为ADR格式"""
        lines = [
            f"# ADR: {title}\n",
            f"\n## 背景 (Context)\n\n{context}\n",
            f"\n## 决策 (Decision)\n\n{decision}\n"
        ]
        
        if consequences:
            lines.append(f"\n## 影响 (Consequences)\n\n{consequences}\n")
        
        if alternatives:
            lines.append("\n## 备选方案 (Alternatives)\n\n")
            for i, alt in enumerate(alternatives, 1):
                lines.append(f"{i}. {alt}\n")
        
        lines.append(f"\n## 日期\n\n{datetime.now().strftime('%Y-%m-%d')}\n")
        
        return "".join(lines)
    
    def _severity_to_importance(self, severity: str) -> int:
        """严重性转重要性"""
        mapping = {
            "critical": 10,
            "high": 8,
            "medium": 5,
            "low": 3
        }
        return mapping.get(severity.lower(), 5)
    
    def _save_memory_to_db(self, memory_data: Dict[str, Any]) -> None:
        """保存记忆到数据库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO project_memories (
                    id, project_id, memory_type, external_memory_id,
                    category, title, content, context, tags,
                    related_tasks, related_issues, importance,
                    created_by, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory_data["id"],
                memory_data["project_id"],
                memory_data["memory_type"],
                memory_data.get("external_memory_id"),
                memory_data["category"],
                memory_data["title"],
                memory_data["content"],
                memory_data.get("context"),
                memory_data.get("tags"),
                memory_data.get("related_tasks"),
                memory_data.get("related_issues"),
                memory_data["importance"],
                memory_data["created_by"],
                memory_data["created_at"],
                memory_data["updated_at"]
            ))
    
    def _save_decision_to_db(
        self,
        project_id: str,
        title: str,
        context: str,
        decision: str,
        consequences: Optional[str],
        alternatives: Optional[str],
        decided_by: str
    ) -> str:
        """保存决策到数据库"""
        decision_id = f"DEC-{uuid.uuid4().hex[:8]}"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO decisions (
                    id, project_id, title, context, decision,
                    consequences, alternatives, status, decided_by, decided_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                decision_id,
                project_id,
                title,
                context,
                decision,
                consequences,
                alternatives,
                'accepted',
                decided_by,
                datetime.now().isoformat()
            ))
        return decision_id
    
    def _save_issue_to_db(
        self,
        project_id: str,
        component_id: Optional[str],
        title: str,
        description: str,
        severity: str,
        status: str
    ) -> str:
        """保存问题到数据库"""
        issue_id = f"ISS-{uuid.uuid4().hex[:8]}"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO issues (
                    id, project_id, component_id, title, description,
                    severity, status, discovered_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                issue_id,
                project_id,
                component_id,
                title,
                description,
                severity,
                status,
                datetime.now().isoformat()
            ))
        return issue_id
    
    def _save_solution_to_db(
        self,
        issue_id: str,
        title: str,
        description: str,
        steps: Optional[str],
        tools_used: Optional[str]
    ) -> str:
        """保存解决方案到数据库"""
        solution_id = f"SOL-{uuid.uuid4().hex[:8]}"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO solutions (
                    id, issue_id, title, description, steps, tools_used, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                solution_id,
                issue_id,
                title,
                description,
                steps,
                tools_used,
                datetime.now().isoformat()
            ))
        return solution_id
    
    def _save_relation_to_db(self, relation_data: Dict[str, Any]) -> None:
        """保存关系到数据库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memory_relations (
                    id, source_memory_id, target_memory_id,
                    relation_type, strength, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                relation_data["id"],
                relation_data["source_memory_id"],
                relation_data["target_memory_id"],
                relation_data["relation_type"],
                relation_data["strength"],
                relation_data["created_at"]
            ))
    
    def _query_memories_from_db(
        self,
        project_id: str,
        category: Optional[str],
        memory_type: Optional[str],
        tags: Optional[List[str]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """从数据库查询记忆"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 构建查询条件
            conditions = ["project_id = ?"]
            params = [project_id]
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            if memory_type:
                conditions.append("memory_type = ?")
                params.append(memory_type)
            
            # TODO: 标签过滤需要JSON查询（SQLite 3.38+）
            # 暂时跳过tags过滤
            
            where_clause = " AND ".join(conditions)
            query = f"""
                SELECT * FROM project_memories
                WHERE {where_clause}
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            """
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为字典列表
            memories = []
            for row in rows:
                memory = dict(row)
                # 解析JSON字段
                if memory.get('context'):
                    try:
                        memory['context'] = json.loads(memory['context'])
                    except:
                        pass
                if memory.get('tags'):
                    try:
                        memory['tags'] = json.loads(memory['tags'])
                    except:
                        memory['tags'] = []
                if memory.get('related_tasks'):
                    try:
                        memory['related_tasks'] = json.loads(memory['related_tasks'])
                    except:
                        memory['related_tasks'] = []
                if memory.get('related_issues'):
                    try:
                        memory['related_issues'] = json.loads(memory['related_issues'])
                    except:
                        memory['related_issues'] = []
                memories.append(memory)
            
            return memories
    
    def _query_important_memories(
        self,
        project_id: str,
        min_importance: int,
        limit: int
    ) -> List[Dict[str, Any]]:
        """查询重要记忆"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM project_memories
                WHERE project_id = ? AND importance >= ?
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            """, (project_id, min_importance, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def _query_recent_memories(
        self,
        project_id: str,
        days: int,
        limit: int
    ) -> List[Dict[str, Any]]:
        """查询最近记忆"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM project_memories
                WHERE project_id = ? AND created_at >= ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (project_id, cutoff_date, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def _query_related_memories(
        self,
        memory_id: str,
        relation_types: Optional[List[str]],
        min_strength: float
    ) -> List[Dict[str, Any]]:
        """查询相关记忆"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 构建查询条件
            conditions = ["(mr.source_memory_id = ? OR mr.target_memory_id = ?)"]
            params = [memory_id, memory_id]
            
            if relation_types:
                placeholders = ",".join("?" * len(relation_types))
                conditions.append(f"mr.relation_type IN ({placeholders})")
                params.extend(relation_types)
            
            conditions.append("mr.strength >= ?")
            params.append(min_strength)
            
            where_clause = " AND ".join(conditions)
            
            # 查询关联的记忆
            query = f"""
                SELECT pm.*, mr.relation_type, mr.strength
                FROM memory_relations mr
                JOIN project_memories pm ON (
                    CASE 
                        WHEN mr.source_memory_id = ? THEN pm.id = mr.target_memory_id
                        ELSE pm.id = mr.source_memory_id
                    END
                )
                WHERE {where_clause}
                ORDER BY mr.strength DESC, pm.importance DESC
            """
            params.insert(0, memory_id)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def _query_memory_stats(self, project_id: str) -> Dict[str, Any]:
        """查询记忆统计"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 尝试从统计表获取
            cursor.execute("""
                SELECT * FROM memory_stats WHERE project_id = ?
            """, (project_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            
            # 如果不存在，实时计算
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_memories,
                    SUM(CASE WHEN memory_type = 'session' THEN 1 ELSE 0 END) as session_memories,
                    SUM(CASE WHEN memory_type = 'ultra' THEN 1 ELSE 0 END) as ultra_memories,
                    SUM(CASE WHEN memory_type = 'decision' THEN 1 ELSE 0 END) as decision_memories,
                    SUM(CASE WHEN memory_type = 'solution' THEN 1 ELSE 0 END) as solution_memories
                FROM project_memories
                WHERE project_id = ?
            """, (project_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    def _update_memory_stats(self, project_id: str, memory_type: str) -> None:
        """更新记忆统计"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查统计记录是否存在
            cursor.execute("""
                SELECT project_id FROM memory_stats WHERE project_id = ?
            """, (project_id,))
            exists = cursor.fetchone() is not None
            
            if exists:
                # 更新现有统计
                update_field = f"{memory_type}_memories" if memory_type != "knowledge" else "total_memories"
                cursor.execute(f"""
                    UPDATE memory_stats
                    SET total_memories = total_memories + 1,
                        {update_field} = {update_field} + 1,
                        last_updated = ?
                    WHERE project_id = ?
                """, (datetime.now().isoformat(), project_id))
            else:
                # 创建新统计记录
                cursor.execute("""
                    INSERT INTO memory_stats (
                        project_id, total_memories, session_memories,
                        ultra_memories, decision_memories, solution_memories,
                        last_updated
                    ) VALUES (?, 1, 0, 0, 0, 0, ?)
                """, (project_id, datetime.now().isoformat()))
    
    def _record_retrieval(
        self,
        project_id: str,
        query: Optional[str],
        memory_ids: List[str]
    ) -> None:
        """记录检索历史"""
        if not query or not memory_ids:
            return
        
        retrieval_id = f"RETR-{uuid.uuid4().hex[:8]}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memory_retrievals (
                    id, project_id, query, memory_ids, retrieved_at
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                retrieval_id,
                project_id,
                query,
                json.dumps(memory_ids),
                datetime.now().isoformat()
            ))
    
    def _merge_memory_results(
        self,
        local_results: List[Dict[str, Any]],
        ultra_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """合并本地和Ultra Memory的结果"""
        # 简单去重合并
        seen_ids = set()
        merged = []
        
        for memory in local_results + ultra_results:
            if memory["id"] not in seen_ids:
                seen_ids.add(memory["id"])
                merged.append(memory)
        
        return merged


# ============================================================================
# 工厂函数
# ============================================================================

def create_project_memory_service(
    state_manager=None,
    db_path: str = "database/data/tasks.db",
    session_memory_enabled: bool = True,
    ultra_memory_enabled: bool = True
) -> ProjectMemoryService:
    """创建项目记忆服务实例
    
    Args:
        state_manager: 状态管理器（弃用，保留兼容性）
        db_path: 数据库文件路径
        session_memory_enabled: 是否启用Session Memory
        ultra_memory_enabled: 是否启用Ultra Memory Cloud
        
    Returns:
        ProjectMemoryService实例
    """
    return ProjectMemoryService(
        state_manager=state_manager,
        db_path=db_path,
        session_memory_enabled=session_memory_enabled,
        ultra_memory_enabled=ultra_memory_enabled
    )

