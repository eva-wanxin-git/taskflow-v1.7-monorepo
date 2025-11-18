#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务所·Flow v1.7 - Dashboard启动脚本

继承v1.6的完整功能 + v1.7的增强（多项目、端口管理）
"""
import sys
import os
import argparse
from pathlib import Path

# ⚠️ 重要：设置工作目录到 apps/dashboard
# 这样所有相对路径 "automation-data/..." 才能正确解析
dashboard_dir = Path(__file__).parent
os.chdir(dashboard_dir)

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from industrial_dashboard import IndustrialDashboard
from industrial_dashboard.adapters import StateManagerAdapter
from automation.state_manager import StateManager

# 添加端口管理
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages" / "shared-utils"))
from port_manager import PortManager


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="任务所·Flow v1.7 Dashboard")
    parser.add_argument("--port", type=int, default=8877, help="Dashboard端口号（默认8877）")
    args = parser.parse_args()
    
    print()
    print("=" * 70)
    print("任务所·Flow v1.7 - Dashboard")
    print("=" * 70)
    print()
    
    # 显示工作目录（用于诊断）
    print(f"[OK] 工作目录: {os.getcwd()}")
    automation_data = Path(os.getcwd()) / "automation-data"
    print(f"[OK] 数据目录: {automation_data}")
    print(f"[OK] 数据目录存在: {automation_data.exists()}")
    print()
    
    # 项目代码
    project_code = "TASKFLOW-v17"
    
    # 使用命令行指定的端口或默认端口8877
    port = args.port
    print(f"[OK] 端口分配: {port}")
    
    # 初始化StateManager（使用v1.7的数据库）
    db_path = Path(__file__).parent.parent.parent / "database" / "data" / "tasks.db"
    sm = StateManager(db_path=str(db_path))
    print("[OK] StateManager initialized")
    
    # 创建适配器
    provider = StateManagerAdapter(sm)
    print("[OK] Data provider created")
    
    # 创建Dashboard（继承v1.6的完整功能）
    dashboard = IndustrialDashboard(
        data_provider=provider,
        title="任务所·FLOW v1.7",
        subtitle="企业级AI任务中枢 | 多项目支持 + 智能端口管理",
        port=port,
        host="127.0.0.1"
    )
    print("[OK] Dashboard ready")
    print()
    print(f"访问地址: http://127.0.0.1:{port}")
    print("=" * 70)
    print()
    
    # 启动
    dashboard.run(open_browser=True)


if __name__ == "__main__":
    main()

