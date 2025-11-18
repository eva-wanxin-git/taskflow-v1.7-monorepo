# 常用代码片段

## 错误处理

```python
try:
    # 业务逻辑
    pass
except Exception as e:
    logger.error(f"Error: {e}")
    return {"error": str(e)}
```

## API路由

```python
@app.get("/api/example")
async def example():
    return {"success": True}
```

---
**维护者**: 开发工程师
