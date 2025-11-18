# -*- coding: utf-8 -*-
"""
任务所·Flow API 主应用

提供RESTful API接口：
- 事件系统API
- 项目记忆API
- 架构师协调API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# 添加packages路径
root_path = Path(__file__).parent.parent.parent.parent
packages_path = root_path / "packages" / "core-domain" / "src"
sys.path.insert(0, str(packages_path))

# 导入路由
from routes.events import router as events_router
from routes.project_memory import router as project_memory_router
from routes.architect import router as architect_router
from routes.listener import router as listener_router
from routes.conversations import router as conversations_router
from routes.conversations_session_memory import router as conversations_session_memory_router
from routes.knowledge_base import router as knowledge_base_router


# ============================================================================
# 创建应用
# ============================================================================

app = FastAPI(
    title="任务所·Flow API",
    description="AI驱动的项目协作与进度监控系统",
    version="1.7.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


# ============================================================================
# 配置CORS
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# 注册路由
# ============================================================================

app.include_router(events_router, tags=["events"])
app.include_router(project_memory_router, tags=["project_memory"])
app.include_router(architect_router, tags=["architect"])
app.include_router(listener_router, tags=["listener"])
app.include_router(conversations_router, tags=["conversations"])
app.include_router(conversations_session_memory_router, tags=["conversations-session-memory"])
app.include_router(knowledge_base_router, tags=["knowledge_base"])


# ============================================================================
# 根端点
# ============================================================================

@app.get("/")
async def root():
    """API根端点"""
    return {
        "name": "任务所·Flow API",
        "version": "1.7.0",
        "status": "running",
        "endpoints": {
            "events": "/api/events",
            "project_memory": "/api/project-memory",
            "architect": "/api/architect",
            "listener": "/api/listener",
            "conversations": "/api/conversations",
            "knowledge_base": "/api/knowledge",
            "docs": "/api/docs"
        }
    }


@app.get("/api/health")
async def health():
    """健康检查端点"""
    return {
        "status": "healthy",
        "version": "1.7.0"
    }


# ============================================================================
# 启动应用
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8800,
        reload=True,
        log_level="info"
    )

