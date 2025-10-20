# AgentCore 部署指南

将百度地图 + Tavily 搜索 Agent 部署到 AWS Bedrock AgentCore。

## 🎯 为什么使用 AgentCore？

- ✅ **Runtime 托管** - 自动容器编排和扩展
- ✅ **企业级** - 高可用、安全、可观测
- ✅ **成本优化** - 按需付费
- ✅ **监控** - X-Ray 追踪 + CloudWatch 日志

## 📋 前置条件

### AWS 配置

- AWS CLI 已安装并配置
- AWS 区域已设置（如 us-west-2）
- Bedrock 模型访问已启用（Claude 3.7 Sonnet）
- IAM 权限：`AmazonBedrockAgentCoreFullAccess`

### 本地环境

- Python 3.10+
- `.env` 文件配置好 API Keys

## 🚀 快速部署

### 方式 1: 手动部署

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate
# 1. 安装工具包
pip install "bedrock-agentcore-starter-toolkit>=0.1.21" strands-agents boto3

# 2. 配置
agentcore configure -e agentcore_baidu_map_agent.py

# 3. 部署
agentcore launch

# 4. 测试
agentcore invoke '{"prompt": "你好"}'
```

## 🔑 环境变量配置

### 生产环境（推荐）

使用 AWS Secrets Manager：

```bash
# 创建 Secret
aws secretsmanager create-secret \
  --name baidu-maps-api-key \
  --secret-string "your_key" \
  --region us-west-2

# 修改代码使用 Secrets Manager
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

BAIDU_API_KEY = get_secret('baidu-maps-api-key')
```

## 🧪 测试部署

### 使用测试客户端（推荐）

我们提供了专门的测试客户端程序：

```bash
# 快速测试（推荐）
python boto3_client.py

```

**功能**:

- ✅ 自动化测试套件
- ✅ 交互式对话
- ✅ 性能统计
- ✅ 错误诊断

查看详细使用说明：[TEST_CLIENT_GUIDE.md](TEST_CLIENT_GUIDE.md)

### 使用 CLI 测试

### 基本功能测试

```bash
# 1. 基本对话
agentcore invoke '{"prompt": "你好，介绍一下你的功能"}'

# 2. 功能列表
agentcore invoke '{"prompt": "你能帮我做什么？"}'
```

### 地理编码测试

```bash
# 地址转坐标
agentcore invoke '{"prompt": "北京天安门的坐标是多少？"}'
agentcore invoke '{"prompt": "上海东方明珠的经纬度"}'
agentcore invoke '{"prompt": "深圳市民中心的地理位置"}'

# 坐标转地址
agentcore invoke '{"prompt": "坐标 116.397128, 39.916527 是什么地方？"}'
agentcore invoke '{"prompt": "经度 121.473701，纬度 31.230416 对应的地址"}'
```

### POI 搜索测试

```bash
# 餐饮搜索
agentcore invoke '{"prompt": "帮我搜索北京市朝阳区附近的咖啡馆"}'
agentcore invoke '{"prompt": "上海浦东新区有哪些好吃的火锅店？"}'
agentcore invoke '{"prompt": "深圳南山区的日料餐厅推荐"}'

# 酒店搜索
agentcore invoke '{"prompt": "找一下杭州西湖附近的五星级酒店"}'
agentcore invoke '{"prompt": "成都春熙路周边的商务酒店"}'

# 景点搜索
agentcore invoke '{"prompt": "广州有哪些著名景点？"}'
agentcore invoke '{"prompt": "南京夫子庙附近的旅游景点"}'

# 购物搜索
agentcore invoke '{"prompt": "北京国贸附近的购物中心"}'
agentcore invoke '{"prompt": "上海淮海路的商场有哪些？"}'
```

### 路线规划测试

```bash
# 驾车路线
agentcore invoke '{"prompt": "从北京西站到天安门怎么走？"}'
agentcore invoke '{"prompt": "从上海虹桥机场到外滩的驾车路线"}'
agentcore invoke '{"prompt": "深圳宝安机场到华强北开车要多久？"}'

# 公交路线
agentcore invoke '{"prompt": "杭州东站到西湖怎么坐公交？"}'
agentcore invoke '{"prompt": "成都双流机场到春熙路的地铁路线"}'

# 步行路线
agentcore invoke '{"prompt": "从广州塔步行到珠江新城要多久？"}'
agentcore invoke '{"prompt": "南京南站到夫子庙步行距离"}'

