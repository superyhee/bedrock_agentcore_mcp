# AgentCore 短期记忆功能指南

## 概述

本 Agent 集成了 **AgentCore Memory** 的短期记忆功能，能够记住对话历史并理解上下文，提供更智能的对话体验。

## 功能特性

### 1. 对话历史记忆

- 自动保存每轮对话（用户输入和 Agent 回复）
- 支持跨会话的对话历史持久化
- 最多保留最近 10 轮对话作为上下文

### 2. 上下文理解

Agent 可以理解以下类型的指代：

- **地点指代**："那里"、"这个地方"、"刚才说的城市"
- **时间指代**："刚才"、"之前"、"上次"
- **事物指代**："它"、"这个"、"那个"

### 3. 智能提示增强

系统会自动将对话历史注入到用户提示中，帮助 LLM 理解上下文。

## 使用方法

### 基本用法

```python
# 启用对话历史（默认）
payload = {
    "prompt": "那里有什么好吃的？",
    "use_history": True  # 可选，默认为 True
}
```

### 禁用对话历史

```python
# 如果不需要上下文，可以禁用
payload = {
    "prompt": "今天天气怎么样？",
    "use_history": False
}
```

### CLI 使用

```bash
# 开始对话
agentcore invoke '{"prompt": "帮我搜索北京的天气"}' --session-id my-session

# 继续对话（使用相同的 session-id）
agentcore invoke '{"prompt": "那里有什么景点？"}' --session-id my-session

# Agent 会理解"那里"指的是北京
```

## 对话示例

### 示例 1：地点查询

```
用户: 帮我搜索一下上海的美食
Agent: [搜索上海美食信息...]

用户: 那里的交通方便吗？
Agent: 上海的交通非常方便，有地铁、公交... [理解"那里"=上海]

用户: 从北京到那个城市怎么走？
Agent: 从北京到上海可以选择... [理解"那个城市"=上海]
```

### 示例 2：路线规划

```
用户: 我想从天安门到故宫
Agent: [规划路线...]

用户: 这条路线需要多长时间？
Agent: 从天安门到故宫大约需要... [理解指代关系]

用户: 附近有地铁站吗？
Agent: 在故宫附近有以下地铁站... [理解"附近"指故宫]
```

### 示例 3：信息查询

```
用户: 搜索一下 AWS Lambda 的最新功能
Agent: [搜索 AWS Lambda 信息...]

用户: 它支持哪些编程语言？
Agent: AWS Lambda 支持以下编程语言... [理解"它"=Lambda]

用户: 价格怎么样？
Agent: AWS Lambda 的定价... [理解上下文]
```

## 技术实现

### 对话历史存储

```python
# 对话历史自动存储在 AgentCore Memory 中
# 每个用户和会话都有独立的存储空间

actor_id = "user123"
session_id = "conversation_001"

# Memory 路径结构
/users/{actor_id}/facts          # 用户相关事实
/users/{actor_id}/preferences    # 用户偏好
/users/{actor_id}/locations      # 位置信息
```

### 上下文增强

```python
def _build_context_aware_prompt(prompt, conversation_history):
    """
    将对话历史注入到提示中

    输入: "那里有什么景点？"

    输出:
    [对话历史]:
    1. user: 帮我搜索北京的天气
    2. assistant: 北京今天天气晴朗...

    [当前问题]:
    那里有什么景点？
    """
```

### 历史检索

```python
# 获取最近 10 轮对话
conversation_history = await _get_conversation_context(
    session_manager,
    max_turns=10
)
```

## 配置选项

### Memory 配置

在 `.bedrock_agentcore.yaml` 中配置：

```yaml
memory:
  enabled: true
  strategies:
    - type: semantic
      namespaces:
        - /users/{actorId}/facts
        - /users/{actorId}/preferences
        - /users/{actorId}/locations
```

### 检索配置

```python
retrieval_config = {
    f"/users/{actor_id}/facts": RetrievalConfig(
        top_k=5,              # 检索前5条相关记录
        relevance_score=0.5   # 相关性阈值
    ),
    f"/users/{actor_id}/preferences": RetrievalConfig(
        top_k=3,
        relevance_score=0.5
    ),
    f"/users/{actor_id}/locations": RetrievalConfig(
        top_k=5,
        relevance_score=0.5
    )
}
```

## 最佳实践

### 1. 使用有意义的 Session ID

```bash
# 好的做法：使用描述性的 session ID
--session-id "user123-travel-planning-2025"

# 避免：使用随机或无意义的 ID
--session-id "abc123"
```

### 2. 合理使用对话历史

```python
# 对于需要上下文的对话，启用历史
payload = {"prompt": "那里怎么样？", "use_history": True}

# 对于独立的查询，可以禁用以提高性能
payload = {"prompt": "今天日期是多少？", "use_history": False}
```

### 3. 定期清理旧会话

```python
# 在生产环境中，定期清理不活跃的会话
# 避免 Memory 存储过多无用数据
```

### 4. 监控 Memory 使用

```python
# 使用 AgentCore Observability 监控
# - Memory 读写延迟
# - 存储使用量
# - 检索准确率
```

## 性能考虑

### 延迟影响

- 获取对话历史：~50-100ms
- 构建增强提示：~10-20ms
- 总体影响：轻微（<150ms）

### 成本优化

- 只保留最近 10 轮对话（可配置）
- 对话历史压缩（只保留关键信息）
- 按需启用/禁用历史功能

### 扩展性

- 每个用户独立的 Memory 空间
- 支持数百万并发会话
- 自动扩展的存储后端

## 故障排查

### 问题 1：Agent 无法理解上下文

**可能原因**：

- Memory 未正确配置
- Session ID 不一致
- 对话历史未启用

**解决方案**：

```bash
# 检查 Memory 配置
agentcore configure --check

# 确保使用相同的 session-id
agentcore invoke '{"prompt": "..."}' --session-id same-id

# 确认启用历史
payload = {"prompt": "...", "use_history": True}
```

### 问题 2：对话历史为空

**可能原因**：

- 首次对话（没有历史）
- Session ID 错误
- Memory 服务异常

**解决方案**：

```python
# 检查日志
logger.info(f"Retrieved {len(conversation_history)} conversation turns")

# 验证 Memory 连接
# 查看 CloudWatch Logs
```

### 问题 3：性能下降

**可能原因**：

- 对话历史过长
- Memory 检索慢

**解决方案**：

```python
# 减少历史轮数
conversation_history = await _get_conversation_context(
    session_manager,
    max_turns=5  # 从 10 减少到 5
)

# 或禁用不必要的查询
payload = {"prompt": "...", "use_history": False}
```

## 下一步

- 查看 [TESTING_GUIDE.md](./TESTING_GUIDE.md) 了解如何测试
- 查看 [README_AGENTCORE.md](./README_AGENTCORE.md) 了解部署
- 运行 `python test_memory.py` 测试记忆功能

## 参考资料

- [AgentCore Memory 文档](https://aws.github.io/bedrock-agentcore-starter-toolkit/user-guide/memory/quickstart.html)
- [Session Management 示例](https://aws.github.io/bedrock-agentcore-starter-toolkit/examples/session-management.html)
- [Strands Agent 文档](https://strands.ai/docs)
