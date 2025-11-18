"""
数据模型定义

定义任务、审查等数据模型，使用 Pydantic 进行数据验证
"""

from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    """任务状态枚举
    
    pending: 📝 待分配 - 任务已创建，等待分配给 Worker
    in_progress: ⚙️ 开发中 - Worker 正在执行任务
    review: 🔍 审查中 - 任务已完成，等待审查者审查
    completed: ✅ 已完成 - 审查通过，任务完成
    revision: 🔧 需修订 - 审查未通过，需要修订
    blocked: ⏸️ 阻塞 - 依赖未完成，任务无法执行
    failed: ❌ 失败 - 任务执行失败
    cancelled: 🚫 已取消 - 任务已被取消
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    REVISION = "revision"
    BLOCKED = "blocked"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """任务优先级
    
    P0: 核心功能，必须完成
    P1: 重要功能，高优先级
    P2: 次要功能，可以延迟
    """
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


class Task(BaseModel):
    """任务数据模型
    
    表示一个可执行的任务，包含任务的基本信息、状态、依赖等
    """
    
    id: str = Field(..., description="任务 ID，格式为 task-{major}.{minor}")
    title: str = Field(..., description="任务标题")
    description: str = Field(default="", description="任务描述")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任务状态")
    priority: TaskPriority = Field(default=TaskPriority.P1, description="优先级")
    
    # 任务关系
    depends_on: List[str] = Field(default_factory=list, description="依赖的任务 ID 列表")
    blocked_by: List[str] = Field(default_factory=list, description="阻塞此任务的任务 ID 列表")
    
    # 执行信息
    assigned_to: Optional[str] = Field(default=None, description="分配给的 Worker ID")
    assigned_at: Optional[datetime] = Field(default=None, description="分配时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    
    # 时间戳
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="最后更新时间")
    
    # 元数据
    estimated_hours: float = Field(default=1.0, description="预估工时（小时）")
    actual_hours: Optional[float] = Field(default=None, description="实际工时（小时）")
    complexity: str = Field(default="medium", description="复杂度：low/medium/high")
    
    # 审查信息
    revision_count: int = Field(default=0, description="修订次数")
    max_revision_attempts: int = Field(default=3, description="最大修订次数")
    
    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "id": "task-1.0",
                "title": "项目初始化",
                "description": "创建项目目录结构",
                "status": "pending",
                "priority": "P0",
                "depends_on": [],
                "estimated_hours": 1.5,
                "complexity": "low"
            }
        }
    )


class ReviewScore(BaseModel):
    """审查评分
    
    对代码或任务进行多维度评分
    """
    
    functionality: int = Field(..., ge=0, le=30, description="功能完整性（0-30分）")
    code_quality: int = Field(..., ge=0, le=25, description="代码质量（0-25分）")
    standards: int = Field(..., ge=0, le=20, description="标准遵守（0-20分）")
    documentation: int = Field(..., ge=0, le=15, description="文档完整（0-15分）")
    testing: int = Field(..., ge=0, le=10, description="测试覆盖（0-10分）")
    
    @property
    def total(self) -> int:
        """计算总分"""
        return (self.functionality + self.code_quality + self.standards + 
                self.documentation + self.testing)
    
    @property
    def passed(self) -> bool:
        """判断是否通过（≥80分）"""
        return self.total >= 80


class Review(BaseModel):
    """审查记录
    
    记录对任务的审查结果
    """
    
    id: str = Field(..., description="审查 ID，格式为 review-task-{major}.{minor}-{日期}")
    task_id: str = Field(..., description="被审查的任务 ID")
    reviewer_id: str = Field(default="reviewer-ai", description="审查者 ID")
    
    score: ReviewScore = Field(..., description="评分详情")
    feedback: str = Field(default="", description="审查意见和建议")
    decision: str = Field(..., description="审查决定：approved/revision_required/rejected")
    
    created_at: datetime = Field(default_factory=datetime.now, description="审查时间")
    
    model_config = ConfigDict(use_enum_values=True)


class ExecutionPlan(BaseModel):
    """执行计划
    
    Worker 在执行任务前生成的计划
    """
    
    task_id: str = Field(..., description="任务 ID")
    worker_id: str = Field(..., description="Worker ID")
    
    steps: List[str] = Field(..., description="执行步骤列表")
    deliverables: List[str] = Field(..., description="交付物列表")
    testing_strategy: str = Field(..., description="测试策略描述")
    
    estimated_time: float = Field(..., description="预估执行时间（分钟）")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "task_id": "task-1.0",
                "worker_id": "cursor-1",
                "steps": ["创建目录结构", "编写配置文件", "测试配置加载"],
                "deliverables": ["所有目录已创建", "配置文件已写入"],
                "testing_strategy": "手动测试配置加载",
                "estimated_time": 45
            }
        }
    )


class WorkerStatus(str, Enum):
    """Worker 状态
    
    idle: 空闲
    busy: 忙碌
    offline: 离线
    """
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"


class Worker(BaseModel):
    """Worker 信息
    
    表示一个执行任务的 Worker
    """
    
    id: str = Field(..., description="Worker ID")
    status: WorkerStatus = Field(default=WorkerStatus.IDLE, description="Worker 状态")
    
    current_task: Optional[str] = Field(default=None, description="当前执行的任务 ID")
    tasks_completed: int = Field(default=0, description="已完成的任务数")
    tasks_failed: int = Field(default=0, description="失败的任务数")
    
    last_heartbeat: datetime = Field(default_factory=datetime.now, description="最后心跳时间")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    
    model_config = ConfigDict(use_enum_values=True)


class SystemStatus(BaseModel):
    """系统整体状态
    
    记录自动化系统的整体运行状态
    """
    
    total_tasks: int = Field(..., description="总任务数")
    pending_tasks: int = Field(..., description="待分配任务数")
    in_progress_tasks: int = Field(..., description="执行中任务数")
    review_tasks: int = Field(..., description="审查中任务数")
    completed_tasks: int = Field(..., description="已完成任务数")
    failed_tasks: int = Field(..., description="失败任务数")
    
    active_workers: int = Field(..., description="活跃 Worker 数")
    last_update: datetime = Field(default_factory=datetime.now, description="最后更新时间")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_tasks": 10,
                "pending_tasks": 3,
                "in_progress_tasks": 2,
                "review_tasks": 1,
                "completed_tasks": 4,
                "failed_tasks": 0,
                "active_workers": 3
            }
        }
    )
