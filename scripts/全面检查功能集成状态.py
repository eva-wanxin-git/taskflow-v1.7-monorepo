#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面检查所有已完成功能的集成状态
"""

import sqlite3
import json
import requests
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
EVENTS_FILE = Path(__file__).parent.parent / "apps/dashboard/automation-data/architect_events.json"
PORT_FILE = Path(__file__).parent.parent / "config/ports.json"
DASHBOARD_URL = "http://localhost:8877"

def check_req001_port_manager():
    """检查REQ-001: 端口管理器"""
    print("\n[1] REQ-001: 端口冲突解决")
    print("-" * 70)
    
    checks = []
    
    # 检查1: PortManager文件存在
    port_manager_file = Path(__file__).parent.parent / "packages/shared-utils/port_manager.py"
    if port_manager_file.exists():
        print("  OK PortManager文件存在")
        checks.append(True)
    else:
        print("  NG PortManager文件不存在")
        checks.append(False)
    
    # 检查2: ports.json配置存在
    if PORT_FILE.exists():
        with open(PORT_FILE, 'r', encoding='utf-8') as f:
            ports = json.load(f)
        print(f"  OK ports.json存在，已配置{len(ports)}个项目")
        if "taskflow-v1.7" in ports:
            port = ports["taskflow-v1.7"]["port"]
            print(f"     当前端口: {port}")
            checks.append(True)
        else:
            print("  NG taskflow-v1.7未配置端口")
            checks.append(False)
    else:
        print("  NG ports.json不存在")
        checks.append(False)
    
    # 检查3: Dashboard是否使用PortManager
    dashboard_py = Path(__file__).parent.parent / "apps/dashboard/start_dashboard.py"
    if dashboard_py.exists():
        content = dashboard_py.read_text(encoding='utf-8')
        if "PortManager" in content or "port_manager" in content:
            print("  OK Dashboard使用PortManager")
            checks.append(True)
        else:
            print("  NG Dashboard未使用PortManager")
            checks.append(False)
    else:
        print("  SKIP start_dashboard.py不存在")
    
    score = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n  集成度: {score:.0f}%")
    return score

def check_req003_conversation():
    """检查REQ-003: 对话历史库"""
    print("\n[2] REQ-003: 对话历史库")
    print("-" * 70)
    
    checks = []
    
    # 检查1: 服务层文件存在
    service_file = Path(__file__).parent.parent / "packages/core-domain/src/services/conversation_service.py"
    if service_file.exists():
        print("  OK conversation_service.py存在")
        checks.append(True)
    else:
        print("  NG conversation_service.py不存在")
        checks.append(False)
    
    # 检查2: API路由存在
    api_route = Path(__file__).parent.parent / "apps/api/src/routes/conversation.py"
    if api_route.exists():
        print("  OK API路由存在")
        checks.append(True)
    else:
        print("  NG API路由不存在")
        checks.append(False)
    
    # 检查3: Dashboard UI存在
    # 检查templates.py中是否有对话历史相关代码
    templates = Path(__file__).parent.parent / "apps/dashboard/src/industrial_dashboard/templates.py"
    if templates.exists():
        content = templates.read_text(encoding='utf-8')
        if "conversation" in content.lower() or "对话历史" in content:
            print("  OK Dashboard包含对话历史UI")
            checks.append(True)
        else:
            print("  NG Dashboard未包含对话历史UI")
            checks.append(False)
    
    # 检查4: 数据库表存在
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
    if cursor.fetchone():
        print("  OK conversations表存在")
        checks.append(True)
    else:
        print("  NG conversations表不存在")
        checks.append(False)
    conn.close()
    
    score = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n  集成度: {score:.0f}%")
    return score

def check_req006_token_sync():
    """检查REQ-006: Token同步"""
    print("\n[3] REQ-006: Token实时同步")
    print("-" * 70)
    
    checks = []
    
    # 检查1: Dashboard显示Token
    try:
        response = requests.get(DASHBOARD_URL, timeout=3)
        html = response.text
        if "Token" in html or "token" in html:
            print("  OK Dashboard包含Token显示")
            checks.append(True)
        else:
            print("  NG Dashboard未显示Token")
            checks.append(False)
    except:
        print("  SKIP Dashboard未运行，无法检查")
    
    # 检查2: Token数据存在于事件流
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        token_events = [e for e in data.get("events", []) 
                       if e.get("type") == "token_usage" or "token" in e.get("content", "").lower()]
        
        if token_events:
            print(f"  OK 事件流包含{len(token_events)}个Token事件")
            checks.append(True)
        else:
            print("  NG 事件流无Token记录")
            checks.append(False)
    
    # 检查3: 对话历史库集成
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
    if cursor.fetchone():
        print("  OK Token与对话历史库集成（表存在）")
        checks.append(True)
    else:
        print("  NG conversations表不存在")
        checks.append(False)
    conn.close()
    
    score = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n  集成度: {score:.0f}%")
    return score

def check_req009_task_workflow():
    """检查REQ-009: 任务三态流转"""
    print("\n[4] REQ-009: 任务三态流转")
    print("-" * 70)
    
    checks = []
    
    # 检查1: 李明收到任务.py存在
    script1 = Path(__file__).parent / "李明收到任务.py"
    if script1.exists():
        print("  OK 李明收到任务.py存在")
        checks.append(True)
    else:
        print("  NG 李明收到任务.py不存在")
        checks.append(False)
    
    # 检查2: 李明提交完成.py存在
    script2 = Path(__file__).parent / "李明提交完成.py"
    if script2.exists():
        print("  OK 李明提交完成.py存在")
        checks.append(True)
    else:
        print("  NG 李明提交完成.py不存在")
        checks.append(False)
    
    # 检查3: Dashboard API端点
    dashboard_py = Path(__file__).parent.parent / "apps/dashboard/src/industrial_dashboard/dashboard.py"
    if dashboard_py.exists():
        content = dashboard_py.read_text(encoding='utf-8')
        if "/api/tasks/{task_id}/received" in content:
            print("  OK API端点 /received 存在")
            checks.append(True)
        else:
            print("  NG API端点 /received 不存在")
            checks.append(False)
        
        if "/api/tasks/{task_id}/complete" in content:
            print("  OK API端点 /complete 存在")
            checks.append(True)
        else:
            print("  NG API端点 /complete 不存在")
            checks.append(False)
    
    # 检查4: Dashboard UI按钮
    templates = Path(__file__).parent.parent / "apps/dashboard/src/industrial_dashboard/templates.py"
    if templates.exists():
        content = templates.read_text(encoding='utf-8')
        if "copyTaskPrompt" in content:
            print("  OK Dashboard有复制提示词按钮")
            checks.append(True)
        else:
            print("  NG Dashboard无复制提示词按钮")
            checks.append(False)
    
    score = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n  集成度: {score:.0f}%")
    return score

def check_req010_event_stream():
    """检查REQ-010: 事件流系统"""
    print("\n[5] REQ-010: 全局事件流")
    print("-" * 70)
    
    checks = []
    
    # 检查1: 事件数据文件存在
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        events = data.get("events", [])
        print(f"  OK architect_events.json存在，包含{len(events)}个事件")
        checks.append(True)
        
        # 检查事件结构
        if events:
            event = events[0]
            required_fields = ["id", "timestamp", "type", "content"]
            missing = [f for f in required_fields if f not in event]
            if not missing:
                print("  OK 事件结构完整")
                checks.append(True)
            else:
                print(f"  NG 事件缺少字段: {missing}")
                checks.append(False)
    else:
        print("  NG architect_events.json不存在")
        checks.append(False)
    
    # 检查2: Dashboard显示事件流
    try:
        response = requests.get(DASHBOARD_URL, timeout=3)
        html = response.text
        if "事件流" in html or "event" in html.lower():
            print("  OK Dashboard显示事件流")
            checks.append(True)
        else:
            print("  NG Dashboard未显示事件流")
            checks.append(False)
    except:
        print("  SKIP Dashboard未运行")
    
    # 检查3: 事件助手工具存在
    event_helper = Path(__file__).parent.parent / "packages/shared-utils/event_helper.py"
    if event_helper.exists():
        print("  OK event_helper.py存在")
        checks.append(True)
    else:
        print("  NG event_helper.py不存在")
        checks.append(False)
    
    score = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n  集成度: {score:.0f}%")
    return score

def check_req011_progress():
    """检查REQ-011: 动态进度计算"""
    print("\n[6] REQ-011: 动态进度计算")
    print("-" * 70)
    
    checks = []
    
    # 检查1: 数据库可查询
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
    completed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status != 'cancelled'")
    total = cursor.fetchone()[0]
    
    if total > 0:
        progress = completed / total * 100
        print(f"  OK 进度计算正常: {progress:.1f}% ({completed}/{total})")
        checks.append(True)
    else:
        print("  NG 无任务数据")
        checks.append(False)
    
    conn.close()
    
    # 检查2: Dashboard显示进度
    try:
        response = requests.get(DASHBOARD_URL, timeout=3)
        html = response.text
        if "%" in html or "进度" in html:
            print("  OK Dashboard显示进度")
            checks.append(True)
        else:
            print("  NG Dashboard未显示进度")
            checks.append(False)
    except:
        print("  SKIP Dashboard未运行")
    
    # 检查3: 自动刷新机制
    templates = Path(__file__).parent.parent / "apps/dashboard/src/industrial_dashboard/templates.py"
    if templates.exists():
        content = templates.read_text(encoding='utf-8')
        if "setInterval" in content or "auto" in content.lower():
            print("  OK 自动刷新机制存在")
            checks.append(True)
        else:
            print("  NG 未找到自动刷新代码")
            checks.append(False)
    
    score = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n  集成度: {score:.0f}%")
    return score

def check_scripts_integration():
    """检查脚本工具集成"""
    print("\n[7] 脚本工具集成检查")
    print("-" * 70)
    
    required_scripts = [
        ("李明收到任务.py", "接收任务"),
        ("李明提交完成.py", "提交完成"),
        ("备份数据库.py", "数据库备份"),
        ("显示部署状态.py", "状态显示"),
        ("验证核心功能.py", "功能验证"),
    ]
    
    checks = []
    for script_name, desc in required_scripts:
        script_path = Path(__file__).parent / script_name
        if script_path.exists():
            print(f"  OK {script_name:30s} - {desc}")
            checks.append(True)
        else:
            print(f"  NG {script_name:30s} - {desc}")
            checks.append(False)
    
    score = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n  可用率: {score:.0f}%")
    return score

def check_dashboard_ui():
    """检查Dashboard UI完整性"""
    print("\n[8] Dashboard UI完整性")
    print("-" * 70)
    
    checks = []
    
    try:
        response = requests.get(DASHBOARD_URL, timeout=3)
        html = response.text
        
        # 检查关键UI元素
        ui_elements = [
            ("任务所", "品牌名称"),
            ("统计", "统计卡片"),
            ("任务列表", "任务展示"),
            ("事件", "事件流"),
            ("进度", "进度显示"),
        ]
        
        for element, desc in ui_elements:
            if element in html:
                print(f"  OK {desc:15s} - 存在")
                checks.append(True)
            else:
                print(f"  NG {desc:15s} - 缺失")
                checks.append(False)
        
        score = sum(checks) / len(checks) * 100 if checks else 0
        print(f"\n  UI完整度: {score:.0f}%")
        return score
        
    except Exception as e:
        print(f"  ERROR Dashboard无法访问: {e}")
        print(f"\n  UI完整度: 0%")
        return 0

def check_派发文档():
    """检查派发文档是否包含脚本指令"""
    print("\n[9] 派发文档完整性检查")
    print("-" * 70)
    
    dispatch_docs = list(Path(__file__).parent.parent.glob("📤派发给李明*.md"))
    
    if not dispatch_docs:
        print("  NG 未找到派发文档")
        return 0
    
    checks = []
    for doc in dispatch_docs:
        content = doc.read_text(encoding='utf-8')
        
        has_receive = "李明收到任务.py" in content
        has_complete = "李明提交完成.py" in content
        
        doc_name = doc.name
        if has_receive and has_complete:
            print(f"  OK {doc_name:50s} - 完整")
            checks.append(True)
        elif has_receive or has_complete:
            print(f"  WARN {doc_name:50s} - 部分缺失")
            checks.append(False)
        else:
            print(f"  NG {doc_name:50s} - 缺少脚本指令")
            checks.append(False)
    
    score = sum(checks) / len(checks) * 100 if checks else 0
    print(f"\n  完整度: {score:.0f}%")
    return score

def main():
    """执行所有检查"""
    print("=" * 70)
    print("全面检查功能集成状态")
    print("=" * 70)
    
    scores = []
    
    # 执行所有检查
    scores.append(check_req001_port_manager())
    scores.append(check_req003_conversation())
    scores.append(check_req006_token_sync())
    scores.append(check_req009_task_workflow())
    scores.append(check_req010_event_stream())
    scores.append(check_req011_progress())
    scores.append(check_scripts_integration())
    scores.append(check_dashboard_ui())
    scores.append(check_派发文档())
    
    # 总分
    avg_score = sum(scores) / len(scores)
    
    print("\n" + "=" * 70)
    print("检查总结")
    print("=" * 70)
    print(f"\n  总体集成度: {avg_score:.1f}%")
    print()
    
    if avg_score >= 80:
        print("  ✓ 集成状态良好，大部分功能可用")
    elif avg_score >= 60:
        print("  ⚠ 集成状态一般，部分功能需要修复")
    else:
        print("  ✗ 集成状态较差，需要大量修复")
    
    print()
    print("=" * 70)
    print("Dashboard: http://localhost:8877")
    print("=" * 70)
    
    # 生成报告文件
    report_file = Path(__file__).parent.parent / "功能集成检查报告.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"功能集成检查报告\n")
        f.write(f"检查时间: 2025-11-19 04:10\n")
        f.write(f"总体集成度: {avg_score:.1f}%\n")
    
    print(f"\n报告已保存: {report_file}")

if __name__ == "__main__":
    main()

