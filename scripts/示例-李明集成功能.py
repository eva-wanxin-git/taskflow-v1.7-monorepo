#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例脚本: 李明集成功能

展示如何在集成功能时触发事件
"""
import sys
import io
from pathlib import Path

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加packages路径
sys.path.insert(0, str(Path(__file__).parent.parent / "packages"))

from shared_utils.event_helper import create_event_helper

def integrate_feature(
    feature_id: str,
    component: str,
    description: str = None,
    version: str = None
):
    """
    集成功能并触发事件
    
    Args:
        feature_id: 功能ID
        component: 集成的组件
        description: 描述
        version: 版本号
    """
    # 1. 创建EventHelper实例
    event_helper = create_event_helper(
        project_id="TASKFLOW",
        actor="李明（全栈工程师）",
        source="ai"
    )
    
    try:
        print(f"功能: {feature_id}")
        print(f"集成到组件: {component}")
        if version:
            print(f"版本: {version}")
        
        # 2. 执行集成操作（这里是模拟，实际项目中可能是Git merge、部署等）
        print(f"\n执行集成操作...")
        print(f"  - 合并代码到 {component}")
        print(f"  - 运行集成测试")
        print(f"  - 更新版本号")
        print(f"✓ 集成完成")
        
        # 3. 触发 feature_integrated 事件
        event = event_helper.feature_integrated(
            feature_id=feature_id,
            component=component,
            description=description or f"功能 {feature_id} 已集成到 {component}",
            version=version
        )
        print(f"✓ 事件已触发: feature.integrated (ID: {event['id'][:8]}...)")
        
        return True
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("===== 示例: 李明集成功能 =====\n")
    
    # 功能集成示例数据
    if len(sys.argv) > 2:
        feature_id = sys.argv[1]
        component = sys.argv[2]
        version = sys.argv[3] if len(sys.argv) > 3 else "v1.7.0"
    else:
        feature_id = "REQ-010"
        component = "api"
        version = "v1.7.0"
    
    print(f"集成功能: {feature_id} → {component}\n")
    
    success = integrate_feature(
        feature_id=feature_id,
        component=component,
        description=f"事件流系统已成功集成到{component}模块，提供完整的事件发射和查询功能",
        version=version
    )
    
    if success:
        print("\n✅ 功能集成完成，事件已触发！")
        print("\n可以通过以下API查询事件:")
        print(f"  GET /api/events?related_entity_type=feature&related_entity_id={feature_id}")
        print(f"  GET /api/events?event_type=feature.integrated")
        print(f"  GET /api/events?category=general")
    else:
        print("\n✗ 功能集成失败")


if __name__ == "__main__":
    main()

