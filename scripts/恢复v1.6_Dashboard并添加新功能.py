#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从v1.6恢复Dashboard，然后只添加必要的新功能
"""

import shutil
from pathlib import Path

V16_DASHBOARD = Path(__file__).parent.parent.parent / "任务所-v1.6-Tab修复版/industrial_dashboard"
V17_DASHBOARD = Path(__file__).parent.parent / "apps/dashboard/src/industrial_dashboard"

def restore_and_upgrade():
    """恢复v1.6并升级"""
    
    print("=" * 70)
    print("恢复v1.6 Dashboard并添加新功能")
    print("=" * 70)
    print()
    
    # 1. 备份当前v1.7
    backup = V17_DASHBOARD.parent / "industrial_dashboard_backup"
    if V17_DASHBOARD.exists():
        if backup.exists():
            shutil.rmtree(backup)
        shutil.copytree(V17_DASHBOARD, backup)
        print("[BACKUP] v1.7已备份")
    
    # 2. 删除v1.7
    if V17_DASHBOARD.exists():
        shutil.rmtree(V17_DASHBOARD)
        print("[DELETE] v1.7已删除")
    
    # 3. 复制v1.6
    shutil.copytree(V16_DASHBOARD, V17_DASHBOARD)
    print("[COPY] v1.6已复制到v1.7")
    
    # 4. 修改start_dashboard.py的端口为8879（全新端口）
    start_script = V17_DASHBOARD.parent / "start_dashboard.py"
    if start_script.exists():
        content = start_script.read_text(encoding='utf-8')
        # 修改端口
        content = content.replace('port=8877', 'port=8879')
        content = content.replace('port=8860', 'port=8879')
        start_script.write_text(content, encoding='utf-8')
        print("[UPDATE] 启动端口改为8879（全新端口）")
    
    print()
    print("=" * 70)
    print("[完成] v1.6恢复完成")
    print("=" * 70)
    print()
    print("v1.6是稳定版本，功能完整")
    print("新端口: 8879")
    print()
    print("启动: python apps/dashboard/start_dashboard.py")

if __name__ == "__main__":
    restore_and_upgrade()

