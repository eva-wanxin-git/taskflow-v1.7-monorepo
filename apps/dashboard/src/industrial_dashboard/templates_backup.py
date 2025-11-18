"""
Dashboard HTML 模板

工业美学风格的前端模板
"""


def get_dashboard_html(title: str, subtitle: str) -> str:
    """
    获取 Dashboard HTML
    
    Args:
        title: 标题
        subtitle: 副标题
    
    Returns:
        str: HTML 内容
    """
    return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            /* 纯白底色 + 黑色主题 */
            --color-bg-main: #FFFFFF;           /* 纯白背景 */
            --color-bg-card: #FFFFFF;           /* 纯白卡片 */
            --color-bg-hover: #F5F5F5;          /* 浅灰悬停 */
            --color-text-primary: #000000;      /* 纯黑文字 */
            --color-text-secondary: #424242;    /* 深灰 */
            --color-text-muted: #757575;        /* 中灰 */
            --color-border: #E0E0E0;            /* 灰色边框 */
            --color-border-light: #EEEEEE;      /* 浅灰边框 */
            
            /* 黑色为主的状态色 */
            --color-pending: #000000;           /* 黑色 */
            --color-progress: #000000;          /* 黑色 */
            --color-review: #424242;            /* 深灰 */
            --color-completed: #000000;         /* 黑色 */
            --color-failed: #000000;            /* 黑色 */
            --color-accent: #000000;            /* 黑色强调 */
            
            /* 阴影效果 */
            --shadow-sm: 0 2px 4px 0 rgba(0, 0, 0, 0.08);
            --shadow-md: 0 4px 8px 0 rgba(0, 0, 0, 0.12);
            --shadow-lg: 0 8px 16px 0 rgba(0, 0, 0, 0.15);
            
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --space-xl: 32px;
            
            /* 奢侈品级字体系统 */
            --font-display: 'Helvetica Neue', 'Arial', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-body: 'Helvetica Neue', 'Arial', sans-serif;
            --font-mono: 'SF Mono', 'Monaco', 'Consolas', monospace;
        }}
        
        body {{
            font-family: var(--font-body);
            background: var(--color-bg-main);
            color: var(--color-text-primary);
            line-height: 1.8;
            padding: 40px 60px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 0 0 40px 0;
            margin-bottom: 48px;
            border-bottom: 1px solid #E0E0E0;
            background: transparent;
        }}
        
        .header-left {{
            flex: 1;
        }}
        
        .project-badge {{
            display: inline-block;
            font-size: 10px;
            font-weight: 500;
            color: #9E9E9E;
            font-family: var(--font-body);
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }}
        
        .header-left h1 {{
            font-size: 36px;
            font-weight: 300;
            color: #000000;
            margin-bottom: 12px;
            font-family: var(--font-display);
            letter-spacing: 0px;
            line-height: 1.2;
        }}
        
        .header-left .subtitle {{
            font-size: 13px;
            color: #757575;
            font-family: var(--font-body);
            letter-spacing: 0.5px;
            margin-bottom: 16px;
            font-weight: 400;
        }}
        
        .project-description {{
            font-size: 12px;
            color: #9E9E9E;
            font-family: var(--font-body);
            letter-spacing: 0.3px;
            line-height: 1.8;
            max-width: 600px;
        }}
        
        .status-indicator {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: #000000;
            border-radius: 2px;
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: 500;
            color: white;
            letter-spacing: 1.5px;
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--color-completed);
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 32px;
            margin-bottom: 64px;
        }}
        
        .stat-card {{
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 0;
            padding: 32px 24px;
            transition: all 0.3s;
        }}
        
        .stat-card:hover {{
            border-color: #000000;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
            transform: translateY(-4px);
        }}
        
        .stat-label {{
            font-size: 10px;
            color: #9E9E9E;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 16px;
            font-family: var(--font-body);
            font-weight: 400;
        }}
        
        .stat-value {{
            font-size: 48px;
            font-weight: 300;
            color: #000000;
            font-family: var(--font-display);
            line-height: 1;
            margin-bottom: 12px;
        }}
        
        .stat-meta {{
            font-size: 12px;
            color: #BDBDBD;
            font-family: var(--font-body);
            font-weight: 400;
        }}
        
        .stat-card.pending {{ 
            border-top: 2px solid #000000; 
        }}
        .stat-card.progress {{ 
            border-top: 2px solid #000000; 
        }}
        .stat-card.completed {{ 
            border-top: 2px solid #000000; 
        }}
        .stat-card.review {{ 
            border-top: 2px solid #000000; 
        }}
        
        .progress-section {{
            padding: 32px 0;
            margin-bottom: 64px;
            border-bottom: 1px solid #E0E0E0;
        }}
        
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 24px;
        }}
        
        .section-title {{
            font-size: 11px;
            font-weight: 400;
            color: #9E9E9E;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-family: var(--font-body);
        }}
        
        .progress-value {{
            font-size: 28px;
            font-weight: 300;
            color: #000000;
            font-family: var(--font-display);
        }}
        
        .progress-bar-container {{
            height: 2px;
            background: #F5F5F5;
            border: none;
            border-radius: 0;
            overflow: hidden;
        }}
        
        .progress-bar-fill {{
            height: 100%;
            background: #000000;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* 功能清单 */
        .features-section {{
            padding: 32px 0;
            margin-bottom: 64px;
            border-bottom: 1px solid #E0E0E0;
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 40px;
            margin-top: 32px;
        }}
        
        .feature-group {{
            background: transparent;
            border: none;
            padding: 0;
        }}
        
        .feature-group-title {{
            font-family: var(--font-body);
            font-size: 10px;
            font-weight: 400;
            color: #BDBDBD;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }}
        
        .feature-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 0;
            font-family: var(--font-body);
            font-size: 13px;
            transition: opacity 0.3s;
        }}
        
        .feature-item[data-status="completed"] {{
            color: #000000;
            font-weight: 400;
        }}
        
        .feature-item[data-status="completed"] .feature-checkbox {{
            color: #000000;
        }}
        
        .feature-item[data-status="pending"] {{
            color: #E0E0E0;
            font-weight: 300;
        }}
        
        .feature-item[data-status="pending"] .feature-checkbox {{
            color: #E0E0E0;
        }}
        
        .feature-checkbox {{
            font-size: 14px;
            font-weight: 400;
        }}
        
        .feature-name {{
            flex: 1;
            letter-spacing: 0.3px;
        }}
        
        .tasks-section {{
            padding: 32px 0;
        }}
        
        .task-list {{
            margin-top: var(--space-md);
        }}
        
        /* 任务卡片 - 奢侈品风格 */
        .task-card {{
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 0;
            padding: 32px;
            margin-bottom: 24px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .task-card:hover {{
            border-color: #000000;
            box-shadow: 0 12px 40px rgba(0,0,0,0.06);
            transform: translateY(-2px);
        }}
        
        .task-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .task-id-badge {{
            font-family: var(--font-mono);
            font-size: 11px;
            color: white;
            font-weight: 500;
            background: #000000;
            padding: 6px 12px;
            border-radius: 2px;
            letter-spacing: 1.5px;
        }}
        
        .task-card-title {{
            font-family: var(--font-display);
            font-size: 20px;
            color: #000000;
            font-weight: 300;
            margin-bottom: 16px;
            letter-spacing: 0.5px;
            line-height: 1.4;
        }}
        
        .task-card-feature {{
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 1px solid #F0F0F0;
        }}
        
        .feature-label {{
            font-family: var(--font-body);
            font-size: 11px;
            color: #BDBDBD;
            font-weight: 400;
            letter-spacing: 0.5px;
        }}
        
        .feature-text {{
            font-family: var(--font-body);
            font-size: 13px;
            color: #000000;
            font-weight: 400;
        }}
        
        /* 卡片内表格 - 极简 */
        .task-detail-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-body);
        }}
        
        .task-detail-table td {{
            padding: 10px 16px 10px 0;
            font-size: 12px;
            vertical-align: top;
        }}
        
        .detail-label {{
            color: #BDBDBD;
            font-weight: 400;
            letter-spacing: 0.5px;
            width: 20%;
        }}
        
        .detail-value {{
            color: #000000;
            font-weight: 400;
            width: 30%;
        }}
        
        .task-status-badge {{
            font-family: var(--font-mono);
            font-size: 9px;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }}
        
        .task-status-badge.pending {{
            background: #F5F5F5;
            color: #9E9E9E;
            border: 1px solid #E0E0E0;
        }}
        
        .task-status-badge.in_progress {{
            background: #000000;
            color: white;
            border: 1px solid #000000;
        }}
        
        .task-status-badge.review {{
            background: #757575;
            color: white;
            border: 1px solid #757575;
        }}
        
        .task-status-badge.completed {{
            background: #000000;
            color: white;
            border: 1px solid #000000;
        }}
        
        .task-status-badge.failed {{
            background: #000000;
            color: white;
            border: 1px solid #000000;
        }}
        
        .empty-state {{
            text-align: center;
            padding: var(--space-xl) var(--space-lg);
            color: var(--color-text-muted);
        }}
        
        .update-time {{
            position: fixed;
            bottom: 32px;
            right: 60px;
            font-family: var(--font-mono);
            font-size: 10px;
            color: #BDBDBD;
            font-weight: 400;
            letter-spacing: 1px;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: var(--space-md); }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .header {{
                flex-direction: column;
                align-items: flex-start;
                gap: var(--space-md);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-left">
                <div class="project-badge">项目 PROJECT</div>
                <h1>{title}</h1>
                <div class="subtitle">{subtitle}</div>
                <div class="project-description">
                    融合 Claude Desktop + LibreChat + AWS + MCP 的 AI 操作系统
                </div>
            </div>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>SYSTEM ONLINE</span>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">总任务数 TOTAL</div>
                <div class="stat-value" id="totalTasks">—</div>
                <div class="stat-meta">Total Tasks</div>
            </div>
            <div class="stat-card pending">
                <div class="stat-label">待处理 PENDING</div>
                <div class="stat-value" id="pendingTasks">—</div>
                <div class="stat-meta">Waiting</div>
            </div>
            <div class="stat-card progress">
                <div class="stat-label">进行中 IN PROGRESS</div>
                <div class="stat-value" id="inProgressTasks">—</div>
                <div class="stat-meta">Working</div>
            </div>
            <div class="stat-card completed">
                <div class="stat-label">已完成 COMPLETED</div>
                <div class="stat-value" id="completedTasks">—</div>
                <div class="stat-meta">Finished</div>
            </div>
        </div>
        
        <div class="progress-section">
            <div class="section-header">
                <span class="section-title">整体进度 OVERALL PROGRESS</span>
                <span class="progress-value" id="progressValue">0%</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" id="progressBar" style="width: 0%"></div>
            </div>
        </div>
        
        <!-- 功能实现状态 -->
        <div class="features-section">
            <div class="section-header">
                <span class="section-title">核心功能 KEY FEATURES</span>
                <span class="stat-meta" id="featureCount">0/12 已实现</span>
            </div>
            <div class="features-grid">
                <!-- Phase 1 -->
                <div class="feature-group">
                    <div class="feature-group-title">Phase 1: MVP 基础</div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">Electron 桌面框架</span>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">LibreChat 对话集成</span>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">项目管理系统</span>
                    </div>
                </div>
                
                <!-- Phase 2 -->
                <div class="feature-group">
                    <div class="feature-group-title">Phase 2: AWS & MCP</div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">AWS SSO 认证</span>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">MCP 工具桥接</span>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">本地工具调用</span>
                    </div>
                </div>
                
                <!-- Phase 3 -->
                <div class="feature-group">
                    <div class="feature-group-title">Phase 3: 插件系统</div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">插件加载器</span>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">核心插件集</span>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">插件市场</span>
                    </div>
                </div>
                
                <!-- Phase 4 -->
                <div class="feature-group">
                    <div class="feature-group-title">Phase 4: 高级特性</div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">Artifacts 系统</span>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">任务白板</span>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <span class="feature-name">多窗口管理</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="tasks-section">
            <div class="section-header">
                <span class="section-title">任务列表 TASK LIST</span>
                <span class="stat-meta" id="taskCount">0 tasks</span>
            </div>
            <div class="task-list" id="taskList">
                <div class="empty-state">Loading...</div>
            </div>
        </div>
    </div>
    
    <div class="update-time" id="updateTime">LAST UPDATE: —</div>
    
    <script>
        function getStatusText(status) {{
            const map = {{
                'pending': '待处理',
                'in_progress': '进行中',
                'review': '审查中',
                'completed': '已完成',
                'failed': '失败'
            }};
            return map[status.toLowerCase()] || status.toUpperCase();
        }}
        
        // 获取任务对应的功能
        function getTaskFeatures(taskId) {{
            const featureMap = {{
                'phase1-task1': 'Electron 桌面框架',
                'phase1-task2': 'LibreChat 对话集成',
                'phase1-task3': '项目管理系统',
                'phase1-task4': '快捷键系统',
                'phase2-task1': 'AWS SSO 认证',
                'phase2-task2': 'MCP 工具桥接',
                'phase2-task3': '本地工具调用',
                'phase2-task4': '消息拦截系统',
                'phase3-task1': '插件 API',
                'phase3-task2': '插件加载器',
                'phase3-task3': '核心插件集',
                'phase3-task4': '插件市场',
                'phase4-task1': 'Artifacts 系统',
                'phase4-task2': '任务白板集成',
                'phase4-task3': '多窗口管理',
                'phase4-task4': '性能优化'
            }};
            return featureMap[taskId] || '-';
        }}
        
        async function loadData() {{
            try {{
                const statsRes = await fetch('/api/stats');
                const stats = await statsRes.json();
                
                document.getElementById('totalTasks').textContent = stats.total_tasks;
                document.getElementById('pendingTasks').textContent = stats.pending_tasks;
                document.getElementById('inProgressTasks').textContent = stats.in_progress_tasks;
                document.getElementById('completedTasks').textContent = stats.completed_tasks;
                
                const progress = stats.total_tasks > 0 
                    ? Math.round((stats.completed_tasks / stats.total_tasks) * 100) 
                    : 0;
                document.getElementById('progressValue').textContent = progress + '%';
                document.getElementById('progressBar').style.width = progress + '%';
                
                const tasksRes = await fetch('/api/tasks');
                const tasks = await tasksRes.json();
                
                const taskList = document.getElementById('taskList');
                document.getElementById('taskCount').textContent = tasks.length + ' tasks';
                
                if (tasks.length === 0) {{
                    taskList.innerHTML = '<div class="empty-state">No tasks found</div>';
                }} else {{
                    taskList.innerHTML = tasks.map(task => `
                        <div class="task-card">
                            <div class="task-card-header">
                                <span class="task-id-badge">${{task.id}}</span>
                                <span class="task-status-badge ${{task.status.toLowerCase().replace(' ', '_')}}">
                                    ${{getStatusText(task.status)}}
                                </span>
                            </div>
                            <div class="task-card-title">${{task.title}}</div>
                            <div class="task-card-feature">
                                <span class="feature-label">实现功能:</span>
                                <span class="feature-text">${{getTaskFeatures(task.id)}}</span>
                            </div>
                            <table class="task-detail-table">
                                <tr>
                                    <td class="detail-label">预估工时</td>
                                    <td class="detail-value">${{task.estimated_hours || 0}} 小时</td>
                                    <td class="detail-label">优先级</td>
                                    <td class="detail-value">${{task.priority || '-'}}</td>
                                </tr>
                                <tr>
                                    <td class="detail-label">复杂度</td>
                                    <td class="detail-value">${{task.complexity || '-'}}</td>
                                    <td class="detail-label">负责人</td>
                                    <td class="detail-value">${{task.assigned_to || '未分配'}}</td>
                                </tr>
                                ${{task.status === 'completed' ? `
                                <tr>
                                    <td class="detail-label">代码量</td>
                                    <td class="detail-value">- 行</td>
                                    <td class="detail-label">文件数</td>
                                    <td class="detail-value">- 个</td>
                                </tr>
                                ` : ''}}
                            </table>
                        </div>
                    `).join('');
                }}
                
                const now = new Date();
                const timeStr = now.toLocaleTimeString('zh-CN', {{ hour12: false }});
                document.getElementById('updateTime').textContent = `LAST UPDATE: ${{timeStr}}`;
                
                // 更新功能清单
                updateFeatures(stats);
                
            }} catch (error) {{
                console.error('Load data error:', error);
            }}
        }}
        
        // 更新功能清单状态
        function updateFeatures(stats) {{
            const completedCount = stats.completed_tasks;
            const totalTasks = stats.total_tasks;
            
            // 计算已完成的功能数量
            let completedFeatures = 0;
            const totalFeatures = 12;
            
            // 根据任务完成情况更新功能状态
            // Phase 1: 前4个任务对应前3个功能
            if (completedCount >= 4) {{
                completedFeatures = 3;
                updateFeatureStatus(0, 3, 'completed');
            }}
            
            // Phase 2: 任务5-8对应功能4-6
            if (completedCount >= 8) {{
                completedFeatures = 6;
                updateFeatureStatus(3, 6, 'completed');
            }}
            
            // Phase 3: 任务9-12对应功能7-9
            if (completedCount >= 12) {{
                completedFeatures = 9;
                updateFeatureStatus(6, 9, 'completed');
            }}
            
            // Phase 4: 任务13-16对应功能10-12
            if (completedCount >= 16) {{
                completedFeatures = 12;
                updateFeatureStatus(9, 12, 'completed');
            }}
            
            // 更新功能计数
            document.getElementById('featureCount').textContent = `${{completedFeatures}}/${{totalFeatures}} 已实现`;
        }}
        
        function updateFeatureStatus(startIdx, endIdx, status) {{
            const items = document.querySelectorAll('.feature-item');
            for (let i = startIdx; i < endIdx && i < items.length; i++) {{
                items[i].setAttribute('data-status', status);
                if (status === 'completed') {{
                    items[i].querySelector('.feature-checkbox').textContent = '☑';
                }}
            }}
        }}
        
        window.onload = function() {{
            loadData();
            setInterval(loadData, 10000);
        }};
    </script>
</body>
</html>
    """

