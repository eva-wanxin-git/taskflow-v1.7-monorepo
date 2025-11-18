#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端口管理器

负责为每个项目分配独立的端口，避免冲突
"""

import socket
import json
import sys
import io
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

# 设置UTF-8输出
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class PortManager:
    """端口管理器
    
    功能：
    1. 自动查询可用端口
    2. 为项目分配独立端口
    3. 记录端口分配历史
    4. 检测端口冲突
    """
    
    # 端口范围：8870-8899（任务所·Flow专用端口段）
    PORT_RANGE_START = 8870
    PORT_RANGE_END = 8899
    
    def __init__(self, config_path: str = "config/ports.json"):
        """初始化端口管理器
        
        Args:
            config_path: 端口配置文件路径
        """
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载或创建配置
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载端口配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 初始化空配置
            config = {
                "version": "1.0",
                "port_range": {
                    "start": self.PORT_RANGE_START,
                    "end": self.PORT_RANGE_END
                },
                "allocated_ports": {},  # project_code -> port
                "history": []
            }
            self._save_config(config)
            return config
    
    def _save_config(self, config: Dict) -> None:
        """保存端口配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def is_port_available(self, port: int) -> bool:
        """检查端口是否可用
        
        Args:
            port: 端口号
            
        Returns:
            True如果端口可用，False如果被占用
        """
        try:
            # 尝试绑定端口
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            # result == 0 表示端口被占用
            # result != 0 表示端口可用
            return result != 0
            
        except Exception:
            # 如果出现异常，认为端口不可用（保守策略）
            return False
    
    def find_available_port(
        self,
        start: Optional[int] = None,
        end: Optional[int] = None
    ) -> Optional[int]:
        """查找可用端口
        
        Args:
            start: 起始端口（默认使用PORT_RANGE_START）
            end: 结束端口（默认使用PORT_RANGE_END）
            
        Returns:
            可用端口号，如果没有可用端口返回None
        """
        start = start or self.PORT_RANGE_START
        end = end or self.PORT_RANGE_END
        
        # 获取已分配的端口列表（active状态）
        allocated_ports = set()
        for info in self.config["allocated_ports"].values():
            if info.get("status") == "active":
                allocated_ports.add(info["port"])
        
        # 查找未分配且系统可用的端口
        for port in range(start, end + 1):
            # 跳过已分配的端口
            if port in allocated_ports:
                continue
            # 检查系统是否可用
            if self.is_port_available(port):
                return port
        
        return None
    
    def allocate_port_for_project(self, project_code: str) -> int:
        """为项目分配端口
        
        如果项目已有端口，返回已分配的端口
        如果项目没有端口，分配一个新的可用端口
        
        Args:
            project_code: 项目代码
            
        Returns:
            分配的端口号
            
        Raises:
            RuntimeError: 如果没有可用端口
        """
        # 1. 检查是否已分配
        allocated = self.config["allocated_ports"]
        if project_code in allocated:
            existing_port = allocated[project_code]["port"]
            print(f"✓ 项目 {project_code} 已有端口: {existing_port}")
            return existing_port
        
        # 2. 查找可用端口
        port = self.find_available_port()
        if port is None:
            raise RuntimeError(
                f"端口范围 {self.PORT_RANGE_START}-{self.PORT_RANGE_END} "
                f"内没有可用端口"
            )
        
        # 3. 记录分配
        allocated[project_code] = {
            "port": port,
            "allocated_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # 4. 记录历史
        self.config["history"].append({
            "action": "allocate",
            "project_code": project_code,
            "port": port,
            "timestamp": datetime.now().isoformat()
        })
        
        # 5. 保存配置
        self._save_config(self.config)
        
        print(f"✓ 为项目 {project_code} 分配端口: {port}")
        return port
    
    def get_port_for_project(self, project_code: str) -> Optional[int]:
        """获取项目的端口
        
        Args:
            project_code: 项目代码
            
        Returns:
            端口号，如果未分配返回None
        """
        allocated = self.config["allocated_ports"]
        if project_code in allocated:
            return allocated[project_code]["port"]
        return None
    
    def list_allocated_ports(self) -> Dict[str, int]:
        """列出所有已分配的端口
        
        Returns:
            {project_code: port} 字典
        """
        result = {}
        for project_code, info in self.config["allocated_ports"].items():
            result[project_code] = info["port"]
        return result
    
    def release_port(self, project_code: str) -> bool:
        """释放项目的端口
        
        Args:
            project_code: 项目代码
            
        Returns:
            True如果成功释放，False如果项目没有分配端口
        """
        allocated = self.config["allocated_ports"]
        if project_code not in allocated:
            return False
        
        port = allocated[project_code]["port"]
        
        # 标记为释放（不直接删除，保留历史）
        allocated[project_code]["status"] = "released"
        allocated[project_code]["released_at"] = datetime.now().isoformat()
        
        # 记录历史
        self.config["history"].append({
            "action": "release",
            "project_code": project_code,
            "port": port,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_config(self.config)
        
        print(f"✓ 已释放项目 {project_code} 的端口: {port}")
        return True
    
    def get_available_ports_summary(self) -> Dict:
        """获取端口使用摘要
        
        Returns:
            {
                "total": 30,
                "available": 25,
                "allocated": 5,
                "ports": [...]
            }
        """
        total = self.PORT_RANGE_END - self.PORT_RANGE_START + 1
        allocated_active = sum(
            1 for info in self.config["allocated_ports"].values()
            if info.get("status") == "active"
        )
        available = total - allocated_active
        
        # 列出已分配的端口
        allocated_ports = [
            {
                "project": project,
                "port": info["port"],
                "allocated_at": info["allocated_at"]
            }
            for project, info in self.config["allocated_ports"].items()
            if info.get("status") == "active"
        ]
        
        return {
            "total": total,
            "available": available,
            "allocated": allocated_active,
            "port_range": f"{self.PORT_RANGE_START}-{self.PORT_RANGE_END}",
            "allocated_ports": allocated_ports
        }


# ============================================================================
# 便捷函数
# ============================================================================

def allocate_project_port(project_code: str) -> int:
    """为项目分配端口（便捷函数）"""
    manager = PortManager()
    return manager.allocate_port_for_project(project_code)


def get_project_port(project_code: str) -> Optional[int]:
    """获取项目端口（便捷函数）"""
    manager = PortManager()
    return manager.get_port_for_project(project_code)


def list_all_ports() -> Dict[str, int]:
    """列出所有端口分配（便捷函数）"""
    manager = PortManager()
    return manager.list_allocated_ports()


def show_port_summary():
    """显示端口使用摘要（便捷函数）"""
    manager = PortManager()
    summary = manager.get_available_ports_summary()
    
    print("\n" + "="*70)
    print("任务所·Flow 端口使用情况")
    print("="*70)
    print(f"端口范围：{summary['port_range']}")
    print(f"总端口数：{summary['total']}")
    print(f"可用端口：{summary['available']}")
    print(f"已分配：{summary['allocated']}")
    print()
    
    if summary['allocated_ports']:
        print("已分配端口：")
        for item in summary['allocated_ports']:
            print(f"  - {item['project']:20s} → 端口 {item['port']}")
    else:
        print("  （暂无分配）")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    # 测试
    show_port_summary()
    
    # 为任务所·Flow本身分配端口
    port = allocate_project_port("TASKFLOW")
    print(f"\n任务所·Flow 端口: {port}")
    
    # 为测试项目分配端口
    test_port = allocate_project_port("TEST_PROJECT")
    print(f"测试项目 端口: {test_port}")
    
    # 显示摘要
    show_port_summary()

