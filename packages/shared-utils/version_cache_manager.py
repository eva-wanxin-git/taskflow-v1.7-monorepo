#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
版本缓存管理器 - 解决浏览器缓存问题

功能：
1. 自动版本号生成（基于时间戳）
2. 提供URL版本参数
3. 管理版本历史
4. 支持手动版本更新
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class VersionCacheManager:
    """版本缓存管理器"""
    
    def __init__(self, version_file: str = "version.json"):
        """
        初始化版本管理器
        
        Args:
            version_file: 版本信息文件路径
        """
        self.version_file = Path(version_file)
        self.current_version = self._load_or_create_version()
    
    def _load_or_create_version(self) -> str:
        """加载或创建版本信息"""
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("current", self._generate_version())
            except Exception:
                return self._generate_version()
        else:
            # 创建新版本
            version = self._generate_version()
            self._save_version(version)
            return version
    
    def _generate_version(self) -> str:
        """
        生成新版本号
        
        格式：v{timestamp}
        例如：v20251118193000
        """
        return f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _save_version(self, version: str):
        """保存版本信息到文件"""
        try:
            # 读取历史版本
            history = []
            if self.version_file.exists():
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history = data.get("history", [])
            
            # 添加当前版本到历史（保留最近20个）
            if hasattr(self, 'current_version') and self.current_version:
                history.insert(0, {
                    "version": self.current_version,
                    "replaced_at": datetime.now().isoformat()
                })
                history = history[:20]
            
            # 保存新版本
            data = {
                "current": version,
                "updated_at": datetime.now().isoformat(),
                "history": history
            }
            
            self.version_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.version_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"⚠️ 保存版本信息失败: {e}")
    
    def get_version(self) -> str:
        """
        获取当前版本号
        
        Returns:
            版本号字符串，例如 'v20251118193000'
        """
        return self.current_version
    
    def get_version_param(self) -> str:
        """
        获取URL版本参数
        
        Returns:
            URL参数字符串，例如 'v=v20251118193000'
        """
        return f"v={self.current_version}"
    
    def bump_version(self) -> str:
        """
        手动更新版本号
        
        Returns:
            新版本号
        """
        new_version = self._generate_version()
        self._save_version(new_version)
        self.current_version = new_version
        print(f"✅ 版本已更新: {new_version}")
        return new_version
    
    def get_history(self) -> list:
        """
        获取版本历史
        
        Returns:
            版本历史列表
        """
        try:
            if self.version_file.exists():
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("history", [])
        except Exception:
            pass
        return []
    
    def get_info(self) -> Dict:
        """
        获取版本信息
        
        Returns:
            包含当前版本、更新时间、历史等信息的字典
        """
        history = self.get_history()
        return {
            "current_version": self.current_version,
            "param": self.get_version_param(),
            "history_count": len(history),
            "latest_history": history[:5] if history else []
        }


# 全局实例（供Dashboard使用）
_global_version_manager: Optional[VersionCacheManager] = None


def get_version_manager(version_file: str = "version.json") -> VersionCacheManager:
    """
    获取全局版本管理器实例（单例模式）
    
    Args:
        version_file: 版本文件路径
        
    Returns:
        VersionCacheManager实例
    """
    global _global_version_manager
    if _global_version_manager is None:
        _global_version_manager = VersionCacheManager(version_file)
    return _global_version_manager


if __name__ == "__main__":
    # 测试代码
    vm = VersionCacheManager("test_version.json")
    print(f"当前版本: {vm.get_version()}")
    print(f"URL参数: {vm.get_version_param()}")
    print(f"版本信息: {vm.get_info()}")
    
    # 测试版本更新
    print("\n更新版本...")
    new_version = vm.bump_version()
    print(f"新版本: {new_version}")
    print(f"历史记录: {len(vm.get_history())}条")

