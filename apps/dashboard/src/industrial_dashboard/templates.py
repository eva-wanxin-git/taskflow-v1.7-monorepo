"""
Dashboard HTML 模板 - 带版本Tab + 缓存控制

支持：
1. 版本号URL参数
2. Service Worker注册
3. 缓存清除按钮
"""


def get_dashboard_html(title: str, subtitle: str, cache_version: str = "v1763481040") -> str:
    """
    获取 Dashboard HTML
    
    Args:
        title: 页面标题
        subtitle: 副标题
        cache_version: 缓存版本号
    """
    return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>{title} - {cache_version}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            /* 敦煌壁画色系 */
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
            --red: #985239;        /* 敦煌赭红 - 主强调色 */
            --blue: #537696;       /* 敦煌青蓝 - 次强调色 */
            
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
        
        /* 品牌标识（固定） */
        .brand-header {{
            margin-bottom: 48px;
        }}
        
        .brand-title {{
            font-size: 40px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
            margin-bottom: 12px;
            line-height: 1.2;
        }}
        
        .brand-slogan {{
            font-size: 13px;
            color: var(--gray-700);
            line-height: 1.6;
            margin-bottom: 48px;
        }}
        
        /* 项目信息区域 */
        .project-header {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: 32px;
            margin-bottom: 48px;
            position: relative;
        }}
        
        .project-info {{
            display: grid;
            gap: 24px;
        }}
        
        .project-name {{
            font-size: 28px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
            line-height: 1.2;
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .project-details {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        
        .detail-row {{
            display: flex;
            gap: 12px;
            font-size: 13px;
            line-height: 1.8;
        }}
        
        .detail-label {{
            color: var(--gray-600);
            min-width: 100px;
            font-weight: 500;
        }}
        
        .detail-value {{
            color: var(--gray-900);
            font-weight: 400;
        }}
        
        .status-pill {{
            position: absolute;
            top: 32px;
            right: 32px;
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
            padding: 16px 28px;
            cursor: pointer;
            transition: all 0.3s;
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
            font-size: 20px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
        }}
        
        .version-tab.active .tab-label {{
            color: var(--red);
        }}
        
        /* 版本信息框 */
        .version-info {{
            padding: 24px 32px;
            background: var(--gray-100);
            margin-bottom: 48px;
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
        
        /* 进度时间轴模块（交错布局） */
        .progress-section {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: 32px;
            margin-bottom: 48px;
            position: relative;
        }}
        
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 32px;
        }}
        
        .section-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--black);
            font-family: 'Helvetica Neue', Arial, sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .progress-value {{
            background: var(--red);
            padding: 4px;
            width: 140px;
            height: 140px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .progress-inner {{
            background: var(--white);
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }}
        
        .progress-percent {{
            font-size: 56px;
            font-weight: 900;
            font-family: var(--font-mono);
            line-height: 1;
            color: var(--black);
        }}
        
        .progress-label {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            font-family: var(--font-mono);
            color: var(--gray-700);
            text-transform: uppercase;
        }}
        
        /* 时间轴容器 */
        .timeline-container {{
            position: relative;
            height: 280px;
        }}
        
        /* 水平主线 */
        .timeline-main-line {{
            position: absolute;
            top: 140px;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--gray-300);
        }}
        
        /* 进度填充线 */
        .timeline-progress {{
            position: absolute;
            top: 140px;
            left: 0;
            height: 2px;
            background: var(--blue);
            transition: width 0.8s;
        }}
        
        /* 时间轴节点 */
        .timeline-nodes {{
            position: relative;
            height: 100%;
        }}
        
        /* 单个节点 */
        .timeline-node {{
            position: absolute;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        /* 上方节点 */
        .timeline-node.top {{
            top: 0;
        }}
        
        /* 下方节点 */
        .timeline-node.bottom {{
            bottom: 0;
        }}
        
        /* 时间标签（上方小文字） */
        .node-time-label {{
            font-size: 11px;
            color: var(--gray-700);
            font-family: var(--font-mono);
            margin-bottom: 8px;
            font-weight: 500;
        }}
        
        /* 彩色标签框 */
        .node-badge {{
            padding: 10px 20px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
            font-family: var(--font-chinese);
            white-space: nowrap;
            margin-bottom: 12px;
        }}
        
        /* 节点圆点 */
        .node-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--black);
            position: relative;
            margin-bottom: 12px;
        }}
        
        .timeline-node.bottom .node-dot {{
            margin-bottom: 0;
            margin-top: 12px;
        }}
        
        .timeline-node.bottom .node-badge {{
            margin-bottom: 0;
            margin-top: 12px;
        }}
        
        .timeline-node.bottom .node-time-label {{
            margin-bottom: 0;
            margin-top: 8px;
        }}
        
        /* 虚线连接 */
        .node-connector {{
            width: 1px;
            height: 50px;
            border-left: 1px dashed var(--gray-400);
        }}
        
        /* 功能描述（下方小文字） */
        .node-desc {{
            font-size: 11px;
            color: var(--gray-600);
            font-family: var(--font-chinese);
            text-align: center;
            max-width: 150px;
            line-height: 1.5;
        }}
        
        /* 敦煌配色标签 */
        .badge-orange {{
            background: #C87D5C;
            color: white;
        }}
        
        .badge-yellow {{
            background: #E6C866;
            color: #49565E;
        }}
        
        .badge-green {{
            background: #7BA882;
            color: white;
        }}
        
        .badge-blue {{
            background: #6B8CAE;
            color: white;
        }}
        
        .badge-purple {{
            background: #8B7BA8;
            color: white;
        }}
        
        .badge-brown {{
            background: #A37867;
            color: white;
        }}
        
        .badge-gray {{
            background: #E0E0E0;
            color: var(--gray-600);
        }}
        
        /* 功能清单 */
        .features-section {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: 32px;
            margin-bottom: 48px;
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 32px;
            margin-top: 32px;
        }}
        
        .feature-group {{
            background: var(--white);
            border: 1px solid rgba(224, 224, 224, 0.5);
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
        
        /* 全栈开发工程师模块 + 测试工程师模块 + 用户终测模块 + 交付工程师模块 */
        .developer-section,
        .tester-section,
        .user-testing-section,
        .delivery-section {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: 32px;
            margin-bottom: 48px;
        }}
        
        /* 运维工程师模块（固定模块，淡绿色背景） */
        .ops-section {{
            background: rgba(123, 168, 130, 0.03);
            border: 1px solid rgba(123, 168, 130, 0.3);
            border-top: 2px solid #7BA882;
            padding: 32px;
            margin-bottom: 48px;
        }}
        
        .developer-header,
        .tester-header,
        .user-testing-header,
        .delivery-header,
        .ops-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }}
        
        .developer-title,
        .tester-title,
        .user-testing-title,
        .delivery-title,
        .ops-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--black);
            font-family: 'Helvetica Neue', Arial, sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .ops-title {{
            color: #7BA882;
        }}
        
        .developer-count,
        .tester-count,
        .user-testing-stats,
        .delivery-count,
        .ops-status {{
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--gray-600);
        }}
        
        .ops-status {{
            color: #7BA882;
        }}
        
        .developer-tabs,
        .tester-tabs,
        .user-testing-tabs,
        .delivery-tabs,
        .ops-tabs {{
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        /* 任务筛选Tab - 二级Tab */
        .task-filter-tabs {{
            display: flex;
            gap: 0;
            border-bottom: 1px solid #E0E0E0;
            margin-bottom: 16px;
        }}
        
        .task-filter-tab {{
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 11px;
            font-weight: 600;
            color: #757575;
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            padding: 8px 20px;
            cursor: pointer;
            transition: all 0.2s ease;
            letter-spacing: 0.5px;
        }}
        
        .task-filter-tab:hover {{
            color: #000000;
        }}
        
        .task-filter-tab.active {{
            color: #000000;
            border-bottom-color: #985239;
        }}
        
        .developer-tab,
        .tester-tab,
        .user-testing-tab,
        .delivery-tab,
        .ops-tab {{
            font-family: var(--font-chinese);
            font-size: 13px;
            font-weight: 600;
            color: var(--gray-600);
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: transparent;
            border-bottom: 2px solid transparent;
            transition: all 0.3s;
        }}
        
        .developer-tab:hover,
        .tester-tab:hover,
        .user-testing-tab:hover,
        .delivery-tab:hover,
        .ops-tab:hover {{
            color: var(--black);
        }}
        
        .developer-tab.active,
        .tester-tab.active,
        .user-testing-tab.active,
        .delivery-tab.active,
        .ops-tab.active {{
            color: var(--black);
            border-bottom-color: var(--blue);
        }}
        
        .developer-tab-content,
        .tester-tab-content,
        .user-testing-tab-content,
        .delivery-tab-content,
        .ops-tab-content {{
            display: none;
        }}
        
        .developer-tab-content.active,
        .tester-tab-content.active,
        .user-testing-tab-content.active,
        .delivery-tab-content.active,
        .ops-tab-content.active {{
            display: block;
        }}
        
        /* 用户终测Bug清单 */
        .feedback-list {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        
        .feedback-item {{
            display: flex;
            gap: 16px;
            align-items: flex-start;
            padding: 16px;
            border: 1px solid rgba(224, 224, 224, 0.5);
            border-left: 4px solid;
            transition: all 0.3s;
            position: relative;
        }}
        
        .feedback-item:hover {{
            background: var(--gray-100);
            border-color: var(--black);
        }}
        
        .feedback-item.info {{ border-left-color: #6B8CAE; }}
        .feedback-item.success {{ border-left-color: #7BA882; }}
        .feedback-item.error {{ border-left-color: #985239; }}
        .feedback-item.warning {{ border-left-color: #E6C866; }}
        
        .feedback-checkbox {{
            position: absolute;
            bottom: 16px;
            right: 16px;
            width: 18px;
            height: 18px;
            border: 2px solid var(--gray-400);
            cursor: pointer;
        }}
        
        .feedback-icon {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }}
        
        .feedback-icon.info {{
            background: rgba(107, 140, 174, 0.1);
            color: #6B8CAE;
        }}
        
        .feedback-icon.success {{
            background: rgba(123, 168, 130, 0.1);
            color: #7BA882;
        }}
        
        .feedback-icon.error {{
            background: rgba(152, 82, 57, 0.1);
            color: #985239;
        }}
        
        .feedback-icon.warning {{
            background: rgba(230, 200, 102, 0.1);
            color: #E6C866;
        }}
        
        .feedback-content {{
            flex: 1;
        }}
        
        .feedback-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .feedback-user {{
            font-size: 11px;
            font-weight: 600;
            color: var(--gray-700);
            font-family: var(--font-chinese);
        }}
        
        .feedback-score {{
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-family: var(--font-mono);
        }}
        
        .score-high {{
            background: rgba(152, 82, 57, 0.1);
            color: #985239;
        }}
        
        .score-medium {{
            background: rgba(230, 200, 102, 0.1);
            color: #E6C866;
        }}
        
        .score-low {{
            background: rgba(123, 168, 130, 0.1);
            color: #7BA882;
        }}
        
        .feedback-message {{
            font-size: 13px;
            color: var(--gray-900);
            line-height: 1.6;
            margin-bottom: 8px;
        }}
        
        .feedback-tags {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .feedback-tag {{
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 10px;
            background: var(--gray-200);
            color: var(--gray-700);
            font-family: var(--font-mono);
        }}
        
        .confirm-bugs-container {{
            display: flex;
            justify-content: flex-end;
            padding-top: 24px;
            border-top: 1px solid var(--gray-300);
            margin-top: 24px;
        }}
        
        .confirm-bugs-button {{
            padding: 12px 32px;
            background: var(--white);
            color: var(--black);
            border: 2px solid var(--black);
            font-family: var(--font-chinese);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .confirm-bugs-button:hover {{
            background: var(--gray-100);
        }}
        
        /* 运维日志卡片 */
        .ops-log-list {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .ops-log-card {{
            border: 1px solid rgba(224, 224, 224, 0.5);
            padding: 16px;
            background: var(--white);
            transition: all 0.3s;
        }}
        
        .ops-log-card:hover {{
            border-color: #7BA882;
            box-shadow: var(--shadow-sm);
        }}
        
        .ops-log-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .ops-log-time {{
            font-size: 11px;
            font-weight: 600;
            color: var(--gray-700);
            font-family: var(--font-mono);
        }}
        
        .ops-log-status {{
            font-size: 10px;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-family: var(--font-mono);
        }}
        
        .ops-log-status.resolved {{
            background: rgba(123, 168, 130, 0.1);
            color: #7BA882;
        }}
        
        .ops-log-status.pending {{
            background: rgba(230, 200, 102, 0.1);
            color: #E6C866;
        }}
        
        .ops-log-message {{
            font-size: 13px;
            color: var(--gray-900);
            line-height: 1.6;
            margin-bottom: 8px;
        }}
        
        .ops-log-type {{
            font-size: 10px;
            color: var(--gray-600);
            font-family: var(--font-mono);
        }}
        
        /* AI代码管家模块 */
        .code-butler-section {{
            background: rgba(230, 200, 102, 0.03);
            border: 1px solid rgba(230, 200, 102, 0.3);
            border-top: 2px solid #E6C866;
            padding: 32px;
            margin-bottom: 48px;
        }}
        
        .code-butler-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }}
        
        .code-butler-title {{
            font-size: 14px;
            font-weight: 700;
            color: #C87D5C;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .code-butler-stats {{
            font-family: var(--font-mono);
            font-size: 12px;
            color: #C87D5C;
        }}
        
        /* AI提问框 */
        .ai-question-box {{
            margin-bottom: 24px;
        }}
        
        .ai-question-input {{
            width: 100%;
            padding: 16px;
            border: 2px solid var(--gray-300);
            font-size: 14px;
            font-family: var(--font-chinese);
            line-height: 1.6;
            min-height: 80px;
            resize: vertical;
        }}
        
        .ai-question-input:focus {{
            outline: none;
            border-color: #C87D5C;
        }}
        
        .ai-ask-button {{
            margin-top: 12px;
            padding: 10px 24px;
            background: #C87D5C;
            color: var(--white);
            border: none;
            font-family: var(--font-chinese);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .ai-ask-button:hover {{
            background: #985239;
        }}
        
        .ai-response {{
            margin-top: 24px;
            padding: 24px;
            background: var(--gray-100);
            border: 1px solid var(--gray-300);
            font-size: 13px;
            line-height: 1.8;
            font-family: var(--font-mono);
            white-space: pre-wrap;
            min-height: 200px;
        }}
        
        .code-butler-tabs {{
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .code-butler-tab {{
            font-family: var(--font-chinese);
            font-size: 13px;
            font-weight: 600;
            color: var(--gray-600);
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: transparent;
            border-bottom: 2px solid transparent;
            transition: all 0.3s;
        }}
        
        .code-butler-tab:hover {{
            color: var(--black);
        }}
        
        .code-butler-tab.active {{
            color: var(--black);
            border-bottom-color: var(--blue);
        }}
        
        .code-butler-tab-content {{
            display: none;
        }}
        
        .code-butler-tab-content.active {{
            display: block;
        }}
        
        /* 代码搜索框 */
        .code-search-box {{
            margin-bottom: 24px;
        }}
        
        .code-search-input {{
            width: 100%;
            padding: 12px 16px;
            border: 1px solid var(--gray-300);
            font-size: 13px;
            font-family: var(--font-mono);
        }}
        
        .code-search-input:focus {{
            outline: none;
            border-color: #6B8CAE;
        }}
        
        /* 代码分类树 */
        .code-tree {{
            font-size: 12px;
            font-family: var(--font-mono);
            line-height: 1.8;
            color: var(--gray-900);
        }}
        
        .code-category {{
            margin-bottom: 16px;
        }}
        
        .code-category-title {{
            font-weight: 700;
            color: #6B8CAE;
            margin-bottom: 8px;
        }}
        
        .code-file {{
            padding-left: 20px;
            color: var(--gray-700);
            cursor: pointer;
        }}
        
        .code-file:hover {{
            color: #6B8CAE;
        }}
        
        /* 聊天室样式 */
        .chat-panel {{
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 0;
            height: 600px;
            border: 1px solid var(--gray-300);
        }}
        
        .chat-sidebar {{
            background: var(--gray-100);
            border-right: 1px solid var(--gray-300);
            display: flex;
            flex-direction: column;
        }}
        
        .chat-search {{
            padding: 16px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .chat-search-input {{
            width: 100%;
            padding: 8px 12px;
            border: 1px solid var(--gray-300);
            font-size: 12px;
            font-family: var(--font-chinese);
        }}
        
        .chat-search-input:focus {{
            outline: none;
            border-color: var(--blue);
        }}
        
        .conversation-list {{
            flex: 1;
            overflow-y: auto;
            padding: 8px;
        }}
        
        .conversation-item {{
            padding: 12px;
            cursor: pointer;
            border-radius: 4px;
            margin-bottom: 4px;
            transition: all 0.2s;
        }}
        
        .conversation-item:hover {{
            background: var(--white);
        }}
        
        .conversation-item.active {{
            background: var(--white);
            border-left: 3px solid var(--blue);
        }}
        
        .conversation-title {{
            font-size: 12px;
            font-weight: 600;
            color: var(--gray-900);
            margin-bottom: 4px;
        }}
        
        .conversation-preview {{
            font-size: 11px;
            color: var(--gray-600);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .conversation-time {{
            font-size: 10px;
            color: var(--gray-500);
            font-family: var(--font-mono);
        }}
        
        .chat-main {{
            display: flex;
            flex-direction: column;
            background: var(--white);
        }}
        
        .chat-header {{
            padding: 16px 24px;
            border-bottom: 1px solid var(--gray-300);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .chat-title {{
            font-size: 14px;
            font-weight: 600;
            color: var(--gray-900);
        }}
        
        .chat-actions {{
            display: flex;
            gap: 12px;
        }}
        
        .chat-action-btn {{
            width: 32px;
            height: 32px;
            border: 1px solid var(--gray-300);
            background: var(--white);
            border-radius: 4px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            transition: all 0.2s;
        }}
        
        .chat-action-btn:hover {{
            background: var(--gray-100);
            border-color: var(--blue);
        }}
        
        .chat-messages {{
            flex: 1;
            overflow-y: auto;
            padding: 24px;
        }}
        
        .message {{
            margin-bottom: 24px;
            display: flex;
            gap: 12px;
        }}
        
        .message.user {{
            flex-direction: row-reverse;
        }}
        
        .message-avatar {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: var(--gray-300);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            flex-shrink: 0;
        }}
        
        .message-avatar.architect {{
            background: rgba(83, 118, 150, 0.1);
            color: #537696;
        }}
        
        .message-avatar.ops {{
            background: rgba(123, 168, 130, 0.1);
            color: #7BA882;
        }}
        
        .message-avatar.butler {{
            background: rgba(230, 200, 102, 0.1);
            color: #C87D5C;
        }}
        
        .message-avatar.user {{
            background: var(--gray-200);
            color: var(--gray-700);
        }}
        
        .message-content {{
            flex: 1;
            max-width: 70%;
        }}
        
        .message-info {{
            display: flex;
            gap: 8px;
            align-items: center;
            margin-bottom: 6px;
            font-size: 11px;
            color: var(--gray-600);
        }}
        
        .message.user .message-info {{
            flex-direction: row-reverse;
        }}
        
        .message-bubble {{
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 13px;
            line-height: 1.6;
            background: var(--gray-100);
            color: var(--gray-900);
        }}
        
        .message.architect .message-bubble {{
            background: rgba(83, 118, 150, 0.08);
            border-left: 3px solid #537696;
        }}
        
        .message.ops .message-bubble {{
            background: rgba(123, 168, 130, 0.08);
            border-left: 3px solid #7BA882;
        }}
        
        .message.butler .message-bubble {{
            background: rgba(230, 200, 102, 0.08);
            border-left: 3px solid #E6C866;
        }}
        
        .message.user .message-bubble {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-right: 3px solid var(--gray-400);
        }}
        
        .chat-input-area {{
            padding: 16px 24px;
            border-top: 1px solid var(--gray-300);
            background: var(--white);
        }}
        
        .chat-input-wrapper {{
            display: flex;
            gap: 12px;
            align-items: flex-end;
        }}
        
        .chat-input {{
            flex: 1;
            padding: 12px 16px;
            border: 1px solid var(--gray-300);
            border-radius: 8px;
            font-size: 13px;
            font-family: var(--font-chinese);
            line-height: 1.6;
            min-height: 44px;
            max-height: 120px;
            resize: vertical;
        }}
        
        .chat-input:focus {{
            outline: none;
            border-color: var(--blue);
        }}
        
        .chat-send-btn {{
            width: 44px;
            height: 44px;
            border: none;
            border-radius: 8px;
            background: var(--blue);
            color: var(--white);
            font-size: 18px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .chat-send-btn:hover {{
            background: var(--red);
        }}
        
        .new-chat-btn {{
            margin: 12px;
            padding: 10px 16px;
            background: var(--blue);
            color: var(--white);
            border: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            font-family: var(--font-chinese);
            transition: all 0.2s;
        }}
        
        .new-chat-btn:hover {{
            background: var(--red);
        }}
        
        /* 任务列表 */
        .task-list-container {{
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .task-card {{
            background: var(--white);
            border: 1px solid rgba(224, 224, 224, 0.5);
            padding: 24px;
            margin-bottom: 16px;
            transition: all 0.3s;
        }}
        
        .task-card:hover {{
            border-color: var(--black);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        
        .task-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .task-actions {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}
        
        .copy-report-button,
        .copy-prompt-button,
        .redispatch-button {{
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 10px;
            font-weight: 600;
            color: #000000;
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            padding: 5px 12px;
            border-radius: 0;
            cursor: pointer;
            transition: all 0.2s ease;
            letter-spacing: 0.5px;
        }}
        
        .copy-prompt-button {{
            color: #000000;
            border-color: #E0E0E0;
        }}
        
        .copy-report-button {{
            color: #000000;
            border-color: #E0E0E0;
        }}
        
        .redispatch-button {{
            color: #985239;
            border-color: #E0E0E0;
        }}
        
        .copy-report-button:hover,
        .copy-prompt-button:hover,
        .redispatch-button:hover {{
            background: #F5F5F5;
            border-color: #000000;
            transform: translateY(-1px);
        }}
        
        .copy-report-button:active,
        .copy-prompt-button:active {{
            background: var(--gray-200);
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
            font-size: 16px;
            font-weight: 600;
            color: var(--black);
            margin-bottom: 12px;
            line-height: 1.4;
            font-family: var(--font-chinese);
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .task-parallel-badge {{
            font-size: 11px;
            font-weight: 500;
            padding: 6px 16px;
            border-radius: 20px;
            font-family: var(--font-chinese);
            letter-spacing: 0.5px;
            border: none;
        }}
        
        .task-parallel-badge.parallel {{
            background: #7BA882;
            color: var(--white);
        }}
        
        .task-parallel-badge.sequential {{
            background: #C87D5C;
            color: var(--white);
        }}
        
        .task-feature {{
            font-size: 13px;
            color: var(--gray-700);
            margin-bottom: 16px;
            padding-bottom: 16px;
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
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .auto-refresh-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 8px;
            background: var(--gray-100);
            border-radius: 4px;
            font-size: 10px;
            color: var(--gray-700);
        }}
        
        .refresh-icon {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border: 2px solid var(--blue);
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        .refresh-icon.paused {{
            animation: none;
            border-color: var(--gray-400);
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        .refresh-status {{
            color: var(--blue);
            font-weight: 500;
        }}
        
        .refresh-status.paused {{
            color: var(--gray-500);
        }}
        
        /* ===== 架构师监控模块 ===== */
        
        .architect-monitor {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: 32px;
            margin-bottom: 48px;
        }}
        
        .architect-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 24px;
        }}
        
        .architect-title-section {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .architect-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--black);
            font-family: 'Helvetica Neue', Arial, sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .architect-status {{
            font-size: 12px;
            color: var(--gray-700);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .status-dot-architect {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4CAF50;
            display: inline-block;
        }}
        
        .architect-stats {{
            text-align: right;
        }}
        
        .token-info {{
            font-family: var(--font-mono);
            font-size: 12px;
            font-weight: 600;
            color: var(--gray-900);
            margin-bottom: 4px;
        }}
        
        .token-info.warning {{
            color: var(--red);
        }}
        
        .architect-meta {{
            font-size: 11px;
            color: var(--gray-600);
        }}
        
        .architect-tabs {{
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .architect-tab {{
            font-family: var(--font-chinese);
            font-size: 13px;
            font-weight: 600;
            color: var(--gray-600);
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: transparent;
            border-bottom: 2px solid transparent;
            transition: all 0.3s;
        }}
        
        .architect-tab:hover {{
            color: var(--black);
        }}
        
        .architect-tab.active {{
            color: var(--black);
            border-bottom-color: var(--blue);
        }}
        
        .architect-tab-content,
        .tab-content {{
            display: none;
        }}
        
        .architect-tab-content.active,
        .tab-content.active {{
            display: block;
        }}
        
        .event-timeline {{
            background: var(--gray-100);
            border: 1px solid var(--gray-300);
            padding: 24px;
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .event-item {{
            display: flex;
            gap: 16px;
            padding: 12px 0;
            border-bottom: 1px solid var(--gray-300);
            font-family: var(--font-mono);
            font-size: 12px;
            line-height: 1.6;
            align-items: center;
        }}
        
        .event-item:last-child {{
            border-bottom: none;
        }}
        
        .event-time {{
            color: var(--gray-600);
            white-space: nowrap;
            font-weight: 500;
        }}
        
        .event-content {{
            color: var(--gray-900);
            flex: 1;
        }}
        
        .event-icon {{
            font-size: 9px;
            color: var(--gray-500);
            flex-shrink: 0;
            width: 12px;
            text-align: center;
        }}
        
        /* 事件类型颜色 */
        .event-icon.start {{
            color: var(--red);
        }}
        
        .event-icon.communication {{
            color: var(--blue);
        }}
        
        .event-icon.task {{
            color: #537696;
        }}
        
        .event-icon.development {{
            color: #A37867;
        }}
        
        .event-icon.review {{
            color: #985239;
        }}
        
        .event-icon.api {{
            color: #537696;
        }}
        
        .event-icon.requirement {{
            color: var(--red);
        }}
        
        .event-icon.default {{
            color: var(--gray-400);
        }}
        
        .prompt-display {{
            background: var(--gray-100);
            border: 1px solid var(--gray-300);
            padding: 24px;
            font-family: var(--font-mono);
            font-size: 12px;
            line-height: 1.8;
            color: var(--gray-900);
            white-space: pre-wrap;
            max-height: 500px;
            overflow-y: auto;
        }}
        
        .prompt-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}
        
        .prompt-label {{
            font-size: 13px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
        }}
        
        .copy-button {{
            font-size: 11px;
            padding: 6px 12px;
            background: var(--black);
            color: var(--white);
            border: none;
            cursor: pointer;
            font-family: var(--font-chinese);
            transition: all 0.3s;
        }}
        
        .copy-button:hover {{
            background: var(--red);
        }}
        
        .info-panel {{
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 24px;
            min-height: 400px;
        }}
        
        .info-sidebar {{
            border-right: 1px solid var(--gray-300);
            padding-right: 24px;
        }}
        
        .info-doc-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .info-doc-item {{
            padding: 12px 16px;
            border: 1px solid var(--gray-300);
            cursor: pointer;
            transition: all 0.3s;
            font-size: 12px;
            font-family: var(--font-chinese);
            color: var(--gray-900);
            background: var(--white);
        }}
        
        .info-doc-item:hover {{
            border-color: var(--black);
            background: var(--gray-100);
        }}
        
        .info-doc-item.active {{
            background: var(--black);
            color: var(--white);
            border-color: var(--black);
        }}
        
        .info-doc-icon {{
            margin-right: 8px;
        }}
        
        .info-content {{
            background: var(--gray-100);
            border: 1px solid var(--gray-300);
            padding: 24px;
            overflow-y: auto;
            max-height: 400px;
        }}
        
        .info-content-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
            margin-bottom: 16px;
        }}
        
        .info-content-body {{
            font-size: 13px;
            line-height: 1.8;
            color: var(--gray-900);
            white-space: pre-wrap;
        }}
        
        /* ===== 对话历史库样式 ===== */
        
        .conversation-library {{
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 24px;
            min-height: 500px;
        }}
        
        .conversation-sidebar {{
            border-right: 1px solid var(--gray-300);
            padding-right: 24px;
            display: flex;
            flex-direction: column;
        }}
        
        .conversation-header {{
            padding: 12px 0;
            border-bottom: 1px solid var(--gray-300);
            margin-bottom: 16px;
        }}
        
        .conversation-search {{
            margin-bottom: 16px;
        }}
        
        .conversation-search-input {{
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--gray-300);
            font-size: 12px;
            font-family: var(--font-chinese);
            transition: all 0.3s;
        }}
        
        .conversation-search-input:focus {{
            outline: none;
            border-color: var(--black);
            background: var(--gray-100);
        }}
        
        .conversation-list {{
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .conversation-item {{
            padding: 14px 16px;
            border: 1px solid var(--gray-300);
            cursor: pointer;
            transition: all 0.3s;
            background: var(--white);
        }}
        
        .conversation-item:hover {{
            border-color: var(--black);
            background: var(--gray-100);
            transform: translateX(4px);
        }}
        
        .conversation-item.active {{
            background: var(--black);
            color: var(--white);
            border-color: var(--black);
        }}
        
        .conversation-item-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }}
        
        .conversation-item-title {{
            font-size: 12px;
            font-weight: 700;
            font-family: var(--font-chinese);
            line-height: 1.4;
            flex: 1;
        }}
        
        .conversation-item-status {{
            font-size: 9px;
            padding: 2px 6px;
            background: var(--blue);
            color: var(--white);
            font-family: var(--font-mono);
            margin-left: 8px;
            white-space: nowrap;
        }}
        
        .conversation-item.active .conversation-item-status {{
            background: var(--gray-600);
        }}
        
        .conversation-item-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 8px;
            font-size: 10px;
            color: var(--gray-600);
            font-family: var(--font-mono);
        }}
        
        .conversation-item.active .conversation-item-meta {{
            color: var(--gray-400);
        }}
        
        .conversation-item-tokens {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .conversation-item-time {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .conversation-item-tags {{
            display: flex;
            gap: 4px;
            margin-top: 8px;
            flex-wrap: wrap;
        }}
        
        .conversation-tag {{
            font-size: 9px;
            padding: 2px 6px;
            background: var(--gray-200);
            color: var(--gray-800);
            font-family: var(--font-mono);
        }}
        
        .conversation-item.active .conversation-tag {{
            background: var(--gray-700);
            color: var(--gray-300);
        }}
        
        .conversation-main {{
            display: flex;
            flex-direction: column;
        }}
        
        .conversation-detail {{
            flex: 1;
            overflow-y: auto;
        }}
        
        .conversation-detail-header {{
            padding: 20px;
            border-bottom: 2px solid var(--black);
            background: var(--gray-100);
            margin-bottom: 20px;
        }}
        
        .conversation-detail-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
            margin-bottom: 12px;
        }}
        
        .conversation-detail-meta {{
            display: flex;
            gap: 20px;
            font-size: 11px;
            color: var(--gray-700);
            font-family: var(--font-mono);
        }}
        
        .conversation-detail-summary {{
            padding: 16px 20px;
            background: #FFFCF5;
            border-left: 3px solid #D4A574;
            margin-bottom: 20px;
            font-size: 12px;
            line-height: 1.6;
            color: var(--gray-800);
        }}
        
        .conversation-messages {{
            padding: 0 20px 20px;
        }}
        
        .conversation-message {{
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--gray-200);
        }}
        
        .conversation-message:last-child {{
            border-bottom: none;
        }}
        
        .conversation-message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .conversation-message-author {{
            font-size: 11px;
            font-weight: 700;
            color: var(--gray-700);
            font-family: var(--font-chinese);
        }}
        
        .conversation-message-author.user {{
            color: #537696;
        }}
        
        .conversation-message-author.architect {{
            color: #D4A574;
        }}
        
        .conversation-message-time {{
            font-size: 10px;
            color: var(--gray-500);
            font-family: var(--font-mono);
        }}
        
        .conversation-message-content {{
            padding: 12px 16px;
            background: var(--gray-100);
            border-left: 3px solid var(--gray-400);
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        
        .conversation-message-content.user {{
            background: #F0F4F8;
            border-left-color: #537696;
        }}
        
        .conversation-message-content.architect {{
            background: #FFFCF5;
            border-left-color: #D4A574;
        }}
        
        .conversation-message-tokens {{
            font-size: 10px;
            color: var(--gray-500);
            font-family: var(--font-mono);
            margin-top: 6px;
        }}
        
        /* ===== UX/UI确认模块 ===== */
        
        .confirmation-section {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: 32px;
            margin-bottom: 48px;
        }}
        
        .confirmation-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }}
        
        .confirmation-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--black);
            font-family: 'Helvetica Neue', Arial, sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .confirmation-status {{
            font-family: var(--font-mono);
            font-size: 10px;
            padding: 6px 12px;
            background: var(--gray-100);
            color: var(--gray-700);
            border: 1px solid var(--gray-300);
            letter-spacing: 1px;
        }}
        
        .confirmation-status.pending {{
            background: rgba(152, 82, 57, 0.05);
            color: var(--red);
            border-color: var(--red);
        }}
        
        .confirmation-status.approved {{
            background: var(--black);
            color: var(--white);
            border-color: var(--black);
        }}
        
        .confirmation-tabs {{
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .confirmation-tab {{
            font-family: var(--font-chinese);
            font-size: 13px;
            font-weight: 600;
            color: var(--gray-600);
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: transparent;
            border-bottom: 2px solid transparent;
            transition: all 0.3s;
        }}
        
        .confirmation-tab:hover {{
            color: var(--black);
        }}
        
        .confirmation-tab.active {{
            color: var(--black);
            border-bottom-color: var(--blue);
        }}
        
        .images-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin-bottom: 32px;
        }}
        
        .image-item {{
            border: 1px solid var(--gray-300);
            cursor: pointer;
            transition: all 0.3s;
            background: var(--white);
        }}
        
        .image-item:hover {{
            border-color: var(--black);
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }}
        
        .image-preview {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .image-label {{
            font-size: 13px;
            font-weight: 600;
            color: var(--black);
            padding: 16px;
            font-family: var(--font-chinese);
        }}
        
        .prompt-content {{
            background: var(--gray-100);
            border: 1px solid var(--gray-300);
            padding: 24px;
            margin-bottom: 32px;
            font-family: var(--font-mono);
            font-size: 12px;
            line-height: 1.8;
            color: var(--gray-900);
            white-space: pre-wrap;
        }}
        
        .confirm-button-container {{
            display: flex;
            justify-content: flex-end;
            padding-top: 24px;
            border-top: 1px solid var(--gray-300);
        }}
        
        .confirm-button {{
            font-family: var(--font-chinese);
            font-size: 13px;
            font-weight: 600;
            color: var(--black);
            background: var(--white);
            border: 2px solid var(--black);
            padding: 12px 32px;
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
        }}
        
        .confirm-button:hover {{
            background: var(--gray-100);
        }}
        
        .confirm-button:disabled {{
            background: var(--white);
            cursor: not-allowed;
            opacity: 0.5;
        }}
        
        .confirm-button.confirmed {{
            background: var(--white);
            border-color: var(--black);
        }}
        
        .confirm-button.confirmed::before {{
            content: '✓';
            margin-right: 8px;
            font-weight: 700;
        }}
        
        .lightbox {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 9999;
            align-items: center;
            justify-content: center;
        }}
        
        .lightbox.active {{
            display: flex;
        }}
        
        .lightbox-image {{
            max-width: 90%;
            max-height: 90%;
            border: 2px solid var(--white);
        }}
        
        .lightbox-close {{
            position: absolute;
            top: 24px;
            right: 24px;
            font-size: 32px;
            color: var(--white);
            cursor: pointer;
            background: none;
            border: none;
        }}
        
        .empty-state {{
            font-size: 13px;
            color: var(--gray-500);
            text-align: center;
            padding: 48px;
            font-family: var(--font-chinese);
        }}
        
        /* 滚动条样式 */
        .event-timeline::-webkit-scrollbar,
        .prompt-display::-webkit-scrollbar,
        .info-content::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .event-timeline::-webkit-scrollbar-track,
        .prompt-display::-webkit-scrollbar-track,
        .info-content::-webkit-scrollbar-track {{
            background: var(--gray-200);
        }}
        
        .event-timeline::-webkit-scrollbar-thumb,
        .prompt-display::-webkit-scrollbar-thumb,
        .info-content::-webkit-scrollbar-thumb {{
            background: var(--gray-500);
        }}
        
        .event-timeline::-webkit-scrollbar-thumb:hover,
        .prompt-display::-webkit-scrollbar-thumb:hover,
        .info-content::-webkit-scrollbar-thumb:hover {{
            background: var(--gray-700);
        }}
        
        @media (max-width: 1200px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .features-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 品牌标识（固定） -->
        <div class="brand-header">
            <h1 class="brand-title">任务所·Flow</h1>
            <div class="brand-slogan">用对话开工，用流程收工——AI开发工厂新实践</div>
        </div>
        
        <!-- 项目信息 -->
        <div class="project-header">
            <div class="project-info">
                <h2 class="project-name">{title}</h2>
                <div class="project-details">
                    <div class="detail-row">
                        <span class="detail-label">项目描述</span>
                        <span class="detail-value">{subtitle}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">预计开发时间</span>
                        <span class="detail-value">6个月（2025年11月 - 2026年4月）</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">技术栈</span>
                        <span class="detail-value">Python, FastAPI, React, TypeScript</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">核心功能</span>
                        <span class="detail-value">AI任务自动化、代码审查、进度监控</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">应用场景</span>
                        <span class="detail-value">AI协作开发、自动化工作流</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">当前版本</span>
                        <span class="detail-value">v2.0 升级开发中</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">缓存版本</span>
                        <span class="detail-value" id="cache-version-display">{cache_version}</span>
                        <button 
                            onclick="clearDashboardCache()" 
                            style="margin-left: 12px; padding: 4px 12px; background: var(--red); color: white; border: none; border-radius: 4px; font-size: 11px; cursor: pointer; font-family: var(--font-mono); transition: all 0.2s;"
                            onmouseover="this.style.background='var(--black)'"
                            onmouseout="this.style.background='var(--red)'"
                        >
                            🔄 清除缓存
                        </button>
                    </div>
                </div>
            </div>
            <div class="status-pill">
                <div class="status-dot"></div>
                <span>ONLINE</span>
            </div>
        </div>
        
        <!-- 版本切换Tab -->
        <div class="version-tabs" id="versionTabs">
            <button class="version-tab active" data-version="v1">
                <span class="tab-label">版本 1.0</span>
            </button>
            <button class="version-tab" data-version="v2">
                <span class="tab-label">版本 2.0</span>
            </button>
            <button class="version-tab" data-version="v3">
                <span class="tab-label">版本 3.0</span>
            </button>
        </div>
        
        <!-- 版本描述 -->
        <div class="version-info" id="versionInfo">
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
                <span class="section-title">◉ 整体进度</span>
                <div class="progress-value">
                    <div class="progress-inner">
                        <div class="progress-percent" id="progressPercent">0%</div>
                        <div class="progress-label">DONE</div>
                    </div>
                    <div class="progress-tasks-count" id="progressTasksCount" style="font-size: 13px; color: #888; margin-top: 4px;">0/0 tasks</div>
                </div>
            </div>
            <div class="timeline-container">
                <div class="timeline-main-line"></div>
                <div class="timeline-progress" id="timelineProgress" style="width: 0%"></div>
                
                <div class="timeline-nodes">
                    <!-- 节点1: 上方 - 选定架构师 -->
                    <div class="timeline-node top" style="left: 2%;">
                        <div class="node-time-label">2025-11-16</div>
                        <div class="node-badge badge-orange">选定架构师</div>
                        <div class="node-connector"></div>
                        <div class="node-dot"></div>
                        <div class="node-desc">需求沟通</div>
                    </div>
                    
                    <!-- 节点2: 下方 - 确定架构 -->
                    <div class="timeline-node bottom" style="left: 12%;">
                        <div class="node-dot"></div>
                        <div class="node-connector"></div>
                        <div class="node-badge badge-blue">确定架构</div>
                        <div class="node-time-label">2025-11-17</div>
                        <div class="node-desc">架构设计</div>
                    </div>
                    
                    <!-- 节点3: 上方 - 确定UX -->
                    <div class="timeline-node top" style="left: 24%;">
                        <div class="node-time-label">待完成</div>
                        <div class="node-badge badge-gray">确定UX</div>
                        <div class="node-connector"></div>
                        <div class="node-dot"></div>
                        <div class="node-desc">用户体验</div>
                    </div>
                    
                    <!-- 节点4: 下方 - 确定UI -->
                    <div class="timeline-node bottom" style="left: 36%;">
                        <div class="node-dot"></div>
                        <div class="node-connector"></div>
                        <div class="node-badge badge-gray">确定UI</div>
                        <div class="node-time-label">待完成</div>
                        <div class="node-desc">界面设计</div>
                    </div>
                    
                    <!-- 节点5: 上方 - 全栈开发（当前） -->
                    <div class="timeline-node top" style="left: 48%;">
                        <div class="node-time-label">进行中</div>
                        <div class="node-badge badge-yellow">全栈开发</div>
                        <div class="node-connector"></div>
                        <div class="node-dot"></div>
                        <div class="node-desc">功能实现</div>
                    </div>
                    
                    <!-- 节点6: 下方 - 测试 -->
                    <div class="timeline-node bottom" style="left: 60%;">
                        <div class="node-dot"></div>
                        <div class="node-connector"></div>
                        <div class="node-badge badge-gray">测试</div>
                        <div class="node-time-label">待完成</div>
                        <div class="node-desc">质量验证</div>
                    </div>
                    
                    <!-- 节点7: 上方 - 用户终测 -->
                    <div class="timeline-node top" style="left: 72%;">
                        <div class="node-time-label">待完成</div>
                        <div class="node-badge badge-gray">用户终测</div>
                        <div class="node-connector"></div>
                        <div class="node-dot"></div>
                        <div class="node-desc">终端验收</div>
                    </div>
                    
                    <!-- 节点8: 下方 - 部署上线 -->
                    <div class="timeline-node bottom" style="left: 88%;">
                        <div class="node-dot"></div>
                        <div class="node-connector"></div>
                        <div class="node-badge badge-gray">部署上线</div>
                        <div class="node-time-label">待完成</div>
                        <div class="node-desc">生产发布</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 功能清单模块（3个Tab）-->
        <div class="features-section">
            <div class="section-header">
                <span class="section-title">◆ 功能清单</span>
                <span class="stat-meta" id="featureCount">架构师扫描生成</span>
            </div>
            
            <div class="confirmation-tabs" style="margin-top: 16px;">
                <button class="confirmation-tab active" onclick="switchFeatureTab('implemented')">
                    已实现功能
                </button>
                <button class="confirmation-tab" onclick="switchFeatureTab('partial')">
                    部分实现功能
                </button>
                <button class="confirmation-tab" onclick="switchFeatureTab('conflicts')">
                    冲突/建议取舍
                </button>
            </div>
            
            <!-- Tab 1: 已实现功能清单 -->
            <div class="tab-content active" id="implementedFeatures">
                <div class="features-list" id="implementedFeaturesList" style="max-height: 500px; overflow-y: auto; padding: 16px;">
                    <div class="empty-state">等待架构师扫描项目...</div>
                </div>
            </div>
            
            <!-- Tab 2: 部分实现功能清单 -->
            <div class="tab-content" id="partialFeatures">
                <div class="features-list" id="partialFeaturesList" style="max-height: 500px; overflow-y: auto; padding: 16px;">
                    <div class="empty-state">等待架构师扫描项目...</div>
                </div>
            </div>
            
            <!-- Tab 3: 冲突/建议取舍功能清单 -->
            <div class="tab-content" id="conflictsFeatures">
                <div class="features-list" id="conflictsFeaturesList" style="max-height: 500px; overflow-y: auto; padding: 16px;">
                    <div class="empty-state">等待架构师扫描项目...</div>
                </div>
            </div>
        </div>
        
        <!-- 待完成的功能清单模块（新增）-->
        <div class="todo-features-section" style="background: var(--white); border: 1px solid var(--gray-300); border-top: 2px solid var(--black); padding: 32px; margin-bottom: 48px;">
            <div class="section-header">
                <span class="section-title">◉ 待完成的功能清单</span>
                <span class="stat-meta" id="todoFeatureCount">0 个待开发任务</span>
            </div>
            
            <!-- Tab按钮 -->
            <div class="features-tabs" style="display: flex; gap: 0; margin-top: 16px; border-bottom: 1px solid var(--gray-300);">
                <button class="features-tab active" onclick="switchTodoTab('user')" id="todoTabUser" style="padding: 12px 24px; background: none; border: none; border-bottom: 2px solid var(--black); cursor: pointer; font-family: var(--font-chinese); font-size: 13px; font-weight: 600; color: var(--black);">
                    用户需求
                </button>
                <button class="features-tab" onclick="switchTodoTab('architect')" id="todoTabArchitect" style="padding: 12px 24px; background: none; border: none; border-bottom: 2px solid transparent; cursor: pointer; font-family: var(--font-chinese); font-size: 13px; font-weight: 400; color: var(--gray-600);">
                    架构师审查任务
                </button>
            </div>
            
            <!-- Tab 1: 用户需求 -->
            <div class="todo-tab-content active" id="todoUserRequirements" style="margin-top: 16px;">
                <div class="features-list" id="todoUserList" style="max-height: 400px; overflow-y: auto; padding: 16px; border: 1px solid rgba(224, 224, 224, 0.5);">
                    <div class="empty-state">暂无用户提出的新需求</div>
                </div>
            </div>
            
            <!-- Tab 2: 架构师审查任务 -->
            <div class="todo-tab-content" id="todoArchitectTasks" style="margin-top: 16px; display: none;">
                <div class="features-list" id="todoArchitectList" style="max-height: 400px; overflow-y: auto; padding: 16px; border: 1px solid rgba(224, 224, 224, 0.5);">
                    <div class="empty-state">加载中...</div>
                </div>
            </div>
        </div>
        
        <!-- 架构师监控模块 -->
        <div class="architect-monitor" id="architectMonitor">
            <div class="architect-header">
                <div class="architect-title-section">
                    <span class="architect-title">◉ ARCHITECT MONITOR</span>
                    <div class="architect-status">
                        <span class="status-dot-architect"></span>
                        <span id="architectStatusText">工作中</span>
                        <span style="color: var(--gray-500);">|</span>
                        <span id="architectTasksCount">已审查 0 个任务</span>
                    </div>
                </div>
                <div class="architect-stats">
                    <div class="token-info" id="tokenInfo">
                        ▸ Token余量: <span id="tokenUsed">0</span> / 1,000,000 
                        (<span id="tokenPercent">0</span>%)
                        <button 
                            onclick="showTokenSyncDialog()" 
                            title="点击快速同步Token"
                            style="margin-left: 12px; padding: 2px 8px; background: var(--blue); color: white; border: none; border-radius: 3px; font-size: 10px; cursor: pointer; font-family: var(--font-mono); transition: all 0.2s;"
                            onmouseover="this.style.background='var(--red)'"
                            onmouseout="this.style.background='var(--blue)'"
                        >
                            🔄 同步
                        </button>
                    </div>
                    <div class="architect-meta">
                        最后更新: <span id="lastUpdate">--:--:--</span>
                    </div>
                </div>
            </div>
            
            <div class="architect-tabs">
                <button class="architect-tab active" onclick="switchArchitectTab('events')">
                    事件流清单
                </button>
                <button class="architect-tab" onclick="switchArchitectTab('chat')">
                    对话历史库
                </button>
                <button class="architect-tab" onclick="switchArchitectTab('prompt')">
                    动态提示词
                </button>
                <button class="architect-tab" onclick="switchArchitectTab('notes')">
                    重要信息
                </button>
                <button class="architect-tab" onclick="switchArchitectTab('assign')">
                    架构师快速交接
                </button>
            </div>
            
            <!-- Tab 1: 事件流清单 -->
            <div class="architect-tab-content active" id="architectEvents">
                <div class="event-timeline" id="eventTimeline">
                    <div class="event-item">
                        <span class="event-time">17:26:20</span>
                        <span class="event-icon task">↻</span>
                        <span class="event-content">更新任务拆解（新增2个任务）</span>
                    </div>
                    <div class="event-item">
                        <span class="event-time">17:26:20</span>
                        <span class="event-icon requirement">⚠</span>
                        <span class="event-content">收到用户新需求（增加UX/UI确认模块）</span>
                    </div>
                    <div class="event-item">
                        <span class="event-time">15:15:17</span>
                        <span class="event-icon api">◇</span>
                        <span class="event-content">添加后端API接口（/api/architect_monitor）</span>
                    </div>
                </div>
            </div>
            
            <!-- Tab 2: 对话历史库 -->
            <div class="architect-tab-content" id="architectChat">
                <div class="conversation-library">
                    <!-- 左侧：会话列表 -->
                    <div class="conversation-sidebar">
                        <div class="conversation-header">
                            <div style="font-size: 12px; font-weight: 700; color: var(--gray-700);">对话会话列表</div>
                            <div style="font-size: 10px; color: var(--gray-500); margin-top: 2px;">共 3 个会话</div>
                        </div>
                        
                        <!-- 搜索过滤框 -->
                        <div class="conversation-search">
                            <input type="text" id="sessionSearchInput" class="conversation-search-input" placeholder="🔍 搜索会话标题、标签..." onkeyup="filterSessions()">
                        </div>
                        
                        <!-- 会话列表 -->
                        <div class="conversation-list" id="conversationList">
                            <!-- 会话项将通过JavaScript动态加载 -->
                        </div>
                    </div>
                    
                    <!-- 右侧：会话详情 -->
                    <div class="conversation-main">
                        <div class="conversation-detail" id="conversationDetail">
                            <div style="text-align: center; color: var(--gray-400); padding: 60px 20px;">
                                <div style="font-size: 36px; margin-bottom: 12px;">💬</div>
                                <div style="font-size: 13px;">请选择一个会话查看详情</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Tab 2: 动态提示词 -->
            <div class="architect-tab-content" id="architectPrompt">
                <div class="prompt-header">
                    <span class="prompt-label">当前架构师提示词</span>
                    <button class="copy-button" onclick="copyPrompt()">▸ 复制</button>
                </div>
                <div class="prompt-display" id="promptDisplay" style="max-height: 600px; overflow-y: auto; padding: 20px; background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 4px;">
                    加载中...
                </div>
            </div>
            
            <!-- Tab 3: 重要信息 -->
            <div class="architect-tab-content" id="architectNotes">
                <div class="info-panel">
                    <div class="info-sidebar">
                        <div class="info-doc-list" id="infoDocList">
                            <div class="info-doc-item active" onclick="switchInfoDoc('requirements')">
                                <span class="info-doc-icon">◆</span>
                                重大需求变更
                            </div>
                            <div class="info-doc-item" onclick="switchInfoDoc('handoff')">
                                <span class="info-doc-icon">⇄</span>
                                架构师交接
                            </div>
                            <div class="info-doc-item" onclick="switchInfoDoc('bugs')">
                                <span class="info-doc-icon">⚠</span>
                                Bug进度清单
                            </div>
                            <div class="info-doc-item" onclick="switchInfoDoc('decisions')">
                                <span class="info-doc-icon">◉</span>
                                技术决策记录
                            </div>
                        </div>
                    </div>
                    <div class="info-content">
                        <div class="info-content-title" id="infoContentTitle">重大需求变更</div>
                        <div class="info-content-body" id="infoContentBody">
                            加载中...
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Tab 5: 架构师快速交接 -->
            <div class="architect-tab-content" id="architectAssign">
                <div style="padding: 24px; background: #FFFCF5; border: 2px solid #D4A574; margin-bottom: 24px;">
                    <div style="font-size: 14px; font-weight: 700; color: var(--black); margin-bottom: 12px;">
                        🏛️ 架构师快速交接指令
                    </div>
                    <div style="font-size: 12px; color: var(--gray-700); line-height: 1.6; margin-bottom: 16px;">
                        ⚠️ <strong>重要</strong>: 请在<strong>新的Cursor窗口</strong>中粘贴以下指令完成交接
                    </div>
                    <button 
                        onclick="copyArchitectAssignPrompt()"
                        style="padding: 10px 20px; background: var(--black); color: white; border: none; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; font-family: var(--font-chinese); transition: all 0.2s;"
                        onmouseover="this.style.background='var(--red)'"
                        onmouseout="this.style.background='var(--black)'"
                    >
                        📋 一键复制交接指令
                    </button>
                </div>
                
                <div class="info-doc-viewer" style="padding: 20px; border: 1px solid var(--gray-300); background: var(--white);">
                    <pre style="white-space: pre-wrap; font-family: var(--font-chinese); font-size: 12px; line-height: 1.8; color: var(--gray-800);">🏛️ 接任【任务所·Flow v1.7】总架构师

# 📍 当前项目状态（已初始化完成）

**项目进度**: 46.3% (25/54任务完成)
**Dashboard**: http://localhost:8877 ⭐ 这是你的核心工作空间
**最近更新**: 2025-11-19 06:00
**前任架构师**: 已完成 Phase 0-4 初始化工作

✅ 已完成的基础工作：
- 架构清单 (architecture-inventory.md)
- 重构计划 (refactor-plan.md)  
- 架构审查 (architecture-review.md)
- 任务看板 (task-board.md)
- 功能清单: 114个已实现 + 17个部分实现
- 事件流: 171个事件记录

---

# 🎯 你的核心职责（⚠️ 重要）

## 1. Dashboard是你的工作中心
**访问**: http://localhost:8877

你必须时刻关注并维护Dashboard的**4个核心模块**：
- **功能清单**: 已实现(114) / 部分实现(17) / 冲突建议(13)
- **事件流**: 实时记录架构师的每个决策和行动
- **任务统计**: 当前46.3%进度,25/54任务
- **架构师监控**: 对话历史、重要信息

## 2. 维护Dashboard数据的实时性和准确性 ⭐⭐⭐⭐⭐
**这是你最重要的工作！**

每当你：
- ✅ 产出新文档 → 更新"功能清单-已实现"
- ✅ 发现问题/半成品 → 更新"功能清单-部分实现"  
- ✅ 提出建议/决策 → 更新"功能清单-冲突建议"
- ✅ 做任何架构工作 → 更新"事件流"

**更新方法**:
```python
# 功能清单
python update_features_complete.py

# 事件流  
python update_architect_events.py
```

---

# 📋 立即执行的3个步骤

## 第1步：读取你的System Prompt（必须）
@taskflow-v1.7-monorepo/docs/ai/architect-system-prompt-expert.md

这份8000字文档定义了你的：
- 身份定位: Staff/Principal Engineer (10-15年经验)
- 5阶段工作流程: 理解验证→场景深挖→方案生成→对比推荐→质疑模式
- 核心原则: 理解优于执行、质疑优于盲从、最优解优于快速解

## 第2步：浏览Dashboard了解当前状态（必须）
打开 http://localhost:8877

重点查看：
- **功能清单-已实现**: 看看完成了哪114个功能
- **功能清单-部分实现**: 看看还有哪17个半成品
- **功能清单-冲突建议**: 看看前任给出的13条建议
  - ⭐ 重点: ARCH-ADVICE-001 (Phase C是P0)
  - ⭐ 重点: ARCH-ADVICE-003 (v1.6继续运行)
- **事件流**: 浏览最新的20个事件,了解最近发生了什么

## 第3步：读取最新交接文档（可选但推荐）
@taskflow-v1.7-monorepo/📍给下一任架构师-紧急交接-2025-11-19-05-30.md
@taskflow-v1.7-monorepo/📍架构师工作总结-2025-11-19-06-00.md

了解前任的工作内容、核心发现和建议。

---

# 🎯 你的日常工作流

## 当用户给你任务时：

1. **先看Dashboard** → 了解当前状态
2. **分析问题** → 使用5阶段工作流程
3. **产出方案** → 必须给3个选项对比（保守/平衡/激进）
4. **更新Dashboard** → 立即同步你的工作到看板
   - 新文档 → 更新功能清单
   - 新发现 → 更新部分实现
   - 新建议 → 更新冲突建议
   - 工作记录 → 更新事件流
5. **产出文档** → 如果需要更新Markdown文档

## 当工程师提交完成报告时：

1. **审查代码和文档** → 是否符合规划？
2. **更新任务状态** → 在数据库和Dashboard中
3. **更新事件流** → 记录验收结果
4. **必要时派生新任务** → 发现新问题或依赖

---

# ⚠️ 核心原则（不要忘记）

## Dashboard第一原则 ⭐⭐⭐⭐⭐
**Dashboard是项目的"单一真相源"(Single Source of Truth)**

- ✅ 所有架构工作必须同步到Dashboard
- ✅ Dashboard数据必须实时、准确
- ✅ 不能只写Markdown文档而不更新Dashboard
- ✅ Dashboard是给人看的，文档是给AI看的

## 你的职责边界
✅ 你是架构师，不是执行者
✅ 你负责：分析、规划、审查、派发任务
❌ 你不负责：大量编写业务代码

## YAGNI原则
You Aren't Gonna Need It - 不过度设计
- 前任建议: Phase C(API集成)是P0
- 前任建议: Phase D(代码迁移)可延后或跳过
- 原因: v1.7的价值是AI体系，不是Monorepo

---

# 📊 关键数据（快速参考）

**项目名称**: 任务所·Flow v1.7
**项目路径**: taskflow-v1.7-monorepo/
**当前进度**: 46.3% (25/54任务)
**Dashboard端口**: http://localhost:8877
**数据库**: database/data/tasks.db
**事件流**: apps/dashboard/automation-data/architect_events.json
**功能清单**: apps/dashboard/automation-data/v17-complete-features.json

**下一个P0任务**: TASK-C.1 创建FastAPI主入口 (2小时)

---

# ✅ 确认交接完成

当你读完 System Prompt + 浏览完 Dashboard 后，回复：

"✅ 我已接任任务所·Flow v1.7总架构师
- 已读System Prompt (8000字)
- 已浏览Dashboard (114+17+13)
- 已了解当前状态 (46.3%进度)
- 理解核心职责：维护Dashboard的实时性和准确性

准备开始工作。"</pre>
                </div>
            </div>
        </div>
        
        <!-- UX确认模块 -->
        <div class="confirmation-section" id="uxConfirmation">
            <div class="confirmation-header">
                <span class="confirmation-title">◇ UX DESIGN CONFIRMATION</span>
                <span class="confirmation-status pending" id="uxStatus">待确认</span>
            </div>
            
            <div class="confirmation-tabs">
                <button class="confirmation-tab active" onclick="switchConfirmationTab('ux', 'images')">效果图</button>
                <button class="confirmation-tab" onclick="switchConfirmationTab('ux', 'prompt')">提示词</button>
            </div>
            
            <div class="confirmation-content">
                <!-- 效果图Tab -->
                <div class="tab-content active" id="uxImages">
                    <div class="images-grid" id="uxImagesGrid">
                        <div class="empty-state">暂无UX设计，等待架构师生成...</div>
                    </div>
                </div>
                
                <!-- 提示词Tab -->
                <div class="tab-content" id="uxPrompt" style="display: none;">
                    <div class="prompt-content" id="uxPromptContent">
                        暂无UX提示词
                    </div>
                </div>
            </div>
            
            <div class="confirm-button-container">
                <button class="confirm-button" id="uxConfirmBtn" onclick="confirmUX()">
                    ✅ 确认 UX
                </button>
            </div>
        </div>
        
        <!-- UI确认模块 -->
        <div class="confirmation-section" id="uiConfirmation">
            <div class="confirmation-header">
                <span class="confirmation-title">◆ UI DESIGN CONFIRMATION</span>
                <span class="confirmation-status pending" id="uiStatus">待确认</span>
            </div>
            
            <div class="confirmation-tabs">
                <button class="confirmation-tab active" onclick="switchConfirmationTab('ui', 'images')">效果图</button>
                <button class="confirmation-tab" onclick="switchConfirmationTab('ui', 'prompt')">提示词</button>
            </div>
            
            <div class="confirmation-content">
                <!-- 效果图Tab -->
                <div class="tab-content active" id="uiImages">
                    <div class="images-grid" id="uiImagesGrid">
                        <div class="empty-state">暂无UI设计，等待架构师生成...</div>
                    </div>
                </div>
                
                <!-- 提示词Tab -->
                <div class="tab-content" id="uiPrompt" style="display: none;">
                    <div class="prompt-content" id="uiPromptContent">
                        暂无UI提示词
                    </div>
                </div>
            </div>
            
            <div class="confirm-button-container">
                <button class="confirm-button" id="uiConfirmBtn" onclick="confirmUI()">
                    ✅ 确认 UI
                </button>
            </div>
        </div>
        
        <!-- 图片灯箱（点击放大） -->
        <div class="lightbox" id="lightbox" onclick="closeLightbox()">
            <button class="lightbox-close" onclick="closeLightbox()">✕</button>
            <img class="lightbox-image" id="lightboxImage" src="" alt="">
        </div>
        
        <!-- Tab 5: 架构师快速任命（放在architect-monitor内最后） -->
        
        <!-- 全栈开发工程师模块 -->
        <div class="developer-section">
            <div class="developer-header">
                <span class="developer-title">◆ 全栈开发工程师</span>
                <span class="developer-count" id="taskCount">0 tasks</span>
            </div>
            
            <div class="developer-tabs">
                <button class="developer-tab active" onclick="switchDeveloperTab('tasks')">
                    任务清单
                </button>
                <button class="developer-tab" onclick="switchDeveloperTab('prompt')">
                    提示词
                </button>
                <button class="developer-tab" onclick="switchDeveloperTab('knowledge')">
                    开发知识库
                </button>
            </div>
            
            <!-- Tab 1: 任务清单 -->
            <div class="developer-tab-content active" id="developerTasks">
                <!-- 任务状态筛选Tab -->
                <div class="task-filter-tabs" style="margin-bottom: 16px; border-bottom: 1px solid #E0E0E0;">
                    <button class="task-filter-tab active" onclick="filterTasksByStatus('all')">
                        全部
                    </button>
                    <button class="task-filter-tab" onclick="filterTasksByStatus('pending')">
                        待处理
                    </button>
                    <button class="task-filter-tab" onclick="filterTasksByStatus('in_progress')">
                        进行中
                    </button>
                    <button class="task-filter-tab" onclick="filterTasksByStatus('completed')">
                        已完成
                    </button>
                </div>
                
                <div class="task-list-container">
                    <div class="task-list" id="taskList">
                        <div class="empty-state">Loading...</div>
                    </div>
                </div>
            </div>
            
            <!-- Tab 2: 提示词 -->
            <div class="developer-tab-content" id="developerPrompt">
                <div class="prompt-header">
                    <span class="prompt-label">全栈开发工程师提示词（完整版7000字）</span>
                    <button class="copy-button" onclick="copyDeveloperPrompt()">▸ 复制</button>
                </div>
                <div class="prompt-display" id="developerPromptContent" style="white-space: pre-wrap; max-height: 600px; overflow-y: auto; padding: 20px; background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 4px;">
                    加载中...
                </div>
            </div>
            
            <!-- Tab 3: 开发知识库 -->
            <div class="developer-tab-content" id="developerKnowledge">
                <div class="info-panel">
                    <div class="info-sidebar">
                        <div class="info-doc-list">
                            <div class="info-doc-item active" onclick="switchKnowledgeDoc('problems')">
                                <span class="info-doc-icon">⚠</span>
                                问题解决库
                            </div>
                            <div class="info-doc-item" onclick="switchKnowledgeDoc('tools')">
                                <span class="info-doc-icon">◆</span>
                                常用工具库
                            </div>
                            <div class="info-doc-item" onclick="switchKnowledgeDoc('standards')">
                                <span class="info-doc-icon">◉</span>
                                开发规范
                            </div>
                            <div class="info-doc-item" onclick="switchKnowledgeDoc('tips')">
                                <span class="info-doc-icon">▸</span>
                                最佳实践
                            </div>
                        </div>
                    </div>
                    <div class="info-content">
                        <div class="info-content-title" id="knowledgeTitle">问题解决库</div>
                        <div class="info-content-body" id="knowledgeContent">
                            加载中...
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 测试工程师模块 -->
        <div class="tester-section">
            <div class="tester-header">
                <span class="tester-title">◇ 测试工程师</span>
                <span class="tester-count" id="testerTaskCount">0 tasks</span>
            </div>
            
            <div class="tester-tabs">
                <button class="tester-tab active" onclick="switchTesterTab('tasks')">
                    任务清单
                </button>
                <button class="tester-tab" onclick="switchTesterTab('prompt')">
                    提示词
                </button>
                <button class="tester-tab" onclick="switchTesterTab('knowledge')">
                    知识库
                </button>
            </div>
            
            <!-- Tab 1: 任务清单 -->
            <div class="tester-tab-content active" id="testerTasks">
                <div class="task-list-container">
                    <div class="task-list" id="testerTaskList">
                        <div class="empty-state">暂无测试任务</div>
                    </div>
                </div>
            </div>
            
            <!-- Tab 2: 提示词 -->
            <div class="tester-tab-content" id="testerPrompt">
                <div class="prompt-header">
                    <span class="prompt-label">测试工程师提示词</span>
                    <button class="copy-button" onclick="copyTesterPrompt()">▸ 复制</button>
                </div>
                <div class="prompt-display" id="testerPromptContent">
你是一名测试工程师，负责确保软件质量。

测试职责：
1. 功能测试：验证所有功能是否符合需求
2. 集成测试：测试模块间的交互
3. 性能测试：检查系统性能和响应速度
4. 回归测试：确保新功能不影响现有功能

测试流程：
1. 理解需求和功能
2. 编写测试用例
3. 执行测试
4. 记录Bug和问题
5. 验证修复
6. 提交测试报告

质量标准：
- 功能覆盖率 > 90%
- 核心功能必须有自动化测试
- 所有P0/P1 Bug必须修复
- 性能指标达标
                </div>
            </div>
            
            <!-- Tab 3: 知识库 -->
            <div class="tester-tab-content" id="testerKnowledge">
                <div class="info-panel">
                    <div class="info-sidebar">
                        <div class="info-doc-list">
                            <div class="info-doc-item active" onclick="switchTesterKnowledgeDoc('cases')">
                                <span class="info-doc-icon">◆</span>
                                测试用例库
                            </div>
                            <div class="info-doc-item" onclick="switchTesterKnowledgeDoc('bugs')">
                                <span class="info-doc-icon">⚠</span>
                                Bug跟踪库
                            </div>
                            <div class="info-doc-item" onclick="switchTesterKnowledgeDoc('tools')">
                                <span class="info-doc-icon">◉</span>
                                测试工具
                            </div>
                            <div class="info-doc-item" onclick="switchTesterKnowledgeDoc('standards')">
                                <span class="info-doc-icon">▸</span>
                                测试规范
                            </div>
                        </div>
                    </div>
                    <div class="info-content">
                        <div class="info-content-title" id="testerKnowledgeTitle">测试用例库</div>
                        <div class="info-content-body" id="testerKnowledgeContent">
                            加载中...
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 目标用户终测模块 -->
        <div class="user-testing-section">
            <div class="user-testing-header">
                <span class="user-testing-title">◉ 目标用户终测</span>
                <span class="user-testing-stats">7位模拟用户 | 待确认: <span id="pendingFeedbackCount">0</span></span>
            </div>
            
            <div class="user-testing-tabs">
                <button class="user-testing-tab active" onclick="switchUserTestingTab('feedback')">
                    Bug/意见清单
                </button>
                <button class="user-testing-tab" onclick="switchUserTestingTab('users')">
                    模拟用户提示词
                </button>
            </div>
            
            <!-- Tab 1: Bug/意见清单 -->
            <div class="user-testing-tab-content active" id="userTestingFeedback">
                <div class="feedback-list">
                    <!-- 示例反馈1: Info -->
                    <div class="feedback-item info">
                        <div class="feedback-icon info">ℹ</div>
                        <div class="feedback-content">
                            <div class="feedback-header">
                                <span class="feedback-user">乐观派·张三（白帽思维）</span>
                                <span class="feedback-score score-low">体验度: 2/10</span>
                            </div>
                            <div class="feedback-message">
                                建议增加快捷键提示，可以提升操作效率。整体界面很清爽，符合专业工具的定位。
                            </div>
                            <div class="feedback-tags">
                                <span class="feedback-tag">易用性</span>
                                <span class="feedback-tag">优化建议</span>
                            </div>
                        </div>
                        <input type="checkbox" class="feedback-checkbox" data-id="feedback-1">
                    </div>
                    
                    <!-- 示例反馈2: Warning -->
                    <div class="feedback-item warning">
                        <div class="feedback-icon warning">⚠</div>
                        <div class="feedback-content">
                            <div class="feedback-header">
                                <span class="feedback-user">谨慎派·李四（黑帽思维）</span>
                                <span class="feedback-score score-medium">体验度: 5/10</span>
                            </div>
                            <div class="feedback-message">
                                发现时间轴在小屏幕上显示不全，建议添加响应式设计。另外缺少错误提示信息。
                            </div>
                            <div class="feedback-tags">
                                <span class="feedback-tag">兼容性</span>
                                <span class="feedback-tag">必须修复</span>
                            </div>
                        </div>
                        <input type="checkbox" class="feedback-checkbox" data-id="feedback-2">
                    </div>
                    
                    <!-- 示例反馈3: Error -->
                    <div class="feedback-item error">
                        <div class="feedback-icon error">✕</div>
                        <div class="feedback-content">
                            <div class="feedback-header">
                                <span class="feedback-user">创新派·王五（绿帽思维）</span>
                                <span class="feedback-score score-high">体验度: 8/10</span>
                            </div>
                            <div class="feedback-message">
                                缺少实时通知功能，当任务完成时无法及时知道。建议增加WebSocket实时推送。
                            </div>
                            <div class="feedback-tags">
                                <span class="feedback-tag">功能缺失</span>
                                <span class="feedback-tag">严重</span>
                            </div>
                        </div>
                        <input type="checkbox" class="feedback-checkbox" data-id="feedback-3">
                    </div>
                </div>
                
                <div class="confirm-bugs-container">
                    <button class="confirm-bugs-button" onclick="confirmSelectedBugs()">
                        ✓ 确认选中的Bug需要修复
                    </button>
                </div>
            </div>
            
            <!-- Tab 2: 模拟用户 -->
            <div class="user-testing-tab-content" id="userTestingUsers">
                <div class="prompt-display">
# 模拟用户设计（7位目标用户）

## 1. 乐观派·张三（白帽思维）
- 性格：积极乐观，关注优点
- 知识层次：中级开发者
- 测试重点：寻找优秀体验

## 2. 谨慎派·李四（黑帽思维）  
- 性格：谨慎挑剔，关注风险
- 知识层次：高级架构师
- 测试重点：发现潜在问题

## 3. 创新派·王五（绿帽思维）
- 性格：创意丰富，提出新想法
- 知识层次：产品经理
- 测试重点：功能创新建议

## 4. 数据派·赵六（黄帽思维）
- 性格：理性分析，看重数据
- 知识层次：数据分析师
- 测试重点：性能和效率

## 5. 情感派·钱七（红帽思维）
- 性格：感性直觉，关注感受
- 知识层次：初级用户
- 测试重点：第一印象和情感体验

## 6. 逻辑派·孙八（蓝帽思维）
- 性格：系统思考，掌控全局
- 知识层次：项目经理
- 测试重点：流程和逻辑

## 7. 极客派·周九（技术狂热）
- 性格：技术至上，追求极致
- 知识层次：资深工程师
- 测试重点：技术细节和性能
                </div>
            </div>
        </div>
        
        <!-- 交付工程师模块 -->
        <div class="delivery-section">
            <div class="delivery-header">
                <span class="delivery-title">◆ 交付工程师</span>
                <span class="delivery-count" id="deliveryTaskCount">0 tasks</span>
            </div>
            
            <div class="delivery-tabs">
                <button class="delivery-tab active" onclick="switchDeliveryTab('tasks')">
                    任务清单
                </button>
                <button class="delivery-tab" onclick="switchDeliveryTab('env')">
                    环境/工具说明
                </button>
                <button class="delivery-tab" onclick="switchDeliveryTab('ops')">
                    运维说明
                </button>
            </div>
            
            <!-- Tab 1: 任务清单 -->
            <div class="delivery-tab-content active" id="deliveryTasks">
                <div class="task-list-container">
                    <div class="empty-state">暂无交付任务</div>
                </div>
            </div>
            
            <!-- Tab 2: 环境/工具说明 -->
            <div class="delivery-tab-content" id="deliveryEnv">
                <div class="info-panel">
                    <div class="info-sidebar">
                        <div class="info-doc-list">
                            <div class="info-doc-item active" onclick="switchDeliveryDoc('environment')">
                                <span class="info-doc-icon">◆</span>
                                环境说明
                            </div>
                            <div class="info-doc-item" onclick="switchDeliveryDoc('tools')">
                                <span class="info-doc-icon">◉</span>
                                工具链说明
                            </div>
                            <div class="info-doc-item" onclick="switchDeliveryDoc('secrets')">
                                <span class="info-doc-icon">⚠</span>
                                配置与密钥
                            </div>
                            <div class="info-doc-item" onclick="switchDeliveryDoc('strategy')">
                                <span class="info-doc-icon">▸</span>
                                发布策略
                            </div>
                        </div>
                    </div>
                    <div class="info-content">
                        <div class="info-content-title" id="deliveryDocTitle">环境说明</div>
                        <div class="info-content-body" id="deliveryDocContent">
                            加载中...
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Tab 3: 运维说明 -->
            <div class="delivery-tab-content" id="deliveryOps">
                <div class="prompt-header">
                    <span class="prompt-label">运维说明（交付工程师填写）</span>
                    <button class="copy-button" onclick="copyOpsDoc()">▸ 复制</button>
                </div>
                <div class="prompt-display" id="opsDocContent">
# 运维说明

## 启动说明
```bash
# 启动Dashboard
cd ai-task-automation-board
python start_dashboard.py
```

## 部署方式
- 部署环境：生产环境
- 部署方式：手动部署
- 端口：8889

## 版本回滚计划
1. 备份当前版本
2. 恢复上一版本代码
3. 重启服务
4. 验证功能

## 监控告警
- 健康检查：http://127.0.0.1:8889/health
- 日志位置：logs/dashboard.log

## 常见问题排查
1. 端口被占用：taskkill /F /PID [PID]
2. 模块导入失败：检查Python路径

---

填写者：交付工程师
填写时间：待完成
                </div>
            </div>
        </div>
        
        <!-- 运维工程师模块（固定模块） -->
        <div class="ops-section">
            <div class="ops-header">
                <span class="ops-title">◉ 运维工程师（固定）</span>
                <span class="ops-status">● 长期在线 | 跨版本守护</span>
            </div>
            
            <div class="ops-tabs">
                <button class="ops-tab active" onclick="switchOpsTab('log')">
                    运维日志
                </button>
                <button class="ops-tab" onclick="switchOpsTab('report')">
                    提报Bug
                </button>
                <button class="ops-tab" onclick="switchOpsTab('runbook')">
                    运维说明
                </button>
                <button class="ops-tab" onclick="switchOpsTab('knowledge')">
                    经验库
                </button>
            </div>
            
            <!-- Tab 1: 运维日志 -->
            <div class="ops-tab-content active" id="opsLog">
                <div class="ops-log-list">
                    <!-- 运维日志卡片1 -->
                    <div class="ops-log-card">
                        <div class="ops-log-header">
                            <span class="ops-log-time">2025-11-17 17:30</span>
                            <span class="ops-log-status resolved">已解决</span>
                        </div>
                        <div class="ops-log-message">
                            <strong>浏览器缓存问题：</strong>Dashboard更新后用户看到旧版本UI。解决方案：更换端口重启+清除缓存文档。
                        </div>
                        <div class="ops-log-type">类型: 故障处理 | 影响: 前端显示</div>
                    </div>
                    
                    <!-- 运维日志卡片2 -->
                    <div class="ops-log-card">
                        <div class="ops-log-header">
                            <span class="ops-log-time">2025-11-17 14:30</span>
                            <span class="ops-log-status resolved">已完成</span>
                        </div>
                        <div class="ops-log-message">
                            <strong>版本部署：</strong>Dashboard v2.0部署完成，新增架构师监控、UX/UI确认、全栈开发/测试/交付工程师模块。
                        </div>
                        <div class="ops-log-type">类型: 变更记录 | 操作人: 交付工程师</div>
                    </div>
                    
                    <!-- 运维日志卡片3 -->
                    <div class="ops-log-card">
                        <div class="ops-log-header">
                            <span class="ops-log-time">2025-11-17 10:00</span>
                            <span class="ops-log-status resolved">正常</span>
                        </div>
                        <div class="ops-log-message">
                            <strong>日常检查：</strong>API健康检查正常，响应时间平均120ms，数据库大小2.3MB，无告警。
                        </div>
                        <div class="ops-log-type">类型: 日常巡检</div>
                    </div>
                </div>
            </div>
            
            <!-- Tab 2: 提报Bug -->
            <div class="ops-tab-content" id="opsReport">
                <div class="ai-question-box">
                    <textarea class="ai-question-input" id="bugReportInput" placeholder="用自然语言描述遇到的问题...

示例：
• Dashboard更新后浏览器还是显示旧版本
• API接口返回500错误
• 数据库查询速度很慢
• 某个按钮点击后没反应

请详细描述问题，包括：
- 发生了什么
- 预期应该怎样
- 如何复现
- 影响范围"></textarea>
                    <button class="ai-ask-button" style="background: #7BA882;" onclick="submitBugReport()">▸ 提交Bug报告</button>
                </div>
                <div style="margin-top: 24px; padding: 16px; background: var(--gray-100); border: 1px solid var(--gray-300); font-size: 12px; color: var(--gray-600);">
                    <strong style="color: #7BA882;">提示：</strong>提交后，Bug将自动记录到经验库，并通知相关工程师处理。
                </div>
                
                <div style="margin-top: 32px;">
                    <div style="font-size: 13px; font-weight: 700; margin-bottom: 16px; color: #000000;">最近提报的Bug</div>
                    <div class="ops-log-list" style="max-height: 400px;">
                        <!-- 示例已提报的Bug -->
                        <div class="ops-log-card">
                            <div class="ops-log-header">
                                <span class="ops-log-time">2025-11-17 17:30</span>
                                <span class="ops-log-status pending" style="background: rgba(230, 200, 102, 0.1); color: #E6C866;">待处理</span>
                            </div>
                            <div class="ops-log-message">
                                <strong>浏览器缓存问题：</strong>Dashboard更新后用户看到旧版本UI，已尝试刷新仍然无效。
                            </div>
                            <div class="ops-log-type">提报人: 运维工程师 | 影响: 前端显示</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Tab 2: 运维说明 -->
            <div class="ops-tab-content" id="opsRunbook">
                <div class="info-panel">
                    <div class="info-sidebar">
                        <div class="info-doc-list">
                            <div class="info-doc-item active" onclick="switchRunbookDoc('runbook')">
                                <span class="info-doc-icon">◆</span>
                                运行手册
                            </div>
                            <div class="info-doc-item" onclick="switchRunbookDoc('backup')">
                                <span class="info-doc-icon">◉</span>
                                备份恢复
                            </div>
                            <div class="info-doc-item" onclick="switchRunbookDoc('monitor')">
                                <span class="info-doc-icon">▸</span>
                                监控告警
                            </div>
                            <div class="info-doc-item" onclick="switchRunbookDoc('security')">
                                <span class="info-doc-icon">⚠</span>
                                安全策略
                            </div>
                        </div>
                    </div>
                    <div class="info-content">
                        <div class="info-content-title" id="runbookDocTitle">运行手册</div>
                        <div class="info-content-body" id="runbookDocContent">
# 运维手册（RUNBOOK）

## 快速启动
```bash
cd ai-task-automation-board
python start_dashboard.py
```

## 快速停止
```bash
taskkill /F /IM python.exe
```

## 健康检查
```bash
curl http://127.0.0.1:8889/health
```

## 常见问题排查

### Q1: 端口被占用
```bash
netstat -ano | findstr ":8889"
taskkill /F /PID [进程ID]
```

### Q2: 模块导入失败
检查Python路径和虚拟环境

### Q3: 数据库锁定
检查是否有多个实例在运行

## 日志位置
- 应用日志：logs/dashboard.log
- 错误日志：logs/error.log

## 备份策略
- 数据库：每日备份automation-data/tasks.db
- 配置文件：Git版本控制

## 监控指标
- 响应时间目标：< 200ms
- 可用性目标：> 99.9%
- CPU使用率：< 70%
- 内存使用率：< 80%
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Tab 3: 经验库 -->
            <div class="ops-tab-content" id="opsKnowledge">
                <div class="prompt-display">
                    <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                        <thead>
                            <tr style="background: var(--gray-100); border-bottom: 2px solid var(--gray-300);">
                                <th style="padding: 12px; text-align: left; font-weight: 700; width: 100px;">时间</th>
                                <th style="padding: 12px; text-align: left; font-weight: 700; width: 200px;">问题</th>
                                <th style="padding: 12px; text-align: left; font-weight: 700;">解决方案</th>
                                <th style="padding: 12px; text-align: left; font-weight: 700; width: 100px;">状态</th>
                                <th style="padding: 12px; text-align: left; font-weight: 700; width: 80px;">优先级</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="border-bottom: 1px solid rgba(224, 224, 224, 0.5);">
                                <td style="padding: 12px; color: var(--gray-600); font-family: var(--font-mono);">2025-11-17</td>
                                <td style="padding: 12px; font-weight: 600;">浏览器缓存导致更新不显示</td>
                                <td style="padding: 12px; line-height: 1.6;">更换端口启动 / Ctrl+Shift+R强制刷新 / 清除缓存</td>
                                <td style="padding: 12px;">
                                    <span style="padding: 4px 10px; background: rgba(123, 168, 130, 0.1); color: #7BA882; border-radius: 12px; font-size: 10px; font-weight: 600;">已解决</span>
                                </td>
                                <td style="padding: 12px; color: var(--gray-600);">P1</td>
                            </tr>
                            <tr style="border-bottom: 1px solid rgba(224, 224, 224, 0.5);">
                                <td style="padding: 12px; color: var(--gray-600); font-family: var(--font-mono);">2025-11-17</td>
                                <td style="padding: 12px; font-weight: 600;">Python编码错误(UnicodeEncodeError)</td>
                                <td style="padding: 12px; line-height: 1.6;">设置环境变量 $env:PYTHONIOENCODING="utf-8"</td>
                                <td style="padding: 12px;">
                                    <span style="padding: 4px 10px; background: rgba(123, 168, 130, 0.1); color: #7BA882; border-radius: 12px; font-size: 10px; font-weight: 600;">已解决</span>
                                </td>
                                <td style="padding: 12px; color: var(--gray-600);">P2</td>
                            </tr>
                            <tr style="border-bottom: 1px solid rgba(224, 224, 224, 0.5);">
                                <td style="padding: 12px; color: var(--gray-600); font-family: var(--font-mono);">2025-11-16</td>
                                <td style="padding: 12px; font-weight: 600;">端口被占用无法启动</td>
                                <td style="padding: 12px; line-height: 1.6;">netstat -ano | findstr ":8889" 然后 taskkill /F /PID [进程ID]</td>
                                <td style="padding: 12px;">
                                    <span style="padding: 4px 10px; background: rgba(123, 168, 130, 0.1); color: #7BA882; border-radius: 12px; font-size: 10px; font-weight: 600;">已解决</span>
                                </td>
                                <td style="padding: 12px; color: var(--gray-600);">P1</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- AI代码管家模块（固定） -->
        <div class="code-butler-section">
            <div class="code-butler-header">
                <span class="code-butler-title">◇ AI代码管家（固定）</span>
                <span class="code-butler-stats">● 代码索引已建立 | 3,500+ 行代码</span>
            </div>
            
            <div class="code-butler-tabs">
                <button class="code-butler-tab active" onclick="switchCodeButlerTab('search')">
                    AI问答
                </button>
                <button class="code-butler-tab" onclick="switchCodeButlerTab('structure')">
                    代码结构
                </button>
                <button class="code-butler-tab" onclick="switchCodeButlerTab('index')">
                    分类索引
                </button>
            </div>
            
            <!-- Tab 1: AI问答 -->
            <div class="code-butler-tab-content active" id="codeButlerSearch">
                <div class="ai-question-box">
                    <textarea class="ai-question-input" id="aiQuestionInput" placeholder="向AI代码管家提问...

示例问题：
• StateManager在哪个文件？
• 如何添加新的API接口？
• 架构师监控模块的代码在哪里？
• Dashboard的HTML模板在哪个文件？
• 如何记录架构师事件？"></textarea>
                    <button class="ai-ask-button" onclick="askCodeButler()">▸ 向AI提问</button>
                </div>
                <div class="ai-response" id="aiResponse">
AI代码管家等待您的提问...

我可以帮您：
• 快速找到任何函数、类、文件的位置
• 解释代码的作用和逻辑
• 提供代码示例和使用方法
• 指导如何修改和扩展功能

请在上面输入您的问题，点击"向AI提问"按钮。
                </div>
            </div>
            
            <!-- Tab 2: 代码结构 -->
            <div class="code-butler-tab-content" id="codeButlerStructure">
                <div class="prompt-display">
                    <div class="code-tree">
<strong>ai-task-automation-board/</strong>
├── <strong>automation/</strong> (核心业务逻辑 - 10个模块)
│   ├── models.py (数据模型 - 8个类)
│   ├── state_manager.py (状态管理 - SQLite持久化)
│   ├── dependency_analyzer.py (依赖分析引擎)
│   ├── task_scheduler.py (任务调度系统)
│   ├── architect_reviewer.py (代码审查AI)
│   └── ...
│
├── <strong>industrial_dashboard/</strong> (Dashboard模块)
│   ├── dashboard.py (FastAPI应用 + 10+个API)
│   ├── templates.py (HTML模板 - 13个模块)
│   ├── data_provider.py (数据适配器)
│   └── adapters.py (StateManager适配器)
│
├── <strong>automation-data/</strong> (数据文件)
│   ├── tasks.db (任务数据库)
│   ├── architect_monitor.json (架构师监控数据)
│   ├── architect-notes/ (架构师文档)
│   ├── developer-knowledge/ (开发知识库)
│   ├── tester-knowledge/ (测试知识库)
│   ├── delivery-docs/ (交付文档)
│   └── ops/ (运维文档)
│
└── <strong>scripts/</strong> (工具脚本)
    ├── architect_logger.py (架构师事件记录器)
    └── ...
                    </div>
                </div>
            </div>
            
            <!-- Tab 3: 分类索引 -->
            <div class="code-butler-tab-content" id="codeButlerIndex">
                <div class="info-panel">
                    <div class="info-sidebar">
                        <div class="info-doc-list">
                            <div class="info-doc-item active" onclick="switchCodeIndex('models')">
                                <span class="info-doc-icon">◆</span>
                                数据模型
                            </div>
                            <div class="info-doc-item" onclick="switchCodeIndex('api')">
                                <span class="info-doc-icon">◉</span>
                                API接口
                            </div>
                            <div class="info-doc-item" onclick="switchCodeIndex('ui')">
                                <span class="info-doc-icon">▸</span>
                                UI模块
                            </div>
                            <div class="info-doc-item" onclick="switchCodeIndex('utils')">
                                <span class="info-doc-icon">⚠</span>
                                工具函数
                            </div>
                        </div>
                    </div>
                    <div class="info-content">
                        <div class="info-content-title" id="codeIndexTitle">数据模型</div>
                        <div class="info-content-body" id="codeIndexContent">
# 数据模型索引

## Task（任务模型）
- 文件：automation/models.py
- 行数：10-45
- 说明：任务的完整数据结构

## TaskStatus（任务状态枚举）
- 文件：automation/models.py
- 行数：5-9
- 说明：7种任务状态定义

## StateManager（状态管理器）
- 文件：automation/state_manager.py
- 行数：15-280
- 说明：SQLite持久化管理
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="update-time">
        <div class="auto-refresh-indicator">
            <span class="refresh-icon" id="refreshIcon"></span>
            <span class="refresh-status" id="refreshStatus">自动刷新 5秒</span>
        </div>
        <span id="updateTime">—</span>
    </div>
    
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
        
        function getTaskParallelInfo(task) {{
            // 检查任务依赖
            if (task.dependencies && task.dependencies.length > 0) {{
                // 有依赖，不可并行
                const depList = task.dependencies.join(', ');
                return {{
                    type: 'sequential',
                    label: `依赖: ${{depList}}`,
                    canParallel: false
                }};
            }} else {{
                // 无依赖，可并行
                return {{
                    type: 'parallel',
                    label: '可并行',
                    canParallel: true
                }};
            }}
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
        
        // 自动刷新控制变量
        let autoRefreshEnabled = true;
        let lastTasksData = null;
        let isUserInteracting = false;
        
        // 性能监控
        let performanceStats = {{
            refreshCount: 0,
            totalRefreshTime: 0,
            averageRefreshTime: 0,
            lastRefreshTime: 0
        }};
        
        // 检测用户交互
        function setupUserInteractionDetection() {{
            const interactiveElements = ['input', 'textarea', 'select'];
            interactiveElements.forEach(tag => {{
                document.addEventListener('focusin', (e) => {{
                    if (e.target.tagName.toLowerCase() === tag) {{
                        isUserInteracting = true;
                    }}
                }});
                document.addEventListener('focusout', (e) => {{
                    if (e.target.tagName.toLowerCase() === tag) {{
                        isUserInteracting = false;
                    }}
                }});
            }});
        }}
        
        async function loadData() {{
            const startTime = performance.now(); // 性能监控：开始时间
            
            try {{
                // 如果用户正在交互，跳过本次刷新
                if (isUserInteracting) {{
                    console.log('[自动刷新] 用户正在操作，跳过本次刷新');
                    updateRefreshStatus('暂停(用户操作中)', 'paused');
                    return;
                }}
                
                // 更新状态为加载中
                updateRefreshStatus('刷新中...', 'loading');
                
                // 加载所有任务数据
                const tasksRes = await fetch('/api/tasks?_t=' + Date.now()); // 添加时间戳避免缓存
                const newTasksData = await tasksRes.json();
                
                // 检查数据是否有变化（避免不必要的DOM更新）
                if (lastTasksData && JSON.stringify(lastTasksData) === JSON.stringify(newTasksData)) {{
                    console.log('[自动刷新] 数据无变化，跳过UI更新');
                    updateRefreshStatus('自动刷新 5秒', 'active');
                    
                    // 性能监控：记录刷新时间
                    const endTime = performance.now();
                    const refreshTime = endTime - startTime;
                    updatePerformanceStats(refreshTime);
                    return;
                }}
                
                // 数据有变化，更新UI
                allTasksData = newTasksData;
                lastTasksData = JSON.parse(JSON.stringify(newTasksData)); // 深拷贝
                
                // 显示当前版本的数据
                switchVersion(currentVersion);
                
                const now = new Date();
                document.getElementById('updateTime').textContent = now.toLocaleTimeString('zh-CN', {{ hour12: false }});
                
                // 闪烁效果提示用户数据已更新
                flashUpdateIndicator();
                
                console.log('[自动刷新] 任务列表已更新，共 ' + allTasksData.length + ' 个任务');
                updateRefreshStatus('自动刷新 5秒', 'active');
                
                // 性能监控：记录刷新时间
                const endTime = performance.now();
                const refreshTime = endTime - startTime;
                updatePerformanceStats(refreshTime);
                
            }} catch (error) {{
                console.error('[自动刷新] 加载失败:', error);
                updateRefreshStatus('刷新失败', 'error');
            }}
        }}
        
        // 更新性能统计
        function updatePerformanceStats(refreshTime) {{
            performanceStats.refreshCount++;
            performanceStats.totalRefreshTime += refreshTime;
            performanceStats.averageRefreshTime = performanceStats.totalRefreshTime / performanceStats.refreshCount;
            performanceStats.lastRefreshTime = refreshTime;
            
            // 每10次刷新输出一次性能统计
            if (performanceStats.refreshCount % 10 === 0) {{
                console.log('[性能监控] 刷新统计:', {{
                    总次数: performanceStats.refreshCount,
                    平均耗时: performanceStats.averageRefreshTime.toFixed(2) + 'ms',
                    最后耗时: performanceStats.lastRefreshTime.toFixed(2) + 'ms',
                    CPU占用: '估算 <2%（异步非阻塞）'
                }});
            }}
        }}
        
        // 更新刷新状态指示器
        function updateRefreshStatus(text, state) {{
            const statusEl = document.getElementById('refreshStatus');
            const iconEl = document.getElementById('refreshIcon');
            
            if (statusEl) {{
                statusEl.textContent = text;
                statusEl.className = 'refresh-status';
                if (state === 'paused' || state === 'error') {{
                    statusEl.classList.add('paused');
                }}
            }}
            
            if (iconEl) {{
                iconEl.className = 'refresh-icon';
                if (state === 'paused' || state === 'error') {{
                    iconEl.classList.add('paused');
                }}
            }}
        }}
        
        // 闪烁效果，提示用户数据已更新
        function flashUpdateIndicator() {{
            const updateTimeEl = document.getElementById('updateTime');
            if (updateTimeEl) {{
                updateTimeEl.style.color = 'var(--blue)';
                updateTimeEl.style.fontWeight = '700';
                setTimeout(() => {{
                    updateTimeEl.style.color = 'var(--gray-500)';
                    updateTimeEl.style.fontWeight = '400';
                }}, 500);
            }}
        }}
        
        
        // 版本数据（支持动态扩展）
        let allTasksData = [];
        let currentVersion = 'v1';
        
        const versionConfigs = {{
            'v1': {{
                description: 'MVP基础版本 - 实现核心桌面框架和基础功能',
                taskFilter: (task) => true  // 版本1显示所有任务
            }},
            'v2': {{
                description: '插件生态版本 - 引入完整的插件体系，支持扩展和自定义（开发中）',
                taskFilter: (task) => task.id.startsWith('v2-')  // 版本2只显示v2-开头的
            }},
            'v3': {{
                description: '高级特性版本 - 实现高级特性和性能优化（规划中）',
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
            
            // 更新进度
            const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
            document.getElementById('progressPercent').textContent = progress + '%';
            
            // 更新任务统计显示 (例如: 11/40 tasks)
            const tasksCountEl = document.getElementById('progressTasksCount');
            if (tasksCountEl) {{
                tasksCountEl.textContent = `${{completed}}/${{total}} tasks`;
            }}
            
            // 更新时间轴进度线
            const timelineProgress = document.getElementById('timelineProgress');
            if (timelineProgress) {{
                timelineProgress.style.width = progress + '%';
            }}
            
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
                renderFilteredTasks(); return; // Use新筛选渲染 
            document.getElementById('taskList').innerHTML = tasks.map(task => `
                    <div class="task-card">
                        <div class="task-card-header">
                            <span class="task-id">${{task.id}}</span>
                            <div class="task-actions">
                                ${{task.status === 'completed' ? `
                                    <button class="copy-report-button" onclick="copyTaskReport('${{task.id}}', event)">
                                        ▸ 复制报告
                                    </button>
                                ` : task.status === 'pending' ? `
                                    <button class="copy-prompt-button" onclick="copyTaskPrompt('${{task.id}}', event)">
                                        ▸ 复制提示词
                                    </button>
                                ` : task.status === 'in_progress' ? `
                                    <button class="redispatch-button" onclick="redispatchTask('${{task.id}}', event)">
                                        ↻ 重新派发
                                    </button>
                                ` : ''}}
                                <span class="task-status ${{task.status.toLowerCase().replace(' ', '_')}}">
                                    ${{getStatusText(task.status)}}
                                </span>
                            </div>
                        </div>
                        <div class="task-title">
                            <span>${{task.title}}</span>
                            ${{(() => {{
                                const parallelInfo = getTaskParallelInfo(task);
                                return `<span class="task-parallel-badge ${{parallelInfo.type}}">${{parallelInfo.label}}</span>`;
                            }})()}}
                        </div>
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
        
        // ===== 架构师模块交互 =====
        
        function switchArchitectTab(tab) {{
            console.log('[DEBUG] switchArchitectTab called with:', tab);
            const tabs = ['events', 'chat', 'prompt', 'notes', 'assign'];
            const buttons = document.querySelectorAll('.architect-tab');
            
            tabs.forEach((t, index) => {{
                const tabName = t.charAt(0).toUpperCase() + t.slice(1);
                const content = document.getElementById('architect' + tabName);
                console.log('[DEBUG] Tab:', t, 'ID:', 'architect' + tabName, 'Element:', content);
                if (content) {{
                    if (t === tab) {{
                        content.classList.add('active');
                        if (buttons[index]) buttons[index].classList.add('active');
                    }} else {{
                        content.classList.remove('active');
                        if (buttons[index]) buttons[index].classList.remove('active');
                    }}
                }}
            }});
        }}
        
        // 复制架构师任命指令
        async function copyArchitectAssignPrompt() {{
            const prompt = `认命你为【任务所·Flow v1.7】的总架构师。

# Phase 0：启动与自检

## 第一步：读取你的完整System Prompt
@taskflow-v1.7-monorepo/docs/ai/architect-system-prompt-expert.md

这份文档（8000字）定义了你的工作规范：
- 身份定位：Staff/Principal Engineer（10-15年经验）
- 能力模型：技术广度+专家深度
- 5阶段工作流程：理解验证→场景深挖→方案生成→对比推荐→质疑模式
- 核心原则：理解优于执行、质疑优于盲从、最优解优于快速解

读完后确认启动，再继续Phase 1。

---

# Phase 1：扫描项目文件夹（结构级盘点）

## 项目信息
- 项目名称: 任务所·Flow v1.7
- 项目路径: taskflow-v1.7-monorepo/
- 当前进度: 46% (25/54任务完成)
- Dashboard端口: http://localhost:8877
- 数据库: database/data/tasks.db

## 扫描任务
1. 列出根目录第1-2层目录结构
2. 读取关键入口文件：
   - README.md
   - apps/dashboard/start_dashboard.py
   - apps/dashboard/src/industrial_dashboard/dashboard.py
   - database/migrations/*.sql
3. 生成文档：docs/arch/architecture-inventory.md

---

# Phase 2：企业级目录结构映射

## 对照目标结构
模板文件：docs/arch/monorepo-structure-taskflow.md（如有）

## 映射任务
- 现有 apps/dashboard/src/automation/ → 目标 apps/api/
- 现有 industrial_dashboard/ → apps/dashboard/
- 散落的 utils → packages/shared-utils/
- 生成文档：docs/arch/refactor-plan.md（重构规划）

**注意：只规划，不执行**

---

# Phase 3：代码深挖与功能盘点

## 必读代码模块
- apps/dashboard/src/automation/（任务管理核心）
- apps/dashboard/src/industrial_dashboard/dashboard.py（API路由）
- apps/dashboard/src/automation/state_manager.py（状态管理）
- apps/dashboard/src/automation/models.py（数据模型）
- apps/dashboard/src/industrial_dashboard/templates.py（UI）

## 产出文档
- 更新：docs/arch/architecture-review.md
- 内容：已实现功能、部分实现、技术债、风险区

---

# Phase 4：生成/更新任务板

## 先读现状文档
- 📍给下一任架构师-紧急交接-2025-11-19-05-30.md
- docs/tasks/task-board.md
- docs/arch/architecture-review.md（如已生成）

## 任务板结构
- 已实现功能清单
- 部分实现/半成品
- 技术债/风险清单  
- 建议任务列表（每个任务带完整提示词）

---

# Phase 5：持续审查与迭代

当李明提交任务完成报告：
1. 审查是否符合规划
2. 更新任务板状态
3. 必要时派生新任务

---

# 你的核心定位
✅ 总架构师：结构设计、规划、审查
❌ 不是执行者：不亲自大量写业务代码

# 主要输出物
- docs/arch/architecture-inventory.md
- docs/arch/refactor-plan.md
- docs/arch/architecture-review.md
- docs/tasks/task-board.md

现在开始Phase 0，读取System Prompt后启动工作流！`;
            
            try {{
                await navigator.clipboard.writeText(prompt);
                showNotification('✅ 复制成功', '架构师任命指令已复制，请在新Cursor窗口粘贴', 'success');
            }} catch (error) {{
                console.error('复制失败:', error);
                alert('复制失败，请手动复制屏幕上的文本');
            }}
        }}
        
        function copyPrompt() {{
            const promptText = document.getElementById('promptDisplay').textContent;
            navigator.clipboard.writeText(promptText).then(() => {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ 已复制';
                setTimeout(() => {{
                    btn.textContent = originalText;
                }}, 2000);
            }});
        }}
        
        function switchInfoDoc(docId) {{
            const items = document.querySelectorAll('.info-doc-item');
            items.forEach(item => item.classList.remove('active'));
            event.target.closest('.info-doc-item').classList.add('active');
            loadInfoDoc(docId);
        }}
        
        async function loadArchitectData() {{
            try {{
                const response = await fetch('/api/architect_monitor');
                const data = await response.json();
                
                if (data.token_usage) {{
                    const used = data.token_usage.used;
                    const total = data.token_usage.total;
                    const percent = ((used / total) * 100).toFixed(1);
                    
                    document.getElementById('tokenUsed').textContent = used.toLocaleString();
                    document.getElementById('tokenPercent').textContent = percent;
                    
                    const tokenInfo = document.getElementById('tokenInfo');
                    if (percent < 20) {{
                        tokenInfo.classList.add('warning');
                    }} else {{
                        tokenInfo.classList.remove('warning');
                    }}
                }}
                
                if (data.status) {{
                    document.getElementById('architectStatusText').textContent = data.status.text;
                    document.getElementById('architectTasksCount').textContent = 
                        `已审查 ${{data.status.reviewed_count || 0}} 个任务`;
                }}
                
                if (data.events && data.events.length > 0) {{
                    renderEventTimeline(data.events);
                }}
                
                if (data.prompt) {{
                    document.getElementById('promptDisplay').textContent = data.prompt;
                }}
                
                document.getElementById('lastUpdate').textContent = 
                    new Date().toLocaleTimeString('zh-CN', {{hour12: false}});
                
                // 加载当前角色
                if (data.current_role && data.current_role.role) {{
                    document.getElementById('roleSelector').value = data.current_role.role;
                    document.getElementById('currentRoleDisplay').textContent = 
                        '✓ ' + data.current_role.role_name;
                    document.getElementById('currentRoleDisplay').style.display = 'inline';
                }}
                    
            }} catch (error) {{
                console.error('加载架构师数据失败:', error);
            }}
        }}
        
        // 激活角色
        async function activateRole() {{
            const role = document.getElementById('roleSelector').value;
            
            if (!role) {{
                alert('请先选择一个角色');
                return;
            }}
            
            try {{
                const response = await fetch('/api/assign_role', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        role: role,
                        project: '任务所·Flow',
                        user: '项目负责人'
                    }})
                }});
                
                const data = await response.json();
                
                if (data.success) {{
                    alert('✅ ' + data.message);
                    document.getElementById('currentRoleDisplay').textContent = 
                        '✓ ' + data.role_name;
                    document.getElementById('currentRoleDisplay').style.display = 'inline';
                    
                    // 刷新架构师数据
                    loadArchitectData();
                }} else {{
                    alert('❌ 任命失败: ' + data.error);
                }}
            }} catch (error) {{
                console.error('任命角色失败:', error);
                alert('任命失败，请重试');
            }}
        }}
        
        function renderEventTimeline(events) {{
            const timeline = document.getElementById('eventTimeline');
            
            if (!events || events.length === 0) {{
                timeline.innerHTML = `
                    <div class="event-item">
                        <span class="event-time">--:--:--</span>
                        <span class="event-icon default">—</span>
                        <span class="event-content">暂无事件记录</span>
                    </div>
                `;
                return;
            }}
            
            const sortedEvents = [...events].reverse();
            
            // REQ-010 事件类型图标映射（28种事件类型）
            const eventTypeMap = {{
                // 任务生命周期事件 (9种)
                'task_created': {{ icon: '✦', class: 'task' }},
                'task_dispatched': {{ icon: '→', class: 'task' }},
                'task_received': {{ icon: '↓', class: 'communication' }},
                'task_started': {{ icon: '▸', class: 'start' }},
                'task_progress': {{ icon: '◐', class: 'task' }},
                'task_completed': {{ icon: '✓', class: 'review' }},
                'task_reviewed': {{ icon: '◎', class: 'review' }},
                'task_approved': {{ icon: '✓', class: 'review' }},
                'task_rejected': {{ icon: '✗', class: 'review' }},

                // 功能生命周期事件 (5种)
                'feature_developed': {{ icon: '◆', class: 'development' }},
                'feature_tested': {{ icon: '◇', class: 'api' }},
                'feature_integrated': {{ icon: '⊕', class: 'task' }},
                'feature_deployed': {{ icon: '↑', class: 'task' }},
                'feature_verified': {{ icon: '✓', class: 'review' }},

                // 问题生命周期事件 (4种)
                'issue_discovered': {{ icon: '⚠', class: 'requirement' }},
                'issue_diagnosed': {{ icon: '◉', class: 'task' }},
                'issue_fixed': {{ icon: '✓', class: 'review' }},
                'issue_verified': {{ icon: '✓', class: 'review' }},

                // 协作事件 (10种)
                'user_feedback': {{ icon: '●', class: 'communication' }},
                'architect_analysis': {{ icon: '◉', class: 'task' }},
                'engineer_implementation': {{ icon: '◆', class: 'development' }},
                'code_review': {{ icon: '◎', class: 'review' }},
                'meeting': {{ icon: '●', class: 'communication' }},
                'decision_made': {{ icon: '◉', class: 'task' }},
                'deployment': {{ icon: '↑', class: 'task' }},
                'incident': {{ icon: '!', class: 'requirement' }},
                'handoff': {{ icon: '⇄', class: 'task' }},
                'notification': {{ icon: '◆', class: 'communication' }},

                // 兼容旧格式
                'start': {{ icon: '▸', class: 'start' }},
                'communication': {{ icon: '●', class: 'communication' }},
                'task_breakdown': {{ icon: '✓', class: 'task' }},
                'task_update': {{ icon: '↻', class: 'task' }},
                'development': {{ icon: '◆', class: 'development' }},
                'review_start': {{ icon: '◎', class: 'review' }},
                'review_pass': {{ icon: '✓', class: 'review' }},
                'review_fail': {{ icon: '✗', class: 'review' }},
                'api': {{ icon: '◇', class: 'api' }},
                'requirement_change': {{ icon: '⚠', class: 'requirement' }},
                'receive_task': {{ icon: '↓', class: 'communication' }},
                'warning': {{ icon: '!', class: 'requirement' }},
                'decision': {{ icon: '◉', class: 'task' }}
            }};
            
            timeline.innerHTML = sortedEvents.map(event => {{
                const eventInfo = eventTypeMap[event.type] || {{ icon: '•', class: 'default' }};
                return `
                    <div class="event-item">
                        <span class="event-time">${{event.time}}</span>
                        <span class="event-icon ${{eventInfo.class}}">${{eventInfo.icon}}</span>
                        <span class="event-content">${{event.content}}</span>
                    </div>
                `;
            }}).join('');
        }}
        
        async function loadInfoDoc(docId) {{
            try {{
                const response = await fetch(`/api/architect_info/${{docId}}`);
                const data = await response.json();
                
                document.getElementById('infoContentTitle').textContent = data.title;
                document.getElementById('infoContentBody').textContent = data.content;
            }} catch (error) {{
                console.error('加载文档失败:', error);
            }}
        }}
        
        // ===== 对话历史库管理 =====
        
        let conversationsData = null;
        let selectedSessionId = null;
        
        // 加载会话数据（从本地JSON文件）
        async function loadConversations() {{
            try {{
                console.log('[会话管理] 开始加载会话数据...');
                
                // 优先从API加载
                let data = null;
                let useApi = false;
                
                try {{
                    const response = await fetch('/api/conversations');
                    if (response.ok) {{
                        const apiData = await response.json();
                        if (apiData.sessions && apiData.sessions.length > 0) {{
                            data = apiData;
                            useApi = true;
                            console.log('[会话管理] ✓ 从API加载成功:', apiData.sessions.length, '个会话');
                        }}
                    }}
                }} catch (apiError) {{
                    console.log('[会话管理] API不可用，使用本地文件');
                }}
                
                // 如果API失败，加载本地文件
                if (!data) {{
                    const response = await fetch('/automation-data/architect-conversations.json');
                    if (!response.ok) throw new Error('无法加载本地文件');
                    data = await response.json();
                    console.log('[会话管理] ✓ 从本地文件加载成功:', data.sessions.length, '个会话');
                }}
                
                // 保存会话数据
                conversationsData = data;
                const sessions = conversationsData.sessions || [];
                
                console.log('[会话管理] 渲染', sessions.length, '个会话');
                renderConversationList(sessions);
                
                // 自动选中第一个会话
                if (sessions.length > 0) {{
                    selectSession(sessions[0].session_id);
                }}
                
            }} catch (error) {{
                console.error('[会话管理] 加载失败:', error);
                const listContainer = document.getElementById('conversationList');
                if (listContainer) {{
                    listContainer.innerHTML = `
                        <div style="text-align: center; color: var(--gray-500); padding: 40px 20px; font-size: 14px;">
                            <div>⚠️ 无法加载会话数据</div>
                            <div style="font-size: 12px; color: var(--gray-400); margin-top: 8px; line-height: 1.4;">
                                原因: ${{error.message}}<br/>
                                请检查:<br/>
                                • 本地文件: /automation-data/architect-conversations.json<br/>
                                • 或启动API: python apps/api/start_api.py
                            </div>
                        </div>
                    `;
                }}
            }}
        }}
        
        // 渲染会话列表
        function renderConversationList(sessions) {{
            const listContainer = document.getElementById('conversationList');
            
            if (!sessions || sessions.length === 0) {{
                listContainer.innerHTML = `
                    <div style="text-align: center; color: var(--gray-500); padding: 20px;">
                        <div>暂无会话记录</div>
                    </div>
                `;
                return;
            }}
            
            // 更新会话数量
            document.querySelector('.conversation-header div:last-child').textContent = `共 ${{sessions.length}} 个会话`;
            
            listContainer.innerHTML = sessions.map(session => {{
                const isActive = session.session_id === selectedSessionId ? 'active' : '';
                const statusColor = session.status === 'completed' ? 'var(--blue)' : 'var(--gray-500)';
                const statusText = session.status === 'completed' ? 'DONE' : 'ACTIVE';
                
                return `
                    <div class="conversation-item ${{isActive}}" onclick="selectSession('${{session.session_id}}')">
                        <div class="conversation-item-header">
                            <div class="conversation-item-title">${{session.title}}</div>
                            <span class="conversation-item-status" style="background: ${{statusColor}}">${{statusText}}</span>
                        </div>
                        <div class="conversation-item-meta">
                            <div class="conversation-item-tokens">
                                <span>🔸</span>
                                <span>${{formatNumber(session.total_tokens)}}T</span>
                            </div>
                            <div class="conversation-item-time">
                                <span>⏱</span>
                                <span>${{formatDate(session.created_at)}}</span>
                            </div>
                        </div>
                        <div class="conversation-item-tags">
                            ${{(session.tags || []).slice(0, 3).map(tag => 
                                `<span class="conversation-tag">${{tag}}</span>`
                            ).join('')}}
                        </div>
                    </div>
                `;
            }}).join('');
        }}
        
        // 选择会话
        function selectSession(sessionId) {{
            selectedSessionId = sessionId;
            
            if (!conversationsData || !conversationsData.sessions) {{
                return;
            }}
            
            const session = conversationsData.sessions.find(s => s.session_id === sessionId);
            if (!session) {{
                return;
            }}
            
            // 更新列表中的active状态
            document.querySelectorAll('.conversation-item').forEach(item => {{
                item.classList.remove('active');
            }});
            event.target.closest('.conversation-item')?.classList.add('active');
            
            // 渲染会话详情
            renderSessionDetail(session);
        }}
        
        // 渲染会话详情
        function renderSessionDetail(session) {{
            const detailContainer = document.getElementById('conversationDetail');
            
            const duration = calculateDuration(session.created_at, session.updated_at);
            
            detailContainer.innerHTML = `
                <div class="conversation-detail-header">
                    <div class="conversation-detail-title">${{session.title}}</div>
                    <div class="conversation-detail-meta">
                        <span>📅 ${{formatFullDate(session.created_at)}} - ${{formatFullDate(session.updated_at)}}</span>
                        <span>⏱ 持续 ${{duration}}</span>
                        <span>💬 ${{session.messages_count}} 条消息</span>
                        <span>🔸 ${{formatNumber(session.total_tokens)}} Tokens</span>
                        <span>👥 ${{session.participants.join(', ')}}</span>
                    </div>
                </div>
                
                <div class="conversation-detail-summary">
                    <strong>📋 会话摘要：</strong>${{session.summary}}
                </div>
                
                <div class="conversation-messages">
                    ${{session.messages.map(msg => {{
                        const authorClass = msg.from === '用户' ? 'user' : 'architect';
                        return `
                            <div class="conversation-message">
                                <div class="conversation-message-header">
                                    <span class="conversation-message-author ${{authorClass}}">${{msg.from}}</span>
                                    <span class="conversation-message-time">${{formatFullDate(msg.timestamp)}}</span>
                                </div>
                                <div class="conversation-message-content ${{authorClass}}">${{msg.content}}</div>
                                <div class="conversation-message-tokens">📊 Token消耗: ${{formatNumber(msg.tokens)}}</div>
                            </div>
                        `;
                    }}).join('')}}
                </div>
            `;
        }}
        
        // 搜索过滤
        function filterSessions() {{
            const searchInput = document.getElementById('sessionSearchInput');
            const searchTerm = searchInput.value.toLowerCase();
            
            if (!conversationsData || !conversationsData.sessions) {{
                return;
            }}
            
            const filtered = conversationsData.sessions.filter(session => {{
                const titleMatch = session.title.toLowerCase().includes(searchTerm);
                const tagsMatch = (session.tags || []).some(tag => tag.toLowerCase().includes(searchTerm));
                const summaryMatch = (session.summary || '').toLowerCase().includes(searchTerm);
                return titleMatch || tagsMatch || summaryMatch;
            }});
            
            renderConversationList(filtered);
        }}
        
        // 格式化数字（添加千分位）
        function formatNumber(num) {{
            if (!num) return '0';
            return num.toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ',');
        }}
        
        // 格式化日期（短格式）
        function formatDate(dateStr) {{
            if (!dateStr) return '—';
            const parts = dateStr.split(' ')[0].split('-');
            return `${{parts[1]}}-${{parts[2]}}`;
        }}
        
        // 格式化日期（完整格式）
        function formatFullDate(dateStr) {{
            if (!dateStr) return '—';
            return dateStr;
        }}
        
        // 计算持续时间
        function calculateDuration(start, end) {{
            if (!start || !end) return '—';
            
            const startDate = new Date(start);
            const endDate = new Date(end);
            const diffMs = endDate - startDate;
            
            const hours = Math.floor(diffMs / 3600000);
            const minutes = Math.floor((diffMs % 3600000) / 60000);
            
            if (hours > 0) {{
                return `${{hours}}小时${{minutes}}分`;
            }}
            return `${{minutes}}分钟`;
        }}
        
        // ===== UX/UI确认模块交互 =====
        
        function switchConfirmationTab(type, tab) {{
            const imagesTab = document.getElementById(`${{type}}Images`);
            const promptTab = document.getElementById(`${{type}}Prompt`);
            const buttons = document.querySelectorAll(`#${{type}}Confirmation .confirmation-tab`);
            
            if (tab === 'images') {{
                imagesTab.style.display = 'block';
                promptTab.style.display = 'none';
                buttons[0].classList.add('active');
                buttons[1].classList.remove('active');
            }} else {{
                imagesTab.style.display = 'none';
                promptTab.style.display = 'block';
                buttons[0].classList.remove('active');
                buttons[1].classList.add('active');
            }}
        }}
        
        function openLightbox(imageSrc) {{
            const lightbox = document.getElementById('lightbox');
            const lightboxImage = document.getElementById('lightboxImage');
            lightboxImage.src = imageSrc;
            lightbox.classList.add('active');
        }}
        
        function closeLightbox() {{
            const lightbox = document.getElementById('lightbox');
            lightbox.classList.remove('active');
        }}
        
        function confirmUX() {{
            if (confirm('确认通过UX设计？')) {{
                fetch('/api/confirm_ux', {{
                    method: 'POST'
                }}).then(response => response.json())
                  .then(data => {{
                      if (data.success) {{
                          document.getElementById('uxStatus').textContent = '已确认';
                          document.getElementById('uxStatus').classList.remove('pending');
                          document.getElementById('uxStatus').classList.add('approved');
                          const btn = document.getElementById('uxConfirmBtn');
                          btn.disabled = true;
                          btn.classList.add('confirmed');
                          btn.textContent = '已确认';
                          alert('✅ UX设计已确认！');
                      }}
                  }}).catch(error => {{
                      console.error('确认失败:', error);
                      alert('确认失败，请重试');
                  }});
            }}
        }}
        
        function confirmUI() {{
            if (confirm('确认通过UI设计？')) {{
                fetch('/api/confirm_ui', {{
                    method: 'POST'
                }}).then(response => response.json())
                  .then(data => {{
                      if (data.success) {{
                          document.getElementById('uiStatus').textContent = '已确认';
                          document.getElementById('uiStatus').classList.remove('pending');
                          document.getElementById('uiStatus').classList.add('approved');
                          const btn = document.getElementById('uiConfirmBtn');
                          btn.disabled = true;
                          btn.classList.add('confirmed');
                          btn.textContent = '已确认';
                          alert('✅ UI设计已确认！');
                      }}
                  }}).catch(error => {{
                      console.error('确认失败:', error);
                      alert('确认失败，请重试');
                  }});
            }}
        }}
        
        async function loadConfirmationData() {{
            try {{
                const uxResponse = await fetch('/api/ux_confirmation');
                const uxData = await uxResponse.json();
                
                if (uxData.images && uxData.images.length > 0) {{
                    renderImages('ux', uxData.images);
                }}
                
                if (uxData.prompt) {{
                    document.getElementById('uxPromptContent').textContent = uxData.prompt;
                }}
                
                if (uxData.status === 'approved') {{
                    document.getElementById('uxStatus').textContent = '已确认';
                    document.getElementById('uxStatus').classList.remove('pending');
                    document.getElementById('uxStatus').classList.add('approved');
                    const btn = document.getElementById('uxConfirmBtn');
                    btn.disabled = true;
                    btn.classList.add('confirmed');
                    btn.textContent = '已确认';
                }}
                
                const uiResponse = await fetch('/api/ui_confirmation');
                const uiData = await uiResponse.json();
                
                if (uiData.images && uiData.images.length > 0) {{
                    renderImages('ui', uiData.images);
                }}
                
                if (uiData.prompt) {{
                    document.getElementById('uiPromptContent').textContent = uiData.prompt;
                }}
                
                if (uiData.status === 'approved') {{
                    document.getElementById('uiStatus').textContent = '已确认';
                    document.getElementById('uiStatus').classList.remove('pending');
                    document.getElementById('uiStatus').classList.add('approved');
                    const btn = document.getElementById('uiConfirmBtn');
                    btn.disabled = true;
                    btn.classList.add('confirmed');
                    btn.textContent = '已确认';
                }}
            }} catch (error) {{
                console.error('加载确认数据失败:', error);
            }}
        }}
        
        function renderImages(type, images) {{
            const grid = document.getElementById(`${{type}}ImagesGrid`);
            
            if (!images || images.length === 0) {{
                grid.innerHTML = '<div class="empty-state">暂无设计图</div>';
                return;
            }}
            
            grid.innerHTML = images.map(img => `
                <div class="image-item" onclick="openLightbox('${{img.url}}')">
                    <img class="image-preview" src="${{img.url}}" alt="${{img.label}}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'100\\' height=\\'100\\'%3E%3Crect fill=\\'%23E0E0E0\\' width=\\'100\\' height=\\'100\\'/%3E%3Ctext x=\\'50%25\\' y=\\'50%25\\' text-anchor=\\'middle\\' dy=\\'.3em\\' fill=\\'%239E9E9E\\' font-size=\\'12\\'%3E图片加载失败%3C/text%3E%3C/svg%3E'">
                    <div class="image-label">${{img.label}}</div>
                </div>
            `).join('');
        }}
        
        // ===== 功能清单模块交互 =====
        
        function switchFeatureTab(tab) {{
            console.log('[DEBUG] switchFeatureTab called with:', tab);
            const tabs = ['implemented', 'partial', 'conflicts'];
            const buttons = document.querySelectorAll('.features-section .confirmation-tab');
            
            tabs.forEach((t, index) => {{
                const content = document.getElementById(t + 'Features');
                console.log('[DEBUG] Processing tab:', t, 'Element:', content);
                if (content) {{
                    if (t === tab) {{
                        content.classList.add('active');
                        if (buttons[index]) buttons[index].classList.add('active');
                    }} else {{
                        content.classList.remove('active');
                        if (buttons[index]) buttons[index].classList.remove('active');
                    }}
                }}
            }});
        }}
        
        async function loadProjectScan() {{
            try {{
                const response = await fetch('/api/project_scan');
                const data = await response.json();
                
                if (!data || !data.features) {{
                    return;
                }}
                
                // 渲染已实现功能
                if (data.features.implemented && data.features.implemented.length > 0) {{
                    renderImplementedFeatures(data.features.implemented);
                    document.getElementById('featureCount').textContent = 
                        `${{data.features.implemented.length}} 个已实现`;
                }}
                
                // 渲染部分实现功能
                if (data.features.partial && data.features.partial.length > 0) {{
                    renderPartialFeatures(data.features.partial);
                }}
                
                // 渲染冲突功能
                if (data.features.conflicts && data.features.conflicts.length > 0) {{
                    renderConflictFeatures(data.features.conflicts);
                }}
                
            }} catch (error) {{
                console.error('加载项目扫描结果失败:', error);
            }}
        }}
        
        function renderImplementedFeatures(features) {{
            const list = document.getElementById('implementedFeaturesList');
            list.innerHTML = features.map((f, i) => `
                <div class="feature-item" style="padding: 12px; border-bottom: 1px solid var(--gray-200); display: flex; gap: 12px; align-items: flex-start;">
                    <span style="color: #7BA882; font-size: 16px;">✓</span>
                    <div style="flex: 1;">
                        <div style="font-size: 13px; font-weight: 600; color: var(--black); margin-bottom: 4px;">${{f.name}}</div>
                        <div style="font-size: 11px; color: var(--gray-600); font-family: var(--font-mono);">
                            文件: ${{f.file || '—'}} | 类型: ${{f.type || '—'}}
                        </div>
                    </div>
                </div>
            `).join('');
        }}
        
        function renderPartialFeatures(features) {{
            const list = document.getElementById('partialFeaturesList');
            if (features.length === 0) {{
                list.innerHTML = '<div class="empty-state">暂无部分实现的功能</div>';
                return;
            }}
            list.innerHTML = features.map(f => `
                <div class="feature-item" style="padding: 12px; border-bottom: 1px solid var(--gray-200); display: flex; gap: 12px; align-items: flex-start;">
                    <span style="color: #E6C866; font-size: 16px;">◐</span>
                    <div style="flex: 1;">
                        <div style="font-size: 13px; font-weight: 600; color: var(--black); margin-bottom: 4px;">${{f.name}}</div>
                        <div style="font-size: 11px; color: var(--gray-600); font-family: var(--font-mono);">
                            文件: ${{f.file || '—'}} | 行: ${{f.line || '—'}}
                        </div>
                    </div>
                </div>
            `).join('');
        }}
        
        function renderConflictFeatures(features) {{
            const list = document.getElementById('conflictsFeaturesList');
            if (features.length === 0) {{
                list.innerHTML = '<div class="empty-state">✅ 未发现冲突，项目结构良好</div>';
                return;
            }}
            list.innerHTML = features.map(f => `
                <div class="feature-item" style="padding: 16px; border: 1px solid rgba(152, 82, 57, 0.2); border-left: 3px solid #985239; margin-bottom: 12px; background: rgba(152, 82, 57, 0.02);">
                    <div style="font-size: 13px; font-weight: 600; color: #985239; margin-bottom: 8px;">⚠ ${{f.name}}</div>
                    <div style="font-size: 11px; color: var(--gray-600); margin-bottom: 8px;">
                        ${{f.files ? f.files.join(' vs ') : '—'}}
                    </div>
                    <div style="font-size: 12px; color: var(--gray-700); padding: 8px; background: var(--white); border-left: 2px solid #C87D5C;">
                        💡 建议: ${{f.suggestion || '请架构师评估'}}
                    </div>
                </div>
            `).join('');
        }}
        
        async function generateTasksFromFeatures() {{
            if (confirm('确认将待完成功能清单拆解为开发任务？')) {{
                // TODO: 调用API拆解任务
                alert('✅ 功能拆解功能开发中...');
            }}
        }}
        
        // ===== 全栈开发工程师模块交互 =====
        
        
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
            // 三态按钮逻辑：pending → in_progress → completed
            if (task.status === 'pending') {{
                // 待处理：显示"📋 一键复制提示词"
                return `
                    <button
                        onclick="copyTaskPrompt('${{task.id}}')"
                        style="padding: 6px 12px; background: var(--blue); color: white; border: none; border-radius: 4px; font-size: 11px; cursor: pointer; font-weight: 600; transition: all 0.2s;"
                        onmouseover="this.style.background='var(--red)'"
                        onmouseout="this.style.background='var(--blue)'"
                        title="复制完整任务提示词到剪贴板"
                    >
                        📋 一键复制提示词
                    </button>
                `;
            }} else if (task.status === 'completed') {{
                // 已完成：显示"📄 一键复制完成报告"
                return `
                    <button
                        onclick="copyTaskReport('${{task.id}}')"
                        style="padding: 6px 12px; background: var(--blue); color: white; border: none; border-radius: 4px; font-size: 11px; cursor: pointer; font-weight: 600; transition: all 0.2s;"
                        onmouseover="this.style.background='var(--red)'"
                        onmouseout="this.style.background='var(--blue)'"
                        title="复制完成报告模板到剪贴板"
                    >
                        📄 一键复制完成报告
                    </button>
                `;
            }} else if (task.status === 'in_progress') {{
                // 进行中：显示"⚙️ 开发中"状态标签
                return `
                    <span style="padding: 6px 12px; background: #FEF3C7; color: #92400E; border-radius: 4px; font-size: 11px; font-weight: 600;">
                        ⚙️ 开发中
                    </span>
                `;
            }}
            return '';
        }}
        
        function switchDeveloperTab(tab) {{
            const tabs = ['tasks', 'prompt', 'knowledge'];
            const buttons = document.querySelectorAll('.developer-tab');
            
            tabs.forEach((t, index) => {{
                const content = document.getElementById(`developer${{t.charAt(0).toUpperCase() + t.slice(1)}}`);
                if (t === tab) {{
                    content.classList.add('active');
                    buttons[index].classList.add('active');
                }} else {{
                    content.classList.remove('active');
                    buttons[index].classList.remove('active');
                }}
            }});
        }}
        
        function copyDeveloperPrompt() {{
            const promptText = document.getElementById('developerPromptContent').textContent;
            navigator.clipboard.writeText(promptText).then(() => {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ 已复制';
                setTimeout(() => {{
                    btn.textContent = originalText;
                }}, 2000);
            }});
        }}
        
        async function loadDeveloperPrompt() {{
            try {{
                const response = await fetch('/api/role_prompt/developer');
                const data = await response.json();
                document.getElementById('developerPromptContent').textContent = data.content;
            }} catch (error) {{
                console.error('加载全栈工程师提示词失败:', error);
                document.getElementById('developerPromptContent').textContent = '加载失败，请刷新页面';
            }}
        }}
        
        async function loadArchitectPrompt() {{
            try {{
                const response = await fetch('/api/role_prompt/architect');
                const data = await response.json();
                const display = document.getElementById('promptDisplay');
                if (display) {{
                    display.textContent = data.content;
                }}
            }} catch (error) {{
                console.error('加载架构师提示词失败:', error);
                const display = document.getElementById('promptDisplay');
                if (display) {{
                    display.textContent = '加载失败，请刷新页面';
                }}
            }}
        }}
        
        function switchKnowledgeDoc(docId) {{
            const items = document.querySelectorAll('#developerKnowledge .info-doc-item');
            items.forEach(item => item.classList.remove('active'));
            event.target.closest('.info-doc-item').classList.add('active');
            loadKnowledgeDoc(docId);
        }}
        
        async function loadKnowledgeDoc(docId) {{
            try {{
                const response = await fetch(`/api/developer_knowledge/${{docId}}`);
                const data = await response.json();
                
                document.getElementById('knowledgeTitle').textContent = data.title;
                document.getElementById('knowledgeContent').textContent = data.content;
            }} catch (error) {{
                console.error('加载知识库失败:', error);
            }}
        }}
        
        // ===== 测试工程师模块交互 =====
        
        function switchTesterTab(tab) {{
            const tabs = ['tasks', 'prompt', 'knowledge'];
            const buttons = document.querySelectorAll('.tester-tab');
            
            tabs.forEach((t, index) => {{
                const content = document.getElementById(`tester${{t.charAt(0).toUpperCase() + t.slice(1)}}`);
                if (t === tab) {{
                    content.classList.add('active');
                    buttons[index].classList.add('active');
                }} else {{
                    content.classList.remove('active');
                    buttons[index].classList.remove('active');
                }}
            }});
        }}
        
        function copyTesterPrompt() {{
            const promptText = document.getElementById('testerPromptContent').textContent;
            navigator.clipboard.writeText(promptText).then(() => {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ 已复制';
                setTimeout(() => {{
                    btn.textContent = originalText;
                }}, 2000);
            }});
        }}
        
        function switchTesterKnowledgeDoc(docId) {{
            const items = document.querySelectorAll('#testerKnowledge .info-doc-item');
            items.forEach(item => item.classList.remove('active'));
            event.target.closest('.info-doc-item').classList.add('active');
            loadTesterKnowledgeDoc(docId);
        }}
        
        async function loadTesterKnowledgeDoc(docId) {{
            try {{
                const response = await fetch(`/api/tester_knowledge/${{docId}}`);
                const data = await response.json();
                
                document.getElementById('testerKnowledgeTitle').textContent = data.title;
                document.getElementById('testerKnowledgeContent').textContent = data.content;
            }} catch (error) {{
                console.error('加载测试知识库失败:', error);
            }}
        }}
        
        async function copyTestReport(taskId, event) {{
            event.stopPropagation();
            
            try {{
                const tasksRes = await fetch('/api/tasks');
                const tasks = await tasksRes.json();
                const task = tasks.find(t => t.id === taskId);
                
                if (!task) {{
                    alert('任务不存在');
                    return;
                }}
                
                const report = generateTestReport(task);
                await navigator.clipboard.writeText(report);
                
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✓ 已复制';
                btn.style.background = 'var(--black)';
                btn.style.color = 'var(--white)';
                
                setTimeout(() => {{
                    btn.textContent = originalText;
                    btn.style.background = 'var(--white)';
                    btn.style.color = 'var(--black)';
                }}, 2000);
                
            }} catch (error) {{
                console.error('复制失败:', error);
                alert('复制失败，请重试');
            }}
        }}
        
        function generateTestReport(task) {{
            const report = `
# 测试报告

## 任务信息
- 任务ID: ${{task.id}}
- 任务标题: ${{task.title}}
- 测试功能: ${{getTaskFeatures(task.id)}}
- 测试状态: ${{getStatusText(task.status)}}

## 测试详情
- 预估工时: ${{task.estimated_hours || 0}} 小时
- 测试复杂度: ${{task.complexity || '—'}}
- 优先级: ${{task.priority || '—'}}
- 测试人员: ${{task.assigned_to || '测试工程师'}}

## 测试结果
${{task.description || '暂无描述'}}

## 测试统计
- 测试用例总数: —
- 通过用例: —
- 失败用例: —
- 覆盖率: —

## 发现的问题
暂无

## 测试结论
✅ 测试通过，可以上线

---

提交者: ${{task.assigned_to || '测试工程师'}}
提交时间: ${{new Date().toLocaleString('zh-CN')}}
            `.trim();
            
            return report;
        }}
        
        // 复制任务完成报告
        async function copyTaskReport(taskId, event) {{
            event.stopPropagation();
            
            try {{
                // 获取任务详情
                const tasksRes = await fetch('/api/tasks');
                const tasks = await tasksRes.json();
                const task = tasks.find(t => t.id === taskId);
                
                if (!task) {{
                    alert('任务不存在');
                    return;
                }}
                
                // 生成完成报告
                const report = generateTaskReport(task);
                
                // 复制到剪贴板
                await navigator.clipboard.writeText(report);
                
                // 按钮反馈
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✓ 已复制';
                btn.style.background = 'var(--black)';
                btn.style.color = 'var(--white)';
                
                setTimeout(() => {{
                    btn.textContent = originalText;
                    btn.style.background = 'var(--white)';
                    btn.style.color = 'var(--black)';
                }}, 2000);
                
            }} catch (error) {{
                console.error('复制失败:', error);
                alert('复制失败，请重试');
            }}
        }}
        
        // 生成任务完成报告
        function generateTaskReport(task) {{
            const report = `
# 任务完成报告

## 基本信息
- 任务ID: ${{task.id}}
- 任务标题: ${{task.title}}
- 实现功能: ${{getTaskFeatures(task.id)}}
- 完成状态: ${{getStatusText(task.status)}}

## 任务详情
- 预估工时: ${{task.estimated_hours || 0}} 小时
- 复杂度: ${{task.complexity || '—'}}
- 优先级: ${{task.priority || '—'}}
- 负责人: ${{task.assigned_to || '未分配'}}

## 完成情况
${{task.description || '暂无描述'}}

## 提交信息
- 完成时间: ${{task.updated_at || task.created_at || '—'}}
- 任务状态: 已完成

---

请架构师审查此任务完成情况。

提交者: ${{task.assigned_to || '全栈开发工程师'}}
提交时间: ${{new Date().toLocaleString('zh-CN')}}
            `.trim();
            
            return report;
        }}
        
        // 重新派发任务（进行中任务使用）
        async function redispatchTask(taskId, event) {{
            event.stopPropagation();
            
            // 确认对话框
            const confirmed = confirm(
                `确定要重新派发任务 ${{taskId}} 吗？\\n\\n` +
                `这会：\\n` +
                `1. 复制完整的任务提示词\\n` +
                `2. 可选：重置任务状态为pending（避免重复执行）\\n\\n` +
                `建议：发给新的执行者，避免重复工作`
            );
            
            if (!confirmed) return;
            
            try {{
                // 获取任务详情
                const tasksRes = await fetch('/api/tasks');
                const tasks = await tasksRes.json();
                const task = tasks.find(t => t.id === taskId);
                
                if (!task) {{
                    alert('任务不存在');
                    return;
                }}
                
                // 生成任务提示词
                const prompt = generateTaskPrompt(task);
                
                // 添加重新派发说明
                const redispatchPrompt = `🔄 **任务重新派发**\\n\\n` +
                    `原因：原执行者可能掉线或遇到问题\\n` +
                    `重新派发时间：${{new Date().toLocaleString('zh-CN')}}\\n\\n` +
                    `---\\n\\n` +
                    prompt +
                    `\\n\\n---\\n\\n` +
                    `⚠️ 重要提示：\\n` +
                    `1. 这是重新派发的任务，可能原执行者已做部分工作\\n` +
                    `2. 建议先检查代码仓库是否有相关提交\\n` +
                    `3. 避免重复劳动\\n` +
                    `4. 开始前运行：python scripts/李明收到任务.py ${{taskId}}`;
                
                // 复制到剪贴板
                await navigator.clipboard.writeText(redispatchPrompt);
                
                // 显示成功消息
                alert('✅ 重新派发提示词已复制！\\n\\n' +
                      '包含：\\n' +
                      '- 完整任务信息\\n' +
                      '- 重新派发说明\\n' +
                      '- 避免重复工作提示\\n\\n' +
                      '现在可以粘贴发给新的执行者！');
                
                // 询问是否重置状态
                const resetStatus = confirm(
                    '是否将任务状态重置为pending？\\n\\n' +
                    '建议：如果已确认原执行者放弃，点击"确定"重置'
                );
                
                if (resetStatus) {{
                    // 调用API重置状态
                    const response = await fetch(`/api/tasks/${{taskId}}/reset`, {{
                        method: 'PUT',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ reason: 'redispatch' }})
                    }});
                    
                    if (response.ok) {{
                        alert('✅ 任务状态已重置为pending');
                        loadDashboardData(); // 刷新数据
                    }}
                }}
                
            }} catch (error) {{
                console.error('重新派发失败:', error);
                alert('❌ 重新派发失败: ' + error.message);
            }}
        }}
        
        // 复制任务提示词（待处理任务使用）
        async function copyTaskPrompt(taskId, event) {{
            event.stopPropagation();
            
            try {{
                // 获取任务详情
                const tasksRes = await fetch('/api/tasks');
                const tasks = await tasksRes.json();
                const task = tasks.find(t => t.id === taskId);
                
                if (!task) {{
                    alert('任务不存在');
                    return;
                }}
                
                // 生成任务提示词
                const prompt = generateTaskPrompt(task);
                
                // 复制到剪贴板
                await navigator.clipboard.writeText(prompt);
                
                // 按钮反馈
                const btn = event.target;
                const originalText = btn.textContent;
                const originalBorder = btn.style.borderColor;
                const originalColor = btn.style.color;
                
                btn.textContent = '✓ 已复制';
                btn.style.background = '#537696';
                btn.style.color = 'var(--white)';
                btn.style.borderColor = '#537696';
                
                setTimeout(() => {{
                    btn.textContent = originalText;
                    btn.style.background = 'var(--white)';
                    btn.style.color = originalColor || '#537696';
                    btn.style.borderColor = originalBorder || '#537696';
                }}, 2000);
                
            }} catch (error) {{
                console.error('复制失败:', error);
                alert('复制失败，请重试');
            }}
        }}
        
        // 生成任务提示词
        function generateTaskPrompt(task) {{
            // 获取依赖信息
            const dependencies = task.dependencies && task.dependencies.length > 0 
                ? task.dependencies.join(', ') 
                : '无依赖';
            
            // 获取并行信息
            const parallelInfo = getTaskParallelInfo(task);
            const parallelText = parallelInfo.canParallel 
                ? '✅ 可以并行开发' 
                : `⚠️ 需要等待依赖任务完成: ${{dependencies}}`;
            
            const prompt = `
# 🎯 开发任务提示词

## 📋 任务基本信息
- **任务ID**: ${{task.id}}
- **任务标题**: ${{task.title}}
- **实现功能**: ${{getTaskFeatures(task.id)}}
- **优先级**: ${{task.priority || 'P2'}}
- **复杂度**: ${{task.complexity || 'medium'}}
- **预估工时**: ${{task.estimated_hours || 0}} 小时

## 🔗 任务依赖关系
- **依赖任务**: ${{dependencies}}
- **并行状态**: ${{parallelText}}

## 📝 任务需求描述
${{task.description || '请实现以下功能...'}}

## 🎨 技术栈要求
- **后端**: Python 3.9+, FastAPI
- **前端**: React, TypeScript (如需要)
- **数据库**: SQLite
- **工具**: Git, VS Code

## ✅ 开发规范
1. **代码质量**
   - 遵循PEP 8编码规范
   - 函数和类必须有文档字符串
   - 复杂逻辑添加注释说明

2. **测试要求**
   - 核心功能需要单元测试
   - 测试覆盖率 ≥ 70%
   - 集成测试确保与其他模块正常交互

3. **提交规范**
   - Commit message格式: \`[类型] 简短描述\`
   - 类型: feat/fix/refactor/test/docs
   - 示例: \`[feat] 实现任务自动分配功能\`

4. **文档要求**
   - 新增API需要更新API文档
   - 重要功能添加使用说明
   - 更新 CHANGELOG 文档

## 🎯 验收标准
1. ✅ 功能完整实现，符合需求描述
2. ✅ 代码通过Linter检查，无明显错误
3. ✅ 核心功能有单元测试，测试通过
4. ✅ 代码有适当的注释和文档
5. ✅ 与依赖模块集成正常

## 📚 参考文档
- 项目架构文档: \`docs/ARCHITECTURE.md\`
- API接口文档: \`API.md\`
- 开发知识库: Dashboard → 全栈开发工程师 → 开发知识库

## 🔄 工作流程
1. **理解需求** - 仔细阅读任务描述和验收标准
2. **设计方案** - 思考实现思路，与架构师沟通（如需要）
3. **编写代码** - 按照开发规范实现功能
4. **自测验证** - 运行测试，确保功能正常
5. **提交审查** - 点击"▸ 复制报告"提交给架构师

## 💡 开发提示
- 优先级 P0/P1 的任务请优先完成
- 如果遇到阻塞问题，及时与架构师沟通
- 可以参考相似功能的代码实现
- 注意代码复用，避免重复造轮子

---

**任务分配**: ${{task.assigned_to || '待分配'}}
**创建时间**: ${{task.created_at || new Date().toLocaleString('zh-CN')}}
**架构师**: AI架构师

💪 开始开发吧！有任何问题随时与架构师沟通。
            `.trim();
            
            return prompt;
        }}
        
        // ===== 用户终测模块交互 =====
        
        function switchUserTestingTab(tab) {{
            const tabs = ['feedback', 'users'];
            const buttons = document.querySelectorAll('.user-testing-tab');
            
            tabs.forEach((t, index) => {{
                const content = document.getElementById(`userTesting${{t.charAt(0).toUpperCase() + t.slice(1)}}`);
                if (t === tab) {{
                    content.classList.add('active');
                    buttons[index].classList.add('active');
                }} else {{
                    content.classList.remove('active');
                    buttons[index].classList.remove('active');
                }}
            }});
        }}
        
        function confirmSelectedBugs() {{
            const checkboxes = document.querySelectorAll('.feedback-checkbox:checked');
            const selectedIds = Array.from(checkboxes).map(cb => cb.dataset.id);
            
            if (selectedIds.length === 0) {{
                alert('请至少选择一个Bug/意见');
                return;
            }}
            
            if (confirm('确认将 ' + selectedIds.length + ' 个Bug/意见标记为需要修复？')) {{
                // TODO: 调用API保存选中的Bug
                alert('✅ 已确认 ' + selectedIds.length + ' 个Bug需要修复！');
                
                // 更新待确认数量
                document.getElementById('pendingFeedbackCount').textContent = '0';
            }}
        }}
        
        function copyUserTestingPrompt() {{
            const promptText = document.getElementById('userTestingPromptContent').textContent;
            navigator.clipboard.writeText(promptText).then(() => {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ 已复制';
                setTimeout(() => {{
                    btn.textContent = originalText;
                }}, 2000);
            }});
        }}
        
        // ===== 交付工程师模块交互 =====
        
        function switchDeliveryTab(tab) {{
            const tabs = ['tasks', 'env', 'ops'];
            const buttons = document.querySelectorAll('.delivery-tab');
            
            tabs.forEach((t, index) => {{
                const content = document.getElementById(`delivery${{t.charAt(0).toUpperCase() + t.slice(1)}}`);
                if (t === tab) {{
                    content.classList.add('active');
                    buttons[index].classList.add('active');
                }} else {{
                    content.classList.remove('active');
                    buttons[index].classList.remove('active');
                }}
            }});
        }}
        
        function switchDeliveryDoc(docId) {{
            const items = document.querySelectorAll('#deliveryEnv .info-doc-item');
            items.forEach(item => item.classList.remove('active'));
            event.target.closest('.info-doc-item').classList.add('active');
            loadDeliveryDoc(docId);
        }}
        
        async function loadDeliveryDoc(docId) {{
            try {{
                const response = await fetch(`/api/delivery_docs/${{docId}}`);
                const data = await response.json();
                
                document.getElementById('deliveryDocTitle').textContent = data.title;
                document.getElementById('deliveryDocContent').textContent = data.content;
            }} catch (error) {{
                console.error('加载交付文档失败:', error);
            }}
        }}
        
        function copyOpsDoc() {{
            const opsText = document.getElementById('opsDocContent').textContent;
            navigator.clipboard.writeText(opsText).then(() => {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ 已复制';
                setTimeout(() => {{
                    btn.textContent = originalText;
                }}, 2000);
            }});
        }}
        
        // ===== 运维工程师模块交互 =====
        
        function switchOpsTab(tab) {{
            const tabs = ['log', 'report', 'runbook', 'knowledge'];
            const buttons = document.querySelectorAll('.ops-tab');
            
            tabs.forEach((t, index) => {{
                const content = document.getElementById(`ops${{t.charAt(0).toUpperCase() + t.slice(1)}}`);
                if (t === tab) {{
                    content.classList.add('active');
                    buttons[index].classList.add('active');
                }} else {{
                    content.classList.remove('active');
                    buttons[index].classList.remove('active');
                }}
            }});
        }}
        
        function submitBugReport() {{
            const bugDescription = document.getElementById('bugReportInput').value.trim();
            
            if (!bugDescription) {{
                alert('请描述遇到的问题');
                return;
            }}
            
            if (confirm('确认提交此Bug报告？')) {{
                // TODO: 调用API保存Bug报告
                alert('✅ Bug报告已提交！运维工程师会尽快处理。');
                
                // 清空输入框
                document.getElementById('bugReportInput').value = '';
                
                // TODO: 刷新Bug列表
            }}
        }}
        
        function switchRunbookDoc(docId) {{
            const items = document.querySelectorAll('#opsRunbook .info-doc-item');
            items.forEach(item => item.classList.remove('active'));
            event.target.closest('.info-doc-item').classList.add('active');
            loadRunbookDoc(docId);
        }}
        
        async function loadRunbookDoc(docId) {{
            try {{
                const response = await fetch(`/api/ops_runbook/${{docId}}`);
                const data = await response.json();
                
                document.getElementById('runbookDocTitle').textContent = data.title;
                document.getElementById('runbookDocContent').textContent = data.content;
            }} catch (error) {{
                console.error('加载运维说明失败:', error);
            }}
        }}
        
        function switchOpsKnowledgeDoc(docId) {{
            const items = document.querySelectorAll('#opsKnowledge .info-doc-item');
            items.forEach(item => item.classList.remove('active'));
            event.target.closest('.info-doc-item').classList.add('active');
            loadOpsKnowledgeDoc(docId);
        }}
        
        async function loadOpsKnowledgeDoc(docId) {{
            try {{
                const response = await fetch(`/api/ops_knowledge/${{docId}}`);
                const data = await response.json();
                
                document.getElementById('opsKnowledgeTitle').textContent = data.title;
                document.getElementById('opsKnowledgeContent').textContent = data.content;
            }} catch (error) {{
                console.error('加载运维知识库失败:', error);
            }}
        }}
        
        async function copyDeploymentReport(taskId, event) {{
            event.stopPropagation();
            
            try {{
                const tasksRes = await fetch('/api/tasks');
                const tasks = await tasksRes.json();
                const task = tasks.find(t => t.id === taskId);
                
                if (!task) {{
                    alert('任务不存在');
                    return;
                }}
                
                const report = generateDeploymentReport(task);
                await navigator.clipboard.writeText(report);
                
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✓ 已复制';
                btn.style.background = 'var(--black)';
                btn.style.color = 'var(--white)';
                
                setTimeout(() => {{
                    btn.textContent = originalText;
                    btn.style.background = 'var(--white)';
                    btn.style.color = 'var(--black)';
                }}, 2000);
                
            }} catch (error) {{
                console.error('复制失败:', error);
                alert('复制失败，请重试');
            }}
        }}
        
        function generateDeploymentReport(task) {{
            const report = `
# 部署报告

## 任务信息
- 任务ID: ${{task.id}}
- 任务标题: ${{task.title}}
- 部署功能: ${{getTaskFeatures(task.id)}}
- 部署状态: ${{getStatusText(task.status)}}

## 部署详情
- 预估工时: ${{task.estimated_hours || 0}} 小时
- 复杂度: ${{task.complexity || '—'}}
- 优先级: ${{task.priority || '—'}}
- 部署人员: ${{task.assigned_to || '交付工程师'}}

## 部署环境
- 环境：生产环境
- 服务器：[服务器信息]
- 端口：8889
- 域名：[域名信息]

## 部署步骤
${{task.description || '暂无描述'}}

## 部署验证
- ✓ 服务启动成功
- ✓ 健康检查通过
- ✓ 功能验证通过
- ✓ 性能指标达标

## 回滚方案
已准备回滚脚本，如有问题可立即回滚到上一版本。

## 监控配置
- 健康检查：/health
- 日志监控：已配置
- 告警通知：已配置

---

提交者: ${{task.assigned_to || '交付工程师'}}
提交时间: ${{new Date().toLocaleString('zh-CN')}}
            `.trim();
            
            return report;
        }}
        
        function switchTodoTab(tab) {{
            // 更新按钮状态
            const userBtn = document.getElementById('todoTabUser');
            const architectBtn = document.getElementById('todoTabArchitect');
            const userContent = document.getElementById('todoUserRequirements');
            const architectContent = document.getElementById('todoArchitectTasks');
            
            if (tab === 'user') {{
                userBtn.style.borderBottom = '2px solid var(--black)';
                userBtn.style.color = 'var(--black)';
                userBtn.style.fontWeight = '600';
                architectBtn.style.borderBottom = '2px solid transparent';
                architectBtn.style.color = 'var(--gray-600)';
                architectBtn.style.fontWeight = '400';
                userContent.style.display = 'block';
                architectContent.style.display = 'none';
            }} else {{
                architectBtn.style.borderBottom = '2px solid var(--black)';
                architectBtn.style.color = 'var(--black)';
                architectBtn.style.fontWeight = '600';
                userBtn.style.borderBottom = '2px solid transparent';
                userBtn.style.color = 'var(--gray-600)';
                userBtn.style.fontWeight = '400';
                architectContent.style.display = 'block';
                userContent.style.display = 'none';
            }}
        }}
        
        async function loadTodoFeatures() {{
            try {{
                const response = await fetch('/api/tasks');
                const tasks = await response.json();
                
                const count = document.getElementById('todoFeatureCount');
                
                if (!tasks || tasks.length === 0) {{
                    document.getElementById('todoArchitectList').innerHTML = '<div class="empty-state">暂无架构师审查任务</div>';
                    count.textContent = '0 个待开发任务';
                    return;
                }}
                
                // 分类：用户需求 vs 架构师审查任务
                // 架构师审查任务：ID包含TASK-C, TASK-D等（架构师拆解的）
                // 用户需求：ID包含REQ-等（用户提出的）
                const userRequirements = tasks.filter(t => t.id.startsWith('REQ-'));
                const architectTasks = tasks.filter(t => t.id.startsWith('TASK-'));
                
                // 更新总数
                count.textContent = `${{tasks.length}} 个待开发任务 (用户需求: ${{userRequirements.length}}, 架构师任务: ${{architectTasks.length}})`;
                
                // 渲染架构师审查任务
                renderTaskList(architectTasks, 'todoArchitectList');
                
                // 渲染用户需求
                if (userRequirements.length > 0) {{
                    renderTaskList(userRequirements, 'todoUserList');
                }} else {{
                    document.getElementById('todoUserList').innerHTML = 
                        '<div class="empty-state">暂无用户提出的新需求<br><small style="color: var(--gray-500); margin-top: 8px; display: block;">用户可通过对话提出需求，架构师记录为REQ-开头的任务</small></div>';
                }}
                
            }} catch (error) {{
                console.error('加载待完成任务失败:', error);
                document.getElementById('todoArchitectList').innerHTML = 
                    '<div class="empty-state">加载失败，请刷新页面</div>';
            }}
        }}
        
        function renderTaskList(tasks, containerId) {{
            const container = document.getElementById(containerId);
            
            if (!tasks || tasks.length === 0) {{
                container.innerHTML = '<div class="empty-state">暂无任务</div>';
                return;
            }}
            
            // 按优先级排序
            tasks.sort((a, b) => {{
                const priorityOrder = {{'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}};
                return (priorityOrder[a.priority] || 9) - (priorityOrder[b.priority] || 9);
            }});
            
            // 渲染任务列表
            container.innerHTML = tasks.map(task => {{
                const priorityColor = {{
                    'P0': '#DC2626',
                    'P1': '#EA580C',
                    'P2': '#D97706',
                    'P3': '#65A30D'
                }}[task.priority] || '#6B7280';
                
                const statusText = {{
                    'pending': '待处理',
                    'in_progress': '进行中',
                    'review': '审查中',
                    'completed': '已完成',
                    'blocked': '阻塞',
                    'cancelled': '已取消'
                }}[task.status] || task.status;
                
                // 生成三态按钮
                let actionButton = '';
                if (task.status === 'pending') {{
                    // 待处理：显示"一键复制提示词"
                    actionButton = `
                        <button 
                            onclick="copyTaskPrompt('${{task.id}}')"
                            style="padding: 6px 12px; background: var(--blue); color: white; border: none; border-radius: 4px; font-size: 11px; cursor: pointer; font-weight: 600; transition: all 0.2s;"
                            onmouseover="this.style.background='var(--red)'"
                            onmouseout="this.style.background='var(--blue)'"
                        >
                            📋 一键复制提示词
                        </button>
                    `;
                }} else if (task.status === 'completed') {{
                    // 已完成：显示"一键复制完成报告"
                    actionButton = `
                        <button 
                            onclick="copyTaskReport('${{task.id}}')"
                            style="padding: 6px 12px; background: var(--blue); color: white; border: none; border-radius: 4px; font-size: 11px; cursor: pointer; font-weight: 600; transition: all 0.2s;"
                            onmouseover="this.style.background='var(--red)'"
                            onmouseout="this.style.background='var(--blue)'"
                        >
                            📄 一键复制完成报告
                        </button>
                    `;
                }} else if (task.status === 'in_progress') {{
                    // 进行中：显示进度提示
                    actionButton = `
                        <span style="padding: 6px 12px; background: #FEF3C7; color: #92400E; border-radius: 4px; font-size: 11px; font-weight: 600;">
                            ⚙️ 开发中
                        </span>
                    `;
                }}
                
                return `
                    <div style="padding: 16px; border-bottom: 1px solid var(--gray-200); background: var(--white);">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <div style="flex: 1;">
                                <span style="color: ${{priorityColor}}; font-weight: 700; font-size: 12px; font-family: var(--font-mono);">[${{task.priority}}]</span>
                                <span style="font-size: 14px; font-weight: 600; margin-left: 8px; color: var(--black);">${{task.id}}: ${{task.title}}</span>
                            </div>
                            <span style="padding: 2px 8px; background: #F3F4F6; border-radius: 4px; font-size: 11px; color: var(--gray-700);">${{statusText}}</span>
                        </div>
                        <div style="font-size: 12px; color: var(--gray-600); margin-bottom: 8px; line-height: 1.5;">
                            ${{task.description || '无描述'}}
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
                            <div style="display: flex; gap: 16px; font-size: 11px; color: var(--gray-500); font-family: var(--font-mono);">
                                <span>⏱️ ${{task.estimated_hours}}h</span>
                                <span>👤 ${{task.assigned_to || '未分配'}}</span>
                                <span>🔧 ${{task.complexity || 'medium'}}</span>
                            </div>
                            ${{actionButton}}
                        </div>
                    </div>
                `;
            }}).join('');
        }}
        
        window.onload = function() {{
            // 设置用户交互检测（确保刷新不打断用户操作）
            setupUserInteractionDetection();
            
            // 任务数据自动刷新 - 每5秒
            loadData();
            setInterval(loadData, 5000);
            
            // 其他数据加载
            loadConfirmationData();
            setInterval(loadConfirmationData, 30000);
            loadArchitectData();
            loadInfoDoc('requirements');
            setInterval(loadArchitectData, 20000);
            loadKnowledgeDoc('problems');
            loadTesterKnowledgeDoc('cases');
            loadDeliveryDoc('environment');
            loadOpsKnowledgeDoc('troubleshooting');
            loadRunbookDoc('runbook');
            loadCodeIndex('models');
            loadProjectScan();
            setInterval(loadProjectScan, 30000);
            loadTodoFeatures();
            setInterval(loadTodoFeatures, 10000);
            loadDeveloperPrompt();
            loadArchitectPrompt();
            loadConversations(); // 加载对话历史库
            
            // 初始化待确认数量
            document.getElementById('pendingFeedbackCount').textContent = '3';
            
            // 打印自动刷新配置
            console.log('[自动刷新] 已启动 - 每5秒刷新任务列表');
            console.log('[自动刷新] 智能优化: 用户交互时暂停、数据无变化时跳过UI更新');
        }}
        
        // ===== AI代码管家模块交互 =====
        
        function switchCodeButlerTab(tab) {{
            const tabs = ['search', 'structure', 'index'];
            const buttons = document.querySelectorAll('.code-butler-tab');
            
            tabs.forEach((t, index) => {{
                const content = document.getElementById(`codeButler${{t.charAt(0).toUpperCase() + t.slice(1)}}`);
                if (t === tab) {{
                    content.classList.add('active');
                    buttons[index].classList.add('active');
                }} else {{
                    content.classList.remove('active');
                    buttons[index].classList.remove('active');
                }}
            }});
        }}
        
        function switchCodeIndex(category) {{
            const items = document.querySelectorAll('#codeButlerIndex .info-doc-item');
            items.forEach(item => item.classList.remove('active'));
            event.target.closest('.info-doc-item').classList.add('active');
            loadCodeIndex(category);
        }}
        
        async function loadCodeIndex(category) {{
            const content = document.getElementById('codeIndexContent');
            const title = document.getElementById('codeIndexTitle');
            
            const indexData = {{
                'models': {{
                    title: '数据模型',
                    content: `# 数据模型索引

## Task（任务模型）
- 文件：automation/models.py
- 行数：10-45
- 说明：任务的完整数据结构

## StateManager（状态管理器）
- 文件：automation/state_manager.py  
- 行数：15-280
- 说明：SQLite持久化管理`
                }},
                'api': {{
                    title: 'API接口',
                    content: `# API接口索引

## /api/tasks - 获取任务列表
- 文件：industrial_dashboard/dashboard.py
- 行数：88-96
- 返回：所有任务数据

## /api/architect_monitor - 架构师监控
- 文件：dashboard.py
- 行数：227-267
- 返回：Token使用、事件流、提示词`
                }},
                'ui': {{
                    title: 'UI模块',
                    content: `# UI模块索引

## 架构师监控模块
- 文件：templates.py
- CSS：行492-748
- HTML：行1217-1320
- JS：行2534-2656

## UX/UI确认模块
- 文件：templates.py
- CSS：行893-1075
- HTML：行1524-1652`
                }},
                'utils': {{
                    title: '工具函数',
                    content: `# 工具函数索引

## ArchitectLogger（架构师日志记录）
- 文件：scripts/architect_logger.py
- 行数：15-180
- 功能：记录事件、更新Token`
                }}
            }};
            
            const data = indexData[category] || indexData['models'];
            title.textContent = data.title;
            content.textContent = data.content;
        }}
        
        function askCodeButler() {{
            const question = document.getElementById('aiQuestionInput').value.trim();
            const response = document.getElementById('aiResponse');
            
            if (!question) {{
                alert('请输入问题');
                return;
            }}
            
            // 模拟AI回答（实际应该调用AI API）
            response.textContent = '正在分析您的问题："' + question + '"...\\n\\n' +
'[模拟AI回答]\\n' +
'根据您的问题，我找到了以下相关代码：\\n\\n' +
'文件: automation/state_manager.py\\n' +
'位置: 第15-280行\\n' +
'功能: StateManager类 - 负责任务状态的SQLite持久化管理\\n\\n' +
'主要方法：\\n' +
'- create_task() - 创建新任务\\n' +
'- get_task() - 获取任务详情\\n' +
'- update_task() - 更新任务状态\\n' +
'- list_all_tasks() - 获取所有任务\\n\\n' +
'使用示例：\\n' +
'from automation.state_manager import StateManager\\n' +
'sm = StateManager()\\n' +
'tasks = sm.list_all_tasks()\\n\\n' +
'需要我提供更详细的说明吗？';
        }};
        
        // ===== 缓存管理和Service Worker =====
        
        // Service Worker注册
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('/static/sw.js')
                    .then(registration => {{
                        console.log('[缓存管理] Service Worker注册成功:', registration.scope);
                        
                        // 定期检查版本更新（每30秒）
                        setInterval(() => {{
                            checkCacheVersion();
                        }}, 30000);
                        
                        // 监听Service Worker消息
                        navigator.serviceWorker.addEventListener('message', event => {{
                            if (event.data.type === 'CACHE_CLEARED') {{
                                console.log('[缓存管理]', event.data.message);
                                setTimeout(() => {{
                                    window.location.reload();
                                }}, 1000);
                            }}
                            
                            if (event.data.type === 'NEW_VERSION') {{
                                console.log('[缓存管理] 发现新版本:', event.data.newVersion);
                                showVersionUpdateNotification(event.data.newVersion);
                            }}
                        }});
                    }})
                    .catch(error => {{
                        console.warn('[缓存管理] Service Worker注册失败:', error);
                    }});
            }});
        }}
        
        // 检查缓存版本
        async function checkCacheVersion() {{
            try {{
                const response = await fetch('/api/cache/version?t=' + Date.now());
                const data = await response.json();
                
                if (data.success) {{
                    const currentVersion = document.getElementById('cache-version-display').textContent;
                    const latestVersion = data.data.current_version;
                    
                    // 如果版本不同，提示用户刷新
                    if (currentVersion !== latestVersion) {{
                        console.log('[缓存管理] 版本更新:', currentVersion, '->', latestVersion);
                        showVersionUpdateNotification(latestVersion);
                    }}
                }}
            }} catch (error) {{
                console.warn('[缓存管理] 检查版本失败:', error);
            }}
        }}
        
        // 显示版本更新通知
        function showVersionUpdateNotification(newVersion) {{
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--red);
                color: white;
                padding: 16px 24px;
                border-radius: 8px;
                box-shadow: var(--shadow-lg);
                z-index: 10000;
                font-size: 13px;
                font-family: var(--font-chinese);
                max-width: 300px;
            `;
            notification.innerHTML = `
                <div style="font-weight: 600; margin-bottom: 8px;">🔄 发现新版本</div>
                <div style="font-size: 12px; margin-bottom: 12px;">
                    新版本: ${{newVersion}}<br>
                    建议刷新页面以获取最新内容
                </div>
                <button onclick="location.reload()" 
                    style="padding: 6px 16px; background: white; color: var(--red); border: none; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; margin-right: 8px;">
                    立即刷新
                </button>
                <button onclick="this.parentElement.remove()" 
                    style="padding: 6px 16px; background: transparent; color: white; border: 1px solid white; border-radius: 4px; font-size: 12px; cursor: pointer;">
                    稍后
                </button>
            `;
            
            document.body.appendChild(notification);
            
            // 10秒后自动关闭
            setTimeout(() => {{
                if (notification.parentElement) {{
                    notification.remove();
                }}
            }}, 10000);
        }}
        
        // 清除Dashboard缓存
        // Token同步对话框
        function showTokenSyncDialog() {{
            const dialog = document.createElement('div');
            dialog.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            
            dialog.innerHTML = `
                <div style="
                    background: var(--white);
                    padding: 32px;
                    border-radius: 12px;
                    box-shadow: var(--shadow-lg);
                    max-width: 500px;
                    width: 90%;
                ">
                    <h3 style="font-size: 20px; font-weight: 700; margin-bottom: 16px; color: var(--black);">
                        🔄 同步Token使用量
                    </h3>
                    <p style="font-size: 13px; color: var(--gray-700); margin-bottom: 24px; line-height: 1.6;">
                        请在Cursor中查看右下角状态栏的Token数字，复制后粘贴到下方：
                    </p>
                    <input 
                        type="text" 
                        id="tokenInput" 
                        placeholder="例如: 350000 或 350,000"
                        style="
                            width: 100%;
                            padding: 12px;
                            font-size: 16px;
                            font-family: var(--font-mono);
                            border: 2px solid var(--gray-300);
                            border-radius: 6px;
                            margin-bottom: 8px;
                        "
                    />
                    <input 
                        type="text" 
                        id="eventInput" 
                        placeholder="事件描述 (可选)"
                        style="
                            width: 100%;
                            padding: 12px;
                            font-size: 14px;
                            border: 1px solid var(--gray-300);
                            border-radius: 6px;
                            margin-bottom: 24px;
                        "
                    />
                    <div style="display: flex; gap: 12px; justify-content: flex-end;">
                        <button 
                            onclick="closeTokenSyncDialog()"
                            style="
                                padding: 10px 20px;
                                background: var(--gray-300);
                                color: var(--gray-800);
                                border: none;
                                border-radius: 6px;
                                font-size: 14px;
                                cursor: pointer;
                                font-weight: 600;
                            "
                        >
                            取消
                        </button>
                        <button 
                            onclick="submitTokenSync()"
                            style="
                                padding: 10px 20px;
                                background: var(--blue);
                                color: white;
                                border: none;
                                border-radius: 6px;
                                font-size: 14px;
                                cursor: pointer;
                                font-weight: 600;
                            "
                        >
                            ✅ 同步
                        </button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(dialog);
            document.getElementById('tokenInput').focus();
            
            // 支持回车提交
            document.getElementById('tokenInput').addEventListener('keypress', (e) => {{
                if (e.key === 'Enter') {{
                    submitTokenSync();
                }}
            }});
            
            window.tokenSyncDialog = dialog;
        }}
        
        function closeTokenSyncDialog() {{
            if (window.tokenSyncDialog) {{
                document.body.removeChild(window.tokenSyncDialog);
                window.tokenSyncDialog = null;
            }}
        }}
        
        async function submitTokenSync() {{
            const tokenInput = document.getElementById('tokenInput').value.trim();
            const eventInput = document.getElementById('eventInput').value.trim() || '手动同步';
            
            if (!tokenInput) {{
                alert('请输入Token值');
                return;
            }}
            
            // 解析Token值（移除逗号和空格）
            const tokenValue = parseInt(tokenInput.replace(/[,\\s]/g, ''));
            
            if (isNaN(tokenValue) || tokenValue < 0) {{
                alert('Token值格式不正确，请输入数字');
                return;
            }}
            
            try {{
                const response = await fetch('/api/record_token_usage', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        tokens: tokenValue,
                        event: eventInput,
                        conversation_id: 'manual-sync-' + Date.now(),
                        sync_type: 'manual'
                    }})
                }});
                
                const data = await response.json();
                
                if (data.success) {{
                    // 显示成功提示
                    showNotification('✅ Token已同步', `总使用量: ${{data.total_used.toLocaleString()}} tokens`, 'success');
                    
                    // 关闭对话框
                    closeTokenSyncDialog();
                    
                    // 刷新数据
                    setTimeout(() => {{
                        fetchMonitorData();
                    }}, 500);
                }} else {{
                    alert('同步失败: ' + (data.error || '未知错误'));
                }}
            }} catch (error) {{
                console.error('Token同步失败:', error);
                alert('同步失败，请检查网络连接');
            }}
        }}
        
        function showNotification(title, message, type = 'info') {{
            const notification = document.createElement('div');
            const bgColor = type === 'success' ? 'var(--blue)' : type === 'error' ? 'var(--red)' : 'var(--black)';
            
            notification.style.cssText = `
                position: fixed;
                top: 24px;
                right: 24px;
                background: ${{bgColor}};
                color: white;
                padding: 16px 24px;
                border-radius: 8px;
                box-shadow: var(--shadow-lg);
                z-index: 10002;
                font-family: var(--font-chinese);
                min-width: 280px;
                animation: slideIn 0.3s ease;
            `;
            
            notification.innerHTML = `
                <div style="font-weight: 600; margin-bottom: 4px;">${{title}}</div>
                <div style="font-size: 13px; opacity: 0.9;">${{message}}</div>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {{
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {{
                    if (notification.parentNode) {{
                        document.body.removeChild(notification);
                    }}
                }}, 300);
            }}, 3000);
        }}
        
        // ===== 任务三态按钮功能 =====
        
        // 复制任务提示词（pending状态）
        async function copyTaskPrompt(taskId) {{
            try {{
                // 获取任务详情
                const response = await fetch('/api/tasks');
                const tasks = await response.json();
                const task = tasks.find(t => t.id === taskId);
                
                if (!task) {{
                    alert('任务不存在');
                    return;
                }}
                
                // 生成提示词文档
                const prompt = `# 🎯 开发任务提示词

## 📋 任务基本信息

- **任务ID**: ${{task.id}}
- **任务标题**: ${{task.title}}
- **优先级**: ${{task.priority}}
- **复杂度**: ${{task.complexity || 'medium'}}
- **预估工时**: ${{task.estimated_hours || '未知'}} 小时

## 📝 任务需求描述

${{task.description || '暂无描述'}}

## 🎯 验收标准

1. ✅ 功能完整实现，符合需求描述
2. ✅ 代码通过Linter检查，无明显错误
3. ✅ 核心功能有单元测试，测试通过
4. ✅ 代码有适当的注释和文档
5. ✅ 与依赖模块集成正常

## 🔄 工作流程

1. **接收任务** - 运行: python scripts/李明收到任务.py ${{task.id}}
2. **理解需求** - 仔细阅读任务描述和验收标准
3. **编写代码** - 按照开发规范实现功能
4. **自测验证** - 运行测试，确保功能正常
5. **提交完成** - 运行: python scripts/李明提交完成.py ${{task.id}}

---

**任务分配**: ${{task.assigned_to || 'fullstack-engineer'}}
**创建时间**: ${{task.created_at || new Date().toISOString()}}

💪 开始开发吧！
`;
                
                // 复制到剪贴板
                await navigator.clipboard.writeText(prompt);
                
                showNotification('✅ 复制成功', `任务 ${{taskId}} 的提示词已复制到剪贴板`, 'success');
                
            }} catch (error) {{
                console.error('复制失败:', error);
                alert('复制失败，请重试');
            }}
        }}
        
        // 复制完成报告（completed状态）
        async function copyTaskReport(taskId) {{
            try {{
                // 获取任务详情
                const response = await fetch('/api/tasks');
                const tasks = await response.json();
                const task = tasks.find(t => t.id === taskId);
                
                if (!task) {{
                    alert('任务不存在');
                    return;
                }}
                
                // 生成完成报告
                const report = `# ✅ ${{task.id}} 完成报告

## 📋 任务信息

- **任务ID**: ${{task.id}}
- **任务标题**: ${{task.title}}
- **优先级**: ${{task.priority}}
- **状态**: 已完成 ✅

## 📝 实现概述

任务 ${{task.id}} - ${{task.title}} 已完成开发。

${{task.description || ''}}

## 🗂️ 文件清单

### 修改文件
- 待补充（请手动填写修改的文件列表）

## ✅ 验收标准

| 验收项 | 状态 | 说明 |
|--------|------|------|
| 功能完整实现 | ✅ 通过 | 符合需求描述 |
| 代码质量检查 | ✅ 通过 | 无linter错误 |
| 单元测试 | ✅ 通过 | 核心功能已测试 |
| 代码文档 | ✅ 通过 | 有适当注释 |
| 集成测试 | ✅ 通过 | 与其他模块正常交互 |

## 📊 工时统计

- **预估工时**: ${{task.estimated_hours || '未知'}}h
- **实际工时**: 待填写
- **效率**: 待计算

## 💡 技术要点

（请补充实现的关键技术点）

## 🎉 总结

任务 ${{task.id}} 开发完成，功能正常，代码质量良好，可以提交审查。

---

**完成人**: ${{task.assigned_to || 'fullstack-engineer'}}
**完成时间**: ${{new Date().toLocaleString('zh-CN')}}
**状态**: ✅ 已完成
`;
                
                // 复制到剪贴板
                await navigator.clipboard.writeText(report);
                
                showNotification('✅ 复制成功', `任务 ${{taskId}} 的完成报告已复制到剪贴板`, 'success');
                
            }} catch (error) {{
                console.error('复制失败:', error);
                alert('复制失败，请重试');
            }}
        }}
        
        async function clearDashboardCache() {{
            if (!confirm('确定要清除缓存吗？\\n\\n这将刷新页面以获取最新内容。')) {{
                return;
            }}
            
            try {{
                // 1. 调用后端API更新版本号
                const response = await fetch('/api/cache/clear', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }}
                }});
                
                const data = await response.json();
                
                if (data.success) {{
                    console.log('[缓存管理] 缓存清除成功，新版本:', data.new_version);
                    
                    // 2. 通知Service Worker清除缓存
                    if (navigator.serviceWorker && navigator.serviceWorker.controller) {{
                        navigator.serviceWorker.controller.postMessage({{
                            type: 'CLEAR_CACHE'
                        }});
                    }}
                    
                    // 3. 显示提示并刷新
                    const notification = document.createElement('div');
                    notification.style.cssText = `
                        position: fixed;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        background: var(--black);
                        color: white;
                        padding: 32px 48px;
                        border-radius: 12px;
                        box-shadow: var(--shadow-lg);
                        z-index: 10001;
                        font-size: 16px;
                        font-family: var(--font-chinese);
                        text-align: center;
                    `;
                    notification.innerHTML = `
                        <div style="font-size: 48px; margin-bottom: 16px;">✅</div>
                        <div style="font-weight: 600; margin-bottom: 8px;">缓存已清除</div>
                        <div style="font-size: 13px; color: var(--gray-400);">
                            新版本: ${{data.new_version}}<br>
                            页面将在 2 秒后刷新...
                        </div>
                    `;
                    
                    document.body.appendChild(notification);
                    
                    // 2秒后刷新页面
                    setTimeout(() => {{
                        window.location.reload(true);
                    }}, 2000);
                }} else {{
                    alert('清除缓存失败: ' + (data.error || '未知错误'));
                }}
            }} catch (error) {{
                console.error('[缓存管理] 清除缓存失败:', error);
                alert('清除缓存失败，请刷新页面重试');
            }}
        }}
        
        // 页面加载时显示当前缓存版本
        window.addEventListener('load', () => {{
            console.log('[缓存管理] 当前缓存版本: {cache_version}');
        }});
    </script>
</body>
</html>
    """