# 骑行路线
agentcore invoke '{"prompt": "从北京国贸骑车到三里屯多远？"}'
```

### 天气查询测试

```bash
# 实时天气
agentcore invoke '{"prompt": "北京今天天气怎么样？"}'
agentcore invoke '{"prompt": "上海现在的温度是多少？"}'
agentcore invoke '{"prompt": "深圳今天会下雨吗？"}'

# 天气预报
agentcore invoke '{"prompt": "杭州未来三天的天气预报"}'
agentcore invoke '{"prompt": "成都这周末天气如何？"}'
agentcore invoke '{"prompt": "广州明天适合出游吗？"}'

# 空气质量
agentcore invoke '{"prompt": "北京今天空气质量怎么样？"}'
agentcore invoke '{"prompt": "上海今天需要戴口罩吗？"}'
```

### 交通查询测试

```bash
# 实时路况
agentcore invoke '{"prompt": "北京三环现在堵车吗？"}'
agentcore invoke '{"prompt": "上海延安高架的实时路况"}'
agentcore invoke '{"prompt": "深圳北环大道现在车多吗？"}'
agentcore invoke '{"prompt": "杭州中河高架的交通情况"}'
```

### 网络搜索测试

```bash
# 技术搜索
agentcore invoke '{"prompt": "搜索一下 Python 最新版本"}'
agentcore invoke '{"prompt": "AWS Bedrock AgentCore 有什么功能？"}'
agentcore invoke '{"prompt": "什么是 MCP 协议？"}'

# 新闻搜索
agentcore invoke '{"prompt": "2024年人工智能最新进展"}'
agentcore invoke '{"prompt": "最近有什么科技新闻？"}'

# 知识搜索
agentcore invoke '{"prompt": "什么是 Strands Agent 框架？"}'
agentcore invoke '{"prompt": "如何部署 AI Agent 到生产环境？"}'
```

### 组合查询测试

```bash
# 天气 + 景点
agentcore invoke '{"prompt": "北京今天天气怎么样？适合去哪些景点？"}'

# 路线 + 路况
agentcore invoke '{"prompt": "从上海浦东机场到外滩怎么走？路上会堵车吗？"}'

# POI + 天气
agentcore invoke '{"prompt": "深圳南山区有哪些咖啡馆？今天天气适合出门吗？"}'

# 地理 + POI
agentcore invoke '{"prompt": "杭州西湖的坐标是多少？附近有什么好吃的？"}'

# 路线 + POI
agentcore invoke '{"prompt": "从成都东站到春熙路怎么走？那边有什么购物中心？"}'
```

### 实用场景测试

```bash
# 商务出行
agentcore invoke '{"prompt": "我在北京国贸，想找个附近的餐厅吃午饭"}'
agentcore invoke '{"prompt": "上海陆家嘴附近有会议室可以租吗？"}'

# 旅游规划
agentcore invoke '{"prompt": "杭州一日游路线推荐，包括西湖和灵隐寺"}'
agentcore invoke '{"prompt": "成都三天两夜旅游攻略"}'

# 交通出行
agentcore invoke '{"prompt": "从深圳湾口岸到香港机场怎么走最快？"}'
agentcore invoke '{"prompt": "广州南站到白云机场，开车还是坐地铁快？"}'

# 生活服务
agentcore invoke '{"prompt": "南京新街口附近有24小时便利店吗？"}'
agentcore invoke '{"prompt": "武汉光谷有哪些健身房？"}'
```

### 压力测试

```bash
# 连续查询
for i in {1..5}; do
  agentcore invoke '{"prompt": "北京今天天气怎么样？"}'
  sleep 2
done

# 复杂查询
agentcore invoke '{"prompt": "帮我规划一个北京一日游：早上去天安门，中午在附近吃饭，下午去故宫，晚上去王府井购物，每个地点之间的路线和时间都告诉我"}'
```

## 📊 监控和日志

### 查看状态

```bash
agentcore status
```

### 查看日志

```bash
# 获取日志命令
agentcore status | grep "aws logs tail"

# 查看最近日志
aws logs tail /aws/bedrock-agentcore/runtimes/AGENT_ID-DEFAULT \
  --log-stream-name-prefix "YYYY/MM/DD/[runtime-logs]" \
  --since 30m

