"""
版本管理系统

管理项目的不同版本，每个版本有独立的任务集和说明
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class VersionManager:
    """版本管理器"""
    
    def __init__(self, data_file: str = "automation-data/versions.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_data()
    
    def _load_data(self):
        """加载版本数据"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.versions = json.load(f)
        else:
            # 默认版本
            self.versions = {
                "current_version": "v1.0",
                "versions": [
                    {
                        "id": "v1.0",
                        "name": "版本 1.0 - MVP",
                        "description": "LibreChat Desktop 首个版本，实现核心桌面框架和基础功能",
                        "features": [
                            "Electron 桌面应用框架",
                            "LibreChat 对话集成",
                            "项目管理系统",
                            "AWS SSO 认证"
                        ],
                        "released_at": datetime.now().isoformat(),
                        "task_prefix": "phase1-"  # 这个版本的任务ID前缀
                    }
                ]
            }
            self._save_data()
    
    def _save_data(self):
        """保存版本数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.versions, f, ensure_ascii=False, indent=2)
    
    def add_version(
        self,
        version_id: str,
        name: str,
        description: str,
        features: List[str],
        upgrades: List[str] = None,
        task_prefix: str = ""
    ):
        """
        添加新版本
        
        Args:
            version_id: 版本ID（如 v2.0）
            name: 版本名称
            description: 版本描述
            features: 核心功能列表
            upgrades: 升级内容列表
            task_prefix: 任务ID前缀
        """
        version = {
            "id": version_id,
            "name": name,
            "description": description,
            "features": features,
            "upgrades": upgrades or [],
            "released_at": datetime.now().isoformat(),
            "task_prefix": task_prefix
        }
        
        self.versions["versions"].append(version)
        self._save_data()
        return version
    
    def get_all_versions(self) -> List[Dict]:
        """获取所有版本"""
        return self.versions["versions"]
    
    def get_current_version(self) -> str:
        """获取当前版本ID"""
        return self.versions["current_version"]
    
    def set_current_version(self, version_id: str):
        """设置当前版本"""
        self.versions["current_version"] = version_id
        self._save_data()
    
    def get_version_tasks(self, version_id: str, all_tasks: List) -> List:
        """获取指定版本的任务"""
        version = next((v for v in self.versions["versions"] if v["id"] == version_id), None)
        if not version:
            return []
        
        prefix = version.get("task_prefix", "")
        if prefix:
            return [t for t in all_tasks if t.id.startswith(prefix)]
        return all_tasks


# 初始化示例版本
if __name__ == "__main__":
    vm = VersionManager()
    
    # 添加 v2.0 版本示例
    vm.add_version(
        version_id="v2.0",
        name="版本 2.0 - 插件生态",
        description="引入完整的插件体系，支持扩展和自定义",
        features=[
            "插件API和加载器",
            "核心插件集（AWS、GitHub、Memory）",
            "插件市场",
            "Artifacts系统"
        ],
        upgrades=[
            "新增插件系统架构",
            "支持第三方插件开发",
            "插件市场浏览和安装",
            "Artifacts实时预览"
        ],
        task_prefix="phase3-"
    )
    
    print("[OK] Versions initialized")
    print(f"Versions: {[v['id'] for v in vm.get_all_versions()]}")

