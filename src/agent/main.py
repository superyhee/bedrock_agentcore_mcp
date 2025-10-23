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

import logging
from typing import Dict, Any, List
from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

from src.config import MEMORY_ID, REGION, MODEL_ID
from src.tools.baidu_maps import initialize_baidu_mcp_client
from src.tools.tavily_search import tavily_search
from src.utils.memory import (
    get_actor_and_session_id,
    create_memory_config,
    build_context_aware_prompt,
    get_conversation_context
)
from src.utils.prompts import SYSTEM_PROMPT

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 AgentCore App
app = BedrockAgentCoreApp()


def _get_mcp_client():
    """获取 MCP 客户端实例
    
    Returns:
        MCPClient 实例或 None
    """
    try:
        return initialize_baidu_mcp_client()
    except Exception as e:
        logger.warning(f"Failed to initialize Baidu MCP client: {e}")
        return None


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
        actor_id, session_id = get_actor_and_session_id(context)
        logger.info(f"Processing request for actor: {actor_id}, session: {session_id}")
        
        # 配置 Memory
        memory_config = create_memory_config(MEMORY_ID, actor_id, session_id)
        
        # 创建会话管理器
        session_manager = AgentCoreMemorySessionManager(memory_config, REGION)
        
        # 获取对话历史（短期记忆）
        conversation_history = []
        if use_conversation_history:
            conversation_history = await get_conversation_context(session_manager, max_turns=10)
        
        # 如果有对话历史，增强提示词
        enhanced_prompt = prompt
        if conversation_history:
            enhanced_prompt = build_context_aware_prompt(prompt, conversation_history)
            logger.info("Enhanced prompt with conversation history")
        
        # 获取 MCP 客户端
        mcp_client = _get_mcp_client()
        
        # 准备基础工具
        tools = [tavily_search]
        
        # 如果有 MCP 客户端，在其上下文中运行 Agent
        if mcp_client:
            with mcp_client:
                # 在 MCP 上下文中加载百度地图工具
                baidu_map_tools = mcp_client.list_tools_sync()
                tools.extend(baidu_map_tools)
                logger.info(f"Loaded {len(baidu_map_tools)} Baidu Maps tools")
                
                # 创建 Agent（在 MCP 上下文中）
                agent = Agent(
                    model=MODEL_ID,
                    session_manager=session_manager,
                    system_prompt=SYSTEM_PROMPT,
                    tools=tools
                )
                
                # 流式输出
                stream = agent.stream_async(enhanced_prompt)
                
                async for event in stream:
                    if isinstance(event, dict) and 'event' in event:
                        event_data = event['event']
                        if 'contentBlockDelta' in event_data:
                            yield {"event": event_data}
        else:
            # 没有 MCP 客户端，只使用 Tavily 搜索
            logger.info("Running without Baidu Maps tools")
            agent = Agent(
                model=MODEL_ID,
                session_manager=session_manager,
                system_prompt=SYSTEM_PROMPT,
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
