# 项目文件清单

## 总览

**总文件数**: 35  
**代码文件**: 14 (Python)  
**文档文件**: 11 (Markdown)  
**配置文件**: 4  
**工具文件**: 2

## 文件分类

### 📁 源代码 (src/)

#### Agent 核心

- `src/agent/__init__.py` - 模块初始化
- `src/agent/main.py` - Agent 主入口，包含 invoke 函数

#### 工具模块

- `src/tools/__init__.py` - 模块初始化
- `src/tools/baidu_maps.py` - 百度地图 MCP 客户端
- `src/tools/tavily_search.py` - Tavily 搜索工具

#### 工具函数

- `src/utils/__init__.py` - 模块初始化
- `src/utils/memory.py` - Memory 相关函数
- `src/utils/prompts.py` - 系统提示词配置

#### 配置

- `src/__init__.py` - 模块初始化
- `src/config.py` - 配置管理

### 🧪 测试 (tests/)

- `tests/__init__.py` - 模块初始化
- `tests/test_memory.py` - Memory 功能测试

### 💻 客户端 (clients/)

- `clients/__init__.py` - 模块初始化
- `clients/boto3_client.py` - Boto3 测试客户端

### 📚 文档 (docs/)

#### 技术文档

- `docs/__init__.py` - 模块初始化
- `docs/README.md` - 详细部署指南
- `docs/ARCHITECTURE.md` - 系统架构设计
- `docs/PROJECT_STRUCTURE.md` - 项目结构说明

#### 使用文档

- `docs/TESTING_GUIDE.md` - 测试指南
- `docs/MEMORY_GUIDE.md` - Memory 使用指南
- `docs/SUMMARY.md` - 项目总结

### 📄 根目录文档

#### 主要文档

- `README.md` - 项目主 README（简洁版）
- `PROJECT_OVERVIEW.md` - 项目概览
- `QUICK_REFERENCE.md` - 快速参考指南

#### 维护文档

- `MIGRATION.md` - 迁移指南
- `CHANGELOG.md` - 更新日志
- `OPTIMIZATION_SUMMARY.md` - 优化总结
- `PROJECT_FILES.md` - 本文件

### ⚙️ 配置文件

- `.env.example` - 环境变量示例
- `.gitignore` - Git 忽略配置
- `.dockerignore` - Docker 忽略配置
- `.bedrock_agentcore.yaml` - AgentCore 配置

### 🔧 工具文件

- `agentcore_baidu_map_agent.py` - 向后兼容入口
- `verify_structure.py` - 结构验证脚本
- `Makefile` - 常用命令快捷方式
- `requirements.txt` - Python 依赖
- `project_files.txt` - 文件列表

## 文件详情

### 核心文件 (必需)

| 文件                           | 行数 | 用途           |
| ------------------------------ | ---- | -------------- |
| `src/agent/main.py`            | ~100 | Agent 核心逻辑 |
| `src/config.py`                | ~20  | 配置管理       |
| `src/tools/baidu_maps.py`      | ~30  | 百度地图工具   |
| `src/tools/tavily_search.py`   | ~80  | Tavily 搜索    |
| `src/utils/memory.py`          | ~120 | Memory 函数    |
| `src/utils/prompts.py`         | ~20  | 系统提示词     |
| `agentcore_baidu_map_agent.py` | ~10  | 入口文件       |

### 测试文件

| 文件                      | 行数 | 用途        |
| ------------------------- | ---- | ----------- |
| `tests/test_memory.py`    | ~150 | Memory 测试 |
| `clients/boto3_client.py` | ~200 | 客户端测试  |
| `verify_structure.py`     | ~150 | 结构验证    |

### 文档文件

| 文件                        | 字数  | 用途        |
| --------------------------- | ----- | ----------- |
| `README.md`                 | ~500  | 项目简介    |
| `docs/README.md`            | ~3000 | 详细指南    |
| `docs/ARCHITECTURE.md`      | ~2000 | 架构设计    |
| `docs/PROJECT_STRUCTURE.md` | ~1500 | 结构说明    |
| `docs/TESTING_GUIDE.md`     | ~1000 | 测试指南    |
| `docs/MEMORY_GUIDE.md`      | ~800  | Memory 指南 |
| `MIGRATION.md`              | ~1200 | 迁移指南    |
| `CHANGELOG.md`              | ~600  | 更新日志    |
| `PROJECT_OVERVIEW.md`       | ~2000 | 项目概览    |
| `OPTIMIZATION_SUMMARY.md`   | ~1800 | 优化总结    |
| `QUICK_REFERENCE.md`        | ~400  | 快速参考    |

### 配置文件

| 文件                      | 用途            |
| ------------------------- | --------------- |
| `.env.example`            | 环境变量模板    |
| `.gitignore`              | Git 忽略规则    |
| `.dockerignore`           | Docker 忽略规则 |
| `.bedrock_agentcore.yaml` | AgentCore 配置  |
| `requirements.txt`        | Python 依赖     |
| `Makefile`                | 命令快捷方式    |

## 文件依赖关系

```
agentcore_baidu_map_agent.py (入口)
    └── src/agent/main.py
        ├── src/config.py
        ├── src/tools/baidu_maps.py
        │   └── src/config.py
        ├── src/tools/tavily_search.py
        │   └── src/config.py
        ├── src/utils/memory.py
        └── src/utils/prompts.py

clients/boto3_client.py (独立)

tests/test_memory.py
    └── src/agent/main.py

verify_structure.py (独立)
```

## 文件大小统计

### 代码文件

- 总行数: ~900 行
- 平均每个模块: ~60 行
- 最大文件: `clients/boto3_client.py` (~200 行)
- 最小文件: `src/__init__.py` (1 行)

### 文档文件

- 总字数: ~15,000 字
- 平均每个文档: ~1,400 字
- 最大文档: `docs/README.md` (~3,000 字)

### 配置文件

- 总行数: ~100 行
- 环境变量: 4 个

## 文件状态

### ✅ 已完成

- 所有核心代码文件
- 所有测试文件
- 所有文档文件
- 所有配置文件
- 所有工具文件

### 🔄 持续更新

- `CHANGELOG.md` - 随版本更新
- `docs/README.md` - 随功能更新
- `requirements.txt` - 随依赖更新

### 📝 待添加

- 单元测试覆盖
- 集成测试
- 性能测试
- API 文档

## 维护建议

### 代码文件

- 保持模块独立性
- 每个文件不超过 200 行
- 添加完整的文档字符串

### 文档文件

- 代码变更后同步更新
- 保持示例的准确性
- 定期审查和更新

### 配置文件

- 敏感信息使用环境变量
- 提供完整的示例
- 添加必要的注释

## 快速查找

### 需要修改配置？

→ `src/config.py` 和 `.env`

### 需要添加工具？

→ `src/tools/` 目录

### 需要修改提示词？

→ `src/utils/prompts.py`

### 需要查看文档？

→ `docs/` 目录

### 需要运行测试？

→ `tests/` 目录

### 需要部署？

→ `agentcore_baidu_map_agent.py`

---

**生成时间**: 2025-10-21  
**文件总数**: 35  
**代码行数**: ~900  
**文档字数**: ~15,000
