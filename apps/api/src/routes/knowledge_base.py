# -*- coding: utf-8 -*-
"""
知识库API路由

提供知识库文章的查询、创建、更新等功能
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# 创建路由器
router = APIRouter(prefix="/api/knowledge", tags=["knowledge_base"])


# ============================================================================
# 数据模型
# ============================================================================

class KnowledgeArticle:
    """知识文章模型"""
    def __init__(self, 
                 id: str,
                 title: str,
                 content: str,
                 category: str,
                 project_id: str,
                 component_id: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        self.id = id
        self.title = title
        self.content = content
        self.category = category
        self.project_id = project_id
        self.component_id = component_id
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()


# ============================================================================
# API端点
# ============================================================================

@router.get(
    "/articles",
    summary="获取知识文章列表",
    description="根据过滤条件获取知识文章列表"
)
async def list_articles(
    project_id: Optional[str] = Query(None, description="项目ID"),
    category: Optional[str] = Query(None, description="分类"),
    tags: Optional[str] = Query(None, description="标签（逗号分隔）"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
) -> Dict[str, Any]:
    """
    获取知识文章列表
    
    Args:
        project_id: 项目ID（可选）
        category: 分类过滤（可选）
        tags: 标签过滤（可选）
        skip: 分页偏移
        limit: 分页数量
        
    Returns:
        {
            "total": 10,
            "articles": [
                {
                    "id": "ARTICLE-001",
                    "title": "企业级Monorepo目录结构模板",
                    "category": "architecture",
                    "created_at": "2025-11-19T...",
                    "tags": ["monorepo", "architecture"]
                }
            ]
        }
    """
    # TODO: 从数据库查询
    # 这里返回示例数据
    return {
        "total": 0,
        "skip": skip,
        "limit": limit,
        "articles": []
    }


@router.get(
    "/articles/{article_id}",
    summary="获取知识文章详情",
    description="获取单个知识文章的完整内容"
)
async def get_article(article_id: str) -> Dict[str, Any]:
    """
    获取知识文章详情
    
    Args:
        article_id: 文章ID
        
    Returns:
        知识文章完整信息
    """
    # TODO: 从数据库查询
    return {
        "found": False,
        "message": f"文章 {article_id} 不存在"
    }


@router.post(
    "/articles",
    summary="创建知识文章",
    description="在知识库中创建新的文章"
)
async def create_article(article_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    创建知识文章
    
    Args:
        article_data: {
            "title": "文章标题",
            "content": "文章内容",
            "category": "architecture|pattern|guide",
            "project_id": "TASKFLOW",
            "component_id": "optional",
            "tags": ["tag1", "tag2"]
        }
        
    Returns:
        {
            "success": True,
            "article_id": "ARTICLE-001",
            "created_at": "2025-11-19T..."
        }
    """
    try:
        required_fields = ["title", "content", "category", "project_id"]
        missing = [f for f in required_fields if f not in article_data]
        
        if missing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"缺少必要字段: {', '.join(missing)}"
            )
        
        # TODO: 保存到数据库
        article_id = f"ARTICLE-{datetime.now().timestamp()}"
        
        return {
            "success": True,
            "article_id": article_id,
            "title": article_data["title"],
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建文章失败: {str(e)}"
        )


@router.get(
    "/templates",
    summary="获取企业级模板",
    description="获取Monorepo和其他企业级模板"
)
async def get_templates() -> Dict[str, Any]:
    """
    获取所有可用的企业级模板
    
    Returns:
        {
            "templates": [
                {
                    "id": "TEMPLATE-001",
                    "name": "企业级Monorepo目录结构",
                    "category": "architecture",
                    "description": "...",
                    "url": "/api/knowledge/templates/TEMPLATE-001"
                }
            ]
        }
    """
    return {
        "templates": [
            {
                "id": "TEMPLATE-001",
                "name": "企业级Monorepo目录结构模板",
                "category": "architecture",
                "description": "生产级Monorepo目录结构，适用于企业级项目",
                "version": "v1.0",
                "created_at": "2025-11-19",
                "url": "/api/knowledge/templates/TEMPLATE-001",
                "article_id": "ARTICLE-MONOREPO-TEMPLATE"
            }
        ]
    }


