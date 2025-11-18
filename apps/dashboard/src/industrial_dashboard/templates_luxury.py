"""
奢侈品级工业美学 Dashboard 模板

设计理念: Porsche Design + Hermès + Bang & Olufsen
核心: 极简即奢华 + 精密工学美学 + 建筑级空间比例
"""


def get_dashboard_html(title: str, subtitle: str) -> str:
    """获取奢侈品级 Dashboard HTML"""
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
            /* === 黑白红三色体系 === */
            --black: #000000;
            --black-light: #1A1A1A;
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
            
            /* === 红色强调系统 === */
            --red: #D32F2F;
            --red-dark: #B71C1C;
            --red-light: #EF5350;
            --red-lighter: #FFEBEE;
            
            /* === 空间系统（8px模数） === */
            --space-1: 4px;
            --space-2: 8px;
            --space-3: 12px;
            --space-4: 16px;
            --space-5: 20px;
            --space-6: 24px;
            --space-8: 32px;
            --space-10: 40px;
            --space-12: 48px;
            --space-16: 64px;
            --space-20: 80px;
            
            /* === 阴影系统 === */
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04);
            
            /* === 字体系统 === */
            --font-primary: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            --font-chinese: 'Microsoft YaHei', '微软雅黑', 'SimHei', '黑体', sans-serif;
            --font-mono: 'JetBrains Mono', 'SF Mono', 'Consolas', monospace;
            
            --text-xs: 11px;
            --text-sm: 13px;
            --text-base: 15px;
            --text-lg: 17px;
            --text-xl: 20px;
            --text-2xl: 24px;
            --text-3xl: 32px;
            
            --weight-light: 300;
            --weight-normal: 400;
            --weight-medium: 500;
            --weight-semibold: 600;
            --weight-bold: 700;
        }}
        
        body {{
            font-family: var(--font-primary);
            background: var(--white);
            color: var(--gray-900);
            line-height: 1.6;
            padding: var(--space-12) var(--space-16);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* === 页面标题区域 === */
        .page-header {{
            padding: 0 0 var(--space-12) 0;
            margin-bottom: var(--space-12);
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .project-badge {{
            font-size: var(--text-xs);
            font-weight: var(--weight-medium);
            color: var(--gray-600);
            letter-spacing: 0.25em;
            text-transform: uppercase;
            margin-bottom: var(--space-4);
            display: block;
        }}
        
        .page-title {{
            font-size: 40px;
            font-weight: var(--weight-bold);
            color: var(--black);
            font-family: var(--font-chinese);
            letter-spacing: 0;
            margin-bottom: var(--space-3);
            line-height: 1.2;
            text-align: left;
        }}
        
        .page-subtitle {{
            font-size: var(--text-sm);
            font-weight: var(--weight-normal);
            color: var(--gray-700);
            letter-spacing: 0.025em;
            margin-bottom: var(--space-4);
        }}
        
        .page-description {{
            font-size: var(--text-sm);
            color: var(--gray-600);
            letter-spacing: 0.015em;
            line-height: 1.8;
            max-width: 600px;
        }}
        
        .status-pill {{
            position: absolute;
            top: var(--space-12);
            right: var(--space-16);
            display: inline-flex;
            align-items: center;
            gap: var(--space-2);
            padding: var(--space-2) var(--space-4);
            background: var(--red);
            color: white;
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: var(--weight-medium);
            letter-spacing: 0.1em;
        }}
        
        .status-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: white;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}
        
        /* === 统计卡片 === */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--space-6);
            margin-bottom: var(--space-16);
        }}
        
        .stat-card {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: var(--space-8) var(--space-6);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .stat-card:hover {{
            border-color: var(--black);
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }}
        
        .stat-label {{
            font-size: var(--text-xs);
            font-weight: var(--weight-medium);
            color: var(--gray-600);
            text-transform: uppercase;
            letter-spacing: 0.2em;
            margin-bottom: var(--space-4);
        }}
        
        .stat-value {{
            font-size: 48px;
            font-weight: var(--weight-light);
            color: var(--black);
            line-height: 1;
            margin-bottom: var(--space-3);
        }}
        
        .stat-meta {{
            font-size: var(--text-sm);
            color: var(--gray-500);
            font-weight: var(--weight-normal);
        }}
        
        /* === 进度区域 === */
        .progress-section {{
            padding: var(--space-8) 0;
            margin-bottom: var(--space-12);
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: var(--space-6);
        }}
        
        .section-title {{
            font-size: 16px;
            font-weight: var(--weight-bold);
            color: var(--black);
            font-family: var(--font-chinese);
            text-transform: none;
            letter-spacing: 1px;
        }}
        
        .progress-value {{
            font-size: var(--text-2xl);
            font-weight: var(--weight-medium);
            color: var(--red);
        }}
        
        .progress-bar {{
            height: 3px;
            background: var(--gray-200);
            position: relative;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: var(--red);
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* === 功能清单 === */
        .features-section {{
            padding: var(--space-8) 0;
            margin-bottom: var(--space-12);
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--space-10);
            margin-top: var(--space-8);
        }}
        
        .feature-group {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            padding: var(--space-8);
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
            font-weight: var(--weight-bold);
            color: var(--black);
            font-family: var(--font-chinese);
            text-transform: none;
            letter-spacing: 0.5px;
            margin-bottom: var(--space-5);
        }}
        
        .feature-item {{
            display: flex;
            align-items: center;
            gap: var(--space-3);
            padding: var(--space-2) 0;
            font-size: var(--text-sm);
            transition: opacity 0.3s;
        }}
        
        .feature-item[data-status="completed"] {{
            color: var(--black);
            font-weight: var(--weight-medium);
        }}
        
        .feature-item[data-status="pending"] {{
            color: var(--gray-400);
            font-weight: var(--weight-normal);
        }}
        
        .feature-checkbox {{
            font-size: 14px;
            color: inherit;
        }}
        
        /* === 版本Tab切换（顶部标签页） === */
        .version-tabs-container {{
            margin-bottom: var(--space-12);
        }}
        
        .version-tabs {{
            display: flex;
            gap: 0;
            border-bottom: 1px solid var(--gray-300);
            margin-bottom: 0;
        }}
        
        .version-tab {{
            font-family: var(--font-chinese);
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            padding: var(--space-4) var(--space-6);
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: var(--space-1);
        }}
        
        .version-tab:hover {{
            background: var(--gray-100);
            border-bottom-color: var(--gray-500);
        }}
        
        .version-tab.active {{
            background: transparent;
            border-bottom-color: var(--black);
        }}
        
        .tab-label {{
            font-size: 14px;
            font-weight: var(--weight-semibold);
            color: var(--black);
        }}
        
        .tab-subtitle {{
            font-size: 11px;
            font-weight: var(--weight-normal);
            color: var(--gray-600);
        }}
        
        .version-tab.active .tab-subtitle {{
            color: var(--red);
        }}
        
        .version-info {{
            padding: var(--space-6) 0 var(--space-8) 0;
            border-bottom: 1px solid var(--gray-300);
            margin-bottom: var(--space-12);
        }}
        
        .version-name {{
            font-size: var(--text-lg);
            font-weight: var(--weight-bold);
            color: var(--black);
            font-family: var(--font-chinese);
            margin-bottom: var(--space-3);
        }}
        
        .version-description {{
            font-size: var(--text-sm);
            color: var(--gray-700);
            line-height: 1.8;
            margin-bottom: var(--space-4);
        }}
        
        .version-upgrades {{
            margin-top: var(--space-5);
        }}
        
        .version-upgrades-title {{
            font-size: 13px;
            font-weight: var(--weight-bold);
            color: var(--black);
            font-family: var(--font-chinese);
            margin-bottom: var(--space-3);
        }}
        
        .upgrade-item {{
            font-size: var(--text-sm);
            color: var(--gray-700);
            padding-left: var(--space-5);
            position: relative;
            margin-bottom: var(--space-2);
            line-height: 1.6;
        }}
        
        .upgrade-item::before {{
            content: '•';
            position: absolute;
            left: 0;
            color: var(--red);
            font-weight: bold;
        }}
        
        /* === 任务卡片 === */
        .tasks-section {{
            padding: var(--space-8) 0;
        }}
        
        .task-card {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            padding: var(--space-8);
            margin-bottom: var(--space-6);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
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
            margin-bottom: var(--space-5);
        }}
        
        .task-id {{
            font-family: var(--font-mono);
            font-size: 11px;
            color: white;
            font-weight: var(--weight-medium);
            background: var(--black);
            padding: var(--space-2) var(--space-3);
            letter-spacing: 0.15em;
        }}
        
        .task-status {{
            font-family: var(--font-mono);
            font-size: 10px;
            padding: var(--space-2) var(--space-3);
            font-weight: var(--weight-medium);
            text-transform: uppercase;
            letter-spacing: 0.15em;
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
            font-size: var(--text-xl);
            font-weight: var(--weight-normal);
            color: var(--black);
            margin-bottom: var(--space-4);
            letter-spacing: 0.025em;
            line-height: 1.4;
        }}
        
        .task-feature {{
            font-size: var(--text-sm);
            color: var(--gray-700);
            margin-bottom: var(--space-6);
            padding-bottom: var(--space-6);
            border-bottom: 1px solid var(--gray-200);
        }}
        
        .feature-label {{
            color: var(--gray-600);
            font-weight: var(--weight-medium);
            margin-right: var(--space-2);
        }}
        
        .feature-value {{
            color: var(--black);
            font-weight: var(--weight-medium);
        }}
        
        /* === 卡片内表格 === */
        .task-details {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--space-5) var(--space-6);
            font-size: var(--text-sm);
        }}
        
        .detail-item {{
            display: flex;
            flex-direction: column;
            gap: var(--space-1);
        }}
        
        .detail-label {{
            font-size: var(--text-xs);
            color: var(--gray-600);
            font-weight: var(--weight-medium);
            letter-spacing: 0.05em;
        }}
        
        .detail-value {{
            font-size: var(--text-sm);
            color: var(--gray-900);
            font-weight: var(--weight-medium);
        }}
        
        /* === 空状态 === */
        .empty-state {{
            text-align: center;
            padding: var(--space-16);
            color: var(--mercury);
            font-size: var(--text-sm);
        }}
        
        /* === 页脚时间戳 === */
        .update-time {{
            position: fixed;
            bottom: var(--space-8);
            right: var(--space-16);
            font-family: var(--font-mono);
            font-size: 10px;
            color: var(--gray-500);
            font-weight: var(--weight-normal);
            letter-spacing: 0.1em;
        }}
        
        /* === 响应式 === */
        @media (max-width: 1200px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .features-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: var(--space-6) var(--space-4); }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .features-grid {{ grid-template-columns: 1fr; }}
            .task-details {{ grid-template-columns: repeat(2, 1fr); }}
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
        
        <!-- 版本切换Tab（标签页） -->
        <div class="version-tabs-container">
            <div class="version-tabs" id="versionTabs">
                <button class="version-tab active" data-version="v1.0">
                    <span class="tab-label">版本 1.0</span>
                    <span class="tab-subtitle">MVP基础</span>
                </button>
                <button class="version-tab" data-version="v2.0">
                    <span class="tab-label">版本 2.0</span>
                    <span class="tab-subtitle">插件生态</span>
                </button>
                <button class="version-tab" data-version="v3.0">
                    <span class="tab-label">版本 3.0</span>
                    <span class="tab-subtitle">高级特性</span>
                </button>
            </div>
        </div>
        
        <!-- 版本描述框 -->
        <div class="version-info" id="versionInfo">
            <div class="version-name">版本 1.0 - MVP</div>
            <div class="version-description">LibreChat Desktop 首个版本，实现核心桌面框架和基础功能</div>
        </div>
        
        <!-- 统计卡片 -->
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
        
        <!-- 整体进度 -->
        <div class="progress-section">
            <div class="section-header">
                <span class="section-title">整体进度</span>
                <span class="progress-value" id="progressValue">0%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressBar" style="width: 0%"></div>
            </div>
        </div>
        
        <!-- 核心功能清单 -->
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
        
        <!-- 任务列表 -->
        <div class="tasks-section">
            <div class="section-header">
                <span class="section-title">任务列表</span>
                <span class="stat-meta" id="taskCount">0 tasks</span>
            </div>
            <div class="task-list" id="taskList">
                <div class="empty-state">Loading...</div>
            </div>
        </div>
        
    </div><!-- 关闭 container -->
    
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
        
        // 获取任务完成详情
        function getCompletionDetails(task) {{
            try {{
                if (!task.description || task.description === '') return '';
                
                const completion = JSON.parse(task.description);
                if (!completion.features_implemented) return '';
                
                return `
                    <div style="margin-top: 24px; padding-top: 24px; border-top: 1px solid #EEEEEE;">
                        <div style="font-size: 12px; font-weight: 600; color: #000000; margin-bottom: 12px; font-family: 'Microsoft YaHei';">
                            ✓ 已实现功能清单
                        </div>
                        <div style="display: grid; gap: 8px;">
                            ${{completion.features_implemented.map(feature => `
                                <div style="font-size: 13px; color: #424242; padding-left: 16px; position: relative;">
                                    <span style="position: absolute; left: 0; color: #D32F2F;">•</span>
                                    ${{feature}}
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
                    taskList.innerHTML = '<div class="empty-state">暂无任务</div>';
                }} else {{
                    taskList.innerHTML = tasks.map(task => `
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
                        </div>
                    `).join('');
                }}
                
                // 更新功能清单
                updateFeatures(stats);
                
                const now = new Date();
                const timeStr = now.toLocaleTimeString('zh-CN', {{ hour12: false }});
                document.getElementById('updateTime').textContent = timeStr;
                
            }} catch (error) {{
                console.error('Load data error:', error);
            }}
        }}
        
        function updateFeatures(stats) {{
            const completedCount = stats.completed_tasks;
            let completedFeatures = 0;
            
            if (completedCount >= 4) {{
                completedFeatures = 3;
                updateFeatureStatus(0, 3, 'completed');
            }}
            if (completedCount >= 8) {{
                completedFeatures = 6;
                updateFeatureStatus(3, 6, 'completed');
            }}
            if (completedCount >= 12) {{
                completedFeatures = 9;
                updateFeatureStatus(6, 9, 'completed');
            }}
            if (completedCount >= 16) {{
                completedFeatures = 12;
                updateFeatureStatus(9, 12, 'completed');
            }}
            
            document.getElementById('featureCount').textContent = `${{completedFeatures}}/12 已实现`;
        }}
        
        function updateFeatureStatus(start, end, status) {{
            const items = document.querySelectorAll('.feature-item');
            for (let i = start; i < end && i < items.length; i++) {{
                items[i].setAttribute('data-status', status);
                if (status === 'completed') {{
                    items[i].querySelector('.feature-checkbox').textContent = '☑';
                }}
            }}
        }}
        
        // 版本数据
        const versions = {{
            'v1.0': {{
                name: '版本 1.0 - MVP',
                description: 'LibreChat Desktop 首个版本，实现核心桌面框架和基础功能',
                features: ['Electron 桌面框架', 'LibreChat 对话集成', '项目管理', 'AWS SSO 认证'],
                taskPrefix: 'phase1-'
            }},
            'v2.0': {{
                name: '版本 2.0 - 插件生态',
                description: '引入完整的插件体系，支持扩展和自定义功能',
                upgrades: ['新增插件系统架构', '支持第三方插件开发', '插件市场上线', 'Artifacts实时预览'],
                taskPrefix: 'phase2-'
            }},
            'v3.0': {{
                name: '版本 3.0 - 高级特性',
                description: '完整的任务白板集成和多窗口管理',
                upgrades: ['任务白板深度集成', '多窗口并行开发', '性能全面优化', '企业级部署支持'],
                taskPrefix: 'phase3-'
            }}
        }};
        
        let currentVersion = 'v1.0';
        let allTasksCache = [];
        
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
            const version = versions[versionId];
            const infoHtml = `
                <div class="version-name">${{version.name}}</div>
                <div class="version-description">${{version.description}}</div>
                ${{version.upgrades ? `
                    <div class="version-upgrades">
                        <div class="version-upgrades-title">🔄 本版升级内容</div>
                        ${{version.upgrades.map(u => `<div class="upgrade-item">${{u}}</div>`).join('')}}
                    </div>
                ` : ''}}
            `;
            document.getElementById('versionInfo').innerHTML = infoHtml;
            
            // 过滤任务
            filterTasksByVersion(versionId);
        }}
        
        // 根据版本过滤任务
        function filterTasksByVersion(versionId) {{
            const version = versions[versionId];
            const prefix = version.taskPrefix || '';
            
            let filteredTasks = allTasksCache;
            if (prefix) {{
                filteredTasks = allTasksCache.filter(task => task.id.startsWith(prefix));
            }}
            
            displayTasks(filteredTasks);
        }}
        
        // 显示任务列表
        function displayTasks(tasks) {{
            const taskList = document.getElementById('taskList');
            document.getElementById('taskCount').textContent = tasks.length + ' tasks';
            
            if (tasks.length === 0) {{
                taskList.innerHTML = '<div class="empty-state">此版本暂无任务</div>';
                return;
            }}
            
            taskList.innerHTML = tasks.map(task => `
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
        
        // 绑定Tab点击事件
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('.version-tab').forEach(tab => {{
                tab.addEventListener('click', function() {{
                    switchVersion(this.dataset.version);
                }});
            }});
        }});
        
        // 修改原loadData函数
        async function loadDataOriginal() {{
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
                allTasksCache = await tasksRes.json();
                
                // 更新功能清单
                updateFeatures(stats);
                
                // 显示当前版本的任务
                filterTasksByVersion(currentVersion);
                
                const now = new Date();
                const timeStr = now.toLocaleTimeString('zh-CN', {{ hour12: false }});
                document.getElementById('updateTime').textContent = timeStr;
                
            }} catch (error) {{
                console.error('Load data error:', error);
            }}
        }}
        
        // 重命名函数
        const loadData = loadDataOriginal;
        
        window.onload = function() {{
            loadData();
            setInterval(loadData, 10000);
            switchVersion('v1.0');  // 默认显示v1.0
        }};
    </script>
</body>
</html>
    """

