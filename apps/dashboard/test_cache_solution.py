#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试缓存解决方案

验证4个核心功能：
1. 版本号URL参数
2. no-cache HTTP头
3. Service Worker版本控制
4. 清除缓存按钮
"""
import sys
from pathlib import Path
import time

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages" / "shared-utils"))
from version_cache_manager import VersionCacheManager


def test_version_manager():
    """测试版本管理器"""
    print("\n" + "=" * 70)
    print("测试 1: 版本管理器")
    print("=" * 70)
    
    # 创建临时版本管理器
    vm = VersionCacheManager("test_version.json")
    
    print(f"✓ 版本管理器初始化成功")
    print(f"  当前版本: {vm.get_version()}")
    print(f"  URL参数: {vm.get_version_param()}")
    
    # 测试版本更新
    old_version = vm.get_version()
    time.sleep(0.1)  # 确保版本号不同
    new_version = vm.bump_version()
    
    assert old_version != new_version, "版本更新失败"
    print(f"✓ 版本更新成功: {old_version} -> {new_version}")
    
    # 测试版本历史
    history = vm.get_history()
    assert len(history) >= 1, "版本历史记录失败"
    print(f"✓ 版本历史记录成功: {len(history)} 条记录")
    
    # 清理测试文件
    test_file = Path("test_version.json")
    if test_file.exists():
        test_file.unlink()
    
    print("✅ 版本管理器测试通过\n")


def test_dashboard_integration():
    """测试Dashboard集成"""
    print("=" * 70)
    print("测试 2: Dashboard集成")
    print("=" * 70)
    
    # 检查关键文件
    files_to_check = [
        ("版本管理模块", Path(__file__).parent.parent.parent / "packages" / "shared-utils" / "version_cache_manager.py"),
        ("Service Worker", Path(__file__).parent / "src" / "industrial_dashboard" / "static" / "sw.js"),
        ("Dashboard主文件", Path(__file__).parent / "src" / "industrial_dashboard" / "dashboard.py"),
        ("模板文件", Path(__file__).parent / "src" / "industrial_dashboard" / "templates.py"),
    ]
    
    all_exist = True
    for name, file_path in files_to_check:
        if file_path.exists():
            print(f"✓ {name}: {file_path.name}")
        else:
            print(f"✗ {name}: 文件不存在")
            all_exist = False
    
    if all_exist:
        print("✅ 所有关键文件存在\n")
    else:
        print("⚠️ 部分文件缺失\n")
        return False
    
    return True


def test_api_endpoints():
    """测试API端点（需要服务器运行）"""
    print("=" * 70)
    print("测试 3: API端点")
    print("=" * 70)
    
    print("⚠️ 此测试需要Dashboard服务器运行")
    print("  请手动测试以下端点:")
    print("  1. GET  /api/cache/version  - 获取缓存版本")
    print("  2. POST /api/cache/bump     - 更新缓存版本")
    print("  3. POST /api/cache/clear    - 清除缓存")
    print("  4. GET  /static/sw.js       - Service Worker文件")
    print()


def test_service_worker():
    """测试Service Worker"""
    print("=" * 70)
    print("测试 4: Service Worker")
    print("=" * 70)
    
    sw_file = Path(__file__).parent / "src" / "industrial_dashboard" / "static" / "sw.js"
    
    if not sw_file.exists():
        print("✗ Service Worker文件不存在")
        return False
    
    # 读取并检查关键功能
    content = sw_file.read_text(encoding='utf-8')
    
    checks = [
        ("缓存前缀定义", "CACHE_PREFIX"),
        ("版本控制", "CACHE_VERSION"),
        ("不缓存模式", "NO_CACHE_PATTERNS"),
        ("install事件", "addEventListener('install'"),
        ("activate事件", "addEventListener('activate'"),
        ("fetch拦截", "addEventListener('fetch'"),
        ("消息监听", "addEventListener('message'"),
        ("版本检查", "CHECK_VERSION"),
        ("缓存清除", "CLEAR_CACHE"),
    ]
    
    all_passed = True
    for name, keyword in checks:
        if keyword in content:
            print(f"✓ {name}")
        else:
            print(f"✗ {name}: 未找到")
            all_passed = False
    
    if all_passed:
        print("✅ Service Worker功能完整\n")
    else:
        print("⚠️ Service Worker部分功能缺失\n")
    
    return all_passed


def test_ui_components():
    """测试UI组件"""
    print("=" * 70)
    print("测试 5: UI组件")
    print("=" * 70)
    
    template_file = Path(__file__).parent / "src" / "industrial_dashboard" / "templates.py"
    
    if not template_file.exists():
        print("✗ 模板文件不存在")
        return False
    
    # 读取并检查UI组件
    content = template_file.read_text(encoding='utf-8')
    
    checks = [
        ("缓存版本显示", "cache-version-display"),
        ("清除缓存按钮", "clearDashboardCache"),
        ("Service Worker注册", "serviceWorker.register"),
        ("版本检查函数", "checkCacheVersion"),
        ("版本更新通知", "showVersionUpdateNotification"),
        ("no-cache meta标签", 'meta http-equiv="Cache-Control"'),
        ("cache_version参数", "cache_version:"),
    ]
    
    all_passed = True
    for name, keyword in checks:
        if keyword in content:
            print(f"✓ {name}")
        else:
            print(f"✗ {name}: 未找到")
            all_passed = False
    
    if all_passed:
        print("✅ UI组件完整\n")
    else:
        print("⚠️ UI组件部分功能缺失\n")
    
    return all_passed


def main():
    """主测试函数"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "缓存解决方案测试" + " " * 22 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = []
    
    # 运行测试
    try:
        test_version_manager()
        results.append(("版本管理器", True))
    except Exception as e:
        print(f"✗ 版本管理器测试失败: {e}\n")
        results.append(("版本管理器", False))
    
    try:
        result = test_dashboard_integration()
        results.append(("Dashboard集成", result))
    except Exception as e:
        print(f"✗ Dashboard集成测试失败: {e}\n")
        results.append(("Dashboard集成", False))
    
    test_api_endpoints()
    results.append(("API端点", None))  # 需要手动测试
    
    try:
        result = test_service_worker()
        results.append(("Service Worker", result))
    except Exception as e:
        print(f"✗ Service Worker测试失败: {e}\n")
        results.append(("Service Worker", False))
    
    try:
        result = test_ui_components()
        results.append(("UI组件", result))
    except Exception as e:
        print(f"✗ UI组件测试失败: {e}\n")
        results.append(("UI组件", False))
    
    # 显示测试总结
    print("=" * 70)
    print("测试总结")
    print("=" * 70)
    
    for name, result in results:
        if result is True:
            print(f"✅ {name}: 通过")
        elif result is False:
            print(f"❌ {name}: 失败")
        else:
            print(f"⚠️  {name}: 需要手动测试")
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    manual = sum(1 for _, r in results if r is None)
    
    print()
    print(f"总计: {passed} 通过, {failed} 失败, {manual} 需要手动测试")
    print("=" * 70)
    
    # 使用说明
    print()
    print("📋 手动测试步骤：")
    print()
    print("1. 启动Dashboard服务器:")
    print("   cd apps/dashboard")
    print("   python start_dashboard.py")
    print()
    print("2. 打开浏览器访问 http://127.0.0.1:8877")
    print()
    print("3. 检查页面是否显示\"缓存版本\"和\"清除缓存\"按钮")
    print()
    print("4. 打开浏览器开发者工具 (F12):")
    print("   - Application -> Service Workers -> 检查是否注册成功")
    print("   - Console -> 查看 [缓存管理] 日志")
    print()
    print("5. 点击\"清除缓存\"按钮，验证:")
    print("   - 是否显示确认对话框")
    print("   - 是否显示\"缓存已清除\"提示")
    print("   - 页面是否自动刷新")
    print("   - 版本号是否更新")
    print()
    print("6. 修改代码后刷新页面 (Ctrl+F5):")
    print("   - 检查是否看到最新内容")
    print("   - 不需要换端口")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

