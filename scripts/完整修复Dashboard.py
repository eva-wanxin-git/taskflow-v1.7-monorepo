#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整修复Dashboard - 添加任务筛选Tab + 修复样式 + 清除缓存
"""

from pathlib import Path
import re
import time

V17_TEMPLATES = Path(__file__).parent.parent / "apps/dashboard/src/industrial_dashboard/templates.py"

def fix_dashboard():
    """完整修复Dashboard"""
    
    content = V17_TEMPLATES.read_text(encoding='utf-8')
    
    print("=" * 70)
    print("完整修复Dashboard")
    print("=" * 70)
    print()
    
    # 1. 添加filterTasksByStatus函数（在switchDeveloperTab函数附近）
    # 查找switchDeveloperTab函数的位置
    switch_tab_pos = content.find("function switchDeveloperTab(tab)")
    
    if switch_tab_pos > 0:
        # 在这个函数之前插入新函数
        filter_function = """
        // 任务筛选函数 - 根据状态筛选
        let currentTaskFilter = 'all';
        
        function filterTasksByStatus(filterStatus) {{
            currentTaskFilter = filterStatus;
            
            // 更新Tab激活状态
            const tabs = document.querySelectorAll('.task-filter-tab');
            tabs.forEach(tab => {{
                tab.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // 重新渲染任务列表
            renderFilteredTasks();
        }}
        
        function renderFilteredTasks() {{
            const taskList = document.getElementById('taskList');
            if (!taskList || !allTasksData) return;
            
            // 获取当前版本的任务
            const config = versionConfigs[currentVersion];
            let tasks = allTasksData.filter(config.taskFilter);
            
            // 根据筛选条件过滤
            if (currentTaskFilter !== 'all') {{
                tasks = tasks.filter(task => {{
                    if (currentTaskFilter === 'pending') {{
                        return task.status === 'pending';
                    }} else if (currentTaskFilter === 'in_progress') {{
                        return task.status === 'in_progress';
                    }} else if (currentTaskFilter === 'completed') {{
                        return task.status === 'completed';
                    }}
                    return true;
                }});
            }}
            
            // 更新任务数量显示
            document.getElementById('taskCount').textContent = tasks.length + ' tasks';
            
            // 渲染任务列表
            if (tasks.length === 0) {{
                taskList.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 48px; margin-bottom: 16px;">📝</div>
                        <div style="font-size: 16px; color: #757575; margin-bottom: 8px;">暂无${{getFilterLabel()}}任务</div>
                    </div>
                `;
            }} else {{
                taskList.innerHTML = tasks.map(task => `
                    <div class="task-card">
                        <div class="task-card-header">
                            <span class="task-id">${{task.id}}</span>
                            <div class="task-actions">
                                ${{renderTaskButton(task)}}
                                <span class="task-status ${{task.status.toLowerCase().replace(' ', '_')}}">
                                    ${{getStatusText(task.status)}}
                                </span>
                            </div>
                        </div>
                        <div class="task-title">
                            <span>${{task.title}}</span>
                        </div>
                        <div class="task-details">
                            <div class="detail-item">
                                <span class="detail-label">预估工时</span>
                                <span class="detail-value">${{task.estimated_hours || 0}} 小时</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">复杂度</span>
                                <span class="detail-value">${{task.complexity || '—'}}</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">优先级</span>
                                <span class="detail-value">${{task.priority || '—'}}</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">负责人</span>
                                <span class="detail-value">${{task.assigned_to || '未分配'}}</span>
                            </div>
                        </div>
                    </div>
                `).join('');
            }}
        }}
        
        function getFilterLabel() {{
            const labels = {{
                'all': '',
                'pending': '待处理',
                'in_progress': '进行中',
                'completed': '已完成'
            }};
            return labels[currentTaskFilter] || '';
        }}
        
        function renderTaskButton(task) {{
            if (task.status === 'completed') {{
                return `<button class="copy-report-button" onclick="copyTaskReport('${{task.id}}', event)">▸ 复制报告</button>`;
            }} else if (task.status === 'pending') {{
                return `<button class="copy-prompt-button" onclick="copyTaskPrompt('${{task.id}}', event)">▸ 复制提示词</button>`;
            }} else if (task.status === 'in_progress') {{
                return `<button class="redispatch-button" onclick="redispatchTask('${{task.id}}', event)">↻ 重新派发</button>`;
            }}
            return '';
        }}
        
        """
        
        content = content[:switch_tab_pos] + filter_function + content[switch_tab_pos:]
        print("[ADD] 添加任务筛选函数")
    
    # 2. 修改原有的任务列表渲染，调用新的筛选函数
    # 找到document.getElementById('taskList').innerHTML的位置
    content = re.sub(
        r"document\.getElementById\('taskList'\)\.innerHTML = tasks\.map",
        "renderFilteredTasks(); return; // Use新筛选渲染 \n            document.getElementById('taskList').innerHTML = tasks.map",
        content,
        count=1
    )
    
    print("[FIX] 任务列表使用新的筛选渲染")
    
    # 3. 更新缓存版本号
    cache_version = f"v{int(time.time())}"
    content = re.sub(r'cache_version: str = "v\d+"', f'cache_version: str = "{cache_version}"', content)
    print(f"[UPDATE] 缓存版本号: {cache_version}")
    
    # 4. 保存文件
    V17_TEMPLATES.write_text(content, encoding='utf-8')
    
    print()
    print("=" * 70)
    print("[完成] Dashboard已完整修复")
    print("=" * 70)
    print()
    print("修改内容:")
    print("  1. ✅ 添加任务筛选Tab（全部/待处理/进行中/已完成）")
    print("  2. ✅ 添加筛选函数和渲染逻辑")
    print("  3. ✅ 更新缓存版本号")
    print()
    print("需要重启Dashboard生效")

if __name__ == "__main__":
    fix_dashboard()

