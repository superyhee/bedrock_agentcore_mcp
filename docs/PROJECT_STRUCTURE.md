# 项目结构说明

## 目录结构

```
.
├── src/                        # 源代码目录
│   ├── __init__.py
│   ├── config.py              # 配置管理（环境变量、常量）
│   ├── agent/                 # Agent 核心模块
│   │   ├── __init__.py
│   │   └── main.py           # AgentCore 主入口，包含 invoke 函数
│   ├── tools/                 # 工具模块
│   │   ├── __init__.py
│   │   ├── baidu_maps.py     # 百度地图 MCP 客户端
│   │   └── tavily_search.py  # Tavily 搜索工具
│   └── utils/                 # 工具函数模块
│       ├── __init__.py
│       ├── memory.py         # Memory 相关函数
│       └── prompts.py        # 系统提示词配置
│
├── clients/                   # 客户端代码
│   ├── __init__.py
│   └── boto3_client.py       # Boto3 测试客户端
│
├── tests/                     # 测试代码
│   ├── __init__.py
│   └── test_memory.py        # Memory 功能测试
│
├── docs/                      # 文档目录
│   ├── __init__.py
│   ├── README.md             # 详细部署指南
│   ├── ARCHITECTURE.md       # 系统架构文档
│   ├── TESTING_GUIDE.md      # 测试指南
│   ├── MEMORY_GUIDE.md       # Memory 使用指南
│   ├── SUMMARY.md            # 项目总结
│   └── PROJECT_STRUCTURE.md  # 本文档
│
├── agentcore_baidu_map_agent.py  # 向后兼容入口（重定向到 src/agent/main.py）
├── requirements.txt          # Python 依赖
├── .env.example              # 环境变量示例
├── .gitignore                # Git 忽略文件
├── .dockerignore             # Docker 忽略文件
├── .bedrock_agentcore.yaml   # AgentCore 配置（部署后生成）
└── README.md                 # 项目主 README
```

## 模块说明

### src/config.py

集中管理所有配置项：

- AWS 配置（Region、Memory ID、Model ID）
- API Keys（百度地图、Tavily）
- API 配置（URL、超时时间）

### src/agent/main.py

AgentCore 主入口文件：

- `app`: BedrockAgentCoreApp 实例
- `invoke()`: AgentCore 入口函数，处理流式响应
- `_load_tools()`: 加载所有可用工具

### src/tools/

工具模块，每个文件对应一个工具集：

- `baidu_maps.py`: 百度地图 MCP 客户端初始化
- `tavily_search.py`: Tavily 搜索工具实现

### src/utils/

工具函数模块：

- `memory.py`: Memory 相关函数（会话管理、上下文检索）
- `prompts.py`: 系统提示词配置

### clients/

客户端代码，用于测试和调用部署的 Agent：

- `boto3_client.py`: 使用 Boto3 调用 AgentCore Runtime

### tests/

测试代码：

- `test_memory.py`: 测试对话记忆功能

### docs/

项目文档：

- `README.md`: 详细的部署和使用指南
- `ARCHITECTURE.md`: 系统架构设计文档
- `TESTING_GUIDE.md`: 测试指南
- `MEMORY_GUIDE.md`: Memory 功能使用指南

## 设计原则

### 1. 模块化

- 每个功能模块独立，职责单一
- 便于维护和扩展

### 2. 可复用

- 工具和工具函数可以在不同场景复用
- 配置集中管理，避免重复

### 3. 可测试

- 模块独立，便于单元测试
- 提供专门的测试目录

### 4. 向后兼容

- 保留原有的 `agentcore_baidu_map_agent.py` 入口
- 重定向到新的模块化结构

### 5. 清晰的文档

- 每个模块都有详细的文档字符串
- 提供完整的项目文档

## 依赖关系

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
```

## 部署说明

部署时，AgentCore 会使用 `agentcore_baidu_map_agent.py` 作为入口文件，该文件会自动导入并使用新的模块化结构。

```bash
# 配置（指定入口文件）
agentcore configure -e agentcore_baidu_map_agent.py

# 部署
agentcore launch
```

## 开发建议

### 添加新工具

1. 在 `src/tools/` 创建新的工具文件
2. 在 `src/agent/main.py` 的 `_load_tools()` 中加载
3. 更新文档

### 修改配置

1. 在 `src/config.py` 中添加新配置项
2. 在 `.env.example` 中添加示例
3. 更新文档

### 添加工具函数

1. 在 `src/utils/` 对应模块中添加函数
2. 在需要的地方导入使用
3. 添加单元测试

### 编写测试

1. 在 `tests/` 目录创建测试文件
2. 使用 `pytest` 运行测试
3. 确保测试覆盖率

## 迁移指南

如果你有基于旧结构的代码，可以这样迁移：

### 旧代码

```python
from agentcore_baidu_map_agent import invoke, tavily_search
```

### 新代码

```python
from src.agent.main import invoke
from src.tools.tavily_search import tavily_search
```

或者继续使用旧的导入方式（向后兼容）：

```python
from agentcore_baidu_map_agent import invoke
```