# 实时日志
aws logs tail /aws/bedrock-agentcore/runtimes/AGENT_ID-DEFAULT \
  --log-stream-name-prefix "YYYY/MM/DD/[runtime-logs]" \
  --follow
```

### CloudWatch 仪表板

```bash
# 从 status 获取仪表板 URL
agentcore status
```

访问 GenAI Observability 仪表板查看：

- 请求追踪
- 工具调用
- 延迟分析
- 错误率

## 🔧 故障排查

### 错误：RuntimeClientError

**症状**：

```
An error occurred when starting the runtime
```

**原因**：环境变量未配置

**解决**：

```bash
# 1. 检查配置
cat .bedrock_agentcore.yaml | grep -A 5 "environment:"

# 2. 如果没有，添加环境变量
nano .bedrock_agentcore.yaml

# 3. 重新部署
agentcore launch
```

### 错误：工具加载失败

**症状**：只有 Tavily 搜索，没有百度地图

**解决**：

```bash
# 1. 验证 API Key
cat .bedrock_agentcore.yaml | grep BAIDU_MAPS_API_KEY

# 2. 查看日志
agentcore status | grep "aws logs tail"

# 3. 检查日志中的错误信息
```

### 错误：权限不足

**症状**：AccessDeniedException

**解决**：

```bash
# 检查 IAM 角色权限
cat .bedrock_agentcore.yaml | grep execution_role

# 确保角色有以下权限：
# - AmazonBedrockAgentCoreFullAccess
# - Bedrock 模型访问
# - CloudWatch Logs 写入
```

## 🧹 清理资源

```bash
agentcore destroy
```

这会删除：

- Runtime 端点
- ECR 仓库和镜像
- IAM 角色（如果自动创建）
- CloudWatch 日志组

## 📁 项目文件

```
.
├── agentcore_baidu_map_agent.py    # AgentCore 版本
├── test_agentcore_local.py         # 本地测试
├── deploy.sh                       # 自动部署脚本
├── requirements-agentcore.txt      # AgentCore 依赖
├── .bedrock_agentcore.yaml         # 配置文件（部署后生成）
└── README_AGENTCORE.md             # 本文档
```

## 🔄 代码差异

### 本地版本

```python
def main():
    agent = Agent(tools=[...])
    while True:
        user_input = input("...")
        response = agent(user_input)
```

### AgentCore 版本

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    agent = Agent(tools=[...])
    result = agent(payload.get("prompt"))
    return {"response": result}

if __name__ == "__main__":
    app.run()
```

## 📊 功能对比

| 功能         | 本地版本 | AgentCore 版本 |
| ------------ | -------- | -------------- |
| 百度地图工具 | ✅       | ✅             |
| Tavily 搜索  | ✅       | ✅             |
| 命令行交互   | ✅       | ❌             |
| HTTP API     | ❌       | ✅             |
| 自动扩展     | ❌       | ✅             |
| 监控追踪     | ❌       | ✅             |
| 生产就绪     | ❌       | ✅             |

## 💰 成本估算

- **Runtime**: 按请求数和执行时间
- **Bedrock**: 按 token 使用量
- **CloudWatch**: 按日志和指标量
- **X-Ray**: 按追踪数量

**优化建议**：

- 配置合适的超时时间
- 监控 API 调用次数
- 使用缓存减少重复调用

## 🎓 最佳实践

### 开发环境

1. 使用 `.env` 文件
2. 本地测试通过后再部署
3. 使用 `test_agentcore_local.py` 验证

### 测试环境

1. 使用 `.bedrock_agentcore.yaml` 配置
2. 启用 Observability
3. 监控日志和指标

### 生产环境

1. 使用 AWS Secrets Manager
2. 配置 IAM 权限最小化
3. 启用密钥轮换
4. 设置监控告警
5. 定期审查日志

## 📚 参考资源

- [AgentCore 官方文档](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Strands Agents 文档](https://strandsagents.com/)
- [百度地图 MCP](https://github.com/baidu-maps/mcp)
- [AgentCore Starter Toolkit](https://github.com/aws/bedrock-agentcore-starter-toolkit)

## 🆘 获取帮助

1. 查看日志：`agentcore status`
2. 检查配置：`cat .bedrock_agentcore.yaml`
3. 本地测试：`python test_agentcore_local.py`
4. 查看 AWS 服务状态：https://status.aws.amazon.com/

---

**提示**：部署前确保在 `.bedrock_agentcore.yaml` 中配置了环境变量！
