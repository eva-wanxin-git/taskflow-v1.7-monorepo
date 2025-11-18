# 开发规范

## 代码风格

### Python
- PEP 8标准
- 函数≤50行
- 类≤300行
- 完整的类型标注

### 命名规范
- 类名: PascalCase
- 函数/变量: snake_case
- 常量: UPPER_SNAKE_CASE

## 目录规范

### Monorepo结构
```
apps/          # 应用层
packages/      # 共享代码
docs/          # 文档
database/      # 数据库
ops/           # 运维
```

### 后端分层
```
routes/        # 路由层
services/      # 业务层
repositories/  # 数据层
entities/      # 实体层
```

## Git规范

### Commit格式
```
[类型] 简短描述

详细说明（可选）
```

### 类型
- feat: 新功能
- fix: Bug修复
- refactor: 重构
- docs: 文档
- test: 测试

## 测试规范

### 覆盖率目标
- 新代码: ≥80%
- 核心模块: ≥90%

### 测试文件位置
- 单元测试: tests/unit/
- 集成测试: tests/integration/
- E2E测试: tests/e2e/
