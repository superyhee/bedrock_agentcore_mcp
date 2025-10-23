# 快速参考指南

## 常用命令

### 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env

# 验证结构
python3 verify_structure.py

# 运行测试
python3 tests/test_memory.py
```

### 部署

```bash
# 配置 AgentCore
agentcore configure -e agentcore_baidu_map_agent.py

# 部署
agentcore launch

# 查看状态
agentcore status

# 销毁
agentcore destroy
```

### 测试

```bash
# CLI 测试
agentcore invoke '{"prompt": "你的问题"}'

# Python 客户端测试
python3 clients/boto3_client.py

# Memory 功能测试
python3 tests/test_memory.py
```

## 项目结构速查

```
src/
├── agent/main.py          # Agent 核心入口
├── tools/
│   ├── baidu_maps.py     # 百度地图工具
│   └── tavily_search.py  # Tavily 搜索
├── utils/
│   ├── memory.py         # Memory 函数
│   └── prompts.py        # 系统提示词
└── config.py             # 配置管理

clients/boto3_client.py    # 测试客户端
tests/test_memory.py       # Memory 测试
docs/                      # 所有文档
```

## 常用导入

```python
# Agent 核心
from src.agent.main import app, invoke

# 配置
from src.config import MEMORY_ID, REGION, MODEL_ID

# 工具
from src.tools.tavily_search import tavily_search
from src.tools.baidu_maps import initialize_baidu_mcp_client

# 工具函数
from src.utils.memory import get_actor_and_session_id
from src.utils.prompts import SYSTEM_PROMPT
```

## 环境变量

```bash
# AWS 配置
AWS_REGION=us-west-2
BEDROCK_AGENTCORE_MEMORY_ID=your-memory-id

# API Keys
BAIDU_MAPS_API_KEY=your-baidu-key
TAVILY_API_KEY=your-tavily-key
```

## 测试示例

### 地理编码

```bash
agentcore invoke '{"prompt": "北京天安门的坐标是多少？"}'
```

### POI 搜索

```bash
agentcore invoke '{"prompt": "帮我搜索上海外滩附近的餐厅"}'
```

### 路线规划

```bash
agentcore invoke '{"prompt": "从成都到西安的自驾路线"}'
```

### 多轮对话

```bash
# 第一轮
agentcore invoke '{"prompt": "搜索北京的天气"}'

# 第二轮（使用上下文）
agentcore invoke '{"prompt": "那里有什么著名景点？"}'
```

## 文档速查

| 文档                                                   | 用途         |
| ------------------------------------------------------ | ------------ |
| [README.md](README.md)                                 | 项目简介     |
| [docs/README.md](docs/README.md)                       | 详细部署指南 |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)           | 系统架构     |
| [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | 项目结构     |
| [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)         | 测试指南     |
| [docs/MEMORY_GUIDE.md](docs/MEMORY_GUIDE.md)           | Memory 指南  |
| [MIGRATION.md](MIGRATION.md)                           | 迁移指南     |
| [CHANGELOG.md](CHANGELOG.md)                           | 更新日志     |

## 常见问题

### Q: 如何添加新工具？

A: 在 `src/tools/` 创建新文件，在 `src/agent/main.py` 的 `_load_tools()` 中加载。

### Q: 如何修改配置？

A: 编辑 `src/config.py` 和 `.env` 文件。

### Q: 如何运行测试？

A: `python3 tests/test_memory.py`

### Q: 部署失败怎么办？

A: 检查 `.env` 配置，查看 `agentcore status` 日志。

### Q: 如何查看日志？

A: 使用 `agentcore status` 获取日志命令。

## 快速链接

- 🏠 [项目主页](README.md)
- 📖 [完整文档](docs/)
- 🐛 [问题反馈](https://github.com/your-repo/issues)
- 💬 [讨论区](https://github.com/your-repo/discussions)

## 版本信息

- **当前版本**: 2.0.0
- **最后更新**: 2025-10-21
- **Python 版本**: 3.10+
- **AWS 区域**: us-west-2

---

**提示**: 使用 `Ctrl+F` 快速搜索本文档
