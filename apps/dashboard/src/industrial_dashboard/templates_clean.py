"""
Dashboard HTML 模板 - 带版本Tab

只在顶部增加版本切换Tab，其他内容完全保持
"""


def get_dashboard_html(title: str, subtitle: str) -> str:
    """获取 Dashboard HTML"""
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
            /* 黑白红三色体系 */
            --black: #000000;
            --gray-900: #212121;
            --gray-800: #424242;
            --gray-700: #616161;
            --gray-600: #757575;
            --gray-500: #9E9E9E;
            --gray-400: #BDBDBD;
            --gray-300: #E0E0E0;
            --gray-200: #EEEEEE;
            --gray-100: #F5F5F5;
            --white: #FFFFFF;
            --red: #D32F2F;
            
            /* 空间系统 */
            --space-2: 8px;
            --space-4: 16px;
            --space-6: 24px;
            --space-8: 32px;
            --space-12: 48px;
            --space-16: 64px;
            
            /* 阴影 */
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
            
            /* 字体 */
            --font-primary: 'Helvetica Neue', 'Arial', sans-serif;
            --font-chinese: 'Microsoft YaHei', '微软雅黑', sans-serif;
            --font-mono: 'Consolas', 'Monaco', monospace;
        }}
        
        body {{
            font-family: var(--font-primary);
            background: var(--white);
            color: var(--gray-900);
            line-height: 1.6;
            padding: 40px 60px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* 页面标题 */
        .page-header {{
            padding: 0 0 32px 0;
            margin-bottom: 32px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .project-badge {{
            font-size: 10px;
            font-weight: 500;
            color: var(--gray-600);
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 16px;
            display: block;
        }}
        
        .page-title {{
            font-size: 40px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
            margin-bottom: 12px;
            line-height: 1.2;
        }}
        
        .page-subtitle {{
            font-size: 13px;
            color: var(--gray-700);
            margin-bottom: 16px;
        }}
        
        .page-description {{
            font-size: 12px;
            color: var(--gray-600);
            line-height: 1.8;
        }}
        
        .status-pill {{
            position: absolute;
            top: 48px;
            right: 60px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            background: var(--red);
            color: white;
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: 500;
            letter-spacing: 1px;
        }}
        
        .status-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: white;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}
        
        /* 版本Tab（浏览器标签页风格） */
        .version-tabs {{
            display: flex;
            gap: 4px;
            margin-bottom: 0;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .version-tab {{
            font-family: var(--font-chinese);
            background: var(--gray-100);
            border: 1px solid var(--gray-300);
            border-bottom: none;
            padding: 12px 24px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
            gap: 4px;
            align-items: flex-start;
            border-radius: 4px 4px 0 0;
        }}
        
        .version-tab:hover {{
            background: var(--white);
        }}
        
        .version-tab.active {{
            background: var(--white);
            border-bottom: 2px solid var(--white);
            margin-bottom: -1px;
            z-index: 1;
            position: relative;
        }}
        
        .tab-label {{
            font-size: 13px;
            font-weight: 600;
            color: var(--black);
        }}
        
        .tab-subtitle {{
            font-size: 11px;
            color: var(--gray-600);
        }}
        
        .version-tab.active .tab-subtitle {{
            color: var(--red);
        }}
        
        /* 版本信息框 */
        .version-info {{
            padding: 24px 32px;
            background: var(--gray-100);
            margin-bottom: 48px;
        }}
        
        .version-name {{
            font-size: 17px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
            margin-bottom: 12px;
        }}
        
        .version-description {{
            font-size: 13px;
            color: var(--gray-700);
            line-height: 1.8;
        }}
        
        /* 统计卡片 */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
            margin-bottom: 64px;
        }}
        
        .stat-card {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: 32px 24px;
            transition: all 0.3s;
        }}
        
        .stat-card:hover {{
            border-color: var(--black);
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }}
        
        .stat-label {{
            font-size: 10px;
            color: var(--gray-600);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 16px;
            font-weight: 500;
        }}
        
        .stat-value {{
            font-size: 48px;
            font-weight: 300;
            color: var(--black);
            line-height: 1;
            margin-bottom: 12px;
        }}
        
        .stat-meta {{
            font-size: 12px;
            color: var(--gray-500);
        }}
        
        /* 进度条 */
        .progress-section {{
            padding: 32px 0;
            margin-bottom: 64px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 24px;
        }}
        
        .section-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
        }}
        
        .progress-value {{
            font-size: 24px;
            font-weight: 500;
            color: var(--red);
        }}
        
        .progress-bar {{
            height: 3px;
            background: var(--gray-200);
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: var(--red);
            transition: width 0.8s;
        }}
        
        /* 功能清单 */
        .features-section {{
            padding: 32px 0;
            margin-bottom: 64px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 32px;
            margin-top: 32px;
        }}
        
        .feature-group {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            padding: 24px;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s;
        }}
        
        .feature-group:hover {{
            border-color: var(--black);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        
        .feature-group-title {{
            font-size: 13px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
            margin-bottom: 20px;
        }}
        
        .feature-item {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 8px 0;
            font-size: 13px;
        }}
        
        .feature-item[data-status="completed"] {{
            color: var(--black);
            font-weight: 500;
        }}
        
        .feature-item[data-status="pending"] {{
            color: var(--gray-400);
        }}
        
        .feature-checkbox {{
            font-size: 14px;
            flex-shrink: 0;
            margin-top: 2px;
        }}
        
        .feature-content {{
            flex: 1;
        }}
        
        .feature-name {{
            display: block;
            margin-bottom: 4px;
        }}
        
        .feature-description {{
            font-size: 11px;
            color: var(--gray-500);
            line-height: 1.5;
        }}
        
        /* 任务列表 */
        .tasks-section {{
            padding: 32px 0;
        }}
        
        .task-card {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            padding: 32px;
            margin-bottom: 24px;
            transition: all 0.3s;
        }}
        
        .task-card:hover {{
            border-color: var(--black);
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }}
        
        .task-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .task-id {{
            font-family: var(--font-mono);
            font-size: 11px;
            color: white;
            font-weight: 500;
            background: var(--black);
            padding: 6px 12px;
            letter-spacing: 1.5px;
        }}
        
        .task-status {{
            font-family: var(--font-mono);
            font-size: 10px;
            padding: 6px 12px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border: 1px solid;
        }}
        
        .task-status.pending {{
            background: var(--gray-100);
            color: var(--gray-700);
            border-color: var(--gray-300);
        }}
        
        .task-status.in_progress {{
            background: var(--red);
            color: white;
            border-color: var(--red);
        }}
        
        .task-status.completed {{
            background: var(--black);
            color: white;
            border-color: var(--black);
        }}
        
        .task-title {{
            font-size: 20px;
            font-weight: 400;
            color: var(--black);
            margin-bottom: 16px;
            line-height: 1.4;
        }}
        
        .task-feature {{
            font-size: 13px;
            color: var(--gray-700);
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--gray-200);
        }}
        
        .feature-label {{
            color: var(--gray-600);
            font-weight: 500;
            margin-right: 8px;
        }}
        
        .feature-value {{
            color: var(--black);
            font-weight: 500;
        }}
        
        .task-details {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}
        
        .detail-item {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        
        .detail-label {{
            font-size: 11px;
            color: var(--gray-600);
            font-weight: 500;
        }}
        
        .detail-value {{
            font-size: 13px;
            color: var(--gray-900);
            font-weight: 500;
        }}
        
        .update-time {{
            position: fixed;
            bottom: 32px;
            right: 60px;
            font-family: var(--font-mono);
            font-size: 10px;
            color: var(--gray-500);
            letter-spacing: 1px;
        }}
        
        @media (max-width: 1200px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .features-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 页面标题 -->
        <div class="page-header">
            <span class="project-badge">项目 PROJECT</span>
            <h1 class="page-title">{title}</h1>
            <div class="page-subtitle">{subtitle}</div>
            <div class="page-description">
                融合 Claude Desktop + LibreChat + AWS + MCP 的 AI 操作系统
            </div>
            <div class="status-pill">
                <div class="status-dot"></div>
                <span>SYSTEM ONLINE</span>
            </div>
        </div>
        
        <!-- 版本切换Tab -->
        <div class="version-tabs" id="versionTabs">
            <button class="version-tab active" data-version="v1">
                <span class="tab-label">版本 1</span>
                <span class="tab-subtitle">MVP基础</span>
            </button>
            <button class="version-tab" data-version="v2">
                <span class="tab-label">版本 2</span>
                <span class="tab-subtitle">插件生态</span>
            </button>
            <button class="version-tab" data-version="v3">
                <span class="tab-label">版本 3</span>
                <span class="tab-subtitle">高级特性</span>
            </button>
        </div>
        
        <!-- 版本描述 -->
        <div class="version-info" id="versionInfo">
            <div class="version-name">版本 1.0 - MVP</div>
            <div class="version-description">LibreChat Desktop 首个版本，实现核心桌面框架和基础功能</div>
        </div>
        
        <!-- 以下是原有的完整内容 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">总任务数</div>
                <div class="stat-value" id="totalTasks">—</div>
                <div class="stat-meta">Total Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">待处理</div>
                <div class="stat-value" id="pendingTasks">—</div>
                <div class="stat-meta">Pending</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">进行中</div>
                <div class="stat-value" id="inProgressTasks">—</div>
                <div class="stat-meta">In Progress</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">已完成</div>
                <div class="stat-value" id="completedTasks">—</div>
                <div class="stat-meta">Completed</div>
            </div>
        </div>
        
        <div class="progress-section">
            <div class="section-header">
                <span class="section-title">整体进度</span>
                <span class="progress-value" id="progressValue">0%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressBar" style="width: 0%"></div>
            </div>
        </div>
        
        <div class="features-section">
            <div class="section-header">
                <span class="section-title">核心功能</span>
                <span class="stat-meta" id="featureCount">0/12 已实现</span>
            </div>
            <div class="features-grid">
                <div class="feature-group">
                    <div class="feature-group-title">第一阶段：基础框架</div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">Electron 桌面框架</span>
                            <span class="feature-description">Vite + React + TypeScript</span>
                        </div>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">LibreChat 对话集成</span>
                            <span class="feature-description">Webview 嵌入对话界面</span>
                        </div>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">项目管理系统</span>
                            <span class="feature-description">项目CRUD + 本地存储</span>
                        </div>
                    </div>
                </div>
                <div class="feature-group">
                    <div class="feature-group-title">第二阶段：云端集成</div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">AWS SSO 认证</span>
                            <span class="feature-description">单点登录 + 凭证管理</span>
                        </div>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">MCP 工具桥接</span>
                            <span class="feature-description">IPC 通信 + 工具调用</span>
                        </div>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">本地工具调用</span>
                            <span class="feature-description">文件系统 + Shell 命令</span>
                        </div>
                    </div>
                </div>
                <div class="feature-group">
                    <div class="feature-group-title">第三阶段：插件体系</div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">插件加载器</span>
                            <span class="feature-description">动态加载 + 沙箱隔离</span>
                        </div>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">核心插件集</span>
                            <span class="feature-description">AWS + GitHub + Memory</span>
                        </div>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">插件市场</span>
                            <span class="feature-description">浏览 + 安装 + 更新</span>
                        </div>
                    </div>
                </div>
                <div class="feature-group">
                    <div class="feature-group-title">第四阶段：高级特性</div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">Artifacts 系统</span>
                            <span class="feature-description">代码 + 文档 + 图表</span>
                        </div>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">任务白板集成</span>
                            <span class="feature-description">任务管理 + 对话关联</span>
                        </div>
                    </div>
                    <div class="feature-item" data-status="pending">
                        <span class="feature-checkbox">☐</span>
                        <div class="feature-content">
                            <span class="feature-name">多窗口管理</span>
                            <span class="feature-description">并行开发 + 状态同步</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="tasks-section">
            <div class="section-header">
                <span class="section-title">任务列表</span>
                <span class="stat-meta" id="taskCount">0 tasks</span>
            </div>
            <div class="task-list" id="taskList">
                <div class="empty-state">Loading...</div>
            </div>
        </div>
    </div>
    
    <div class="update-time" id="updateTime">—</div>
    
    <script>
        function getStatusText(status) {{
            const map = {{
                'pending': '待处理',
                'in_progress': '进行中',
                'review': '审查中',
                'completed': '已完成',
                'failed': '失败'
            }};
            return map[status.toLowerCase()] || status;
        }}
        
        function getTaskFeatures(taskId) {{
            const map = {{
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
            return map[taskId] || '—';
        }}
        
        function getCompletionDetails(task) {{
            try {{
                if (!task.description) return '';
                const completion = JSON.parse(task.description);
                if (!completion.features_implemented) return '';
                
                return `
                    <div style="margin-top: 24px; padding-top: 24px; border-top: 1px solid #EEEEEE;">
                        <div style="font-size: 13px; font-weight: 700; color: #000000; margin-bottom: 12px; font-family: 'Microsoft YaHei';">
                            ✓ 已实现功能清单
                        </div>
                        <div style="display: grid; gap: 8px;">
                            ${{completion.features_implemented.map(f => `
                                <div style="font-size: 13px; color: #424242; padding-left: 20px; position: relative;">
                                    <span style="position: absolute; left: 0; color: #D32F2F; font-weight: bold;">•</span>
                                    ${{f}}
                                </div>
                            `).join('')}}
                        </div>
                        ${{completion.metrics ? `
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #F5F5F5;">
                            <div>
                                <div style="font-size: 11px; color: #9E9E9E;">代码量</div>
                                <div style="font-size: 14px; color: #000000; font-weight: 600;">${{completion.metrics.code_lines || 0}} 行</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: #9E9E9E;">新建文件</div>
                                <div style="font-size: 14px; color: #000000; font-weight: 600;">${{completion.metrics.files_created || 0}} 个</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: #9E9E9E;">修改文件</div>
                                <div style="font-size: 14px; color: #000000; font-weight: 600;">${{completion.metrics.files_modified || 0}} 个</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; color: #9E9E9E;">实际工时</div>
                                <div style="font-size: 14px; color: #000000; font-weight: 600;">${{completion.metrics.actual_hours || 0}} 小时</div>
                            </div>
                        </div>
                        ` : ''}}
                    </div>
                `;
            }} catch (e) {{
                return '';
            }}
        }}
        
        async function loadData() {{
            try {{
                // 加载所有任务数据
                const tasksRes = await fetch('/api/tasks');
                allTasksData = await tasksRes.json();
                
                // 显示当前版本的数据
                switchVersion(currentVersion);
                
                const now = new Date();
                document.getElementById('updateTime').textContent = now.toLocaleTimeString('zh-CN', {{ hour12: false }});
                
            }} catch (error) {{
                console.error('Load error:', error);
            }}
        }}
        
        
        // 版本数据（支持动态扩展）
        let allTasksData = [];
        let currentVersion = 'v1';
        
        const versionConfigs = {{
            'v1': {{
                name: '版本 1 - MVP',
                description: 'LibreChat Desktop 首个版本，实现核心桌面框架和基础功能',
                taskFilter: (task) => true  // 版本1显示所有任务
            }},
            'v2': {{
                name: '版本 2 - 插件生态', 
                description: '引入完整的插件体系，支持扩展和自定义（开发中）',
                taskFilter: (task) => task.id.startsWith('v2-')  // 版本2只显示v2-开头的
            }},
            'v3': {{
                name: '版本 3 - 高级特性',
                description: '实现高级特性和性能优化（规划中）',
                taskFilter: (task) => task.id.startsWith('v3-')  // 版本3只显示v3-开头的
            }}
        }};
        
        // 切换版本
        function switchVersion(versionId) {{
            currentVersion = versionId;
            
            // 更新Tab状态
            document.querySelectorAll('.version-tab').forEach(tab => {{
                if (tab.dataset.version === versionId) {{
                    tab.classList.add('active');
                }} else {{
                    tab.classList.remove('active');
                }}
            }});
            
            // 更新版本信息
            const config = versionConfigs[versionId];
            document.getElementById('versionInfo').innerHTML = `
                <div class="version-name">${{config.name}}</div>
                <div class="version-description">${{config.description}}</div>
            `;
            
            // 过滤并显示该版本的任务
            const versionTasks = allTasksData.filter(config.taskFilter);
            displayVersionData(versionTasks);
        }}
        
        // 显示版本数据
        function displayVersionData(tasks) {{
            const completed = tasks.filter(t => t.status === 'completed').length;
            const inProgress = tasks.filter(t => t.status === 'in_progress').length;
            const pending = tasks.filter(t => t.status === 'pending').length;
            const total = tasks.length;
            
            // 更新统计卡片
            document.getElementById('totalTasks').textContent = total;
            document.getElementById('pendingTasks').textContent = pending;
            document.getElementById('inProgressTasks').textContent = inProgress;
            document.getElementById('completedTasks').textContent = completed;
            
            // 更新进度条
            const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
            document.getElementById('progressValue').textContent = progress + '%';
            document.getElementById('progressBar').style.width = progress + '%';
            
            // 更新任务列表
            document.getElementById('taskCount').textContent = total + ' tasks';
            
            if (total === 0) {{
                document.getElementById('taskList').innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 48px; margin-bottom: 16px;">📝</div>
                        <div style="font-size: 16px; color: #757575; margin-bottom: 8px;">此版本暂无任务</div>
                        <div style="font-size: 13px; color: #BDBDBD;">版本 ${{currentVersion}} 的任务尚未创建</div>
                    </div>
                `;
            }} else {{
                document.getElementById('taskList').innerHTML = tasks.map(task => `
                    <div class="task-card">
                        <div class="task-card-header">
                            <span class="task-id">${{task.id}}</span>
                            <span class="task-status ${{task.status.toLowerCase().replace(' ', '_')}}">
                                ${{getStatusText(task.status)}}
                            </span>
                        </div>
                        <div class="task-title">${{task.title}}</div>
                        <div class="task-feature">
                            <span class="feature-label">实现功能</span>
                            <span class="feature-value">${{getTaskFeatures(task.id)}}</span>
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
                        ${{task.status === 'completed' ? getCompletionDetails(task) : ''}}
                    </div>
                `).join('');
            }}
            
            // 更新功能清单（简化版，实际应该根据版本配置）
            const featureCompleted = Math.floor(completed / 4 * 3);
            document.getElementById('featureCount').textContent = `${{featureCompleted}}/12 已实现`;
        }}
        
        // 绑定Tab点击事件
        document.querySelectorAll('.version-tab').forEach(tab => {{
            tab.addEventListener('click', function() {{
                switchVersion(this.dataset.version);
            }});
        }});
        
        window.onload = function() {{
            loadData();
            setInterval(loadData, 10000);
        }};
    </script>
</body>
</html>
    """
