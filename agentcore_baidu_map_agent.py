"""
百度地图 + Tavily 搜索 Agent - AgentCore 流式输出版本
使用 Strands Agent 框架集成百度地图 MCP Server 和 Tavily API
部署到 AWS Bedrock AgentCore

特性：
- 流式响应输出 (Streaming Response)
- 实时返回 Agent 执行过程中的事件
- 支持百度地图 MCP 工具和 Tavily 搜索
- 集成 AgentCore Memory 进行会话管理
"""

import os
import logging
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from mcp.client.sse import sse_client
from strands import Agent, tool
from strands.tools.mcp import MCPClient
import requests
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载 .env 文件（仅用于本地测试）
load_dotenv()

# 初始化 AgentCore App
app = BedrockAgentCoreApp()

# 配置常量
MEMORY_ID = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")
REGION = os.getenv("AWS_REGION", "us-west-2")
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
BAIDU_API_KEY = os.getenv("BAIDU_MAPS_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_API_URL = "https://api.tavily.com/search"
REQUEST_TIMEOUT = 30

# 验证环境变量
if not BAIDU_API_KEY:
    logger.warning("BAIDU_MAPS_API_KEY not set. Baidu Maps features will be unavailable.")
if not TAVILY_API_KEY:
    logger.warning("TAVILY_API_KEY not set. Tavily search features will be unavailable.")


def _format_search_results(query: str, data: Dict[str, Any]) -> str:
    """格式化搜索结果为可读文本"""
    results_text = f"搜索查询: {query}\n\n"
    
    if data.get("answer"):
        results_text += f"答案摘要:\n{data['answer']}\n\n"
    
    results_text += "搜索结果:\n"
    for i, result in enumerate(data.get("results", []), 1):
        results_text += f"\n{i}. {result.get('title', '无标题')}\n"
        results_text += f"   URL: {result.get('url', '')}\n"
        results_text += f"   内容: {result.get('content', '')}\n"
    
    return results_text


@tool
def get_conversation_summary(topic: str = "") -> Dict[str, Any]:
    """获取对话历史摘要
    
    Args:
        topic: 可选的主题过滤，如"位置"、"搜索"等
    
    Returns:
        对话历史摘要
    """
    # 注意：这个工具需要在运行时访问 session_manager
    # 实际实现会在 Agent 创建时动态注入
    return {
        "status": "info",
        "content": [{"text": "此工具用于查询对话历史，需要在 Agent 运行时使用"}]
    }


@tool
def tavily_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """使用 Tavily API 搜索网络信息
    
    Args:
        query: 搜索查询关键词
        max_results: 返回的最大结果数量，默认为5
    
    Returns:
        包含搜索结果的字典
    """
    if not TAVILY_API_KEY:
        logger.error("TAVILY_API_KEY not configured")
        return {
            "status": "error",
            "content": [{"text": "错误：未设置 TAVILY_API_KEY 环境变量"}]
        }
    
    try:
        response = requests.post(
            TAVILY_API_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "include_answer": True,
                "include_raw_content": False
            },
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        results_text = _format_search_results(query, data)
        
        return {
            "status": "success",
            "content": [
                {"text": results_text},
                {"json": data}
            ]
        }
        
    except requests.exceptions.Timeout:
        logger.error(f"Tavily search timeout for query: {query}")
        return {
            "status": "error",
            "content": [{"text": "搜索请求超时，请稍后重试"}]
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Tavily search request failed: {e}")
        return {
            "status": "error",
            "content": [{"text": f"搜索请求失败: {str(e)}"}]
        }
    except Exception as e:
        logger.exception(f"Unexpected error in tavily_search: {e}")
        return {
            "status": "error",
            "content": [{"text": f"发生错误: {str(e)}"}]
        }


def initialize_baidu_mcp_client() -> Optional[MCPClient]:
    """初始化百度地图 MCP 客户端
    
    Returns:
        MCPClient 实例或 None（如果初始化失败）
    """
    if not BAIDU_API_KEY:
        logger.warning("BAIDU_MAPS_API_KEY not set, Baidu Maps features unavailable")
        return None
    
    try:
        baidu_map_sse_url = f"https://mcp.map.baidu.com/sse?ak={BAIDU_API_KEY}"
        return MCPClient(lambda: sse_client(baidu_map_sse_url))
    except Exception as e:
        logger.error(f"Failed to initialize Baidu MCP client: {e}")
        return None


def _get_actor_and_session_id(context) -> tuple[str, str]:
    """从上下文中提取 actor_id 和 session_id
    
    Args:
        context: AgentCore 运行时上下文
    
    Returns:
        (actor_id, session_id) 元组
    """
    actor_id = 'user'
    if hasattr(context, 'headers'):
        actor_id = context.headers.get(
            'X-Amzn-Bedrock-AgentCore-Runtime-Custom-Actor-Id',
            'user'
        )
    
    session_id = getattr(context, 'session_id', 'default')
    return actor_id, session_id


def _create_memory_config(actor_id: str, session_id: str) -> AgentCoreMemoryConfig:
    """创建 Memory 配置
    
    Args:
        actor_id: 用户标识
        session_id: 会话标识
    
    Returns:
        AgentCoreMemoryConfig 实例
    """
    return AgentCoreMemoryConfig(
        memory_id=MEMORY_ID,
        session_id=session_id,
        actor_id=actor_id,
        retrieval_config={
            f"/users/{actor_id}/facts": RetrievalConfig(top_k=5, relevance_score=0.5),
            f"/users/{actor_id}/preferences": RetrievalConfig(top_k=3, relevance_score=0.5),
            f"/users/{actor_id}/locations": RetrievalConfig(top_k=5, relevance_score=0.5)
        }
    )


def _load_tools() -> List:
    """加载所有可用的工具
    
    Returns:
        工具列表
    """
    tools = [tavily_search]
    
    try:
        mcp_client = initialize_baidu_mcp_client()
        if mcp_client:
            with mcp_client:
                baidu_map_tools = mcp_client.list_tools_sync()
                tools.extend(baidu_map_tools)
                logger.info(f"Loaded {len(baidu_map_tools)} Baidu Maps tools")
    except Exception as e:
        logger.warning(f"Failed to load Baidu Maps tools: {e}")
        logger.info("Continuing with Tavily search only")
    
    return tools


def _build_context_aware_prompt(prompt: str, conversation_history: List[Dict[str, Any]]) -> str:
    """构建包含对话历史的上下文感知提示
    
    Args:
        prompt: 用户当前输入
        conversation_history: 最近的对话历史
    
    Returns:
        增强后的提示词
    """
    if not conversation_history:
        return prompt
    
    # 构建对话历史摘要
    history_text = "\n\n[对话历史]:\n"
    for i, turn in enumerate(conversation_history[-5:], 1):  # 只使用最近5轮对话
        role = turn.get('role', 'unknown')
        content = turn.get('content', '')
        history_text += f"{i}. {role}: {content[:200]}...\n" if len(content) > 200 else f"{i}. {role}: {content}\n"
    
    history_text += "\n[当前问题]:\n"
    
    return history_text + prompt


async def _get_conversation_context(session_manager, max_turns: int = 10) -> List[Dict[str, Any]]:
    """获取对话历史上下文
    
    Args:
        session_manager: AgentCore Memory 会话管理器
        max_turns: 获取的最大对话轮数
    
    Returns:
        对话历史列表
    """
    try:
        # 获取最近的对话历史
        turns = session_manager.get_last_k_turns(k=max_turns)
        
        conversation_history = []
        for turn in turns:
            # 提取角色和内容
            role = turn.get('role', 'unknown')
            content = turn.get('content', '')
            
            if isinstance(content, list):
                # 如果内容是列表，提取文本
                text_content = ' '.join([
                    item.get('text', '') for item in content 
                    if isinstance(item, dict) and 'text' in item
                ])
                content = text_content
            
            conversation_history.append({
                'role': role,
                'content': content
            })
        
        logger.info(f"Retrieved {len(conversation_history)} conversation turns")
        return conversation_history
        
    except Exception as e:
        logger.warning(f"Failed to retrieve conversation history: {e}")
        return []


@app.entrypoint
async def invoke(payload: Dict[str, Any], context):
    """
    AgentCore 入口函数 - 流式输出版本（支持短期记忆）
    
    Args:
        payload: 包含 prompt 的请求负载
        context: AgentCore 运行时上下文
    
    Yields:
        流式响应事件
    """
    # 验证 Memory 配置
    if not MEMORY_ID:
        logger.error("Memory not configured")
        yield {"error": "Memory not configured. Please run 'agentcore configure' first."}
        return
    
    # 验证输入
    prompt = payload.get("prompt", "").strip()
    if not prompt:
        logger.warning("Empty prompt received")
        yield {"error": "No prompt provided"}
        return
    
    # 是否启用对话历史增强（默认启用）
    use_conversation_history = payload.get("use_history", True)
    
    try:
        # 获取用户和会话信息
        actor_id, session_id = _get_actor_and_session_id(context)
        logger.info(f"Processing request for actor: {actor_id}, session: {session_id}")
        
        # 配置 Memory
        memory_config = _create_memory_config(actor_id, session_id)
        
        # 创建会话管理器
        session_manager = AgentCoreMemorySessionManager(memory_config, REGION)
        
        # 获取对话历史（短期记忆）
        conversation_history = []
        if use_conversation_history:
            conversation_history = await _get_conversation_context(session_manager, max_turns=10)
        
        # 加载工具
        tools = _load_tools()
        
        # 构建系统提示（包含记忆能力说明）
        system_prompt = """你是一个智能助手，集成了百度地图服务和网络搜索功能。

你可以帮助用户：
1. 查询地理位置信息（地址转坐标、坐标转地址）
2. 搜索地点和 POI（餐厅、酒店、景点等）
3. 规划路线（驾车、步行、骑行、公交）
4. 查询天气和交通信息
5. 进行网络搜索获取最新信息

重要能力：
- 你可以记住之前的对话内容，理解上下文和指代关系
- 当用户说"那里"、"刚才那个地方"、"上次提到的"等时，请参考对话历史
- 如果用户的问题依赖之前的对话，请结合历史信息给出准确回答

请根据用户的问题选择合适的工具，并提供清晰、有用的回答。
对于地理位置相关的问题，优先使用百度地图工具。
对于一般信息查询，使用 Tavily 搜索工具。"""
        
        # 如果有对话历史，增强提示词
        enhanced_prompt = prompt
        if conversation_history:
            enhanced_prompt = _build_context_aware_prompt(prompt, conversation_history)
            logger.info("Enhanced prompt with conversation history")
        
        # 创建 Agent
        agent = Agent(
            model=MODEL_ID,
            session_manager=session_manager,
            system_prompt=system_prompt,
            tools=tools
        )
        
        # 流式输出
        stream = agent.stream_async(enhanced_prompt)
        
        async for event in stream:
            if isinstance(event, dict) and 'event' in event:
                event_data = event['event']
                if 'contentBlockDelta' in event_data:
                    yield {"event": event_data}
        
        logger.info("Request completed successfully")
        
    except Exception as e:
        logger.exception(f"Agent execution failed: {e}")
        yield {"error": f"Agent execution failed: {str(e)}"}


if __name__ == "__main__":
    # 运行 AgentCore Runtime
    app.run()
