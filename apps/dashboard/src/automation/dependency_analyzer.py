"""
依赖分析引擎

分析任务依赖关系、检测循环依赖、计算关键路径
"""

from typing import Dict, List, Set, Tuple, Optional
from .models import Task, TaskStatus


class DependencyAnalyzer:
    """依赖分析器 - 分析任务依赖关系
    
    职责:
    - 分析任务依赖关系
    - 检测循环依赖
    - 计算关键路径
    - 识别可执行任务
    """
    
    def __init__(self):
        """初始化依赖分析器"""
        pass
    
    def has_cycle(self, tasks: List[Task]) -> bool:
        """检测是否存在循环依赖
        
        Args:
            tasks: 任务列表
            
        Returns:
            是否存在循环依赖
        """
        # 构建任务图
        task_dict = {task.id: task for task in tasks}
        
        # DFS 检测循环
        visited = set()
        rec_stack = set()
        
        def has_cycle_dfs(task_id: str) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            
            task = task_dict.get(task_id)
            if task is None:
                return False
            
            for dep_id in task.depends_on:
                if dep_id not in visited:
                    if has_cycle_dfs(dep_id):
                        return True
                elif dep_id in rec_stack:
                    return True
            
            rec_stack.remove(task_id)
            return False
        
        for task in tasks:
            if task.id not in visited:
                if has_cycle_dfs(task.id):
                    return True
        
        return False
    
    def get_topological_order(self, tasks: List[Task]) -> Optional[List[str]]:
        """获取任务的拓扑排序
        
        Args:
            tasks: 任务列表
            
        Returns:
            拓扑排序后的任务ID列表，如果有循环依赖返回None
        """
        if self.has_cycle(tasks):
            return None
        
        # 构建任务图
        task_dict = {task.id: task for task in tasks}
        
        # 计算入度
        in_degree = {}
        for task in tasks:
            in_degree[task.id] = len(task.depends_on)
        
        # 拓扑排序（Kahn算法）
        queue = [task_id for task_id in in_degree if in_degree[task_id] == 0]
        result = []
        
        while queue:
            task_id = queue.pop(0)
            result.append(task_id)
            
            # 检查依赖此任务的其他任务
            for other in tasks:
                if task_id in other.depends_on:
                    in_degree[other.id] -= 1
                    if in_degree[other.id] == 0:
                        queue.append(other.id)
        
        return result if len(result) == len(tasks) else None
    
    def get_critical_path(self, tasks: List[Task]) -> List[str]:
        """计算关键路径
        
        Args:
            tasks: 任务列表
            
        Returns:
            关键路径上的任务ID列表
        """
        # 构建任务图
        task_dict = {task.id: task for task in tasks}
        
        # 计算每个任务的最长路径
        memo = {}
        
        def longest_path(task_id: str) -> float:
            if task_id in memo:
                return memo[task_id]
            
            task = task_dict.get(task_id)
            if task is None:
                return 0
            
            max_dep_time = 0
            for dep_id in task.depends_on:
                dep_task = task_dict.get(dep_id)
                if dep_task:
                    max_dep_time = max(max_dep_time, longest_path(dep_id) + dep_task.estimated_hours)
            
            memo[task_id] = max(task.estimated_hours, max_dep_time)
            return memo[task_id]
        
        # 找出端点任务
        all_ids = set(task_dict.keys())
        dep_ids = set()
        for task in tasks:
            dep_ids.update(task.depends_on)
        
        end_tasks = all_ids - dep_ids
        
        # 找出最长的关键路径
        max_path_length = 0
        critical_task = None
        
        for task_id in end_tasks:
            path_length = longest_path(task_id)
            if path_length > max_path_length:
                max_path_length = path_length
                critical_task = task_id
        
        # 反向追踪关键路径
        if critical_task is None:
            return []
        
        critical_path = []
        current = critical_task
        
        while current:
            critical_path.insert(0, current)
            task = task_dict.get(current)
            
            # 找出依赖链中时间最长的
            next_task = None
            max_time = 0
            
            for dep_id in task.depends_on if task else []:
                dep_task = task_dict.get(dep_id)
                if dep_task and dep_task.estimated_hours > max_time:
                    max_time = dep_task.estimated_hours
                    next_task = dep_id
            
            current = next_task
        
        return critical_path
    
    def get_executable_tasks(self, tasks: List[Task], completed_tasks: Set[str]) -> List[str]:
        """获取可执行的任务
        
        Args:
            tasks: 所有任务列表
            completed_tasks: 已完成的任务ID集合
            
        Returns:
            可以执行的任务ID列表（所有依赖都已完成）
        """
        executable = []
        task_dict = {task.id: task for task in tasks}
        
        for task in tasks:
            # 检查任务状态 - 包括 PENDING 和其他未执行的状态
            task_status = task.status.value if hasattr(task.status, 'value') else task.status
            if task_status not in [TaskStatus.PENDING.value if hasattr(TaskStatus.PENDING, 'value') else TaskStatus.PENDING]:
                # 检查是否是待分配状态
                status_str = str(task_status).lower()
                if status_str not in ['pending', 'blocked']:
                    continue
            
            # 检查依赖是否都完成
            all_deps_done = True
            for dep_id in task.depends_on:
                if dep_id not in completed_tasks:
                    all_deps_done = False
                    break
            
            if all_deps_done:
                executable.append(task.id)
        
        return executable
    
    def identify_blocking_tasks(self, tasks: List[Task], target_task_id: str) -> List[str]:
        """识别阻塞特定任务的关键任务
        
        Args:
            tasks: 任务列表
            target_task_id: 目标任务ID
            
        Returns:
            阻塞该任务的关键任务列表
        """
        task_dict = {task.id: task for task in tasks}
        blocking = []
        
        def find_blocking(task_id: str):
            task = task_dict.get(task_id)
            if task is None:
                return
            
            for dep_id in task.depends_on:
                dep_task = task_dict.get(dep_id)
                if dep_task:
                    if dep_task.status not in [TaskStatus.COMPLETED]:
                        blocking.append(dep_id)
                    find_blocking(dep_id)
        
        find_blocking(target_task_id)
        return list(set(blocking))  # 去重
    
    def get_parallelizable_groups(self, tasks: List[Task]) -> List[List[str]]:
        """识别可以并行执行的任务组
        
        Args:
            tasks: 任务列表
            
        Returns:
            任务组列表，每组内的任务可以并行执行
        """
        task_dict = {task.id: task for task in tasks}
        
        # 按层级分组
        levels = {}
        
        def get_level(task_id: str) -> int:
            if task_id in levels:
                return levels[task_id]
            
            task = task_dict.get(task_id)
            if task is None:
                return 0
            
            if not task.depends_on:
                level = 0
            else:
                level = 1 + max(get_level(dep_id) for dep_id in task.depends_on)
            
            levels[task_id] = level
            return level
        
        # 计算每个任务的层级
        for task in tasks:
            get_level(task.id)
        
        # 按层级分组
        groups_dict = {}
        for task_id, level in levels.items():
            if level not in groups_dict:
                groups_dict[level] = []
            groups_dict[level].append(task_id)
        
        # 返回按层级排序的组
        return [groups_dict[i] for i in sorted(groups_dict.keys())]
    
    def estimate_total_time(self, tasks: List[Task]) -> float:
        """估计完成所有任务的总时间
        
        Args:
            tasks: 任务列表
            
        Returns:
            总时间（小时）
        """
        if not tasks:
            return 0
        
        # 找出关键路径
        critical_path = self.get_critical_path(tasks)
        
        task_dict = {task.id: task for task in tasks}
        
        # 计算关键路径上的总时间
        total_time = 0
        for task_id in critical_path:
            task = task_dict.get(task_id)
            if task:
                total_time += task.estimated_hours
        
        return total_time
