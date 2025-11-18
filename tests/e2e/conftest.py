# -*- coding: utf-8 -*-
"""
pytest配置文件（E2E测试）

提供共享的fixtures和测试配置
"""

import pytest
import sys
from pathlib import Path


# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "apps" / "api" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "packages"))


def pytest_configure(config):
    """pytest配置钩子"""
    # 注册自定义标记
    config.addinivalue_line(
        "markers",
        "e2e: 标记为端到端测试"
    )
    config.addinivalue_line(
        "markers",
        "slow: 标记为慢速测试"
    )
    config.addinivalue_line(
        "markers",
        "integration: 标记为集成测试"
    )


@pytest.fixture(scope="session", autouse=True)
def test_environment():
    """设置测试环境"""
    print("\n" + "="*70)
    print("初始化测试环境...")
    print(f"项目根目录: {PROJECT_ROOT}")
    print("="*70)
    
    yield
    
    print("\n" + "="*70)
    print("清理测试环境...")
    print("="*70)