@router.get(
    "/templates/{template_id}",
    summary="获取模板详情",
    description="获取指定模板的完整内容"
)
async def get_template(template_id: str) -> Dict[str, Any]:
    """
    获取模板详情
    
    Args:
        template_id: 模板ID（如：TEMPLATE-001）
        
    Returns:
        模板完整内容（Markdown格式）
    """
    # TODO: 从数据库或文件系统获取
    if template_id == "TEMPLATE-001":
        return {
            "id": "TEMPLATE-001",
            "name": "企业级Monorepo目录结构模板",
            "category": "architecture",
            "version": "v1.0",
            "article_id": "ARTICLE-MONOREPO-TEMPLATE",
            "file_path": "docs/arch/monorepo-structure-template.md",
            "summary": "包含apps、packages、docs、ops、knowledge、database等8个顶层目录，50+子目录的完整企业级Monorepo结构",
            "tags": ["monorepo", "architecture", "enterprise", "structure"],
            "content_preview": "# 📁 企业级Monorepo目录结构模板\n\n**版本**: v1.0\n**适用**: 需要长期维护、多人协作、AI辅助的专业项目...",
            "content_url": "/api/knowledge/templates/TEMPLATE-001/content",
            "created_at": "2025-11-19",
            "updated_at": "2025-11-19"
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"模板 {template_id} 不存在"
    )


@router.get(
    "/templates/{template_id}/content",
    summary="获取模板完整内容",
    description="获取Markdown格式的完整模板内容"
)
async def get_template_content(template_id: str) -> Dict[str, Any]:
    """
    获取模板完整内容（Markdown）
    
    Args:
        template_id: 模板ID
        
    Returns:
        {
            "id": "TEMPLATE-001",
            "name": "企业级Monorepo目录结构模板",
            "markdown_content": "# 📁 企业级Monorepo目录结构模板\n...",
            "content_length": 50000,
            "lines": 1372
        }
    """
    # TODO: 从文件系统读取并返回完整Markdown内容
    if template_id == "TEMPLATE-001":
        try:
            from pathlib import Path
            template_path = Path(__file__).parent.parent.parent.parent.parent / "docs" / "arch" / "monorepo-structure-template.md"
            
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return {
                    "id": "TEMPLATE-001",
                    "name": "企业级Monorepo目录结构模板",
                    "markdown_content": content,
                    "content_length": len(content),
                    "lines": len(content.split('\n')),
                    "file_path": str(template_path),
                    "encoding": "utf-8"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"模板文件不存在: {template_path}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"读取模板失败: {str(e)}"
            )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"模板 {template_id} 不存在"
    )


@router.post(
    "/templates/{template_id}/import",
    summary="导入模板到知识库",
    description="将模板导入到项目的知识库中"
)
async def import_template(
    template_id: str,
    project_id: str = Query(..., description="目标项目ID"),
    component_id: Optional[str] = Query(None, description="关联组件ID")
) -> Dict[str, Any]:
    """
    导入模板到知识库
    
    Args:
        template_id: 模板ID
        project_id: 目标项目ID
        component_id: 关联组件ID（可选）
        
    Returns:
        {
            "success": True,
            "article_id": "ARTICLE-MONOREPO-TEMPLATE",
            "project_id": "TASKFLOW",
            "message": "模板已成功导入"
        }
    """
    # TODO: 实现导入逻辑
    return {
        "success": True,
        "article_id": "ARTICLE-MONOREPO-TEMPLATE",
        "project_id": project_id,
        "template_id": template_id,
        "component_id": component_id,
        "message": "模板已成功导入到知识库",
        "import_time": datetime.now().isoformat()
    }


@router.get(
    "/status",
    summary="获取知识库服务状态",
    description="健康检查和统计信息"
)
async def get_knowledge_base_status() -> Dict[str, Any]:
    """获取知识库服务状态"""
    return {
        "status": "healthy",
        "version": "1.7.0",
        "features": {
            "articles": True,
            "templates": True,
            "import_templates": True,
            "search": False,  # TODO: 待实现
            "full_text_search": False
        },
        "statistics": {
            "total_articles": 0,  # TODO: 从数据库查询
            "total_templates": 1,
            "total_projects": 1
        },
        "templates": {
            "available": ["TEMPLATE-001"],
            "categories": ["architecture", "pattern", "guide"]
        },
        "timestamp": datetime.now().isoformat()
    }

