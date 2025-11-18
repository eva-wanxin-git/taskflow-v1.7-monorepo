# -*- coding: utf-8 -*-
"""
知识库集成测试

测试Monorepo模板的集成功能
"""

import sys
import pytest
from pathlib import Path
import json

# 添加src路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from routes.knowledge_base import router


class TestKnowledgeBaseIntegration:
    """知识库集成测试"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)
    
    def test_get_templates_list(self, client):
        """测试获取模板列表"""
        response = client.get("/api/knowledge/templates")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "templates" in data
        assert len(data["templates"]) > 0
        
        # 检查模板结构
        template = data["templates"][0]
        assert "id" in template
        assert "name" in template
        assert "category" in template
        assert template["name"] == "企业级Monorepo目录结构模板"
    
    def test_get_monorepo_template(self, client):
        """测试获取Monorepo模板详情"""
        response = client.get("/api/knowledge/templates/TEMPLATE-001")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "TEMPLATE-001"
        assert data["name"] == "企业级Monorepo目录结构模板"
        assert data["category"] == "architecture"
        assert "content_url" in data
    
    def test_get_template_content(self, client):
        """测试获取模板完整内容"""
        response = client.get("/api/knowledge/templates/TEMPLATE-001/content")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "TEMPLATE-001"
        assert "markdown_content" in data
        assert len(data["markdown_content"]) > 0
        assert data["content_length"] > 0
        assert "企业级Monorepo" in data["markdown_content"]
    
    def test_template_content_validation(self, client):
        """验证模板内容的有效性"""
        response = client.get("/api/knowledge/templates/TEMPLATE-001/content")
        
        assert response.status_code == 200
        data = response.json()
        content = data["markdown_content"]
        
        # 检查关键部分
        assert "📁" in content or "apps" in content  # 目录结构
        assert "packages" in content  # 共享代码
        assert "docs" in content  # 文档
        assert "ops" in content  # 运维
    
    def test_import_template(self, client):
        """测试导入模板"""
        response = client.post(
            "/api/knowledge/templates/TEMPLATE-001/import?project_id=TASKFLOW&component_id=TASKFLOW-ARCH"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] == True
        assert data["project_id"] == "TASKFLOW"
        assert "article_id" in data
    
    def test_import_template_validation(self, client):
        """测试导入模板验证"""
        # 不提供project_id应该报错
        response = client.post("/api/knowledge/templates/TEMPLATE-001/import")
        
        assert response.status_code == 422  # 验证错误
    
    def test_get_knowledge_base_status(self, client):
        """测试知识库服务状态"""
        response = client.get("/api/knowledge/status")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "features" in data
        assert "statistics" in data
        assert data["features"]["templates"] == True
        assert data["statistics"]["total_templates"] == 1
    
    def test_get_nonexistent_template(self, client):
        """测试获取不存在的模板"""
        response = client.get("/api/knowledge/templates/TEMPLATE-999")
        
        assert response.status_code == 404
    
    def test_template_list_categories(self, client):
        """测试模板分类"""
        response = client.get("/api/knowledge/status")
        
        assert response.status_code == 200
        data = response.json()
        
        categories = data["statistics"]["total_templates"]
        assert categories >= 1
    
    def test_template_metadata(self, client):
        """测试模板元数据"""
        response = client.get("/api/knowledge/templates/TEMPLATE-001")
        
        assert response.status_code == 200
        data = response.json()
        
        # 检查元数据完整性
        assert "id" in data
        assert "name" in data
        assert "category" in data
        assert "version" in data
        assert "created_at" in data
        assert "tags" in data
        
        # 检查标签
        tags = data.get("tags", [])
        assert "monorepo" in tags or "architecture" in tags


class TestKnowledgeBaseAPI:
    """知识库API测试"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)
    
    def test_list_articles(self, client):
        """测试获取文章列表"""
        response = client.get("/api/knowledge/articles")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total" in data
        assert "articles" in data
        assert "skip" in data
        assert "limit" in data
    
    def test_get_knowledge_base_root(self, client):
        """测试知识库API根路径"""
        response = client.get("/api/knowledge/status")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "version" in data


class TestTemplateIntegration:
    """模板集成测试（实际文件系统）"""
    
    def test_template_file_exists(self):
        """测试模板文件是否存在"""
        template_path = Path(__file__).parent.parent.parent / "docs" / "arch" / "monorepo-structure-template.md"
        
        assert template_path.exists(), f"模板文件不存在: {template_path}"
    
    def test_template_file_readable(self):
        """测试模板文件是否可读"""
        template_path = Path(__file__).parent.parent.parent / "docs" / "arch" / "monorepo-structure-template.md"
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert len(content) > 0, "模板文件为空"
            assert "Monorepo" in content, "模板文件缺少预期内容"
        except Exception as e:
            pytest.fail(f"无法读取模板文件: {e}")
    
    def test_template_file_size(self):
        """测试模板文件大小"""
        template_path = Path(__file__).parent.parent.parent / "docs" / "arch" / "monorepo-structure-template.md"
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 模板应该至少有1000字符（600行左右）
        assert len(content) > 1000, f"模板文件太小: {len(content)} 字符"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

