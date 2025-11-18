"""
状态管理模块

负责任务状态的持久化存储、查询、更新
使用 SQLite 作为后端数据库
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from .models import Task, TaskStatus, TaskPriority, Review, Worker, SystemStatus


class StateManager:
    """状态管理器
    
    负责与 SQLite 数据库交互，管理任务、审查等数据的持久化
    """
    
    def __init__(self, db_path: str = "automation-data/state.db"):
        """初始化状态管理器
        
        Args:
            db_path: SQLite 数据库文件路径
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_db()
    
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
    
    def _init_db(self) -> None:
        """初始化数据库表
        
        创建任务、审查、Worker 等数据表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建任务表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    priority TEXT,
                    depends_on TEXT,
                    blocked_by TEXT,
                    assigned_to TEXT,
                    assigned_at TEXT,
                    completed_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    estimated_hours REAL,
                    actual_hours REAL,
                    complexity TEXT,
                    revision_count INTEGER DEFAULT 0,
                    max_revision_attempts INTEGER DEFAULT 3
                )
            """)
            
            # 创建审查表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    reviewer_id TEXT,
                    functionality_score INTEGER,
                    code_quality_score INTEGER,
                    standards_score INTEGER,
                    documentation_score INTEGER,
                    testing_score INTEGER,
                    feedback TEXT,
                    decision TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks(id)
                )
            """)
            
            # 创建 Worker 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workers (
                    id TEXT PRIMARY KEY,
                    status TEXT,
                    current_task TEXT,
                    tasks_completed INTEGER DEFAULT 0,
                    tasks_failed INTEGER DEFAULT 0,
                    last_heartbeat TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            
            # 创建索引以加速查询
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_assigned ON tasks(assigned_to)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_task ON reviews(task_id)")
    
    def _task_dict_to_model(self, row: sqlite3.Row) -> Task:
        """将数据库行转换为 Task 模型
        
        Args:
            row: SQLite 行对象
            
        Returns:
            Task 模型实例
        """
        # 兼容v1.7 schema（使用dict.get处理缺失字段）
        row_dict = dict(row)
        
        depends_on_str = row_dict.get('depends_on')
        depends_on = json.loads(depends_on_str) if depends_on_str else []
        
        blocked_by_str = row_dict.get('blocked_by')
        blocked_by = json.loads(blocked_by_str) if blocked_by_str else []
        
        return Task(
            id=row_dict['id'],
            title=row_dict['title'],
            description=row_dict.get('description') or "",
            status=row_dict['status'],
            priority=row_dict.get('priority') or TaskPriority.P1,
            depends_on=depends_on,
            blocked_by=blocked_by,
            assigned_to=row_dict.get('assigned_to'),
            assigned_at=datetime.fromisoformat(row_dict['assigned_at']) if row_dict.get('assigned_at') else None,
            completed_at=datetime.fromisoformat(row_dict['completed_at']) if row_dict.get('completed_at') else None,
            created_at=datetime.fromisoformat(row_dict['created_at']),
            updated_at=datetime.fromisoformat(row_dict['updated_at']),
            estimated_hours=row_dict.get('estimated_hours') or 1.0,
            actual_hours=row_dict.get('actual_hours'),
            complexity=row_dict.get('complexity') or "medium",
            revision_count=row_dict.get('revision_count') or 0,
            max_revision_attempts=row_dict.get('max_revision_attempts') or 3,
        )
    
    # ========== 任务管理 ==========
    
    def create_task(self, task: Task) -> bool:
        """创建新任务
        
        Args:
            task: 任务对象
            
        Returns:
            是否创建成功
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO tasks (
                        id, title, description, status, priority,
                        depends_on, blocked_by, assigned_to,
                        created_at, updated_at, estimated_hours,
                        complexity, revision_count, max_revision_attempts
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    task.id,
                    task.title,
                    task.description,
                    task.status.value if isinstance(task.status, TaskStatus) else task.status,
                    task.priority.value if isinstance(task.priority, TaskPriority) else task.priority,
                    json.dumps(task.depends_on),
                    json.dumps(task.blocked_by),
                    task.assigned_to,
                    task.created_at.isoformat(),
                    task.updated_at.isoformat(),
                    task.estimated_hours,
                    task.complexity,
                    task.revision_count,
                    task.max_revision_attempts,
                ))
                return True
            except sqlite3.IntegrityError:
                return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务
        
        Args:
            task_id: 任务 ID
            
        Returns:
            任务对象，如果不存在则返回 None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            
            if row:
                return self._task_dict_to_model(row)
            return None
    
    def update_task_status(self, task_id: str, new_status: TaskStatus) -> bool:
        """更新任务状态
        
        Args:
            task_id: 任务 ID
            new_status: 新的状态
            
        Returns:
            是否更新成功
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE tasks
                SET status = ?, updated_at = ?
                WHERE id = ?
            """, (
                new_status.value if isinstance(new_status, TaskStatus) else new_status,
                datetime.now().isoformat(),
                task_id,
            ))
            
            return cursor.rowcount > 0
    
    def list_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """按状态列出任务
        
        Args:
            status: 任务状态
            
        Returns:
            任务列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY created_at",
                (status.value if isinstance(status, TaskStatus) else status,)
            )
            rows = cursor.fetchall()
            
            return [self._task_dict_to_model(row) for row in rows]
    
    def list_all_tasks(self) -> List[Task]:
        """列出所有任务
        
        Returns:
            所有任务列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at")
            rows = cursor.fetchall()
            
            return [self._task_dict_to_model(row) for row in rows]
    
    def list_tasks_assigned_to(self, worker_id: str) -> List[Task]:
        """列出分配给特定 Worker 的任务
        
        Args:
            worker_id: Worker ID
            
        Returns:
            任务列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tasks WHERE assigned_to = ? ORDER BY created_at",
                (worker_id,)
            )
            rows = cursor.fetchall()
            
            return [self._task_dict_to_model(row) for row in rows]
    
    # ========== 审查管理 ==========
    
    def create_review(self, review: Review) -> bool:
        """创建审查记录
        
        Args:
            review: 审查对象
            
        Returns:
            是否创建成功
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO reviews (
                        id, task_id, reviewer_id,
                        functionality_score, code_quality_score, standards_score,
                        documentation_score, testing_score,
                        feedback, decision, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review.id,
                    review.task_id,
                    review.reviewer_id,
                    review.score.functionality,
                    review.score.code_quality,
                    review.score.standards,
                    review.score.documentation,
                    review.score.testing,
                    review.feedback,
                    review.decision,
                    review.created_at.isoformat(),
                ))
                return True
            except sqlite3.IntegrityError:
                return False
    
    def get_review(self, review_id: str) -> Optional[Review]:
        """获取审查记录
        
        Args:
            review_id: 审查 ID
            
        Returns:
            审查对象，如果不存在则返回 None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            from .models import ReviewScore
            score = ReviewScore(
                functionality=row['functionality_score'],
                code_quality=row['code_quality_score'],
                standards=row['standards_score'],
                documentation=row['documentation_score'],
                testing=row['testing_score'],
            )
            
            return Review(
                id=row['id'],
                task_id=row['task_id'],
                reviewer_id=row['reviewer_id'],
                score=score,
                feedback=row['feedback'] or "",
                decision=row['decision'],
                created_at=datetime.fromisoformat(row['created_at']),
            )
    
    # ========== Worker 管理 ==========
    
    def register_worker(self, worker_id: str) -> bool:
        """注册 Worker
        
        Args:
            worker_id: Worker ID
            
        Returns:
            是否注册成功
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO workers (id, status, created_at, last_heartbeat)
                    VALUES (?, ?, ?, ?)
                """, (
                    worker_id,
                    "idle",
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                ))
                return True
            except sqlite3.IntegrityError:
                return False
    
    def get_system_status(self) -> SystemStatus:
        """获取系统整体状态
        
        Returns:
            系统状态对象
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 统计各状态的任务数
            cursor.execute("SELECT COUNT(*) FROM tasks")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = ?", (TaskStatus.PENDING.value,))
            pending = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = ?", (TaskStatus.IN_PROGRESS.value,))
            in_progress = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = ?", (TaskStatus.REVIEW.value,))
            review = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = ?", (TaskStatus.COMPLETED.value,))
            completed = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = ?", (TaskStatus.FAILED.value,))
            failed = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM workers WHERE status = ?", ("idle",))
            # Count active workers (last heartbeat within 5 minutes)
            active_workers = cursor.fetchone()[0]
            
            return SystemStatus(
                total_tasks=total,
                pending_tasks=pending,
                in_progress_tasks=in_progress,
                review_tasks=review,
                completed_tasks=completed,
                failed_tasks=failed,
                active_workers=active_workers,
            )
