"""
Git 辅助模块

提供 Git 相关的操作函数
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def run_git_command(command: List[str], cwd: str = ".") -> Tuple[int, str, str]:
    """运行 Git 命令
    
    Args:
        command: Git 命令列表 (如 ["git", "status"])
        cwd: 工作目录
        
    Returns:
        (返回码, 标准输出, 标准错误)
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timeout"
    except Exception as e:
        return -1, "", str(e)


def create_git_branch(task_id: str, base_branch: str = "main") -> bool:
    """创建 Git 分支
    
    Args:
        task_id: 任务ID (如 task-1.0)
        base_branch: 基础分支 (默认 main)
        
    Returns:
        是否创建成功
    """
    branch_name = f"feature/{task_id}"
    
    # 检查分支是否已存在
    returncode, _, _ = run_git_command(["git", "show-ref", "--verify", f"refs/heads/{branch_name}"])
    if returncode == 0:
        # 分支已存在，先删除
        run_git_command(["git", "branch", "-D", branch_name])
    
    # 创建新分支
    returncode, _, stderr = run_git_command(
        ["git", "checkout", "-b", branch_name, base_branch]
    )
    
    return returncode == 0


def get_current_branch() -> Optional[str]:
    """获取当前分支名称
    
    Returns:
        分支名称，如果获取失败返回 None
    """
    returncode, stdout, _ = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if returncode == 0:
        return stdout.strip()
    return None


def commit_code(task_id: str, message: str = "") -> bool:
    """提交代码到 Git
    
    Args:
        task_id: 任务ID
        message: 提交消息 (可选，默认生成)
        
    Returns:
        是否提交成功
    """
    if not message:
        message = f"[{task_id}] 完成任务实现"
    
    # 暂存所有改动
    returncode, _, _ = run_git_command(["git", "add", "-A"])
    if returncode != 0:
        return False
    
    # 检查是否有改动
    returncode, status, _ = run_git_command(["git", "status", "--porcelain"])
    if returncode != 0 or not status.strip():
        # 没有改动
        return False
    
    # 提交
    returncode, _, _ = run_git_command(
        ["git", "commit", "-m", message]
    )
    
    return returncode == 0


def get_git_status() -> Dict[str, List[str]]:
    """获取 Git 状态
    
    Returns:
        {
            "modified": [...],
            "added": [...],
            "deleted": [...],
            "untracked": [...]
        }
    """
    returncode, stdout, _ = run_git_command(["git", "status", "--porcelain"])
    
    result = {
        "modified": [],
        "added": [],
        "deleted": [],
        "untracked": []
    }
    
    if returncode != 0:
        return result
    
    for line in stdout.strip().split('\n'):
        if not line:
            continue
        
        status_code = line[:2]
        filename = line[3:]
        
        if status_code == 'M ':
            result["modified"].append(filename)
        elif status_code == 'A ':
            result["added"].append(filename)
        elif status_code == 'D ':
            result["deleted"].append(filename)
        elif status_code == '??':
            result["untracked"].append(filename)
    
    return result


def get_recent_commits(n: int = 5) -> List[Dict[str, str]]:
    """获取最近的提交历史
    
    Args:
        n: 获取的提交数量
        
    Returns:
        提交列表
    """
    format_str = "%H%n%an%n%ae%n%s"
    returncode, stdout, _ = run_git_command(
        ["git", "log", f"-{n}", f"--format={format_str}"]
    )
    
    commits = []
    if returncode == 0:
        lines = stdout.strip().split('\n')
        for i in range(0, len(lines), 4):
            if i + 3 < len(lines):
                commits.append({
                    "hash": lines[i],
                    "author": lines[i+1],
                    "email": lines[i+2],
                    "message": lines[i+3]
                })
    
    return commits


def push_to_remote(branch: str = "") -> bool:
    """推送到远程仓库
    
    Args:
        branch: 分支名称 (默认当前分支)
        
    Returns:
        是否推送成功
    """
    if not branch:
        branch = get_current_branch() or "main"
    
    returncode, _, _ = run_git_command(
        ["git", "push", "origin", branch]
    )
    
    return returncode == 0


def checkout_branch(branch: str) -> bool:
    """切换分支
    
    Args:
        branch: 分支名称
        
    Returns:
        是否切换成功
    """
    returncode, _, _ = run_git_command(["git", "checkout", branch])
    return returncode == 0


def is_git_repo() -> bool:
    """检查当前目录是否是 Git 仓库
    
    Returns:
        是否是 Git 仓库
    """
    returncode, _, _ = run_git_command(["git", "rev-parse", "--git-dir"])
    return returncode == 0
