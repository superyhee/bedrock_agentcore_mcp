# AgentCore 流式输出测试指南

本指南介绍如何测试 AgentCore 百度地图 Agent 的流式输出功能。

## 🚀 快速开始

### 选项 1: 使用测试脚本（最简单）

```bash
# 本地测试
./test_streaming.sh local

# 部署后测试
./test_streaming.sh deployed
```

### 选项 2: 手动测试

## 📋 测试方法详解

### 方法 1: agentcore invoke（推荐）

这是最简单和推荐的测试方法，会自动显示流式输出。

#### 本地测试步骤

**终端 1 - 启动本地 Runtime:**

```bash
# 启动本地 AgentCore Runtime
agentcore launch --local

# 你会看到类似输出:
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8080
```

**终端 2 - 调用 Agent:**

```bash
# 测试基本查询
agentcore invoke '{"prompt": "北京天安门广场的经纬度是多少？"}' --local

# 测试搜索功能
agentcore invoke '{"prompt": "帮我搜索上海外滩附近的餐厅"}' --local

# 测试位置查询
agentcore invoke '{"prompt": "深圳市南山区科技园的位置信息"}' --local
```

#### 部署后测试步骤

```bash
# 1. 部署到 AWS
agentcore launch

# 2. 调用已部署的 Agent
agentcore invoke '{"prompt": "北京天安门广场的经纬度是多少？"}'

# 3. 使用 session ID 保持会话上下文
SESSION_ID="my-session-$(date +%s)"
agentcore invoke '{"prompt": "北京天安门广场的经纬度是多少？"}' --session-id "$SESSION_ID"
agentcore invoke '{"prompt": "那附近有什么景点？"}' --session-id "$SESSION_ID"
```

### 方法 2: 使用 Boto3 客户端

```bash
# 确保已部署 Agent
agentcore launch

# 测试单个问题
python boto3_client.py "北京天安门广场的经纬度是多少？"

# 运行所有测试问题
python boto3_client.py
```

### 方法 3: 使用 curl

```bash
# 确保本地 Runtime 正在运行
agentcore launch --local

# 在另一个终端使用 curl 测试
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "北京天安门广场的经纬度是多少？"}' \
  --no-buffer

# --no-buffer 很重要，确保立即显示流式输出
```

### 方法 4: 直接运行 Python 文件

```bash
# 直接运行 Agent 文件
python agentcore_baidu_map_agent.py

# 在另一个终端测试
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "北京天安门广场的经纬度是多少？"}' \
  --no-buffer
```

## 🔍 观察流式输出

当你调用 Agent 时，你应该能看到类似这样的流式输出：

```
╭────────── agentcore_baidu_map_agent ──────────╮
│ Session: session_abc123...                     │
│ Request ID: req-456...                         │
│ ARN: arn:aws:bedrock-agentcore:...            │
╰────────────────────────────────────────────────╯

Response:
{"type": "text", "content": "正在查询北京天安门广场的位置信息..."}
{"type": "tool_call", "tool": "baidu_geocoding", "args": {...}}
{"type": "tool_result", "result": {...}}
{"type": "text", "content": "北京天安门广场的经纬度是..."}
```

## 📊 测试用例

### 测试用例 1: 地理编码

```bash
agentcore invoke '{"prompt": "北京天安门广场的经纬度是多少？"}' --local
```

**期望**: 应该调用百度地图工具，返回经纬度坐标

### 测试用例 2: POI 搜索

```bash
agentcore invoke '{"prompt": "帮我搜索上海外滩附近的餐厅"}' --local
```

**期望**: 应该调用百度地图 POI 搜索工具，返回餐厅列表

### 测试用例 3: 网络搜索

```bash
agentcore invoke '{"prompt": "2024年最新的人工智能发展趋势"}' --local
```

**期望**: 应该调用 Tavily 搜索工具，返回网络搜索结果

### 测试用例 4: 会话上下文

```bash
SESSION_ID="test-$(date +%s)"
agentcore invoke '{"prompt": "北京天安门广场在哪里？"}' --session-id "$SESSION_ID" --local
agentcore invoke '{"prompt": "那附近有什么景点？"}' --session-id "$SESSION_ID" --local
```

**期望**: 第二个问题应该能理解"那附近"指的是天安门广场

## 🐛 故障排查

### 问题 1: 看不到流式输出

**可能原因**:

- 使用了旧版本的客户端
- 网络缓冲问题

**解决方案**:

```bash
# 使用 curl 时添加 --no-buffer
curl --no-buffer ...

# 使用 agentcore invoke 会自动处理流式输出
agentcore invoke '{"prompt": "..."}' --local
```

### 问题 2: 本地测试连接失败

**可能原因**: 本地 Runtime 未启动

**解决方案**:

```bash
# 检查 8080 端口是否被占用
lsof -i :8080

# 启动本地 Runtime
agentcore launch --local
```

### 问题 3: 工具调用失败

**可能原因**: 环境变量未设置

**解决方案**:

```bash
# 检查环境变量
echo $BAIDU_MAPS_API_KEY
echo $TAVILY_API_KEY

# 设置环境变量
export BAIDU_MAPS_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

# 或者在 .env 文件中设置
```

### 问题 4: Memory 配置错误

**可能原因**: 未配置 AgentCore Memory

**解决方案**:

```bash
# 配置 Memory
agentcore configure --entrypoint agentcore_baidu_map_agent.py

# 检查配置
agentcore status
```

## 📝 查看日志

### 本地日志

本地运行时，日志会直接显示在终端中。

### AWS CloudWatch 日志

```bash
# 部署后，agentcore invoke 会显示日志命令
agentcore invoke '{"prompt": "test"}'

# 输出会包含类似这样的命令:
# aws logs tail /aws/bedrock-agentcore/... --follow

# 复制并运行该命令查看实时日志
```

## 🎯 性能测试

### 测试响应时间

```bash
# 使用 time 命令测量
time agentcore invoke '{"prompt": "北京天安门广场的经纬度是多少？"}' --local

# 观察流式输出的首字节时间（TTFB）
```

### 并发测试

```bash
# 使用多个终端同时调用
for i in {1..5}; do
  agentcore invoke '{"prompt": "测试问题 '$i'"}' --local &
done
wait
```

## 📚 更多资源

- [AgentCore 文档](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Strands Agent 文档](https://strands.ai/)
- [流式输出实现指南](./STREAMING_GUIDE.md)
- [项目 README](./README_AGENTCORE.md)
