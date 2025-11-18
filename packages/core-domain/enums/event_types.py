"""
任务所·Flow - 项目事件类型枚举

定义了系统中所有事件类型、优先级和分类。
共28种核心事件类型，分为4大类：任务、功能、问题、协作。

创建时间: 2025-11-18
设计文档: docs/arch/event-types-design.md
"""

from enum import Enum
from typing import Dict


class EventType(str, Enum):
    """事件类型枚举
    
    共28种事件类型，分为4大类：
    - 任务生命周期: 9种
    - 功能生命周期: 5种
    - 问题生命周期: 6种
    - 协作事件: 8种
    """
    
    # ===== 任务生命周期事件 (9种) =====
    TASK_CREATED = "TASK_CREATED"           # 任务创建
    TASK_ASSIGNED = "TASK_ASSIGNED"         # 任务分配
    TASK_STARTED = "TASK_STARTED"           # 任务开始
    TASK_BLOCKED = "TASK_BLOCKED"           # 任务阻塞
    TASK_UNBLOCKED = "TASK_UNBLOCKED"       # 任务解除阻塞
    TASK_SUBMITTED = "TASK_SUBMITTED"       # 任务提交审查
    TASK_REVIEWED = "TASK_REVIEWED"         # 任务审查完成
    TASK_COMPLETED = "TASK_COMPLETED"       # 任务完成
    TASK_CANCELLED = "TASK_CANCELLED"       # 任务取消
    
    # ===== 功能生命周期事件 (5种) =====
    FEATURE_PROPOSED = "FEATURE_PROPOSED"       # 功能提案
    FEATURE_APPROVED = "FEATURE_APPROVED"       # 功能批准
    FEATURE_IN_PROGRESS = "FEATURE_IN_PROGRESS" # 功能开发中
    FEATURE_COMPLETED = "FEATURE_COMPLETED"     # 功能完成
    FEATURE_DEPLOYED = "FEATURE_DEPLOYED"       # 功能部署
    
    # ===== 问题生命周期事件 (6种) =====
    ISSUE_DISCOVERED = "ISSUE_DISCOVERED"   # 问题发现
    ISSUE_ASSIGNED = "ISSUE_ASSIGNED"       # 问题分配
    ISSUE_IN_PROGRESS = "ISSUE_IN_PROGRESS" # 问题处理中
    ISSUE_SOLVED = "ISSUE_SOLVED"           # 问题解决
    ISSUE_VERIFIED = "ISSUE_VERIFIED"       # 问题验证
    ISSUE_CLOSED = "ISSUE_CLOSED"           # 问题关闭
    
    # ===== 协作事件 (8种) =====
    ARCHITECT_HANDOVER = "ARCHITECT_HANDOVER"       # 架构师交接
    ARCHITECT_RESUME = "ARCHITECT_RESUME"           # 新架构师接管
    CODE_REVIEW_REQUESTED = "CODE_REVIEW_REQUESTED" # 代码审查请求
    DECISION_RECORDED = "DECISION_RECORDED"         # 技术决策记录
    KNOWLEDGE_CAPTURED = "KNOWLEDGE_CAPTURED"       # 知识捕获
    DEPENDENCY_ADDED = "DEPENDENCY_ADDED"           # 依赖添加
    MILESTONE_REACHED = "MILESTONE_REACHED"         # 里程碑达成
    RISK_IDENTIFIED = "RISK_IDENTIFIED"             # 风险识别
    
    @classmethod
    def get_category(cls, event_type: str) -> str:
        """获取事件类型的分类
        
        Args:
            event_type: 事件类型
            
        Returns:
            分类名称: "task" | "feature" | "issue" | "collaboration"
        """
        if event_type.startswith("TASK_"):
            return EventCategory.TASK.value
        elif event_type.startswith("FEATURE_"):
            return EventCategory.FEATURE.value
        elif event_type.startswith("ISSUE_"):
            return EventCategory.ISSUE.value
        else:
            return EventCategory.COLLABORATION.value
    
    @classmethod
    def is_lifecycle_event(cls, event_type: str) -> bool:
        """判断是否为生命周期事件（任务/功能/问题）
        
        Args:
            event_type: 事件类型
            
        Returns:
            True: 生命周期事件
            False: 协作事件
        """
        return event_type.startswith(("TASK_", "FEATURE_", "ISSUE_"))


