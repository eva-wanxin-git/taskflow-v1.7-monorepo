"""
任务完成详情管理

存储和管理任务的完成详情，包括实现的功能清单、代码指标等
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class TaskCompletion:
    """任务完成详情管理器"""
    
    def __init__(self, data_file: str = "automation-data/task_completions.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.completions = json.load(f)
        else:
            self.completions = {}
    
    def _save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.completions, f, ensure_ascii=False, indent=2)
    
    def update_completion(
        self,
        task_id: str,
        features_implemented: List[str],
        code_lines: int = 0,
        files_created: int = 0,
        files_modified: int = 0,
        actual_hours: float = 0.0,
        key_achievements: List[str] = None,
        tech_stack: List[str] = None,
        notes: str = ""
    ):
        """
        更新任务完成详情
        
        Args:
            task_id: 任务ID
            features_implemented: 实现的功能列表
            code_lines: 代码行数
            files_created: 新建文件数
            files_modified: 修改文件数
            actual_hours: 实际工时
            key_achievements: 关键成就
            tech_stack: 使用的技术栈
            notes: 备注
        """
        self.completions[task_id] = {
            "task_id": task_id,
            "completed_at": datetime.now().isoformat(),
            "features_implemented": features_implemented or [],
            "metrics": {
                "code_lines": code_lines,
                "files_created": files_created,
                "files_modified": files_modified,
                "actual_hours": actual_hours
            },
            "key_achievements": key_achievements or [],
            "tech_stack": tech_stack or [],
            "notes": notes
        }
        self._save_data()
        return self.completions[task_id]
    
    def get_completion(self, task_id: str) -> Dict[str, Any]:
        """获取任务完成详情"""
        return self.completions.get(task_id)
    
    def get_all_completions(self) -> Dict[str, Any]:
        """获取所有完成详情"""
        return self.completions


# 示例：如何更新任务完成详情
if __name__ == "__main__":
    tc = TaskCompletion()
    
    # 示例：更新 phase1-task3 的完成详情
    tc.update_completion(
        task_id="phase1-task3",
        features_implemented=[
            "项目CRUD功能（创建、读取、更新、删除）",
            "本地存储系统（localStorage封装）",
            "项目卡片组件（ProjectCard）",
            "编辑弹窗组件（ProjectModal）",
            "侧边栏组件（ProjectSidebar）",
            "图标和颜色选择器",
            "自动初始化示例项目",
            "流畅的动画过渡效果"
        ],
        code_lines=1250,
        files_created=8,
        files_modified=2,
        actual_hours=2.0,
        key_achievements=[
            "完整的TypeScript类型定义",
            "React Hooks最佳实践",
            "组件化设计",
            "用户体验流畅"
        ],
        tech_stack=[
            "React 18",
            "TypeScript",
            "localStorage API",
            "CSS Modules"
        ],
        notes="项目侧边栏功能完整，超预期完成"
    )
    
    print("[OK] Task completion details updated")
    print(f"[File] {tc.data_file}")

