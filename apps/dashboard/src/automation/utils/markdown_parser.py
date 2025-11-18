"""
Markdown 解析模块

解析任务 Markdown 文件，提取关键信息
"""

import re
from pathlib import Path
from typing import Dict, List, Any


def parse_task_markdown(file_path: str) -> Dict[str, Any]:
    """解析任务 Markdown 文件
    
    Args:
        file_path: 任务文件路径 (如 tasks/task-1.0.md)
        
    Returns:
        解析后的任务信息字典
    """
    try:
        content = Path(file_path).read_text(encoding='utf-8')
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}
    
    result = {
        "file_path": file_path,
        "title": "",
        "objective": "",
        "requirements": [],
        "acceptance_criteria": [],
        "dependencies": [],
        "estimated_hours": 0.0,
        "complexity": "medium",
    }
    
    # 解析标题
    title_match = re.search(r'# Task-[\d.]+: (.+)', content)
    if title_match:
        result["title"] = title_match.group(1).strip()
    
    # 解析任务目标
    if "## 🎯 任务目标" in content or "## 任务目标" in content:
        objective_match = re.search(
            r'## 🎯 任务目标\n\n(.+?)\n##', content, re.DOTALL
        )
        if not objective_match:
            objective_match = re.search(
                r'## 任务目标\n\n(.+?)\n##', content, re.DOTALL
            )
        if objective_match:
            result["objective"] = objective_match.group(1).strip()
    
    # 解析需求部分
    if "## 📋 具体要求" in content:
        requirements_section = re.search(
            r'## 📋 具体要求\n\n(.+?)(?=\n## |\Z)', content, re.DOTALL
        )
        if requirements_section:
            # 提取列表项
            items = re.findall(r'^\s*[-*]\s+(.+)$', requirements_section.group(1), re.MULTILINE)
            result["requirements"] = [item.strip() for item in items]
    
    # 解析验收标准
    if "## ✅ 验收标准" in content:
        criteria_section = re.search(
            r'## ✅ 验收标准\n\n(.+?)(?=\n## |\Z)', content, re.DOTALL
        )
        if criteria_section:
            # 提取复选框项目
            items = re.findall(r'- \[[\sx]\] (.+)$', criteria_section.group(1), re.MULTILINE)
            result["acceptance_criteria"] = [item.strip() for item in items]
    
    # 解析依赖任务
    if "## 🔗 依赖任务" in content:
        deps_section = re.search(
            r'## 🔗 依赖任务\n\n(.+?)(?=\n## |\Z)', content, re.DOTALL
        )
        if deps_section:
            content_text = deps_section.group(1)
            if content_text.lower() != "无":
                # 提取 task-X.X 格式
                deps = re.findall(r'task-[\d.]+', content_text)
                result["dependencies"] = list(set(deps))
    
    # 解析预估工时
    if "## ⏱️ 预估工时" in content:
        hours_match = re.search(
            r'## ⏱️ 预估工时\n\n([\d.]+)', content
        )
        if hours_match:
            result["estimated_hours"] = float(hours_match.group(1))
    
    # 解析复杂度
    if "## 🎯 复杂度" in content:
        complexity_match = re.search(
            r'## 🎯 复杂度\n\n(\w+)', content
        )
        if complexity_match:
            complexity = complexity_match.group(1).lower()
            if complexity in ["low", "medium", "high"]:
                result["complexity"] = complexity
    
    return result


def extract_code_blocks(content: str, language: str = "python") -> List[str]:
    """从 Markdown 中提取代码块
    
    Args:
        content: Markdown 内容
        language: 编程语言 (默认 python)
        
    Returns:
        代码块列表
    """
    pattern = rf'```{language}\n(.*?)\n```'
    blocks = re.findall(pattern, content, re.DOTALL)
    return blocks


def extract_section(content: str, section_title: str) -> str:
    """从 Markdown 中提取特定章节
    
    Args:
        content: Markdown 内容
        section_title: 章节标题
        
    Returns:
        章节内容
    """
    pattern = rf'## {section_title}\n\n(.+?)(?=\n## |\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""