class EventPriority(str, Enum):
    """事件优先级枚举
    
    定义了4个优先级级别及其处理要求：
    - CRITICAL: 项目级关键事件，立即响应
    - HIGH: 重要事件，30分钟内响应
    - MEDIUM: 正常事件，2小时内响应
    - LOW: 一般信息，无响应时间要求
    """
    
    CRITICAL = "critical"   # 紧急
    HIGH = "high"           # 高
    MEDIUM = "medium"       # 中
    LOW = "low"             # 低
    
    @classmethod
    def get_level(cls, priority: str) -> int:
        """获取优先级数值（用于比较）
        
        Args:
            priority: 优先级字符串
            
        Returns:
            优先级数值: 0-3
        """
        level_map = {
            cls.LOW: 0,
            cls.MEDIUM: 1,
            cls.HIGH: 2,
            cls.CRITICAL: 3
        }
        return level_map.get(priority, 1)
    
    @classmethod
    def compare(cls, priority1: str, priority2: str) -> int:
        """比较两个优先级
        
        Args:
            priority1: 优先级1
            priority2: 优先级2
            
        Returns:
            1: priority1 > priority2
            0: priority1 == priority2
            -1: priority1 < priority2
        """
        level1 = cls.get_level(priority1)
        level2 = cls.get_level(priority2)
        
        if level1 > level2:
            return 1
        elif level1 == level2:
            return 0
        else:
            return -1


class EventCategory(str, Enum):
    """事件类别枚举
    
    将28种事件类型归为4大类：
    - TASK: 任务生命周期（9种）
    - FEATURE: 功能生命周期（5种）
    - ISSUE: 问题生命周期（6种）
    - COLLABORATION: 协作事件（8种）
    """
    
    TASK = "task"                   # 任务
    FEATURE = "feature"             # 功能
    ISSUE = "issue"                 # 问题
    COLLABORATION = "collaboration" # 协作


class ActorType(str, Enum):
    """触发者类型枚举
    
    定义事件的触发者类型：
    - HUMAN: 人类用户
    - AI: AI代理（架构师/工程师/审查者）
    - SYSTEM: 系统自动触发
    """
    
    HUMAN = "human"     # 人类
    AI = "ai"           # AI
    SYSTEM = "system"   # 系统


# ===== 事件类型默认优先级映射 =====

DEFAULT_EVENT_PRIORITIES: Dict[str, str] = {
    # 任务生命周期
    EventType.TASK_CREATED: EventPriority.MEDIUM,
    EventType.TASK_ASSIGNED: EventPriority.MEDIUM,
    EventType.TASK_STARTED: EventPriority.MEDIUM,
    EventType.TASK_BLOCKED: EventPriority.HIGH,      # 阻塞需要关注
    EventType.TASK_UNBLOCKED: EventPriority.MEDIUM,
    EventType.TASK_SUBMITTED: EventPriority.MEDIUM,
    EventType.TASK_REVIEWED: EventPriority.MEDIUM,
    EventType.TASK_COMPLETED: EventPriority.MEDIUM,
    EventType.TASK_CANCELLED: EventPriority.LOW,
    
    # 功能生命周期
    EventType.FEATURE_PROPOSED: EventPriority.LOW,
    EventType.FEATURE_APPROVED: EventPriority.MEDIUM,
    EventType.FEATURE_IN_PROGRESS: EventPriority.MEDIUM,
    EventType.FEATURE_COMPLETED: EventPriority.HIGH,     # 功能完成重要
    EventType.FEATURE_DEPLOYED: EventPriority.CRITICAL,  # 部署最重要
    
    # 问题生命周期（默认，会根据问题严重程度动态调整）
    EventType.ISSUE_DISCOVERED: EventPriority.MEDIUM,
    EventType.ISSUE_ASSIGNED: EventPriority.MEDIUM,
    EventType.ISSUE_IN_PROGRESS: EventPriority.MEDIUM,
    EventType.ISSUE_SOLVED: EventPriority.MEDIUM,
    EventType.ISSUE_VERIFIED: EventPriority.MEDIUM,
    EventType.ISSUE_CLOSED: EventPriority.LOW,
    
    # 协作事件
    EventType.ARCHITECT_HANDOVER: EventPriority.HIGH,       # 交接重要
    EventType.ARCHITECT_RESUME: EventPriority.MEDIUM,
    EventType.CODE_REVIEW_REQUESTED: EventPriority.MEDIUM,
    EventType.DECISION_RECORDED: EventPriority.HIGH,        # 决策重要
    EventType.KNOWLEDGE_CAPTURED: EventPriority.LOW,
    EventType.DEPENDENCY_ADDED: EventPriority.MEDIUM,
    EventType.MILESTONE_REACHED: EventPriority.CRITICAL,    # 里程碑关键
    EventType.RISK_IDENTIFIED: EventPriority.CRITICAL       # 风险关键
}


