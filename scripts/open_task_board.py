#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打开任务看板（工业美学版 - 继承v1.6样式）

功能：
1. 为当前项目分配/获取端口
2. 生成精美HTML版本的任务看板（黑白红工业美学）
3. 自动在浏览器中打开
"""

import sys
import io
from pathlib import Path
import webbrowser
import re
from datetime import datetime

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加packages到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "packages" / "shared-utils"))

from port_manager import PortManager


def parse_markdown_task_board(md_content: str) -> dict:
    """解析Markdown任务板"""
    data = {
        "title": "任务看板",
        "project_code": "TASKFLOW",
        "port": 8870,
        "stats": {},
        "phases": [],
        "tasks": []
    }
    
    # 提取项目代码和端口
    if match := re.search(r'\*\*项目代码\*\*:\s*(\w+)', md_content):
        data["project_code"] = match.group(1)
    
    if match := re.search(r'\*\*Dashboard端口\*\*:\s*(\d+)', md_content):
        data["port"] = int(match.group(1))
    
    # 提取统计数据
    if match := re.search(r'总任务\*\*:\s*(\d+)', md_content):
        data["stats"]["total"] = int(match.group(1))
    if match := re.search(r'已完成\*\*:\s*(\d+)', md_content):
        data["stats"]["completed"] = int(match.group(1))
    if match := re.search(r'待处理\*\*:\s*(\d+)', md_content):
        data["stats"]["pending"] = int(match.group(1))
    
    return data


def generate_task_board_html(project_code: str, port: int) -> str:
    """生成工业美学风格的任务看板HTML（继承v1.6样式）"""
    
    # 读取任务板内容
    task_board_md = PROJECT_ROOT / "docs" / "tasks" / "task-board.md"
    if task_board_md.exists():
        md_content = task_board_md.read_text(encoding='utf-8')
        data = parse_markdown_task_board(md_content)
    else:
        data = {
            "project_code": project_code,
            "port": port,
            "stats": {"total": 18, "completed": 8, "pending": 10},
            "tasks": []
        }
    
    # 统计数据
    total = data["stats"].get("total", 18)
    completed = data["stats"].get("completed", 8)
    pending = data["stats"].get("pending", 10)
    progress = int((completed / total * 100)) if total > 0 else 0
    
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>任务看板 - {project_code}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --black: #000000;
            --white: #FFFFFF;
            --red: #D32F2F;
            --gray-900: #212121;
            --gray-700: #616161;
            --gray-500: #9E9E9E;
            --gray-300: #E0E0E0;
            --gray-100: #F5F5F5;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
            background: var(--white);
            color: var(--black);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 60px;
        }}
        
        /* 头部 */
        .header {{
            border-bottom: 2px solid var(--black);
            padding-bottom: 32px;
            margin-bottom: 48px;
        }}
        
        .brand {{
            font-size: 40px;
            font-weight: 700;
            color: var(--black);
            margin-bottom: 8px;
        }}
        
        .subtitle {{
            font-size: 14px;
            color: var(--gray-700);
            letter-spacing: 0.5px;
        }}
        
        .project-info {{
            display: flex;
            gap: 24px;
            margin-top: 16px;
            font-size: 13px;
            color: var(--gray-500);
        }}
        
        .project-info-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* 端口信息卡片 */
        .port-card {{
            background: var(--gray-100);
            border-left: 4px solid var(--red);
            padding: 24px;
            margin-bottom: 48px;
        }}
        
        .port-title {{
            font-size: 13px;
            font-weight: 700;
            color: var(--black);
            margin-bottom: 12px;
        }}
        
        .port-content {{
            font-size: 13px;
            color: var(--gray-700);
            line-height: 2;
        }}
        
        .port-link {{
            color: var(--red);
            text-decoration: none;
            font-weight: 600;
        }}
        
        .port-link:hover {{
            text-decoration: underline;
        }}
        
        /* 统计卡片 */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
            margin-bottom: 48px;
        }}
        
        .stat-card {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            padding: 32px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 56px;
            font-weight: 700;
            color: var(--black);
            font-family: 'SF Mono', 'Consolas', monospace;
            margin-bottom: 12px;
        }}
        
        .stat-label {{
            font-size: 13px;
            color: var(--gray-700);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* 进度条 */
        .progress-section {{
            margin-bottom: 48px;
        }}
        
        .progress-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 16px;
        }}
        
        .progress-label {{
            font-size: 13px;
            font-weight: 700;
            color: var(--black);
        }}
        
        .progress-percent {{
            font-size: 13px;
            font-weight: 700;
            color: var(--red);
        }}
        
        .progress-bar {{
            width: 100%;
            height: 4px;
            background: var(--gray-300);
            position: relative;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: var(--red);
            transition: width 0.3s ease;
        }}
        
        /* 区域标题 */
        .section {{
            margin-bottom: 48px;
        }}
        
        .section-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--black);
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        /* Phase卡片 */
        .phase-card {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            margin-bottom: 24px;
        }}
        
        .phase-header {{
            padding: 24px;
            border-bottom: 1px solid var(--gray-300);
            background: var(--gray-100);
        }}
        
        .phase-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--black);
        }}
        
        .phase-status {{
            display: inline-block;
            margin-left: 12px;
            padding: 4px 12px;
            font-size: 11px;
            border-radius: 2px;
        }}
        
        .phase-status.completed {{
            background: var(--black);
            color: var(--white);
        }}
        
        .phase-status.pending {{
            background: var(--gray-300);
            color: var(--gray-700);
        }}
        
        .phase-content {{
            padding: 24px;
        }}
        
        .phase-tasks {{
            font-size: 13px;
            color: var(--gray-700);
            line-height: 2;
        }}
        
        /* 刷新提示 */
        .refresh-notice {{
            position: fixed;
            bottom: 32px;
            right: 32px;
            background: var(--black);
            color: var(--white);
            padding: 16px 24px;
            font-size: 12px;
            border: 1px solid var(--gray-300);
            letter-spacing: 0.5px;
        }}
        
        /* 打印样式 */
        @media print {{
            .refresh-notice {{ display: none; }}
            body {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <div class="brand">任务所·FLOW</div>
            <div class="subtitle">用对话，开工；用流程，收工 | AI任务协作与进度监控系统</div>
            <div class="project-info">
                <div class="project-info-item">
                    <span>📦</span>
                    <span>项目: {project_code}</span>
                </div>
                <div class="project-info-item">
                    <span>🔌</span>
                    <span>端口: {port}</span>
                </div>
                <div class="project-info-item">
                    <span>⏰</span>
                    <span>更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
                </div>
            </div>
        </div>
        
        <!-- 端口信息 -->
        <div class="port-card">
            <div class="port-title">📍 端口信息</div>
            <div class="port-content">
                <strong>Dashboard端口</strong>: {port}（自动分配，避免冲突）<br>
                <strong>访问地址</strong>: <a href="http://localhost:{port}" class="port-link" target="_blank">http://localhost:{port}</a><br>
                <strong>端口范围</strong>: 8870-8899（任务所·Flow专用）<br>
                <strong>端口管理</strong>: 通过PortManager自动分配
            </div>
        </div>
        
        <!-- 统计卡片 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total}</div>
                <div class="stat-label">总任务数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{pending}</div>
                <div class="stat-label">待处理</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">进行中</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{completed}</div>
                <div class="stat-label">已完成</div>
            </div>
        </div>
        
        <!-- 进度条 -->
        <div class="progress-section">
            <div class="progress-header">
                <div class="progress-label">整体进度</div>
                <div class="progress-percent">{progress}%</div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
        </div>
        
        <!-- Phase状态 -->
        <div class="section">
            <div class="section-title">里程碑状态</div>
            
            <div class="phase-card">
                <div class="phase-header">
                    <span class="phase-title">Phase 1-2: Monorepo骨架 + 知识库数据库</span>
                    <span class="phase-status completed">✓ 已完成</span>
                </div>
                <div class="phase-content">
                    <div class="phase-tasks">
                        ✓ 创建Monorepo目录结构（50+目录）<br>
                        ✓ 编写ADR-0001架构决策<br>
                        ✓ 创建12表知识库Schema<br>
                        ✓ 数据库初始化（1项目+5组件+5工具）
                    </div>
                </div>
            </div>
            
            <div class="phase-card">
                <div class="phase-header">
                    <span class="phase-title">Phase A-B: AI Prompts系统</span>
                    <span class="phase-status completed">✓ 已完成</span>
                </div>
                <div class="phase-content">
                    <div class="phase-tasks">
                        ✓ 4套AI System Prompts（25000字）<br>
                        ✓ ArchitectOrchestrator服务（400行）<br>
                        ✓ 6个API端点定义<br>
                        ✓ 完整的协作指南
                    </div>
                </div>
            </div>
            
            <div class="phase-card">
                <div class="phase-header">
                    <span class="phase-title">Phase C: API集成</span>
                    <span class="phase-status pending">⏳ 待开始</span>
                </div>
                <div class="phase-content">
                    <div class="phase-tasks">
                        ☐ TASK-C.1: 创建FastAPI主应用（2h）<br>
                        ☐ TASK-C.2: 集成数据库（3h）<br>
                        ☐ TASK-C.3: 端到端测试（1.5h）
                    </div>
                </div>
            </div>
            
            <div class="phase-card">
                <div class="phase-header">
                    <span class="phase-title">Phase D-E: 代码迁移 + 测试</span>
                    <span class="phase-status pending">⏳ 可延后</span>
                </div>
                <div class="phase-content">
                    <div class="phase-tasks">
                        ☐ 迁移models到core-domain（2h）<br>
                        ☐ 迁移state_manager到infra（3h）<br>
                        ☐ 完整功能测试（2h）<br>
                        <span style="color: var(--gray-500);">（架构师建议：可延后到Phase C后）</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 下一步行动 -->
        <div class="section">
            <div class="section-title">🎯 下一步行动（Day 2）</div>
            <div class="port-card" style="border-left-color: #FF9800;">
                <div class="port-title">立即开始：Phase C - API集成</div>
                <div class="port-content">
                    <strong>优先级</strong>: 🔴 P0（Critical）<br>
                    <strong>预估时间</strong>: 6.5小时<br>
                    <strong>核心价值</strong>: 让架构师API真正可用<br>
                    <br>
                    <strong>具体任务</strong>:<br>
                    1. TASK-C.1: 创建main.py（2h）<br>
                    2. TASK-C.2: 集成数据库（3h）<br>
                    3. TASK-C.3: E2E测试（1.5h）<br>
                    <br>
                    <strong>建议执行者</strong>: 全栈工程师·李明<br>
                    <br>
                    <a href="docs/tasks/task-board.md" class="port-link">📋 查看完整任务详情</a>
                </div>
            </div>
        </div>
        
        <!-- 快速链接 -->
        <div class="section">
            <div class="section-title">🔗 快速链接</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
                <a href="docs/arch/architecture-inventory.md" style="display: block; padding: 16px; border: 1px solid var(--gray-300); text-decoration: none; color: var(--black);">
                    📐 架构清单
                </a>
                <a href="docs/arch/architect-workflow.md" style="display: block; padding: 16px; border: 1px solid var(--gray-300); text-decoration: none; color: var(--black);">
                    🔄 工作流程
                </a>
                <a href="docs/ai/" style="display: block; padding: 16px; border: 1px solid var(--gray-300); text-decoration: none; color: var(--black);">
                    🤖 AI Prompts
                </a>
            </div>
        </div>
    </div>
    
    <!-- 刷新提示 -->
    <div class="refresh-notice">
        每30秒自动刷新 | {datetime.now().strftime('%H:%M:%S')}
    </div>
    
    <script>
        // 30秒自动刷新
        setTimeout(function() {{
            location.reload();
        }}, 30000);
        
        console.log('任务看板加载完成');
        console.log('项目: {project_code}');
        console.log('端口: {port}');
    </script>
</body>
</html>
    """
    
    return html


def main():
    print("\n" + "="*70)
    print("任务所·Flow - 任务看板查看器（工业美学版）")
    print("="*70 + "\n")
    
    # 1. 确定项目代码
    project_code = "TASKFLOW"
    print(f"[1/4] 项目代码: {project_code}")
    
    # 2. 分配/获取端口
    manager = PortManager()
    port = manager.allocate_port_for_project(project_code)
    print(f"[2/4] 分配端口: {port}")
    
    # 3. 生成HTML（工业美学风格）
    html_content = generate_task_board_html(project_code, port)
    html_file = PROJECT_ROOT / "task-board.html"
    html_file.write_text(html_content, encoding='utf-8')
    print(f"[3/4] 生成HTML: {html_file.name}（工业美学风格）")
    
    # 4. 在浏览器中打开
    print(f"[4/4] 在浏览器中打开...")
    webbrowser.open(f"file:///{html_file.absolute()}")
    
    print("\n" + "="*70)
    print(f"✅ 任务看板已在浏览器中打开！")
    print(f"📍 项目: {project_code}")
    print(f"📍 端口: {port}")
    print(f"📍 样式: 工业美学（黑白红配色）")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
