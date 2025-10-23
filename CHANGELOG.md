# 更新日志

## [2.0.0] - 2025-10-21

### 重大变更 - 项目结构优化

#### 新增

- ✨ 模块化代码结构
- 📁 `src/` 源代码目录
  - `agent/` - Agent 核心模块
  - `tools/` - 工具模块
  - `utils/` - 工具函数模块
  - `config.py` - 配置管理
- 📁 `clients/` 客户端目录
- 📁 `tests/` 测试目录
- 📁 `docs/` 文档目录
- 📄 项目结构文档 (`docs/PROJECT_STRUCTURE.md`)
- 📄 迁移指南 (`MIGRATION.md`)
- 📄 更新日志 (`CHANGELOG.md`)
- 🔧 `.gitignore` 文件

#### 改进

- 🔨 代码重构为模块化设计
- 📦 配置集中管理
- 🧪 测试代码独立目录
- 📚 文档统一组织
- ♻️ 提高代码复用性
- 🎯 清晰的职责分离

#### 向后兼容

- ✅ 保留原有入口文件 `agentcore_baidu_map_agent.py`
- ✅ 自动重定向到新结构
- ✅ 部署命令无需修改

### 文件变更

#### 移动

- `test_memory.py` → `tests/test_memory.py`
- `boto3_client.py` → `clients/boto3_client.py`
- `README.md` → `docs/README.md` (详细文档)
- `ARCHITECTURE.md` → `docs/ARCHITECTURE.md`
- `TESTING_GUIDE.md` → `docs/TESTING_GUIDE.md`
- `MEMORY_GUIDE.md` → `docs/MEMORY_GUIDE.md`
- `SUMMARY.md` → `docs/SUMMARY.md`

#### 拆分

- `agentcore_baidu_map_agent.py` 拆分为：
  - `src/agent/main.py` - Agent 核心
  - `src/tools/baidu_maps.py` - 百度地图工具
  - `src/tools/tavily_search.py` - Tavily 搜索工具
  - `src/utils/memory.py` - Memory 工具函数
  - `src/utils/prompts.py` - 系统提示词
  - `src/config.py` - 配置管理

#### 新建

- `README.md` - 新的简洁主 README
- `MIGRATION.md` - 迁移指南
- `CHANGELOG.md` - 本文件
- `docs/PROJECT_STRUCTURE.md` - 项目结构说明
- `.gitignore` - Git 忽略文件

### 优势

#### 开发效率

- 代码结构清晰，易于理解
- 模块独立，便于并行开发
- 配置集中，修改方便

#### 可维护性

- 职责分离，降低耦合
- 便于定位和修复问题
- 易于添加新功能

#### 可测试性

- 模块独立，便于单元测试
- 测试代码独立目录
- 提高测试覆盖率

#### 可扩展性

- 添加新工具只需新建文件
- 修改配置不影响业务逻辑
- 便于集成新功能

### 迁移指南

详见 [MIGRATION.md](MIGRATION.md)

### 文档

- [项目结构](docs/PROJECT_STRUCTURE.md)
- [部署指南](docs/README.md)
- [架构设计](docs/ARCHITECTURE.md)
- [测试指南](docs/TESTING_GUIDE.md)
- [Memory 指南](docs/MEMORY_GUIDE.md)

---

## [1.0.0] - 2025-10-20

### 初始版本

- ✨ 集成百度地图 MCP Server
- ✨ 集成 Tavily 搜索
- ✨ AgentCore Memory 支持
- ✨ 流式响应输出
- 📚 完整文档
