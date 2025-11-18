#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目扫描器 - 自动扫描项目结构和功能
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ProjectScanner:
    """项目扫描器 - 识别已实现/部分实现/冲突功能"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.scan_result = {}
    
    def scan_project(self) -> Dict[str, Any]:
        """扫描项目，返回完整分析结果"""
        print("[扫描] 开始扫描项目...")
        
        result = {
            "scan_time": datetime.now().isoformat(),
            "project_path": str(self.project_path.absolute()),
            "project_name": self._detect_project_name(),
            "project_type": self._detect_project_type(),
            "files_count": self._count_files(),
            "technologies": self._detect_technologies(),
            "features": {
                "implemented": self._scan_implemented_features(),
                "partial": self._scan_partial_features(),
                "conflicts": self._scan_conflict_features()
            },
            "structure": self._analyze_structure()
        }
        
        self.scan_result = result
        print(f"[扫描] 完成！识别到 {len(result['features']['implemented'])} 个已实现功能")
        return result
    
    def _detect_project_name(self) -> str:
        """检测项目名称"""
        # 从package.json读取
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("name", self.project_path.name)
            except:
                pass
        
        # 从README读取
        for readme in ["README.md", "README.txt", "readme.md"]:
            readme_file = self.project_path / readme
            if readme_file.exists():
                try:
                    with open(readme_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith('#'):
                            return first_line.replace('#', '').strip()
                except:
                    pass
        
        return self.project_path.name
    
    def _detect_project_type(self) -> str:
        """检测项目类型"""
        # Python项目
        if (self.project_path / "requirements.txt").exists() or \
           (self.project_path / "setup.py").exists() or \
           (self.project_path / "pyproject.toml").exists():
            if (self.project_path / "app").exists() or (self.project_path / "api").exists():
                return "Python后端项目 (FastAPI/Flask)"
            return "Python项目"
        
        # Node.js项目
        if (self.project_path / "package.json").exists():
            package_json = self.project_path / "package.json"
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    deps = data.get("dependencies", {})
                    if "react" in deps:
                        return "React前端项目"
                    elif "vue" in deps:
                        return "Vue前端项目"
                    elif "next" in deps:
                        return "Next.js全栈项目"
                    return "Node.js项目"
            except:
                return "Node.js项目"
        
        return "未知类型"
    
    def _count_files(self) -> Dict[str, int]:
        """统计文件数量"""
        counts = {
            "python": 0,
            "javascript": 0,
            "typescript": 0,
            "markdown": 0,
            "json": 0,
            "yaml": 0,
            "total": 0
        }
        
        extensions = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".md": "markdown",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml"
        }
        
        for root, dirs, files in os.walk(self.project_path):
            # 跳过常见的排除目录
            dirs[:] = [d for d in dirs if d not in [
                'node_modules', '__pycache__', '.git', 'venv', 
                '.venv', 'dist', 'build', '.next'
            ]]
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in extensions:
                    counts[extensions[ext]] += 1
                    counts["total"] += 1
        
        return counts
    
    def _detect_technologies(self) -> List[str]:
        """检测使用的技术栈"""
        techs = []
        
        # Python相关
        if (self.project_path / "requirements.txt").exists():
            try:
                with open(self.project_path / "requirements.txt", 'r') as f:
                    content = f.read().lower()
                    if "fastapi" in content:
                        techs.append("FastAPI")
                    if "flask" in content:
                        techs.append("Flask")
                    if "django" in content:
                        techs.append("Django")
                    if "sqlalchemy" in content:
                        techs.append("SQLAlchemy")
                    if "pytest" in content:
                        techs.append("Pytest")
            except:
                pass
        
        # Node.js相关
        if (self.project_path / "package.json").exists():
            try:
                with open(self.project_path / "package.json", 'r') as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                    
                    if "react" in deps:
                        techs.append("React")
                    if "vue" in deps:
                        techs.append("Vue")
                    if "typescript" in deps:
                        techs.append("TypeScript")
                    if "express" in deps:
                        techs.append("Express")
            except:
                pass
        
        return techs if techs else ["未识别"]
    
    def _scan_implemented_features(self) -> List[Dict[str, Any]]:
        """扫描已实现的功能"""
        features = []
        
        # 扫描Python项目的API端点
        for py_file in self.project_path.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['__pycache__', 'venv', '.venv', 'test']):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 检测API端点
                    if "@app.get" in content or "@app.post" in content:
                        features.append({
                            "name": f"API接口 - {py_file.stem}",
                            "file": str(py_file.relative_to(self.project_path)),
                            "type": "后端API",
                            "status": "已实现"
                        })
                    
                    # 检测类定义
                    if "class " in content and "def __init__" in content:
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.strip().startswith('class ') and '(' in line:
                                class_name = line.split('class ')[1].split('(')[0].strip()
                                # 检查是否有文档字符串
                                if i + 1 < len(lines) and '"""' in lines[i + 1]:
                                    features.append({
                                        "name": f"{class_name}类",
                                        "file": str(py_file.relative_to(self.project_path)),
                                        "type": "核心模块",
                                        "status": "已实现"
                                    })
                                    break
            except:
                pass
        
        # 如果没识别到，添加默认功能
        if not features:
            features = [
                {"name": "项目基础框架", "file": "—", "type": "基础", "status": "已实现"},
                {"name": "文件目录结构", "file": "—", "type": "基础", "status": "已实现"}
            ]
        
        return features[:20]  # 最多20个
    
    def _scan_partial_features(self) -> List[Dict[str, Any]]:
        """扫描部分实现的功能"""
        features = []
        
        # 检查TODO/FIXME标记
        for py_file in self.project_path.rglob("*.py"):
            if any(skip in str(py_file) for skip in ['__pycache__', 'venv', '.venv']):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if "TODO" in line or "FIXME" in line:
                            features.append({
                                "name": line.strip().replace('#', '').replace('TODO:', '').replace('FIXME:', '').strip()[:50],
                                "file": str(py_file.relative_to(self.project_path)),
                                "line": i + 1,
                                "type": "待完善",
                                "status": "部分实现"
                            })
                            if len(features) >= 10:
                                break
                    if len(features) >= 10:
                        break
            except:
                pass
        
        return features
    
    def _scan_conflict_features(self) -> List[Dict[str, Any]]:
        """扫描冲突或建议取舍的功能"""
        conflicts = []
        
        # 检查重复文件
        file_names = {}
        for file in self.project_path.rglob("*.py"):
            if any(skip in str(file) for skip in ['__pycache__', 'venv', '.venv']):
                continue
            
            name = file.stem
            if name in file_names:
                conflicts.append({
                    "name": f"重复文件名: {name}.py",
                    "files": [str(f.relative_to(self.project_path)) for f in [file_names[name], file]],
                    "type": "命名冲突",
                    "suggestion": "建议重命名或合并"
                })
            else:
                file_names[name] = file
        
        return conflicts
    
    def _analyze_structure(self) -> Dict[str, Any]:
        """分析项目结构"""
        structure = {
            "has_tests": False,
            "has_docs": False,
            "has_config": False,
            "has_api": False,
            "has_database": False
        }
        
        # 检查测试目录
        for test_dir in ["tests", "test", "__tests__"]:
            if (self.project_path / test_dir).exists():
                structure["has_tests"] = True
                break
        
        # 检查文档
        for doc_file in ["README.md", "docs"]:
            if (self.project_path / doc_file).exists():
                structure["has_docs"] = True
                break
        
        # 检查配置文件
        config_files = ["config.py", "config.json", "settings.py", ".env"]
        for config in config_files:
            if (self.project_path / config).exists():
                structure["has_config"] = True
                break
        
        # 检查API
        for api_dir in ["api", "app", "src/api"]:
            if (self.project_path / api_dir).exists():
                structure["has_api"] = True
                break
        
        # 检查数据库
        for db_file in ["*.db", "*.sqlite", "*.sqlite3"]:
            if list(self.project_path.glob(db_file)):
                structure["has_database"] = True
                break
        
        return structure
    
    def save_scan_result(self) -> Dict[str, Any]:
        """保存扫描结果到文件"""
        if not self.scan_result:
            self.scan_project()
        
        # 保存到automation-data
        data_dir = self.project_path / "automation-data"
        data_dir.mkdir(exist_ok=True)
        
        output_file = data_dir / "project_scan.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.scan_result, f, ensure_ascii=False, indent=2)
        
        print(f"[保存] 扫描结果已保存到: {output_file}")
        return self.scan_result
    
    def initialize_with_knowledge_base(self) -> Dict[str, Any]:
        """扫描项目并初始化知识库"""
        # 1. 扫描项目
        scan_result = self.scan_project()
        
        # 2. 初始化知识库
        try:
            from automation.knowledge_base_initializer import KnowledgeBaseInitializer
            kb_init = KnowledgeBaseInitializer("automation-data")
            kb_result = kb_init.initialize_all(scan_result)
            scan_result["knowledge_base"] = kb_result
        except Exception as e:
            print(f"[警告] 知识库初始化失败: {e}")
            scan_result["knowledge_base"] = {"status": "failed", "error": str(e)}
        
        # 3. 保存结果
        data_dir = self.project_path / "automation-data"
        output_file = data_dir / "project_scan.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scan_result, f, ensure_ascii=False, indent=2)
        
        return scan_result


if __name__ == "__main__":
    scanner = ProjectScanner(".")
    result = scanner.save_scan_result()
    
    print("\n" + "=" * 70)
    print("项目扫描报告")
    print("=" * 70)
    print(f"\n项目名称: {result['project_name']}")
    print(f"项目类型: {result['project_type']}")
    print(f"技术栈: {', '.join(result['technologies'])}")
    print(f"\n代码文件: Python={result['files_count']['python']}, "
          f"JS/TS={result['files_count']['javascript'] + result['files_count']['typescript']}")
    print(f"\n已实现功能: {len(result['features']['implemented'])} 个")
    print(f"部分实现: {len(result['features']['partial'])} 个")
    print(f"冲突/建议: {len(result['features']['conflicts'])} 个")
    print("\n" + "=" * 70)

