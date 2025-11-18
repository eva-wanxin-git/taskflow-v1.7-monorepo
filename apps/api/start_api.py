# -*- coding: utf-8 -*-
"""
任务所·Flow API 启动脚本
"""

import uvicorn
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    print("=" * 70)
    print("Starting TaskFlow API Server...")
    print("=" * 70)
    print()
    print("API Endpoints:")
    print("  - Root: http://localhost:8800/")
    print("  - Health: http://localhost:8800/api/health")
    print("  - Events: http://localhost:8800/api/events")
    print("  - Docs: http://localhost:8800/api/docs")
    print()
    print("=" * 70)
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8800,
        reload=True,
        log_level="info"
    )