# ===== 辅助函数 =====

def get_default_priority(event_type: EventType) -> EventPriority:
    """获取事件类型的默认优先级
    
    Args:
        event_type: 事件类型
        
    Returns:
        默认优先级
    """
    return DEFAULT_EVENT_PRIORITIES.get(
        event_type,
        EventPriority.MEDIUM  # 默认为中等优先级
    )


def get_event_display_name(event_type: EventType) -> str:
    """获取事件类型的显示名称（中文）
    
    Args:
        event_type: 事件类型
        
    Returns:
        中文显示名称
    """
    display_names = {
        # 任务生命周期
        EventType.TASK_CREATED: "任务创建",
        EventType.TASK_ASSIGNED: "任务分配",
        EventType.TASK_STARTED: "任务开始",
        EventType.TASK_BLOCKED: "任务阻塞",
        EventType.TASK_UNBLOCKED: "任务解除阻塞",
        EventType.TASK_SUBMITTED: "任务提交审查",
        EventType.TASK_REVIEWED: "任务审查完成",
        EventType.TASK_COMPLETED: "任务完成",
        EventType.TASK_CANCELLED: "任务取消",
        
        # 功能生命周期
        EventType.FEATURE_PROPOSED: "功能提案",
        EventType.FEATURE_APPROVED: "功能批准",
        EventType.FEATURE_IN_PROGRESS: "功能开发中",
        EventType.FEATURE_COMPLETED: "功能完成",
        EventType.FEATURE_DEPLOYED: "功能部署",
        
        # 问题生命周期
        EventType.ISSUE_DISCOVERED: "问题发现",
        EventType.ISSUE_ASSIGNED: "问题分配",
        EventType.ISSUE_IN_PROGRESS: "问题处理中",
        EventType.ISSUE_SOLVED: "问题解决",
        EventType.ISSUE_VERIFIED: "问题验证",
        EventType.ISSUE_CLOSED: "问题关闭",
        
        # 协作事件
        EventType.ARCHITECT_HANDOVER: "架构师交接",
        EventType.ARCHITECT_RESUME: "新架构师接管",
        EventType.CODE_REVIEW_REQUESTED: "代码审查请求",
        EventType.DECISION_RECORDED: "技术决策记录",
        EventType.KNOWLEDGE_CAPTURED: "知识捕获",
        EventType.DEPENDENCY_ADDED: "依赖添加",
        EventType.MILESTONE_REACHED: "里程碑达成",
        EventType.RISK_IDENTIFIED: "风险识别"
    }
    return display_names.get(event_type, event_type.value)


