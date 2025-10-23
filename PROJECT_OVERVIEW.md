# 项目概览

## 项目信息

**项目名称**: AgentCore 百度地图 Agent  
**版本**: 2.0.0  
**最后更新**: 2025-10-21  
**状态**: ✅ 生产就绪

## 简介

基于 AWS Bedrock AgentCore 的智能地图助手，集成百度地图 MCP Server 和 Tavily 搜索功能，支持对话记忆和流式响应。

## 核心功能

### 1. 百度地图服务 🗺️

- 地理编码（地址 ↔ 坐标）
- POI 搜索（餐厅、酒店、景点等）
- 路线规划（驾车、步行、骑行、公交）
- 天气查询
- 交通路况

### 2. Tavily 网络搜索 🔍

- 实时网络信息检索
- 智能答案摘要
- 多源信息聚合

### 3. 对话记忆 💬

- 短期记忆（最近 10 轮对话）
- 上下文理解
- 指代消解

### 4. 流式响应 🌊

- 实时返回处理结果
- 降低首字延迟
- 提升用户体验

## 技术栈

### 核心框架

- **AWS Bedrock AgentCore** - 云端 Agent 托管平台
- **Strands Agents** - Agent 开发框架
- **Claude 3.7 Sonnet** - 大语言模型

### 工具集成

- **百度地图 MCP Server** - 地图服务
- **Tavily API** - 网络搜索
- **AgentCore Memory** - 对话记忆

### 开发工具

- **Python 3.10+** - 编程语言
- **Boto3** - AWS SDK
- **python-dotenv** - 环境变量管理

## 项目结构

```
AgentCore-Baidu-Map-Agent/
│
├── 📁 src/                      # 源代码
│   ├── 📁 agent/               # Agent 核心
│   │   └── main.py            # 主入口
│   ├── 📁 tools/               # 工具模块
│   │   ├── baidu_maps.py      # 百度地图
│   │   └── tavily_search.py   # Tavily 搜索
│   ├── 📁 utils/               # 工具函数
│   │   ├── memory.py          # Memory 函数
│   │   └── prompts.py         # 系统提示词
│   └── config.py              # 配置管理
│
├── 📁 clients/                  # 客户端
│   └── boto3_client.py        # Boto3 测试客户端
│
├── 📁 tests/                    # 测试
│   └── test_memory.py         # Memory 测试
│
├── 📁 docs/                     # 文档
│   ├── README.md              # 详细部署指南
│   ├── ARCHITECTURE.md        # 架构设计
│   ├── TESTING_GUIDE.md       # 测试指南
│   ├── MEMORY_GUIDE.md        # Memory 指南
│   ├── PROJECT_STRUCTURE.md   # 项目结构
│   └── SUMMARY.md             # 项目总结
│
├── 📄 agentcore_baidu_map_agent.py  # 入口文件
├── 📄 README.md                     # 项目主 README
├── 📄 MIGRATION.md                  # 迁移指南
├── 📄 CHANGELOG.md                  # 更新日志
├── 📄 PROJECT_OVERVIEW.md           # 本文件
├── 📄 requirements.txt              # Python 依赖
├── 📄 .env.example                  # 环境变量示例
├── 📄 .gitignore                    # Git 忽略
└── 📄 .bedrock_agentcore.yaml       # AgentCore 配置
```

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd AgentCore-Baidu-Map-Agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

```bash
cp .env.example .env
# 编辑 .env，填写 API Keys
```

### 4. 部署

```bash
agentcore configure -e agentcore_baidu_map_agent.py
agentcore launch
```

### 5. 测试

```bash
python clients/boto3_client.py
```

## 文档导航

### 入门文档

- [README.md](README.md) - 项目简介和快速开始
- [docs/README.md](docs/README.md) - 详细部署指南

### 技术文档

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - 系统架构设计
- [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - 代码组织结构

### 使用文档

- [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md) - 测试方法和示例
- [docs/MEMORY_GUIDE.md](docs/MEMORY_GUIDE.md) - Memory 功能说明

### 维护文档

- [MIGRATION.md](MIGRATION.md) - 结构优化说明
- [CHANGELOG.md](CHANGELOG.md) - 版本更新日志

## 开发指南

### 添加新工具

1. 在 `src/tools/` 创建工具文件
2. 实现工具函数（使用 `@tool` 装饰器）
3. 在 `src/agent/main.py` 的 `_load_tools()` 中加载
4. 更新文档

### 修改配置

1. 在 `src/config.py` 添加配置项
2. 在 `.env.example` 添加示例
3. 更新相关文档

### 编写测试

1. 在 `tests/` 创建测试文件
2. 编写测试用例
3. 运行测试验证

### 更新文档

1. 修改代码后同步更新文档
2. 保持文档的准确性和完整性
3. 添加必要的示例和说明

## 部署架构

```
┌─────────────────────────────────────────┐
│         AWS Bedrock AgentCore           │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │      Runtime (Serverless)         │ │
│  │  • 自动扩展                       │ │
│  │  • 负载均衡                       │ │
│  │  • 流式响应                       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │      Memory (DynamoDB)            │ │
│  │  • 对话历史                       │ │
│  │  • 语义搜索                       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │   CloudWatch Logs & Metrics       │ │
│  │  • 日志聚合                       │ │
│  │  • 性能监控                       │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 性能指标

### 响应时间

- 首字延迟: < 1s
- 平均响应: 2-5s
- 流式输出: 实时

### 可用性

- 自动扩展: ✅
- 负载均衡: ✅
- 故障恢复: ✅

### 成本优化

- 按需付费: ✅
- 自动休眠: ✅
- 资源优化: ✅

## 安全性

### 认证授权

- AWS IAM 权限控制
- Actor ID 隔离
- Session 级别隔离

### 数据安全

- 传输加密 (TLS)
- 存储加密 (DynamoDB)
- API Key 安全管理

### 监控审计

- CloudWatch 日志
- X-Ray 追踪
- 操作审计

## 最佳实践

### 开发环境

- 使用 `.env` 文件管理配置
- 本地测试通过后再部署
- 使用版本控制

### 测试环境

- 启用 Observability
- 监控日志和指标
- 定期测试功能

### 生产环境

- 使用 AWS Secrets Manager
- 配置 IAM 权限最小化
- 设置监控告警
- 定期审查日志

## 贡献指南

### 代码规范

- 遵循 PEP 8 风格
- 添加类型注解
- 编写文档字符串

### 提交规范

- 清晰的提交信息
- 关联 Issue
- 更新文档

### 测试要求

- 添加单元测试
- 确保测试通过
- 保持测试覆盖率

## 许可证

MIT License

## 联系方式

- 项目仓库: [GitHub](https://github.com/your-repo)
- 问题反馈: [Issues](https://github.com/your-repo/issues)
- 文档: [Wiki](https://github.com/your-repo/wiki)

## 致谢

- AWS Bedrock AgentCore Team
- Strands Agents Framework
- 百度地图 MCP Server
- Tavily Search API

---

**最后更新**: 2025-10-21  
**维护者**: Your Team  
**版本**: 2.0.0
