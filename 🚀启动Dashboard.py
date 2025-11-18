#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务所·Flow v1.7 - Dashboard 一键启动脚本

功能：
1. 自动检查并安装Python依赖
2. 检查数据库和配置文件
3. 启动Dashboard服务
4. 自动打开浏览器

使用方法：
    python3 🚀启动Dashboard.py
"""

import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

def print_header(text):
    """打印标题"""
    print("\n" + "="*70)
    print(text)
    print("="*70 + "\n")

def print_step(step_num, total_steps, text):
    """打印步骤"""
    print(f"[步骤 {step_num}/{total_steps}] {text}")

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python版本过低，需要 Python 3.9+")
        print(f"   当前版本: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")

def check_and_install_package(package_name):
    """检查并安装Python包"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} 已安装")
        return True
    except ImportError:
        print(f"⚠️  {package_name} 未安装，正在安装...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package_name, "-q"
            ])
            print(f"✅ {package_name} 安装成功")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ {package_name} 安装失败")
            return False

def check_port(port):
    """检查端口是否被占用"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0  # True = 端口被占用

def main():
    """主函数"""
    print_header("任务所·Flow v1.7 - Dashboard 全自动启动")

    # 进入项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # 步骤1: 检查Python环境
    print_step(1, 5, "检查Python环境...")
    check_python_version()
    print()

    # 步骤2: 检查并安装依赖
    print_step(2, 5, "检查Python依赖...")
    dependencies = ["fastapi", "uvicorn", "requests"]
    all_installed = True
    for package in dependencies:
        if not check_and_install_package(package):
            all_installed = False

    if not all_installed:
        print("\n❌ 部分依赖安装失败，请手动安装:")
        print(f"   pip install {' '.join(dependencies)}")
        sys.exit(1)
    print()

    # 步骤3: 检查数据库
    print_step(3, 5, "检查数据库...")
    db_path = project_root / "database" / "data" / "tasks.db"
    if db_path.exists():
        db_size = db_path.stat().st_size / 1024  # KB
        print(f"✅ 数据库存在: {db_path} ({db_size:.1f} KB)")
    else:
        print(f"⚠️  数据库不存在: {db_path}")
        print("   Dashboard将使用默认配置")
    print()

    # 步骤4: 检查端口
    print_step(4, 5, "检查端口占用...")
    port = 8877
    if check_port(port):
        print(f"⚠️  端口 {port} 已被占用")
        response = input("是否终止旧进程并重启？(y/n): ").strip().lower()
        if response == 'y':
            print("正在终止旧进程...")
            # 尝试终止旧进程
            try:
                if sys.platform == "win32":
                    subprocess.run(f"taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Dashboard*\"", shell=True)
                else:
                    subprocess.run(f"lsof -ti:{port} | xargs kill -9", shell=True)
                time.sleep(2)
                print("✅ 旧进程已终止")
            except Exception as e:
                print(f"⚠️  终止进程时出错: {e}")
        else:
            print("❌ 取消启动")
            sys.exit(0)
    else:
        print(f"✅ 端口 {port} 可用")
    print()

    # 步骤5: 启动Dashboard
    print_step(5, 5, "启动Dashboard...")
    dashboard_dir = project_root / "apps" / "dashboard"

    print("-" * 70)
    print(f"📍 工作目录: {dashboard_dir}")
    print(f"🌐 访问地址: http://127.0.0.1:{port}")
    print(f"📊 功能模块: 架构师监控 | 全栈工程师 | 功能清单 | Token管理")
    print("-" * 70)
    print("\n💡 提示:")
    print("   - 按 Ctrl+C 停止服务")
    print("   - Dashboard会自动在浏览器中打开")
    print("   - 数据每5-20秒自动刷新")
    print()
    print("=" * 70)
    print()

    # 启动Dashboard
    try:
        # 切换到dashboard目录
        os.chdir(dashboard_dir)

        print("正在启动Dashboard服务...")
        print()

        # 等待2秒后打开浏览器
        def open_browser():
            time.sleep(2)
            url = f"http://127.0.0.1:{port}"
            print(f"\n🌐 正在打开浏览器: {url}\n")
            webbrowser.open(url)

        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # 启动Dashboard（阻塞模式）
        subprocess.run([sys.executable, "start_dashboard.py", "--port", str(port)])

    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard 已停止")
        print("感谢使用任务所·Flow v1.7！")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("\n请检查错误信息或手动启动:")
        print(f"  cd {dashboard_dir}")
        print(f"  python3 start_dashboard.py --port {port}")
        sys.exit(1)

if __name__ == "__main__":
    main()
