"""
配置管理模块

用于加载和管理自动化系统的所有配置
- Claude API 配置
- 路径配置
- Worker 配置
- 审查配置
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any


class AutomationConfig:
    """自动化配置类
    
    负责加载 YAML 配置文件，并支持环境变量替换
    """
    
    def __init__(self, config_path: str = "automation-config/automation.yaml"):
        """初始化配置管理器
        
        Args:
            config_path: 配置文件路径，相对于项目根目录
            
        Raises:
            FileNotFoundError: 配置文件不存在时抛出
        """
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件
        
        Returns:
            解析后的配置字典
            
        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: YAML 格式错误
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config is None:
                config = {}
            
            # 环境变量替换
            config = self._replace_env_vars(config)
            return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"配置文件格式错误: {e}")
    
    def _replace_env_vars(self, obj: Any) -> Any:
        """递归替换环境变量
        
        支持 ${VAR_NAME} 格式的环境变量替换
        
        Args:
            obj: 要处理的对象（支持 dict、list、str）
            
        Returns:
            替换后的对象
        """
        if isinstance(obj, dict):
            return {k: self._replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
            env_var = obj[2:-1]
            value = os.getenv(env_var)
            if value is None:
                # 环境变量未设置，保持原样
                return obj
            return value
        else:
            return obj
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（支持点号路径）
        
        Args:
            key: 配置键，支持点号分隔的路径，如 'claude.api_key'
            default: 默认值，如果键不存在则返回
            
        Returns:
            配置值或默认值
            
        Example:
            >>> config.get('claude.pm_model')
            'claude-4.5-sonnet-20250514'
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置
        
        Returns:
            完整的配置字典
        """
        return self._config


# 全局配置实例
try:
    config = AutomationConfig()
except FileNotFoundError:
    # 未找到配置文件，使用空配置
    config = AutomationConfig.__new__(AutomationConfig)
    config._config = {}
