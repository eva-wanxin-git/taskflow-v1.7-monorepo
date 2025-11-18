"""
Industrial Dashboard 核心类 - 支持多版本

工业美学风格的监控面板，支持动态版本管理
"""
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Optional
from pathlib import Path
import json
from datetime import datetime
import sys

# 添加版本缓存管理器
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "packages" / "shared-utils"))
from version_cache_manager import get_version_manager

from .data_provider import DataProvider
from .templates import get_dashboard_html
from .event_stream_provider import EventStreamProvider


class IndustrialDashboard:
    """工业美学 Dashboard"""
    
    def __init__(
        self,
        data_provider: DataProvider,
        title: str = "AI Task Automation System",
        subtitle: str = "Industrial Dashboard",
        port: int = 8888,
        host: str = "127.0.0.1",
        auto_reload: bool = False
    ):
        self.data_provider = data_provider
        self.title = title
        self.subtitle = subtitle
        self.port = port
        self.host = host
        self.auto_reload = auto_reload
        
        # 初始化版本管理器
        # 使用项目根目录的automation-data
        project_root = Path(__file__).parent.parent.parent.parent.parent
        version_file = project_root / "automation-data" / "dashboard_version.json"
        self.version_manager = get_version_manager(str(version_file))
        print(f"[版本管理] 当前版本: {self.version_manager.get_version()}")
        print(f"[版本管理] 数据文件: {version_file}")
        
        # 初始化事件流提供器
        self.event_stream_provider = EventStreamProvider()
        print(f"[事件流] Event Stream Provider 已初始化")
        
        self.app = FastAPI(title=title)
        self._setup_routes()
        self._setup_static_files()
    
    def _get_versions(self):
        """获取版本列表"""
        versions_file = Path("automation-data/versions.json")
        if versions_file.exists():
            with open(versions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("versions", [])
        return [{"id": "v1", "name": "版本 1", "description": "MVP基础版本", "subtitle": "MVP基础"}]
    
    def _setup_static_files(self):
        """配置静态文件服务"""
        # 使用模块所在目录的static子目录
        static_dir = Path(__file__).parent / "static"
        static_dir.mkdir(exist_ok=True)
        
        # 创建ux和ui子目录
        (static_dir / "ux").mkdir(exist_ok=True)
        (static_dir / "ui").mkdir(exist_ok=True)
        
        # 挂载静态文件服务
        if static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
            print(f"[OK] 静态文件目录: {static_dir}")
    
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard(response: Response):
            # 设置强制不缓存的HTTP头
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            
            # 传递版本号到模板
            html = get_dashboard_html(
                self.title, 
                self.subtitle, 
                cache_version=self.version_manager.get_version()
            )
            return html
        
        @self.app.get("/api/versions")
        async def get_versions():
            """获取版本列表"""
            try:
                versions = self._get_versions()
                return JSONResponse(content={"versions": versions})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/stats")
        async def get_stats():
            try:
                stats = self.data_provider.get_stats()
                return JSONResponse(content=stats.to_dict())
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/tasks")
        async def get_tasks():
            try:
                tasks = self.data_provider.get_tasks()
                tasks_dict = [task.to_dict() for task in tasks]
                tasks_dict.sort(key=lambda x: x.get('created_at', ''), reverse=True)
                return JSONResponse(content=tasks_dict)
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/health")
        async def health_check():
            from datetime import datetime
            return {"status": "healthy", "timestamp": datetime.now().isoformat()}
        
        @self.app.get("/events", response_class=HTMLResponse)
        async def event_stream_page():
            """事件流可视化页面（v2增强版）"""
            try:
                template_path = Path(__file__).parent / "event_stream_template_v2.html"
                if template_path.exists():
                    with open(template_path, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    # 如果v2不存在，回退到v1
                    template_path_v1 = Path(__file__).parent / "event_stream_template.html"
                    if template_path_v1.exists():
                        with open(template_path_v1, 'r', encoding='utf-8') as f:
                            return f.read()
                    return "<h1>事件流模板未找到</h1>"
            except Exception as e:
                return f"<h1>加载事件流页面失败</h1><p>{str(e)}</p>"
        
        @self.app.get("/api/ux_confirmation")
        async def get_ux_confirmation():
            """
            获取UX确认数据
            
            Returns:
                {
                    "images": [
                        {"url": "/static/ux/login.png", "label": "登录页原型"},
                        {"url": "/static/ux/dashboard.png", "label": "仪表盘原型"}
                    ],
                    "prompt": "UX设计提示词内容...",
                    "status": "pending" | "approved"
                }
            """
            try:
                data_file = Path("automation-data/design_confirmations.json")
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return JSONResponse(content=data.get("ux", {
                            "images": [],
                            "prompt": "暂无UX提示词",
                            "status": "pending"
                        }))
                return JSONResponse(content={
                    "images": [],
                    "prompt": "暂无UX提示词",
                    "status": "pending"
                })
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/ui_confirmation")
        async def get_ui_confirmation():
            """
            获取UI确认数据
            
            Returns:
                {
                    "images": [
                        {"url": "/static/ui/login.png", "label": "登录页效果图"},
                        {"url": "/static/ui/dashboard.png", "label": "仪表盘效果图"}
                    ],
                    "prompt": "UI设计提示词内容...",
                    "status": "pending" | "approved"
                }
            """
            try:
                data_file = Path("automation-data/design_confirmations.json")
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return JSONResponse(content=data.get("ui", {
                            "images": [],
                            "prompt": "暂无UI提示词",
                            "status": "pending"
                        }))
                return JSONResponse(content={
                    "images": [],
                    "prompt": "暂无UI提示词",
                    "status": "pending"
                })
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.post("/api/confirm_ux")
        async def confirm_ux():
            """用户确认UX设计"""
            try:
                from datetime import datetime
                data_file = Path("automation-data/design_confirmations.json")
                
                # 读取现有数据
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                else:
                    data = {"ux": {}, "ui": {}}
                
                # 更新UX确认状态
                if "ux" not in data:
                    data["ux"] = {}
                data["ux"]["status"] = "approved"
                data["ux"]["confirmed_at"] = datetime.now().isoformat()
                
                # 保存数据
                data_file.parent.mkdir(parents=True, exist_ok=True)
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={"success": True, "message": "UX已确认"})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.post("/api/confirm_ui")
        async def confirm_ui():
            """用户确认UI设计"""
            try:
                from datetime import datetime
                data_file = Path("automation-data/design_confirmations.json")
                
                # 读取现有数据
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                else:
                    data = {"ux": {}, "ui": {}}
                
                # 更新UI确认状态
                if "ui" not in data:
                    data["ui"] = {}
                data["ui"]["status"] = "approved"
                data["ui"]["confirmed_at"] = datetime.now().isoformat()
                
                # 保存数据
                data_file.parent.mkdir(parents=True, exist_ok=True)
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={"success": True, "message": "UI已确认"})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/project_scan")
        async def get_project_scan():
            """获取项目扫描结果（v1.7完整功能清单）"""
            try:
                # 读取v1.7完整功能清单(108个细粒度功能)
                # 使用绝对路径确保找到文件
                # dashboard.py在apps/dashboard/src/industrial_dashboard/
                # 需要回到apps/dashboard/才能找到automation-data/
                base_dir = Path(__file__).parent.parent.parent  # 回到apps/dashboard/
                features_file = base_dir / "automation-data" / "v17-complete-features.json"
                if features_file.exists():
                    with open(features_file, 'r', encoding='utf-8') as f:
                        complete_data = json.load(f)
                    
                    implemented = complete_data.get("implemented", [])
                    partial = complete_data.get("partial", [])
                    conflicts = complete_data.get("conflicts", [])
                    
                    # 返回完整的v1.7功能清单
                    return JSONResponse(content={
                        "features": {
                            "implemented": implemented,
                            "partial": partial,
                            "conflicts": conflicts
                        },
                        "summary": {
                            "total_features": len(implemented) + 4,
                            "implemented": len(implemented),
                            "partial": 4,
                            "completion_rate": len(implemented) / (len(implemented) + 4),
                            "by_version": complete_data.get("summary", {}).get("by_version", {}),
                            "by_type": complete_data.get("summary", {}).get("by_type", {})
                        },
                        "last_updated": datetime.now().isoformat()
                    })
                else:
                    # 如果文件不存在，返回简化版本
                    return JSONResponse(content={
                        "features": {
                            "implemented": [
                                {"name": "Monorepo目录结构", "file": "docs/adr/0001-monorepo-structure.md", "type": "架构", "completion": 1.0}
                            ],
                            "partial": [],
                            "conflicts": []
                        },
                        "summary": {"total_features": 1, "implemented": 1, "partial": 0},
                        "last_updated": datetime.now().isoformat()
                    })
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.post("/api/upload_design/{design_type}")
        async def upload_design(design_type: str, request: Request):
            """上传设计图片（UX或UI）"""
            try:
                data = await request.json()
                image_url = data.get("url", "")
                label = data.get("label", "设计稿")
                
                if not image_url:
                    return JSONResponse(content={"success": False, "error": "缺少图片URL"}, status_code=400)
                
                # 读取现有确认数据
                data_file = Path("automation-data/design_confirmations.json")
                confirmation_data = {}
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        confirmation_data = json.load(f)
                else:
                    confirmation_data = {"ux": {}, "ui": {}}
                
                # 添加图片
                if design_type not in confirmation_data:
                    confirmation_data[design_type] = {'images': [], 'prompt': '', 'status': 'pending'}
                
                if 'images' not in confirmation_data[design_type]:
                    confirmation_data[design_type]['images'] = []
                
                confirmation_data[design_type]['images'].append({
                    'url': image_url,
                    'label': label,
                    'uploaded_at': datetime.now().isoformat()
                })
                
                # 保存
                data_file.parent.mkdir(parents=True, exist_ok=True)
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(confirmation_data, f, ensure_ascii=False, indent=2)
                
                #  添加事件到事件流
                events_file = Path("automation-data/architect_events.json")
                if events_file.exists():
                    with open(events_file, 'r', encoding='utf-8') as f:
                        events_data = json.load(f)
                else:
                    events_data = {"events": []}
                
                new_event = {
                    "id": f"event-{len(events_data['events']) + 1}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "design_upload",
                    "content": f"架构师上传{design_type.upper()}设计稿：{label}",
                    "metadata": {"design_type": design_type, "url": image_url}
                }
                events_data["events"].insert(0, new_event)
                
                with open(events_file, 'w', encoding='utf-8') as f:
                    json.dump(events_data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={"success": True, "message": f"{design_type.upper()}图片已上传"})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.post("/api/assign_role")
        async def assign_role(request: Request):
            """任命角色"""
            try:
                data = await request.json()
                role = data.get("role", "")
                project = data.get("project", "任务所·Flow")
                user = data.get("user", "AI助手")
                
                if not role:
                    return JSONResponse(content={"success": False, "error": "缺少角色参数"}, status_code=400)
                
                # 角色中文映射
                role_names = {
                    "architect": "架构师",
                    "ux_designer": "UX设计师",
                    "ui_designer": "UI设计师",
                    "developer": "全栈开发工程师",
                    "tester": "测试工程师",
                    "ops": "运维工程师"
                }
                
                role_name = role_names.get(role, role)
                
                # 🔥 如果是架构师，自动扫描项目并初始化知识库
                scan_result = None
                kb_result = None
                if role == "architect":
                    try:
                        import sys
                        sys.path.insert(0, str(Path(__file__).parent.parent))
                        from automation.project_scanner import ProjectScanner
                        
                        scanner = ProjectScanner(".")
                        scan_result = scanner.initialize_with_knowledge_base()
                        kb_result = scan_result.get("knowledge_base", {})
                        
                        # 更新项目名称
                        if scan_result:
                            project = scan_result.get("project_name", project)
                        
                        print(f"[架构师] 项目扫描完成: {scan_result.get('project_name')}")
                        print(f"[架构师] 知识库初始化: {kb_result.get('created_dirs', 0)}个目录, {kb_result.get('created_files', 0)}个文件")
                        
                    except Exception as e:
                        print(f"⚠️ 项目扫描/初始化失败: {e}")
                        # 扫描失败不影响任命
                
                # 更新architect_monitor.json
                monitor_file = Path("automation-data/architect_monitor.json")
                monitor_data = {}
                if monitor_file.exists():
                    with open(monitor_file, 'r', encoding='utf-8') as f:
                        monitor_data = json.load(f)
                else:
                    monitor_data = {
                        "token_usage": {"used": 0, "total": 1000000},
                        "status": {"text": "初始化", "reviewed_count": 0},
                        "prompt": ""
                    }
                
                # 更新角色和状态
                monitor_data["current_role"] = {
                    "role": role,
                    "role_name": role_name,
                    "project": project,
                    "assigned_at": datetime.now().isoformat(),
                    "assigned_by": user
                }
                monitor_data["status"]["text"] = f"{role_name}工作中"
                
                monitor_file.parent.mkdir(parents=True, exist_ok=True)
                with open(monitor_file, 'w', encoding='utf-8') as f:
                    json.dump(monitor_data, f, ensure_ascii=False, indent=2)
                
                # 添加事件到事件流
                events_file = Path("automation-data/architect_events.json")
                if events_file.exists():
                    with open(events_file, 'r', encoding='utf-8') as f:
                        events_data = json.load(f)
                else:
                    events_data = {"events": []}
                
                new_event = {
                    "id": f"event-{len(events_data['events']) + 1}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "role_assignment",
                    "content": f"任命AI为{role_name}（项目：{project}）",
                    "metadata": {"role": role, "project": project, "user": user}
                }
                events_data["events"].insert(0, new_event)
                
                # 如果是架构师且扫描成功，添加额外事件
                if role == "architect" and scan_result:
                    # 添加扫描完成事件
                    scan_event = {
                        "id": f"event-{len(events_data['events']) + 1}",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": "project_scan",
                        "content": f"架构师扫描项目完成：{scan_result['files_count'].get('python', 0) + scan_result['files_count'].get('javascript', 0)}个代码文件，识别{len(scan_result.get('features', {}).get('implemented', []))}个功能",
                        "metadata": {
                            "files_total": scan_result['files_count'].get('total', 0),
                            "features_count": len(scan_result.get('features', {}).get('implemented', [])),
                            "conflicts_count": len(scan_result.get('features', {}).get('conflicts', []))
                        }
                    }
                    events_data["events"].insert(0, scan_event)
                    
                    # 添加知识库初始化事件
                    if kb_result and kb_result.get('status') == 'success':
                        kb_event = {
                            "id": f"event-{len(events_data['events']) + 1}",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "knowledge_base_init",
                            "content": f"知识库初始化完成：创建{kb_result.get('created_dirs', 0)}个目录，{kb_result.get('created_files', 0)}个文件",
                            "metadata": {
                                "dirs_count": kb_result.get('created_dirs', 0),
                                "files_count": kb_result.get('created_files', 0)
                            }
                        }
                        events_data["events"].insert(0, kb_event)
                
                with open(events_file, 'w', encoding='utf-8') as f:
                    json.dump(events_data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={
                    "success": True,
                    "message": f"已任命为{role_name}" + ("，项目扫描和知识库初始化完成" if scan_result else ""),
                    "role": role,
                    "role_name": role_name,
                    "scan_result": scan_result,
                    "knowledge_base": kb_result
                })
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/current_role")
        async def get_current_role():
            """获取当前角色"""
            try:
                monitor_file = Path("automation-data/architect_monitor.json")
                if monitor_file.exists():
                    with open(monitor_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return JSONResponse(content=data.get("current_role", {}))
                return JSONResponse(content={})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.post("/api/record_token_usage")
        async def record_token_usage(request: Request):
            """记录Token使用（支持手动同步和自动估算）"""
            try:
                data = await request.json()
                tokens = data.get("tokens", 0)
                event = data.get("event", "对话")
                conversation_id = data.get("conversation_id", "")
                sync_type = data.get("sync_type", "auto")  # manual/auto/estimate
                
                # 读取监控数据
                monitor_file = Path("automation-data/architect_monitor.json")
                monitor_data = {}
                if monitor_file.exists():
                    with open(monitor_file, 'r', encoding='utf-8') as f:
                        monitor_data = json.load(f)
                else:
                    monitor_data = {
                        "token_usage": {"used": 0, "total": 1000000, "sessions": []},
                        "status": {"text": "工作中", "reviewed_count": 0}
                    }
                
                # 确保token_usage结构完整
                if "token_usage" not in monitor_data:
                    monitor_data["token_usage"] = {"used": 0, "total": 1000000, "sessions": []}
                if "sessions" not in monitor_data["token_usage"]:
                    monitor_data["token_usage"]["sessions"] = []
                
                # 处理不同的同步类型
                if sync_type == "manual":
                    # 手动同步：直接设置总量（而不是累加）
                    increment = tokens - monitor_data["token_usage"]["used"]
                    if increment < 0:
                        increment = tokens
                        monitor_data["token_usage"]["used"] = tokens
                    else:
                        monitor_data["token_usage"]["used"] = tokens
                    
                    tokens_to_record = increment  # 记录增量
                else:
                    # 自动记录：累加
                    monitor_data["token_usage"]["used"] += tokens
                    tokens_to_record = tokens
                
                # 记录会话
                session_record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "tokens": tokens_to_record,
                    "event": event,
                    "conversation_id": conversation_id,
                    "sync_type": sync_type
                }
                monitor_data["token_usage"]["sessions"].insert(0, session_record)
                
                # 只保留最近100条记录
                if len(monitor_data["token_usage"]["sessions"]) > 100:
                    monitor_data["token_usage"]["sessions"] = monitor_data["token_usage"]["sessions"][:100]
                
                # 保存
                monitor_file.parent.mkdir(parents=True, exist_ok=True)
                with open(monitor_file, 'w', encoding='utf-8') as f:
                    json.dump(monitor_data, f, ensure_ascii=False, indent=2)
                
                # 添加事件到事件流
                events_file = Path("automation-data/architect_events.json")
                if events_file.exists():
                    with open(events_file, 'r', encoding='utf-8') as f:
                        events_data = json.load(f)
                else:
                    events_data = {"events": []}
                
                sync_label = "手动同步" if sync_type == "manual" else "自动记录"
                new_event = {
                    "id": f"event-{len(events_data['events']) + 1}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "token_usage",
                    "content": f"Token更新: {tokens_to_record:,} ({sync_label} - {event})",
                    "metadata": {"tokens": tokens_to_record, "event": event, "sync_type": sync_type}
                }
                events_data["events"].insert(0, new_event)
                
                with open(events_file, 'w', encoding='utf-8') as f:
                    json.dump(events_data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={
                    "success": True,
                    "message": "Token使用已记录",
                    "total_used": monitor_data["token_usage"]["used"],
                    "increment": tokens_to_record if sync_type == "manual" else tokens
                })
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/token_sessions")
        async def get_token_sessions():
            """获取Token使用会话记录"""
            try:
                monitor_file = Path("automation-data/architect_monitor.json")
                if monitor_file.exists():
                    with open(monitor_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return JSONResponse(content={
                            "sessions": data.get("token_usage", {}).get("sessions", [])
                        })
                return JSONResponse(content={"sessions": []})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.put("/api/tasks/{task_id}/received")
        async def receive_task(task_id: str, request: Request):
            """
            李明接收任务 - 状态从 pending → in_progress
            
            Request Body:
            {
                "actor": "fullstack-engineer",
                "notes": "已开始处理此任务"
            }
            """
            try:
                import sys
                from pathlib import Path as PathLib
                
                # 导入StateManager
                packages_path = PathLib(__file__).parent.parent.parent.parent.parent / "packages"
                if str(packages_path) not in sys.path:
                    sys.path.insert(0, str(packages_path))
                
                from automation.state_manager import StateManager
                
                # 解析请求体
                body = await request.json() if request.headers.get("content-type") == "application/json" else {}
                actor = body.get("actor", "fullstack-engineer")
                notes = body.get("notes", "任务已接收")
                
                # 更新任务状态
                state_manager = StateManager()
                success = state_manager.update_task_status(task_id, "in_progress")
                
                if not success:
                    return JSONResponse(content={
                        "success": False,
                        "message": f"任务 {task_id} 不存在或更新失败"
                    }, status_code=404)
                
                # 记录事件
                events_file = Path("automation-data/architect_events.json")
                if events_file.exists():
                    with open(events_file, 'r', encoding='utf-8') as f:
                        events_data = json.load(f)
                else:
                    events_data = {"events": []}
                
                new_event = {
                    "id": f"event-{len(events_data['events']) + 1}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "task_received",
                    "content": f"{actor} 接收任务: {task_id}",
                    "metadata": {"task_id": task_id, "actor": actor, "notes": notes}
                }
                events_data["events"].insert(0, new_event)
                
                with open(events_file, 'w', encoding='utf-8') as f:
                    json.dump(events_data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={
                    "success": True,
                    "message": f"任务 {task_id} 已接收",
                    "task_id": task_id,
                    "status": "in_progress",
                    "actor": actor
                })
                
            except Exception as e:
                import traceback
                return JSONResponse(content={
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }, status_code=500)
        
        @self.app.put("/api/tasks/{task_id}/start")
        async def start_task(task_id: str, request: Request):
            """
            开始执行任务 - 触发 task_started 事件
            
            Request Body:
            {
                "actor": "fullstack-engineer",
                "work_plan": "1. 理解需求 2. 编码 3. 测试",
                "planned_completion": "2025-11-18T20:00:00"
            }
            """
            try:
                import sys
                from pathlib import Path as PathLib
                
                # 导入EventHelper
                packages_path = PathLib(__file__).parent.parent.parent.parent.parent / "packages"
                if str(packages_path) not in sys.path:
                    sys.path.insert(0, str(packages_path))
                
                from shared_utils.event_helper import create_event_helper
                from automation.state_manager import StateManager
                
                # 解析请求体
                body = await request.json() if request.headers.get("content-type") == "application/json" else {}
                actor = body.get("actor", "fullstack-engineer")
                work_plan = body.get("work_plan")
                planned_completion = body.get("planned_completion")
                
                # 更新任务状态
                state_manager = StateManager()
                success = state_manager.update_task_status(task_id, "in_progress")
                
                if not success:
                    return JSONResponse(content={
                        "success": False,
                        "message": f"任务 {task_id} 不存在或更新失败"
                    }, status_code=404)
                
                # 触发 task_started 事件
                event_helper = create_event_helper(
                    project_id="TASKFLOW",
                    actor=actor,
                    source="ai"
                )
                
                event = event_helper.task_started(
                    task_id=task_id,
                    actor=actor,
                    planned_completion=planned_completion,
                    work_plan=work_plan
                )
                
                return JSONResponse(content={
                    "success": True,
                    "message": f"任务 {task_id} 已开始",
                    "event_id": event['id'],
                    "task_id": task_id,
                    "status": "in_progress"
                })
                
            except Exception as e:
                import traceback
                return JSONResponse(content={
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }, status_code=500)
        
        @self.app.post("/api/tasks/{task_id}/complete")
        async def complete_task(task_id: str, request: Request):
            """
            完成任务 - 触发 task_completed 事件
            
            Request Body:
            {
                "actor": "fullstack-engineer",
                "actual_hours": 2.5,
                "files_modified": ["file1.py", "file2.py"],
                "completion_summary": "任务完成摘要"
            }
            """
            try:
                import sys
                from pathlib import Path as PathLib
                
                # 导入EventHelper
                packages_path = PathLib(__file__).parent.parent.parent.parent.parent / "packages"
                if str(packages_path) not in sys.path:
                    sys.path.insert(0, str(packages_path))
                
                from shared_utils.event_helper import create_event_helper
                from automation.state_manager import StateManager
                
                # 解析请求体
                body = await request.json() if request.headers.get("content-type") == "application/json" else {}
                actor = body.get("actor", "fullstack-engineer")
                actual_hours = body.get("actual_hours")
                files_modified = body.get("files_modified", [])
                completion_summary = body.get("completion_summary")
                
                # 更新任务状态
                state_manager = StateManager()
                success = state_manager.update_task_status(task_id, "completed")
                
                if not success:
                    return JSONResponse(content={
                        "success": False,
                        "message": f"任务 {task_id} 不存在或更新失败"
                    }, status_code=404)
                
                # 触发 task_completed 事件
                event_helper = create_event_helper(
                    project_id="TASKFLOW",
                    actor=actor,
                    source="ai"
                )
                
                event = event_helper.task_completed(
                    task_id=task_id,
                    actor=actor,
                    actual_hours=actual_hours,
                    files_modified=files_modified,
                    completion_summary=completion_summary
                )
                
                return JSONResponse(content={
                    "success": True,
                    "message": f"任务 {task_id} 已完成",
                    "event_id": event['id'],
                    "task_id": task_id,
                    "status": "completed"
                })
                
            except Exception as e:
                import traceback
                return JSONResponse(content={
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }, status_code=500)
        
        @self.app.post("/api/tasks/{task_id}/approve")
        async def approve_task(task_id: str, request: Request):
            """
            批准任务 - 触发 task_approved 事件
            
            Request Body:
            {
                "reviewer": "architect",
                "score": 95,
                "feedback": "代码质量优秀，批准通过"
            }
            """
            try:
                import sys
                from pathlib import Path as PathLib
                
                # 导入EventHelper
                packages_path = PathLib(__file__).parent.parent.parent.parent.parent / "packages"
                if str(packages_path) not in sys.path:
                    sys.path.insert(0, str(packages_path))
                
                from shared_utils.event_helper import create_event_helper
                from automation.state_manager import StateManager
                
                # 解析请求体
                body = await request.json() if request.headers.get("content-type") == "application/json" else {}
                reviewer = body.get("reviewer", "architect")
                score = body.get("score")
                feedback = body.get("feedback")
                
                # 更新任务状态为完成（批准后）
                state_manager = StateManager()
                success = state_manager.update_task_status(task_id, "completed")
                
                if not success:
                    return JSONResponse(content={
                        "success": False,
                        "message": f"任务 {task_id} 不存在或更新失败"
                    }, status_code=404)
                
                # 触发 task_approved 事件
                event_helper = create_event_helper(
                    project_id="TASKFLOW",
                    actor=reviewer,
                    source="ai"
                )
                
                event = event_helper.task_approved(
                    task_id=task_id,
                    reviewer=reviewer,
                    score=score,
                    feedback=feedback
                )
                
                return JSONResponse(content={
                    "success": True,
                    "message": f"任务 {task_id} 已批准",
                    "event_id": event['id'],
                    "task_id": task_id,
                    "status": "completed",
                    "score": score
                })
                
            except Exception as e:
                import traceback
                return JSONResponse(content={
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }, status_code=500)
        
        @self.app.post("/api/architect/review_task/{task_id}")
        async def architect_review_task(task_id: str):
            """架构师审查任务"""
            try:
                from automation.architect_reviewer import ArchitectReviewer
                from automation.state_manager import StateManager
                
                state_manager = StateManager()
                architect = ArchitectReviewer(state_manager)
                
                # 执行审查
                success = architect.complete_task_review(task_id)
                
                if success:
                    return JSONResponse(content={
                        "success": True,
                        "message": f"任务 {task_id} 审查完成，已更新为已完成状态"
                    })
                else:
                    return JSONResponse(content={
                        "success": False,
                        "message": f"任务 {task_id} 审查未通过或部署预览未通过"
                    }, status_code=400)
                    
            except Exception as e:
                return JSONResponse(content={
                    "success": False,
                    "error": str(e)
                }, status_code=500)
        
        @self.app.get("/api/architect/task_report/{task_id}")
        async def get_task_report(task_id: str):
            """获取任务执行报告"""
            try:
                report_file = Path(f"automation-data/task_reports/{task_id}_report.json")
                if report_file.exists():
                    with open(report_file, 'r', encoding='utf-8') as f:
                        report = json.load(f)
                    return JSONResponse(content=report)
                else:
                    return JSONResponse(content={
                        "error": "报告不存在"
                    }, status_code=404)
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/architect_events")
        async def get_architect_events():
            """获取架构师事件流"""
            try:
                events_file = Path("automation-data/architect_events.json")
                if events_file.exists():
                    with open(events_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    return JSONResponse(content=data)
                else:
                    return JSONResponse(content={"events": []})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.post("/api/architect_events")
        async def add_architect_event(request: Request):
            """添加架构师事件"""
            try:
                event_data = await request.json()
                events_file = Path("automation-data/architect_events.json")
                
                # 读取现有事件
                if events_file.exists():
                    with open(events_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                else:
                    data = {"events": []}
                
                # 添加新事件
                from datetime import datetime
                new_event = {
                    "id": f"event-{len(data['events']) + 1}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": event_data.get("type", "communication"),
                    "content": event_data.get("content", ""),
                    "metadata": event_data.get("metadata", {})
                }
                data["events"].insert(0, new_event)
                
                # 保存
                with open(events_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={"success": True, "event": new_event})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/architect_monitor")
        async def get_architect_monitor():
            """
            获取架构师监控数据
            
            Returns:
                {
                    "token_usage": {
                        "used": 132418,
                        "total": 1000000
                    },
                    "status": {
                        "text": "工作中",
                        "reviewed_count": 3
                    },
                    "events": [
                        {
                            "time": "10:30:15",
                            "icon": "🎯",
                            "content": "接手项目总架构师+产品经理"
                        }
                    ],
                    "prompt": "你是【项目名称】的总架构师..."
                }
            """
            try:
                # 使用绝对路径，确保找到数据文件
                base_dir = Path(__file__).parent.parent.parent  # 回到apps/dashboard/
                data_file = base_dir / "automation-data" / "architect_monitor.json"
                events_file = base_dir / "automation-data" / "architect_events.json"
                
                # 读取基础监控数据
                data = {}
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                else:
                    data = {
                        "token_usage": {"used": 0, "total": 1000000},
                        "status": {"text": "初始化", "reviewed_count": 0},
                        "prompt": "暂无提示词"
                    }
                
                # 读取事件流数据
                if events_file.exists():
                    with open(events_file, 'r', encoding='utf-8') as f:
                        events_data = json.load(f)
                        data["events"] = events_data.get("events", [])
                else:
                    data["events"] = []
                
                return JSONResponse(content=data)
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/architect_info/{doc_id}")
        async def get_architect_info(doc_id: str):
            """
            获取重要信息文档
            
            Args:
                doc_id: 文档ID（requirements, handoff, bugs, decisions）
                
            Returns:
                {
                    "title": "重大需求变更",
                    "content": "文档内容..."
                }
            """
            try:
                base_dir = Path(__file__).parent.parent.parent  # 回到apps/dashboard/
                doc_map = {
                    "requirements": {
                        "title": "重大需求变更",
                        "file": base_dir / "automation-data" / "architect-notes" / "requirements.md"
                    },
                    "handoff": {
                        "title": "架构师交接提示词",
                        "file": base_dir / "automation-data" / "architect-notes" / "handoff.md"
                    },
                    "bugs": {
                        "title": "Bug进度清单",
                        "file": base_dir / "automation-data" / "architect-notes" / "bugs.md"
                    },
                    "decisions": {
                        "title": "技术决策记录",
                        "file": base_dir / "automation-data" / "architect-notes" / "decisions.md"
                    }
                }
                
                if doc_id not in doc_map:
                    return JSONResponse(content={"title": "未知文档", "content": ""})
                
                doc_info = doc_map[doc_id]
                file_path = doc_info["file"]
                
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return JSONResponse(content={"title": doc_info["title"], "content": content})
                else:
                    return JSONResponse(content={"title": doc_info["title"], "content": "文档暂未创建"})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/role_prompt/{role}")
        async def get_role_prompt(role: str):
            """获取AI角色的完整提示词"""
            try:
                base_dir = Path(__file__).parent.parent.parent  # 回到apps/dashboard/
                prompt_map = {
                    "architect": "09-role-prompts/architect-prompt.md",
                    "developer": "09-role-prompts/developer-prompt.md",
                    "code-steward": "09-role-prompts/code-steward-prompt.md",
                    "sre": "09-role-prompts/ops-prompt.md"
                }
                
                if role not in prompt_map:
                    return JSONResponse(content={"content": f"未知角色: {role}"})
                
                prompt_file = base_dir / "automation-data" / prompt_map[role]
                if prompt_file.exists():
                    with open(prompt_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return JSONResponse(content={"role": role, "content": content, "size": len(content)})
                else:
                    return JSONResponse(content={"content": f"提示词文件不存在: {prompt_map[role]}"})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/developer_knowledge/{doc_id}")
        async def get_developer_knowledge(doc_id: str):
            """
            获取开发知识库文档
            
            Args:
                doc_id: 文档ID（problems, tools, standards, tips）
            """
            try:
                doc_map = {
                    "problems": {
                        "title": "问题解决库",
                        "file": "automation-data/developer-knowledge/problems.md"
                    },
                    "tools": {
                        "title": "常用工具库",
                        "file": "automation-data/developer-knowledge/tools.md"
                    },
                    "standards": {
                        "title": "开发规范",
                        "file": "automation-data/developer-knowledge/standards.md"
                    },
                    "tips": {
                        "title": "最佳实践",
                        "file": "automation-data/developer-knowledge/tips.md"
                    }
                }
                
                if doc_id not in doc_map:
                    return JSONResponse(content={"title": "未知文档", "content": ""})
                
                doc_info = doc_map[doc_id]
                file_path = Path(doc_info["file"])
                
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return JSONResponse(content={"title": doc_info["title"], "content": content})
                else:
                    return JSONResponse(content={"title": doc_info["title"], "content": "文档暂未创建"})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/tester_knowledge/{doc_id}")
        async def get_tester_knowledge(doc_id: str):
            """获取测试工程师知识库"""
            try:
                doc_map = {
                    "cases": {
                        "title": "测试用例库",
                        "file": "automation-data/tester-knowledge/cases.md"
                    },
                    "bugs": {
                        "title": "Bug跟踪库",
                        "file": "automation-data/tester-knowledge/bugs.md"
                    },
                    "tools": {
                        "title": "测试工具",
                        "file": "automation-data/tester-knowledge/tools.md"
                    },
                    "standards": {
                        "title": "测试规范",
                        "file": "automation-data/tester-knowledge/standards.md"
                    }
                }
                
                if doc_id not in doc_map:
                    return JSONResponse(content={"title": "未知文档", "content": ""})
                
                doc_info = doc_map[doc_id]
                file_path = Path(doc_info["file"])
                
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return JSONResponse(content={"title": doc_info["title"], "content": content})
                else:
                    return JSONResponse(content={"title": doc_info["title"], "content": "文档暂未创建"})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/delivery_docs/{doc_id}")
        async def get_delivery_docs(doc_id: str):
            """获取交付工程师文档"""
            try:
                doc_map = {
                    "environment": {
                        "title": "环境说明",
                        "file": "automation-data/delivery-docs/environment.md"
                    },
                    "tools": {
                        "title": "工具链说明",
                        "file": "automation-data/delivery-docs/tools.md"
                    },
                    "secrets": {
                        "title": "配置与密钥",
                        "file": "automation-data/delivery-docs/secrets.md"
                    },
                    "strategy": {
                        "title": "发布策略",
                        "file": "automation-data/delivery-docs/strategy.md"
                    }
                }
                
                if doc_id not in doc_map:
                    return JSONResponse(content={"title": "未知文档", "content": ""})
                
                doc_info = doc_map[doc_id]
                file_path = Path(doc_info["file"])
                
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return JSONResponse(content={"title": doc_info["title"], "content": content})
                else:
                    return JSONResponse(content={"title": doc_info["title"], "content": "文档暂未创建"})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/ops_knowledge/{doc_id}")
        async def get_ops_knowledge(doc_id: str):
            """获取运维工程师知识库"""
            try:
                doc_map = {
                    "incidents": {
                        "title": "故障记录",
                        "file": "automation-data/ops/incidents.md"
                    },
                    "troubleshooting": {
                        "title": "问题解决库",
                        "file": "automation-data/ops/troubleshooting.md"
                    },
                    "lessons": {
                        "title": "经验教训",
                        "file": "automation-data/ops/lessons.md"
                    },
                    "metrics": {
                        "title": "性能基线",
                        "file": "automation-data/ops/metrics.md"
                    }
                }
                
                if doc_id not in doc_map:
                    return JSONResponse(content={"title": "未知文档", "content": ""})
                
                doc_info = doc_map[doc_id]
                file_path = Path(doc_info["file"])
                
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return JSONResponse(content={"title": doc_info["title"], "content": content})
                else:
                    return JSONResponse(content={"title": doc_info["title"], "content": "暂无记录"})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/cache/version")
        async def get_cache_version():
            """获取当前缓存版本信息"""
            try:
                info = self.version_manager.get_info()
                return JSONResponse(content={
                    "success": True,
                    "data": info
                })
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.post("/api/cache/bump")
        async def bump_cache_version():
            """手动更新缓存版本（强制刷新）"""
            try:
                new_version = self.version_manager.bump_version()
                
                # 记录事件
                events_file = Path("automation-data/architect_events.json")
                if events_file.exists():
                    with open(events_file, 'r', encoding='utf-8') as f:
                        events_data = json.load(f)
                else:
                    events_data = {"events": []}
                
                new_event = {
                    "id": f"event-{len(events_data['events']) + 1}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "cache_clear",
                    "content": f"手动更新缓存版本: {new_version}",
                    "metadata": {"new_version": new_version}
                }
                events_data["events"].insert(0, new_event)
                
                with open(events_file, 'w', encoding='utf-8') as f:
                    json.dump(events_data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={
                    "success": True,
                    "message": "缓存版本已更新，请刷新页面",
                    "new_version": new_version
                })
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/conversations")
        async def get_conversations():
            """获取所有对话会话"""
            try:
                conversations_file = Path("automation-data/architect-conversations.json")
                if conversations_file.exists():
                    with open(conversations_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    return JSONResponse(content=data)
                else:
                    return JSONResponse(content={"sessions": []})
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.get("/api/conversations/{session_id}")
        async def get_conversation(session_id: str):
            """获取单个对话会话详情"""
            try:
                conversations_file = Path("automation-data/architect-conversations.json")
                if conversations_file.exists():
                    with open(conversations_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    sessions = data.get("sessions", [])
                    session = next((s for s in sessions if s["session_id"] == session_id), None)
                    
                    if session:
                        return JSONResponse(content=session)
                    else:
                        return JSONResponse(content={"error": "会话不存在"}, status_code=404)
                else:
                    return JSONResponse(content={"error": "数据文件不存在"}, status_code=404)
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
        
        @self.app.post("/api/conversations")
        async def create_conversation(request: Request):
            """创建新的对话会话"""
            try:
                req_data = await request.json()
                conversations_file = Path("automation-data/architect-conversations.json")
                
                # 读取现有数据
                if conversations_file.exists():
                    with open(conversations_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                else:
                    data = {"sessions": []}
                
                # 生成新会话ID
                session_count = len(data.get("sessions", []))
                new_session_id = f"session-{str(session_count + 1).zfill(3)}"
                
                # 创建新会话
                new_session = {
                    "session_id": new_session_id,
                    "title": req_data.get("title", "新会话"),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "active",
                    "total_tokens": 0,
                    "messages_count": 0,
                    "participants": req_data.get("participants", ["用户", "架构师AI"]),
                    "tags": req_data.get("tags", []),
                    "summary": req_data.get("summary", ""),
                    "messages": []
                }
                
                # 添加到列表
                data["sessions"].insert(0, new_session)
                
                # 保存
                conversations_file.parent.mkdir(parents=True, exist_ok=True)
                with open(conversations_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={"success": True, "session": new_session})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.post("/api/conversations/{session_id}/messages")
        async def add_message(session_id: str, request: Request):
            """向会话添加消息"""
            try:
                req_data = await request.json()
                conversations_file = Path("automation-data/architect-conversations.json")
                
                if not conversations_file.exists():
                    return JSONResponse(content={"error": "数据文件不存在"}, status_code=404)
                
                # 读取数据
                with open(conversations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 查找会话
                sessions = data.get("sessions", [])
                session = next((s for s in sessions if s["session_id"] == session_id), None)
                
                if not session:
                    return JSONResponse(content={"error": "会话不存在"}, status_code=404)
                
                # 生成消息ID
                msg_count = len(session.get("messages", []))
                new_msg_id = f"msg-{str(msg_count + 1).zfill(3)}"
                
                # 创建新消息
                new_message = {
                    "id": new_msg_id,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "from": req_data.get("from", "用户"),
                    "content": req_data.get("content", ""),
                    "type": req_data.get("type", "request"),
                    "tokens": req_data.get("tokens", 0)
                }
                
                # 更新会话
                session["messages"].append(new_message)
                session["messages_count"] = len(session["messages"])
                session["total_tokens"] = sum(m.get("tokens", 0) for m in session["messages"])
                session["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 保存
                with open(conversations_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse(content={"success": True, "message": new_message})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.post("/api/cache/clear")
        async def clear_cache():
            """清除浏览器缓存（通过版本更新实现）"""
            try:
                new_version = self.version_manager.bump_version()
                return JSONResponse(content={
                    "success": True,
                    "message": "缓存已清除，页面将自动刷新",
                    "new_version": new_version,
                    "action": "reload"
                })
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        # ============================================================================
        # 事件流API端点
        # ============================================================================
        
        @self.app.get("/api/events/stream")
        async def get_event_stream(
            event_type: Optional[str] = None,
            category: Optional[str] = None,
            actor: Optional[str] = None,
            severity: Optional[str] = None,
            hours: int = 24,
            limit: int = 100
        ):
            """
            获取事件流
            
            Query参数:
                - event_type: 事件类型过滤
                - category: 分类过滤 (task/issue/decision/deployment/system)
                - actor: 操作者过滤
                - severity: 严重性过滤 (info/warning/error/critical)
                - hours: 最近N小时的事件
                - limit: 返回数量限制
            """
            try:
                events = self.event_stream_provider.get_events(
                    event_type=event_type,
                    category=category,
                    actor=actor,
                    severity=severity,
                    hours=hours,
                    limit=limit
                )
                return JSONResponse(content={"success": True, "events": events, "count": len(events)})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/events/stats")
        async def get_event_stats():
            """获取事件统计"""
            try:
                stats = self.event_stream_provider.get_event_stats()
                return JSONResponse(content={"success": True, "stats": stats})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/events/categories")
        async def get_categories_summary():
            """获取各分类事件数量汇总"""
            try:
                summary = self.event_stream_provider.get_categories_summary()
                return JSONResponse(content={"success": True, "categories": summary})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/events/severities")
        async def get_severities_summary():
            """获取各严重性事件数量汇总"""
            try:
                summary = self.event_stream_provider.get_severities_summary()
                return JSONResponse(content={"success": True, "severities": summary})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/events/actors")
        async def get_actors_summary(hours: int = 24):
            """获取各操作者的事件数量"""
            try:
                summary = self.event_stream_provider.get_actors_summary(hours=hours)
                return JSONResponse(content={"success": True, "actors": summary})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/events/search")
        async def search_events(q: str, limit: int = 50):
            """搜索事件"""
            try:
                events = self.event_stream_provider.search_events(keyword=q, limit=limit)
                return JSONResponse(content={"success": True, "events": events, "count": len(events)})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
        
        @self.app.get("/api/events/recent")
        async def get_recent_events(hours: int = 1, limit: int = 50):
            """获取最近的事件（用于实时刷新）"""
            try:
                events = self.event_stream_provider.get_recent_events(hours=hours, limit=limit)
                return JSONResponse(content={"success": True, "events": events, "count": len(events)})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
    
    def run(self, open_browser: bool = True):
        print()
        print("=" * 70)
        print(f"{self.title}")
        print("=" * 70)
        print()
        print(f"[URL] http://{self.host}:{self.port}")
        print(f"[Design] Luxury Industrial Aesthetics")
        print(f"[Features] Version Support | Task Management")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 70)
        print()
        
        if open_browser:
            import webbrowser
            import threading
            import time
            
            def open_browser_delayed():
                time.sleep(1.5)
                webbrowser.open(f"http://{self.host}:{self.port}")
            
            threading.Thread(target=open_browser_delayed, daemon=True).start()
        
        try:
            uvicorn.run(self.app, host=self.host, port=self.port, log_level="warning")
        except KeyboardInterrupt:
            print("\n\nDashboard stopped")