def get_priority_display_name(priority: EventPriority) -> str:
    """获取优先级的显示名称（中文）
    
    Args:
        priority: 优先级
        
    Returns:
        中文显示名称
    """
    display_names = {
        EventPriority.CRITICAL: "🔴 紧急",
        EventPriority.HIGH: "🟠 高",
        EventPriority.MEDIUM: "🟡 中",
        EventPriority.LOW: "🟢 低"
    }
    return display_names.get(priority, priority.value)


def get_category_display_name(category: EventCategory) -> str:
    """获取类别的显示名称（中文）
    
    Args:
        category: 类别
        
    Returns:
        中文显示名称
    """
    display_names = {
        EventCategory.TASK: "📋 任务",
        EventCategory.FEATURE: "✨ 功能",
        EventCategory.ISSUE: "🐛 问题",
        EventCategory.COLLABORATION: "🤝 协作"
    }
    return display_names.get(category, category.value)


# ===== 事件类型分组 =====

TASK_LIFECYCLE_EVENTS = [
    EventType.TASK_CREATED,
    EventType.TASK_ASSIGNED,
    EventType.TASK_STARTED,
    EventType.TASK_BLOCKED,
    EventType.TASK_UNBLOCKED,
    EventType.TASK_SUBMITTED,
    EventType.TASK_REVIEWED,
    EventType.TASK_COMPLETED,
    EventType.TASK_CANCELLED
]

FEATURE_LIFECYCLE_EVENTS = [
    EventType.FEATURE_PROPOSED,
    EventType.FEATURE_APPROVED,
    EventType.FEATURE_IN_PROGRESS,
    EventType.FEATURE_COMPLETED,
    EventType.FEATURE_DEPLOYED
]

ISSUE_LIFECYCLE_EVENTS = [
    EventType.ISSUE_DISCOVERED,
    EventType.ISSUE_ASSIGNED,
    EventType.ISSUE_IN_PROGRESS,
    EventType.ISSUE_SOLVED,
    EventType.ISSUE_VERIFIED,
    EventType.ISSUE_CLOSED
]

COLLABORATION_EVENTS = [
    EventType.ARCHITECT_HANDOVER,
    EventType.ARCHITECT_RESUME,
    EventType.CODE_REVIEW_REQUESTED,
    EventType.DECISION_RECORDED,
    EventType.KNOWLEDGE_CAPTURED,
    EventType.DEPENDENCY_ADDED,
    EventType.MILESTONE_REACHED,
    EventType.RISK_IDENTIFIED
]

# 关键事件（需要立即通知）
CRITICAL_EVENTS = [
    EventType.FEATURE_DEPLOYED,
    EventType.MILESTONE_REACHED,
    EventType.RISK_IDENTIFIED
]

# 阻塞相关事件（需要特别关注）
BLOCKING_EVENTS = [
    EventType.TASK_BLOCKED,
    EventType.TASK_UNBLOCKED
]


if __name__ == "__main__":
    # 测试代码
    import sys
    
    # 设置UTF-8编码
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("===== TaskFlow Event Type System =====\n")
    
    print("Event Type Statistics:")
    print(f"  - Task Lifecycle: {len(TASK_LIFECYCLE_EVENTS)} types")
    print(f"  - Feature Lifecycle: {len(FEATURE_LIFECYCLE_EVENTS)} types")
    print(f"  - Issue Lifecycle: {len(ISSUE_LIFECYCLE_EVENTS)} types")
    print(f"  - Collaboration: {len(COLLABORATION_EVENTS)} types")
    print(f"  - Total: {len(list(EventType))} types\n")
    
    print("Critical Events:")
    for event in CRITICAL_EVENTS:
        priority = get_default_priority(event)
        print(f"  - {event.value} (priority: {priority.value})")
    
    print("\nTask Lifecycle Events:")
    for event in TASK_LIFECYCLE_EVENTS[:5]:  # 只显示前5个
        priority = get_default_priority(event)
        print(f"  - {event.value} (priority: {priority.value})")
    print(f"  ... and {len(TASK_LIFECYCLE_EVENTS) - 5} more")
    
    print("\nEnum Test Passed!")

