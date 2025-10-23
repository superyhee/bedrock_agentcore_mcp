# 项目结构优化说明

## 优化内容

项目已从扁平结构重构为模块化结构，提高了代码的可维护性和可扩展性。

## 新旧结构对比

### 旧结构（扁平）

```
.
├── agentcore_baidu_map_agent.py  # 所有代码在一个文件
├── boto3_client.py
├── test_memory.py
├── README.md
├── ARCHITECTURE.md
├── TESTING_GUIDE.md
├── MEMORY_GUIDE.md
└── requirements.txt
```

### 新结构（模块化）

```
.
├── src/                          # 源代码
│   ├── agent/                   # Agent 核心
│   │   └── main.py
│   ├── tools/                   # 工具模块
│   │   ├── baidu_maps.py
│   │   └── tavily_search.py
│   ├── utils/                   # 工具函数
│   │   ├── memory.py
│   │   └── prompts.py
│   └── config.py                # 配置管理
├── clients/                      # 客户端
│   └── boto3_client.py
├── tests/                        # 测试
│   └── test_memory.py
├── docs/                         # 文档
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── TESTING_GUIDE.md
│   ├── MEMORY_GUIDE.md
│   └── PROJECT_STRUCTURE.md
├── agentcore_baidu_map_agent.py  # 向后兼容入口
├── README.md                     # 项目主 README
└── requirements.txt
```

## 主要改进

### 1. 模块化设计

- **配置管理**: 所有配置集中在 `src/config.py`
- **工具分离**: 每个工具独立文件，便于维护
- **工具函数**: Memory 和提示词相关函数独立管理
- **清晰分层**: Agent → Tools → Utils

### 2. 代码复用

- 配置统一管理，避免重复
- 工具函数可在多处复用
- 便于单元测试

### 3. 文档组织

- 所有文档移至 `docs/` 目录
- 新增项目结构说明文档
- 保持文档的完整性和可访问性

### 4. 向后兼容

- 保留原有入口文件 `agentcore_baidu_map_agent.py`
- 自动重定向到新结构
- 现有部署无需修改

## 使用说明

### 部署（无需修改）

```bash
# 配置和部署命令保持不变
agentcore configure -e agentcore_baidu_map_agent.py
agentcore launch
```

### 开发

```python
# 导入 Agent
from src.agent.main import app, invoke

# 导入工具
from src.tools.tavily_search import tavily_search
from src.tools.baidu_maps import initialize_baidu_mcp_client

# 导入配置
from src.config import MEMORY_ID, REGION, MODEL_ID

# 导入工具函数
from src.utils.memory import get_actor_and_session_id
from src.utils.prompts import SYSTEM_PROMPT
```

### 测试

```bash
# 运行测试
python tests/test_memory.py

# 或使用 pytest
pytest tests/
```

## 文件映射

| 旧位置                         | 新位置                       | 说明             |
| ------------------------------ | ---------------------------- | ---------------- |
| `agentcore_baidu_map_agent.py` | `src/agent/main.py`          | Agent 核心代码   |
| -                              | `src/config.py`              | 配置管理（新增） |
| -                              | `src/tools/baidu_maps.py`    | 百度地图工具     |
| -                              | `src/tools/tavily_search.py` | Tavily 搜索工具  |
| -                              | `src/utils/memory.py`        | Memory 工具函数  |
| -                              | `src/utils/prompts.py`       | 系统提示词       |
| `boto3_client.py`              | `clients/boto3_client.py`    | 测试客户端       |
| `test_memory.py`               | `tests/test_memory.py`       | Memory 测试      |
| `README.md`                    | `docs/README.md`             | 详细文档         |
| `ARCHITECTURE.md`              | `docs/ARCHITECTURE.md`       | 架构文档         |
| `TESTING_GUIDE.md`             | `docs/TESTING_GUIDE.md`      | 测试指南         |
| `MEMORY_GUIDE.md`              | `docs/MEMORY_GUIDE.md`       | Memory 指南      |

## 优势

### 开发效率

- ✅ 代码结构清晰，易于理解
- ✅ 模块独立，便于并行开发
- ✅ 配置集中，修改方便

### 可维护性

- ✅ 职责分离，降低耦合
- ✅ 便于定位和修复问题
- ✅ 易于添加新功能

### 可测试性

- ✅ 模块独立，便于单元测试
- ✅ 测试代码独立目录
- ✅ 提高测试覆盖率

### 可扩展性

- ✅ 添加新工具只需新建文件
- ✅ 修改配置不影响业务逻辑
- ✅ 便于集成新功能

## 注意事项

1. **导入路径**: 如果你有自定义代码，需要更新导入路径
2. **环境变量**: 配置项现在统一在 `src/config.py` 管理
3. **测试**: 运行测试前确保导入路径正确
4. **部署**: 入口文件保持不变，无需修改部署配置

## 下一步

1. 查看 [项目结构文档](docs/PROJECT_STRUCTURE.md) 了解详细结构
2. 查看 [部署指南](docs/README.md) 了解如何部署
3. 查看 [架构文档](docs/ARCHITECTURE.md) 了解系统设计
4. 开始开发新功能！

## 问题反馈

如果在使用新结构时遇到问题，请检查：

1. 导入路径是否正确
2. 环境变量是否配置
3. 依赖是否安装完整

---

**优化完成时间**: 2025-10-21
