# AgentCore 百度地图 Agent

基于 AWS Bedrock AgentCore 的智能地图助手，集成百度地图 MCP Server 和 Tavily 搜索功能。

## ✨ 功能特性

- 🗺️ **百度地图服务** - 地理编码、POI 搜索、路线规划、天气查询
- 🔍 **Tavily 网络搜索** - 实时网络信息检索
- 💬 **对话记忆** - 支持多轮对话上下文理解
- 🌊 **流式响应** - 实时返回处理结果
- ☁️ **云端托管** - AWS Bedrock AgentCore 自动扩展

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填写 API Keys
```

### 3. 部署

```bash
agentcore configure -e agentcore_baidu_map_agent.py
agentcore launch
```

### 4. 测试

```bash
# CLI 测试
agentcore invoke '{"prompt": "北京天安门的坐标是多少？"}'

# Python 客户端测试
python clients/boto3_client.py
```

## 📁 项目结构

```
.
├── src/                 # 源代码
│   ├── agent/          # Agent 核心
│   ├── tools/          # 工具模块
│   ├── utils/          # 工具函数
│   └── config.py       # 配置管理
├── clients/            # 客户端
├── tests/              # 测试
├── docs/               # 文档
└── agentcore_baidu_map_agent.py  # 入口文件
```

详细结构说明：[PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

## 📚 文档

- [详细部署指南](docs/README.md) - 完整的部署和使用说明
- [架构设计](docs/ARCHITECTURE.md) - 系统架构和设计原理
- [测试指南](docs/TESTING_GUIDE.md) - 测试方法和示例
- [Memory 指南](docs/MEMORY_GUIDE.md) - 对话记忆功能说明
- [项目结构](docs/PROJECT_STRUCTURE.md) - 代码组织和模块说明
- [迁移指南](MIGRATION.md) - 结构优化说明

## 🔧 开发

### 添加新工具

1. 在 `src/tools/` 创建工具文件
2. 在 `src/agent/main.py` 中加载
3. 更新文档

### 运行测试

```bash
python tests/test_memory.py
```

### 本地调试

```bash
python agentcore_baidu_map_agent.py
```

## 🎯 使用示例

```python
# 地理编码
"北京天安门的坐标是多少？"

# POI 搜索
"帮我搜索上海外滩附近的餐厅"

# 路线规划
"从成都到西安的自驾路线"

# 多轮对话
"搜索北京的天气"
"那里有什么著名景点？"  # Agent 会理解"那里"指北京
```

## 📝 许可证

MIT

---

**最近更新**: 2025-10-21 - 项目结构优化为模块化设计
