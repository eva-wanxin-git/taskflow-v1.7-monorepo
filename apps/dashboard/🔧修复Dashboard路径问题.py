#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🔧 修复 Dashboard 路径问题

问题: 功能清单、架构师模块、提示词等内容没有显示
原因: 相对路径 Path("automation-data/...") 基于启动时的工作目录
解决: 将所有相对路径改为基于 apps/dashboard 的绝对路径

修复步骤:
1. 确定 apps/dashboard 的正确路径
2. 在 dashboard.py 初始化时设置工作目录
3. 所有数据文件路径都基于 apps/dashboard
"""

import sys
from pathlib import Path
import json

def diagnose():
    """诊断当前问题"""
    print("=" * 70)
    print("🔧 Dashboard 路径诊断")
    print("=" * 70)
    print()
    
    # 1. 找到 dashboard.py 的位置
    dashboard_py = Path(__file__).parent / "src" / "industrial_dashboard" / "dashboard.py"
    print(f"✓ dashboard.py 路径: {dashboard_py}")
    print(f"✓ 存在: {dashboard_py.exists()}")
    print()
    
    # 2. 找到 apps/dashboard 根目录
    app_dashboard_root = Path(__file__).parent
    print(f"✓ apps/dashboard 根: {app_dashboard_root}")
    print(f"✓ 存在: {app_dashboard_root.exists()}")
    print()
    
    # 3. 检查 automation-data 目录
    automation_data = app_dashboard_root / "automation-data"
    print(f"✓ automation-data 路径: {automation_data}")
    print(f"✓ 存在: {automation_data.exists()}")
    print()
    
    # 4. 检查关键数据文件
    files_to_check = [
        "architect_monitor.json",
        "architect_events.json",
        "v17-complete-features.json",
        "design_confirmations.json",
    ]
    
    print("关键数据文件检查:")
    for filename in files_to_check:
        filepath = automation_data / filename
        exists = "✅" if filepath.exists() else "❌"
        print(f"  {exists} {filename}")
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"      └─ 大小: {size} bytes")
    print()
    
    # 5. 列出 automation-data 中的 JSON 文件
    print("automation-data 中的数据文件:")
    if automation_data.exists():
        json_files = list(automation_data.glob("*.json"))
        for jf in json_files:
            size = jf.stat().st_size
            print(f"  ✓ {jf.name} ({size} bytes)")
    print()
    
    return app_dashboard_root

def fix_dashboard_py(dashboard_root):
    """修复 dashboard.py 中的路径问题"""
    
    print("=" * 70)
    print("🔧 修复步骤 1: 更新 dashboard.py")
    print("=" * 70)
    print()
    
    dashboard_py = dashboard_root / "src" / "industrial_dashboard" / "dashboard.py"
    
    # 读取文件
    with open(dashboard_py, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有 dashboard_root 设置
    if "self.dashboard_root" in content:
        print("✓ dashboard.py 已经有 dashboard_root 设置")
        return True
    
    # 在 __init__ 方法中找到 version_file 的设置位置，在之后添加 dashboard_root
    print("正在扫描需要修复的位置...")
    
    # 找到 version_file 的定义
    version_file_line = 'version_file = project_root / "automation-data" / "dashboard_version.json"'
    
    if version_file_line in content:
        # 在这行之后添加 dashboard_root 的设置
        replacement = version_file_line + '\n        self.dashboard_root = project_root / "apps" / "dashboard"'
        content = content.replace(version_file_line, replacement)
        print("✓ 已添加 dashboard_root 设置")
    
    # 现在替换所有的 Path("automation-data/...") 为 self.dashboard_root / "automation-data" / ...
    # 这需要小心处理，避免破坏代码
    
    old_pattern = 'Path("automation-data/'
    if old_pattern in content:
        print(f"✓ 检测到 {content.count(old_pattern)} 处需要修复的相对路径")
        
        # 这样修复可能比较复杂，需要逐行处理
        # 更好的办法是在路由函数开始时获取正确的路径
        
    return False

def create_patch_file():
    """创建补丁文件"""
    
    patch_content = '''
# 在 dashboard.py 的 _setup_routes 方法前添加以下代码

def _get_automation_data_path(self):
    """获取 automation-data 目录的绝对路径"""
    dashboard_root = Path(__file__).parent.parent.parent  # apps/dashboard
    return dashboard_root / "automation-data"

# 然后在所有使用 Path("automation-data/...") 的地方改为：
# data_file = self._get_automation_data_path() / "architect_monitor.json"

# 或者更简单的办法，在每个路由函数中添加：
# dashboard_root = Path(__file__).parent.parent.parent  # apps/dashboard
# automation_data = dashboard_root / "automation-data"
'''
    
    return patch_content

def main():
    """主诊断程序"""
    
    dashboard_root = diagnose()
    
    print("=" * 70)
    print("📋 问题分析")
    print("=" * 70)
    print()
    print("""
主要问题:
1. dashboard.py 中大量使用相对路径 Path("automation-data/...")
2. 这些路径是基于启动脚本的工作目录
3. 启动脚本可能不在 apps/dashboard 目录下
4. 导致 automation-data 目录找不到

症状:
✗ 功能清单模块显示为空
✗ 架构师模块没有数据
✗ 提示词内容不显示
✓ 但浏览器页面本身加载正常

根本原因:
  启动脚本的工作目录 ≠ apps/dashboard 目录
  相对路径 "automation-data/..." 无法正确解析
    """)
    
    print()
    print("=" * 70)
    print("✅ 解决方案")
    print("=" * 70)
    print()
    print("""
推荐修复方案 (简单快速):

在 start_dashboard.py 中添加以下代码:

```python
import os

def main():
    # 切换工作目录到 apps/dashboard
    dashboard_dir = Path(__file__).parent
    os.chdir(dashboard_dir)
    print(f"[OK] 工作目录已切换到: {os.getcwd()}")
    
    # ... 其他代码 ...
```

或者,  在 dashboard.py 的 _setup_routes 前添加:

```python
def _get_data_path(self, filename):
    '''获取数据文件的完整路径'''
    # 项目根: .../taskflow-v1.7-monorepo/
    # apps/dashboard 在: .../taskflow-v1.7-monorepo/apps/dashboard/
    dashboard_root = Path(__file__).parent.parent.parent / "apps" / "dashboard"
    return dashboard_root / "automation-data" / filename
```

然后在所有路由中使用:
```python
data_file = self._get_data_path("architect_monitor.json")
```
    """)
    
    print()
    print("=" * 70)
    print("🔧 快速修复命令")
    print("=" * 70)
    print()
    print(f"""
cd "{dashboard_root}"

# 或者
cd "{dashboard_root.parent.parent / 'apps' / 'dashboard'}"

# 然后启动:
python start_dashboard.py --port 8877

# 也可以修改 start_dashboard.py,  在 main() 开始添加:

import os
os.chdir(Path(__file__).parent)  # 切换到 apps/dashboard
    """)

if __name__ == "__main__":
    main()

